import os
import json
import pandas as pd
from flask import render_template, jsonify, request

COLONNES_SERIAL = ["SERIAL", "SERIAL NUMBER", "SN", "S/N"]
COLONNES_ASSET = ["ASSET", "ASSET TAG", "TAG", "ASSETTAG"]
FAV_FILE = "favoris_gestion.json"

def charger_favoris():
    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def update_favoris(req):
    chemin = req.form.get("chemin", "").strip()
    action = req.form.get("action", "")
    favoris = charger_favoris()
    if action == "ajouter" and chemin not in favoris:
        favoris.append(chemin)
    elif action == "supprimer" and chemin in favoris:
        favoris.remove(chemin)
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favoris, f, indent=2)
    return jsonify({"success": True, "favoris": favoris})

def handler(req):
    favoris = charger_favoris()
    return render_template("projet3.html", favoris=favoris)

def get_fichiers(req):
    chemin = req.form.get("chemin", "").strip()
    if not os.path.isdir(chemin):
        return jsonify({"success": False, "message": "❌ Dossier invalide."})
    fichiers = [f for f in os.listdir(chemin) if f.lower().endswith(".xlsx")]
    return jsonify({"success": True, "fichiers": fichiers})

def get_feuilles(req):
    chemin = req.form.get("chemin", "").strip()
    fichier = req.form.get("fichier", "").strip()
    fichier_path = os.path.join(chemin, fichier)
    if not os.path.isfile(fichier_path):
        return jsonify({"success": False, "message": "❌ Fichier introuvable."})
    try:
        xls = pd.ExcelFile(fichier_path)
        return jsonify({"success": True, "feuilles": xls.sheet_names})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erreur : {e}"})
def appliquer_action(req):
    dossier = req.form.get("chemin", "").strip()
    fichier = req.form.get("fichier", "").strip()
    feuille = req.form.get("feuille", "").strip()
    operation = req.form.get("operation")
    serial = req.form.get("serial", "").strip()
    asset = req.form.get("asset", "").strip()
    champ = req.form.get("champ", "").strip().upper()
    valeur = req.form.get("valeur", "").strip()

    chemin_fichier = os.path.join(dossier, fichier)
    if not os.path.isfile(chemin_fichier):
        return jsonify({"message": "❌ Fichier introuvable."})
    if not feuille:
        return jsonify({"message": "❌ Aucune feuille sélectionnée."})

    try:
        df = pd.read_excel(chemin_fichier, sheet_name=feuille)
    except Exception as e:
        return jsonify({"message": f"Erreur lecture : {e}"})

    df = df.loc[:, ~df.columns.duplicated()]
    df.columns = [str(c).strip().upper() for c in df.columns]

    col_serial = next((col for col in df.columns if col in [c.upper() for c in COLONNES_SERIAL]), None)
    col_asset = next((col for col in df.columns if col in [c.upper() for c in COLONNES_ASSET]), None)

    if not serial and not asset:
        return jsonify({"message": "❌ Aucun identifiant fourni."})

    df_valid = df.copy()
    if col_serial:
        df_valid[col_serial] = df_valid[col_serial].astype(str).str.strip()
    if col_asset:
        df_valid[col_asset] = df_valid[col_asset].astype(str).str.strip()

    trouve = pd.DataFrame()
    if serial and col_serial:
        trouve = df_valid[df_valid[col_serial].str.lower() == serial.lower()]
    if asset and col_asset and trouve.empty:
        trouve = df_valid[df_valid[col_asset].str.lower() == asset.lower()]

    if operation == "ajouter":
        if not trouve.empty:
            ligne = int(trouve.index[0]) + 2
            return jsonify({"message": f"⚠️ Déjà présent (ligne Excel {ligne})."})
        ligne_data = {}
        if col_serial and serial:
            ligne_data[col_serial] = serial.upper()
        if col_asset and asset:
            ligne_data[col_asset] = asset.upper()
        nouvelle = pd.DataFrame([ligne_data]).reindex(columns=df.columns, fill_value="")
        df = pd.concat([df, nouvelle], ignore_index=True)

    elif operation == "supprimer":
        if trouve.empty:
            return jsonify({"message": "ℹ️ Aucun identifiant trouvé."})
        df = df.drop(trouve.index).reset_index(drop=True)

    elif operation == "modifier":
        if trouve.empty:
            return jsonify({"message": "ℹ️ Aucun identifiant trouvé pour modification."})
        if champ not in df.columns:
            return jsonify({"message": f"❌ Colonne inconnue : {champ}"})
        df.loc[trouve.index, champ] = valeur

    try:
        with pd.ExcelWriter(chemin_fichier, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, index=False, sheet_name=feuille)
    except Exception as e:
        return jsonify({"message": f"Erreur enregistrement : {e}"})

    action_msg = {
        "ajouter": "✅ Ligne ajoutée.",
        "supprimer": "🗑️ Ligne supprimée.",
        "modifier": f"✏️ Colonne {champ} modifiée → {valeur}"
    }

    return jsonify({"message": action_msg.get(operation, "✅ Opération réussie.")})
