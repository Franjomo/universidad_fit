from django.db import models

class ContractType(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    class Meta:
        db_table = 'contract_types'
        verbose_name = 'Contract Type'
        verbose_name_plural = 'Contract Types'
        ordering = ['name']

    def __str__(self):
        return self.name


class EmployeeType(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    class Meta:
        db_table = 'employee_types'
        verbose_name = 'Employee Type'
        verbose_name_plural = 'Employee Types'
        ordering = ['name']

    def __str__(self):
        return self.name
