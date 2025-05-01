from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from .models import Document, Emprunt, Reservation
from .reservation_utils import est_date_disponible
from .models import ProfilUtilisateur
from django.utils import timezone



# Fonction pour vérifier si l'abonnement est valide
def abonnement_valide(user):
    try:
        profil = ProfilUtilisateur.objects.get(user=user)
        return profil.abonnement_valide
    except ProfilUtilisateur.DoesNotExist:
        return False


def accueil(request):
    return render(request, 'accueil.html')
def contact(request):
    return render(request, 'contact.html')

# Inscription et création de compte
def inscription(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_naissance = request.POST['date_naissance']
        ville = request.POST['ville']
        etudiant = request.POST.get('etudiant') == 'on'
        email = request.POST['email']
        password = request.POST['password']

        # Créer l'utilisateur
        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()

        # Créer son profil automatiquement
        ProfilUtilisateur.objects.create(user=user, date_naissance=date_naissance, ville=ville, etudiant=etudiant)

        messages.success(request, "Votre compte a été créé ! Veuillez venir à la médiathèque pour activer votre abonnement.")
        return redirect('/connexion/')

    return render(request, 'inscription.html')

# Connexion de l'utilisateur    
def connexion(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  # Redirige vers la page d'accueil après connexion
        else:
            messages.error(request, "Identifiants invalides. Veuillez réessayer.")
            return redirect('/connexion/')

    return render(request, 'connexion.html')

# Déconnexion de l'utilisateur
def deconnexion(request):
    logout(request)
    return redirect('/') 

# Page des documents si l'utilisateur est connecté et a payé son abonnement
@login_required
def documents(request):
    if not abonnement_valide(request.user):
        messages.info(request, "Vous pouvez consulter les documents mais vous devez être abonné pour réserver.")


    documents = Document.objects.all()
    date_choisie_str = request.GET.get('date_choisie')
    
    date_choisie = date.today()
    if date_choisie_str:
        try:
            date_choisie = date.fromisoformat(date_choisie_str)
        except ValueError:
            pass

    type_doc = request.GET.get('type_document')
    auteur = request.GET.get('auteur')
    genre = request.GET.get('genre')
    date_min = request.GET.get('date_min')  # nouveau
    duree_max = request.GET.get('duree_max')  # nouveau

    if type_doc:
            documents = documents.filter(type_document=type_doc)
    if auteur:
            documents = documents.filter(auteur__icontains=auteur)
    if genre:
            documents = documents.filter(genre__icontains=genre)
    if date_min:
            documents = documents.filter(date_sortie__gte=date_min)  # >= la date choisie
    if duree_max:
            documents = documents.filter(duree_minutes__lte=duree_max)  # <= la durée max


    documents_info = []
    today = date.today()

    for doc in documents:
        reservations = Reservation.objects.filter(document=doc)
        dispo = True
        for resa in reservations:
            debut = resa.date_venue
            fin = debut + timedelta(days=3)
            if debut <= today <= fin:
                dispo = False
                break
        documents_info.append({
            'document': doc,
            'disponible': dispo,
        })

    return render(request, 'documents.html', {'documents_info': documents_info, 'abonnement_valide': abonnement_valide(request.user),})

# Page de réservation d'un document si l'utilisateur est connecté et a payé son abonnement
@login_required
def reserver_document(request, document_id):
    if not abonnement_valide(request.user):
        messages.error(request, "Votre abonnement n'est pas encore activé. Merci de venir à la médiathèque.")
        return redirect('accueil')
    
    document = Document.objects.get(id=document_id)

    if request.method == 'POST':
        date_venue_str = request.POST.get('date_venue')
        date_venue = datetime.strptime(date_venue_str, "%Y-%m-%d").date()

        reservations_en_cours = Reservation.objects.filter(utilisateur=request.user, date_venue__gte=date.today()).count()

        # Bloquer à 4 réservations maximum en même temps par abonné 
        if reservations_en_cours >= 4:
            messages.error(request, "Vous avez déjà atteint la limite de 4 emprunts. Merci de rendre un document avant de réserver un nouveau.")
            return render(request, 'reserver.html', {'document': document})
        
        # Vérifier si la date est valide
        if not est_date_disponible(document, date_venue):
            messages.error(request, "Ce document est déjà réservé sur cette période. Merci de choisir une autre date.")
            return render(request, 'reserver.html', {'document': document})

        # Créer la réservation
        Reservation.objects.create(
            utilisateur=request.user,
            document=document,
            date_venue=date_venue
        )
        messages.success(request, "Réservation confirmée !")
        return redirect('documents')

    return render(request, 'reserver.html', {'document': document})

# Page de gestion des réservations de l'utilisateur
@login_required
def mes_reservations(request):
    if not abonnement_valide(request.user):
        messages.error(request, "Votre abonnement n'est pas encore activé. Merci de venir à la médiathèque.")
        return redirect('accueil')
    
    reservations = Reservation.objects.filter(utilisateur=request.user).order_by('date_venue')
    return render(request, 'mes_reservations.html', {'reservations': reservations})

# Possibilité d'annuler une réservation
@login_required
def annuler_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id, utilisateur=request.user)
        reservation.delete()
        messages.success(request, "Réservation annulée avec succès.")
    except Reservation.DoesNotExist:
        messages.error(request, "Réservation introuvable.")

    return redirect('mes_reservations')

# Information sur le compte utilisateur
@login_required
def mon_compte(request):
    try:
        profil = ProfilUtilisateur.objects.get(user=request.user)
    except ProfilUtilisateur.DoesNotExist:
        messages.error(request, "Profil introuvable.")
        return redirect('accueil')

    # Calcul de la prochaine date de cotisation de l'abonement 
    date_renouvellement = profil.date_abonnement.replace(year=profil.date_abonnement.year + 1)
    aujourd_hui = timezone.now().date()

    emprunts = Emprunt.objects.filter(utilisateur=request.user).order_by('-date_emprunt')
    
    # Statut abonnement et lettre de rappel envoyé 
    abonnement_en_retard = aujourd_hui > date_renouvellement and not profil.lettre_envoyee

    return render(request, 'mon_compte.html', {
        'profil': profil,
        'date_renouvellement': date_renouvellement,
        'abonnement_en_retard': abonnement_en_retard,
        'emprunts': emprunts, 
    })