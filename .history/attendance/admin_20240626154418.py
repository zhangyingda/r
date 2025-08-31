from django.contrib import admin
from .models import Student, Event,Period

class PeriodAdmin(admin.ModelAdmin):
    fields=["name"]

class StatusAdmin(admin.ModelAdmin):
    fields=["name"]

class StudentAdmin(admin.ModelAdmin):
    fields=["student_id","name","gender","grade","class_name","dorm_number","bed_number"]
    list_display=["student_id","name","gender","grade","class_name","dorm_number","bed_number"]
    list_filter=["gender","grade","class_name","dorm_number","bed_number"]

class EventAdmin(admin.ModelAdmin):
    fields=["timestamp","period","status","student","recorded_by"]

admin.site.register(Period,PeriodAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Event,EventAdmin)