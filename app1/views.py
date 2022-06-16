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
	if request.method == 'POST' and 'ajouterVideo' in request.POST:
		titre = request.POST['titre']
		description = request.POST['description']
		videoFile = request.FILES['video']
		video = Video.objects.create(titre=titre, description=description,videoFile=videoFile)
		video.save()
		return redirect('adminVideo')
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
		return redirect('editeQuizze', quizze_id)
	else:
		idQuizze = request.POST['idQuizze']
		return render(request, "ajouterQuestion.html", locals())

def ajouterQuizze(request):
	if request.method == 'POST' and 'ajouter' in request.POST:
		titre = request.POST['titre']
		description = request.POST['description']
		image = request.FILES['image']
		quizze = Quizze.objects.create(titre=titre, description=description, image=image)
		quizze.save()
		return redirect('adminQuizze')
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

def editeCours(request, id):
	cours = Cours.objects.get(id=id)
	chapitres = cours.chapitres.all()
	parties = {}
	for chap in chapitres:
		parties[chap.titreChapitre]=len(chap.parties.all())
	if request.method == 'POST' and 'editeCours' in request.POST:
		cours.titreCours = request.POST['titreCours']
		cours.description = request.POST['description']
		if 'image' in request.FILES:
			image = request.FILES['image']
		cours.save()
		return redirect('editeCours', id)
	else:
		return render(request, 'editeCours.html', locals())

def editeChapitre(request, idCours, idChapitre):
	cours = Cours.objects.get(id=idCours)
	chapitre = Chapitre.objects.get(id=idChapitre)
	parties = chapitre.parties.all()
	if request.method == 'POST' and 'editeChapitre' in request.POST:
		chapitre.titreChapitre = request.POST['titreChapitre']
		chapitre.save()
		return redirect('editeChapitre', idCours=idCours, idChapitre=idChapitre)
	else:
		return render(request, 'editeChapitre.html', locals())

def editePartie(request, idCours, idChapitre, idPartie):
	cours = Cours.objects.get(id=idCours)
	chapitre = Chapitre.objects.get(id=idChapitre)
	partie = Partie.objects.get(id=idPartie)
	if request.method == 'POST' and 'editePartie' in request.POST:
		partie.titrePartie = request.POST['titrePartie']
		partie.content = request.POST['content']
		partie.save()
		return redirect('editeChapitre', idCours=idCours, idChapitre=idChapitre)
	else:
		return render(request, 'editePartie.html', locals())

def editeQuizze(request, idQuizze):
	quizze = Quizze.objects.get(id=idQuizze)
	questions = quizze.questions.all()
	if request.method == 'POST' and 'editeQuizze' in request.POST:
		quizze.titre = request.POST['titre']
		quizze.description = request.POST['description']
		if 'image' in request.FILES:
			quizze.image = request.FILES['image']
		quizze.save()
		return redirect('editeQuizze', idQuizze)
	else:
		return render(request, 'editeQuizze.html', locals())

def editeQuestion(request, idQuizze, idQuestion):
	quizze = Quizze.objects.get(id=idQuizze)
	question = Question.objects.get(id=idQuestion)
	if request.method == 'POST' and 'editeQuestion' in request.POST:
		question.question = request.POST['question']
		question.choix1 = request.POST['choix1']
		question.choix2 = request.POST['choix2']
		question.choix3 = request.POST['choix3']
		question.choix4 = request.POST['choix4']
		question.reponse = request.POST['reponse']
		question.save()
		return redirect('editeQuizze', idQuizze)
	else:
		return render(request, 'editeQuestion.html', locals())

def editeVideo(request, idVideo):
	video =Video.objects.get(id=idVideo)
	if request.method == 'POST' and 'editeVideo' in request.POST:
		video.titre = request.POST['titre']
		video.description = request.POST['description']
		if 'video' in request.FILES:
			video.videoFile = request.FILES['video']
		video.save()
		return redirect('adminVideo')
	else:
		return render(request, 'editeVideo.html', locals())

def deleteVideo(request, idVideo):
	video =Video.objects.get(id=idVideo)
	video.delete()
	return redirect('adminVideo')

def deleteQuestion(request, idQuizze, idQuestion):
	question = Question.objects.get(id=idQuestion)
	question.delete()
	return redirect('editeQuizze', idQuizze)

def deleteQuizze(request, idQuizze):
	quizze = Quizze.objects.get(id=idQuizze)
	questions = quizze.questions.all()
	for quest in questions:
		quest.delete()
	quizze.delete()
	return redirect('adminQuizze')

def deletePartie(request, idCours, idChapitre, idPartie):
	partie = Partie.objects.get(id=idPartie)
	partie.delete()
	return redirect('editeChapitre', idCours=idCours, idChapitre=idChapitre)

def deleteChapitre(request, idCours, idChapitre):
	chapitre = Chapitre.objects.get(id=idChapitre)
	parties = chapitre.parties.all()
	for part in parties:
		part.delete()
	chapitre.delete()
	return redirect('editeCours', idCours)

def ajouterCours(request):
	if request.method == 'POST' and 'ajouter' in request.POST:
		titreCours = request.POST['titreCours']
		image = request.FILES['image']
		description = request.POST['description']
		cours = Cours.objects.create(titreCours=titreCours, image=image, description=description)
		cours.save()
		cours = Cours.objects.all()
		return render(request, "adminCours.html", locals())
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
		return redirect('editeCours',idCours)
	else:
		idCours = request.POST['idCours']
		return render(request, "ajouterChapitre.html", locals())

def ajouterPartie(request):
	if request.method == 'POST' and 'ajouter' in request.POST:
		titrePartie = request.POST['titrePartie']
		content = request.POST['content']
		idChapitre = request.POST['idChapitre']
		idCours = request.POST['idCours']
		partie = Partie.objects.create(titrePartie=titrePartie, content=content)
		partie.save()
		chapitre = Chapitre.objects.get(id=idChapitre)
		chapitre.parties.add(partie)
		return redirect('editeChapitre', idCours=idCours, idChapitre=idChapitre)
	else:
		idCours = request.POST['idCours']
		idChapitre = request.POST['idChapitre']
		return render(request, "ajouterPartie.html", locals())

def tousCours(request):
	cours = Cours.objects.all()
	return render(request, 'tousCours.html', locals())

def deleteCours(request, id):
	cours = Cours.objects.get(id=id)
	for chap in cours.chapitres.all():
		for part in chap.parties.all():
			part.delete()
		chap.delete()
	cours.delete()
	cours = Cours.objects.all()
	return redirect('adminCours')

def adminPanel(request):
	cours = Cours.objects.all()
	video = Video.objects.all()
	quizze = Quizze.objects.all()
	nbrCours = len(cours)
	nbrVideo = len(video)
	nbrQuizze = len(quizze)
	return render(request, 'admin.html', locals())

def tousQuizze(request):
	quizze = Quizze.objects.all()
	return render(request, 'tousQuizze.html', locals())

def adminCours(request):
	cours = Cours.objects.all()
	return render(request, 'adminCours.html', locals())

def adminVideo(request):
	video = Video.objects.all()
	return render(request, 'adminVideo.html', locals())

def adminQuizze(request):
	quizze = Quizze.objects.all()
	return render(request, 'adminQuizze.html', locals())