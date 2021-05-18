from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('movie/<int:movie_id>/', views.movie, name='movie'),
    path('actor/<int:actor_id>/', views.actor, name='actor'),

]