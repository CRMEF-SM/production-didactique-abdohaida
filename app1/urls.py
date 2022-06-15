from django.urls import path ,include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns=[
url(r'^home$',views.home,name='home'),
url(r'^ajouterVideo$', views.ajouterVideo, name='ajouterVideo'),
url(r'^afficherVideo/(?P<id>\d+)$', views.afficherVideo, name='afficherVideo'),
url(r'^tousVideo$', views.tousVideo, name='tousVideo'),
url(r'^ajouterCours$', views.ajouterCours, name='ajouterCours'),
url(r'^afficherQuizze/(?P<id>\d+)$', views.afficherQuizze, name='afficherQuizze'),
url(r'^afficherCours/(?P<id>\d+)$', views.afficherCours, name='afficherCours'),
url(r'^editeCours/(?P<id>\d+)$', views.editeCours, name='editeCours'),
url(r'^ajouterQuestion$', views.ajouterQuestion, name='ajouterQuestion'),
url(r'^ajouterQuizze$', views.ajouterQuizze, name='ajouterQuizze'),
url(r'^ajouterChapitre$', views.ajouterChapitre, name='ajouterChapitre'),
url(r'^ajouterPartie$', views.ajouterPartie, name='ajouterPartie'),
url(r'^tousCours$', views.tousCours, name='tousCours'),
url(r'^tousQuizze$', views.tousQuizze, name='tousQuizze'),
url(r'^adminPanel$', views.adminPanel, name='adminPanel'),
url(r'^deleteCours/(?P<id>\d+)$', views.deleteCours, name='deleteCours'),
url(r'^adminCours$', views.adminCours, name='adminCours'),
url(r'^adminQuizze$', views.adminQuizze, name='adminQuizze'),
url(r'^adminVideo$', views.adminVideo, name='adminVideo'),



] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)