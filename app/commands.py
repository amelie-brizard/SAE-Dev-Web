from datetime import date
import click
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
    db.session.commit()

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
    db.session.commit()

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
    db.session.commit()

    for dico_concert in data["CONCERT"]:
        concert = Concert(
            IDconcert=dico_concert["IDconcert"],
            nom_concert=dico_concert["nom_concert"],
            prix=dico_concert["prix"]
        )
        db.session.add(concert)
    db.session.commit()

    for dico_favori in data["ETRE_FAVORI"]:
        favori = EtreFavori(
            IDartiste=dico_favori["IDartiste"],
            IDutil=dico_favori["IDutil"]
        )
        db.session.add(favori)
    db.session.commit()

    for dico_hebergement in data["HEBERGEMENT"]:
        hebergement = Hebergement(
            IDhebergement=dico_hebergement["IDhebergement"],
            nom_hebergement=dico_hebergement["nom_hebergement"],
            nb_places=dico_hebergement["nb_places"]
        )
        db.session.add(hebergement)
    db.session.commit()

    for dico_loger in data["LOGER"]:
        loger = Loger(
            IDartiste=dico_loger["IDartiste"],
            IDhebergement=dico_loger["IDhebergement"],
            nb_Jours=dico_loger["nb_Jours"]
        )
        db.session.add(loger)
    db.session.commit()

    for dico_membres in data["MEMBRES"]:
        membres = Membres(
            IDmembre=dico_membres["IDmembre"],
            nom_membre=dico_membres["nom_membre"],
            description=dico_membres["description"],
            instrument=dico_membres["instrument"],
            IDartiste=dico_membres["IDartiste"]
        )
        db.session.add(membres)
    db.session.commit()

    for dico_photos in data["PHOTOS"]:
        photos = Photos(
            IDphoto=dico_photos["IDphoto"],
            nom_photo=dico_photos["nom_photo"],
            lien_photo=dico_photos["lien_photo"],
            IDartiste=dico_photos["IDartiste"]
        )
        db.session.add(photos)
    db.session.commit()

    for dico_programmer in data["PROGRAMMER"]:
        programmer = Programmer(
            IDconcert=dico_programmer["IDconcert"],
            date_debut=dico_programmer["date_debut"],
            heure_debut=dico_programmer["heure_debut"],
            IDartiste=dico_programmer["IDartiste"],
            lieu_concert=dico_programmer["lieu_concert"],
            duree_concert=dico_programmer["duree_concert"],
            tps_montage=dico_programmer["tps_montage"],
            tps_demontage=dico_programmer["tps_demontage"]
        )
        db.session.add(programmer)
    db.session.commit()

    for dico_reseaux in data["RESEAUX_SOCIAUX"]:
        reseaux = ReseauxSociaux(
            IDrs=dico_reseaux["IDrs"],
            nom_plateforme=dico_reseaux["nom_plateforme"],
            lien_rs=dico_reseaux["lien_rs"],
            IDartiste=dico_reseaux["IDartiste"]
        )
        db.session.add(reseaux)
    db.session.commit()

    for dico_reserver in data["RESERVER"]:
        reserver = Reserver(
            IDutil=dico_reserver["IDutil"],
            IDtype_billet=dico_reserver["IDtype_billet"],
            IDconcert=dico_reserver["IDconcert"]
        )
        db.session.add(reserver)
    db.session.commit()

    for dico_typebillet in data["TYPE_BILLET"]:
        type_billet = TypeBillet(
            IDtype_billet=dico_typebillet["IDtype_billet"],
            nom_type_billet=dico_typebillet["nom_type_billet"]
        )
        db.session.add(type_billet)
    db.session.commit()

    for dico_typeutil in data["TYPE_UTILISATEUR"]:
        type_util = TypeUtilisateur(
            IDtype_util=dico_typeutil["IDtype_util"],
            nom_type_util=dico_typeutil["nom_type_util"]
        )
        db.session.add(type_util)
    db.session.commit()

    for dico_util in data["UTILISATEUR"]:
        utilisateur = Utilisateur(
            IDutil=dico_util["IDutil"],
            nom_util=dico_util["nom_util"],
            prenom_util=dico_util["prenom_util"],
            mdp_util=dico_util["mdp_util"],
            email_util=dico_util["email_util"],
            date_de_naissance=dico_util["date_de_naissance"],
            IDtype_util=dico_util["IDtype_util"]
        )
        db.session.add(utilisateur)
    db.session.commit()

    for dico_videos in data["VIDEOS"]:
        videos = Videos(
            IDvideo=dico_videos["IDvideo"],
            nom_video=dico_videos["nom_video"],
            lien_video=dico_videos["lien_video"],
            IDartiste=dico_videos["IDartiste"]
        )
        db.session.add(videos)
    db.session.commit()
