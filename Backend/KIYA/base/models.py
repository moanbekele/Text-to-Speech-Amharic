from django.db import models

# Create your models here.

class Texttospeech(models.Model):
    text = models.CharField(max_length=200, null=True)
    audio = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)