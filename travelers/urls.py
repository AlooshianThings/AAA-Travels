"""
URL configuration for travelers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('passengerdetails/', views.passenger),
    path('payment/', views.payment),
    path('', views.index),
    path('thank_you/', views.payment_confirmation),
    path('bus/', views.bus),
    path('cancel/', views.cancel),
    path('passenger/', views.passenger),
    path('seat/', views.seat),
    path('train/', views.train),
    path('portfolio/', views.portfolio),
    path('privacy/', views.privacy),
    path('cancel_bus/',views.cancel_bus),
    path('packages/', views.packages),
    path('hotel_list/', views.hotel_list, name='hotel_list'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('book/<int:room_id>/', views.book_hotel, name='book_hotel'),
    path('booking/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),

    path("registers/",views.register),
    path("login/",views.login_user),
    path("f/",views.search_flights),


    path('book_flight/', views.book_flight, name='book_flight'),
    path('submit_details/',views.submit_details),
    # path('thanku/',views.thanku),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


