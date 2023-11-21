from datetime import date
import click
import os
from app.app import db, app

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''Creates the tables and populates them with data.'''

    # création de toutes les tables
    db.create_all()

    # Chargement de notre jeu de données
    import yaml
    data = yaml.safe_load(open(filename, 'r', encoding='utf-8'))

    # Import des modèles
    from .models import Role, Utilisateur, Domaine, Categorie, Materiel, Commande, Alerte

    # Création des différentes tables de notre base de données
    # {Categorie:[{code: 1, nom:"", code_domaine:1}, {...}]}

    liste_roles = data["Role"]
    liste_users = data["Utilisateur"]
    liste_domaines = data["Domaine"]
    liste_categories = data["Categorie"]
    liste_materiels = data["Materiel"]
    liste_commandes = data["Commande"]
    liste_alertes = data["Alerte"]

    for dico_role in liste_roles:
        role = Role(intitule=dico_role["intitule"])
        db.session.add(role)
    db.session.commit()

    for dico_domaines in liste_domaines:
        domaine = Domaine(nom=dico_domaines["nomD"])
        db.session.add(domaine)
    db.session.commit()

    for dico_categories in liste_categories:
        categorie = Categorie(code=dico_categories["codeC"],
                              nom=dico_categories["nomC"],
                              code_domaine=dico_categories["codeD"])
        db.session.add(categorie)
    db.session.commit()

    users = dict()
    for dico_users in liste_users:
        user_email = dico_users["emailUti"]
        if user_email not in users:
            o = Utilisateur(nom=dico_users["nomUti"],
                            prenom=dico_users["prenomUti"],
                            email=dico_users["emailUti"],
                            password=dico_users["password"],
                            modifications=dico_users["modifications"],
                            id_role=dico_users["idRole"])
            db.session.add(o)
            users[user_email] = o
    db.session.commit()

    materials = dict()
    for dico_materials in liste_materiels:
        material_ref = dico_materials["refMateriel"]
        if material_ref not in materials:
            date_peremption_str = dico_materials["datePeremption"]
            date_peremption = None
            if date_peremption_str is not None:
                d_peremption = date_peremption_str.split("-")
                date_peremption = date(int(d_peremption[0]),
                                       int(d_peremption[1]),
                                       int(d_peremption[2]))
            image = dico_materials["image"]
            if image:
                pathtest = os.path.join("static", "images", image)
                if os.path.isfile(pathtest):
                    with open(pathtest, "rb") as image_file:
                        image_data = image_file.read()
                else:
                    image_data = None
            else:
                image_data = None
            o = Materiel(reference=material_ref,
                         nom=dico_materials["nomMateriel"],
                         rangement=dico_materials["precisionMateriel"],
                         commentaire=dico_materials["commentaire"],
                         quantite_globale=dico_materials["qteMateriel"],
                         quantite_max=dico_materials["qteMax"],
                         unite=dico_materials["unite"],
                         quantite_restante=dico_materials["qteRestante"],
                         complements=dico_materials["complements"],
                         fiche_fds=dico_materials["ficheFDS"],
                         date_peremption=date_peremption,
                         seuil_quantite=dico_materials["seuilQte"],
                         seuil_peremption=dico_materials["seuilPeremption"],
                         image=image_data,
                         code_categorie=dico_materials["codeC"],
                         code_domaine=dico_materials["codeD"])
            db.session.add(o)
            materials[material_ref] = o
    db.session.commit()

    commandes = dict()
    for dico_commandes in liste_commandes:
        num_commande = dico_commandes["numeroCommande"]
        if num_commande not in commandes:
            date_commande_str = dico_commandes["dateCommande"]
            date_reception_str = dico_commandes["dateReception"]
            date_commande = None
            date_reception = None
            if date_peremption_str is not None:
                d_commande = date_commande_str.split("-")
                d_reception = date_reception_str.split("-")
                date_commande = date(int(d_commande[0]), int(d_commande[1]),
                                     int(d_commande[2]))
                date_reception = date(int(d_reception[0]), int(d_reception[1]),
                                      int(d_reception[2]))
            o = Commande(numero=dico_commandes["numeroCommande"],
                         date_commande=date_commande,
                         date_reception=date_reception,
                         statut=dico_commandes["statut"],
                         id_util=dico_commandes["idUti"],
                         quantite_commandee=dico_commandes["qteCommandee"],
                         ref_materiel=dico_commandes["refMateriel"])
            db.session.add(o)
            commandes[num_commande] = o
    db.session.commit()

    for dico_alertes in liste_alertes:
        o = Alerte(id=dico_alertes["idAlerte"],
                   commentaire=dico_alertes["commentaire"],
                   ref_materiel=dico_alertes["refMateriel"])
        db.session.add(o)
    db.session.commit()
