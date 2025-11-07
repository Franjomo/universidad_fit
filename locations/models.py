from django.db import models

class Country(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'countries'

    def __str__(self):
        return self.name

class Department(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    country = models.ForeignKey('locations.Country', on_delete=models.CASCADE, db_column='country_code')

    class Meta:
        db_table = 'departments'

    def __str__(self):
        return self.name


class City(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    department = models.ForeignKey('locations.Department', on_delete=models.CASCADE, db_column='dept_code')

    class Meta:
        db_table = 'cities'

    def __str__(self):
        return self.name


class Campus(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    city = models.ForeignKey('locations.City', on_delete=models.CASCADE, db_column='city_code')

    class Meta:
        db_table = 'campuses'

    def __str__(self):
        return self.name or f"Campus {self.code}"


class Faculty(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    location = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=15)
    dean_id = models.CharField(max_length=15, null=True, blank=True, unique=True)

    class Meta:
        db_table = 'faculties'

    def __str__(self):
        return self.name


class Area(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    faculty = models.ForeignKey('locations.Faculty', on_delete=models.CASCADE, db_column='faculty_code')
    coordinator_id = models.CharField(max_length=15, unique=True)

    class Meta:
        db_table = 'areas'

    def __str__(self):
        return self.name
