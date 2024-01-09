#yolo pose predict model=yolov8m-pose.pt source=0 show=true

from ultralytics import YOLO
import cv2

# Créez une instance YOLOv8
yolo = YOLO(model='yolov8n-pose.pt')

# Capturez la vidéo de votre webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Effectuez la détection de pose avec YOLOv8
    results = yolo.predict(frame)
    results = yolo.predict(source="0", show=True) # Display preds. Accepts all YOLO predict arguments

    # Obtenez l'image avec les détections
    frame = results[0]

    # Affichez le cadre avec les détections
    cv2.imshow('YOLOv8 Pose Detection', frame)

    # Pour quitter, appuyez sur 'q'
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()