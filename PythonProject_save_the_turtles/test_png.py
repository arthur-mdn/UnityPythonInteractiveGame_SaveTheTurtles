from ultralytics import YOLO
import cv2
import numpy as np  # Assurez-vous d'ajouter cette importation

# Créez une instance YOLOv8
yolo = YOLO(model='yolov8n-pose.pt')

# Chargez votre image PNG
image_path = 'floor6.png'  # Remplacez par le chemin vers votre image PNG
frame = cv2.imread(image_path)

if frame is not None:
    results = yolo.predict(frame)
    print(results)
    annotated_frame = results.orig_img

    # Affichez l'image annotée
    cv2.imshow('YOLOv8 Pose Detection', annotated_frame)
    cv2.waitKey(0)

cv2.destroyAllWindows()