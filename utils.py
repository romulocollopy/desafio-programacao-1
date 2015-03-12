from django.core.files.uploadedfile import InMemoryUploadedFile


def ws_to_under(string):
    return string.replace(" ", "_")

