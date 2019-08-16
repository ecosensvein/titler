from django.views.generic import TemplateView
from django.urls import path

app_name = 'titler'
urlpatterns = [
    path('', TemplateView.as_view(template_name="collector/index.html"),
         name='index'),
]
