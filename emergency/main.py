import os
import sqlite3
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from math import radians, sin, cos, sqrt, atan2
from ultralytics import YOLO
app = FastAPI()
DATABASE = "emergency.db"
def init_database():
 
    connection = sqlite3.connect(DATABASE)
 
    cursor = connection.cursor()
 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emergencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emergency_id TEXT,
            latitude REAL,
            longitude REAL,
            severity TEXT,
            hazard_type TEXT,
            status TEXT,
            ambulance_id TEXT,
            hospital_id TEXT,
            route_status TEXT,
            created_at TEXT
        )
    """)
 
    connection.commit()
 
    connection.close()
init_database()
def save_emergency(
    emergency_id,
    latitude,
    longitude,
    severity,
    hazard_type,
    status,
    ambulance_id,
    hospital_id,
    route_status
):
 
    connection = sqlite3.connect(DATABASE)
 
    cursor = connection.cursor()
 
    cursor.execute("""
        INSERT INTO emergencies (
            emergency_id,
            latitude,
            longitude,
            severity,
            hazard_type,
            status,
            ambulance_id,
            hospital_id,
            route_status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        emergency_id,
        latitude,
        longitude,
        severity,
        hazard_type,
        status,
        ambulance_id,
        hospital_id,
        route_status,
        datetime.now().isoformat()
    ))
 
    connection.commit()
 
    connection.close()
model = YOLO("yolo11n.pt")
UPLOAD_FOLDER = "uploads"
 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def calculate_distance(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float
):
    earth_radius = 6371
 
    lat1 = radians(latitude1)
    lat2 = radians(latitude2)
 
    difference_latitude = radians(latitude2 - latitude1)
    difference_longitude = radians(longitude2 - longitude1)
 
    a = (
        sin(difference_latitude / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(difference_longitude / 2) ** 2
    )
 
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
 
    distance = earth_radius * c
 
    return round(distance, 2)
class EmergencyType(str, Enum):
    ambulance = "ambulance"
    police = "police"
    fire = "fire"
    other = "other"
class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"
 
app = FastAPI(
    title="Smart AI Traffic Management - Emergency Service",
    description="Emergency and Smart Response API",
    version="1.0.0"
)
 
 
class EmergencyRequest(BaseModel):
    emergency_type: EmergencyType
    latitude: float
    longitude: float
    description: str
    severity: Severity
 
 
emergency_counter = 0
emergencies = {}
emergency_services = [
    {
        "service_id": "AMB-001",
        "service_type": "ambulance",
        "name": "Amalapuram Ambulance 1",
        "latitude": 16.5830,
        "longitude": 82.0055,
        "available": True
    },
    {
        "service_id": "AMB-002",
        "service_type": "ambulance",
        "name": "Amalapuram Ambulance 2",
        "latitude": 16.5900,
        "longitude": 82.0150,
        "available": True
    },
    {
        "service_id": "POL-001",
        "service_type": "police",
        "name": "Amalapuram Police Unit 1",
        "latitude": 16.5800,
        "longitude": 82.0000,
        "available": True
    },
    {
        "service_id": "FIR-001",
        "service_type": "fire",
        "name": "Amalapuram Fire Service 1",
        "latitude": 16.5750,
        "longitude": 82.0100,
        "available": True
    }
]
hospitals = [
    {
        "hospital_id": "HOS-001",
        "name": "Amalapuram General Hospital",
        "latitude": 16.5850,
        "longitude": 82.0080,
        "available": True,
        "emergency_support": True,
        "trauma_support": False
    },
    {
        "hospital_id": "HOS-002",
        "name": "Amalapuram Trauma Care Hospital",
        "latitude": 16.5750,
        "longitude": 82.0120,
        "available": True,
        "emergency_support": True,
        "trauma_support": True
    },
    {
        "hospital_id": "HOS-003",
        "name": "Amalapuram City Hospital",
        "latitude": 16.5950,
        "longitude": 82.0200,
        "available": True,
        "emergency_support": True,
        "trauma_support": False
    }
]
def analyze_hazard_image(filename: str):
 
    filename_lower = filename.lower()
 
    # Temporary prototype detection
    # This will be replaced by a real computer-vision model later.
 
    if "accident" in filename_lower:
        return {
            "detected": True,
            "hazard_type": "accident",
            "confidence": 0.90,
            "severity": "high"
        }
 
    elif "fire" in filename_lower:
        return {
            "detected": True,
            "hazard_type": "fire",
            "confidence": 0.90,
            "severity": "critical"
        }
 
    elif "block" in filename_lower:
        return {
            "detected": True,
            "hazard_type": "road_block",
            "confidence": 0.85,
            "severity": "medium"
        }
 
    elif "construction" in filename_lower:
        return {
            "detected": True,
            "hazard_type": "construction",
            "confidence": 0.85,
            "severity": "medium"
        }
 
    else:
        return {
            "detected": False,
            "hazard_type": "normal_road",
            "confidence": 0.70,
            "severity": "low"
        }
def calculate_visual_risk(detections):
 
    risk_score = 0
    reasons = []
 
    object_names = [
        detection["object"]
        for detection in detections
    ]
 
    # Many people in one scene
    person_count = object_names.count("person")
 
    if person_count >= 3:
        risk_score += 2
        reasons.append(
            "Multiple people detected in the scene"
        )
 
    # Large vehicles
    if "truck" in object_names:
        risk_score += 1
        reasons.append(
            "Large vehicle detected"
        )
 
    if "bus" in object_names:
        risk_score += 1
        reasons.append(
            "Bus detected"
        )
 
    # Motorcycle
    if "motorcycle" in object_names:
        risk_score += 1
        reasons.append(
            "Motorcycle detected"
        )
 
    # Car
    if "car" in object_names:
        reasons.append(
            "Vehicle detected"
        )
 
    # Determine risk
    if risk_score >= 5:
        risk_level = "high"
 
    elif risk_score >= 3:
        risk_level = "medium"
 
    else:
        risk_level = "low"
 
    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "reasons": reasons
    }
