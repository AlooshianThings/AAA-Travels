from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.safestring import mark_safe
from datetime import datetime
class travelers(models.Model):
    booking_id = models.IntegerField(primary_key=True)
    passenger_1_name = models.CharField(max_length=100)
    passenger_1_age = models.IntegerField()
    passenger_1_email = models.CharField(max_length=100)
    passenger_2_name = models.CharField(max_length=100, blank=True, null=True)
    passenger_2_age = models.IntegerField(blank=True, null=True)
    passenger_2_email = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.BigIntegerField()

    class Meta:
        db_table = "travelers"


class states(models.Model):
    state=models.CharField(max_length=100)
    def __str__(self):
        return self.state
    class Meta:
        db_table="state"
class the_city(models.Model):
    city=models.CharField(max_length=30)
    state=models.ForeignKey(states,on_delete=CASCADE)
    def __str__(self) -> str:
        return self.city
    class Meta:
        db_table="the_city" 
class package(models.Model):
    name = models.CharField(max_length=50)
    city= models.ForeignKey(the_city,on_delete=CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')
    
    day1_name = models.TextField()
    day1_description = models.TextField()
    image1 = models.ImageField(upload_to='packages/')

    day2_name = models.TextField()
    day2_description = models.TextField()
    image2 = models.ImageField(upload_to='packages/')

    day3_name = models.TextField()
    day3_description = models.TextField()
    image3 = models.ImageField(upload_to='packages/')

    day4_name = models.TextField()
    day4_description = models.TextField()
    image4 = models.ImageField(upload_to='packages/')

    day5_name = models.TextField()
    day5_description = models.TextField()
    image5 = models.ImageField(upload_to='packages/')
from django.utils import timezone

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    city= models.ForeignKey(the_city,on_delete=CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image1 = models.ImageField(upload_to='hotels/')
    image2 = models.ImageField(upload_to='hotels/')
    image3 = models.ImageField(upload_to='hotels/')
    image4 = models.ImageField(upload_to='hotels/')

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.IntegerField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'Room {self.room_number} in {self.hotel.name}'
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField(default=timezone.now)
    check_out_date = models.DateField(default=timezone.now)
    no_of_guests = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default="1000")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Booking {self.id}'

    def calculate_price(self):
        days_of_stay = ((datetime.strptime(self.check_out_date, '%Y-%m-%d')) - (datetime.strptime(self.check_in_date, '%Y-%m-%d'))).days
        price_per_day = self.room.price
        self.price = price_per_day * days_of_stay
        self.save()   
        
# -------

class login(models.Model):
    uname = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    class Meta:
        db_table = "login"
        

class Airports(models.Model):
    airport_name = models.CharField(max_length=255, primary_key=True)
    city = models.CharField(max_length=100)
    class Meta:
        db_table = "Airports"

class Airlines(models.Model):
    airline_id = models.AutoField(primary_key=True)
    airline_name = models.CharField(max_length=255)
    class Meta:
        db_table = "Airline"

class Flights(models.Model):
    flight_id = models.AutoField(primary_key=True)
    departure_airport_name = models.ForeignKey(Airports, on_delete=models.CASCADE, related_name='departures')
    arrival_airport_name = models.ForeignKey(Airports, on_delete=models.CASCADE, related_name='arrivals')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airline_id = models.ForeignKey(Airlines, on_delete=models.CASCADE)
    duration_minutes = models.IntegerField()
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = "Flights"


class Bookings(models.Model):
    booking_id = models.AutoField(primary_key=True)
    flight_id = models.IntegerField()  # Assuming you'll handle the foreign key relationship manually
    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)

    class Meta:
        db_table = "Bookings"

                                 
