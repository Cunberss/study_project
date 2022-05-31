import os
import uuid
import datetime

import docx
import pytesseract
from django.contrib import messages
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from googletrans import Translator

from .forms import form0
from .models import count,Pictures
import PIL.Image
from io import BytesIO
import base64
from django.http import HttpResponseRedirect, HttpResponse, Http404


@login_required
def main(request):
    if request.method == 'POST' and ('Обработать' in request.POST):
        form = form0(request.POST)
        tim = request.POST.get('im')
        names = str(uuid.uuid4())
        if form.is_valid():
            data = base64.b64decode(tim)
            img0 = "media/" + names + '.png'
            with open(img0, 'wb') as f:
                f.write(data)
            img1 = PIL.Image.open(img0)
            # Распознавалка
            try:
                #text = pytesseract.image_to_string(img1, lang='rus')[:-2]
                text = names + 'Урарарара'
                if len(text) == 0:
                    messages.info(request, 'Не смог что-то понять:(')
                    return render(request,'cnv/canvas.html')
            except:
                os.remove(img0)
                messages.info(request, 'Что то пошло не так!')
                return render(request,'cnv/canvas.html')
            os.remove(img0)
            o = count(name='Текст от ' + '.'.join(str(datetime.datetime.now()).split('.')[:-1]),
                      text=text,
                      sender=str(request.user.username),
                      )
            o.save()
            messages.info(request, 'Изображение обработано!')
            return redirect('/cnv/history')
        else:
            return HttpResponseRedirect('/lose')

    elif (request.method == 'POST') and ('Отправить' in request.POST):
        try:
            uploadedFile = request.FILES["uploadedFile"]
            filename, file_extension = os.path.splitext(uploadedFile.name)
            allowed_extension = ['.png','.bmp','.jpeg']
            if file_extension not in allowed_extension:
                messages.info(request, 'Недопустимый формат!')
                return render(request,'cnv/canvas.html')
            filename = str(uuid.uuid4()) + file_extension
            uploadedFile.name = filename
            pict = Pictures(
                uploadedFile=uploadedFile
            )
            pict.save()

            image = Image.open('media/' + filename)

            text = filename + 'Урурарара'
            #text = pytesseract.image_to_string(image, lang='rus')

            o = count(name='Текст от ' + '.'.join(str(datetime.datetime.now()).split('.')[:-1]),
                    text=text,
                    sender=str(request.user.username),
                    )
            o.save()
            os.remove('media/' + filename)
            messages.info(request, 'Изображение обработано!')
            return redirect('/cnv/history')
        except:
            messages.info(request, 'Что-то пошло не так!')
            return render(request,'cnv/canvas.html')

    else:
        return render(request, 'cnv/canvas.html')


@login_required
def history(request):
    latest_text_list = count.objects.filter(sender=str(request.user.username)).order_by('-id')
    return render(request, 'cnv/cnvhistory.html', {'latest_text_list': latest_text_list})


@csrf_exempt
@login_required
def detail(request, id):
    if request.method == 'GET':
        try:
            a = count.objects.get(id=id)
        except:
            raise Http404('Запись не найдена!')
        if a.sender == request.user.username:
            return render(request, 'cnv/cnvdetail.html', {'text': a})
        else:
            return HttpResponse('Запись не найдена')

    elif (request.method == "POST") and ('Удалить' in request.POST):
        a = count.objects.get(id=id)
        a.delete()
        return redirect('/cnv/history')

    elif (request.method == "POST") and ('Сохранить в Word' in request.POST):
        a = count.objects.get(id=id)
        doc = docx.Document()
        doc.add_paragraph(a.text)
        doc.save('media/Result Files/' + a.name + '_' + str(a.id) + '.docx')
        return redirect('/media/Result Files/' + a.name + '_' + str(a.id) + '.docx')

    elif (request.method == "POST") and ('Перевести' in request.POST):
        a = count.objects.get(id=id)
        translator = Translator()
        if request.POST.get('Selectedeng') == '1':
            result = translator.translate(a.text, src='ru', dest='en')
            a.text = result.text
            a.save()
        else:
            result = translator.translate(a.text, src='en', dest='ru')
            a.text = result.text
            a.save()
        return render(request, 'cnv/cnvdetail.html', {'text': a})

    else:
        return HttpResponse(200)