def combine_visual_risk_with_severity(
    visual_risk,
    emergency_type="ambulance"
):
 
    risk_level = visual_risk["risk_level"]
    risk_score = visual_risk["risk_score"]
 
    if risk_level == "high":
        severity = "critical"
 
    elif risk_level == "medium":
        severity = "high"
 
    else:
        severity = "medium"
 
    return {
        "emergency_type": emergency_type,
        "visual_risk_level": risk_level,
        "visual_risk_score": risk_score,
        "final_severity": severity,
        "reasons": visual_risk["reasons"]
    }
 
def assess_emergency_severity(
    emergency_type: str,
    description: str
):
 
    description_lower = description.lower()
 
    score = 0
    reasons = []
 
    # Accident indicators
    if emergency_type == "ambulance":
        score += 2
        reasons.append("Medical assistance requested")
 
    if "accident" in description_lower:
        score += 2
        reasons.append("Accident detected")
 
    if "collision" in description_lower:
        score += 2
        reasons.append("Vehicle collision detected")
 
    # Injury indicators
    if "injured" in description_lower:
        score += 3
        reasons.append("Injured person reported")
 
    if "injury" in description_lower:
        score += 3
        reasons.append("Injury reported")
 
    # Fire indicators
    if "fire" in description_lower:
        score += 4
        reasons.append("Fire detected")
 
    if "smoke" in description_lower:
        score += 3
        reasons.append("Smoke detected")
 
    # Multiple people
    if "multiple" in description_lower:
        score += 3
        reasons.append("Multiple people potentially affected")
 
    # Serious condition
    if "unconscious" in description_lower:
        score += 5
        reasons.append("Unconscious person reported")
 
    if "critical" in description_lower:
        score += 5
        reasons.append("Critical condition reported")
 
    # Determine severity
    if score >= 9:
        severity = "critical"
 
    elif score >= 6:
        severity = "high"
 
    elif score >= 3:
        severity = "medium"
 
    else:
        severity = "low"
 
    return {
        "severity": severity,
        "score": score,
        "reasons": reasons
    }
 
 
@app.get("/")
def home():
    return {
        "message": "Emergency Service is running",
        "status": "active"
    }
 
 
@app.get("/emergency/test")
def emergency_test():
    return {
        "message": "Emergency API is working",
        "service": "Emergency & Smart Response",
        "status": "ready"
    }
 
 
@app.post("/emergency/report")
def report_emergency(emergency: EmergencyRequest):
    global emergency_counter
 
    emergency_counter += 1
 
    emergency_id = f"EMG-{emergency_counter:06d}"
 
    reported_at = datetime.now().isoformat()
 
    emergency_data = {
        "emergency_id": emergency_id,
        "emergency_type": emergency.emergency_type.value,
        "latitude": emergency.latitude,
        "longitude": emergency.longitude,
        "description": emergency.description,
        "severity": emergency.severity.value,
        "status": "received",
        "verification_status": "pending",
        "reported_at": reported_at
    }
 
    emergencies[emergency_id] = emergency_data
 
    return {
        "message": "Emergency report received",
        **emergency_data
    }
@app.get("/emergency/{emergency_id}")
def get_emergency(emergency_id: str):
 
    if emergency_id not in emergencies:
        return {
            "message": "Emergency not found",
            "emergency_id": emergency_id,
            "available_emergencies": list(emergencies.keys())
        }
 
    return emergencies[emergency_id]
