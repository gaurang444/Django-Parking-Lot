from django.contrib import admin
from django.urls import path
from parkinglot.urls import parkinglot_urlpatterns
from django.conf.urls import url,include

urlpatterns = [
    url(r'^parking-lot/', include((parkinglot_urlpatterns, 'parking-lot-url-patterns'), namespace='parking-lot-urls')),
    url(r'^admin/',(admin.site.urls)),
]