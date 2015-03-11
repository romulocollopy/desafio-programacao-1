# coding: utf-8

from django import forms
from django.forms import ModelForm
from core.models import Purchase

class UploadForm(forms.Form):
    sourcefile = forms.FileField()


class PurchaseForm(ModelForm):

    class Meta:
        model = Purchase

        fields = [
            'item_price', 'merchant_address', 'purchase_count',
            'item_description', 'purchaser_name', 'merchant_name'
        ]
