from django import forms
from .models import Event,Student,Grade,Class,Quantify,Period

class QuantifyForm(forms.ModelForm):
    class Meta:
        model=Quantify
        fields='__all__'

class QuantifyFilterForm(forms.Form):
    student_name = forms.CharField(required=False, label='Student Name')
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), required=False, label='Grade')
    class_name = forms.ModelChoiceField(queryset=Class.objects.all(), required=False, label='Class')
    period = forms.ModelChoiceField(queryset=Period.objects.all(), required=False, label='Period')
    min_score = forms.IntegerField(required=False, label='Min Score')
    max_score = forms.IntegerField(required=False, label='Max Score')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['action']

class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['student_id', 'name', 'gender', 'grade', 'class_name', 'dorm_number', 'bed_number', 'flag']