import datetime
import os
import re
import sys
import uuid
from .ysk import text_to_sound
from django.contrib import messages
from pydub import AudioSegment
import speech_recognition as speech_recog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
from .models import AudioText
from . import models
from playsound import playsound

sys.path.append(os.path.abspath('..'))
from recognition import models as mod


@login_required
@csrf_exempt
def texttospeech(request):
    if request.method == 'POST':
        uploadedtext = request.POST.get('texts')
        try:
            s = gTTS(uploadedtext, lang='ru')
            filename = str(uuid.uuid4()) + '.mp3'
            s.save('media/Uploaded Files/' + filename)
            path = 'media/Uploaded Files/' + filename
            text = models.AudioText(
                title='Запись от ' + '.'.join(str(datetime.datetime.now()).split('.')[:-1]),
                uploadedFile=path,
                sender=str(request.user.username),
                namefile=filename
            )
            text.save()
            messages.info(request, 'Запись переведена в аудио!')
        except:
            messages.info(request, 'Извините, мне не понятен ваш текст')
        return render(request, 'texttospeech/texttospeechmain.html')

    else:
        return render(request, 'texttospeech/texttospeechmain.html')


@login_required
def history(request):
    latest_text_list = AudioText.objects.filter(sender=str(request.user.username)).order_by('-id')
    return render(request, 'texttospeech/historytwo.html', {'latest_text_list': latest_text_list})


@csrf_exempt
@login_required
def detail(request, id):
    if request.method == 'GET':
        try:
            a = AudioText.objects.get(id=id)
        except:
            raise Http404('Запись не найдена!')
        if a.sender == request.user.username:
            return render(request, 'texttospeech/detailaudio.html', {'text': a})
        else:
            return HttpResponse('Запись не найдена')

    elif (request.method == "POST") and ('Отправить запись' in request.POST):
        users = User.objects.all()
        users_list = str(users)
        nameuser = str(request.POST.get('nameuser'))

        if re.search(r'\<User: ' + nameuser + r'\>', users_list) is None or nameuser == str(request.user.username):
            a = AudioText.objects.get(id=id)
            messages.info(request, 'Такого пользователя не существует или вы пытаетесь отправить себе')
            return render(request, 'texttospeech/detailaudio.html', {'text': a})
        else:
            a = AudioText.objects.get(id=id)
            a.recipients += str(request.POST.get('nameuser')) + ','
            a.save()
            messages.info(request, 'Запись отправлена пользователю:' + str(request.POST.get('nameuser')))
            return render(request, 'texttospeech/detailaudio.html', {'text': a})

    elif (request.method == "POST") and ('Удалить' in request.POST):
        a = AudioText.objects.get(id=id)
        a.delete()
        return redirect('/texttospeech/history')

    elif (request.method == "POST") and ('Перевести в текст' in request.POST):
        a = AudioText.objects.get(id=id)
        try:
            filename = a.namefile

            sound = AudioSegment.from_mp3('media/Uploaded Files/' + filename)

            sound.export('media/Result Files/' + filename + '.wav', format="wav")
            sample_audio = speech_recog.AudioFile('media/Result Files/' + filename + '.wav')
            recog = speech_recog.Recognizer()
            with sample_audio as audio_file:
                audio_content = recog.record(audio_file)
            result = recog.recognize_google(audio_content, language='ru-RU')
            os.remove('media/Result Files/' + filename + '.wav')
            textaudio = mod.TextAudio(
                text=result,
                title='Запись от ' + '.'.join(str(datetime.datetime.now()).split('.')[:-1]),
                sender=str(request.user.username)
            )
            textaudio.save()
            messages.info(request, 'Запись переведена в текст!')
        except:
            messages.info(request, 'Что-то пошло не так')
        return render(request, 'texttospeech/detailaudio.html', {'text': a})
    else:
        return HttpResponse(200)


@login_required
def sendhistory(request):
    user = request.user.username
    latest_text_list = AudioText.objects.filter(recipients__contains=str(user)).order_by('-id')
    return render(request, 'texttospeech/sendhistory.html', {'latest_text_list': latest_text_list})


@csrf_exempt
@login_required
def detailsend(request, id):
    if request.method == 'GET':
        try:
            a = AudioText.objects.get(id=id)
        except:
            raise Http404('Запись не найдена!')
        if request.user.username in a.recipients.split(','):
            return render(request, 'texttospeech/senddetail.html', {'text': a})
        else:
            return HttpResponse('Эта не ваша запись!')

    elif (request.method == "POST") and ('Перевести в текст' in request.POST):
        a = AudioText.objects.get(id=id)
        filename = a.namefile

        sound = AudioSegment.from_mp3('media/Uploaded Files/' + filename)

        sound.export('media/Result Files/' + filename + '.wav', format="wav")

        sample_audio = speech_recog.AudioFile('media/Result Files/' + filename + '.wav')
        recog = speech_recog.Recognizer()
        with sample_audio as audio_file:
            audio_content = recog.record(audio_file)
        result = recog.recognize_google(audio_content, language='ru-RU')
        os.remove('media/Result Files/' + filename + '.wav')
        textaudio = mod.TextAudio(
            text=result,
            title='Запись от ' + '.'.join(str(datetime.datetime.now()).split('.')[:-1]),
            sender=str(request.user.username)
        )
        textaudio.save()
        messages.info(request, 'Запись переведена в текст!')
        return render(request, 'texttospeech/detailaudio.html', {'text': a})

    elif (request.method == "POST") and ('Удалить' in request.POST):
        a = AudioText.objects.get(id=id)
        recip = a.recipients
        rec = recip.replace(str(request.user.username) + ',', ' ')
        a.recipients = rec
        a.save()
        return redirect('/texttospeech/sendhistory')


    else:
        return HttpResponse(200)


@login_required
@csrf_exempt
def yandexkit(request):
    if request.method == 'POST':
        uploadedtext = request.POST.get('texts')
        print(uploadedtext)

        iam_token = 't1.9euelZqRy5uayY6Oz5TJloqUzpqWx-3rnpWaiZSNmJmMjJKVzZiTkZSUz43l8_c2XF9t-e8IIzlE_t3z93YKXW357wgjOUT-.rR6gN3w-ogyhcN3cFfLYAY395Obo2Lmts4n63MRF3-hvWJjEcD7CqdOXJFt0TSfhijEQZyaiNWCHtGgG1l7bDQ'
        folder_id = 'b1gcj077528pofd7e90e'

        if request.POST.get('Select') == '1':
            voice = 'alena'
        elif request.POST.get('Select') == '2':
            voice = 'oksana:rc'
        elif request.POST.get('Select') == '3':
            voice = 'filipp'
        else:
            voice = 'ermil:rc'

        filename = text_to_sound(iam_token, folder_id, uploadedtext, voice)
        path = 'media/Uploaded Files/' + filename
        text = models.AudioText(
            title='Запись от ' + '.'.join(str(datetime.datetime.now()).split('.')[:-1]),
            uploadedFile=path,
            sender=str(request.user.username),
            namefile=filename
        )
        text.save()
        messages.info(request, 'Запись переведена в аудио!')
        return render(request, 'texttospeech/yandexkit.html')

    else:
        return render(request, 'texttospeech/yandexkit.html')


