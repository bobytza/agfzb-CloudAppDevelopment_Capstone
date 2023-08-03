from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel 
    extra = 2
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    model = CarModel
    #inlines = [CarModelInline]
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    model= CarMake
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)