@app.post("/emergency/{emergency_id}/verify")
def verify_emergency(emergency_id: str):
 
    if emergency_id not in emergencies:
        return {
            "message": "Emergency not found",
            "emergency_id": emergency_id
        }
 
    emergencies[emergency_id]["status"] = "verifying"
 
    emergencies[emergency_id]["verification_status"] = "verified"
 
    emergencies[emergency_id]["status"] = "verified"
 
    return {
        "message": "Emergency verified successfully",
        "emergency_id": emergency_id,
        "verification_status": "verified",
        "status": "verified"
    }
@app.post("/emergency/{emergency_id}/decision")
def emergency_decision(emergency_id: str):
 
    if emergency_id not in emergencies:
        return {
            "message": "Emergency not found",
            "emergency_id": emergency_id
        }
 
    emergency = emergencies[emergency_id]
 
    if emergency["verification_status"] != "verified":
        return {
            "message": "Emergency must be verified first",
            "emergency_id": emergency_id,
            "verification_status": emergency["verification_status"]
        }
 
    severity = emergency["severity"]
 
    if severity == "critical":
        response_priority = "immediate"
        recommended_action = "Dispatch nearest emergency service immediately"
 
    elif severity == "high":
        response_priority = "high"
        recommended_action = "Dispatch emergency service with high priority"
 
    elif severity == "medium":
        response_priority = "normal"
        recommended_action = "Send emergency service"
 
    else:
        response_priority = "low"
        recommended_action = "Review emergency and provide assistance"
 
    return {
        "emergency_id": emergency_id,
        "verification_status": "verified",
        "severity": severity,
        "response_priority": response_priority,
        "recommended_action": recommended_action
    }
@app.get("/emergency/{emergency_id}/nearest-service")
def find_nearest_service(emergency_id: str):
 
    if emergency_id not in emergencies:
        return {
            "message": "Emergency not found",
            "emergency_id": emergency_id
        }
 
    emergency = emergencies[emergency_id]
 
    if emergency["verification_status"] != "verified":
        return {
            "message": "Emergency must be verified first",
            "emergency_id": emergency_id,
            "verification_status": emergency["verification_status"]
        }
 
    emergency_type = emergency["emergency_type"]
 
    if emergency_type == "ambulance":
        required_service = "ambulance"
 
    elif emergency_type == "police":
        required_service = "police"
 
    elif emergency_type == "fire":
        required_service = "fire"
 
    else:
        required_service = "ambulance"
 
    available_services = [
        service
        for service in emergency_services
        if service["service_type"] == required_service
        and service["available"] is True
    ]
 
    if not available_services:
        return {
            "message": "No available emergency service found",
            "service_type": required_service
        }
 
    services_with_distance = []
 
    for service in available_services:
 
        distance = calculate_distance(
            emergency["latitude"],
            emergency["longitude"],
            service["latitude"],
            service["longitude"]
        )
 
        service_copy = service.copy()
 
        service_copy["distance_km"] = distance
 
        services_with_distance.append(service_copy)
 
    nearest_service = min(
        services_with_distance,
        key=lambda service: service["distance_km"]
    )
 
    return {
        "message": "Nearest emergency service found",
        "emergency_id": emergency_id,
        "required_service": required_service,
        "nearest_service": nearest_service,
        "available_services": services_with_distance
    }
@app.get("/emergency/{emergency_id}/nearest-hospital")
def find_nearest_hospital(emergency_id: str):
 
    if emergency_id not in emergencies:
        return {
            "message": "Emergency not found",
            "emergency_id": emergency_id
        }
 
    emergency = emergencies[emergency_id]
 
    if emergency["verification_status"] != "verified":
        return {
            "message": "Emergency must be verified first",
            "emergency_id": emergency_id,
            "verification_status": emergency["verification_status"]
        }
 
    severity = emergency["severity"]
 
    suitable_hospitals = [
        hospital
        for hospital in hospitals
        if hospital["available"] is True
        and hospital["emergency_support"] is True
    ]
 
    if severity in ["high", "critical"]:
 
        trauma_hospitals = [
            hospital
            for hospital in suitable_hospitals
            if hospital["trauma_support"] is True
        ]
 
        if trauma_hospitals:
            suitable_hospitals = trauma_hospitals
 
    if not suitable_hospitals:
        return {
            "message": "No suitable hospital found"
        }
 
    hospitals_with_distance = []
 
    for hospital in suitable_hospitals:
 
        distance = calculate_distance(
            emergency["latitude"],
            emergency["longitude"],
            hospital["latitude"],
            hospital["longitude"]
        )
 
        hospital_copy = hospital.copy()
 
        hospital_copy["distance_km"] = distance
 
        hospitals_with_distance.append(hospital_copy)
 
    nearest_hospital = min(
        hospitals_with_distance,
        key=lambda hospital: hospital["distance_km"]
    )
 
    return {
        "message": "Nearest suitable hospital found",
        "emergency_id": emergency_id,
        "severity": severity,
        "nearest_hospital": nearest_hospital,
        "available_hospitals": hospitals_with_distance
    }
