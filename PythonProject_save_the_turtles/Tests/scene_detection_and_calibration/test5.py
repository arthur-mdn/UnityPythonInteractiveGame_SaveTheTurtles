import cv2
import numpy as np

# Remplacez ceci par une valeur appropriée pour vos images
MIN_CONTOUR_AREA = 50000
def order_points(pts):
    # Initialiser une liste de coordonnées qui seront ordonnées
    # tel que le premier point sera en haut à gauche, le second en haut à droite,
    # le troisième sera en bas à droite et le quatrième en bas à gauche
    rect = np.zeros((4, 2), dtype="float32")

    # le point avec la somme la plus petite sera notre point en haut à gauche
    # le point avec la somme la plus grande sera notre point en bas à droite
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # maintenant, calculons la différence entre les points,
    # le point avec la différence la plus petite sera en haut à droite
    # le point avec la différence la plus grande sera en bas à gauche
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def four_point_transform(image, pts):
    # obtenir un ordre cohérent des points et les préparer pour la transformation
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # calculer la largeur de la nouvelle image qui sera la
    # distance maximale entre le bas à droite et le bas à gauche
    # x-coordonnées ou les haut à droite et haut à gauche x-coordonnées
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # calculer la hauteur de la nouvelle image qui sera la
    # distance maximale entre le haut à droite et le bas à droite
    # y-coordonnées ou le haut à gauche et le bas à gauche y-coordonnées
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # maintenant que nous avons les dimensions de la nouvelle image, construisons
    # l'ensemble des points pour obtenir la vue "de face", c'est-à-dire
    # la vue de haut de notre image, en spécifiant les points dans
    # le sens horaire à partir du haut à gauche
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # calculer la matrice de transformation de perspective et appliquer
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # retourner l'image mise en perspective
    return warped
def auto_detect_edges(image_path):
    # Charger l'image
    image = cv2.imread(image_path)
    orig = image.copy()
    
    # Convertir en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Flouter l'image pour réduire le bruit
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Détecter les bords
    edged = cv2.Canny(blurred, 30, 150)
    
    cv2.imshow("Edges", edged)
    cv2.waitKey(0)

    # Trouver les contours dans l'image des bords, et initialiser notre contour de la scène
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    valid_contours = []

    # Boucle sur les contours
    for contour in contours:
        # Calculer l'aire du contour
        area = cv2.contourArea(contour)

        # Ignorer les petits contours
        if area < MIN_CONTOUR_AREA:
            continue

        # Approximer le contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        # Le contour doit être fermé et avoir quatre points
        if len(approx) == 4:
            valid_contours.append(approx)

    # Dessiner les contours valides
    cv2.drawContours(image, valid_contours, -1, (0, 255, 0), 3)

    # Afficher l'image
    cv2.imshow("Valid Contours", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Retourner le premier contour valide si disponible
    if valid_contours:
        return valid_contours[0].reshape(4, 2)
    else:
        return None

# Remplacez 'floor.png' par votre image
contour_points = auto_detect_edges('floor3.png')
if contour_points is not None:
    print(contour_points)
else:
    print("No suitable contour found")
