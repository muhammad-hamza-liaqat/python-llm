from django.urls import path
from llm.views import DeepSeekGenerateView

urlpatterns = [
    path("generate/", DeepSeekGenerateView.as_view(), name="deepseek_generate"),
]
