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

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)