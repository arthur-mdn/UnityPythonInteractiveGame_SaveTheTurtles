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

## Utilisation
### Unity
Ouvrez le projet `/UnityProject_save_the_turtles` avec **Unity `2022.3.10f1`** 
Ouvrez la scène `BallGame` pour démarrer.

### Python
#### Pour lancer l'écoute du serveur python (sur Windows)

```bash
python server.py
```

#### Retour sur Unity
Une fois l'écoute du serveur python lancée, démarrer la scène avec le bouton play.