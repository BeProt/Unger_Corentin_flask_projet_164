"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.entrepot.gestion_entrepot_wtf_forms import FormWTFAjouterEntrepot
from APP_FILMS_164.entrepot.gestion_entrepot_wtf_forms import FormWTFDeleteEntrepot
from APP_FILMS_164.entrepot.gestion_entrepot_wtf_forms import FormWTFUpdateEntrepot

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /entrepot_afficher
    
    Test : ex : http://127.0.0.1:5575/entrepot_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                IDEntrepot_sel = 0 >> tous les genres.
                IDEntrepot_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/entrepot_afficher/<string:order_by>/<int:IDEntrepot_sel>", methods=['GET', 'POST'])
def entrepot_afficher(order_by, IDEntrepot_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and IDEntrepot_sel == 0:
                    strsql_entrepot_afficher = """SELECT * FROM t_entrepot"""
                    mc_afficher.execute(strsql_entrepot_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_entrepot"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_IDEntrepot_selected_dictionnaire = {"value_IDEntrepot_selected": IDEntrepot_sel}
                    strsql_entrepot_afficher = """SELECT * FROM t_entrepot WHERE EntrepotAdresse = %(value_IDEntrepot_selected)s"""

                    mc_afficher.execute(strsql_entrepot_afficher, valeur_IDEntrepot_selected_dictionnaire)
                else:
                    strsql_entrepot_afficher = """SELECT * FROM t_entrepot"""

                    mc_afficher.execute(strsql_entrepot_afficher)

                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and IDEntrepot_sel == 0:
                    flash("""La table "t_entrepot" est vide. !!""", "warning")
                elif not data_genres and IDEntrepot_sel > 0:
                    # Si l'utilisateur change l'IDEntrepot dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_entrepot" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données Entrepôts affichés !!", "success")

        except Exception as Exception_entrepot_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{entrepot_afficher.__name__} ; "
                                          f"{Exception_entrepot_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("entrepot/entrepot_afficher.html", data=data_genres)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter
    
    Test : ex : http://127.0.0.1:5575/genres_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/entrepot_ajouter", methods=['GET', 'POST'])
def entrepot_ajouter_wtf():
    form = FormWTFAjouterEntrepot()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                IDLo_wtf = form.IDLo_wtf.data
                EntrepotNom_wtf = form.EntrepotNom_wtf.data
                EntrepotAdresse_wtf = form.EntrepotAdresse_wtf.data

                valeurs_insertion_dictionnaire = {
                    "value_IDLo": IDLo_wtf,
                    "value_EntrepotNom": EntrepotNom_wtf,
                    "value_EntrepotAdresse": EntrepotAdresse_wtf,
                    "value_localite_entrepot": request.form.get("value_localite_entrepot", "")  # Valeur par défaut ""
                }

                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_entrepot = """INSERT INTO t_entrepot (IDLo, EntrepotNom, EntrepotAdresse) VALUES (NULL, %(value_EntrepotNom)s, 
                (SELECT IDLo FROM t_localite WHERE IDLo = %(value_localite_entrepot)s))"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_entrepot, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('entrepot_afficher', order_by='DESC', IDEntrepot_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{entrepot_ajouter_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")


    return render_template("entrepot/entrepot_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /entrepot_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "entrepot_afficher.html"
    
    Remarque :  Dans le champ "EntrepotNom_wtf" du formulaire "genres/entrepot_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/entrepot_update", methods=['GET', 'POST'])
def entrepot_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "IDEntrepot"
    IDEntrepot_update = request.values['IDEntrepot_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateEntrepot()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "entrepot_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_Entrepot_update = form_update.EntrepotNom_wtf.data
            # name_Entrepot_update = name_Entrepot_update.lower()
            date_genre_essai = form_update.nom_Adresse_update_wtf.data

            valeur_update_dictionnaire = {"value_IDEntrepot": IDEntrepot_update,
                                          "value_EntrepotNom": name_Entrepot_update,
                                          "value_date_genre_essai": date_genre_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_entrepot SET EntrepotNom = %(value_EntrepotNom)s, 
            EntrepotAdresse = %(value_date_genre_essai)s WHERE IDEntrepot = %(value_IDEntrepot)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"IDEntrepot_update"
            return redirect(url_for('entrepot_afficher', order_by="ASC", IDEntrepot_sel=IDEntrepot_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "IDEntrepot" et "EntrepotNom" de la "t_entrepot"
            str_sql_IDEntrepot = "SELECT IDEntrepot, IDLo, EntrepotNom, EntrepotAdresse FROM t_entrepot " \
                               "WHERE IDEntrepot = %(value_IDEntrepot)s"
            valeur_select_dictionnaire = {"value_IDEntrepot": IDEntrepot_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_IDEntrepot, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_EntrepotNom = mybd_conn.fetchone()
            print("data_EntrepotNom ", data_EntrepotNom, " type ", type(data_EntrepotNom), " Nom ",
                  data_EntrepotNom["EntrepotNom"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "entrepot_update_wtf.html"
            form_update.EntrepotNom_wtf.data = data_EntrepotNom["EntrepotNom"]
            form_update.nom_Adresse_update_wtf.data = data_EntrepotNom["EntrepotAdresse"]


    except Exception as Exception_entrepot_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{entrepot_update_wtf.__name__} ; "
                                      f"{Exception_entrepot_update_wtf}")

    return render_template("entrepot/entrepot_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "entrepot_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/entrepot_delete", methods=['GET', 'POST'])
def entrepot_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "IDEntrepot"
    IDEntrepot_delete = request.values['IDEntrepot_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteEntrepot()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("entrepot_afficher", order_by="ASC", IDEntrepot_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = session['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_IDEntrepot": IDEntrepot_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_genre = """DELETE FROM t_produit_stocker_entrepot WHERE FKEntrepot = %(value_IDEntrepot)s"""
                str_sql_delete_idgenre = """DELETE FROM t_entrepot WHERE IDEntrepot = %(value_IDEntrepot)s"""
                # Manière brutale d'effacer d'abord la "FKEntrepot", même si elle n'existe pas dans la "t_produit_stocker_entrepot"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_produit_stocker_entrepot"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_genre, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('entrepot_afficher', order_by="ASC", IDEntrepot_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_IDEntrepot": IDEntrepot_delete}
            print(IDEntrepot_delete, type(IDEntrepot_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_genres_films_delete = """SELECT IDProEntrepot, ProNom, IDEntrepot, EntrepotNom FROM t_produit_stocker_entrepot 
                                            INNER JOIN t_produit ON t_produit_stocker_entrepot.FKPro = t_produit.IDPro
                                            INNER JOIN t_entrepot ON t_produit_stocker_entrepot.FKEntrepot = t_entrepot.IDEntrepot
                                            WHERE FKEntrepot = %(value_IDEntrepot)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau...
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "IDEntrepot" et "EntrepotNom" de la "t_entrepot"
                str_sql_IDEntrepot = "SELECT IDEntrepot, EntrepotNom FROM t_entrepot WHERE IDEntrepot = %(value_IDEntrepot)s"

                mydb_conn.execute(str_sql_IDEntrepot, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_EntrepotNom = mydb_conn.fetchone()
                print("data_EntrepotNom ", data_EntrepotNom, " type ", type(data_EntrepotNom), " genre ",
                      data_EntrepotNom["EntrepotNom"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_delete_wtf.html"
            form_delete.nom_genre_delete_wtf.data = data_EntrepotNom["EntrepotNom"]

            # Le bouton pour l'action "DELETE" dans le form. "genre_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_genre_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{entrepot_delete_wtf.__name__} ; "
                                      f"{Exception_genre_delete_wtf}")

    return render_template("entrepot/entrepot_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_entrepot_associes=data_films_attribue_genre_delete)
