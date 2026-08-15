from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base


# ---------------- USERS ----------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    role = Column(String, default="user")


# ---------------- TRAFFIC ----------------

class TrafficReport(Base):
    __tablename__ = "traffic_reports"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    traffic_level = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)


# ---------------- REPORTS / HAZARDS ----------------

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    report_type = Column(String, nullable=False)
    description = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    image_url = Column(String)
    status = Column(String, default="pending")


# ---------------- EMERGENCIES ----------------

class Emergency(Base):
    __tablename__ = "emergencies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    emergency_type = Column(String, nullable=False)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    severity = Column(String)
    status = Column(String, default="pending")


# ---------------- EMERGENCY SERVICES ----------------

class EmergencyService(Base):
    __tablename__ = "emergency_services"

    id = Column(Integer, primary_key=True, index=True)
    service_type = Column(String, nullable=False)
    location = Column(String)
    phone = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)


# ---------------- NOTIFICATIONS ----------------

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)