@app.get("/emergency/{emergency_id}/route")
def emergency_route(emergency_id: str):
 
    if emergency_id not in emergencies:
        return {
            "message": "Emergency not found",
            "emergency_id": emergency_id
        }
 
    emergency = emergencies[emergency_id]
 
    if emergency["verification_status"] != "verified":
        return {
            "message": "Emergency must be verified first",
            "emergency_id": emergency_id,
            "verification_status": emergency["verification_status"]
        }
 
    # Find required emergency service
    emergency_type = emergency["emergency_type"]
 
    if emergency_type == "ambulance":
        required_service = "ambulance"
    elif emergency_type == "police":
        required_service = "police"
    elif emergency_type == "fire":
        required_service = "fire"
    else:
        required_service = "ambulance"
 
    # Find available services
    available_services = [
        service
        for service in emergency_services
        if service["service_type"] == required_service
        and service["available"] is True
    ]
 
    if not available_services:
        return {
            "message": "No available emergency service found",
            "service_type": required_service
        }
 
    # Find nearest emergency service
    services_with_distance = []
 
    for service in available_services:
 
        distance = calculate_distance(
            emergency["latitude"],
            emergency["longitude"],
            service["latitude"],
            service["longitude"]
        )
 
        service_copy = service.copy()
        service_copy["distance_to_emergency_km"] = distance
 
        services_with_distance.append(service_copy)
 
    nearest_service = min(
        services_with_distance,
        key=lambda service: service["distance_to_emergency_km"]
    )
 
    # Find suitable hospitals
    suitable_hospitals = [
        hospital
        for hospital in hospitals
        if hospital["available"] is True
        and hospital["emergency_support"] is True
    ]
 
    # Serious emergencies should prefer trauma hospitals
    if emergency["severity"] in ["high", "critical"]:
 
        trauma_hospitals = [
            hospital
            for hospital in suitable_hospitals
            if hospital["trauma_support"] is True
        ]
 
        if trauma_hospitals:
            suitable_hospitals = trauma_hospitals
 
    if not suitable_hospitals:
        return {
            "message": "No suitable hospital found"
        }
 
    # Calculate hospital distance from accident
    hospitals_with_distance = []
 
    for hospital in suitable_hospitals:
 
        distance = calculate_distance(
            emergency["latitude"],
            emergency["longitude"],
            hospital["latitude"],
            hospital["longitude"]
        )
 
        hospital_copy = hospital.copy()
        hospital_copy["distance_from_accident_km"] = distance
 
        hospitals_with_distance.append(hospital_copy)
 
    nearest_hospital = min(
        hospitals_with_distance,
        key=lambda hospital: hospital["distance_from_accident_km"]
    )
 
    # Calculate ambulance distance to hospital
    ambulance_to_hospital = calculate_distance(
        nearest_service["latitude"],
        nearest_service["longitude"],
        nearest_hospital["latitude"],
        nearest_hospital["longitude"]
    )
 
    return {
        "message": "Emergency route calculated",
        "emergency_id": emergency_id,
 
        "emergency_location": {
            "latitude": emergency["latitude"],
            "longitude": emergency["longitude"]
        },
 
        "assigned_service": {
            "service_id": nearest_service["service_id"],
            "name": nearest_service["name"],
            "service_type": nearest_service["service_type"],
            "distance_to_emergency_km":
                nearest_service["distance_to_emergency_km"]
        },
 
        "hospital": {
            "hospital_id": nearest_hospital["hospital_id"],
            "name": nearest_hospital["name"],
            "distance_from_accident_km":
                nearest_hospital["distance_from_accident_km"]
        },
 
        "ambulance_to_hospital_km":
            round(ambulance_to_hospital, 2),
 
        "route_status": "ready"
    }
 
@app.put("/emergency/{emergency_id}/status")
def update_emergency_status(
    emergency_id: str,
    status: str
):
    if emergency_id not in emergencies:
        return {
            "message": "Emergency not found",
            "emergency_id": emergency_id
        }
 
    emergencies[emergency_id]["status"] = status
 
    return {
        "message": "Emergency status updated",
        "emergency_id": emergency_id,
        "status": status
    }
