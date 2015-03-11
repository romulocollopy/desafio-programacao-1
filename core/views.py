# coding: utf-8

import csv

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView

from core.forms import UploadForm, PurchaseForm
from core.models import Purchase, UploadAction

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
    ua = parse_file(file)

    return HttpResponseRedirect('/success/', {'ua': ua})


def success(request):
    import ipdb; ipdb.set_trace()
    upload_receipt = UploadAction.upload_receipt()
    return HttpResponse(
        'A receita bruta do upload é de {}'.format(upload_receipt)
        )


def parse_file(file):
    ua = UploadAction()
    content = csv.DictReader(file, dialect='excel-tab')

    for i in content:
        i['uploadaction'] = ua
        pf = PurchaseForm(i)
        pf.save()

    return ua

