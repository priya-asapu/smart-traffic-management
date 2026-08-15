from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import (
    User,
    TrafficReport,
    Report,
    Emergency,
    EmergencyService,
    Notification
)

from schemas import (
    UserCreate,
    UserResponse,
    TrafficCreate,
    TrafficResponse,
    ReportCreate,
    ReportResponse,
    EmergencyCreate,
    EmergencyResponse,
    EmergencyServiceCreate,
    EmergencyServiceResponse,
    NotificationCreate,
    NotificationResponse
)


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Smart Traffic Management System",
    version="1.0.0"
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "Smart Traffic Management System API is running"
    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# =========================================================
# ROUTE
# =========================================================

@app.post("/route")
def get_route(data: dict):
    source = data.get("source")
    destination = data.get("destination")

    if not source or not destination:
        raise HTTPException(
            status_code=400,
            detail="source and destination are required"
        )

    return {
        "source": source,
        "destination": destination,
        "message": f"Route calculated from {source} to {destination}"
    }


# =========================================================
# USERS
# =========================================================

@app.post("/users/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    db_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.get("/users", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# =========================================================
# TRAFFIC
# =========================================================

@app.get("/traffic", response_model=list[TrafficResponse])
def get_traffic(
    db: Session = Depends(get_db)
):
    return db.query(TrafficReport).all()


@app.post("/traffic", response_model=TrafficResponse)
def create_traffic(
    traffic: TrafficCreate,
    db: Session = Depends(get_db)
):
    db_traffic = TrafficReport(
        location=traffic.location,
        traffic_level=traffic.traffic_level,
        latitude=traffic.latitude,
        longitude=traffic.longitude
    )

    db.add(db_traffic)
    db.commit()
    db.refresh(db_traffic)

    return db_traffic


@app.get("/traffic/{traffic_id}", response_model=TrafficResponse)
def get_traffic_by_id(
    traffic_id: int,
    db: Session = Depends(get_db)
):
    traffic = db.query(TrafficReport).filter(
        TrafficReport.id == traffic_id
    ).first()

    if not traffic:
        raise HTTPException(
            status_code=404,
            detail="Traffic report not found"
        )

    return traffic


@app.put("/traffic/{traffic_id}", response_model=TrafficResponse)
def update_traffic(
    traffic_id: int,
    traffic: TrafficCreate,
    db: Session = Depends(get_db)
):
    db_traffic = db.query(TrafficReport).filter(
        TrafficReport.id == traffic_id
    ).first()

    if not db_traffic:
        raise HTTPException(
            status_code=404,
            detail="Traffic report not found"
        )

    db_traffic.location = traffic.location
    db_traffic.traffic_level = traffic.traffic_level
    db_traffic.latitude = traffic.latitude
    db_traffic.longitude = traffic.longitude

    db.commit()
    db.refresh(db_traffic)

    return db_traffic


# =========================================================
# REPORTS / HAZARDS
# =========================================================

@app.get("/reports", response_model=list[ReportResponse])
def get_reports(
    db: Session = Depends(get_db)
):
    return db.query(Report).all()


@app.post("/reports", response_model=ReportResponse)
def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):
    db_report = Report(
        user_id=report.user_id,
        report_type=report.report_type,
        description=report.description,
        location=report.location,
        latitude=report.latitude,
        longitude=report.longitude,
        image_url=report.image_url
    )

    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return db_report


@app.get("/reports/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    report = db.query(Report).filter(
        Report.id == report_id
    ).first()

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return report


@app.put("/reports/{report_id}", response_model=ReportResponse)
def update_report(
    report_id: int,
    report: ReportCreate,
    db: Session = Depends(get_db)
):
    db_report = db.query(Report).filter(
        Report.id == report_id
    ).first()

    if not db_report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    db_report.user_id = report.user_id
    db_report.report_type = report.report_type
    db_report.description = report.description
    db_report.location = report.location
    db_report.latitude = report.latitude
    db_report.longitude = report.longitude
    db_report.image_url = report.image_url

    db.commit()
    db.refresh(db_report)

    return db_report


# =========================================================
# EMERGENCIES
# =========================================================

@app.get("/emergencies", response_model=list[EmergencyResponse])
def get_emergencies(
    db: Session = Depends(get_db)
):
    return db.query(Emergency).all()


@app.post("/emergencies", response_model=EmergencyResponse)
def create_emergency(
    emergency: EmergencyCreate,
    db: Session = Depends(get_db)
):
    db_emergency = Emergency(
        user_id=emergency.user_id,
        emergency_type=emergency.emergency_type,
        location=emergency.location,
        latitude=emergency.latitude,
        longitude=emergency.longitude,
        severity=emergency.severity
    )

    db.add(db_emergency)
    db.commit()
    db.refresh(db_emergency)

    return db_emergency


@app.get("/emergencies/{emergency_id}", response_model=EmergencyResponse)
def get_emergency(
    emergency_id: int,
    db: Session = Depends(get_db)
):
    emergency = db.query(Emergency).filter(
        Emergency.id == emergency_id
    ).first()

    if not emergency:
        raise HTTPException(
            status_code=404,
            detail="Emergency not found"
        )

    return emergency


@app.put("/emergencies/{emergency_id}", response_model=EmergencyResponse)
def update_emergency(
    emergency_id: int,
    emergency: EmergencyCreate,
    db: Session = Depends(get_db)
):
    db_emergency = db.query(Emergency).filter(
        Emergency.id == emergency_id
    ).first()

    if not db_emergency:
        raise HTTPException(
            status_code=404,
            detail="Emergency not found"
        )

    db_emergency.user_id = emergency.user_id
    db_emergency.emergency_type = emergency.emergency_type
    db_emergency.location = emergency.location
    db_emergency.latitude = emergency.latitude
    db_emergency.longitude = emergency.longitude
    db_emergency.severity = emergency.severity

    db.commit()
    db.refresh(db_emergency)

    return db_emergency


# =========================================================
# EMERGENCY SERVICES
# =========================================================

@app.get(
    "/emergency-services",
    response_model=list[EmergencyServiceResponse]
)
def get_emergency_services(
    db: Session = Depends(get_db)
):
    return db.query(EmergencyService).all()


@app.post(
    "/emergency-services",
    response_model=EmergencyServiceResponse
)
def create_emergency_service(
    service: EmergencyServiceCreate,
    db: Session = Depends(get_db)
):
    db_service = EmergencyService(
        service_type=service.service_type,
        location=service.location,
        phone=service.phone,
        latitude=service.latitude,
        longitude=service.longitude
    )

    db.add(db_service)

    try:
        db.commit()
        db.refresh(db_service)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    return db_service


@app.get(
    "/emergency-services/{service_id}",
    response_model=EmergencyServiceResponse
)
def get_emergency_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    service = db.query(EmergencyService).filter(
        EmergencyService.id == service_id
    ).first()

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Emergency service not found"
        )

    return service


# =========================================================
# NOTIFICATIONS
# =========================================================

@app.get(
    "/notifications",
    response_model=list[NotificationResponse]
)
def get_notifications(
    db: Session = Depends(get_db)
):
    return db.query(Notification).all()


@app.post(
    "/notifications",
    response_model=NotificationResponse
)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):
    db_notification = Notification(
        user_id=notification.user_id,
        title=notification.title,
        message=notification.message
    )

    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return db_notification


@app.get(
    "/notifications/{notification_id}",
    response_model=NotificationResponse
)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return notification


@app.put(
    "/notifications/{notification_id}/read",
    response_model=NotificationResponse
)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification