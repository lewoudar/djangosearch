from django.urls import path

from . import views

app_name = 'starwars'
urlpatterns = [
    path('', views.list_characters, name='index'),
    path('<int:pk>/', views.show_character, name='show-character'),
]
