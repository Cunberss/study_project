from . import views
from django.urls import path

app_name = 'texttospeech'

urlpatterns = [
    path('', views.texttospeech, name = 'texttospeech'),
    path('history/', views.history, name = 'history'),
    path('history/<int:id>/',views.detail, name = 'detail'),
    path('sendhistory/', views.sendhistory, name='sendhistory'),
    path('sendhistory/<int:id>/', views.detailsend, name='detailsend'),
    path('yandexkit', views.yandexkit, name = 'yandexkit'),
]