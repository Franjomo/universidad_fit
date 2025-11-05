from django.db import models
from django.utils import timezone


class Program(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    area = models.ForeignKey('locations.Area', on_delete=models.CASCADE, related_name='programs')

    def __str__(self):
        return f"{self.name} ({self.code})"


class Subject(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name


class Group(models.Model):
    nrc = models.CharField(max_length=10, primary_key=True)
    number = models.IntegerField()
    semester = models.CharField(max_length=6)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='groups')
    professor = models.ForeignKey('accounts.Employee', on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return f"{self.subject.name} - NRC {self.nrc}"


class Enrollment(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='enrollments')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=15)

    class Meta:
        unique_together = ('student', 'group')  # Equivalente a la PK compuesta (student_id, nrc)

    def __str__(self):
        return f"{self.student.id} → {self.group.nrc} ({self.status})"
