from django.db import models

class Pictures(models.Model):
    uploadedFile = models.FileField(upload_to = "")

class count(models.Model):
    name = models.TextField()
    text = models.TextField('распознанный текст',default='')
    sender = models.CharField('имя аккаунта',max_length=200,default='SOME STRING')
    recipients = models.TextField('получатели записи', default='')