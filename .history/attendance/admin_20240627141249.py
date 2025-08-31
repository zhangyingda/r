from django.contrib import admin
from .models import Student, Event,Period,Action,Flag,Grade,Class,Dorm,Bed
from massadmin.massadmin import MassAdmin

class DormAdmin(admin.ModelAdmin):
    fields=["name"]

class BedAdmin(admin.ModelAdmin):
    fields=["name"]

class GradeAdmin(admin.ModelAdmin):
    fields=["name"]

class ClassAdmin(admin.ModelAdmin):
    fields=["name"]

class FlagAdmin(admin.ModelAdmin):
    fields=["name"]

class FlagAdmin(admin.ModelAdmin):
    fields=["name"]

class PeriodAdmin(admin.ModelAdmin):
    fields=["name"]

class ActionAdmin(admin.ModelAdmin):
    fields=["name"]

class StudentAdmin(MassAdmin):
    fields=["student_id","name","gender","grade","class_name","dorm_number","bed_number"]
    list_display=["student_id","name","gender","grade","class_name","dorm_number","bed_number"]
    list_filter=["gender","grade","class_name","dorm_number","bed_number"]

class EventAdmin(admin.ModelAdmin):
    fields=["period","action","student","recorded_by"]

admin.site.register(Period,PeriodAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Action,ActionAdmin)
admin.site.register(Flag,FlagAdmin)
admin.site.register(Grade,GradeAdmin)
admin.site.register(Class,ClassAdmin)
admin.site.register(Dorm,DormAdmin)
admin.site.register(Bed,BedAdmin)