from django.contrib import admin

from .models import Behavior, LogEntry

# Register your models here.
@admin.register(Behavior)
class BehaviorAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['date', 'behavior', 'quality']