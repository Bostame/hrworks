from django.contrib import admin

# Register your models here.
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_time', 'end_time', 'created_by', 'location')
    search_fields = ('title', 'description', 'event_type', 'location')
    list_filter = ('event_type', 'start_time')

