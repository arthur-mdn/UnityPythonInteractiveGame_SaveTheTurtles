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
webcam_index = 0 # 0 pour la première webcam, 1 pour la deuxième webcam, etc.
webcam_backend = cv2.CAP_DSHOW # cv2.CAP_DSHOW pour les webcams Windows, Utilisez cv2.CAP_ANY si vous rencontrez des problèmes
video_path = "Elements/wall_vid.mp4"
show_calibrate_result = False
show_live_transformed_calibrated_positions = True
alpha = 0.5  # Facteur de lissage, ajustez selon les besoins
smoothed_left_hand = [0, 0]  # Initialiser avec une position de départ
smoothed_right_hand = [0, 0]  # Initialiser avec une position de départ

def add_position(smoothed_position, new_position):
    smoothed_position[0] = alpha * new_position[0] + (1 - alpha) * smoothed_position[0]
    smoothed_position[1] = alpha * new_position[1] + (1 - alpha) * smoothed_position[1]

def get_smoothed_position(smoothed_position):
    return smoothed_position

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

def start_yolo_hands_detection(to_launch_new_game=False):
    global model
    cap = cv2.VideoCapture(webcam_index, webcam_backend)
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
            if to_launch_new_game:
                message = {
                    "sender": "python",
                    "message": "start_new_game"
                }
            else:
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
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
    aruco_params = cv2.aruco.DetectorParameters()

    # Détecter les marqueurs
    corners, ids, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=aruco_params)

    if ids is not None:
        # S'assurer que les marqueurs requis sont détectés
        required_markers = [10, 150, 200, 80]
        marker_positions = {}

        for i, marker_id in enumerate(ids.flatten()):
            if marker_id in required_markers:
                # Obtenir les coins du marqueur
                marker_corner = corners[i].reshape((4, 2))

                # Sélectionner un coin spécifique basé sur l'ID du marqueur
                if marker_id == 10:  # Marqueur haut gauche
                    selected_corner = marker_corner[0]  # Coin supérieur gauche
                elif marker_id == 150:  # Marqueur haut droit
                    selected_corner = marker_corner[1]  # Coin supérieur droit
                elif marker_id == 200:  # Marqueur bas gauche
                    selected_corner = marker_corner[3]  # Coin inférieur gauche
                elif marker_id == 80:  # Marqueur bas droit
                    selected_corner = marker_corner[2]  # Coin inférieur droit

                marker_positions[marker_id] = selected_corner

        if all(marker in marker_positions for marker in required_markers):
            # Ordonner les coins dans l'ordre haut gauche, haut droit, bas droit, bas gauche
            ordered_positions = [
                marker_positions[10],    # Haut gauche
                marker_positions[150],   # Haut droit
                marker_positions[80],    # Bas droit
                marker_positions[200]    # Bas gauche
            ]
            return np.array(ordered_positions, dtype=np.float32)
        else:
            print("Missing required markers")
            return None
    else:
        print("No markers found")
        return None

def auto_detect_edges(image):
    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    marker_positions = detect_aruco_markers(gray)
    if marker_positions is None:
        print("Could not detect all required ArUco markers")
        return None

    return marker_positions

def capture_and_process_image(tries=20):
    global show_calibrate_result
    for _ in range(tries):
        # Ouvrir la caméra
        cap = cv2.VideoCapture(webcam_index, webcam_backend)

        # Tenter de capturer une image
        success, frame = cap.read()

        # Toujours libérer la caméra après la capture
        cap.release()

        if success:
            # Utiliser la fonction auto_detect_edges pour traiter l'image capturée
            processed_points = auto_detect_edges(frame)
            if processed_points is not None:
                print("Calibration points detected:", processed_points)
                # Dessiner les points de calibration sur l'image
                for point in processed_points:
                    cv2.circle(frame, (int(point[0]), int(point[1])), 5, (0, 255, 0), -1)  # Dessiner un cercle vert
                # Afficher l'image avec les points de calibration
                if show_calibrate_result:
                    cv2.imshow("Calibration Points", frame)
                    cv2.waitKey(0)  # Attendre une touche pour fermer
                    cv2.destroyAllWindows()
                return processed_points
            else:
                print("Failed to detect edges on try:", _ + 1)
        else:
            print("Failed to capture image on try:", _ + 1)

    # Si la calibration a échoué après toutes les tentatives
    print("Calibration failed after {} tries".format(tries))
    return None


def capture_and_process_image_from_video(video_path, tries=10):
    # Ouvrir le fichier vidéo
    cap = cv2.VideoCapture(video_path)

    for _ in range(tries):
        # Lire une image du flux vidéo
        success, frame = cap.read()

        if success:
            # Utiliser la fonction auto_detect_edges pour traiter l'image capturée
            processed_points = auto_detect_edges(frame)
            if processed_points is not None:
                print("Calibration points detected:", processed_points)
                return processed_points
            else:
                print("Failed to detect edges on try:", _ + 1)
        else:
            print("Failed to read frame on try:", _ + 1)

    # Fermer le fichier vidéo après les tentatives
    cap.release()

    # Si la calibration a échoué après toutes les tentatives
    print("Calibration failed after {} tries".format(tries))
    return None

