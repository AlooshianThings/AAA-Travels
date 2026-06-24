import random
from django.shortcuts import render, redirect
from .models import *

generated_numbers = set()

def index(request):
    return render(request, 'index.html')

def generate_unique_four_digit():
    while True:
        four_digit_number = random.randint(1000, 9999)
        if four_digit_number not in generated_numbers:
            generated_numbers.add(four_digit_number)
            return four_digit_number

def passenger(request):
    msg = {}
    unique_number = generate_unique_four_digit()
    if request.method == "POST":
        passenger1_name = request.POST.get("passenger1Name")
        passenger1_age = request.POST.get("passenger1Age")
        passenger1_email = request.POST.get("passenger1Email")
        passenger2_name = request.POST.get("passenger2Name")
        passenger2_age = request.POST.get("passenger2Age")
        passenger2_email = request.POST.get("passenger2Email")

        if passenger1_name and passenger1_age and passenger1_email:
            rec = travelers(
                booking_id=unique_number,
                passenger_1_name=passenger1_name,
                passenger_1_age=passenger1_age,
                passenger_1_email=passenger1_email,
                passenger_2_name=passenger2_name,
                passenger_2_age=passenger2_age,
                passenger_2_email=passenger2_email,
                card_number = 000000
            )
            rec.save()
            return redirect("/payment/?unique_number=" + str(unique_number))
        else:
            msg["msg"] = "Invalid details"

    return render(request, "passenger.html", {"msg": msg, "unique_number": unique_number})

def payment(request):
    msg = {}
    unique_number = request.GET.get("unique_number")
    if request.method == "POST":
        card_number = request.POST.get("cardNumber")
        expiry = request.POST.get("expiry")
        cvv = request.POST.get("cvv")
        rec = travelers.objects.get(booking_id=unique_number)
        if card_number and expiry and cvv:
            rec.card_number = card_number
            rec.save()
            return redirect("/thank_you/?unique_number=" + str(unique_number))
        else:
            msg["msg"] = "Invalid details"

    return render(request, "payment.html", {"msg": msg, "unique_number": unique_number})

def payment_confirmation(request):
    unique_number = request.GET.get("unique_number")
    if travelers.objects.get(booking_id=unique_number):
        rec = travelers.objects.get(booking_id=unique_number)
        data={"booking":rec.booking_id,
        "name":rec.passenger_1_name,
        "age":rec.passenger_1_age,
        "email":rec.passenger_1_email}
    return render(request, 'payment_confirmation.html', data)
def bus(request):
    return render(request, 'buses.html')
def cancel(request):
    return render(request, 'cancel.html')
def seat(request):
    return render(request, 'seat.html')
def train(request):
    return render(request, 'train.html')
def portfolio(request):
    return render(request, 'portfolio.html')
def privacy(request):
    return render(request, 'privacy.html')
from django.http import JsonResponse, HttpResponse


def cancel_bus(request):
    data = {}
    if 'ticketId' in request.GET:
        booking_id = request.GET.get('ticketId')
        try:
            rec = travelers.objects.get(booking_id=booking_id)
            data = {
                "booking": rec.booking_id,
                "name": rec.passenger_1_name,
                "age": rec.passenger_1_age,
                "email": rec.passenger_1_email,
                "price": 2000,
                "status": "Bus ticket canceled successfully!"
            }
            rec.delete()
        except travelers.DoesNotExist:
            data = {'msg': 'No such record found!'}

    return render(request, 'cancel_bus.html', data)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import *
from django.db.models import Q
from django.db import connection

def packages(request):
    packages = package.objects.all()
    context = {'packages': packages}
    if request.method == 'POST':
        selected_package = package.objects.get(id=request.POST.get('package'))
        context = {'selected_package': selected_package}
        return render(request, 'selected_package.html', context)
    return render(request, 'packages.html', context)

def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel_list.html', {'hotels': hotels})


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.rooms.filter(is_available=True)
    return render(request, 'hotel_detail.html', {'hotel': hotel, 'rooms': rooms})

