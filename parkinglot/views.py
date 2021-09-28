import math
from tracemalloc import start
from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.conf import settings
import requests
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .models import *
import csv

@csrf_exempt
def add_parking_lot(request):
    res={}
    if request.method!='POST':
        res['status']="Invalid Method"
        return HttpResponse(json.dumps(res), content_type='application/json')  
     
    parking_name=request.POST.get("parking_name",'')
    parking_address=request.POST.get('parking_address','')
    manager_name=request.POST.get('manager_name','')
    manager_phone=request.POST.get('manager_phone','')
    
    print(parking_name,parking_address,manager_phone,manager_name)
    if parking_name=="" or parking_address=="":
        res={"status":"parking name and address should be mentioned"}
        return HttpResponse(json.dumps(res), content_type='application/json')
    parking_obj=ParkingLot.objects.filter(parking_slot_name=parking_name).first()
    if parking_obj:
        res={"status":"parking_exists"}
        return HttpResponse(json.dumps(res), content_type='application/json')
    new_parking_obj=ParkingLot(parking_slot_name=parking_name,parking_slot_adress=parking_address,manager_name=manager_name,manager_phone=manager_phone)
    new_parking_obj.save()
    res={"status":"parking-registered-successfully"}
    return HttpResponse(json.dumps(res), content_type='application/json')     
             #check for existing parking lot on same address
@csrf_exempt
def register_rate_card(request):
    res={}
    if request.method!='POST':
        res['status']="Invalid Method"
        return HttpResponse(json.dumps(res), content_type='application/json')
    slot_type=request.POST.get("slot_type",'')
    start_hour=request.POST.get("start_hour",'')
    end_hour=request.POST.get("end_hour",'')
    pricing=request.POST.get("pricing",'')
    parking_lot=request.POST.get("parking_lot",'')  #parking lot db id
    if slot_type=="" or start_hour=="" or end_hour=="" or pricing=="" or parking_lot=="":
        res={"status":"please mention all fields"}
        return HttpResponse(json.dumps(res), content_type='application/json')
    parking_obj=ParkingLot.objects.filter(id=int(parking_lot)).first()
    if not parking_obj:
        res={"status":"Parking Object does not exist"}
        return HttpResponse(json.dumps(res), content_type='application/json')
    
    rate_card=Ratecard(slot_type=slot_type,start_hour=start_hour,end_hour=end_hour,pricing=pricing,parking_lot=parking_obj)
    rate_card.save()
    res={"status":"ratecard-registered-successfully"}
    return HttpResponse(json.dumps(res), content_type='application/json')    

@csrf_exempt
def find_spot_and_park(request):
    res={}
    if request.method!='POST':
        res['status']="Invalid Method"
        return HttpResponse(json.dumps(res), content_type='application/json')
    vehicle_number=request.POST.get("vehicle_number",'')
    slot_type=request.POST.get("slot_type",'')
    driving_license=request.POST.get("driving_license",'')

    spot_obj=Spot.objects.filter(is_Occupied=False,slot_type=slot_type).order_by('id').first()
    if not spot_obj:
        res={"status":"All spots are full"}
        return HttpResponse(json.dumps(res), content_type='application/json')
    vehicle_obj=Vehicle(vehicle_number=vehicle_number,driving_license=driving_license)
    vehicle_obj.save()                #vehicle object entring the system
    spot_obj.is_Occupied=True
    spot_obj.vehicle_list.add(vehicle_obj)
    spot_obj.save()
    res={"status":"parked-successfully"}
    return HttpResponse(json.dumps(res), content_type='application/json')


@csrf_exempt
def exit_booking_complete(request):
    res={}
    if request.method!='POST':
        res['status']="Invalid Method"
        return HttpResponse(json.dumps(res), content_type='application/json')
    vehicle_id=request.POST.get("vehicle_id",'')  #from request at the time of exit will be issue by manager at exit gate
    vehicle_type=request.POST.get("vehicle_type",'') #he will also send vehicle_type at the time of exit
    parking_lot_id=request.POST.get("vehicle_type",'') #this would be auto generated from frotend app
    spot_id= request.POST.get("spot_id",'')  #manager will ask for spot recipt booked at the the time of entry and he will pass this spot id fro rice card
    spot_obj=Spot.objects.filter(id=int(spot_id)).first()
    parking_lot_obj=ParkingLot.objects.filter(id=int(parking_lot_id)).first() #from request at the time of exit
    exit_time=timezone.now()  #exit time will be the timestamp of booking exit
    vehicle_obj=Vehicle.objects.filter(id=int(vehicle_id)).first()
    if spot_obj is None or parking_lot_obj is None:
        res={"status":"OOPS ! SOMETHING WENT WRONG"}
        return HttpResponse(json.dumps(res), content_type='application/json')
    if not vehicle_obj:
        res={"status":"Vehicle not found"}
        return HttpResponse(json.dumps(res), content_type='application/json')
    start_time=vehicle_obj.system_entry   #startime of vehicle willl be recorded as it was saved at the time of vehicle obj formation
    time_duration=(exit_time-start_time).total_seconds()/3600   ## time duration in hours
    print(time_duration)

    #find the pricing card for the ride suppose car stays for 6.5 hour so we will find out 6.5 lies between which start and end time for that parking lot and vehicle type
    rate_card_obj=Ratecard.objects.filter(start_hour__lte=time_duration, end_hour__gte=time_duration,parking_lot=parking_lot_obj,slot_type=vehicle_type).first()
    price=rate_card_obj.pricing
    print(price)

    #forming final booking object
    booking_obj=Booking(parking_lot_entry_time=start_time,parking_lot_exit_time=exit_time,vehicle_used=vehicle_obj,pricing=rate_card_obj,spot_used=spot_obj)
    #completing booking

    #MAKING SPOT FREE AGAIN TO BE USED AGAIN
    spot_obj.is_Occupied=False
    ##########
    spot_obj.save()
    booking_obj.save()
    rate_card_obj.save()
    parking_lot_obj.save()
    return HttpResponse(json.dumps(res), content_type='application/json')

def find_parking_history_by_vehicle(request):
    res={}
    #this will be a get method for query searching
    if request.method=='POST':
        res['status']="Invalid Method"
        return HttpResponse(json.dumps(res), content_type='application/json')
    vehicle_id=request.GET.get("vehicle_id",'')
    vehicle_obj=Vehicle.objects.filter(id=int(vehicle_id)).first()
    if not vehicle_obj:
        res={"status":"Vehicle not found"}
        return HttpResponse(json.dumps(res), content_type='application/json')
    
    #FINDING ALL BOOKING WITH THE VEHICLE OBJ USED
    #to find parking lot history by vehcile we need to print the booking object associated with that vehicle id.
    all_booking=Booking.objects.filter(vehicle_used=vehicle_obj)
    print(all_booking)  #will print the booking detials for each booking
    res['all_bookings']=all_booking
    return HttpResponse(json.dumps(res), content_type='application/json')




    