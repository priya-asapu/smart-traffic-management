from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("../yolo11n.pt")

# Open laptop camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera open avvaledu")
        break

    # Detect objects
    results = model(frame)

    # Check detected objects
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            if class_name == "person":
                cv2.putText(
                    frame,
                    "HAZARD: PERSON DETECTED",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2
                )

            elif class_name in ["car", "bus", "truck", "motorcycle"]:
                cv2.putText(
                    frame,
                    "TRAFFIC VEHICLE DETECTED",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2
                )

    # Show camera
    cv2.imshow("Smart Traffic Hazard Detection", frame)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()