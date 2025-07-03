import os
import json
import pandas as pd
from flask import render_template, request, jsonify
from pathlib import Path

FAV_FILE = "favoris_ajout.json"
COLONNES_SERIAL = ["SERIAL", "S/N", "SERIAL NUMBER", "SN"]

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
    return render_template("projet4.html", favoris=favoris)

def update_favoris(request):
    chemin = request.form.get("chemin", "").strip()
    action = request.form.get("action")
    favoris = charger_favoris()
    if action == "ajouter" and chemin and chemin not in favoris:
        favoris.append(chemin)
    elif action == "supprimer" and chemin in favoris:
        favoris.remove(chemin)
    enregistrer_favoris(favoris)
    return jsonify({"success": True, "favoris": favoris})

def get_feuilles(request):
    chemin = request.form.get("chemin", "").strip()
    if not os.path.isfile(chemin) or not chemin.endswith(".xlsx"):
        return jsonify({"success": False, "message": "❌ Fichier Excel invalide."})
    try:
        xls = pd.ExcelFile(chemin)
        return jsonify({"success": True, "feuilles": xls.sheet_names})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erreur : {e}"})

def ajouter_serials(request):
    chemin = request.form.get("chemin", "").strip()
    feuille = request.form.get("feuille", "").strip()
    serials_raw = request.form.get("serials", "").strip()

    serials = [s.strip().upper() for s in serials_raw.splitlines() if s.strip()]
    if not chemin or not os.path.isfile(chemin):
        return jsonify({"message": "❌ Fichier introuvable."})
    if not feuille or not serials:
        return jsonify({"message": "❌ Feuille ou serials manquants."})

    try:
        df = pd.read_excel(chemin, sheet_name=feuille)
        df.columns = [str(c).strip().upper() for c in df.columns]
        col_serial = next((c for c in df.columns if c in [x.upper() for x in COLONNES_SERIAL]), None)
        if not col_serial:
            return jsonify({"message": "❌ Colonne SERIAL non trouvée."})
        existants = df[col_serial].astype(str).str.strip().str.upper().tolist()
        nouveaux = [s for s in serials if s not in existants]
        if not nouveaux:
            return jsonify({"message": "⚠️ Tous les SERIALs sont déjà présents."})

        ajouts = pd.DataFrame({col_serial: nouveaux})
        final = pd.concat([df, ajouts], ignore_index=True)

        with pd.ExcelWriter(chemin, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            final.to_excel(writer, index=False, sheet_name=feuille)

        return jsonify({"message": f"✅ {len(nouveaux)} serial(s) ajouté(s)."})
    except Exception as e:
        return jsonify({"message": f"❌ Erreur : {e}"})
