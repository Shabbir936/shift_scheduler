from django.contrib import admin
from django import forms

# Register your models here.
from .models import Location, Employee

class LocationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,{"fields": ['location_name']}),
    )
    
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'employee_dob':forms.DateInput(attrs={'type': 'date', 'class':'admin-date-field'})
        }

    
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm
    
admin.site.register(Location,LocationAdmin)
admin.site.register(Employee,EmployeeAdmin)