def book_hotel(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        check_in_date = request.POST['check_in_date']
        check_out_date = request.POST['check_out_date']
        no_of_guests = request.POST['no_of_guests']
        booking = Booking.objects.create( room=room, check_in_date=check_in_date, check_out_date=check_out_date, no_of_guests=no_of_guests)
        booking.calculate_price()
        messages.success(request, f'Booking successful. Your booking ID is {booking.id}')
        return redirect('booking_confirmation', booking_id=booking.id)
    return render(request, 'book_hotel.html', {'room': room})

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    total_price = booking.price
    hotel_name = booking.room.hotel.name
    booking_id = booking.id
    context = {
        'booking': booking,
        'total_price': total_price,
        'hotel_name': hotel_name,
        'booking_id': booking_id
    }
    return render(request, 'booking_confirmation.html', context)


# ------
from .models import login,Flights,Airports,Bookings
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect


def register(request):
    msg={}
    if request.GET.get("username") and request.GET.get("name") and request.GET.get("email") and request.GET.get("phone")and request.GET.get("password") and request.GET.get("cpass"):
        rec = login(uname=request.GET.get("username"), name=request.GET.get("name"),phone=request.GET.get("phone"),email=request.GET.get("email"),password=request.GET.get("password"))
        rec.save()
        msg = {"msg": "Record Inserted..."}
    return render(request,"register.html",msg)


def login_user(request):
    msg = {" "}
    if request.POST.get("uname") and request.POST.get("password"):
        uname = request.POST.get("uname")
        password = request.POST.get("password")
        if login.objects.filter(uname=uname, password=password).exists():
            msg= "success"
        else:
            msg = "wrong"
    else:
        msg = "Enter ID"
    
    return render(request, "login.html", {"msg": msg})
    


def search_flights(request):
    results = []
   
    if request.POST.get("from_start") and request.POST.get("to_end"):
        dcity = request.POST.get("from_start")
        acity = request.POST.get("to_end")
        dairport = Airports.objects.get(city=dcity).airport_name
        aairport = Airports.objects.get(city=acity).airport_name
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT f.flight_id, d.airport_name AS departure_airport_name, d.city AS departure_city, f.departure_time,"
                "a.airport_name AS arrival_airport_name, a.city AS arrival_city,f.arrival_time, "
                " f.duration_minutes, f.fare, "
                "airline.airline_name "
                "FROM Flights f "
                "JOIN Airports d ON f.departure_airport_name = d.airport_name "
                "JOIN Airports a ON f.arrival_airport_name = a.airport_name "
                "JOIN Airlines airline ON f.airline_id = airline.airline_id "
                "WHERE d.airport_name = %s AND a.airport_name = %s",
                [dairport, aairport]
            )
            results = cursor.fetchall()
            
    return render(request, 'search.html', {'results': results})

def book_flight(request):
    msg={}
    booking_id = request.POST.get('booked_id')
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT f.flight_id, d.airport_name AS departure_airport_name, d.city AS departure_city, f.departure_time,"
            "a.airport_name AS arrival_airport_name, a.city AS arrival_city,f.arrival_time, "
            " f.duration_minutes, f.fare, "
            "airline.airline_name "
            "FROM Flights f "
            "JOIN Airports d ON f.departure_airport_name = d.airport_name "
            "JOIN Airports a ON f.arrival_airport_name = a.airport_name "
            "JOIN Airlines airline ON f.airline_id = airline.airline_id "
            "WHERE f.flight_id = %s",
            [booking_id]
        )
        msg= cursor.fetchall()

    print(booking_id)  
    return render(request, 'bookings.html', {'msg':msg})


def submit_details(request):
    msg1={}
    if request.method == 'POST':
    # Retrieve form data from POST request
        flight_id = request.POST.get('flight_id')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment')
        
        if not all([flight_id, fullname, email, phone, payment_method]):
            return render(request, 'bookings.html', {'error_message': 'All fields are required'})
        
        
        # Create a Bookings instance and assign the flight_instance
        booking = Bookings.objects.create(
            flight_id=flight_id,
            fullname=fullname,
            email=email,
            phone=phone,
            payment_method=payment_method
        )

        print(booking)
        return render(request,'thanku.html')
    return render(request, 'bookings.html', {'msg1':msg1})
    
    
   
    
    