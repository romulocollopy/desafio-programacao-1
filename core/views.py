# coding: utf-8

import csv
from io import TextIOWrapper

from django.shortcuts import (
    render, HttpResponseRedirect, HttpResponse, get_object_or_404
    )
from django.views.generic.base import TemplateView

from utils import ws_to_under

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

    file = TextIOWrapper(request.FILES['sourcefile'].file, encoding='utf-8')
    file_data = parse_file(file)
    ua = save_data(file_data)
    redirect_url = '/upload-detail/{}'.format(ua.pk)
    return HttpResponseRedirect(redirect_url)


def upload_detail(request, id):
    ua = get_object_or_404(UploadAction, pk=id)
    upload_receipt = UploadAction.upload_receipt(ua)
    context = dict(
        uploadfile = ua,
        total = upload_receipt
        )
    return render(request, 'core/detail.html', context)


def parse_file(file):
    content = csv.DictReader(file, dialect='excel-tab')

    dict_list = []
    for line in content:
        dict_list += [{ws_to_under(k): v for k, v in line.items()}]

    return dict_list


def save_data(dict_list):
    ua = UploadAction()
    ua.save()

    for line in dict_list:
        pf = PurchaseForm(line)

        if not pf.is_valid():
            continue

        pf.instance.uploadaction = ua
        pf.save()

    return ua
