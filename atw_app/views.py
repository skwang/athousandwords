from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from clarifai.client import ClarifaiApi
from urlparse import urlparse
import httplib
from sentiment import generateQuote


def index(request):
    return render(request, 'atw_app/index.html')

def generate_quote(request):
    url = request.GET['url']
    if not verify_image(url): # not a valid image url
        quote = 'The fattest chicken is the first to go'
        speaker = 'They'
        valid = False
        return JsonResponse({'quote':quote, 'speaker':speaker, 'valid':valid})
    else: 
        tags, probs = get_tags_and_probs(url)
        quote = generateQuote(tags, probs)
        # quote = "Creative force, like a musical composer, goes on unweariedly repeating a simple air or theme, now high, now low, in solo, in chorus, ten thousand times reverberated, till it fills earth and heaven with the chant."
        # print quote
        speaker = 'Anonymous'
        valid = True
        return JsonResponse({'quote':quote, 'speaker':speaker, 'valid':valid})

def get_tags_and_probs(url):
    clarifai_api = ClarifaiApi()  
    result = clarifai_api.tag_image_urls(url)
    tags = result['results'][0]['result']['tag']['classes']
    probs = result['results'][0]['result']['tag']['probs']
    #print tags
    #print probs
    return tags, probs

# Helper method to verify if a given string url points to an image
def verify_image(url):
    # requires the http in the start of the url to work
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
