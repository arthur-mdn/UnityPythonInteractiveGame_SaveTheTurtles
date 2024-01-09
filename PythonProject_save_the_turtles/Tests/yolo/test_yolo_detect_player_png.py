from ultralytics import YOLO
import cv2

# Créez une instance YOLOv8
yolo = YOLO(model='../../yolo/yolov8n-pose.pt')

# Chargez votre image PNG
image_path = '../../Elements/floor6.png'  # Remplacez par le chemin vers votre image PNG
frame = cv2.imread(image_path)

if frame is not None:
    # Effectuez la prédiction
    results = yolo.predict(frame)
    
    # Vérifiez si les résultats sont une liste et ont un élément
    if isinstance(results, list) and len(results):
        # Accédez au premier objet Results
        result_obj = results[0]
        
        annotated_frame = result_obj.plot()
        # Display the annotated image
        cv2.imshow('YOLOv8 Pose Detection', annotated_frame)
        cv2.waitKey(0)
    else:
        print("Les résultats ne sont pas dans le format attendu.")

cv2.destroyAllWindows()
