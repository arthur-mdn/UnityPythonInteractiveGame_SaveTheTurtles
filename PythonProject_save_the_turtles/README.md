### Pour lancer l'écoute du serveur python (sur Windows)

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