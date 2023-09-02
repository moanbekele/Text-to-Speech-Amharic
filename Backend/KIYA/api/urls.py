from django.urls import path
from .main import views

urlpatterns = [
    path('', views.getData),
    path('tts/', views.addTTS),
]