def transform_perspective(points, src_coords, dst_coords):
    # Convertir la liste de points en tableau NumPy
    points_array = np.array(points, dtype="float32").reshape(-1, 1, 2)

    # Calculer la matrice de transformation de perspective
    M = cv2.getPerspectiveTransform(src_coords, dst_coords)

    # Appliquer la transformation de perspective
    transformed_points = cv2.perspectiveTransform(points_array, M)

    # Redimensionner pour retourner une liste de points
    return transformed_points.reshape(-1, 2)


def handle_incoming_message(data):
    global capture_running
    data_json = json.loads(data)

    if data_json['message'] == 'stop_game':
        print("Arrêt du jeu demandé.")
        capture_running = False
        message = {
            "sender": "python",
            "message": "game_stopped",
            "data": True
        }
        json_message = json.dumps(message)
        sock.SendData(json_message)

def capture_and_process_player_continuous():
    global capture_running, calibration_points, video_source, show_live_transformed_calibrated_positions

    if calibration_points is None:
        print("Calibration is not yet done.")
        return

    src_coords = np.array(calibration_points, dtype="float32")
    dst_coords = np.array([[0, 0], [640, 0], [640, 360], [0, 360]], dtype="float32")

    if video_source == "webcam":
        cap = cv2.VideoCapture(webcam_index, webcam_backend)
    elif video_source == "file":
        cap = cv2.VideoCapture(video_path)
    else:
        print("Invalid video source")
        return

    while capture_running:
        success, frame = cap.read()
        if not success:
            print("Failed to read frame from video")
            break
        data = sock.ReadReceivedData()
        if data:
            handle_incoming_message(data)
        if not capture_running:
            print("Capture stopped")
            break

        transformed_hand_positions = []

        results = model(frame)
        keypoints = results[0].keypoints.xy.tolist()

        hand_positions = []
        for person in keypoints:
            if len(person) > 0:
                left_hand = person[9]  # left_wrist
                right_hand = person[10]  # right_wrist
                if 0 < left_hand[0] < frame.shape[1] and 0 < left_hand[1] < frame.shape[0]:
                    add_position(smoothed_left_hand, left_hand)
                if 0 < right_hand[0] < frame.shape[1] and 0 < right_hand[1] < frame.shape[0]:
                    add_position(smoothed_right_hand, right_hand)

        if smoothed_left_hand and smoothed_right_hand:
            smoothed_positions = [smoothed_left_hand, smoothed_right_hand]
            transformed_hand_positions = transform_perspective(smoothed_positions, src_coords, dst_coords)

            message = {
                "sender": "python",
                "message": "hands_positions",
                "data": [[pos[0] / 640, pos[1] / 360] for pos in transformed_hand_positions]
            }
            json_message = json.dumps(message)
            sock.SendData(json_message)

        if show_live_transformed_calibrated_positions:
            # Dessiner les mains calibrées sur une nouvelle image
            calib_frame = np.zeros((360, 640, 3), dtype=np.uint8)
            for pos in transformed_hand_positions:
                cv2.circle(calib_frame, (int(pos[0]), int(pos[1])), 10, (255, 0, 0), -1)

    cap.release()
    cv2.destroyAllWindows()



def calibrate_positions(positions, calibration_data):
    calibrated_positions = []

    # Calculer la matrice de transformation en utilisant les coordonnées des coins de la scène calibrée
    src_coords = np.array([
        calibration_data["top_left"],
        calibration_data["top_right"],
        calibration_data["bottom_left"],
        calibration_data["bottom_right"]
    ], dtype="float32")

    for pos in positions:
        # Appliquer la transformation de perspective
        transformed_pos = transform_perspective([pos], src_coords, dst_coords)[0]

        # Ajouter la position calibrée à la liste
        calibrated_positions.append(transformed_pos)
    return calibrated_positions


def start_calibration():
    print("Calibration process started...")
    global is_calibrated, calibration_points, video_source

    if is_calibrated and calibration_points is not None:
        print("Already calibrated")
        message = {
            "sender": "python",
            "message": "calibration_success",
            "data": [point.tolist() for point in calibration_points]
        }
        json_message = json.dumps(message)
        sock.SendData(json_message)
        return
    if video_source == "webcam":
        points = capture_and_process_image()  # Utiliser la webcam pour la capture
    elif video_source == "file":
        points = capture_and_process_image_from_video(video_path)  # Utiliser le fichier vidéo pour la capture
    else:
        print("Invalid video source")
        return

    if points is not None:
        calibration_points = points
        is_calibrated = True
        print("Calibration successful")
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
                if data_json['message'] == "test_connection":
                    message = {
                        "sender": "python",
                        "message": "connection_ok",
                        "data": ""
                    }
                    json_message = json.dumps(message)
                    sock.SendData(json_message)
                elif data_json['message'] == "start_calibration":
                    start_calibration()
                elif data_json['message'] == "start_yolo_hands_detection":
                    start_yolo_hands_detection()
                elif data_json['message'] == "start_yolo_hands_detection_to_launch_new_game":
                    start_yolo_hands_detection(True)
                elif data_json['message'] == "start_detection" and is_calibrated:
                    capture_running = True
                    capture_and_process_player_continuous()
                elif data_json['message'] == "change_source":
                    new_source = data_json['data']
                    change_video_source(new_source)
            pass

# Créer et démarrer le thread
listener_thread = threading.Thread(target=listen_for_data)
listener_thread.daemon = True
listener_thread.start()


sock.SendData('Sent from Python')
while True:
    time.sleep(0.01)
