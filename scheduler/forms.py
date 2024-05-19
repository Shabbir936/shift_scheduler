from django import forms
from datetime import datetime, timedelta
from .models import Employee, Location
from .widgets import TimePickerInput


class ScheduleShiftForm(forms.Form):
    employees = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.SelectMultiple(attrs={"class":"form-control "}),
        required=True,
        label="Employee Names",
        help_text="Hold ctrl to select multiple employees, Hold shift to select employees in a range"
        
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(), label="Duty Location", required=True
    )
    date = forms.DateField(
        widget=forms.SelectDateWidget,
        label="Shift Date",
        required=True,
        initial=(datetime.today() + timedelta(days=1)),
    )
    from_time = forms.TimeField(
        widget=TimePickerInput, label="Shift Start Time", required=True
    )
    to_time = forms.TimeField(
        widget=TimePickerInput, label="Shift End Time", required=True
    )

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if datetime.today().date() > date:
            raise forms.ValidationError(
                "Shift can only be schedule for atleast one day in advance"
            )
        return date

    def clean_to_time(self):
        date = self.cleaned_data.get("date")
        from_time = self.cleaned_data.get("from_time")
        to_time = self.cleaned_data.get("to_time")
        if from_time and to_time and date:
            shift_hours = datetime.combine(date, to_time) - datetime.combine(
                date, from_time
            )
            if from_time > to_time:
                raise forms.ValidationError(
                    "Shift start time should be less than Shift end time"
                )
            elif shift_hours != timedelta(hours=8):
                raise forms.ValidationError(
                    "Shift should be either 4 hours or 8 hours long"
                )
        else:
            raise forms.ValidationError(
                "Please input values for date, shift Start and Shift end"
            )
        return to_time


class ReportFilterForm(forms.Form):
    from_date = forms.DateField(
        widget=forms.SelectDateWidget,
        label="Start Date",
        required=True,
        initial=(datetime.today() + timedelta(days=1)),
    )
    to_date = forms.DateField(
        widget=forms.SelectDateWidget,
        label="End Date",
        required=True,
        initial=(datetime.today() + timedelta(days=2)),
    )
    
    def clean_to_date(self):
        from_date = self.cleaned_data.get('from_date')
        to_date = self.cleaned_data.get('to_date')
        if to_date < from_date:
            raise forms.ValidationError("End date should be greater thatn Start Date")
        return to_date
