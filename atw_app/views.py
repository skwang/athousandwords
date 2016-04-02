from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from clarifai.client import ClarifaiApi
import urllib
# from models import *
# from forms import *
# import random


def index(request):
    return render(request, 'atw_app/index.html')


def generate_quote(request):
    url = request.GET['url']
    image = urllib.URLopener()
    quote = 'A picture is worth a thousand words'
    speaker = 'Anonymous'
    return JsonResponse({'quote':quote, 'speaker':speaker})
