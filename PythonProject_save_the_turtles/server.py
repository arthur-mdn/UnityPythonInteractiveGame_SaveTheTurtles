# server.py
from ultralytics import YOLO
import UdpComms as U
import time
import json
import cv2
import numpy as np
import threading
is_calibrated = False
calibration_points = None
capture_running = False
model = YOLO("yolo/yolov8n-pose.pt")
video_source = "webcam"
video_path = "Elements/wall_vid.mp4"

def are_hands_in_air(keypoints, frame_height):
    if not keypoints[0]:
        return False
    left_hand_y = keypoints[0][9][1]
    right_hand_y = keypoints[0][10][1]
    left_eye_y = keypoints[0][1][1]
    right_eye_y = keypoints[0][2][1]

    if left_hand_y == 0 or right_hand_y == 0:
        return False

    return left_hand_y < left_eye_y and right_hand_y < right_eye_y

def start_yolo_hands_detection():
    global model
    cap = cv2.VideoCapture(0)
    hands_in_air_counter = 0

    while True:
        success, frame = cap.read()

        if not success:
            break

        results = model(frame)
        keypoints = results[0].keypoints.xy.tolist()

        hands_in_air = are_hands_in_air(keypoints, frame.shape[0])
        if hands_in_air:
            hands_in_air_counter += 1
        else:
            hands_in_air_counter = 0

        if hands_in_air_counter >= 10:
            print("Mains en l'air détectées")
            message = {
                "sender": "python",
                "message": "change_scene_to_calibrate"
            }
            json_message = json.dumps(message)
            sock.SendData(json_message)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def detect_aruco_markers(image):
    # Paramètres ArUco
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
    aruco_params = cv2.aruco.DetectorParameters()

    # Détecter les marqueurs
    corners, ids, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=aruco_params)

    if ids is not None:
        # S'assurer que les marqueurs requis sont détectés
        required_markers = [10, 80]
        marker_positions = {}

        for i, marker_id in enumerate(ids):
            if marker_id[0] in required_markers:
                marker_positions[marker_id[0]] = corners[i][0]

        if all(marker in marker_positions for marker in required_markers):
            return marker_positions
        else:
            print("Missing required markers")
            return None
    else:
        print("No markers found")
        return None

def order_points_with_aruco_markers(points, marker_positions):
    # Calculer la distance de chaque point aux marqueurs ArUco
    distances_to_marker_10 = np.sqrt((points[:, 0] - marker_positions[10][0][0]) ** 2 + (points[:, 1] - marker_positions[10][0][1]) ** 2)
    distances_to_marker_80 = np.sqrt((points[:, 0] - marker_positions[80][0][0]) ** 2 + (points[:, 1] - marker_positions[80][0][1]) ** 2)

    # Identifier les points les plus proches de chaque marqueur
    top_left = points[np.argmin(distances_to_marker_10)]  # le plus proche du marqueur 10
    bottom_right = points[np.argmin(distances_to_marker_80)]  # le plus proche du marqueur 80

    # Créer une liste des points restants
    remaining = [pt for pt in points if (pt != top_left).any() and (pt != bottom_right).any()]

    # Vérifier s'il y a suffisamment de points restants
    if len(remaining) < 2:
        print("Not enough unique points were found")
        return None  # ou vous pouvez gérer cette situation différemment

    # Déterminer les points restants en haut à droite et en bas à gauche
    # en comparant leurs coordonnées en X
    if remaining[0][0] > remaining[1][0]:
        top_right = remaining[0]
        bottom_left = remaining[1]
    else:
        top_right = remaining[1]
        bottom_left = remaining[0]

    # Retourner les points ordonnés
    return np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32")


