from django.contrib import admin
# from .models import related models

from .models import CarMake, CarModel
# Register your models here.
# CarModelInline class


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('car_make', 'name', 'dealer_id', 'type', 'year')
    search_fields = ('car_make', 'name', 'dealer_id', 'type', 'year')


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    inlines = [CarModelInline]


# Register models here
admin.site.register(CarMake, CarMakeAdmin)
