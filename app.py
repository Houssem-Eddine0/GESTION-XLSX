from flask import Flask, render_template, request, jsonify
import threading
import webbrowser
import platform
import os

# 📦 Modules
from modules import recherche_ipad, gestion_ciblee, modif_masse, recherche_masse, generation_to

app = Flask(__name__)

# === ROUTES PRINCIPALES ===

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/projet2", methods=["GET", "POST"])
def projet2():
    return recherche_ipad.handler(request)

@app.route("/favoris_projet2", methods=["POST"])
def fav_recherche():
    return recherche_ipad.ajouter_favori(request)

@app.route("/projet3", methods=["GET", "POST"])
def projet3():
    return gestion_ciblee.handler(request)

@app.route("/fichiers_projet3", methods=["POST"])
def fichiers_proj3():
    return gestion_ciblee.get_fichiers(request)

@app.route("/feuilles_projet3", methods=["POST"])
def feuilles_proj3():
    return gestion_ciblee.get_feuilles(request)

@app.route("/appliquer_projet3", methods=["POST"])
def appliquer_proj3():
    return gestion_ciblee.appliquer_action(request)

@app.route("/favoris_projet3", methods=["POST"])
def favoris_proj3():
    return gestion_ciblee.update_favoris(request)

@app.route("/projet4", methods=["GET"])
def projet4():
    return modif_masse.handler(request)

@app.route("/feuilles_projet4", methods=["POST"])
def feuilles_projet4():
    return modif_masse.get_feuilles(request)

@app.route("/ajout_serials", methods=["POST"])
def ajout_serials_route():
    return modif_masse.ajouter_serials(request)

@app.route("/favoris_projet4", methods=["POST"])
def favoris_projet4():
    return modif_masse.update_favoris(request)

@app.route("/projet5", methods=["GET", "POST"])
def projet5():
    return recherche_masse.handler(request)

@app.route("/favoris_projet5", methods=["POST"])
def favoris_masse():
    return recherche_masse.update_favoris(request)

@app.route("/projet6", methods=["GET"])
def projet6():
    return generation_to.handler(request)

@app.route("/gen_retour", methods=["POST"])
def gen_retour():
    return generation_to.generate_retour(request)

@app.route("/favoris_projet6", methods=["POST"])
def favoris_projet6():
    return generation_to.update_favoris(request)

@app.route("/projet7", methods=["GET"])
def projet7():
    return render_template("projet7.html")


# === AUTO-OUVERTURE DU NAVIGATEUR ===

def ouvrir_navigateur():
    url = "http://127.0.0.1:5000"
    try:
        if platform.system() == "Windows":
            os.startfile(url)
        else:
            webbrowser.open(url)
    except:
        webbrowser.open(url)

if __name__ == "__main__":
    threading.Timer(1.0, ouvrir_navigateur).start()
    app.run(debug=False)
