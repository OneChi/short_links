from .services import UrlsController
from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ValidationError

from django.shortcuts import render
from django.views.generic import TemplateView

NO_URL = 'we_dont_recieve_url'

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
        try:
            requested_url = request.POST.get('url', NO_URL)
            short_link = self.short_urls_clas.get_short_url(requested_url)
            return HttpResponse(content=short_link)
        except ValidationError as ex:
            return HttpResponse(ex)

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
