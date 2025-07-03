import os
import json
import pandas as pd
from flask import request, render_template, jsonify

FAV_FILE = "favoris_recherche.json"

def charger_favoris():
    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def update_favoris(request):
    chemin = request.form.get("chemin", "").strip()
    favoris = charger_favoris()
    if request.form.get("action") == "ajouter" and chemin and chemin not in favoris:
        favoris.append(chemin)
    elif request.form.get("action") == "supprimer" and chemin in favoris:
        favoris.remove(chemin)
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favoris, f, indent=2)
    return jsonify({"success": True, "favoris": favoris})

# 🔍 Fonction de tolérance "S"
def serial_variants(s):
    s = s.strip().lower()
    return {s, "s" + s} if not s.startswith("s") else {s, s[1:]}

def handler(request):
    favoris = charger_favoris()

    if request.method == "POST":
        chemin = request.form.get("chemin", "").strip()
        bloc_serials = request.form.get("serials", "").strip()

        if not chemin or not os.path.isdir(chemin):
            return jsonify({"erreur": "❌ Chemin invalide ou introuvable."})
        if not bloc_serials:
            return jsonify({"erreur": "❌ Aucun serial fourni."})

        serials = [s.strip().lower() for s in bloc_serials.splitlines() if s.strip()]
        serials_set = set(serials)
        non_trouves = set(serials_set)
        mapping = {}  # (fichier, feuille, chemin) → serials

        for racine, _, fichiers in os.walk(chemin):
            for fichier in fichiers:
                if not fichier.lower().endswith(".xlsx"):
                    continue
                chemin_fichier = os.path.join(racine, fichier)
                try:
                    feuilles = pd.read_excel(chemin_fichier, sheet_name=None, engine="openpyxl")
                except:
                    continue

                for nom_feuille, df in feuilles.items():
                    try:
                        df.columns = [str(c).strip().upper() for c in df.columns]
                        for col in df.columns:
                            contenu = df[col].astype(str).str.strip().str.lower().tolist()
                            contenu_set = set(contenu)
                            for serial in serials_set:
                                variantes = serial_variants(serial)
                                if contenu_set & variantes:
                                    if serial in non_trouves:
                                        non_trouves.remove(serial)
                                        key = (fichier, nom_feuille, os.path.abspath(chemin_fichier))
                                        mapping.setdefault(key, []).append(serial)
                    except:
                        continue

        groupes = []
        for (fichier, feuille, chemin_fichier), serials_trouvés in mapping.items():
            groupes.append({
                "fichier": fichier,
                "feuille": feuille,
                "chemin": chemin_fichier,
                "serials": sorted([s.upper() for s in serials_trouvés])
            })

        return jsonify({
            "groupes": groupes,
            "non_trouves": sorted([s.upper() for s in non_trouves]),
            "favoris": favoris
        })

    return render_template("projet5.html", favoris=favoris)
