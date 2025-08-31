from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Event
from .forms import EventForm

def student_list(request):
    students = Student.objects.all()
    return render(request, 'attendance/student_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    events = Event.objects.filter(student=student)
    return render(request, 'attendance/student_detail.html', {'student': student, 'events': events})

def record_event(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.student = student
            event.save()
            return redirect('student_detail', student_id=student.student_id)
    else:
        form = EventForm()
    return render(request, 'attendance/record_event.html', {'form': form, 'student': student})