@app.post("/emergency/{emergency_id}/auto-response")
def emergency_auto_response(emergency_id: str):
 
    # ------------------------------------------------
    # STEP 1: Check whether emergency exists
    # ------------------------------------------------
 
    if emergency_id not in emergencies:
        return {
            "message": "Emergency not found",
            "emergency_id": emergency_id,
            "response_status": "failed"
        }
 
    emergency = emergencies[emergency_id]
 
    # ------------------------------------------------
    # STEP 2: Check emergency verification
    # ------------------------------------------------
 
    if emergency["verification_status"] != "verified":
        return {
            "message": "Emergency is not verified",
            "emergency_id": emergency_id,
            "verification_status":
                emergency["verification_status"],
            "response_status": "waiting_for_verification"
        }
 
    # ------------------------------------------------
    # STEP 3: Read emergency information
    # ------------------------------------------------
 
    emergency_type = emergency["emergency_type"]
    severity = emergency["severity"]
 
    latitude = emergency["latitude"]
    longitude = emergency["longitude"]
 
    # ------------------------------------------------
    # STEP 4: Decide required emergency service
    # ------------------------------------------------
 
    if emergency_type == "ambulance":
        required_service = "ambulance"
 
    elif emergency_type == "police":
        required_service = "police"
 
    elif emergency_type == "fire":
        required_service = "fire"
 
    else:
        required_service = "ambulance"
 
    # ------------------------------------------------
    # STEP 5: Find available emergency services
    # ------------------------------------------------
 
    available_services = [
        service
        for service in emergency_services
        if service["service_type"] == required_service
        and service["available"] is True
    ]
 
    if not available_services:
        return {
            "message": "No available emergency service found",
            "emergency_id": emergency_id,
            "required_service": required_service,
            "response_status": "service_unavailable"
        }
 
    # ------------------------------------------------
    # STEP 6: Calculate distance to every service
    # ------------------------------------------------
 
    services_with_distance = []
 
    for service in available_services:
 
        distance = calculate_distance(
            latitude,
            longitude,
            service["latitude"],
            service["longitude"]
        )
 
        service_copy = service.copy()
 
        service_copy["distance_to_emergency_km"] = distance
 
        services_with_distance.append(service_copy)
 
    # ------------------------------------------------
    # STEP 7: Select nearest service
    # ------------------------------------------------
 
    nearest_service = min(
        services_with_distance,
        key=lambda service:
            service["distance_to_emergency_km"]
    )
 
    # ------------------------------------------------
    # STEP 8: Find suitable hospitals
    # ------------------------------------------------
 
    suitable_hospitals = [
        hospital
        for hospital in hospitals
        if hospital["available"] is True
        and hospital["emergency_support"] is True
    ]
 
    # ------------------------------------------------
    # STEP 9: For serious cases prefer trauma hospital
    # ------------------------------------------------
 
    if severity in ["high", "critical"]:
 
        trauma_hospitals = [
            hospital
            for hospital in suitable_hospitals
            if hospital["trauma_support"] is True
        ]
 
        if trauma_hospitals:
            suitable_hospitals = trauma_hospitals
 
    # ------------------------------------------------
    # STEP 10: Check hospital availability
    # ------------------------------------------------
 
    if not suitable_hospitals:
        return {
            "message": "No suitable hospital found",
            "emergency_id": emergency_id,
            "response_status": "hospital_unavailable"
        }
 
    # ------------------------------------------------
    # STEP 11: Calculate distance to hospitals
    # ------------------------------------------------
 
    hospitals_with_distance = []
 
    for hospital in suitable_hospitals:
 
        distance = calculate_distance(
            latitude,
            longitude,
            hospital["latitude"],
            hospital["longitude"]
        )
 
        hospital_copy = hospital.copy()
 
        hospital_copy["distance_from_accident_km"] = distance
 
        hospitals_with_distance.append(hospital_copy)
 
    # ------------------------------------------------
    # STEP 12: Select nearest suitable hospital
    # ------------------------------------------------
 
    nearest_hospital = min(
        hospitals_with_distance,
        key=lambda hospital:
            hospital["distance_from_accident_km"]
    )
 
    # ------------------------------------------------
    # STEP 13: Calculate ambulance to hospital distance
    # ------------------------------------------------
 
    ambulance_to_hospital = calculate_distance(
        nearest_service["latitude"],
        nearest_service["longitude"],
        nearest_hospital["latitude"],
        nearest_hospital["longitude"]
    )
 
    # ------------------------------------------------
    # STEP 14: Return complete AI response
    # ------------------------------------------------
 
    return {
 
        "message": "AI emergency auto-response completed",
 
        "emergency_id": emergency_id,
 
        "verification": emergency["verification_status"],
 
        "emergency_type": emergency_type,
 
        "severity": severity,
 
        "emergency_location": {
            "latitude": latitude,
            "longitude": longitude
        },
 
        "emergency_service": {
 
            "service_id":
                nearest_service["service_id"],
 
            "name":
                nearest_service["name"],
 
            "type":
                nearest_service["service_type"],
 
            "distance_km":
                nearest_service["distance_to_emergency_km"]
        },
 
        "hospital": {
 
            "hospital_id":
                nearest_hospital["hospital_id"],
 
            "name":
                nearest_hospital["name"],
 
            "distance_km":
                nearest_hospital["distance_from_accident_km"]
        },
 
        "ambulance_route": {
 
            "distance_km":
                round(ambulance_to_hospital, 2),
 
            "status": "ready"
        },
 
        "response_status":
            "ambulance_assigned"
    }
