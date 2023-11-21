"""Lien avec la Base de données"""

from base64 import b64encode
from .app import db, login_manager
from flask_login import UserMixin

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    intitule = db.Column(db.String(100))

    def __repr__(self):
        return "<Role (%d) %s>" % (self.id, self.intitule)


class Utilisateur(db.Model, UserMixin):
    __tablename__ = "utilisateur"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    modifications = db.Column(db.Boolean)
    password = db.Column(db.String(100))
    id_role = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role",
                           backref=db.backref("utilisateurs", lazy="dynamic"))

    def __repr__(self):
        return "<Utilisateur (%d) %s %r>" % (self.id, self.nom, self.prenom)

    def is_prof(self):
        """Vérifie si l'utilisateur passé en paramètres est un professeur

        Args:
            user (Utilisateur): un utilisateur

        Returns:
            boolean: True si l'utilisateur est un professeur, False sinon
        """
        role = Role.query.filter(Role.intitule == "Professeur").scalar()
        return role.id == self.id_role

    def is_admin(self):
        """Vérifie si l'utilisateur passé en paramètres est un admin

        Args:
            user (Utilisateur): un utilisateur

        Returns:
            boolean: True si l'utilisateur est un admin, False sinon
        """
        role = Role.query.filter(Role.intitule == "Administrateur").scalar()
        return role.id == self.id_role

    def is_etablissement(self):
        """Vérifie si l'utilisateur passé en paramètres est un établissement

        Args:
            user (Utilisateur): un utilisateur

        Returns:
            boolean: True si l'utilisateur est un établissement, False sinon
        """
        role = Role.query.filter(Role.intitule == "Etablissement").scalar()
        return role.id == self.id_role
    
    def get_id(self):
        return self.id

    def get_role(self):
        return Role.query.filter(Role.id == self.id_role).scalar()


class Domaine(db.Model):
    __tablename__ = "domaine"
    code = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))

    def __repr__(self):
        return "<Domaine (%d) %s>" % (self.code, self.nom)


class Categorie(db.Model):
    __tablename__ = "categorie"
    code = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    code_domaine = db.Column(db.Integer, db.ForeignKey("domaine.code"))
    domaine = db.relationship("Domaine",
                              backref=db.backref("categories", lazy="dynamic"))

    __table_args__ = (db.UniqueConstraint('code', 'code_domaine'),)

    def serialize(self):
        return {
            'codeC': self.code,
            'nom': self.nom,
            'codeD': self.code_domaine,
        }

    def __repr__(self):
        return "<Categorie (%d) %s %r>" % (self.code, self.nom, self.code_domaine)


class Materiel(db.Model):
    __tablename__ = "materiel"
    reference = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    rangement = db.Column(db.String(100))
    commentaire = db.Column(db.String(100))
    quantite_globale = db.Column(db.Integer)
    quantite_max = db.Column(db.Integer)
    unite = db.Column(db.String(100))
    quantite_restante = db.Column(db.Float)
    complements = db.Column(db.String(500))
    fiche_fds = db.Column(db.LargeBinary)
    date_peremption = db.Column(db.Date)
    seuil_quantite = db.Column(db.Integer)
    seuil_peremption = db.Column(db.Integer)
    image = db.Column(db.LargeBinary)
    code_categorie = db.Column(db.Integer, db.ForeignKey("categorie.code"))
    code_domaine = db.Column(db.Integer, db.ForeignKey("domaine.code"))
    categorie = db.relationship("Categorie",
                                backref=db.backref("matériels",
                                                   lazy="dynamic"))
    domaine = db.relationship("Domaine",
                              backref=db.backref("matériels", lazy="dynamic"))

    def get_image(self):
        if self.image is not None:
            return b64encode(self.image).decode("utf-8")
        else:
            default_image_path = "static/images/black_square.png"
            with open(default_image_path, 'rb') as f:
                default_image_data = f.read()
            return b64encode(default_image_data).decode("utf-8")

    def serialize(self):
        return {
            'reference': self.reference,
            'nom': self.nom,
            'quantite_globale': self.quantite_globale,
            'quantite_max': self.quantite_max,
            'unite': self.unite,
            'quantite_restante': self.quantite_restante,
            'complements': self.complements,
            'code_categorie': self.code_categorie,
            'code_domaine': self.code_domaine,
            'image': self.get_image(),
        }


    def __repr__(self):
        return "<Materiel (%d)>" % (self.reference)


class Commande(db.Model):
    __tablename__ = "commande"
    numero = db.Column(db.Integer, primary_key=True)
    date_commande = db.Column(db.Date)
    date_reception = db.Column(db.Date)
    statut = db.Column(db.String(100))
    quantite_commandee = db.Column(db.Integer)
    id_util = db.Column(db.Integer, db.ForeignKey("utilisateur.id"))
    ref_materiel = db.Column(db.Integer, db.ForeignKey("materiel.reference"))
    utilisateur = db.relationship("Utilisateur",
                                  backref=db.backref("commandes",
                                                     lazy="dynamic"))
    materiel = db.relationship("Materiel",
                               backref=db.backref("commandes", lazy="dynamic"))

    def __repr__(self):
        return "<Commande (%d) %s %r %e %c %d>" % (self.numero, self.date_commande, self.statut, self.date_reception, self.id_util, self.ref_materiel)


class Alerte(db.Model):
    __tablename__ = "alerte"
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.String(150))
    ref_materiel = db.Column(db.Integer,
                             db.ForeignKey("materiel.reference"),
                             primary_key=True)
    materiel = db.relationship("Materiel",
                               backref=db.backref("alertes", lazy="dynamic"))

    def __repr__(self):
        return "<Alerte (%d) %s %r>" % (self.id, self.commentaire, self.ref_materiel)

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

def filter_commands(txt, domaine, categorie, statut, commandes):
    liste_materiel = []
    for materiel in Materiel.query.all():
        if txt.upper() in materiel.nom.upper():
            liste_materiel.append(materiel)
    liste_commandes = []
    
    for commande in commandes:
        if commande.materiel in liste_materiel:
            if commande.materiel.domaine.nom == domaine or domaine == "Domaine":
                if commande.materiel.categorie.nom == categorie or categorie == "Categorie":
                    if commande.statut == statut or statut == "Statut":
                        liste_commandes.append(commande)

    return liste_commandes
