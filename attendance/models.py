# attendance/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from pypinyin import lazy_pinyin

class Site(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='site/logo/')

    class Meta:
        verbose_name = 'Site'
        #verbose_name_plural = '1. Site'

    def __str__(self):
        return self.name

# 基于 AbstractUser 定制用户表
# 测试用数据 teacher1-teacher4 密码 1qaz9ol.
class CustomUser(AbstractUser):
    avatar= models.ImageField(upload_to='users/avatar/%Y/%m/%d/', default='users/avatars/default.jpg', blank=True)
    is_teacher = models.BooleanField(default=False)
    is_dorm_manager=models.BooleanField(default=False) # 宿管标志
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(max_length=500,blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'user'
        #verbose_name_plural = '2. User'

    def __str__(self):
        return self.username

# 定义男女选项
GENDER_CHOICES = [
    ('male', '男'),
    ('female', '女'),
]

# 年级
class Grade(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

# 班级
class Class(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 宿舍
class Dorm(models.Model):
    name=models.CharField(max_length=18,unique=True)
    
    def __str__(self):
        return self.name
    
# 床铺号
class Bed(models.Model):
    name=models.CharField(max_length=18,unique=True)
    
    def __str__(self):
        return self.name


# 时间段
class Period(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 行为 请假 销假 异常 复课
class Action(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 标志 正常 请假 异常
class Flag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 学生表
class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True,verbose_name="学号")
    name = models.CharField(max_length=100,verbose_name="姓名")
    name_pinyin = models.CharField(max_length=100, blank=True, verbose_name="姓名拼音")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,verbose_name="性别")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE,verbose_name="年级")
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE,verbose_name="班级")
    dorm_number = models.ForeignKey(Dorm, on_delete=models.CASCADE,verbose_name="宿舍") # dormitory 宿舍
    bed_number = models.ForeignKey(Bed, on_delete=models.CASCADE,verbose_name="床铺")
    flag = models.ForeignKey(Flag, on_delete=models.CASCADE,verbose_name="状态")
    total_score = models.IntegerField(default=0, verbose_name="总分")

    class Meta:
        verbose_name='student'
        #verbose_name_plural='3. student'

    def save(self, *args, **kwargs):
        self.name_pinyin = ''.join(lazy_pinyin(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# 量化表
class Quantify(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="时间")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, verbose_name="时段",null=True)
    reason = models.CharField(max_length=255)
    score = models.IntegerField()

    class Meta:
        verbose_name='quantify'
        #verbose_name_plural='4. quantifies'

    def __str__(self):
        return f"{self.student.name} - {self.reason} - {self.score}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.student.total_score += self.score
        self.student.save()

# 事件表
class Event(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True,verbose_name="时间")
    period = models.ForeignKey(Period, on_delete=models.CASCADE,verbose_name="时段")
    action = models.ForeignKey(Action, on_delete=models.CASCADE,verbose_name="事件")
    student = models.ForeignKey(Student, on_delete=models.CASCADE,verbose_name="学生")
    teacher=models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    reason=models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return f"{self.student.name} - {self.action}"

    def save(self, *args, **kwargs):
        teacher=kwargs.pop('teacher',None)
        if teacher:
            self.teacher=teacher
        super().save(*args, **kwargs)

        # 自动更新学生的 flag 状态
        action_to_flag_mapping = {
            '异常': '异常',  # 根据实际情况填写action 和 flag 对应关系
            '请假': '请假',
            '销假': '正常',
            '复课': '正常',
        }
        if self.action.name in action_to_flag_mapping:
            flag_name = action_to_flag_mapping[self.action.name]
            try:
                new_flag = Flag.objects.get(name=flag_name)
                self.student.flag = new_flag
                self.student.save()
            except Flag.DoesNotExist:
                pass  # 或者处理 flag 不存在的情况


class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审批'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)  # 审批人，如老师
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} 的请假 ({self.start_date} 到 {self.end_date})"