import django_filters
from .models import Student

class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'student_id': ['exact', 'icontains'],
            'name': ['exact', 'icontains'],
            'gender': ['exact'],
            'grade': ['exact'],
            'class_name': ['exact'],
            'dorm_number': ['exact'],
            'bed_number': ['exact'],
            'flag': ['exact'],
        }