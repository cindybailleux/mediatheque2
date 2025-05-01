from django.contrib import admin
from .models import Document, Emprunt, Reservation
from .models import ProfilUtilisateur
from django.utils import timezone
from .models import Emprunt
from django.utils.html import format_html


# créer tableau pour admins pour voir valider abonnement inscrit, lettre envoyée...
@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'abonnement_valide','ville', 'age', 'date_abonnement', 'lettre_envoyee', 'scolarise_agglomeration', 'gratuit', 'get_tarif')
    search_fields = ('user__email',)
    list_filter = ('abonnement_valide', 'lettre_envoyee', 'ville')

    def jours_restant(self, obj):
        today = timezone.now().date()
        fin_abonnement = obj.date_abonnement.replace(year=obj.date_abonnement.year + 1)
        delta = fin_abonnement - today
        return delta.days
    
    def age(self, obj):
        return obj.age()

    def gratuit(self, obj):
        return "Oui" if obj.gratuit() else "Non"

    gratuit.description = "Abonnement gratuit"

    def get_tarif(self, obj):
        return f"{obj.get_tarif()}"
    get_tarif.description = "Tarif abonnement"


# Modifier, créer, ajouter ,supprimer document 
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_sortie', 'type_document', 'genre', 'disponible')
    list_filter = ('type_document', 'disponible', 'date_sortie', 'genre')
    search_fields = ('titre', 'auteur', 'genre')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'document', 'date_venue')
    list_filter = ('date_venue',)
    search_fields = ('utilisateur__email', 'document__titre')


# Créer, modifier, supprimer emprunt et les rendus 
@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = (
        'utilisateur', 
        'document', 
        'date_emprunt', 
        'date_retour_prevue', 
        'date_retour_reelle', 
        'retard_status',
    )
    list_filter = ('date_emprunt', 'date_retour_reelle', 'date_retour_prevue')

    def retard_status(self, obj):
        from datetime import date
        if obj.date_retour_reelle:
            return format_html('<span style="color: green;"> Rendu</span>')
        elif obj.date_retour_prevue and obj.date_retour_prevue < date.today():
            return format_html('<span style="color: red;"> En retard</span>')
        else:
            return format_html('<span style="color: orange;">En cours</span>')

    retard_status.short_description = 'Statut'
