"""Ce module définit les tests de performance pour l'application en utilisant
Locust.

Les utilisateurs simulent des connexions, chargent des compétitions, des
points, et réservent des places.
"""

import random

from locust import HttpUser, TaskSet, between, task

# Liste des clubs avec leurs emails
clubs = [
    {"name": "Simply Lift", "email": "john@simplylift.co"},
    {"name": "Iron Temple", "email": "admin@irontemple.com"},
    {"name": "She Lifts", "email": "kate@shelifts.co.uk"},
]

# Liste des compétitions
competitions = [
    {"name": "Spring Festival", "date": "2025-03-27 10:00:00"},
    {"name": "Fall Classic", "date": "2025-10-22 13:30:00"},
]


class UserBehavior(TaskSet):
    """Define user behavior for the performance test."""

    def on_start(self):
        """Simulate user login with a random email.

        This method runs at the start of each user to simulate login
        with a specific club.
        """
        self.club = random.choice(clubs)
        response = self.client.post("/showSummary", data={"email": self.club["email"]})
        if response.status_code == 200:
            print(f"Connexion réussie pour {self.club['name']}")
        else:
            print(f"Erreur de connexion pour {self.club['name']}")

    @task(1)
    def load_competitions(self):
        """Load the competition page to test response time."""
        self.client.get("/showSummary", params={"email": self.club["email"]})

    @task(1)
    def load_points(self):
        """Load the club points page to test response time."""
        self.client.get("/points")

    @task(1)
    def book_places(self):
        """Book a random number of places in a competition."""
        competition = random.choice(competitions)
        response = self.client.post(
            "/purchasePlaces",
            data={
                "competition": competition["name"],
                "club": self.club["name"],
                "places": str(random.randint(1, 5)),  # Réserver entre 1 et 5 places
            },
        )

        if response.status_code == 200:
            print(
                f"Réservation réussie pour {self.club['name']} dans la compétition {competition['name']}"
            )
        else:
            print(
                f"Erreur lors de la réservation pour {self.club['name']} dans la compétition {competition['name']}"
            )


class WebsiteUser(HttpUser):
    """Define a user interacting with the website."""

    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Temps d'attente entre les requêtes
    host = "http://127.0.0.1:5000"  # L'URL de votre application Flask en local
