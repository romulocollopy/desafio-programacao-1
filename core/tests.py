# coding: utf-8

from django.test import TestCase
from core.forms import UploadForm
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile


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

    def test_form_has_filefield(self):
        form = self.resp.context['form']
        self.assertIsInstance(form.fields['sourcefile'], forms.FileField)


class TestForm(TestCase):
    def setUp(self):
        self.file = SimpleUploadedFile(
            "example_input.tab", b"some\tcontent", content_type="text/csv")

    def test_redirect_on_success(self):
        resp = self.client.post('/', {'sourcefile': self.file})
        self.assertRedirects(resp, '/success/')

    def test_form_fail(self):
        resp = self.client.post('/', {})
        form = resp.context['form']
        self.assertContains(resp, 'This field is required.')

