import cv2
import numpy as np

# Liste pour stocker les points source
src_points = []

def click_event(event, x, y, flags, param):
    global src_points
    if event == cv2.EVENT_LBUTTONDOWN:
        src_points.append((x, y))
        cv2.circle(input_image, (x, y), 20, (0, 0, 255), -1)
        cv2.imshow('Image d\'origine', input_image)

# Charger l'image d'entrée
input_image = cv2.imread('img.png')
base_image = input_image.copy()

# Créer une fenêtre pour l'image d'origine et associer la fonction de clic
cv2.imshow('Image d\'origine', input_image)
cv2.setMouseCallback('Image d\'origine', click_event)

# Attendre que l'utilisateur clique sur au moins 4 points
while len(src_points) < 4:
    cv2.waitKey(1)

# Calcul de Résolution de la sortie
width_AD = np.sqrt(((src_points[0][0] - src_points[3][0]) ** 2) + ((src_points[0][1] - src_points[3][1]) ** 2))
width_BC = np.sqrt(((src_points[1][0] - src_points[2][0]) ** 2) + ((src_points[1][1] - src_points[2][1]) ** 2))
maxWidth = max(int(width_AD), int(width_BC))
 
 
height_AB = np.sqrt(((src_points[0][0] - src_points[1][0]) ** 2) + ((src_points[0][1] - src_points[1][1]) ** 2))
height_CD = np.sqrt(((src_points[2][0] - src_points[3][0]) ** 2) + ((src_points[2][1] - src_points[3][1]) ** 2))
maxHeight = max(int(height_AB), int(height_CD))


# Définir les coordonnées 2D dans l'image de sortie
dst_points = np.float32([[0, 0], [maxWidth-1, 0], [maxWidth-1, maxHeight-1], [0, maxHeight-1]])

# Calculer la matrice de projection
M = cv2.getPerspectiveTransform(np.float32(src_points), dst_points)

# Appliquer la projection
output_image = cv2.warpPerspective(base_image, M, (maxWidth, maxHeight))

resize = cv2.resize(output_image, (maxHeight, maxWidth))

# Afficher l'image projetée
cv2.imwrite('./output.png', resize)
cv2.imshow('Image projetée', resize)
cv2.waitKey(0)
cv2.destroyAllWindows()