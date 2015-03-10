# coding: utf-8

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView

from core.forms import UploadForm


def home(request):
    if request.method == 'POST':
        return parse_form(request)

    context = dict(
        form=UploadForm(),
    )
    return render(request, 'core/home.html', context)


def parse_form(request):
    form = UploadForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'core/home.html', dict(form=form))

    file = form.cleaned_data.get('sourcefile')
    return parse_file(file)


def success(request):
    return HttpResponse('Success')


def parse_file(file):
    bitestr = file.read()

    return HttpResponseRedirect('/success/')