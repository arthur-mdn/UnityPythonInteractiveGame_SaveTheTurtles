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

def detect_color(image, lower, upper):
    mask = cv2.inRange(image, lower, upper)
    kernel = np.ones((5,5), np.uint8)
    mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        biggest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(biggest_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        return (cX, cY)
    else:
        return None

def order_points_with_color_squares(points, green_square, blue_square):
    # Calculer la distance de chaque point aux carrés de couleur
    green_distances = np.sqrt((points[:, 0] - green_square[0]) ** 2 + (points[:, 1] - green_square[1]) ** 2)
    blue_distances = np.sqrt((points[:, 0] - blue_square[0]) ** 2 + (points[:, 1] - blue_square[1]) ** 2)

    # Identifier les points les plus proches de chaque carré
    top_left = points[np.argmin(green_distances)]  # le plus proche du carré vert
    bottom_right = points[np.argmin(blue_distances)]  # le plus proche du carré bleu

    # Créer une liste des points restants
    remaining = [pt for pt in points if (pt != top_left).any() and (pt != bottom_right).any()]

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

    # Plages de couleurs pour le rouge, le vert et le bleu
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    lower_green = np.array([40, 40, 70])  # À ajuster
    upper_green = np.array([80, 255, 255])  # À ajuster
    lower_blue = np.array([100, 150, 0])  # À ajuster
    upper_blue = np.array([140, 255, 255])  # À ajuster

    # Détection des carrés de couleur
    green_square = detect_color(hsv, lower_green, upper_green)
    blue_square = detect_color(hsv, lower_blue, upper_blue)

    if green_square is None or blue_square is None:
        print("Could not detect both color squares")
        return None

    # Détection des contours rouges
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5,5), np.uint8)
    mask_closed = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    masked_gray = cv2.bitwise_and(gray, gray, mask=mask_closed)
    blurred = cv2.GaussianBlur(masked_gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)

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
        ordered_points = order_points_with_color_squares(points, green_square, blue_square)
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


contour_points = auto_detect_edges('floor5.png')

if contour_points is not None:
    orig = cv2.imread('floor5.png')
    
    warped = four_point_transform(orig, contour_points)

    cv2.imshow("Original", orig)
    cv2.imshow("Warped", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No suitable contour found")
