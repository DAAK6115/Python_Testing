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
    return render_template('index.html')

@app.route('/showSummary', methods=['GET', 'POST'])
def showSummary():
    if request.method == 'POST':
        matching_clubs = [club for club in clubs if club['email'] == request.form['email']]
        
        if not matching_clubs:
            flash("Email invalide, veuillez réessayer.")
            return render_template('index.html')

        club = matching_clubs[0]

        # Filtrer les compétitions futures uniquement
        upcoming_competitions = [
            comp for comp in competitions
            if datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S') > datetime.now()
        ]

        return render_template('welcome.html', club=club, competitions=upcoming_competitions)

@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)

    if foundClub and foundCompetition:
        # Vérifier si la compétition est encore à venir
        if datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S') > datetime.now():
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
        else:
            flash("Erreur : Vous ne pouvez pas réserver une compétition dont la date est passée.")
            return redirect(url_for('showSummary'))
    else:
        flash('Erreur: Club invalide ou Competition sélectionnée')
        return redirect(url_for('index'))

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    club_name = request.form['club']
    
    try:
        places_required = int(request.form['places'])  # Tentative de conversion en entier
    except ValueError:
        flash('Erreur : Le nombre de places doit être un entier valide.')
        return redirect(url_for('showSummary'))

    # Vérifier que le nombre de places est positif
    if places_required <= 0:
        flash('Erreur : Le nombre de places doit être supérieur à zéro.')
        return redirect(url_for('showSummary'))

    # Chargement des compétitions et clubs
    competition = next((comp for comp in competitions if comp['name'] == competition_name), None)
    club = next((c for c in clubs if c['name'] == club_name), None)

    if competition and club:
        # Vérifier si la compétition est encore à venir
        if datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
            flash('Erreur : Vous ne pouvez pas réserver des places pour une compétition passée.')
            return redirect(url_for('showSummary'))
        
        # Conversion des points et des places disponibles en entiers
        club_points = int(club['points'])
        competition_places = int(competition['numberOfPlaces'])

        # Vérifications des points et des places disponibles
        if places_required > club_points:
            flash('Erreur : Vous n\'avez pas assez de points pour réserver autant de places.')
        elif places_required > 12:
            flash('Erreur : Vous ne pouvez pas réserver plus de 12 places par compétition.')
        elif competition_places < places_required:
            flash('Erreur : Il n\'y a pas assez de places disponibles pour cette compétition.')
        else:
            # Mise à jour des places disponibles et des points du club
            competition['numberOfPlaces'] = str(competition_places - places_required)
            club['points'] = str(club_points - places_required)
            flash('Réservation complète !')
    else:
        flash('Erreur : Club ou compétition non trouvé.')

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/points')
def show_points():
    return render_template('points.html', clubs=clubs)

@app.route('/points-public')
def points_public():
    return render_template('points_public.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
