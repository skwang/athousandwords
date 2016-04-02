from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from clarifai.client import ClarifaiApi
from urlparse import urlparse
import httplib

# from models import *
# from forms import *
# import random


def index(request):
    return render(request, 'atw_app/index.html')

def generate_quote(request):
    url = request.GET['url']
    if not verify_image(url):
        quote = 'The fattest chicken is the first to go'
        speaker = 'They'
        valid = False
        return JsonResponse({'quote':quote, 'speaker':speaker, 'valid':valid})
    else:
        quote = 'The fattest chicken is the first to go'
        speaker = 'They'
        valid = True
        return JsonResponse({'quote':quote, 'speaker':speaker, 'valid':valid})

# Helper method to verify if a given string url points to an image
def verify_image(url):
    # requires the http
    if "http" not in url:
        url = "http://" + url
    parse_object = urlparse(url)
    try:
        conn = httplib.HTTPConnection(parse_object.netloc)
        conn.request("HEAD", parse_object.path)
        res = conn.getresponse()
        headers = res.getheaders()
        for header in headers:
            if header[0] == 'content-type':
                if 'image' in header[1]:
                    return True
        return False
    except:
        return False