@app.post("/emergency/assess-severity")
def assess_severity_endpoint(
    emergency_type: str,
    description: str
):
 
    result = assess_emergency_severity(
        emergency_type,
        description
    )
 
    return {
        "message": "Emergency severity assessed",
        "emergency_type": emergency_type,
        "description": description,
        "assessment": result
    }
@app.post("/emergency/analyze-image")
async def analyze_emergency_image(
    image: UploadFile = File(...)
):
 
    # Check file type
 
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]
 
    if image.content_type not in allowed_types:
        return {
            "message": "Unsupported image type",
            "supported_types": allowed_types
        }
 
    # Read image
 
    image_data = await image.read()
 
    # Check empty file
 
    if not image_data:
        return {
            "message": "Empty image file"
        }
 
    # Create file name
 
    file_name = image.filename
 
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file_name
    )
 
    # Save image
 
    with open(file_path, "wb") as file:
 
        file.write(image_data)
 
        analysis = analyze_hazard_image(
        file_name
    )
 
    return {
        "message": "Emergency image analyzed successfully",
 
        "file_name": file_name,
 
        "file_path": file_path,
 
        "image_type": image.content_type,
 
        "file_size_bytes": len(image_data),
 
        "analysis": analysis
    }
@app.post("/emergency/yolo-test")
async def yolo_test(
    image: UploadFile = File(...)
):
 
    image_data = await image.read()
 
    if not image_data:
        return {
            "message": "Empty image"
        }
 
    file_path = os.path.join(
        UPLOAD_FOLDER,
        "yolo_test_" + image.filename
    )
 
    with open(file_path, "wb") as file:
        file.write(image_data)
 
    results = model(file_path)
 
    detections = []
 
    for result in results:
 
        for box in result.boxes:
 
            class_id = int(box.cls[0])
 
            confidence = float(box.conf[0])
 
            class_name = model.names[class_id]
 
            detections.append({
                "object": class_name,
                "confidence": round(confidence, 2)
            })
 
    return {
        "message": "YOLO image analysis completed",
        "file_name": image.filename,
        "detections": detections
    }
@app.post("/emergency/visual-risk")
async def visual_risk_test(
    image: UploadFile = File(...)
):
 
    image_data = await image.read()
 
    if not image_data:
        return {
            "message": "Empty image"
        }
 
    file_path = os.path.join(
        UPLOAD_FOLDER,
        "risk_" + image.filename
    )
 
    with open(file_path, "wb") as file:
        file.write(image_data)
 
    # Run YOLO
    results = model(file_path)
 
    detections = []
 
    for result in results:
 
        for box in result.boxes:
 
            class_id = int(box.cls[0])
 
            confidence = float(box.conf[0])
 
            class_name = model.names[class_id]
 
            detections.append({
                "object": class_name,
                "confidence": round(
                    confidence,
                    2
                )
            })
 
    # Calculate visual risk
    risk = calculate_visual_risk(
        detections
    )
 
    return {
        "message": "Visual risk analysis completed",
 
        "file_name": image.filename,
 
        "detections": detections,
 
        "risk_assessment": risk
    }
@app.post("/emergency/ai-assessment")
async def ai_assessment(
    image: UploadFile = File(...)
):
 
    image_data = await image.read()
 
    if not image_data:
        return {
            "message": "Empty image"
        }
 
    file_path = os.path.join(
        UPLOAD_FOLDER,
        "ai_" + image.filename
    )
 
    with open(file_path, "wb") as file:
        file.write(image_data)
 
    # -----------------------------------------
    # Run YOLO
    # -----------------------------------------
 
    results = model(file_path)
 
    detections = []
 
    for result in results:
 
        for box in result.boxes:
 
            class_id = int(box.cls[0])
 
            confidence = float(box.conf[0])
 
            class_name = model.names[class_id]
 
            detections.append({
                "object": class_name,
                "confidence": round(
                    confidence,
                    2
                )
            })
 
    # -----------------------------------------
    # Visual risk
    # -----------------------------------------
 
    visual_risk = calculate_visual_risk(
        detections
    )
 
    # -----------------------------------------
    # Final AI assessment
    # -----------------------------------------
 
    assessment = combine_visual_risk_with_severity(
        visual_risk,
        "ambulance"
    )
 
    return {
        "message": "AI emergency assessment completed",
 
        "file_name": image.filename,
 
        "detections": detections,
 
        "visual_risk": visual_risk,
 
        "assessment": assessment
    }
