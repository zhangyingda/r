from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Action, Event
from .forms import ActionForm

def student_list(request):
    students = Student.objects.all()
    return render(request, 'attendance/student_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    Events = Action.objects.filter(student=student)
    return render(request, 'attendance/student_detail.html', {'student': student, 'Events': Events})

def record_Event(request, student_id):
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