def auto_detect_edges(image):
    orig = image.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 56, 170])
    upper_red = np.array([23, 255, 255])

    # Détection des contours rouges
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5,5), np.uint8)
    mask_closed = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    masked_gray = cv2.bitwise_and(gray, gray, mask=mask_closed)
    blurred = cv2.GaussianBlur(masked_gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    
    marker_positions = detect_aruco_markers(gray)  # gray est l'image en niveaux de gris
    if marker_positions is None:
        print("Could not detect both ArUco markers")
        return None

    # Recherche des contours dans l'image des bords, et ne garde que les plus grands
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    # Boucle sur les contours
    for contour in contours:
        # Approximation du contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        # Si notre contour approximé a quatre points, alors
        # nous pouvons supposer que nous avons trouvé notre écran
        if len(approx) == 4:
            screenCnt = approx
            break

    # Si on a trouvé un contour
    if screenCnt is not None:
        # Récupération des points du contour
        points = screenCnt.reshape(4, 2)
        # Réorganisation des points avec les carrés de couleur
        ordered_points = order_points_with_aruco_markers(points, marker_positions)
        img_with_corners = orig.copy()

        # Dessiner les coins sur l'image
        for i, point in enumerate(ordered_points):
            x, y = point
            cv2.circle(img_with_corners, (int(x), int(y)), 7, (0, 255, 0), -1)  # Dessine un cercle vert autour du coin
            cv2.putText(img_with_corners, f"{i+1}", (int(x) - 25, int(y) - 25), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)  # Numérote le coin

        # Affiche l'image avec les coins
        cv2.imshow("Image with corners", img_with_corners)
        cv2.waitKey(0)  # Attendez que l'utilisateur appuie sur une touche
        cv2.destroyAllWindows()
        return ordered_points
    else:
        print("No suitable contour found")
        return None


def capture_and_process_image(tries=5):
    for _ in range(tries):
        cap = cv2.VideoCapture(0)
        success, frame = cap.read()
        cap.release()

        if success:
            #cv2.imshow("Captured Image", frame)
            #cv2.waitKey(1)  # Attente non bloquante

            processed_points = auto_detect_edges(frame)
            if processed_points is not None:
                print(processed_points)
                #cv2.destroyWindow("Captured Image")  # Fermer la fenêtre après traitement
                return processed_points
            else:
                print("Failed to detect edges on try: {}".format(_ + 1))
        else:
            print("Failed to capture image on try: {}".format(_ + 1))

    #cv2.destroyWindow("Captured Image")  # S'assurer que la fenêtre est fermée en cas d'échec
    print("Calibration failed after {} tries".format(tries))
    return None

def capture_and_process_image_from_video(video_path, tries=5):
    cap = cv2.VideoCapture(video_path)

    for _ in range(tries):
        success, frame = cap.read()

        if success:
            processed_points = auto_detect_edges(frame)
            if processed_points is not None:
                print(processed_points)
                return processed_points
            else:
                print("Failed to detect edges on try: {}".format(_ + 1))
        else:
            print("Failed to read frame on try: {}".format(_ + 1))

    print("Calibration failed after {} tries".format(tries))
    cap.release()
    return None

def transform_perspective(points, src_coords, dst_coords):
    # Assurez-vous que points est un tableau NumPy avec la forme correcte
    points = np.array(points, dtype="float32").reshape(-1, 1, 2)

    # Calculer la matrice de transformation
    M = cv2.getPerspectiveTransform(src_coords, dst_coords)

    # Appliquer la transformation aux points
    transformed_points = cv2.perspectiveTransform(points, M)
    return transformed_points.reshape(-1, 2)



def capture_and_process_player_continuous():
    global capture_running, calibration_points, video_source

    if video_source == "webcam":
        cap = cv2.VideoCapture(0)
    elif video_source == "file":
        cap = cv2.VideoCapture(video_path)
    else:
        print("Invalid video source")
        return
    
    dst_coords = np.array([[0, 0], [640, 0], [640, 360], [0, 360]], dtype="float32")  # Exemple de dimensions 16/9
    
    while capture_running:
        success, frame = cap.read()

        if not success:
            print("Failed to read frame from video")
            break

        # Traitement des keypoints et détection des mains
        results = model(frame)
        keypoints = results[0].keypoints.xy.tolist()

        hand_positions = []
        for person in keypoints:
            if len(person) > 0:
                left_hand = person[9]  # left_wrist
                right_hand = person[10]  # right_wrist
                print(right_hand)
                print(left_hand)
                # Vérifier si les coordonnées des mains sont valides avant de les ajouter
                if 0 < left_hand[0] < frame.shape[1] and 0 < left_hand[1] < frame.shape[0]:
                    hand_positions.append(left_hand)
                    cv2.circle(frame, (int(left_hand[0]), int(left_hand[1])), 10, (0, 255, 0), -1)

                if 0 < right_hand[0] < frame.shape[1] and 0 < right_hand[1] < frame.shape[0]:
                    hand_positions.append(right_hand)
                    cv2.circle(frame, (int(right_hand[0]), int(right_hand[1])), 10, (0, 0, 255), -1)

        if calibration_points is not None and len(hand_positions) > 0:
            transformed_hand_positions = transform_perspective(hand_positions, np.array(calibration_points, dtype="float32"), dst_coords)
            
            max_width = 640  # Largeur maximale
            max_height = 360  # Hauteur maximale
            
            # Envoi des positions des mains transformées à Unity
            message = {
                "sender": "python",
                "message": "hands_positions",
                "data": [[pos[0] / max_width, pos[1] / max_height] for pos in transformed_hand_positions]
            }
            json_message = json.dumps(message)
            print("Sending JSON: ", json_message)
            sock.SendData(json_message)

            # Dessiner les mains calibrées sur une nouvelle image
            calib_frame = np.zeros((360, 640, 3), dtype=np.uint8)
            for pos in transformed_hand_positions:
                cv2.circle(calib_frame, (int(pos[0]), int(pos[1])), 10, (255, 0, 0), -1)

            cv2.imshow("Calibrated Hand Positions", calib_frame)

            
       

        # Afficher la vidéo avec les positions des mains dessinées
        cv2.imshow("Video Stream with Hand Positions", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



def calibrate_positions(positions, calibration_data):
    # calibration_data est une liste de points calibrés [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    # Ici, vous devez appliquer une transformation basée sur ces points
    # Cela pourrait être une transformation de perspective, un ajustement d'échelle, etc.

    calibrated_positions = []

    # Exemple: ajuster les positions à une nouvelle échelle ou zone de jeu
    for pos in positions:
        # Calculer la nouvelle position basée sur la calibration
        # C'est un exemple simplifié. Vous devrez peut-être effectuer une transformation plus complexe
        x_new = (pos[0] - calibration_data[0][0]) / (calibration_data[1][0] - calibration_data[0][0])
        y_new = (pos[1] - calibration_data[0][1]) / (calibration_data[2][1] - calibration_data[0][1])
        
        # Ajouter la position calibrée à la liste
        calibrated_positions.append((x_new, y_new))
        
    return calibrated_positions

def start_calibration():
    print("Calibration process started...")
    global is_calibrated, calibration_points, video_source

    if video_source == "webcam":
        points = capture_and_process_image()  # Utilisez la webcam pour la capture
    elif video_source == "file":
        points = capture_and_process_image_from_video(video_path)  # Utilisez le fichier vidéo pour la capture
    else:
        print("Invalid video source")
        return
    
    if points is not None:
        calibration_points = points
        is_calibrated = True
        message = {
            "sender": "python",
            "message": "calibration_success",
            "data": [point.tolist() for point in points]
        }
        json_message = json.dumps(message)
        sock.SendData(json_message)
    else:
        print("Calibration failed")

def change_video_source(source):
    global video_source
    video_source = source

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

def listen_for_data():
    global is_calibrated, calibration_points, capture_running
    while True:
        data = sock.ReadReceivedData()
        if data is not None:
            data_json = json.loads(data)
            print(data_json)
            if(data_json['message'] != None):
                if data_json['message'] == "start_calibration":
                    start_calibration()
                elif data_json['message'] == "start_yolo_hands_detection":
                    start_yolo_hands_detection()
                elif data_json['message'] == "start_detection" and is_calibrated:
                    capture_running = True
                    capture_and_process_player_continuous()
                elif data_json['message'] == "stop_detection":
                    capture_running = False
                elif data_json['message'] == "stop_game":
                    capture_running = False
                    print("stop game")
                elif data_json['message'] == "change_source":
                    new_source = data_json['data'] 
                    change_video_source(new_source)
            pass
        
# Créer et démarrer le thread
listener_thread = threading.Thread(target=listen_for_data)
listener_thread.daemon = True
listener_thread.start()   


sock.SendData('Sent from Python');
while True:
    time.sleep(0.01)
