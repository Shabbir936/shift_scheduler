from django.core.mail import EmailMessage,send_mail
from django.utils import timezone
from .models import EmployeeShift
import pandas as pd
from io import BytesIO
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_daily_schedule_email():
    today = timezone.now().date()
    reports = EmployeeShift.objects.filter(date=today)
    if reports.exists():
        email_id = "s.hote936@gmail.com"
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

        email_subject = f"Today's Shift Report"
        email_body = f"""Hi,\n
            Please find the attached Daily Shift Report"""
        email_message = EmailMessage(
            subject=email_subject, body=email_body, to=[email_id]
        )
        email_message.attach('shift_report.csv',buffer.getvalue(),'text/csv')
        email_message.send()
    else:
        send_mail(
            subject="Daily Schedule Report",
            message="No Shifts scheduled for today",
            recipient_list=['s.hotel936@gmail.com']
        )
        
@shared_task
def my_log_task():
    logger.info("Executing your_task_name")
    print("this task executed")
        
    