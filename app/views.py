"""Toute les routes et les Formulaires"""
from .app import app, db
from .models import Activite, Artiste, GenreMusical, TypeBillet, Videos, get_infos_artistes, get_les_lieux, get_artistes_favoris, get_billets_achetes, get_informations_profil, seachartist_bd, get_les_photos_artiste, get_genre_musical_artiste, get_programmation_artiste
from .forms import LoginForm, ModificationForm

from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user

@app.route("/")
def accueil():
    return render_template("accueil.html", accueil=True, id_page=0, moncompte=False)

@app.route("/programmation/")
def programmation():
    return render_template("programmation.html",
                           accueil=False,
                           id_page=1,
                           moncompte=False,
                           les_artistes=get_infos_artistes(),
                           les_styles=GenreMusical.query.all(),
                           les_lieux=get_les_lieux())

@app.route("/reservation/")
@login_required
def reservation():
    return render_template("reservation.html", accueil=False, id_page=2, moncompte=False, les_billets=TypeBillet.query.all(), les_lieux=get_les_lieux())

@app.route("/connexion/", methods=["GET", "POST"])
def connexion():
    form = LoginForm()

    if form.validate_on_submit():
        user = form.get_authenticated_user()
        if user:
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("gestion_concerts") if user.is_admin() else url_for("espace_compte"))

    return render_template("connexion.html", accueil=False, id_page=0, moncompte=False, form=form)

@app.route('/deconnexion/')
def deconnexion():
    logout_user()
    return redirect(url_for('connexion'))

@app.route("/inscription/")
def inscription():
    return render_template("inscription.html", accueil=False, id_page=0, moncompte=False)

@app.route("/moncompte/")
@login_required
def espace_compte():
    return render_template("espace-compte.html", accueil=False, id_page=0, moncompte=True)

@app.route("/moncompte/mesinformations/", methods=["GET", "POST"])
@login_required
def edition_informations():
    form = ModificationForm()

    if form.validate_on_submit():
        current_user.nom_util = form.firstname.data
        current_user.prenom_util = form.lastname.data
        current_user.email_util = form.email.data

        if form.password.data:
            current_user.mdp_util = form.password.data

        db.session.commit()

        flash('Modifications enregistrées avec succès', 'success')
        return redirect(url_for('edition_informations'))

    form.firstname.data = current_user.nom_util
    form.lastname.data = current_user.prenom_util
    form.email.data = current_user.email_util
    return render_template("compte-infos.html", accueil=False, id_page=0, moncompte=False, mes_infos=get_informations_profil(current_user.IDutil), form=form)

@app.route("/moncompte/mesfavoris/")
@login_required
def mes_favoris():
    return render_template("favoris.html",
                           accueil=False,
                           id_page=0,
                           moncompte=False,
                           les_artistes=get_artistes_favoris(current_user.IDutil),
                           les_styles=GenreMusical.query.all(),
                           les_lieux=get_les_lieux())

@app.route("/moncompte/mesbillets/")
@login_required
def mes_billets():
    return render_template("billets-achetes.html", accueil=False, id_page=0, moncompte=False, les_billets=get_billets_achetes(current_user.IDutil), les_styles=GenreMusical.query.all(), les_lieux=get_les_lieux())

@app.route("/infosartiste/<int:idartiste>")
def infos_artiste(idartiste):
    return render_template("infos-artistes.html",
                           accueil=False,
                           id_page=0,
                           moncompte=False,
                           idartiste=0,
                           un_artiste=Artiste.query.get(idartiste),
                           photos=get_les_photos_artiste(idartiste),
                           style=get_genre_musical_artiste(idartiste),
                           programmer=get_programmation_artiste(idartiste),
                           activite=Activite.query.filter(idartiste == Activite.IDartiste).scalar(),
                           videos=Videos.query.filter(Videos.IDartiste == idartiste).scalar())

@app.route("/gestionconcerts/")
def gestion_concerts():
    return render_template("gestion-concerts.html", accueil=True, id_page=0, moncompte=True, nom_util=current_user.nom_util)

@app.route('/searchartist/', methods=['GET', 'POST'])
def searchartist():
    if request.method == 'POST':

        name = request.form.get('search')
        genre = request.form.get('Style')
        location = request.form.get('Lieu')
        date = request.form.get('datehour')

        results = seachartist_bd(name, genre, location, date)

    return render_template("programmation.html", accueil=False, id_page=1, moncompte=False, les_artistes=results, les_styles=GenreMusical.query.all(), les_lieux=get_les_lieux())