@app.post("/emergency/ai-auto-response")
async def ai_auto_response(
    image: UploadFile = File(...),
    latitude: float = 16.5837,
    longitude: float = 82.0061
):
    global emergency_counter
 
    # -----------------------------------------
    # 1. Read image
    # -----------------------------------------
 
    image_data = await image.read()
 
    if not image_data:
        return {
            "message": "Empty image"
        }
 
    # -----------------------------------------
    # 2. Save image
    # -----------------------------------------
 
    file_path = os.path.join(
        UPLOAD_FOLDER,
        "emergency_" + image.filename
    )
 
    with open(file_path, "wb") as file:
        file.write(image_data)
 
    # -----------------------------------------
    # 3. Run YOLO
    # -----------------------------------------
 
    results = model(file_path)
 
    detections = []
 
    for result in results:
 
        for box in result.boxes:
 
            class_id = int(box.cls[0])
 
            confidence = float(box.conf[0])
 
            class_name = model.names[class_id]
 
            detections.append({
                "object": class_name,
                "confidence": round(
                    confidence,
                    2
                )
            })
 
    # -----------------------------------------
    # 4. Calculate visual risk
    # -----------------------------------------
 
    visual_risk = calculate_visual_risk(
        detections
    )
 
    # -----------------------------------------
    # 5. Calculate severity
    # -----------------------------------------
 
    assessment = combine_visual_risk_with_severity(
        visual_risk,
        "ambulance"
    )
 
    # -----------------------------------------
    # 6. Emergency decision
    # -----------------------------------------
 
    if assessment["final_severity"] in ["high", "critical"]:
        emergency_created = True
        emergency_counter += 1
        emergency_id = f"EMG-{emergency_counter:06d}"
    else:
        emergency_created = False
        emergency_id = None
 
    # -----------------------------------------
    # 7. Return result
    # -----------------------------------------
    # -----------------------------------------
    # 6b. Find nearest ambulance and hospital
    # -----------------------------------------

    nearest_service = None
    nearest_hospital = None
    ambulance_to_hospital_km = None

    if emergency_created:

        # Find available ambulances
        available_services = [
            service
            for service in emergency_services
            if service["service_type"] == "ambulance"
            and service["available"] is True
        ]

        if available_services:

            services_with_distance = []

            for service in available_services:
                distance = calculate_distance(
                    latitude,
                    longitude,
                    service["latitude"],
                    service["longitude"]
                )
                service_copy = service.copy()
                service_copy["distance_km"] = distance
                services_with_distance.append(service_copy)

            nearest_service = min(
                services_with_distance,
                key=lambda service: service["distance_km"]
            )

        # Find suitable hospitals
        suitable_hospitals = [
            hospital
            for hospital in hospitals
            if hospital["available"] is True
            and hospital["emergency_support"] is True
        ]

        if assessment["final_severity"] in ["high", "critical"]:
            trauma_hospitals = [
                hospital
                for hospital in suitable_hospitals
                if hospital["trauma_support"] is True
            ]
            if trauma_hospitals:
                suitable_hospitals = trauma_hospitals

        if suitable_hospitals:

            hospitals_with_distance = []

            for hospital in suitable_hospitals:
                distance = calculate_distance(
                    latitude,
                    longitude,
                    hospital["latitude"],
                    hospital["longitude"]
                )
                hospital_copy = hospital.copy()
                hospital_copy["distance_km"] = distance
                hospitals_with_distance.append(hospital_copy)

            nearest_hospital = min(
                hospitals_with_distance,
                key=lambda hospital: hospital["distance_km"]
            )

        # Calculate ambulance-to-hospital distance
        if nearest_service and nearest_hospital:
            ambulance_to_hospital_km = calculate_distance(
                nearest_service["latitude"],
                nearest_service["longitude"],
                nearest_hospital["latitude"],
                nearest_hospital["longitude"]
            )

        # Save to database
        save_emergency(
            emergency_id=emergency_id,
            latitude=latitude,
            longitude=longitude,
            severity=assessment["final_severity"],
            hazard_type="ai_detected",
            status="verified",
            ambulance_id=nearest_service["service_id"] if nearest_service else None,
            hospital_id=nearest_hospital["hospital_id"] if nearest_hospital else None,
            route_status="ready" if nearest_service and nearest_hospital else "pending"
        )
 
    return {
        "message": "AI emergency response assessment completed",
 
        "emergency_created": emergency_created,
 
        "emergency_id": emergency_id,
 
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
 
        "image": {
            "file_name": image.filename,
            "file_path": file_path
        },
 
        "detections": detections,
 
        "visual_risk": visual_risk,
 
        "assessment": assessment,

        "ambulance": nearest_service,

        "hospital": nearest_hospital,

        "ambulance_to_hospital_km": ambulance_to_hospital_km
    }
