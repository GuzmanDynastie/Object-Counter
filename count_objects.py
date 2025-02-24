import cv2
from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")
cap = cv2.VideoCapture(0)

cv2.namedWindow("Detección en tiempo real", cv2.WINDOW_NORMAL)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar el frame")
        break 

    frame_resized = cv2.resize(frame, (640, 640))
    results = model(frame, conf=0.75)

    num_mesas = len(results[0].boxes)

    annotated_frame = results[0].plot()
    cv2.putText(annotated_frame, f"Mesas detectadas: {num_mesas}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Detección en tiempo real", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()