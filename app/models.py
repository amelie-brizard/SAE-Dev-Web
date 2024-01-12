from base64 import b64encode
# from .app import db, login_manager
from .app import db
import datetime
from sqlalchemy import func
# from flask_login import UserMixin

# from flask_sqlalchemy import CheckConstraint

class Activite(db.Model):
    __tablename__ = 'ACTIVITES'
    IDactivite = db.Column(db.Integer, primary_key=True)
    nom_activite = db.Column(db.String(42), nullable=False)
    description_activite = db.Column(db.Text)
    IDartiste = db.Column(db.Integer, nullable=False)
    heure = db.Column(db.Time)
    date = db.Column(db.Date)
    lieu_activite = db.Column(db.String(42))

    def __init__(self, IDactivite, nom_activite, description_activite, IDartiste, heure, date, lieu_activite):
        self.IDactivite = IDactivite
        self.nom_activite = nom_activite
        self.description_activite = description_activite
        self.IDartiste = IDartiste
        self.heure = datetime.time.fromisoformat(heure)
        self.date = datetime.date.fromisoformat(date)
        self.lieu_activite = lieu_activite

class Artiste(db.Model):
    __tablename__ = 'ARTISTE'
    IDartiste = db.Column(db.Integer, primary_key=True)
    nom_artiste = db.Column(db.String(42), nullable=False)
    description = db.Column(db.Text)
    date_arrivee = db.Column(db.Date, db.CheckConstraint('date_arrivee < date_depart'))
    date_depart = db.Column(db.Date)
    IDgenre = db.Column(db.Integer, nullable=False)

    def __init__(self, IDartiste, nom_artiste, description, date_arrivee, date_depart, IDgenre):
        self.IDartiste = IDartiste
        self.nom_artiste = nom_artiste
        self.description = description
        self.date_arrivee = datetime.date.fromisoformat(date_arrivee)
        self.date_depart = datetime.date.fromisoformat(date_depart)
        self.IDgenre = IDgenre

class Concert(db.Model):
    __tablename__ = 'CONCERT'
    IDconcert = db.Column(db.Integer, primary_key=True)
    nom_concert = db.Column(db.String(42))
    prix = db.Column(db.Float)

class EtreFavori(db.Model):
    __tablename__ = 'ETRE_FAVORI'
    IDartiste = db.Column(db.Integer, db.ForeignKey("ARTISTE.IDartiste"), primary_key=True)
    IDutil = db.Column(db.Integer, db.ForeignKey("UTILISATEUR.IDutil"), primary_key=True)
    artiste = db.relationship("Artiste", backref=db.backref("favoris", lazy="dynamic"))
    utilisateur = db.relationship("Utilisateur", backref=db.backref("favoris", lazy="dynamic"))

class GenreMusical(db.Model):
    __tablename__ = 'GENRE_MUSICAL'
    IDgenre = db.Column(db.Integer, primary_key=True)
    nom_genre = db.Column(db.String(42))

class Hebergement(db.Model):
    __tablename__ = 'HEBERGEMENT'
    IDhebergement = db.Column(db.Integer, primary_key=True)
    nom_hebergement = db.Column(db.String(42), nullable=False)
    nb_places = db.Column(db.Integer)

class Loger(db.Model):
    __tablename__ = "LOGER"
    IDartiste = db.Column(db.Integer, db.ForeignKey("ARTISTE.IDartiste"), primary_key=True)
    IDhebergement = db.Column(db.Integer, db.ForeignKey("HEBERGEMENT.IDhebergement"), primary_key=True)
    nb_Jours = db.Column(db.Integer)
    artiste = db.relationship("Artiste", backref=db.backref("logements", lazy="dynamic"))
    hebergement = db.relationship("Hebergement", backref=db.backref("logements", lazy="dynamic"))

class Membres(db.Model):
    __tablename__ = "MEMBRES"
    IDmembre = db.Column(db.Integer, primary_key=True)
    nom_membre = db.Column(db.String(42))
    description = db.Column(db.Text)
    instrument = db.Column(db.String(42))
    IDartiste = db.Column(db.Integer, db.ForeignKey("ARTISTE.IDartiste"))
    artiste = db.relationship("Artiste", backref=db.backref("membres", lazy="dynamic"))

