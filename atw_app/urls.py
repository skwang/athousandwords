from django.conf.urls import patterns, url
import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        ]