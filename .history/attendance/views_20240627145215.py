from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Action, Event
from .forms import EventForm,StudentForm
from .filters import StudentFilter
from django.views.generic import ListView
import django_filters

class StudentListView(django_filters.FilterSet, ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'student_list.html'
    filterset_class = StudentFilter

def student_list(request):
    students = Student.objects.all()
    return render(request, 'attendance/student_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    Events = Action.objects.filter(student=student)
    return render(request, 'attendance/student_detail.html', {'student': student, 'Events': Events})

def record_event(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            Event = form.save(commit=False)
            Event.student = student
            Event.save()
            return redirect('student_detail', student_id=student.student_id)
    else:
        form = EventForm()
    return render(request, 'attendance/record_event.html', {'form': form, 'student': student})

def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})