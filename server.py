import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    # Filtrer les compétitions futures uniquement pour la page d'accueil
    upcoming_competitions = [
        comp for comp in competitions
        if datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S') > datetime.now()
    ]
    return render_template('index.html', competitions=upcoming_competitions)

@app.route('/showSummary', methods=['GET', 'POST'])
def showSummary():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
        elif request.method == 'GET':
            email = request.args.get('email')

        if not email:
            flash("Email non fourni, veuillez réessayer.")
            return redirect(url_for('index'))

        matching_clubs = [club for club in clubs if club['email'] == email]

        if not matching_clubs:
            flash("Email invalide, veuillez réessayer.")
            return redirect(url_for('index'))

        club = matching_clubs[0]

        # Filtrer les compétitions futures uniquement
        if not competitions:
            flash("Aucune compétition disponible pour le moment.")
            return redirect(url_for('index'))

        upcoming_competitions = [
            comp for comp in competitions
            if datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S') > datetime.now()
        ]

        return render_template('welcome.html', club=club, competitions=upcoming_competitions)

    except Exception as e:
        print(f"Erreur dans /showSummary : {e}")
        flash("Erreur interne sur le serveur. Veuillez réessayer plus tard.")
        return redirect(url_for('index'))

@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        foundClub = next((c for c in clubs if c['name'] == club), None)
        foundCompetition = next((c for c in competitions if c['name'] == competition), None)

        if foundClub and foundCompetition:
            # Vérifier si la compétition est encore à venir
            if datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S') > datetime.now():
                return render_template('booking.html', club=foundClub, competition=foundCompetition)
            else:
                flash("Erreur : Vous ne pouvez pas réserver une compétition dont la date est passée.")
                return redirect(url_for('showSummary', email=foundClub['email']))
        else:
            flash('Erreur : Club ou compétition non trouvé.')
            return redirect(url_for('index'))
    except Exception as e:
        print(f"Erreur dans /book : {e}")
        flash("Erreur interne sur le serveur. Veuillez réessayer plus tard.")
        return redirect(url_for('index'))

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    try:
        competition_name = request.form.get('competition')
        club_name = request.form.get('club')
        places_required = request.form.get('places')

        if not competition_name or not club_name or not places_required:
            flash("Les informations de réservation sont incomplètes.")
            return redirect(url_for('showSummary'))

        try:
            places_required = int(places_required)  # Tentative de conversion en entier
        except ValueError:
            flash('Erreur : Le nombre de places doit être un entier valide.')
            return redirect(url_for('showSummary'))

        if places_required <= 0:
            flash('Erreur : Le nombre de places doit être supérieur à zéro.')
            return redirect(url_for('showSummary'))

        competition = next((comp for comp in competitions if comp['name'] == competition_name), None)
        club = next((c for c in clubs if c['name'] == club_name), None)

        if not competition or not club:
            flash('Erreur : Club ou compétition non trouvé.')
            return redirect(url_for('showSummary'))

        if datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
            flash('Erreur : Vous ne pouvez pas réserver des places pour une compétition passée.')
            return redirect(url_for('showSummary'))

        club_points = int(club['points'])
        competition_places = int(competition['numberOfPlaces'])

        if places_required > club_points:
            flash('Erreur : Vous n\'avez pas assez de points pour réserver autant de places.')
        elif places_required > 12:
            flash('Erreur : Vous ne pouvez pas réserver plus de 12 places par compétition.')
        elif competition_places < places_required:
            flash('Erreur : Il n\'y a pas assez de places disponibles pour cette compétition.')
        else:
            competition['numberOfPlaces'] = str(competition_places - places_required)
            club['points'] = str(club_points - places_required)
            flash('Réservation complète !')

        upcoming_competitions = [
            comp for comp in competitions
            if datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S') > datetime.now()
        ]

        return render_template('welcome.html', club=club, competitions=upcoming_competitions)

    except Exception as e:
        print(f"Erreur dans /purchasePlaces : {e}")
        flash("Erreur interne sur le serveur. Veuillez réessayer plus tard.")
        return redirect(url_for('index'))

@app.route('/points')
def show_points():
    return render_template('points.html', clubs=clubs)

@app.route('/points-public')
def points_public():
    return render_template('points_public.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

# server.py
def validate_places(places):
    """Fonction de validation du nombre de places"""
    if not isinstance(places, int):
        raise ValueError("Le nombre de places doit être un entier.")
    if places <= 0:
        raise ValueError("Le nombre de places doit être supérieur à zéro.")

