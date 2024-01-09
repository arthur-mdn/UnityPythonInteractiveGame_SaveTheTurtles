import cv2
import numpy as np

def nothing(x):
    pass

# Créez une fenêtre avec des trackbars pour les valeurs HSV
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

while True:
    # Commencez ici à capter votre image avec OpenCV

    # Convertissez l'image de RGB à HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Obtenez les positions actuelles des trackbars
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    # Définissez les plages inférieure et supérieure pour la segmentation
    lower_color = np.array([l_h, l_s, l_v])
    upper_color = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Affichez l'image et le masque
    cv2.imshow("Original", image)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == 27:  # Touche "ESC" pour quitter
        break

cv2.destroyAllWindows()
