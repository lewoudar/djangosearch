from django.core.paginator import Paginator, Page
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django_htmx.middleware import HtmxDetails

from djangosearch.starwars.models import Character
from watson import search


# Typing pattern recommended by django-stubs:
# https://github.com/typeddjango/django-stubs#how-can-i-create-a-httprequest-thats-guaranteed-to-have-an-authenticated-user
class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


ITEMS_PER_PAGE = 10


def get_page_obj(characters: QuerySet, page: str = '1') -> Page:
    paginator = Paginator(characters, ITEMS_PER_PAGE)
    return paginator.get_page(page)


def list_characters(request: HtmxHttpRequest):
    page = request.GET.get('page', '1')
    user_search = request.GET.get('search', '')
    query_set = search.filter(Character, user_search) if user_search else Character.objects.all()
    page_obj = get_page_obj(query_set, page)
    context = {'characters': page_obj, 'user_search': user_search}

    if request.htmx:
        return render(request, 'starwars/list_characters.html#character-list', context)

    return render(request, 'starwars/list_characters.html', context)


def show_character(request: HtmxHttpRequest, pk: int):
    character = get_object_or_404(Character.objects.prefetch_related('movies'), pk=pk)
    return render(request, 'starwars/show_character.html', {'character': character})
