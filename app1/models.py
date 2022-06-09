from django.db import models

# Create your models here.
class Video(models.Model):
	titre = models.CharField(max_length=30)
	description = models.TextField()
	videoFile = models.FileField(upload_to='video/', null=True, verbose_name="Le video")

	def __str__(self):
		return self.titre

class Question(models.Model):
	question = models.TextField()
	choix1 = models.CharField(max_length=80)
	choix2 = models.CharField(max_length=80)
	choix3 = models.CharField(max_length=80)
	choix4 = models.CharField(max_length=80)
	reponse = models.CharField(max_length=80)

	def __str__(self):
		return self.question

class Quizze(models.Model):
	titre = models.CharField(max_length=100)
	description = models.TextField()
	questions = models.ManyToManyField(Question)

	def __str__(self):
		return self.titre

class Partie(models.Model):
	titrePartie = models.CharField(max_length=100)
	content = models.TextField()

	def __str__(self):
		return self.titrePartie

class Chapitre(models.Model):
	titreChapitre = models.CharField(max_length=100)
	parties = models.ManyToManyField(Partie)

	def __str__(self):
		return self.titreChapitre

class Cours(models.Model):
	titreCours = models.CharField(max_length=100)
	image = models.ImageField(upload_to='img/cours', default='image')
	description = models.TextField()
	chapitres = models.ManyToManyField(Chapitre)

	def __str__(self):
		return self.titreCours

