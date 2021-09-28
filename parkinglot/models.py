from django.db import models
from django.utils import timezone
from sqlalchemy import null

class Vehicle(models.Model):
    vehicle_number=models.CharField(max_length=30,blank=True,null=True)
    driving_license=models.CharField(max_length=30,blank=True,null=True)
    system_entry=models.DateTimeField(default=timezone.now)   #will serve as entry time for the booking

class Spot(models.Model):
    VEHICLE_TYPE = [
        ('TWO WHEELER', 'TWO WHEELER'),
        ('FOUR WHEELER', 'FOUR WHEELER'),
    ]
    slot_type=models.CharField(max_length=30, choices=VEHICLE_TYPE,blank=True,null=True)
    is_Occupied=  models.BooleanField(blank=True, null=True, default=False) 
    vehicle_list = models.ManyToManyField(Vehicle, blank=True,null=True)
    created_at=models.DateTimeField(default=timezone.now)

class ParkingLot(models.Model):
    parking_slot_name=models.CharField(max_length=255, null=True, blank=True)
    parking_slot_adress=models.CharField(max_length=255, null=True, blank=True)
    spot_list = models.ManyToManyField(Spot, blank=True,null=True)
    manager_name=models.CharField(max_length=255, null=True, blank=True)
    manager_phone=models.CharField(max_length=255, null=True, blank=True)
    is_Active=  models.BooleanField(blank=True, null=True, default=True) 
    created_at=models.DateTimeField(default=timezone.now)

class Ratecard(models.Model):
    VEHICLE_TYPE = [
        ('TWO WHEELER', 'TWO WHEELER'),
        ('FOUR WHEELER', 'FOUR WHEELER'),
    ]
    slot_type=models.CharField(max_length=30, choices=VEHICLE_TYPE,blank=True,null=True)
    start_hour=models.IntegerField(null=True, blank=True)
    end_hour=models.IntegerField(null=True, blank=True)
    pricing=models.IntegerField(null=True, blank=True)
    parking_lot=models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    created_at=models.DateTimeField(default=timezone.now)

class Booking(models.Model):
    parking_lot_entry_time= models.DateTimeField()
    parking_lot_exit_time= models.DateTimeField()
    spot_used =  models.ForeignKey(Spot, on_delete=models.CASCADE)
    vehicle_used=models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    booking_created_at=models.DateTimeField(default=timezone.now)
    pricing=models.ForeignKey(Ratecard, on_delete=models.CASCADE)





