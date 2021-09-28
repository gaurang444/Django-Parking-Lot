from django.contrib import admin
from django.urls import path
from django.conf.urls import url
import parkinglot.views as views

parkinglot_urlpatterns = [
    url(r'^add-parking/$',views.add_parking_lot, name='add='),
    url(r'^register-rate-card/$',views.register_rate_card, name='register-rate-card'),
    url(r'^find-spot-parking/$',views.find_spot_and_park, name='find-spot-parking'),
    url(r'^exit-parking/$',views.exit_booking_complete, name='exit-parkinglot'),
    url(r'^parking-history/$',views.find_parking_history_by_vehicle, name='parking-history'),    
]