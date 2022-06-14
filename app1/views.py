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
	cours = Cours.objects.all()[:3]
	quizze = Quizze.objects.all()[:3]
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

def ajouterQuizze(request):
	if request.method == 'POST' and 'ajouter' in request.POST:
		titre = request.POST['titre']
		description = request.POST['description']
		image = request.FILES['image']
		quizze = Quizze.objects.create(titre=titre, description=description, image=image)
		quizze.save()
		return render(request, "ajouterQuizze.html", locals())
	else:
		return render(request, "ajouterQuizze.html", locals())


def afficherQuizze(request, id):
	quizze = Quizze.objects.get(id=id)
	questions = quizze.questions.all()
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

def afficherCours(request, id):
	cours = Cours.objects.get(id=id)
	chapitres = cours.chapitres.all()
	parties = {}
	for chap in chapitres:
		parties[chap.titreChapitre]=chap.parties.all()
	return render(request, 'afficherCours.html', locals())

def ajouterCours(request):
	if request.method == 'POST' and 'ajouter' in request.POST:
		titreCours = request.POST['titreCours']
		image = request.FILES['image']
		description = request.POST['description']
		cours = Cours.objects.create(titreCours=titreCours, image=image, description=description)
		cours.save()
		return render(request, "ajouterCours.html", locals())
	else:
		return render(request, "ajouterCours.html", locals())

def ajouterChapitre(request):
	if request.method == 'POST' and 'ajouter' in request.POST:
		titreChapitre = request.POST['titreChapitre']
		idCours = request.POST['idCours']
		chapitre = Chapitre.objects.create(titreChapitre=titreChapitre)
		chapitre.save()
		cours = Cours.objects.get(id=idCours)
		cours.chapitres.add(chapitre)
		return render(request, "ajouterChapitre.html", locals())
	else:
		return render(request, "ajouterChapitre.html", locals())

def ajouterPartie(request):
	if request.method == 'POST' and 'ajouter' in request.POST:
		titrePartie = request.POST['titrePartie']
		content = request.POST['content']
		idChapitre = request.POST['idChapitre']
		partie = Partie.objects.create(titrePartie=titrePartie, content=content)
		partie.save()
		chapitre = Chapitre.objects.get(id=idChapitre)
		chapitre.parties.add(partie)
		return render(request, "ajouterPartie.html", locals())
	else:
		return render(request, "ajouterPartie.html", locals())

def tousCours(request):
	cours = Cours.objects.all()
	return render(request, 'tousCours.html', locals())