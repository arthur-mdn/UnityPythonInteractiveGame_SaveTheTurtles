import cv2
from ultralytics import YOLO

def are_hands_in_air(keypoints):
    # Récupérer les coordonnées "y" des poignets et des épaules
    if not keypoints[0]:
        return False
    left_hand_y = keypoints[0][9][1]
    right_hand_y = keypoints[0][10][1]
    left_eye_y = keypoints[0][1][1]
    right_eye_y = keypoints[0][2][1]

   # si les mains ne sont pas détectées, on retourne false
    if left_hand_y == 0 or right_hand_y == 0:
        return False

    # Si les mains sont plus hautes que yeux, alors les mains sont en l'air
    return left_hand_y < left_eye_y and right_hand_y < right_eye_y

def start_yolo_hands_detection():
    model = YOLO("../yolo/yolov8n-pose.pt")
    cap = cv2.VideoCapture(0)

    hands_in_air_counter = 0

    while True:
        success, frame = cap.read()

        if not success:
            break

        results = model(frame)
        keypoints = results[0].keypoints.xy.tolist()

        cv2.imshow("Yolo Detection", frame)

        hands_in_air = are_hands_in_air(keypoints)
        if hands_in_air:
            hands_in_air_counter += 1
        else:
            hands_in_air_counter = 0
        print("Mains en l'air:", hands_in_air)

        if hands_in_air_counter >= 10:
            print("10 confirmations consécutives que les mains étaient en l'air.")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_yolo_hands_detection()
