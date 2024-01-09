import cv2
import numpy as np

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
    
    # Trouver les contours dans l'image des bords, garder seulement les plus grands,
    # et initialiser notre contour de la scène
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    # Boucle sur les contours
    for contour in contours:
        # Approximer le contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        # Si notre contour approximé a quatre points, alors
        # nous pouvons supposer que nous avons trouvé la scène
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print("No contour detected")
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)

    # Montrer le contour (s'il y en a un)
    cv2.imshow("Outline", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if detected == 1:
        return screenCnt.reshape(4, 2)
    else:
        return None

# Remplacez 'floor.png' par votre image
contour_points = auto_detect_edges('floor.png')
if contour_points is not None:
    # Vous pouvez maintenant utiliser contour_points comme vos points src pour la transformation de perspective
    print(contour_points)
else:
    print("No suitable contour found")
