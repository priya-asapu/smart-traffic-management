from pydantic import BaseModel
from typing import Optional


# ---------------- USERS ----------------

class UserCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    role: str = "user"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    role: str

    class Config:
        from_attributes = True


# ---------------- TRAFFIC ----------------

class TrafficCreate(BaseModel):
    location: str
    traffic_level: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class TrafficResponse(BaseModel):
    id: int
    location: str
    traffic_level: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True


# ---------------- REPORTS / HAZARDS ----------------

class ReportCreate(BaseModel):
    user_id: Optional[int] = None
    report_type: str
    description: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_url: Optional[str] = None


class ReportResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    report_type: str
    description: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_url: Optional[str] = None
    status: str

    class Config:
        from_attributes = True


# ---------------- EMERGENCIES ----------------

class EmergencyCreate(BaseModel):
    user_id: Optional[int] = None
    emergency_type: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    severity: Optional[str] = None


class EmergencyResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    emergency_type: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    severity: Optional[str] = None
    status: str

    class Config:
        from_attributes = True


# ---------------- EMERGENCY SERVICES ----------------

class EmergencyServiceCreate(BaseModel):
    service_type: str
    location: Optional[str] = None
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class EmergencyServiceResponse(BaseModel):
    id: int
    service_type: str
    location: Optional[str] = None
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True


# ---------------- NOTIFICATIONS ----------------

class NotificationCreate(BaseModel):
    user_id: Optional[int] = None
    title: str
    message: str


class NotificationResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    title: str
    message: str
    is_read: bool

    class Config:
        from_attributes = True