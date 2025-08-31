from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Action, Event,Quantify
from .forms import EventForm,StudentForm,QuantifyForm,QuantifyFilterForm
from .filters import StudentFilter
from django.views.generic import ListView
import django_filters
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from .models import Student, CustomUser
from .serializers import StudentSerializer, GroupSerializer, UserSerializer
from pypinyin import lazy_pinyin

from django.contrib.auth.models import Group



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
def search_students(request):
    search_term = request.query_params.get('search', '')
    if search_term:
        # 拼音首字母匹配
        students = Student.objects.filter(name_pinyin__icontains=search_term)
    else:
        students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

def quantify_list(request):
    form = QuantifyFilterForm(request.GET)
    quantifies = Quantify.objects.all()

    if form.is_valid():
        if form.cleaned_data['student_name']:
            quantifies = quantifies.filter(student__name__icontains=form.cleaned_data['student_name'])
        if form.cleaned_data['grade']:
            quantifies = quantifies.filter(student__grade=form.cleaned_data['grade'])
        if form.cleaned_data['class_name']:
            quantifies = quantifies.filter(student__class_name=form.cleaned_data['class_name'])
        if form.cleaned_data['period']:
            quantifies = quantifies.filter(period=form.cleaned_data['period'])
        if form.cleaned_data['min_score'] is not None:
            quantifies = quantifies.filter(score__gte=form.cleaned_data['min_score'])
        if form.cleaned_data['max_score'] is not None:
            quantifies = quantifies.filter(score__lte=form.cleaned_data['max_score'])

    return render(request, 'attendance/quantify_list.html', {'quantifies': quantifies, 'form': form})

def quantify_create(request):
    if request.method == 'POST':
        form = QuantifyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quantify_list')
    else:
        form = QuantifyForm()
    return render(request, 'attendance/quantify_form.html', {'form': form})


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

@login_required
def record_event(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            Event = form.save(commit=False)
            Event.student = student
            Event.teacher=request.user
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


