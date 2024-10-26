"""Ce module définit l'application Flask pour le portail GUDLFT Registration.

L'application permet aux clubs de se connecter, de voir les compétitions
à venir, et de réserver des places pour ces compétitions.
"""

import json
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for


def loadClubs():
    """Charger les clubs depuis un fichier JSON.

    Returns:
        list: Une liste de dictionnaires représentant les clubs.
    """
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    """Charger les compétitions depuis un fichier JSON.

    Returns:
        list: Une liste de dictionnaires représentant les compétitions.
    """
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    """Afficher la page d'accueil.

    Returns:
        str: Le rendu de la page HTML 'index.html'.
    """
    return render_template("index.html")


@app.route("/showSummary", methods=["GET", "POST"])
def showSummary():
    """Afficher le résumé pour un club donné après la connexion.

    Returns:
        str: Le rendu de la page HTML 'welcome.html' avec les informations du club et des compétitions.
    """
    if request.method == "POST":
        email = request.form.get("email")
    elif request.method == "GET":
        email = request.args.get("email")

    if not email:
        flash("Email non fourni, veuillez réessayer.", "error")
        return redirect(url_for("index"))

    matching_clubs = [club for club in clubs if club["email"] == email]
    if not matching_clubs:
        flash("Email invalide, veuillez réessayer.", "error")
        return redirect(url_for("index"))

    club = matching_clubs[0]

    upcoming_competitions = [
        comp
        for comp in competitions
        if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > datetime.now()
    ]

    return render_template(
        "welcome.html", club=club, competitions=upcoming_competitions
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """Permettre à un club de réserver des places pour une compétition donnée.

    Args:
        competition (str): Le nom de la compétition.
        club (str): Le nom du club.

    Returns:
        str: Le rendu de la page HTML 'booking.html' ou redirection vers une autre page en cas d'erreur.
    """
    foundClub = next((c for c in clubs if c["name"] == club), None)
    foundCompetition = next((c for c in competitions if c["name"] == competition), None)

    if foundClub and foundCompetition:
        if (
            datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S")
            > datetime.now()
        ):
            return render_template(
                "booking.html", club=foundClub, competition=foundCompetition
            )
        else:
            flash(
                "Erreur : Vous ne pouvez pas réserver une compétition dont la date est passée.",
                "error",
            )
            return redirect(url_for("showSummary", email=foundClub["email"]))
    else:
        flash("Erreur: Club ou Competition sélectionnée non trouvée", "error")
        return redirect(url_for("index"))


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    """Traiter la demande de réservation de places pour une compétition donnée.

    Returns:
        str: Le rendu de la page HTML 'welcome.html' avec les informations mises à jour ou redirection en cas d'erreur.
    """
    competition_name = request.form["competition"]
    club_name = request.form["club"]

    try:
        places_required = int(request.form["places"])
    except ValueError:
        flash("Erreur : Le nombre de places doit être un entier valide.", "error")
        return redirect(url_for("showSummary", email=club_name))

    if places_required <= 0:
        flash("Erreur : Le nombre de places doit être supérieur à zéro.", "error")
        return redirect(url_for("showSummary", email=club_name))

    competition = next(
        (comp for comp in competitions if comp["name"] == competition_name), None
    )
    club = next((c for c in clubs if c["name"] == club_name), None)

    if not competition or not club:
        flash("Erreur : Club ou compétition non trouvée.", "error")
        return redirect(url_for("showSummary", email=club_name))

    club_points = int(club["points"])
    competition_places = int(competition["numberOfPlaces"])

    if datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S") < datetime.now():
        flash(
            "Erreur : Vous ne pouvez pas réserver des places pour une compétition passée.",
            "error",
        )
        return redirect(url_for("showSummary", email=club_name))

    if places_required > club_points:
        flash(
            "Erreur : Vous n'avez pas assez de points pour réserver autant de places.",
            "error",
        )
    elif places_required > 12:
        flash(
            "Erreur : Vous ne pouvez pas réserver plus de 12 places par compétition.",
            "error",
        )
    elif competition_places < places_required:
        flash(
            "Erreur : Il n'y a pas assez de places disponibles pour cette compétition.",
            "error",
        )
    else:
        competition["numberOfPlaces"] = str(competition_places - places_required)
        club["points"] = str(club_points - places_required)
        flash("Réservation complète !", "success")

    upcoming_competitions = [
        comp
        for comp in competitions
        if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > datetime.now()
    ]

    return render_template(
        "welcome.html", club=club, competitions=upcoming_competitions
    )


def validate_places(places):
    """Valider le nombre de places.

    Args:
        places (int): Le nombre de places à valider.

    Raises:
        ValueError: Si le nombre de places est inférieur ou égal à zéro ou n'est pas un entier.
    """
    if not isinstance(places, int):
        raise ValueError("Le nombre de places doit être un entier.")
    if places <= 0:
        raise ValueError("Le nombre de places doit être supérieur à zéro.")


@app.route("/points")
def show_points():
    """Afficher les points de chaque club.

    Returns:
        str: Le rendu de la page HTML 'points.html'.
    """
    return render_template("points.html", clubs=clubs)


@app.route("/points-public")
def points_public():
    """Afficher les points des clubs publiquement.

    Returns:
        str: Le rendu de la page HTML 'points_public.html'.
    """
    return render_template("points_public.html", clubs=clubs)


@app.route("/logout")
def logout():
    """Déconnecter l'utilisateur et le rediriger vers la page d'accueil.

    Returns:
        werkzeug.wrappers.response.Response: Redirection vers la page d'accueil.
    """
    return redirect(url_for("index"))


def calcul_points(points_avant, places_reservees, points_par_place):
    """Calculer les points restants après une réservation.

    Args:
        points_avant (int): Le nombre de points avant la réservation.
        places_reservees (int): Le nombre de places réservées.
        points_par_place (int): Le coût en points par place réservée.

    Returns:
        int: Le nombre de points restants après la réservation.
    """
    return points_avant - (places_reservees * points_par_place)


def validate_competition_date(date):
    """Valide que la date de la compétition n'est pas dans le passé.

    Args:
        date (datetime): La date de la compétition.

    Raises:
        ValueError: Si la date est dans le passé.
    """
    if date < datetime.now():
        raise ValueError("La compétition est déjà passée.")
