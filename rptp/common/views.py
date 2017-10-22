from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse


def main_view(request: HttpRequest):
    return redirect(reverse('client:video:search'))
