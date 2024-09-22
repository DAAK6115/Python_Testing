import json
from flask import Flask, render_template, request, redirect, flash, url_for

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

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((club for club in clubs if club['email'] == email), None)
    
    if club:
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash('Email non trouvé. Veuillez réessayer.')
        return redirect(url_for('index'))

@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash('Erreur lors de la sélection du club ou de la compétition.')
        return redirect(url_for('index'))

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    club_name = request.form['club']
    places_required = int(request.form['places'])

    competition = next((comp for comp in competitions if comp['name'] == competition_name), None)
    club = next((c for c in clubs if c['name'] == club_name), None)

    if competition and club:
        if places_required > 12:
            flash('Erreur: Tu ne peux pas reserver plus de 12 places par compétition.')
        elif competition['numberOfPlaces'] < places_required:
            flash('Erreur: Pas assez de places disponible pour cette compétition.')
        else:
            competition['numberOfPlaces'] -= places_required
            flash('Great-booking complete!')
    else:
        flash('Erreur: Le Club ou la competition n a pas été trouvé')
    
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
