import cv2
import numpy as np

def auto_detect_edges(image):
    # Convertir en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Améliorer le contraste
    equ = cv2.equalizeHist(gray)
    
    # Seuillage adaptatif
    thresh = cv2.adaptiveThreshold(equ, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # Opérations morphologiques pour éliminer le bruit
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 2)
    
    # Élargir la zone de l'image pour être sûr que le fond est présent
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    
    # Trouver les contours
    contours, _ = cv2.findContours(sure_bg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Si aucun contour n'est trouvé, retourner None
    if not contours:
        return None
    
    # Trouver le plus grand contour en supposant qu'il représente la scène
    max_contour = max(contours, key=cv2.contourArea)
    
    # Approximer le contour pour obtenir 4 coins
    peri = cv2.arcLength(max_contour, True)
    corners = cv2.approxPolyDP(max_contour, 0.02 * peri, True)
    
    # Si nous n'obtenons pas 4 coins, retourner None
    if len(corners) != 4:
        return None
    
    return corners.reshape(4, 2)

image = cv2.imread('img2.jpeg')
contour_points = auto_detect_edges(image)

if contour_points is not None:
    # Vous pouvez maintenant utiliser contour_points comme vos points src pour la transformation de perspective
    print(contour_points)
    cv2.drawContours(image, [contour_points], -1, (0, 255, 0), 2)
    cv2.imshow('Detected Scene', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No suitable contour found")
