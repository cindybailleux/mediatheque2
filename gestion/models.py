from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date


# créer un modèle pour le profil utilisateur
class ProfilUtilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_naissance = models.DateField(null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    scolarise_agglomeration = models.BooleanField(default=False)
    
    abonnement_valide = models.BooleanField(default=False)
    date_abonnement = models.DateField(default=timezone.now)  # Ajout date d'abonnement
    lettre_envoyee = models.BooleanField(default=False)  # Ajout lettre envoyée

    def age(self):
        today = timezone.now().date()
        if self.date_naissance:
            return today.year - self.date_naissance.year - (
                (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
            )
        return None

    def gratuit(self):
        age = self.age()
        if age is None:
            return False
        return (
        (self.ville and self.ville.lower() == 'montpellier') or
        age < 12 or
        (age < 18 and self.scolarise_agglomeration))

    
    def get_tarif(self):
        if self.gratuit():
            return "Gratuit"
        else:
            return "Tarif normal : 22 € par an ou Tarif Reduit sur présentation de justificatif: 10,50 € par mois. "

    
    def __str__(self):
        return f"Profil de {self.user.username} - Abonnement {'Valide' if self.abonnement_valide else 'Non valide'}"

# Les différents types de documents
class Document(models.Model):
    TYPE_CHOICES = [
        ('livre', 'Livre imprimé'),
        ('cd', 'CD / Audio'),
        ('dvd', 'DVD / Blu-Ray'),
        ('magazine', 'Magazine / Périodique'),
    ]

    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=200, blank=True, null=True)
    type_document = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date_sortie = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    nombre_pages = models.IntegerField(blank=True, null=True)  # pour livres
    duree_minutes = models.IntegerField(blank=True, null=True)  # pour CD, DVD
    disponible = models.BooleanField(default=True)


    def __str__(self):
        return self.titre

# Modèle pour gérer les emprunts de documents
class Emprunt(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    date_emprunt = models.DateField(default=timezone.now)
    date_retour_prevue = models.DateField()
    date_retour_reelle = models.DateField(blank=True, null=True)

    def get_date_retour_prevue():
        return timezone.now().date() + timedelta(days=4)

    def est_en_retard(self):
        return self.date_retour_reelle is None and self.date_retour_prevue < timezone.now().date()
    def __str__(self):
        return f"{self.utilisateur.username} a emprunté {self.document.titre}"


# Modèle pour créer une reservation
class Reservation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    date_reservation = models.DateField(default=date.today)
    date_venue = models.DateField()

    def __str__(self):
        return f"{self.utilisateur.username} réserve {self.document.titre} pour le {self.date_venue}"
