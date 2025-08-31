from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Action
from .forms import ActionForm

def student_list(request):
    students = Student.objects.all()
    return render(request, 'attendance/student_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    Actions = Action.objects.filter(student=student)
    return render(request, 'attendance/student_detail.html', {'student': student, 'Actions': Actions})

def record_Action(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            Action = form.save(commit=False)
            Action.student = student
            Action.save()
            return redirect('student_detail', student_id=student.student_id)
    else:
        form = ActionForm()
    return render(request, 'attendance/record_Action.html', {'form': form, 'student': student})