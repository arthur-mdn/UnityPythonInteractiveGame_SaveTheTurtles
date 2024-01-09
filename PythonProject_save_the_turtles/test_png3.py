from ultralytics import YOLO
import cv2
import numpy as np

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

#     widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
#     widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
#     maxWidth = max(int(widthA), int(widthB))
# 
#     heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
#     heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
#     maxHeight = max(int(heightA), int(heightB))
    # Définir la résolution de sortie souhaitée
    maxWidth = 1366
    maxHeight = 768

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


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


def auto_detect_edges(image_path):
    image = cv2.imread(image_path)
    orig = image.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

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

def process_frame(frame):
    # Vous pouvez ajuster la résolution si nécessaire
    # frame = cv2.resize(frame, (1366, 768))

    orig = frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    # Détection des contours rouges
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5,5), np.uint8)
    mask_closed = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    masked_gray = cv2.bitwise_and(gray, gray, mask=mask_closed)
    blurred = cv2.GaussianBlur(masked_gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    marker_positions = detect_aruco_markers(gray)
    if marker_positions is None:
        print("Could not detect both ArUco markers")
        return frame

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is not None:
        points = screenCnt.reshape(4, 2)
        ordered_points = order_points_with_aruco_markers(points, marker_positions)

        # Vérifiez si ordered_points est None avant de continuer
        if ordered_points is None:
            print("Could not order points")
            return frame

        # Dessiner les coins sur le frame
        for i, point in enumerate(ordered_points):
            x, y = point
            cv2.circle(frame, (int(x), int(y)), 7, (0, 255, 0), -1)  # Dessine un cercle vert autour du coin
            cv2.putText(frame, f"{i+1}", (int(x) - 25, int(y) - 25), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)  # Numérote le coin

        return frame
    else:
        print("No suitable contour found")
        return frame


def detect_and_draw_player(frame, backSub):
    # Appliquer la soustraction d'arrière-plan
    fgMask = backSub.apply(frame)
    # Appliquer un seuil pour obtenir une image binaire du mouvement
    _, thresh = cv2.threshold(fgMask, 200, 255, cv2.THRESH_BINARY)
    # Trouver les contours des objets en mouvement
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Supposons que le joueur est le plus grand objet en mouvement
    if contours:
        # Trouver le plus grand contour qui sera notre joueur
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        # Dessiner un rectangle autour du joueur
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Calculer le centre du joueur
        player_position = (x + w//2, y + h//2)
        cv2.circle(frame, player_position, 5, (255, 0, 0), -1)  # Dessine un cercle rouge pour indiquer le centre
    else:
        player_position = None
    return frame, player_position

def get_feet_coordinates(keypoints, image_shape):
    print(keypoints)
    height, width, _ = image_shape
    # Use keypoints directly without calling numpy()
    feet = keypoints.xy[0, -2:, :2].reshape(-1, 2)
    feet_coordinates = [(int(x * width), int(y * height)) for x, y in feet]

    return feet_coordinates



def main():
     # Créez une instance YOLOv8
    yolo = YOLO(model='yolov8n-pose.pt')

    # Chargez votre image PNG
    image_path = 'floor6.png'
    frame = cv2.imread(image_path)

    # Effectuez la prédiction avec YOLOv8
    results = yolo.predict(frame)
    #print(results)

    if isinstance(results, list) and len(results):
        # Accédez au premier objet Results
        result_obj = results[0]
        keypoints = result_obj.keypoints.numpy()  # Obtenir les keypoints sous forme de numpy array
        #print(keypoints)
        feet_coordinates = get_feet_coordinates(keypoints, frame.shape)
        print (feet_coordinates)
        # Utilisez la transformation de perspective ici si nécessaire
        # floor_transformed = four_point_transform(frame, points_perspective)
        # Ici vous pouvez dessiner les cercles rouges sur floor_transformed si vous avez appliqué une transformation

        # Dessinez des cercles rouges sur les emplacements des pieds
        for (x, y) in feet_coordinates:
            cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)  # Dessine un cercle rouge sur chaque pied

        # Affichez l'image
        cv2.imshow('YOLOv8 Pose Detection', frame)
        cv2.waitKey(0)
    else:
        print("Les résultats ne sont pas dans le format attendu.")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()




