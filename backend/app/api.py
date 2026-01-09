from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlmodel import Session, select
from typing import List, Optional
from .database import get_session
from .models import Camera, CameraCreate, CameraRead, Event, EventRead
from .engine import get_latest_frame

router = APIRouter()

@router.post("/cameras", response_model=CameraRead)
def create_camera(camera: CameraCreate, session: Session = Depends(get_session)):
    db_camera = Camera.model_validate(camera)
    session.add(db_camera)
    session.commit()
    session.refresh(db_camera)
    return db_camera

@router.get("/cameras", response_model=List[CameraRead])
def read_cameras(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    cameras = session.exec(select(Camera).offset(offset).limit(limit)).all()
    return cameras

@router.get("/cameras/{camera_id}", response_model=CameraRead)
def read_camera(camera_id: int, session: Session = Depends(get_session)):
    camera = session.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera

@router.get("/cameras/{camera_id}/stream")
def get_camera_stream(camera_id: int):
    frame_bytes = get_latest_frame(camera_id)
    if not frame_bytes:
        # Return a placeholder image or 404
        return Response(status_code=404)
    return Response(content=frame_bytes, media_type="image/jpeg")

@router.get("/events", response_model=List[EventRead])
def read_events(
    camera_id: Optional[int] = None,
    rule: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    query = select(Event)
    if camera_id:
        query = query.where(Event.camera_id == camera_id)
    if rule:
        query = query.where(Event.rule_name == rule)

    query = query.order_by(Event.timestamp.desc()).offset(offset).limit(limit)
    events = session.exec(query).all()
    return events

@router.get("/events/{event_id}", response_model=EventRead)
def read_event(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
