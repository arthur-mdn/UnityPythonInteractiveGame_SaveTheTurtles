# UnityPythonInteractiveGame_SaveTheTurtles

## Introduction
Ce projet consite à relier la bibliothèque Python3 `Ultralytics YoloV8` utilisée pour détecter un joueur sur une source vidéo et en extraire les positions des mains. Puis communiquer avec Unity pour créer un jeu interactif en utilisant les données détectées.


## Installation
Cloner ce repository en local
```bash
git clone https://github.com/arthur-mdn/UnityPythonInteractiveGame_SaveTheTurtles.git
```

## Utilisation
### Unity
Ouvrez le projet `/UnityProject_save_the_turtles` avec **Unity `2022.3.10f1`** 
Ouvrez la scène `BallGame` pour démarrer.

### Python
#### Pour lancer l'écoute du serveur python (sur Windows)

Avec la variable d'environnement python311
```bash
python311 -m venv saveTurtles 
```
Sans la variable d'environnement python311
```bash
Z:\chemin\complet\vers\l\installation\Python\Python311\python.exe -m venv saveTurtles
```
Une fois l'environnement python 3.11 créé, on lance l'installation des paquets et on active le serveur d'écoute
```bash
python311 -m venv saveTurtles 
ou Z:\chemin\complet\vers\l\installation\Python\Python311\python.exe -m venv saveTurtles
.\saveTurtles\Scripts\activate
pip install -r .\requirements.txt
python server.py
```

#### Retour sur Unity
Une fois l'écoute du serveur python lancée, démarrer la scène avec le bouton play.