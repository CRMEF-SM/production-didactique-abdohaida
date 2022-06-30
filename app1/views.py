from django.shortcuts import render ,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django .template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.clickjacking import xframe_options_exempt
from mailer import Mailer
from .models import *
import socket
import requests
import json
from json import dumps
#from rest_framework import serializers
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def home(request):
	video = Video.objects.all()[:3]
	cours = Cours.objects.all()[:3]
	quizze = Quizze.objects.all()[:3]
	nbrCours = len(Cours.objects.all())
	nbrVideo = len(Video.objects.all())
	nbrQuizze = len(Quizze.objects.all())
	nbrMessage = len(Message.objects.all())
	return render(request,'index.html',locals())

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@xframe_options_exempt
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

@xframe_options_exempt
def afficherCours(request, id):
	cours = Cours.objects.get(id=id)
	chapitres = cours.chapitres.all()
	parties = {}
	for chap in chapitres:
		parties[chap.titreChapitre]=chap.parties.all()
	videos = {}
	for chap in chapitres:
		videos[chap.titreChapitre]=chap.videos.all()
	files = {}
	for chap in chapitres:
		files[chap.titreChapitre]=chap.files.all()
	quizzes = {}
	for chap in chapitres:
		quizzes[chap.titreChapitre]=chap.quizzes.all()
	return render(request, 'afficherCours.html', locals())

@login_required(login_url='login')
def editeCours(request, id):
	cours = Cours.objects.get(id=id)
	chapitres = cours.chapitres.all()
	parties = {}
	files = {}
	videos = {}
	quizzes = {}
	for chap in chapitres:
		parties[chap.titreChapitre]=len(chap.parties.all())
		files[chap.titreChapitre]=len(chap.files.all())
		videos[chap.titreChapitre]=len(chap.videos.all())
		quizzes[chap.titreChapitre]=len(chap.quizzes.all())
	if request.method == 'POST' and 'editeCours' in request.POST:
		cours.titreCours = request.POST['titreCours']
		cours.description = request.POST['description']
		if 'image' in request.FILES:
			cours.image = request.FILES['image']
		cours.save()
		return redirect('editeCours', id)
	else:
		return render(request, 'editeCours.html', locals())

@login_required(login_url='login')
def editeChapitre(request, idCours, idChapitre):
	cours = Cours.objects.get(id=idCours)
	chapitre = Chapitre.objects.get(id=idChapitre)
	parties = chapitre.parties.all()
	files = chapitre.files.all()
	videos = chapitre.videos.all()
	quizzes = chapitre.quizzes.all()
	if request.method == 'POST' and 'editeChapitre' in request.POST:
		chapitre.titreChapitre = request.POST['titreChapitre']
		chapitre.save()
		return redirect('editeChapitre', idCours=idCours, idChapitre=idChapitre)
	else:
		return render(request, 'editeChapitre.html', locals())

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def editeVideo(request, idVideo):
	video =Video.objects.get(id=idVideo)
	if request.method == 'POST' and 'editeVideo' in request.POST:
		video.titre = request.POST['titre']
		video.description = request.POST['description']
		if 'video' in request.FILES:
			video.videoFile = request.FILES['video']
		video.save()
		#page = request.META.get('HTTP_REFERER')
		return redirect('adminVideo')
	else:
		return render(request, 'editeVideo.html', locals())

@login_required(login_url='login')
def deleteVideo(request, idVideo):
	video =Video.objects.get(id=idVideo)
	video.delete()
	return redirect('adminVideo')

@login_required(login_url='login')
def deleteQuestion(request, idQuizze, idQuestion):
	question = Question.objects.get(id=idQuestion)
	question.delete()
	return redirect('editeQuizze', idQuizze)

@login_required(login_url='login')
def deleteQuizze(request, idQuizze):
	quizze = Quizze.objects.get(id=idQuizze)
	questions = quizze.questions.all()
	for quest in questions:
		quest.delete()
	quizze.delete()
	return redirect('adminQuizze')

@login_required(login_url='login')
def deletePartie(request, idCours, idChapitre, idPartie):
	partie = Partie.objects.get(id=idPartie)
	partie.delete()
	return redirect('editeChapitre', idCours=idCours, idChapitre=idChapitre)

@login_required(login_url='login')
def deleteChapitre(request, idCours, idChapitre):
	chapitre = Chapitre.objects.get(id=idChapitre)
	parties = chapitre.parties.all()
	videos = chapitre.videos.all()
	files = chapitre.files.all()
	quizzes = chapitre.quizzes.all()
	for part in parties:
		part.delete()
	for vid in videos:
		vid.delete()
	for file in files:
		file.delete()
	for quiz in quizzes:
		quiz.delete()
	chapitre.delete()
	return redirect('editeCours', idCours)

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def deleteCours(request, id):
	cours = Cours.objects.get(id=id)
	for chap in cours.chapitres.all():
		for part in chap.parties.all():
			part.delete()
		chap.delete()
	cours.delete()
	cours = Cours.objects.all()
	return redirect('adminCours')

