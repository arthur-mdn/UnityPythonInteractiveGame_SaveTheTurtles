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
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)  # Utilisation du dictionnaire original
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


def auto_detect_edges(image_path):
    image = cv2.imread(image_path)
    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Détecter les marqueurs ArUco
    marker_positions = detect_aruco_markers(gray)

    if marker_positions is None:
        print("Could not detect both ArUco markers")
        return None

    # Récupérer les points à partir des positions des marqueurs
    points = np.array([marker_positions[10][0], marker_positions[10][1], 
                       marker_positions[80][3], marker_positions[80][2]], dtype="float32")

    # Réorganisation des points
    ordered_points = order_points(points)
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

contour_points = auto_detect_edges('floor6.png')

if contour_points is not None:
    orig = cv2.imread('floor6.png')

    warped = four_point_transform(orig, contour_points)

    cv2.imshow("Original", orig)
    cv2.imshow("Warped", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No suitable contour found")
