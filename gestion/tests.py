from django.test import TestCase
from django.contrib.auth.models import User
from gestion.models import Document

# Création d'un utilisateur test + connexion avec les identifiants et de la redirection vers la page d'accueil
class ConnexionTestCase(TestCase):
    def setUp(self):
        # Création d’un utilisateur test
        self.user = User.objects.create_user(username='test@test.com', email='test@test.com', password='pass1234')


    def test_connexion_utilisateur(self):
        response = self.client.post('/connexion/', {
        'email': 'test@test.com',
        'password': '1234'
    })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/') 

# Test de la création d'un document et vérification de la disponibilité
class DocumentModelTestCase(TestCase):
    def test_creation_document(self):
        doc = Document.objects.create(
            titre="Harry Potter à l'école des sorciers",
            auteur="Rowling",
            type_document="livre",
            genre="Policier",
            disponible=True
        )
        self.assertEqual(doc.titre, "Harry Potter à l'école des sorciers")
        self.assertTrue(doc.disponible)