@login_required(login_url='login')
def adminPanel(request):
	cours = Cours.objects.all()
	video = Video.objects.all()
	quizze = Quizze.objects.all()
	nbrMessage = Message.objects.all().count()
	nbrCours = len(cours)
	nbrVideo = len(video)
	nbrQuizze = len(quizze)
	return render(request, 'admin.html', locals())

def tousQuizze(request):
	quizze = Quizze.objects.all()
	return render(request, 'tousQuizze.html', locals())

@login_required(login_url='login')
def adminCours(request):
	cours = Cours.objects.all()
	return render(request, 'adminCours.html', locals())

@login_required(login_url='login')
def adminVideo(request):
	video = Video.objects.all()
	return render(request, 'adminVideo.html', locals())

@login_required(login_url='login')
def adminQuizze(request):
	quizze = Quizze.objects.all()
	return render(request, 'adminQuizze.html', locals())

def Login(request):
	if request.method == 'POST' and 'login' in request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			login(request, user)
			return redirect('adminPanel')
		else:
			messages.add_message(request, messages.INFO, 'username ou password erronée')
			return render(request, 'login.html',locals())
	else:
		return render(request, 'login.html',locals())

def Logout(request):
	logout(request)
	return render(request, 'login.html',locals())

def register(request):
	username = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	user = User.objects.create_user(username, email, password)
	user.save()
	return redirect('login')

def contact(request):
	name = request.POST['name']
	email = request.POST['email']
	body = request.POST['message']
	page = request.POST.get('page', '/')
	message = Message.objects.create(name=name, email=email, message=body)
	message.save()
	return HttpResponseRedirect(page)

@login_required(login_url='login')
def tousMessage(request):
	messages = Message.objects.all()
	return render(request, 'tousMessage.html', locals())

@login_required(login_url='login')
def deleteMessage(request, id):
	message = Message.objects.get(id=id)
	message.delete()
	return redirect('tousMessage')

@login_required(login_url='login')
def repondreMessage(request, idMessage):
	message = Message.objects.get(id=idMessage)
	if request.method == 'POST' and 'repondre' in request.POST:
		subject = request.POST['subject']
		msg = request.POST['msg']
		source = 'production.diadactique@gmail.com'
		destination = request.POST['to']
		#socket.getaddrinfo('smtp.gmail.com',587)
		mail=Mailer(email=source,password='ijtmsmnbovezumhy')
		mail.send(receiver=destination,subject=subject,message=msg)
		if mail.status:
			messages.add_message(request, messages.INFO, 'message envoyer')
		else:
			messages.add_message(request, messages.INFO, 'erreur')
		return render(request,'repondreMessage.html',locals())
	else:
		return render(request,'repondreMessage.html',locals())

@login_required(login_url='login')
def ajouterVideoToChapitre(request):
	if request.method == 'POST' and 'ajouterVideo' in request.POST:
		titre = request.POST['titre']
		description = request.POST['description']
		videoFile = request.FILES['video']
		idChapitre = request.POST['idChapitre']
		idCours = request.POST['idCours']
		video = Video.objects.create(titre=titre, description=description,videoFile=videoFile)
		video.save()
		chapitre = Chapitre.objects.get(id=idChapitre)
		chapitre.videos.add(video)
		return redirect('editeChapitre', idCours, idChapitre)
	else:
		idCours = request.POST['idCours']
		idChapitre = request.POST['idChapitre']
		return render(request, "ajouterVideoToChapitre.html", locals())


@login_required(login_url='login')
def ajouterFichier(request):
	if request.method == 'POST' and 'ajouter' in request.POST:
		titre = request.POST['titre']
		lien = request.FILES['url']
		idChapitre = request.POST['idChapitre']
		idCours = request.POST['idCours']
		fichier = File.objects.create(titre=titre, lien=lien)
		fichier.save()
		chapitre = Chapitre.objects.get(id=idChapitre)
		chapitre.files.add(fichier)
		return redirect('editeChapitre', idCours=idCours, idChapitre=idChapitre)
	else:
		idCours = request.POST['idCours']
		idChapitre = request.POST['idChapitre']
		return render(request, "ajouterFichier.html", locals())

@login_required(login_url='login')
def ajouterQuizzeToChapitre(request):
	if request.method == 'POST' and 'ajouter' in request.POST:
		titre = request.POST['titre']
		description = request.POST['description']
		image = request.FILES['image']
		idChapitre = request.POST['idChapitre']
		idCours = request.POST['idCours']
		quizze = Quizze.objects.create(titre=titre, description=description, image=image)
		quizze.save()
		chapitre = Chapitre.objects.get(id=idChapitre)
		chapitre.quizzes.add(quizze)
		return redirect('editeChapitre', idCours=idCours, idChapitre=idChapitre)
	else:
		idCours = request.POST['idCours']
		idChapitre = request.POST['idChapitre']
		return render(request, "ajouterQuizzeToChapitre.html", locals())


def quizze(request, id):
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
	return render(request, 'quizze.html', locals())

@login_required(login_url='login')
def deleteFile(request, idCours, idChapitre, idFile):
	file = File.objects.get(id=idFile)
	file.delete()
	return redirect('editeChapitre', idCours=idCours, idChapitre=idChapitre)
