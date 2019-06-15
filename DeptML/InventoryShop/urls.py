from django.urls import path
from django.conf.urls import url

from django.contrib import admin
from .import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='inventory-home'),
    url(r'^iosdeveloper/$', views.iosdeveloper, name='inventory-iosdeveloper'),
    url(r'^datascientist/$', views.datascientist, name='inventory-datascientist'),
    url(r'^softwaretester/$', views.softwaretester, name='softwaretester')
    #url(r'^train/$', Train.as_view(), name="train"),
    #url(r'^predict/$', Predict.as_view(), name="predict"),
]