class Photos(db.Model):
    __tablename__ = "PHOTOS"
    IDphoto = db.Column(db.Integer, primary_key=True)
    nom_photo = db.Column(db.String(42))
    lien_photo = db.Column(db.String(100), unique=True, nullable=False)
    IDartiste = db.Column(db.Integer, db.ForeignKey("ARTISTE.IDartiste"))
    artiste = db.relationship("Artiste", backref=db.backref("photos", lazy="dynamic"))

class Programmer(db.Model):
    __tablename__ = "PROGRAMMER"
    IDconcert = db.Column(db.Integer, primary_key=True)
    date_debut = db.Column(db.Date, primary_key=True)
    heure_debut = db.Column(db.Time, primary_key=True)
    IDartiste = db.Column(db.Integer, db.ForeignKey("ARTISTE.IDartiste"))
    lieu_concert = db.Column(db.String(42))
    duree_concert = db.Column(db.Time, nullable=False)
    tps_montage = db.Column(db.Time, nullable=False)
    tps_demontage = db.Column(db.Time, nullable=False)
    artiste = db.relationship("Artiste", backref=db.backref("programme", lazy="dynamic"))

    def __init__(self, IDconcert, date_debut, heure_debut, IDartiste, lieu_concert, duree_concert, tps_montage, tps_demontage):
        self.IDconcert = IDconcert
        self.date_debut = datetime.date.fromisoformat(date_debut)
        self.heure_debut = datetime.time.fromisoformat(heure_debut)
        self.IDartiste = IDartiste
        self.lieu_concert = lieu_concert
        self.duree_concert = datetime.datetime.strptime(duree_concert, "%H:%M:%S").time()
        self.tps_montage = datetime.datetime.strptime(tps_montage, "%H:%M:%S").time()
        self.tps_demontage = datetime.datetime.strptime(tps_demontage, "%H:%M:%S").time()

class ReseauxSociaux(db.Model):
    __tablename__ = "RESEAUX_SOCIAUX"
    IDrs = db.Column(db.Integer, primary_key=True)
    nom_plateforme = db.Column(db.String(42))
    lien_rs = db.Column(db.String(100), unique=True, nullable=False)
    IDartiste = db.Column(db.Integer, db.ForeignKey("ARTISTE.IDartiste"))
    artiste = db.relationship("Artiste", backref=db.backref("reseau", lazy="dynamic"))

class Reserver(db.Model):
    __tablename__ = "RESERVER"
    IDutil = db.Column(db.Integer, primary_key=True)
    IDtype_billet = db.Column(db.Integer, primary_key=True)
    IDconcert = db.Column(db.Integer, db.ForeignKey("CONCERT.IDconcert"), primary_key=True)
    concert = db.relationship("Concert", backref=db.backref("reservation", lazy="dynamic"))

class TypeBillet(db.Model):
    __tablename__ = 'TYPE_BILLET'
    IDtype_billet = db.Column(db.Integer, primary_key=True)
    nom_type_billet = db.Column(db.String(42), unique=True)

class TypeUtilisateur(db.Model):
    __tablename__ = 'TYPE_UTILISATEUR'
    IDtype_util = db.Column(db.Integer, primary_key=True)
    nom_type_util = db.Column(db.String(42), unique=True)

class Utilisateur(db.Model):
    __tablename__ = 'UTILISATEUR'
    IDutil = db.Column(db.Integer, primary_key=True)
    nom_util = db.Column(db.String(42))
    prenom_util = db.Column(db.String(42))
    mdp_util = db.Column(db.String(42), nullable=False, unique=True)
    email_util = db.Column(db.String(60), nullable=False, unique=True)
    date_de_naissance = db.Column(db.Date)
    IDtype_util = db.Column(db.Integer, db.ForeignKey("TYPE_UTILISATEUR.IDtype_util"), nullable=False)
    typeutil = db.relationship("TypeUtilisateur", backref=db.backref("utilisateur", lazy="dynamic"))

    def __init__(self, IDutil, nom_util, prenom_util, mdp_util, email_util, date_de_naissance, IDtype_util):
        self.IDutil = IDutil
        self.nom_util = nom_util
        self.prenom_util = prenom_util
        self.mdp_util = mdp_util
        self.email_util = email_util
        self.date_de_naissance = datetime.date.fromisoformat(date_de_naissance)
        self.IDtype_util = IDtype_util

