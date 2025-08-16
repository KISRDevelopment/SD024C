

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

STATUS_CHOICES = (
    ('ONGOING', 'Ongoing'),
    ('DONE', 'Done')
)


class Examiner(models.Model):
    STAGE_CHOICES = (
    ('PRIMARY','Primary School'),
    ('SECONDARY','Secondary School'),
    ('BOTH','Primary/Secondary')
)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_id')
    name = models.CharField(max_length=60)
    speciality = models.CharField(max_length=60)
    organization = models.CharField(max_length=60)
    stage = models.CharField(max_length=20,
                  choices=STAGE_CHOICES,
                  default="PRIMARY")

    def __str__(self):
        return f"{self.id}: {self.name}"
    
class Student(models.Model):
    examiner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='examiner_id')
    studentName = models.CharField(max_length=60)
    gender = models.CharField(max_length=60)
    schoolName = models.CharField(max_length=60)
    grade = models.CharField(max_length=60)
    civilID = models.IntegerField()
    eduDistrict = models.CharField(max_length=60)
    nationality = models.CharField(max_length=60)
    examDate = models.DateField(max_length=60)
    birthDate = models.DateField(max_length=60)
    age = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.studentName}"
    

#primary test modal data structure    
class PrimaryTest1(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_correct = models.PositiveIntegerField()
    time_seconds = models.FloatField()
    fluency_score = models.FloatField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
    

class PrimaryTest2(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    scores = models.JSONField()
    total_score = models.PositiveIntegerField()
    time_seconds = models.FloatField()
    fluency_score = models.FloatField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

class PrimaryTest3(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    raw_scores = models.JSONField()
    total_correct = models.PositiveIntegerField()
    durations = models.JSONField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    total_time_secs = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

class PrimaryTest4(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    raw_scores = models.JSONField()
    total_correct = models.PositiveIntegerField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
    
class PrimaryTest5(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    raw_scores = models.JSONField()
    total_correct = models.PositiveIntegerField()
    durations = models.JSONField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    total_time_secs = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

#secondary test modal data structure    
class SecondaryTest1(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_correct = models.PositiveIntegerField()
    time_seconds = models.FloatField()
    fluency_score = models.FloatField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
    
class SecondaryTest2(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    raw_scores = models.JSONField()
    total_correct = models.PositiveIntegerField()
    durations = models.JSONField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    total_time_secs = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
    
    
#add Secondary test 3
class SecondaryTest3(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    raw_scores = models.JSONField()
    total_correct = models.PositiveIntegerField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

#Secondary Test 4
class SecondaryTest4(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    raw_scores = models.JSONField()
    total_correct = models.PositiveIntegerField()
    durations = models.JSONField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    total_time_secs = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"


