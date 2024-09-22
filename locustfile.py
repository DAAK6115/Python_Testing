from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):

    @task(1)
    def load_competitions(self):
        # Tester le temps de chargement de la page des compétitions
        self.client.get("/showSummary", params={"email": "john@simplylift.co"})

    @task(1)
    def load_points(self):
        # Tester le temps de chargement de la page des points des clubs
        self.client.get("/points")

    @task(1)
    def book_places(self):
        # Tester la réservation et la mise à jour des points
        self.client.post("/purchasePlaces", {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "5"
        })

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Temps d'attente entre les requêtes

    # Spécifiez l'hôte ici
    host = "http://127.0.0.1:5000"  # L'URL de votre application Flask en local
