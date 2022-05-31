from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "cnv"

urlpatterns = [
    path('',views.main, name='main'),
    path('history',views.history, name='history'),
    path('history/<int:id>/', views.detail, name='detail'),
]