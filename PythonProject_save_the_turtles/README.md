### Installer les dépendances Python (3.11) sur Windows

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

### Pour lancer l'écoute du serveur python (sur Windows)
```bash
python server.py
```
