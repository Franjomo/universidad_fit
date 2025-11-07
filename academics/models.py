from django.db import models
from django.utils import timezone


class Program(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    area = models.ForeignKey('locations.Area', on_delete=models.CASCADE, db_column='area_code')

    class Meta:
        db_table = 'programs'

    def __str__(self):
        return self.name


class Subject(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    program = models.ForeignKey('academics.Program', on_delete=models.CASCADE, db_column='program_code')

    class Meta:
        db_table = 'subjects'

    def __str__(self):
        return self.name


class Group(models.Model):
    NRC = models.CharField(max_length=10, primary_key=True)
    number = models.IntegerField()
    semester = models.CharField(max_length=6)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, db_column='subject_code')
    professor = models.ForeignKey('accounts.Employee', on_delete=models.PROTECT, db_column='professor_id')

    class Meta:
        db_table = 'groups'

    def __str__(self):
        return f"{self.subject.name} - {self.NRC}"


class Enrollment(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, db_column='student_id')
    group = models.ForeignKey('academics.Group', on_delete=models.CASCADE, db_column='NRC')
    enrollment_date = models.DateField()
    status = models.CharField(max_length=15)

    class Meta:
        db_table = 'enrollments'
        unique_together = ('student', 'group')

    def __str__(self):
        return f"{self.student} - {self.group}"
