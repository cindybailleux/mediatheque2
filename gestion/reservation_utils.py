from datetime import timedelta

def est_date_disponible(document, date_venue):
    from .models import Reservation

    reservations = Reservation.objects.filter(document=document)

    for resa in reservations:
        debut = resa.date_venue
        fin = debut + timedelta(days=3)

        if debut <= date_venue <= fin:
            return False  # Conflit trouvé, date pas libre

    return True  # Pas de conflit, date OK
