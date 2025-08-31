import graphene
import graphql_jwt
from attendance import models, types,queries
from django.utils import timezone
from graphql_jwt.decorators import login_required
from datetime import date

# Mutation sends data to the database
class CreateUser(graphene.Mutation):
    user=graphene.Field(types.UserType) # 见 types.py

    class Arguments:
        username=graphene.String(required=True)
        password=graphene.String(required=True)
        email=graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user=models.CustomUser(username=username,email=email)
        user.set_password(password) # Make sure the password is encrypted
        user.save()

        return CreateUser(user=user)

class CreateAttendance(graphene.Mutation):
    class Arguments:
        input = queries.AttendanceInput(required=True)

    event = graphene.Field(types.EventType)

    @login_required
    def mutate(self, info, input):
        user = info.context.user
        if not user.is_teacher and not user.is_dorm_manager:
            raise Exception("Only teachers or dorm managers can create attendance records")
        try:
            student = models.Student.objects.get(student_id=input.student_id)
            period = models.Period.objects.get(id=input.period_id)
            today = date.today()
            # 检查是否已有批准的请假记录
            has_leave = models.LeaveRequest.objects.filter(
                student=student,
                status='approved',
                start_date__lte=today,
                end_date__gte=today
            ).exists()
            action_name = '请假' if has_leave else '逃课'
            action = models.Action.objects.get(name=action_name)
            event = models.Event(
                student=student,
                period=period,
                action=action,
                teacher=user,
                reason=input.reason
            )
            event.save(teacher=user)
            return CreateAttendance(event=event)
        except (models.Student.DoesNotExist, models.Period.DoesNotExist, models.Action.DoesNotExist):
            raise Exception("Student, period, or action not found")

class CreateStudent(graphene.Mutation):
    class Arguments:
        input = queries.StudentInput(required=True)

    student = graphene.Field(types.StudentType)

    @login_required
    def mutate(self, info, input):
        if not info.context.user.is_teacher:
            raise Exception("Only teachers can create students")
        try:
            student = models.Student(
                student_id=input.student_id,
                name=input.name,
                name_pinyin=input.name_pinyin,
                gender=input.gender,
                grade_id=input.grade_id,
                class_name_id=input.class_name_id,
                dorm_number_id=input.dorm_number_id,
                bed_number_id=input.bed_number_id,
                flag_id=input.flag_id,
                total_score=input.total_score or 0
            )
            student.save()
            return CreateStudent(student=student)
        except Exception as e:
            raise Exception(f"Error creating student: {str(e)}")

class DeleteStudent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    @login_required
    def mutate(self, info, id):
        if not info.context.user.is_teacher:
            raise Exception("Only teachers can delete students")
        try:
            student = models.Student.objects.get(id=id)
            student.delete()
            return DeleteStudent(success=True)
        except models.Student.DoesNotExist:
            return DeleteStudent(success=False)

class CreateEvent(graphene.Mutation):
    class Arguments:
        period_id = graphene.ID(required=True)
        action_id = graphene.ID(required=True)
        student_id = graphene.ID(required=True)

    event = graphene.Field(types.EventType)

    def mutate(self, info, period_id, action_id, student_id):
        period = models.Period.objects.get(pk=period_id)
        action = models.Action.objects.get(pk=action_id)
        student = models.Student.objects.get(pk=student_id)
        event = models.Event(period=period, action=action, student=student)
        event.save()
        return CreateEvent(event=event)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        period_id = graphene.ID(required=True)
        action_id = graphene.ID(required=True)
        student_id = graphene.ID(required=True)

    post = graphene.Field(types.EventType)

    def mutate(self, info, id, period_id, action_id, student_id):
        try:
            event = models.Event.objects.get(pk=id)
        except models.Event.DoesNotExist:
            raise Exception('Event does not exist')

        if action_id is not None:
            event.action = models.Action.objects.get(pk=action_id)

        if student_id is not None:
            event.student = models.Student.objects.get(pk=student_id)

        event.save()
        return UpdateEvent(event=event)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            event = models.Event.objects.get(pk=id)
        except models.Event.DoesNotExist:
            raise Exception('Event does not exist')

        event.delete()
        return DeleteEvent(success=True)
    
class CreateLeaveRequest(graphene.Mutation):
    class Arguments:
        student_id = graphene.Int(required=True)
        reason = graphene.String(required=True)
        start_date = graphene.Date(required=True)
        end_date = graphene.Date(required=True)

    leave_request = graphene.Field(types.LeaveRequestType)

    def mutate(self, info, student_id, reason, start_date, end_date):
        student = models.Student.objects.get(id=student_id)
        leave = models.LeaveRequest(student=student, reason=reason, start_date=start_date, end_date=end_date)
        leave.save()
        return CreateLeaveRequest(leave_request=leave)

class ApproveLeaveRequest(graphene.Mutation):
    class Arguments:
        leave_id = graphene.Int(required=True)
        approve = graphene.Boolean(required=True)  # True 为批准，False 为拒绝

    leave_request = graphene.Field(types.LeaveRequestType)

    def mutate(self, info, leave_id, approve):
        leave = models.LeaveRequest.objects.get(id=leave_id)
        if approve:
            leave.status = 'approved'
        else:
            leave.status = 'rejected'
        leave.approved_at = timezone.now()
        leave.save()
        return ApproveLeaveRequest(leave_request=leave)
    
class UpdateLeaveRequest(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = queries.LeaveRequestInput(required=True)

    leave_request = graphene.Field(models.LeaveRequestType)

    @login_required
    def mutate(self, info, id, input):
        if not info.context.user.is_teacher:
            raise Exception("Only teachers can update leave requests")
        try:
            leave_request = models.LeaveRequest.objects.get(id=id)
            student = models.Student.objects.get(student_id=input.student_id)
            leave_request.student = student
            leave_request.reason = input.reason
            leave_request.start_date = input.start_date
            leave_request.end_date = input.end_date
            leave_request.status = input.status or leave_request.status
            leave_request.approver = info.context.user if input.status in ['approved', 'rejected'] else leave_request.approver
            leave_request.approved_at = timezone.now() if input.status in ['approved', 'rejected'] else leave_request.approved_at
            leave_request.save()
            if leave_request.status == 'approved':
                flag = models.Flag.objects.get(name='请假')
                student.flag = flag
                action = models.Action.objects.get(name='请假')
                period = models.Period.objects.first()
                models.Event.objects.create(
                    student=student,
                    period=period,
                    action=action,
                    teacher=info.context.user,
                    reason=input.reason
                )
            elif leave_request.status == 'rejected':
                flag = models.Flag.objects.get(name='正常')
                student.flag = flag
            student.save()
            return UpdateLeaveRequest(leave_request=leave_request)
        except (models.Student.DoesNotExist, models.LeaveRequest.DoesNotExist, models.Flag.DoesNotExist, models.Action.DoesNotExist):
            raise Exception("Student, leave request, flag, or action not found")

# Ccustomize the behaviour of ObtainJSONWebToken
class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user=graphene.Field(types.UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)

class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token=graphql_jwt.Verify.Field()
    refresh_token=graphql_jwt.Refresh.Field()
    
    create_student=CreateStudent.Field()
    delete_student=DeleteStudent.Field()
    
    create_user = CreateUser.Field()
    
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()
    
    create_leave_request = CreateLeaveRequest.Field()
    update_leave_request=UpdateLeaveRequest.Field()
    approve_leave_request = ApproveLeaveRequest.Field()
    
    create_attendance=CreateAttendance.Field()
