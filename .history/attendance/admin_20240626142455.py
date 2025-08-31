from django.contrib import admin
from .models import Student, Event

class StudentAdmin(admin.ModelAdmin):
    list_display=["student_id","name","gender","grade","class_name","dorm_number","bed_number"]
    list_filter=["gender","grade","class_name","dorm_number","bed_number"]

admin.site.register(Student)
admin.site.register(Event)