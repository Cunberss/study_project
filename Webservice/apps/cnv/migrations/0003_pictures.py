# Generated by Django 3.2.12 on 2022-03-21 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnv', '0002_auto_20220321_1255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploadedFile', models.FileField(upload_to='')),
            ],
        ),
    ]
