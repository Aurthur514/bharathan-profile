from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import json

class CameraBase(SQLModel):
    name: str = Field(index=True)
    rtsp_url: str
    location: Optional[str] = None
    status: str = "offline"
    zone_config: Optional[str] = None # JSON string for now

class Camera(CameraBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    events: List["Event"] = Relationship(back_populates="camera")

class EventBase(SQLModel):
    camera_id: int = Field(foreign_key="camera.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    rule_name: str
    object_type: str
    confidence: float
    snapshot_path: Optional[str] = None

class Event(EventBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    camera: Optional[Camera] = Relationship(back_populates="events")

class CameraCreate(CameraBase):
    pass

class CameraRead(CameraBase):
    id: int

class EventRead(EventBase):
    id: int
