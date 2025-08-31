import graphene
from attendance import models
from attendance import types
from graphql_jwt.decorators import login_required
from datetime import date
from django.utils import timezone

# 输入类型
class StudentInput(graphene.InputObjectType):
    student_id = graphene.String(required=True)
    name = graphene.String(required=True)
    name_pinyin = graphene.String(required=True)
    gender = graphene.String(required=True)
    grade_id = graphene.Int(required=True)
    class_name_id = graphene.Int(required=True)
    dorm_number_id = graphene.Int(required=True)
    bed_number_id = graphene.Int(required=True)
    flag_id = graphene.Int()
    total_score = graphene.Int()

class LeaveRequestInput(graphene.InputObjectType):
    student_id = graphene.String(required=True)
    reason = graphene.String(required=True)
    start_date = graphene.Date(required=True)
    end_date = graphene.Date(required=True)
    status = graphene.String()

class AttendanceInput(graphene.InputObjectType):
    student_id = graphene.String(required=True)
    period_id = graphene.Int(required=True)
    reason = graphene.String(required=True)
    
    
# 查询
class Query(graphene.ObjectType):
    all_students = graphene.List(types.StudentType)
    normal_students = graphene.List(types.StudentType, grade_id=graphene.Int(), class_name_id=graphene.Int(), dorm_number_id=graphene.Int(), gender=graphene.String())
    on_leave_students = graphene.List(types.StudentType, grade_id=graphene.Int(), class_name_id=graphene.Int(), dorm_number_id=graphene.Int(), gender=graphene.String())
    all_leave_requests = graphene.List(types.LeaveRequestType)
    leave_requests_by_student = graphene.List(types.LeaveRequestType, student_id=graphene.String(required=True))
    daily_attendance = graphene.List(types.EventType, date=graphene.Date(), grade_id=graphene.Int(), class_name_id=graphene.Int(), dorm_number_id=graphene.Int(), gender=graphene.String())
    all_periods = graphene.List(types.PeriodType)

    @login_required
    def resolve_all_students(self, info):
        if not info.context.user.is_teacher and not info.context.user.is_dorm_manager:
            raise Exception("Only teachers or dorm managers can view students")
        return models.Student.objects.all()

    @login_required
    def resolve_normal_students(self, info, grade_id=None, class_name_id=None, dorm_number_id=None, gender=None):
        if not info.context.user.is_teacher and not info.context.user.is_dorm_manager:
            raise Exception("Only teachers or dorm managers can view students")
        queryset = models.Student.objects.filter(flag__name='正常')
        if grade_id:
            queryset = queryset.filter(grade_id=grade_id)
        if class_name_id:
            queryset = queryset.filter(class_name_id=class_name_id)
        if dorm_number_id:
            queryset = queryset.filter(dorm_number_id=dorm_number_id)
        if gender:
            queryset = queryset.filter(gender=gender)
        return queryset

    @login_required
    def resolve_on_leave_students(self, info, grade_id=None, class_name_id=None, dorm_number_id=None, gender=None):
        if not info.context.user.is_teacher and not info.context.user.is_dorm_manager:
            raise Exception("Only teachers or dorm managers can view students")
        today = date.today()
        queryset = models.Student.objects.filter(
            leave_requests__status='approved',
            leave_requests__start_date__lte=today,
            leave_requests__end_date__gte=today
        ).distinct()
        if grade_id:
            queryset = queryset.filter(grade_id=grade_id)
        if class_name_id:
            queryset = queryset.filter(class_name_id=class_name_id)
        if dorm_number_id:
            queryset = queryset.filter(dorm_number_id=dorm_number_id)
        if gender:
            queryset = queryset.filter(gender=gender)
        return queryset

    @login_required
    def resolve_all_leave_requests(self, info):
        if not info.context.user.is_teacher and not info.context.user.is_dorm_manager:
            raise Exception("Only teachers or dorm managers can view leave requests")
        return models.LeaveRequest.objects.all()

    @login_required
    def resolve_leave_requests_by_student(self, info, student_id):
        if not info.context.user.is_teacher and not info.context.user.is_dorm_manager:
            raise Exception("Only teachers or dorm managers can view leave requests")
        try:
            student = models.Student.objects.get(student_id=student_id)
            return student.leave_requests.all()
        except models.Student.DoesNotExist:
            raise Exception("Student not found")

    @login_required
    def resolve_daily_attendance(self, info, date=None, grade_id=None, class_name_id=None, dorm_number_id=None, gender=None):
        if not info.context.user.is_teacher and not info.context.user.is_dorm_manager:
            raise Exception("Only teachers or dorm managers can view attendance")
        target_date = date or timezone.now().date()
        start_of_day = timezone.make_aware(timezone.datetime.combine(target_date, timezone.datetime.min.time()))
        end_of_day = timezone.make_aware(timezone.datetime.combine(target_date, timezone.datetime.max.time()))
        queryset = models.Event.objects.filter(timestamp__range=(start_of_day, end_of_day), action__name__in=['请假', '逃课'])
        if grade_id:
            queryset = queryset.filter(student__grade_id=grade_id)
        if class_name_id:
            queryset = queryset.filter(student__class_name_id=class_name_id)
        if dorm_number_id:
            queryset = queryset.filter(student__dorm_number_id=dorm_number_id)
        if gender:
            queryset = queryset.filter(student__gender=gender)
        return queryset

    @login_required
    def resolve_all_periods(self, info):
        return models.Period.objects.all()
