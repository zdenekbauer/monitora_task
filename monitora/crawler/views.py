from django.http import Http404
from django.shortcuts import render

from .models import Actor, Movie
from .forms import SearchForm

from unidecode import unidecode


def search(request):
    form = SearchForm()
    context = {
        'error_message': "",
        'form': form,
        'movies': None,
        'actors': None,
    }

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_value = form.cleaned_data['search'].replace(" ", "").lower()
            context['movies'] = Movie.objects.filter(
                stripped_name__contains=unidecode(search_value)
            ).all()
            context['actors'] = Actor.objects.filter(
                stripped_name__contains=unidecode(search_value)
            ).all()

    return render(request, 'crawler/search.html', context)


def movie(request, movie_id):
    context = {
        'error_message': "",
        'type': 'actor',
        'data': None,
    }
    try:
        context['data'] = Movie.objects.get(id=movie_id).actor_set.all()
    except Movie.DoesNotExist:
        context['error_message'] = "Movie doesn't exist!"

    return render(request, 'crawler/detail.html', context)


def actor(request, actor_id):
    context = {
        'error_message': "",
        'type': 'movie',
        'data': None,
    }
    try:
        context['data'] = Actor.objects.get(id=actor_id).movies.all()
    except Actor.DoesNotExist:
        context['error_message'] = "Actor doesn't exist!"

    return render(request, 'crawler/detail.html', context)
