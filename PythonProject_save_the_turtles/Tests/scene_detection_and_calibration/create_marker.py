# Assurez-vous d'importer les bons modules
import cv2
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl

# Création du dictionnaire ArUco
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# Générer le premier marqueur
fig = plt.figure()
nx = 1
ny = 1
for i in range(1, nx*ny+1):
    ax = fig.add_subplot(ny,nx, i)
    img = aruco.drawMarker(aruco_dict, i, 700) # Remplacer 'i' par l'ID que vous voulez pour votre marqueur
    plt.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")
    ax.axis("off")

plt.savefig("marker1.png")
plt.show()

# Générer le second marqueur
fig = plt.figure()
for i in range(2, nx*ny+2): # Choisissez un ID différent pour le second marqueur
    ax = fig.add_subplot(ny,nx, i-1)
    img = aruco.drawMarker(aruco_dict, i, 700)
    plt.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")
    ax.axis("off")

plt.savefig("marker2.png")
plt.show()