class Videos(db.Model):
    __tablename__ = "VIDEOS"
    IDvideo = db.Column(db.Integer, primary_key=True)
    nom_video = db.Column(db.String(42))
    lien_video = db.Column(db.String(100), unique=True, nullable=False)
    IDartiste = db.Column(db.Integer, db.ForeignKey("ARTISTE.IDartiste"))
    artiste = db.relationship("Artiste", backref=db.backref("videos", lazy="dynamic"))


def get_infos_artistes():
    res = []
    for un_artiste in Artiste.query.all():
        programmation = Programmer.query.filter(Programmer.IDartiste == un_artiste.IDartiste).scalar()
        if programmation is not None:
            date_debut = str(un_artiste.date_arrivee.day) + "/" + str(un_artiste.date_arrivee.month) + "/" + str(un_artiste.date_arrivee.year)
            date_fin = str(un_artiste.date_depart.day) + "/" + str(un_artiste.date_depart.month) + "/" + str(un_artiste.date_depart.year)
            res.append((un_artiste.nom_artiste,
                        GenreMusical.query.get(un_artiste.IDgenre).nom_genre,
                        date_debut, date_fin,
                        programmation.lieu_concert))
    return res

def get_les_lieux():
    res = set()
    for programmation in Programmer.query.all():
        res.add(programmation.lieu_concert)
    return res

def get_artistes_favoris(idutil):
    res = []
    les_favoris = EtreFavori.query.filter(EtreFavori.IDutil == idutil)
    for un_favori in les_favoris:
        un_artiste = Artiste.query.get(un_favori.IDartiste)
        programmation = Programmer.query.filter(Programmer.IDartiste == un_artiste.IDartiste).scalar()
        if programmation is not None:
            date_debut = str(un_artiste.date_arrivee.day) + "/" + str(un_artiste.date_arrivee.month) + "/" + str(un_artiste.date_arrivee.year)
            date_fin = str(un_artiste.date_depart.day) + "/" + str(un_artiste.date_depart.month) + "/" + str(un_artiste.date_depart.year)
            res.append((un_artiste.nom_artiste,
                        GenreMusical.query.get(un_artiste.IDgenre).nom_genre,
                        date_debut, date_fin,
                        programmation.lieu_concert))
    return res

def get_date_fin_concert(idconcert):
    subquery = (
        db.session.query(
            Artiste.IDartiste,
            func.max(Artiste.date_depart).label("max_date_depart")
        )
        .join(Programmer, Artiste.IDartiste == Programmer.IDartiste)
        .filter(Programmer.IDconcert == idconcert)
        .group_by(Artiste.IDartiste)
        .subquery()
    )

    return (
        db.session.query(subquery.c.max_date_depart)
        .filter(Artiste.IDartiste == subquery.c.IDartiste)
        .scalar()
    )

def get_billets_achetes(idutil):
    res = []
    les_reservation = Reserver.query.filter(Reserver.IDutil == idutil)
    for une_reservation in les_reservation:
        concert = Concert.query.get(une_reservation.IDconcert)
        date_debut_concert = Programmer.query.filter(Programmer.IDconcert == concert.IDconcert).scalar().date_debut
        date_fin_concert = get_date_fin_concert(concert.IDconcert)
        nb_jours = int((date_fin_concert - date_debut_concert).days)
        date_debut = str(date_debut_concert.day) + "/" + str(date_debut_concert.month) + "/" + str(date_debut_concert.year)
        if une_reservation.IDtype_billet == 1:
            date_fin = date_debut
            prix = concert.prix // nb_jours
        elif une_reservation.IDtype_billet == 2:
            print(type(date_debut_concert))
            date_fin = date_debut
            prix = (concert.prix // nb_jours) * 2
        else:
            date_fin = date_fin_concert
            prix = concert.prix
        res.append((TypeBillet.query.get(une_reservation.IDtype_billet).nom_type_billet,
                    prix,
                    date_debut,
                    date_fin,
                    Programmer.query.filter(Programmer.IDconcert == concert.IDconcert).scalar().lieu_concert))
    return res
