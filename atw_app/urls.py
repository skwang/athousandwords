from django.conf.urls import patterns, url
import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^generate-quote/$', views.generate_quote, name='generate_quote'),
        ]