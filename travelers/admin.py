from django.contrib import admin
from .models import *
class statesAdmin(admin.ModelAdmin):
    list_display=('state')
admin.site.register(states)
class the_cityAdmin(admin.ModelAdmin):
    list_display=('city','state')
admin.site.register(the_city,the_cityAdmin) 
class packageAdmin(admin.ModelAdmin):
    list_display=('name','city','price','description','image','day1_name','day1_description', 'image1','day2_name','day2_description', 'image2','day3_name','day3_description', 'image3','day4_name','day4_description', 'image4','day5_name','day5_description', 'image5')
admin.site.register(package,packageAdmin)
class HotelAdmin(admin.ModelAdmin):
    list_display=('name','city','price','description','image1','image2','image3','image4')
admin.site.register(Hotel,HotelAdmin)
class RoomAdmin(admin.ModelAdmin):
    list_display=('hotel','room_number','capacity','price','is_available')
admin.site.register(Room,RoomAdmin)
