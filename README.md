# UnityPythonInteractiveGame_SaveTheTurtles

## Introduction
Ce projet consite à relier la bibliothèque Python3 `Ultralytics YoloV8` utilisée pour détecter un joueur sur une source vidéo et en extraire les positions des mains. Puis communiquer avec Unity pour créer un jeu interactif en utilisant les données détectées.

# Prérequis
- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [Unity `2022.3.10f1`](https://unity3d.com/fr/get-unity/download/archive)

## Installation
Cloner ce repository en local
```bash
git clone https://github.com/arthur-mdn/UnityPythonInteractiveGame_SaveTheTurtles.git
```
### Installer les dépendances Python (3.11) sur Windows

Se rendre dans le dossier contenant le projet Python
```bash
cd PythonProject_save_the_turtles
```
- #### Si vous avez une variable d'environnement "python311"
    ```bash
    python311 -m venv saveTurtles 
    ```
- #### Si vous n'avez pas de variable d'environnement "python311"
    ```bash
    Z:\chemin\complet\vers\l\installation\Python\Python311\python.exe -m venv saveTurtles
    ```
Une fois l'environnement Python créé, on l'active
```bash
.\saveTurtles\Scripts\activate
```
Puis on lance l'installation des paquets
```bash
pip install -r .\requirements.txt
```

### Python
#### Pour lancer l'écoute du serveur python (sur Windows)

```bash
python server.py
```

## Utilisation
### Unity
Ouvrez le projet `/UnityProject_save_the_turtles` avec **Unity `2022.3.10f1`** 
Ouvrez la scène `StartScreen` pour démarrer.
Lancez la scène avec le bouton play.

## Fonctionnement sur Unity
Au premier lancement, il va falloir "lever les mains en l'air" pour lancer une calibration.
Écartez-vous du champ de vision de la caméra pour lancer la calibration.
Une fois la calibration terminée, la scène de jeu se lance automatiquement.

## Fonctionnement sur un build du jeu
- Lancez un build du jeu en utilisant le menu Unity `File > Build`.
- Fermez le moteur Unity après le build.
- Lancez le serveur Python.
- Lancez le jeu en utilisant le fichier `.exe` généré.
- Déplacez la fenêtre de jeu sur un écran ayant la résolution 1920x1080 (important).

## Problèmes connus
### Scène vide après le lancement du build Unity.
> ⚠️ Assurez-vous que l'écran sur lequel est projeté le jeu est configuré avec la résolution 1920x1080.
> 
### Écran noir après le lancement du build Unity.
> ⚠️ Assurez-vous que le moteur Unity est FERMÉ lors du build.

> ⚠️ Assurez-vous que le serveur Python est bien lancé.

> ⚠️ Assurez-vous qu'aucun autre programme n'utilise la webcam.

> ⚠️ Assurez-vous qu'aucun autre programme n'utilise les ports d'écoutes (3000 et 3001). 
>
### Impossible d'utiliser la webcam sur MacOS
> ⚠️ Assurez-vous de configurer la backend de la caméra dans le fichier `server.py` pour utiliser `CAP_ANY` au lieu de `CAP_DSHOW`.

Vous devez modifier la ligne suivante dans ``server.py``
```python
webcam_backend = cv2.CAP_DSHOW
```
Par la ligne suivante
```python
webcam_backend = cv2.CAP_ANY
```