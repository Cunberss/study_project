from django.db import models


class AudioText(models.Model):
    title = models.CharField('имя записи', max_length=200,default='')
    uploadedFile = models.CharField('путь до файла', max_length=200,default='')
    sender = models.CharField('имя аккаунта',max_length=200,default='')
    namefile = models.CharField('имя файла', max_length=200,default='')
    recipients = models.TextField('получатели записи', default='')
# Create your models here.
