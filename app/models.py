from base64 import b64encode
# from .app import db, login_manager
from .app import db
# from flask_login import UserMixin

from flask_sqlalchemy import CheckConstraint

class Activite(db.Model):
    __tablename__ = 'ACTIVITES'
    IDactivite = db.Column(db.Integer, primary_key=True)
    nom_activite = db.Column(db.String(42), nullable=False)
    description_activite = db.Column(db.Text)
    IDartiste = db.Column(db.Integer, nullable=False)
    heure = db.Column(db.Time)
    date = db.Column(db.Date)
    lieu_activite = db.Column(db.String(42))

class Artiste(db.Model):
    __tablename__ = 'ARTISTE'
    IDartiste = db.Column(db.Integer, primary_key=True)
    nom_artiste = db.Column(db.String(42), nullable=False)
    description = db.Column(db.Text)
    date_arrivee = db.Column(db.Date, CheckConstraint('date_arrivee < date_depart'))
    date_depart = db.Column(db.Date)
    IDgenre = db.Column(db.Integer, nullable=False)

class Concert(db.Model):
    __tablename__ = 'CONCERT'
    IDconcert = db.Column(db.Integer, primary_key=True)
    nom_concert = db.Column(db.String(42))
    prix = db.Column(db.Float)

class EtreFavori(db.Model):
    __tablename__ = 'ETRE_FAVORI'
    IDartiste = db.Column(db.Integer, db.ForeignKey("ARTISTE.IDartiste"))
    IDutil = db.Column(db.Integer, db.ForeignKey("UTILISATEUR.IDutil"))
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
    IDartiste = db.Column(db.Integer, db.ForeignKey("ARTISTE.IDartiste"))
    IDhebergement = db.Column(db.Integer, db.ForeignKey("HEBERGEMENT.IDhebergement"))
    nb_Jours = db.Column(db.Integer)
    artiste = db.relationship("Artiste", backref=db.backref("logements", lazy="dynamic"))
    hebergement = db.relationship("Hebergement", backref=db.backref("logements", lazy="dynamic"))

class Membres(db.Model):
    __tablename__ = "MEMBRES"
    IDmembre = db.Column(db.Integer, primary_key=True)
    nom_membre = db.Column(db.String(42))
    description = db.Column(db.Text)
    instrument = db.Column(db.String(42))
    IDartiste = db.Column(db.Integer)
    artiste = db.relationship("Artiste", backref=db.backref("membres", lazy="dynamic"))

class Photos(db.Model):
    __tablename__ = "PHOTOS"
    IDphoto = db.Column(db.Integer, primary_key=True)
    nom_photo = db.Column(db.String(42))
    lien_photo = db.Column(db.String(100), unique=True, nullable=False)
    IDartiste = db.Column(db.Integer)
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

class ReseauxSociaux(db.Model):
    __tablename__ = "RESEAUX_SOCIAUX"
    IDrs = db.Column(db.Integer, primary_key=True)
    nom_plateforme = db.Column(db.String(42))
    lien_rs = db.Column(db.String(100), unique=True, nullable=False)
    IDartiste = db.Column(db.Integer)
    artiste = db.relationship("Artiste", backref=db.backref("reseau", lazy="dynamic"))

class Reserver(db.Model):
    __tablename__ = "RESERVER"
    IDutil = db.Column(db.Integer, primary_key=True)
    IDtype_billet = db.Column(db.Integer, primary_key=True)
    IDconcert = db.Column(db.Integer, primary_key=True)

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
    IDtype_util = db.Column(db.Integer, nullable=False)
    typeutil = db.relationship("TypeUtilisateur", backref=db.backref("utilisateur", lazy="dynamic"))

class Videos(db.Model):
    __tablename__ = "VIDEOS"
    IDvideo = db.Column(db.Integer, primary_key=True)
    nom_video = db.Column(db.String(42))
    lien_video = db.Column(db.String(100), unique=True, nullable=False)
    IDartiste = db.Column(db.Integer)
    artiste = db.relationship("Artiste", backref=db.backref("videos", lazy="dynamic"))
