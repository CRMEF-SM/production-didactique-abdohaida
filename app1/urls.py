from django.urls import path ,include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns=[
url(r'^home$',views.home,name='home'),
url(r'^login$',views.Login,name='login'),
url(r'^register$',views.register,name='register'),
url(r'^logout$',views.Logout,name='logout'),
url(r'^contact$',views.contact,name='contact'),
url(r'^ajouterVideo$', views.ajouterVideo, name='ajouterVideo'),
url(r'^afficherVideo/(?P<id>\d+)$', views.afficherVideo, name='afficherVideo'),
url(r'^tousVideo$', views.tousVideo, name='tousVideo'),
url(r'^ajouterCours$', views.ajouterCours, name='ajouterCours'),
url(r'^afficherQuizze/(?P<id>\d+)$', views.afficherQuizze, name='afficherQuizze'),
url(r'^afficherCours/(?P<id>\d+)$', views.afficherCours, name='afficherCours'),
url(r'^editeCours/(?P<id>\d+)$', views.editeCours, name='editeCours'),
url(r'^editeChapitre/(?P<idCours>\d+)/(?P<idChapitre>\d+)$', views.editeChapitre, name='editeChapitre'),
url(r'^editePartie/(?P<idCours>\d+)/(?P<idChapitre>\d+)/(?P<idPartie>\d+)$', views.editePartie, name='editePartie'),
url(r'^editeVideo/(?P<idVideo>\d+)$', views.editeVideo, name='editeVideo'),
url(r'^editeQuizze/(?P<idQuizze>\d+)$', views.editeQuizze, name='editeQuizze'),
url(r'^editeQuestion/(?P<idQuizze>\d+)/(?P<idQuestion>\d+)$', views.editeQuestion, name='editeQuestion'),
url(r'^ajouterQuestion$', views.ajouterQuestion, name='ajouterQuestion'),
url(r'^ajouterQuizze$', views.ajouterQuizze, name='ajouterQuizze'),
url(r'^ajouterChapitre$', views.ajouterChapitre, name='ajouterChapitre'),
url(r'^ajouterPartie$', views.ajouterPartie, name='ajouterPartie'),
url(r'^tousCours$', views.tousCours, name='tousCours'),
url(r'^tousQuizze$', views.tousQuizze, name='tousQuizze'),
url(r'^tousMessage$', views.tousMessage, name='tousMessage'),
url(r'^adminPanel$', views.adminPanel, name='adminPanel'),
url(r'^deleteCours/(?P<id>\d+)$', views.deleteCours, name='deleteCours'),
url(r'^deleteMessage/(?P<id>\d+)$', views.deleteMessage, name='deleteMessage'),
url(r'^deleteQuestion/(?P<idQuizze>\d+)/(?P<idQuestion>\d+)$', views.deleteQuestion, name='deleteQuestion'),
url(r'^deleteVideo/(?P<idVideo>\d+)$', views.deleteVideo, name='deleteVideo'),
url(r'^deleteQuizze/(?P<idQuizze>\d+)$', views.deleteQuizze, name='deleteQuizze'),
url(r'^deletePartie/(?P<idCours>\d+)/(?P<idChapitre>\d+)/(?P<idPartie>\d+)$', views.deletePartie, name='deletePartie'),
url(r'^deleteChapitre/(?P<idCours>\d+)/(?P<idChapitre>\d+)$', views.deleteChapitre, name='deleteChapitre'),
url(r'^adminCours$', views.adminCours, name='adminCours'),
url(r'^adminQuizze$', views.adminQuizze, name='adminQuizze'),
url(r'^adminVideo$', views.adminVideo, name='adminVideo'),
url(r'^repondreMessage/(?P<idMessage>\d+)$', views.repondreMessage, name='repondreMessage'),



] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)