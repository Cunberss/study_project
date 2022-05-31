import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('recognition/', include('recognition.urls')),
    path('admin/', admin.site.urls),
    path('',views.function, name = 'function'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("signup/", include('registration.urls')),
    path('texttospeech/', include('texttospeech.urls')),
    path('news/',views.news,name='news'),
    path('cnv/',include('cnv.urls'))
]

urlpatterns += static('/media/Uploaded Files', document_root=os.path.join(settings.BASE_DIR, 'media/Uploaded Files/'))
urlpatterns += static('/media/Result Files', document_root=os.path.join(settings.BASE_DIR, 'media/Result Files/'))