# coding: utf-8

from django.test import TestCase
from django.forms import FileField

from model_mommy import mommy

from core.views import parse_file
from core.forms import UploadForm
from core.models import Purchase, UploadAction

class TestViews(TestCase):
    """ Test app's URLs """

    def setUp(self):
        self.resp = self.client.get('/')

    def test_home_status_code_200(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'core/home.html')

    def test_form_instance(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, UploadForm)


class TestForm(TestCase):

    def test_redirect_on_success(self):
        with open('example_input.tab', 'rb') as tabfile:
            resp = self.client.post('/', {'sourcefile': tabfile})
            self.assertRedirects(resp, '/success/')

    def test_form_fail(self):
        resp = self.client.post('/', {})
        form = resp.context['form']
        self.assertFalse(form.is_valid())

    def test_form_has_filefield(self):
        resp = self.client.get('/')
        form = resp.context['form']
        self.assertIsInstance(
            form.fields['sourcefile'], FileField)

    def test_file_is_parsed(self):
        """ tests field success parsing titles by comparing two sets """
        with open('example_input.tab') as f:
            content = parse_file(f)
            expected = {
                'item price', 'merchant address', 'purchase count',
                'item description', 'purchaser name', 'merchant name'
                }
            self.assertEqual(expected, set(content.__next__().keys()))


class TestModels(TestCase):
    def setUp(self):
        self.purchase = mommy.make(Purchase)

    def test_purchase_was_created(self):
        self.assertEquals(1, self.purchase.pk)

    def test_purchase_has_fields(self):
        fields = ['item_price', 'merchant_address', 'purchase_count',
                  'item_description', 'purchaser_name', 'merchant_name']
        model_fields = set(self.purchase.__dict__.keys())

        n = set(fields).intersection(model_fields)

        self.assertEqual(set(fields), n)

    def test_receita_bruta(self):
        p1 = self.purchase
        p2 = mommy.make(Purchase)

        total = (
            p1.item_price * p1.purchase_count +
            p2.item_price * p2.purchase_count)

        receita_bruta = Purchase.total_receipt()

        self.assertEqual(total, receita_bruta)

    def test_total_receita_upload(self):
        Purchase.objects.all().delete()

        u1 = mommy.make(UploadAction)
        u2 = mommy.make(UploadAction)

        self.make_purchases(u1, 3)
        self.make_purchases(u2, 5)

        rec1 = UploadAction.upload_receipt(u1)
        rec2 = UploadAction.upload_receipt(u2)

        self.assertEqual(Purchase.total_receipt(), rec1+rec2)

    def make_purchases(self, uploadaction, number):
        for i in range(number):
            mommy.make(Purchase, uploadaction=uploadaction)
