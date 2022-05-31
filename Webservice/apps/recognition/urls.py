from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "recognition"

urlpatterns = [
    path('', views.index, name = 'index'),
    path('history/', views.history, name = 'history'),
    path('history/<int:id>/',views.detail, name = 'detail'),
    path('sendhistory/',views.sendhistory, name='sendhistory'),
    path('sendhistory/<int:id>/',views.detailsend, name='detailsend'),
    path('yandexkit/', views.yandexkit, name = 'yandexkit')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )