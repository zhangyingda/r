from django.db import models

class Period(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Flag(models.Model):
    name = models.CharField(max_length=50, unique=True,default="正常")

    def __str__(self):
        return self.name
    
class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)
    class_name = models.CharField(max_length=50)
    dorm_number = models.CharField(max_length=10)
    bed_number = models.CharField(max_length=10)
    flag = models.ForeignKey(Flag, on_delete=models.CASCADE,default="正常")

    def __str__(self):
        return self.name

class Event(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    recorded_by = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.student.name} - {self.status}"