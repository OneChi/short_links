from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm, ModelForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView,FormView
from django.views.generic import View, TemplateView
from django.urls import reverse_lazy

NO_URL = 'we_dont_recieve_url'

from .services import UrlsController
# Create your views here.

class HomePage(TemplateView):
    template_name = 'index.html'

    def __init__(self, **kwargs: Any) -> None:
        self.text = 0
        super().__init__(**kwargs)
        self.short_urls_clas = UrlsController()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_text'] = kwargs['request'].method
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs) -> HttpResponse:
        validator = URLValidator()
        requested_url = request.POST.get('url', NO_URL)
        try:
            validator(requested_url)
            short_link = self.short_urls_clas.get_short_url(requested_url)
            return HttpResponse(content=short_link)
        except ValidationError as ex:
            return HttpResponse('Непозволительная ссылка!')
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(request, 'index.html')


class Redirector(TemplateView):
    template_name = 'index.html'


    def __init__(self, **kwargs: Any) -> None:
        self.text = 0
        super().__init__(**kwargs)
        self.short_urls_clas = UrlsController()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_text'] = 'Hello text'
        return context

    def get(self, request: HttpRequest, url, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponseRedirect(self.short_urls_clas.get_full_url(url))
    
        