# Generated by Django 3.2.12 on 2022-03-02 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recognition', '0004_textaudio_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='textaudio',
            name='sender',
            field=models.CharField(default='SOME STRING', max_length=200, verbose_name='имя аккаунта'),
        ),
    ]
