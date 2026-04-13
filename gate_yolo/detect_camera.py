from ultralytics import YOLO
import cv2
import csv

model = YOLO("runs/detect/train/weights/best.pt")

cap = cv2.VideoCapture(0)

with open("detections.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["x1","y1","x2","y2","cx","cy","confidence"])

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            conf = box.conf[0]

            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2

            writer.writerow([float(x1),float(y1),float(x2),float(y2),float(cx),float(cy),float(conf)])

        annotated = results[0].plot()
        cv2.imshow("YOLO Detection", annotated)

        if cv2.waitKey(1) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
