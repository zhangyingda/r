from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('student/<str:student_id>/', views.student_detail, name='student_detail'),
    path('student/<str:student_id>/record_event/', views.record_event, name='record_event'),
]