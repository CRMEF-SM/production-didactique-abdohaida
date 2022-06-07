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
from json import dumps
#from rest_framework import serializers
from django.core import serializers

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

def ajouterCours(request):
	#if request.method == 'POST' and 'creer' in request.POST:
	#	titre = request.POST['titre']
	#	description = request.POST['description']
	#	contenue = request.request['contenue']
	#	cours = Cours.objects.create(titre=titre, description=description,videoFile=videoFile)
	#	video.save()
	#	return render(request, 'ajouterVideo.html', locals())
	#else:
	return render(request, 'editeur.html', locals())

def ajouterQuestion(request):
	quizzes = Quizze.objects.all()
	if request.method == 'POST' and 'ajouter' in request.POST:
		question = request.POST['question']
		choix1 = request.POST['choix1']
		choix2 = request.POST['choix2']
		choix3 = request.POST['choix3']
		choix4 = request.POST['choix4']
		reponse = request.POST['reponse']
		quizze_id = request.POST['quizze_id']
		Quest = Question.objects.create(question=question, choix1=choix1, choix2=choix2,choix3=choix3, choix4=choix4,reponse=reponse)
		Quest.save()
		quizze = Quizze.objects.get(id=quizze_id)
		quizze.questions.add(Quest)
		return render(request, "ajouterQuestion.html", locals())
	else:
		return render(request, "ajouterQuestion.html", locals())

def afficherQuizze(request, id):
	questions = Question.objects.all()
	#data = serializers.serialize('json', quest)
	data = []
	for quest in questions:
		val = {
		'question' : quest.question,
		'choix1' : quest.choix1,
		'choix2' : quest.choix2,
		'choix3' : quest.choix3,
		'choix4' : quest.choix4,
		'reponse' : quest.reponse}
		data.append(val)

	questions = dumps(data)
	nbr_questions = len(data)
	return render(request, 'afficherQuizze.html', locals())
