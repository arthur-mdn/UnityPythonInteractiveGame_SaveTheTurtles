import cv2
from ultralytics import YOLO

# Initialisation du modèle YOLOv8 avec le modèle de pose
model = YOLO('../../yolo/yolov8n-pose.pt')

# Capture le flux vidéo de la première webcam disponible
cap = cv2.VideoCapture(0)

while True:
    # Capture frame par frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convertit le frame en format attendu par le modèle (si nécessaire)
    # et utilisation du modèle YOLO pour détecter des poses dans le frame actuel
    results = model(frame)

    # Traitement des résultats
    for result in results:
        boxes = result.boxes.xyxy
        keypoints = result.keypoints 

    # Affiche le frame traité
    cv2.imshow('Processed Frame', frame)

    # Appuyez sur 'q' pour quitter la boucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
