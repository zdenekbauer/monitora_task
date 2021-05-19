from django.shortcuts import render
from unidecode import unidecode

from .forms import SearchForm
from .models import Actor, Movie


def search(request):
    """
    Vyhledá všechny filmy a herce bez ohledu na čárky/háčky a mezery.
    """
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
            search_value = unidecode(
                form.cleaned_data['search'].replace(" ", "").lower()
            )
            context['movies'] = Movie.objects.filter(
                stripped_name__contains=search_value
            ).all()
            context['actors'] = Actor.objects.filter(
                stripped_name__contains=search_value
            ).all()

    return render(request, 'crawler/search.html', context)


def movie(request, movie_id):
    """
    Vyhledá všechny herce z daného filmu.
    """
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
    """
    Vyhledá všechny film z top300 pro daného herce.
    """
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
