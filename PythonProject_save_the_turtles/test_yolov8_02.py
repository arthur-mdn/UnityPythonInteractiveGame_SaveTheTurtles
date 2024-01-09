from ultralytics import YOLO
model = YOLO('yolov8n-pose.pt')
results = model(source='floor6.png', show=True, conf=0.3, save=True)
