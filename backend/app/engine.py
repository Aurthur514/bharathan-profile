import asyncio
import cv2
import time
import os
from sqlmodel import Session, select
from app.database import engine
from app.models import Camera, Event
from app.services.ingestion import CameraManager
from app.services.inference import InferenceEngine
from app.services.rules import RuleEngine
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state to manage running cameras
active_cameras = {}
latest_frames = {} # camera_id -> jpeg_bytes
should_stop = False

class Engine:
    def __init__(self):
        self.inference = InferenceEngine()
        self.rules = RuleEngine()
        self.snapshot_dir = "snapshots"
        self.executor = ThreadPoolExecutor(max_workers=2) # Offload inference
        if not os.path.exists(self.snapshot_dir):
            os.makedirs(self.snapshot_dir)

    async def run(self):
        global should_stop
        logger.info("Engine started.")
        while not should_stop:
            with Session(engine) as session:
                cameras = session.exec(select(Camera)).all()

                # Sync active_cameras with DB
                db_cam_ids = {c.id for c in cameras}
                for cam_id in list(active_cameras.keys()):
                    if cam_id not in db_cam_ids:
                        active_cameras[cam_id].release()
                        del active_cameras[cam_id]
                        if cam_id in latest_frames:
                            del latest_frames[cam_id]

                for camera in cameras:
                    if camera.id not in active_cameras:
                        active_cameras[camera.id] = CameraManager(camera.rtsp_url)

                    cam_manager = active_cameras[camera.id]
                    success, frame = cam_manager.get_frame()

                    if success and frame is not None:
                        # Update status
                        if camera.status != "online":
                            camera.status = "online"
                            session.add(camera)
                            session.commit()

                        # Store latest frame for Live View
                        ret, buffer = cv2.imencode('.jpg', frame)
                        if ret:
                            latest_frames[camera.id] = buffer.tobytes()

                        # Offload inference to thread
                        loop = asyncio.get_running_loop()
                        results = await loop.run_in_executor(self.executor, self.inference.infer, frame)

                        # Rule Check
                        if camera.zone_config:
                            # Check Intrusion
                            intrusion_events = self.rules.check_intrusion(results, camera.zone_config)
                            # Check Loitering
                            loitering_events = self.rules.check_loitering(results, camera.zone_config, camera.id)

                            all_events = intrusion_events + loitering_events

                            for evt_data in all_events:
                                # Simple deduplication logic:
                                # if same rule/zone triggered in last 5 seconds, ignore.
                                # (Omitted for MVP simplicity, but good to note)

                                # Save Snapshot
                                filename = f"{self.snapshot_dir}/{camera.id}_{int(time.time())}_{evt_data['rule_name']}.jpg"
                                cv2.imwrite(filename, frame)

                                event = Event(
                                    camera_id=camera.id,
                                    rule_name=evt_data["rule_name"],
                                    object_type=evt_data["object_type"],
                                    confidence=evt_data["confidence"],
                                    snapshot_path=filename
                                )
                                session.add(event)
                                session.commit()
                                logger.info(f"Event detected: {evt_data}")

                    else:
                        if camera.status != "offline":
                            camera.status = "offline"
                            session.add(camera)
                            session.commit()

            await asyncio.sleep(0.01) # Yield control

engine_instance = Engine()

def start_engine():
    return asyncio.create_task(engine_instance.run())

def stop_engine():
    global should_stop
    should_stop = True
    engine_instance.executor.shutdown(wait=False)

def get_latest_frame(camera_id: int):
    return latest_frames.get(camera_id)
