from django.contrib import admin
from .models import Property, PropertyImage, Location, Amenity

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'title', 'create_date', 'update_date')
    inlines = [PropertyImageInline]
    filter_horizontal = ('locations', 'amenities')

admin.site.register(Location)
admin.site.register(Amenity)