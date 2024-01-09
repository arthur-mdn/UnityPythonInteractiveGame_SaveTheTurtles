import cv2
import numpy as np

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
    
    # Convertir l'image en espace colorimétrique HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Définir les plages de couleurs pour le rouge et le blanc en HSV
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    lower_white = np.array([0, 0, 212])
    upper_white = np.array([131, 255, 255])
    
     # Créer des masques pour isoler les régions rouges et blanches
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    
    # Combinez les masques pour obtenir les régions d'intérêt
    mask_combined = cv2.bitwise_or(mask_red, mask_white)

    # Appliquer une fermeture morphologique pour combler les petits trous dans les contours
    kernel = np.ones((5,5), np.uint8)
    mask_closed = cv2.morphologyEx(mask_combined, cv2.MORPH_CLOSE, kernel)

    # Convertir en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Appliquer le masque à l'image en niveaux de gris
    masked_gray = cv2.bitwise_and(gray, gray, mask=mask_closed)
    
    # Flouter l'image pour réduire le bruit
    blurred = cv2.GaussianBlur(masked_gray, (5, 5), 0)
    
    # Détecter les bords
    edged = cv2.Canny(blurred, 30, 150)
    
    cv2.imshow("Edges", edged)
    cv2.waitKey(0)
    
    # Trouver les contours dans l'image des bords, garder seulement les plus grands,
    # et initialiser notre contour de la scène
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    # Boucle sur les contours
    for i, contour in enumerate(contours):
        # Approximer le contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        
        # Créer une copie de l'image pour dessiner seulement ce contour
        single_contour_img = orig.copy()
        cv2.drawContours(single_contour_img, [contour], -1, (0, 255, 0), 3)
        
        # Afficher le nombre de points du contour
        text = f"Contour {i+1}: {len(approx)} points"
        cv2.putText(single_contour_img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        # Afficher l'image
        cv2.imshow(f"Contour {i+1}", single_contour_img)
        cv2.waitKey(0)

        # Si notre contour approximé a quatre points, alors
        # nous pouvons supposer que nous avons trouvé la scène
        if len(approx) == 4:
            screenCnt = approx
            break


    if screenCnt is not None and len(screenCnt) == 4:
        # Créer une copie de l'image pour dessiner seulement ce contour
        single_contour_img = orig.copy()
        cv2.drawContours(single_contour_img, [screenCnt], -1, (0, 255, 0), 3)

        # Dessinez les quatre coins
        for i, point in enumerate(screenCnt):
            x, y = point.ravel()
            cv2.circle(single_contour_img, (x, y), 7, (255, 0, 0), -1)
            cv2.putText(single_contour_img, f"{i+1}", (x - 25, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

        # Afficher le nombre de points du contour
        text = f"Contour {i+1}: 4 points"
        cv2.putText(single_contour_img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        # Afficher l'image
        cv2.imshow(f"Contour {i+1}", single_contour_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
    else:
        print("No contour detected")

contour_points = auto_detect_edges('floor2.png')

# après avoir détecté les contours :
if contour_points is not None:
    orig = cv2.imread('floor.png')  # Remplacez par le chemin de votre image si différent
    
    # Dessiner les points du contour dans l'ordre
    for i, point in enumerate(contour_points):
        x, y = point
        cv2.circle(orig, (x, y), 7, (0, 255, 0), -1)
        cv2.putText(orig, f"{i+1}", (x - 25, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

    # appliquer la transformation à quatre points
    warped = four_point_transform(orig, contour_points)
    
    # afficher l'image originale et l'image transformée
    cv2.imshow("Original", orig)
    cv2.imshow("Warped", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No suitable contour found")

