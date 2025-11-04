from django.db import models

class Country(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='departments')

    class Meta:
        unique_together = ('name', 'country')

    def __str__(self):
        return f"{self.name} ({self.country.name})"


class City(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        unique_together = ('name', 'department')

    def __str__(self):
        return f"{self.name}, {self.department.name}"


class Campus(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='campuses')

    class Meta:
        db_table = 'campuses'
        ordering = ['name']
        verbose_name = 'Campus'
        verbose_name_plural = 'Campuses'

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Faculty(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='faculties')

    class Meta:
        db_table = 'faculties'
        ordering = ['name']
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return self.name


class Area(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='areas')

    class Meta:
        db_table = 'areas'
        ordering = ['name']
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self):
        return f"{self.name} - {self.faculty.name}"
