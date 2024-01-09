import cv2
import numpy as np

def nothing(x):
    pass

# Demander à l'utilisateur de choisir la source de l'image
print("Choisissez la source de l'image :")
print("1: Webcam")
print("2: Image 'wall.jpg'")
choice = input("Entrez votre choix (1 ou 2): ")

# Initialiser la capture vidéo si le choix est la webcam
if choice == '1':
    cap = cv2.VideoCapture(0)

# Création de fenêtres pour les sliders
cv2.namedWindow('Trackbars')
cv2.createTrackbar('Lower Hue', 'Trackbars', 0, 180, nothing)
cv2.createTrackbar('Lower Saturation', 'Trackbars', 120, 255, nothing)
cv2.createTrackbar('Lower Value', 'Trackbars', 70, 255, nothing)
cv2.createTrackbar('Upper Hue', 'Trackbars', 10, 180, nothing)
cv2.createTrackbar('Upper Saturation', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('Upper Value', 'Trackbars', 255, 255, nothing)

while True:
    # Lire l'image depuis la source choisie
    if choice == '1':
        ret, frame = cap.read()
        if not ret:
            break
    else:
        frame = cv2.imread('Elements/wall.jpg')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Lecture des valeurs des sliders
    l_h = cv2.getTrackbarPos('Lower Hue', 'Trackbars')
    l_s = cv2.getTrackbarPos('Lower Saturation', 'Trackbars')
    l_v = cv2.getTrackbarPos('Lower Value', 'Trackbars')
    u_h = cv2.getTrackbarPos('Upper Hue', 'Trackbars')
    u_s = cv2.getTrackbarPos('Upper Saturation', 'Trackbars')
    u_v = cv2.getTrackbarPos('Upper Value', 'Trackbars')

    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    key = cv2.waitKey(1)
    if key == 27:
        break

if choice == '1':
    cap.release()
cv2.destroyAllWindows()
