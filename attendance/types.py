import graphene
from graphene_django import DjangoObjectType
from attendance import models

class SiteType(DjangoObjectType):
    class Meta:
        model = models.Site

class UserType(DjangoObjectType):
    class Meta:
        model=models.CustomUser
        fields=('id','username','is_teacher','is_dorm_manager')

class PeriodType(DjangoObjectType):
    class Meta:
        model = models.Period

class GradeType(DjangoObjectType):
    class Meta:
        model=models.Grade
        fields=('id','name')

class ClassType(DjangoObjectType):
    class Meta:
        model=models.Class
        fields=('id','name')
        
class DormType(DjangoObjectType):
    class Meta:
        model=models.Dorm
        fields=('id','name')
        
class ActionType(DjangoObjectType):
    class Meta:
        model=models.Action
        fields=('id','name')
        
class PeriodType(DjangoObjectType):
    class Meta:
        model=models.Period
        fields=('id','name')
        
class EventType(DjangoObjectType):
    class Meta:
        model=models.Event
        fields = ('id', 'timestamp', 'period', 'action', 'student', 'teacher', 'reason')

class StudentType(DjangoObjectType):
    class Meta:
        model=models.Student
        fields = ('id', 'student_id', 'name', 'name_pinyin', 'gender', 'grade', 'class_name', 'dorm_number', 'bed_number', 'flag', 'total_score')
        
class LeaveRequestType(DjangoObjectType):
    class Meta:
        model = models.LeaveRequest
        fields=('id', 'student', 'reason', 'start_date', 'end_date', 'status', 'approver', 'approved_at')

class QuantifyType(DjangoObjectType):
    class Meta:
        model=models.Quantify
        fields = '__all__'