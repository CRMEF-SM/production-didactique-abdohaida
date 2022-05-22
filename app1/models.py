from django.db import models

# Create your models here.
class Video(models.Model):
	titre = models.CharField(max_length=30)
	description = models.TextField()
	videoFile = models.FileField(upload_to='video/', null=True, verbose_name="Le video")

	def __str__(self):
		return self.titre