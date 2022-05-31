import os

from django.db import models

# Create your models here.
class Document(models.Model):
    uploadedFile = models.FileField(upload_to = "Uploaded Files/")

class TextAudio(models.Model):
    title = models.CharField('имя записи', max_length=200,default='SOME STRING')
    text = models.TextField('текст записи')
    sender = models.CharField('имя аккаунта',max_length=200,default='SOME STRING')
    recipients = models.TextField('получатели записи', default='')







