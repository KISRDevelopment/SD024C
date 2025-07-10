

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
    

class finalReportPrimary(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_ids')
    examiner = models.ForeignKey(Examiner, on_delete=models.CASCADE, related_name='examiner_ids')
    test_1_skill_sound = models.BooleanField(null=True)
    test_2_skill_sound = models.BooleanField(null=True)
    test_3_skill_speed = models.BooleanField(null=True)
    test_4_skill_speed = models.BooleanField(null=True)
    test_5_skill_memory = models.BooleanField(null=True)
    notes = models.TextField()
    strength = models.TextField()
    weakness = models.TextField()
    result = models.TextField()
    suggestion = models.TextField()

    def __str__(self):
        return f"{self.student}"

class finalReportSecondary(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_idS')
    examiner = models.ForeignKey(Examiner, on_delete=models.CASCADE, related_name='examiner_idS')
    notes = models.TextField()
    strength = models.TextField()
    weakness = models.TextField()
    results = models.TextField()
    suggestion = models.TextField()

    def __str__(self):
        return f"{self.student}"
    
#Test Parts such as part A part B etc (students can take as many tests part and it will be saved)
#Primary - test 1
class RpdNamingObj_Score(models.Model):
    student_id = models.ForeignKey(Student, on_delete = models.CASCADE)
    startT_A = models.DateTimeField(null=True)
    endT_A = models.DateTimeField(null=True)
    wrongAns_A = models.IntegerField(null=True)
    reason_A =models.CharField(max_length=60,null=True)
    startT_B = models.DateTimeField(null=True)
    endT_B = models.DateTimeField(null=True)
    wrongAns_B = models.IntegerField(null=True)
    reason_B =models.CharField(max_length=60,null=True)

    def __str__(self):
        return f"{self.id}: {self.student_id} "
    
#Primary - test 3
class RpdNamingLtrs_Score(models.Model):
    student_id = models.ForeignKey(Student, on_delete = models.CASCADE)
    startT_A = models.DateTimeField(null=True)
    endT_A = models.DateTimeField(null=True)
    wrongAns_A = models.IntegerField(null=True)
    reason_A =models.CharField(max_length=60,null=True)
    startT_B = models.DateTimeField(null=True)
    endT_B = models.DateTimeField(null=True)
    wrongAns_B = models.IntegerField(null=True)
    reason_B =models.CharField(max_length=60,null=True)

    def __str__(self):
        return f"{self.id}: {self.student_id} "

#Primary - test 2
class PhonemeSyllableDel(models.Model):
    student_id = models.ForeignKey(Student, on_delete = models.CASCADE)
    correctAns = models.IntegerField(null=True)
    reason = models.CharField(max_length=60,null=True)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.id}: {self.test_id.student_id} "

#Primary - test 4
class NonWordRepetition(models.Model):
    student_id = models.ForeignKey(Student, on_delete = models.CASCADE)
    correctAns = models.IntegerField(null=True)
    reason = models.CharField(max_length=60,null=True)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.id}: {self.test_id.student_id} "
    
class PrimaryTest1(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_correct = models.PositiveIntegerField()
    time_seconds = models.FloatField()
    fluency_score = models.FloatField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

#Primary - test 5
class NonWordReadingAcc(models.Model):
    student_id = models.ForeignKey(Student, on_delete = models.CASCADE)
    correctAns = models.IntegerField(null=True)
    reason = models.CharField(max_length=60,null=True)
    date= models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.id}: {self.test_id.student_id} "

#Middle School - test 1
class PhonemeSyllableDelSec(models.Model):
    student_id = models.ForeignKey(Student, on_delete = models.CASCADE)
    correctAns = models.IntegerField(null=True)
    reason = models.CharField(max_length=60,null=True)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.id}: {self.test_id.student_id} "

#Middle School - test 2
class RpdNamingObjSec(models.Model):
    student_id = models.ForeignKey(Student, on_delete = models.CASCADE)
    startT_A = models.DateTimeField(null=True)
    endT_A = models.DateTimeField(null=True)
    wrongAns_A = models.IntegerField(null=True)
    reason_A =models.CharField(max_length=60,null=True)
    startT_B = models.DateTimeField(null=True)
    endT_B = models.DateTimeField(null=True)
    wrongAns_B = models.IntegerField(null=True)
    reason_B =models.CharField(max_length=60,null=True)

    def __str__(self):
        return f"{self.id}: {self.student_id} "

#Middle school - test 3
class NonWordRepetitionSec(models.Model):
    student_id = models.ForeignKey(Student, on_delete = models.CASCADE)
    correctAns = models.IntegerField(null=True)
    reason = models.CharField(max_length=60,null=True)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.id}: {self.test_id.student_id} "
    
#Middle school - test 5
class NonWordReadingAccSec(models.Model):
    student_id = models.ForeignKey(Student, on_delete = models.CASCADE)
    correctAns = models.IntegerField(null=True)
    reason = models.CharField(max_length=60,null=True)
    date= models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.id}: {self.test_id.student_id} "