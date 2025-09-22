from django.urls import path
from .views import DeepSeekGenerateView, HuggingFaceGenerateView

urlpatterns = [
    path('deepseek/generate/', DeepSeekGenerateView.as_view(), name='deepseek-generate'),
    path('huggingface/generate/', HuggingFaceGenerateView.as_view(), name='huggingface-generate'),
]
