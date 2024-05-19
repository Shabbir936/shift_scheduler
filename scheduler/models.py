from django.db import models

# Create your models here.

class Location(models.Model):
    location_name = models.CharField(primary_key=True,max_length=50, verbose_name="Location")
    
    def __str__(self) -> str:
        return self.location_name
    
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True, verbose_name="Employee ID")
    employee_name = models.CharField(max_length=200, verbose_name="Employee Name")
    employee_department = models.CharField(max_length=30,verbose_name="Employee Department")
    employee_dob = models.DateField(verbose_name="Employee Date of Birth")
    
    def __str__(self) -> str:
        employee_identifier = f"{self.employee_id} - {self.employee_name}"
        return employee_identifier
    
class EmployeeShift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Shift Date")
    from_time = models.TimeField(verbose_name="Shift start")
    to_time = models.TimeField(verbose_name="Shift End")
    
    def __str__(self) -> str:
        employee_shift = f"{self.employee.employee_name} scheduled for {self.date} from {self.from_time} - {self.to_time}"
        return employee_shift
