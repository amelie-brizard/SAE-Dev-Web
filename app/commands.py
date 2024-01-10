from datetime import date
import click
import os
from app.app import db, app
from .models import Activite, Artiste, Concert, EtreFavori, GenreMusical, Hebergement, Loger, Membres, Photos, Programmer, ReseauxSociaux, Reserver, TypeBillet, TypeUtilisateur, Utilisateur, Videos
import yaml

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''Creates the tables and populates them with data.'''
    db.create_all()

    data = yaml.safe_load(open(filename, 'r', encoding='utf-8'))

    for dico_genre in data["GENRE_MUSICAL"]:
        genre = GenreMusical(
            IDgenre=dico_genre["IDgenre"],
            nom_genre=dico_genre["nom_genre"]
        )
        db.session.add(genre)

    for dico_artiste in data["ARTISTE"]:
        artiste = Artiste(
            IDartiste=dico_artiste["IDartiste"],
            nom_artiste=dico_artiste["nom_artiste"],
            description=dico_artiste["description"],
            date_arrivee=dico_artiste["date_arrivee"],
            date_depart=dico_artiste["date_depart"],
            IDgenre=dico_artiste["IDgenre"]
        )
        db.session.add(artiste)

    for dico_activite in data["ACTIVITES"]:
        activite = Activite(
            IDactivite=dico_activite["IDactivite"],
            nom_activite=dico_activite["nom_activite"],
            description_activite=dico_activite["description_activite"],
            IDartiste=dico_activite["IDartiste"],
            heure=dico_activite["heure"],
            date=dico_activite["date"],
            lieu_activite=dico_activite["lieu_activite"]
        )
        db.session.add(activite)

    for dico_concert in data["CONCERT"]:
        concert = Concert(
            IDconcert=dico_concert["IDconcert"],
            nom_concert=dico_concert["nom_concert"],
            prix=dico_concert["prix"]
        )
        db.session.add(concert)

    for dico_favori in data["ETRE_FAVORI"]:
        favori = EtreFavori(
            IDartiste=dico_favori["IDartiste"],
            IDutil=dico_favori["IDutil"]
        )
        db.session.add(favori)

    for dico_hebergement in data["HEBERGEMENT"]:
        hebergement = Hebergement(
            IDhebergement=dico_hebergement["IDhebergement"],
            nom_hebergement=dico_hebergement["nom_hebergement"],
            nb_places=dico_hebergement["nb_places"]
        )
        db.session.add(hebergement)

    for dico_loger in data["LOGER"]:
        loger = Loger(
            IDartiste=dico_loger["IDartiste"],
            IDhebergement=dico_loger["IDhebergement"],
            nb_Jours=dico_loger["nb_Jours"]
        )
        db.session.add(loger)

    for dico_membres in data["ARTISTE"]:
        membres = Membres(
            IDmembre=dico_membres["IDmembre"],
            nom_membre=dico_membres["nom_membre"],
            description=dico_membres["description"],
            instrument=dico_membres["instrument"],
            IDartiste=dico_membres["IDartiste"]
        )
        db.session.add(membres)

    # TODO
    # PHOTOS
    # PROGRAMMER
    # RESEAUX_SOCIAUX
    # RESERVER
    # TYPE_BILLET
    # TYPE_UTILISATEUR
    # UTILISATEUR
    # VIDEOS

    db.session.commit()
