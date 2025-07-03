import os
import json
import pandas as pd
from flask import render_template, jsonify

COLONNES_SERIAL = ["SERIAL", "SERIAL NUMBER", "SN", "S/N"]
COLONNES_ASSET = ["ASSET", "ASSET TAG", "TAG", "ASSETTAG"]
FAV_FILE = "favoris_recherche.json"

def charger_favoris():
    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def ajouter_favori(request):
    chemin = request.form.get("chemin", "").strip()
    favoris = charger_favoris()
    if request.form.get("action") == "ajouter" and chemin and chemin not in favoris:
        favoris.append(chemin)
    elif request.form.get("action") == "supprimer" and chemin in favoris:
        favoris.remove(chemin)
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favoris, f, indent=2)
    return jsonify({"success": True, "favoris": favoris})

def handler(request):
    favoris = charger_favoris()

    if request.method == "POST":
        chemin = request.form.get("chemin", "").strip()
        valeur = request.form.get("serial", "").strip().lower()
        resultats = []

        if not os.path.isdir(chemin):
            return jsonify({"erreur": "❌ Chemin invalide ou introuvable."})

        for racine, _, fichiers in os.walk(chemin):
            for fichier in fichiers:
                if fichier.endswith(".xlsx"):
                    chemin_fichier = os.path.join(racine, fichier)
                    try:
                        feuilles = pd.read_excel(chemin_fichier, sheet_name=None, engine="openpyxl")
                    except:
                        continue

                    for nom_feuille, df in feuilles.items():
                        try:
                            df.columns = [str(c).strip().upper() for c in df.columns]
                            for col in df.columns:
                                serie = df[col].astype(str).str.strip().str.lower()
                                if valeur in serie.values:
                                    lignes = df[serie == valeur]
                                    for index, ligne in lignes.iterrows():
                                        ligne_dict = {k: str(v) for k, v in ligne.items() if str(v).strip().lower() not in ("nan", "nat", "")}
                                        if not ligne_dict:
                                            continue
                                        resultats.append({
                                            "fichier": fichier,
                                            "feuille": nom_feuille,
                                            "colonne": col,
                                            "ligne_excel": int(index) + 2,
                                            "ligne": ligne_dict,
                                            "chemin_complet": os.path.abspath(chemin_fichier)
                                        })
                        except:
                            continue

        return jsonify(resultats if resultats else {"erreur": "🔍 Aucune correspondance trouvée."})

    return render_template("projet2.html", favoris=favoris)
