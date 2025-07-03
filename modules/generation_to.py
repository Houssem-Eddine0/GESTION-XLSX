import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from flask import render_template, jsonify

FAV_FILE = "favoris_to.json"

def charger_favoris():
    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def enregistrer_favoris(liste):
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(liste, f, indent=2)

def handler(request):
    favoris = charger_favoris()
    return render_template("projet6.html", favoris=favoris)

def update_favoris(request):
    action = request.form.get("action")
    chemin = request.form.get("chemin", "").strip()
    favoris = charger_favoris()

    if action == "ajouter" and chemin and chemin not in favoris:
        favoris.append(chemin)
    elif action == "supprimer" and chemin in favoris:
        favoris.remove(chemin)

    enregistrer_favoris(favoris)
    return jsonify({"success": True, "favoris": favoris})

def generate_retour(request):
    to = request.form.get("to", "").strip()
    raw = request.form.get("feuilles_json")
    try:
        feuilles = json.loads(raw)
    except:
        return jsonify({"message": "❌ Format invalide."})

    if not feuilles:
        return jsonify({"message": "❌ Aucune donnée reçue."})

    feuilles_nettoyees = {
        k.upper(): [s.strip().upper() for s in v.splitlines() if s.strip()]
        for k, v in feuilles.items()
    }

    df_dict = {k: pd.DataFrame({"SERIAL": v}) for k, v in feuilles_nettoyees.items() if v}

    if not df_dict:
        return jsonify({"message": "❌ Aucun serial valide à enregistrer."})

    base = Path.home() / "Documents"
    nom = f"TO_{to}.xlsx" if to else f"Retour_iPAD_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    chemin = base / nom

    try:
        with pd.ExcelWriter(chemin, engine="openpyxl") as writer:
            for nom_feuille, df in df_dict.items():
                df.to_excel(writer, index=False, sheet_name=nom_feuille)
    except Exception as e:
        return jsonify({"message": f"Erreur création fichier : {e}"})

    return jsonify({"message": f"✅ Fichier généré : {chemin}"})
