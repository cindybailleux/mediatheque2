"""
URL configuration for mediatheque2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),
    path('contact/', views.contact, name='contact'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('documents/', views.documents, name='documents'),
    path('reserver/<int:document_id>/', views.reserver_document, name='reserver_document'),
    path('mes_reservations/', views.mes_reservations, name='mes_reservations'),
    path('annuler_reservation/<int:reservation_id>/', views.annuler_reservation, name='annuler_reservation'),
    path('mon_compte/', views.mon_compte, name='mon_compte'),
]
