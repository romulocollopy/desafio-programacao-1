# coding: utf-8

from django.test import TestCase
from core.forms import UploadForm
from django import forms
from core.views import parse_file

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

    # def test_redirect_on_success(self):
    #     with open('example_input.tab') as f:
    #         resp = self.client.post('/', {'sourcefile': f})
    #         self.assertRedirects(resp, '/success/')

    def test_form_fail(self):
        resp = self.client.post('/', {})
        form = resp.context['form']
        self.assertFalse(form.is_valid())

    def test_form_has_filefield(self):
        resp = self.client.get('/')
        form = resp.context['form']
        self.assertIsInstance(
            form.fields['sourcefile'], forms.FileField)

    def test_file_is_parsed(self):
        with open('example_input.tab') as f:
            content = parse_file(f)
            expected = ['purchaser name', 'item description', 'item price', 'purchase count', 'merchant address', 'merchant name']
            self.assertEqual(expected, content.__next__())


