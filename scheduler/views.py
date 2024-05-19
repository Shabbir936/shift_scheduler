from django.shortcuts import render
from .forms import ScheduleShiftForm, ReportFilterForm
from .models import EmployeeShift
from django.contrib import messages
from django.http import FileResponse,HttpResponseRedirect
import pandas as pd
from io import BytesIO
from django.core.mail import EmailMessage

from django.core.mail import send_mail
from django.http import HttpResponse

def test_email(request):
    send_mail(
        'Test Email',
        'This is a test email.',
        's.hotel936@gmail.com',  # From email
        ['s.hotel936@gmail.com'],  # To email
    )
    return HttpResponse("Test email sent")


# Create your views here.
def index(request):
    return render(request, "scheduler/index.html")


def schedule_shift(request):
    success = False
    if request.method == "POST":
        form = ScheduleShiftForm(request.POST)
        if form.is_valid():
            employees = form.cleaned_data.get("employees")
            location = form.cleaned_data.get("location")
            date = form.cleaned_data.get("date")
            from_time = form.cleaned_data.get("from_time")
            to_time = form.cleaned_data.get("to_time")

            for employee in employees:
                EmployeeShift.objects.create(
                    employee=employee,
                    location=location,
                    date=date,
                    from_time=from_time,
                    to_time=to_time,
                )

            success = True
            form = ScheduleShiftForm()
    else:
        form = ScheduleShiftForm()

    return render(
        request, "scheduler/schedule.html", {"form": form, "success": success}
    )


# class EmployeeShiftListView(generic.ListView):
#     model = EmployeeShift
#     template_name = "scheduler/report.html"
#     context_object_name = "employee_shifts"


def shift_report(request):
    if request.method == "POST":
        form = ReportFilterForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data.get("from_date")
            to_date = form.cleaned_data.get("to_date")
            reports = EmployeeShift.objects.filter(
                date__lte=to_date, date__gte=from_date
            )
            return render(
                request,
                "scheduler/report.html",
                {
                    "form": form,
                    "reports": reports,
                    "from_date": from_date.strftime("%Y-%m-%d"),
                    "to_date": to_date.strftime("%Y-%m-%d"),
                },
            )
    else:
        form = ReportFilterForm
    return render(request, "scheduler/report.html", {"form": form})


def download_report(request, from_date, to_date):
    if from_date and to_date:
        print("here")
        reports = EmployeeShift.objects.filter(date__lte=to_date, date__gte=from_date)
        report_df = pd.DataFrame(
            list(
                reports.values(
                    "employee__employee_id",
                    "employee__employee_name",
                    "location__location_name",
                    "date",
                    "from_time",
                    "to_time",
                )
            )
        )
        buffer = BytesIO()
        report_df.to_csv(path_or_buf=buffer, index=False)
        buffer.seek(0)
        response = FileResponse(
            buffer,
            as_attachment=True,
            filename=f"schedule_report_{from_date}-{to_date}.csv",
        )
        return response


def email_report(request):
    if request.method == "POST":
        print('here')
        email_id = request.POST.get("email")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        reports = EmployeeShift.objects.filter(date__lte=to_date, date__gte=from_date)
        report_df = pd.DataFrame(
            list(
                reports.values(
                    "employee__employee_id",
                    "employee__employee_name",
                    "location__location_name",
                    "date",
                    "from_time",
                    "to_time",
                )
            )
        )
        buffer = BytesIO()
        report_df.to_csv(path_or_buf=buffer, index=False)
        buffer.seek(0)

        email_subject = f"Shift report from {from_date} to {to_date}"
        email_body = f"""Hi,\n
            Please find the attached Shift Report from {from_date} to {to_date}"""
        email_message = EmailMessage(
            subject=email_subject, body=email_body, to=[email_id]
        )
        email_message.attach('shift_report.csv',buffer.getvalue(),'text/csv')
        email_message.send()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'scheduler/shift_report.html')
