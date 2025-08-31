from django import forms
from .models import Event,Student,Grade,Class

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['action', 'recorded_by']

class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['student_id', 'name', 'gender', 'grade', 'class_name', 'dorm_number', 'bed_number', 'flag']