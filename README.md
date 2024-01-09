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

### Python
#### Lancer le serveur d'écoute
Pour lancer l'écoute du serveur python (sur Windows) :
```bash
cd PythonProject
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Scripts\Activate.ps1
```