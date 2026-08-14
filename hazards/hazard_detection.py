import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open laptop camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera could not be opened")
        break

    # Detect objects
    results = model(frame, verbose=False)

    # Store detected objects
    detected_objects = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])

            if confidence > 0.5:
                detected_objects.append(class_name)

    # Draw detection boxes
    annotated_frame = results[0].plot()

    # Person hazard
    if "person" in detected_objects:
        cv2.putText(
            annotated_frame,
            "HAZARD: PERSON DETECTED",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )

    # Vehicle detection
    elif any(
        vehicle in detected_objects
        for vehicle in ["car", "motorcycle", "bus", "truck"]
    ):
        cv2.putText(
            annotated_frame,
            "TRAFFIC VEHICLE DETECTED",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )

    # Show camera
    cv2.imshow("AI Vision Hazards Detection", annotated_frame)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()