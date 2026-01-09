from shapely.geometry import Point, Polygon
import json
import time
from typing import List, Dict

class RuleEngine:
    def __init__(self):
        # Track object enter times for loitering: {zone_name: {track_id: start_time}}
        # Note: Since we don't have robust tracking IDs in basic YOLO,
        # we will simulate it or use basic intersection if tracking is not available.
        # For this MVP without tracking, we can't perfectly track "same person",
        # but we can check if *any* person has been in the zone for N frames/seconds
        # if the zone is continuously occupied. This is a simplification.
        self.zone_occupancy = {}

    def check_intrusion(self, detections, zone_config: str) -> List[Dict]:
        """
        Check if any detected person is inside the defined zones.
        """
        events = []
        if not zone_config:
            return events

        try:
            zones = json.loads(zone_config)
        except json.JSONDecodeError:
            return events

        for det in detections.boxes:
            if int(det.cls) == 0: # person
                box = det.xyxy[0].cpu().numpy()
                center_x = (box[0] + box[2]) / 2
                center_y = (box[1] + box[3]) / 2
                point = Point(center_x, center_y)

                for zone in zones:
                    if "points" in zone:
                        poly = Polygon(zone["points"])
                        if poly.contains(point):
                            events.append({
                                "rule_name": "Intrusion",
                                "object_type": "person",
                                "confidence": float(det.conf),
                                "zone_name": zone.get("name", "Unknown")
                            })
        return events

    def check_loitering(self, detections, zone_config: str, camera_id: int) -> List[Dict]:
        """
        Check if a zone has been occupied for > 5 seconds.
        """
        events = []
        if not zone_config:
            return events

        try:
            zones = json.loads(zone_config)
        except json.JSONDecodeError:
            return events

        # Identify currently occupied zones
        occupied_zones = set()

        for det in detections.boxes:
            if int(det.cls) == 0: # person
                box = det.xyxy[0].cpu().numpy()
                point = Point((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
                for zone in zones:
                    if "points" in zone:
                        poly = Polygon(zone["points"])
                        if poly.contains(point):
                            occupied_zones.add(zone.get("name", "Unknown"))

        # Initialize state for this camera if needed
        if camera_id not in self.zone_occupancy:
            self.zone_occupancy[camera_id] = {}

        current_time = time.time()

        # Update occupancy timers
        for zone_name in occupied_zones:
            if zone_name not in self.zone_occupancy[camera_id]:
                self.zone_occupancy[camera_id][zone_name] = current_time
            elif current_time - self.zone_occupancy[camera_id][zone_name] > 5: # 5 seconds threshold
                # Only trigger once per "session" or throttle?
                # For MVP, we'll let the engine handle throttling/deduping
                events.append({
                    "rule_name": "Loitering",
                    "object_type": "person",
                    "confidence": 1.0, # derived
                    "zone_name": zone_name
                })

        # Reset empty zones
        active_zones = list(self.zone_occupancy[camera_id].keys())
        for z in active_zones:
            if z not in occupied_zones:
                del self.zone_occupancy[camera_id][z]

        return events
