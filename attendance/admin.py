from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.utils.html import format_html


class QuantifyAdmin(admin.ModelAdmin):
    fields=["student","period","reason","score"]
    list_display = ["timestamp","get_student_grade","get_student_class","student", "period", "reason", "score"]
    list_filter = ["timestamp", "score","student__grade","student__class_name"]
    search_fields = ["student", "period", "reason", "score"]

    def get_student_grade(self, obj):
        return obj.student.grade.name

    def get_student_class(self, obj):
        return obj.student.class_name.name

    get_student_grade.short_description = 'Grade'
    get_student_class.short_description = 'Class'

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

class StudentAdmin(admin.ModelAdmin):
    fields=["student_id","name","gender","grade","class_name","dorm_number","bed_number","flag"]
    list_display=["student_id","name","gender","grade","class_name","dorm_number","bed_number","flag"]
    list_filter=["flag","gender","grade","class_name","dorm_number","bed_number"]
    search_fields = ["name"]

class EventAdmin(admin.ModelAdmin):
    fields=["student","period","action","teacher"]
    readonly_fields=["teacher"]
    list_display = ["custom_date","student", "period", "action","teacher"]
    list_filter = ["timestamp","period", "action","teacher"]

    def custom_date(self, obj):
        return format_html('<span>{}</span>',
                           obj.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        )
    custom_date.short_description = "时间"


class CustomUserAdmin(UserAdmin):
    # 自定义字段
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('avatar','is_teacher', 'phone_number', 'bio','location','website')}),
    )
    # 这里的第一个字段会带有编辑链接
    list_display = ["username", "avatar","email", "first_name", "last_name", "is_teacher", "phone_number", "bio", "location", "website"]
    search_fields = ["username", "email", "first_name", "last_name", "is_teacher", "phone_number", "bio","location"]

    # 表单，自定义的字段要在 admin 界面中编辑，要定义表单
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # 在这里对表单进行自定义
        return form

admin.site.register(Site)
admin.site.register(Period,PeriodAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Action,ActionAdmin)
admin.site.register(Flag,FlagAdmin)
admin.site.register(Grade,GradeAdmin)
admin.site.register(Class,ClassAdmin)
admin.site.register(Dorm,DormAdmin)
admin.site.register(Bed,BedAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Quantify, QuantifyAdmin)