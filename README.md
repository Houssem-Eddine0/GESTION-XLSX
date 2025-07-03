# 📊 Gestion XLSX — Suite d’Outils pour Excel

Réalisé par **NANE Houssem-Eddine** *(Stagiaire 2025)* 🛠️  
Version actuelle : **v1.7.1**

---

## 🎯 Objectif

**Gestion XLSX** est une suite d’outils développée en Python + Flask pour automatiser et faciliter la manipulation de fichiers Excel.  
Elle regroupe plusieurs modules ciblés : recherche, modification, génération de fichiers TO, et nettoyage de données.

L’application est destinée à être utilisée localement via une interface web simple, ou en version `.exe` compilée pour usage rapide sans Python.

---

## 🧰 Modules disponibles

| Module | Description |
|--------|-------------|
| 🔍 Recherche iPad *(Projet 2)* | Recherche d’un serial dans tous les fichiers d’un dossier |
| ⚙️ Gestion ciblée *(Projet 3)* | Actions précises sur des colonnes Excel (modifier, supprimer, etc.) |
| 🧺 Modifications en masse *(Projet 4)* | Ajout de serials dans des fichiers + favoris |
| 📘 Recherche en masse *(Projet 5)* | Scanner plusieurs serials dans tout un dossier, avec tolérance sur "S" |
| 📤 Génération TO *(Projet 6)* | Génération d’un fichier Excel TO avec feuilles regroupées par équipe |
| 🧪 Préfixe SERIAL *(Projet 7)* | Nettoyage des serials en local (ajout/retrait de "S") – outil JS |

---

## 🛠️ Fonctionnalités principales

- 📁 Favoris par projet : dossiers mémorisables pour éviter les copier-coller
- 🔄 Tolérance sur les variations de serials ("S" en début)
- 📎 Copier facilement le chemin du fichier contenant le résultat
- 🖱️ Interfaces épurées et intuitives par module
- 📤 Export automatique de fichiers `.xlsx` dans `/Documents`
- 🗂️ Moteur robuste avec nettoyage des données foireuses (float, NaN, NaT, etc.)

---

## 🚀 Installation (version développeur)

```bash
git clone https://github.com/ton-utilisateur/Gestion-XLSX.git
cd Gestion-XLSX

pip install -r requirements.txt
python app.py
