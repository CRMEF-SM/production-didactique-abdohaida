from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django .template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.mail import send_mail
from .models import *
import socket
import requests
import json

def home(request):
	video = Video.objects.all()[:3]
	return render(request,'index.html',locals())

def ajouterVideo(request):
	if request.method == 'POST' and 'envoyer' in request.POST:
		titre = request.POST['titre']
		description = request.POST['description']
		videoFile = request.FILES['video']
		video = Video.objects.create(titre=titre, description=description,videoFile=videoFile)
		video.save()
		return render(request, 'ajouterVideo.html', locals())
	else:
		return render(request, 'ajouterVideo.html', locals())

def afficherVideo(request, id):
	video = Video.objects.get(id=id)
	return render(request, 'afficherVideo.html', locals())

def tousVideo(request):
	video = Video.objects.all()
	return render(request, 'tousVideo.html', locals())