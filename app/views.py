"""Toute les routes et les Formulaires"""
from .app import app
from .models import Activite, Artiste, Concert, EtreFavori, GenreMusical, Hebergement, Loger, Membres, Photos, Programmer, ReseauxSociaux, Reserver, TypeBillet, TypeUtilisateur, Utilisateur, Videos, get_infos_artistes, get_les_lieux, get_artistes_favoris, get_billets_achetes, get_informations_profil

from flask import render_template
# from flask import jsonify, render_template, url_for, redirect, request, flash
from flask_login import login_required
# from flask_login import login_required, login_user, logout_user, current_user
# from flask_wtf import FlaskForm
# from wtforms import StringField, HiddenField, PasswordField, SelectField, RadioField, IntegerField
# from wtforms.validators import DataRequired, NumberRange
from hashlib import sha256
# from datetime import datetime

@app.route("/")
def accueil():
    return render_template("accueil.html", accueil=True, id_page=0, moncompte=False)

@app.route("/programmation/")
def programmation():
    return render_template("programmation.html", accueil=False, id_page=1, moncompte=False, les_artistes=get_infos_artistes(), les_styles=GenreMusical.query.all(), les_lieux=get_les_lieux())

@app.route("/reservation/")
# @login_required
def reservation():
    return render_template("reservation.html", accueil=False, id_page=2, moncompte=False)

@app.route("/connexion/")
def connexion():
    return render_template("connexion.html", accueil=False, id_page=0, moncompte=False)

@app.route("/inscription/")
def inscription():
    return render_template("inscription.html", accueil=False, id_page=0, moncompte=False)

@app.route("/moncompte/")
# @login_required
def espace_compte():
    return render_template("espace-compte.html", accueil=False, id_page=0, moncompte=True)

@app.route("/moncompte/mesinformations/")
# @login_required
def edition_informations():
    return render_template("compte-infos.html", accueil=False, id_page=0, moncompte=False, mes_infos=get_informations_profil(1))

@app.route("/moncompte/mesfavoris/")
# @login_required
def mes_favoris():
    return render_template("favoris.html", accueil=False, id_page=0, moncompte=False, les_artistes=get_artistes_favoris(1), les_styles=GenreMusical.query.all(), les_lieux=get_les_lieux())

@app.route("/moncompte/mesbillets/")
# @login_required
def mes_billets():
    return render_template("billets-achetes.html", accueil=False, id_page=0, moncompte=False, les_billets=get_billets_achetes(1), les_styles=GenreMusical.query.all(), les_lieux=get_les_lieux())

@app.route("/infosartiste/")
def infos_artiste():
    return render_template("infos-artistes.html", accueil=False, id_page=0, moncompte=False)

@app.route("/gestionconcerts/")
def gestion_concerts():
    return render_template("gestion-concerts.html", accueil=True, id_page=0, moncompte=True)