@app.post("/emergency/ai-emergency-test")
async def ai_emergency_test(
    latitude: float = 16.5837,
    longitude: float = 82.0061
):
 
    # Controlled hackathon test
    # This simulates a HIGH visual-risk result.
    # It does not contact real emergency services.
 
    visual_risk = {
        "risk_level": "high",
        "risk_score": 5,
        "reasons": [
            "High-risk road scene detected"
        ]
    }
 
    assessment = combine_visual_risk_with_severity(
        visual_risk,
        "ambulance"
    )
 
    emergency_id = "EMG-AI-000001"
 
    return {
        "message": "AI emergency test response created",
 
        "emergency_created": True,
 
        "emergency_id": emergency_id,
 
        "verification_status": "pending_confirmation",
 
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
 
        "visual_risk": visual_risk,
 
        "assessment": assessment,
 
        "next_action": "Emergency services workflow ready for authorized confirmation"
    }
@app.post("/emergency/ai-dispatch-test")
async def ai_dispatch_test(
    latitude: float = 16.5837,
    longitude: float = 82.0061
):
 
    # ------------------------------------------------
    # AI has already determined this is high risk
    # ------------------------------------------------
 
    emergency_id = "EMG-AI-000001"
 
    severity = "critical"
 
    # ------------------------------------------------
    # Existing prototype emergency resources
    # ------------------------------------------------
 
    assigned_service = {
        "service_id": "AMB-001",
        "name": "Amalapuram Ambulance 1",
        "service_type": "ambulance",
        "distance_to_emergency_km": 0.1
    }
 
    hospital = {
        "hospital_id": "HOS-002",
        "name": "Amalapuram Trauma Care Hospital",
        "distance_from_accident_km": 1.15
    }
 
    ambulance_to_hospital_km = 1.13
 
    # ------------------------------------------------
    # Final response
    # ------------------------------------------------
 
    return {
        "message": "AI emergency response ready",
 
        "emergency_id": emergency_id,
 
        "severity": severity,
 
        "emergency_location": {
            "latitude": latitude,
            "longitude": longitude
        },
 
        "assigned_service": assigned_service,
 
        "hospital": hospital,
 
        "ambulance_to_hospital_km":
            ambulance_to_hospital_km,
 
        "route_status": "ready",
 
        "dispatch_status":
            "awaiting_authorized_confirmation"
    }
@app.post("/emergency/save-test")
async def save_emergency_test():
 
    global emergency_counter
 
    # Create a new emergency ID
    emergency_counter += 1
    emergency_id = f"EMG-{emergency_counter:06d}"
 
    # Create emergency in memory
    emergency_data = {
        "emergency_id": emergency_id,
        "emergency_type": "ambulance",
        "latitude": 16.5837,
        "longitude": 82.0061,
        "description": "AI detected road accident",
        "severity": "critical",
        "status": "verified",
        "verification_status": "verified",
        "reported_at": datetime.now().isoformat()
    }
 
    # Save to memory
    emergencies[emergency_id] = emergency_data
 
    # Save to SQLite database
    save_emergency(
        emergency_id=emergency_id,
        latitude=16.5837,
        longitude=82.0061,
        severity="critical",
        hazard_type="accident",
        status="verified",
        ambulance_id="AMB-001",
        hospital_id="HOS-002",
        route_status="ready"
    )
 
    return {
        "message": "Emergency saved successfully",
        "emergency_id": emergency_id,
        "verification_status": "verified",
        "database_saved": True,
        "memory_saved": True
    }
@app.get("/history/emergencies")
async def database_history():
 
    try:
        connection = sqlite3.connect(DATABASE)
        connection.row_factory = sqlite3.Row
 
        cursor = connection.cursor()
 
        cursor.execute("""
            SELECT
                id,
                emergency_id,
                latitude,
                longitude,
                severity,
                hazard_type,
                status,
                ambulance_id,
                hospital_id,
                route_status,
                created_at
            FROM emergencies
            ORDER BY id DESC
        """)
 
        rows = cursor.fetchall()
 
        connection.close()
 
        emergencies = []
 
        for row in rows:
            emergencies.append({
                "id": row["id"],
                "emergency_id": row["emergency_id"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "severity": row["severity"],
                "hazard_type": row["hazard_type"],
                "status": row["status"],
                "ambulance_id": row["ambulance_id"],
                "hospital_id": row["hospital_id"],
                "route_status": row["route_status"],
                "created_at": row["created_at"]
            })
 
        return {
            "message": "Emergency history retrieved successfully",
            "count": len(emergencies),
            "emergencies": emergencies
        }
 
    except Exception as e:
 
        return {
            "message": "Database error",
            "error": str(e)
        }
 
