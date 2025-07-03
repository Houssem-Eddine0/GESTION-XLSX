@echo off
echo 🔧 Construction de l'exécutable Gestion XLSX...
pyinstaller --name "Gestion XLSX" --onefile --noconsole app.py
echo ✅ Terminé ! L'exécutable se trouve dans le dossier /dist
pause
