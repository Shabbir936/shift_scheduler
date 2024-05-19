from django.urls import path

from . import views

app_name = "scheduler"
urlpatterns = [
    path("", views.index, name="index"),
    path("schedule_shift/",views.schedule_shift, name="schedule_shift"),
    path("shift_report/",views.shift_report, name="shift_report"),
    path("download_report/<str:from_date>/<str:to_date>",views.download_report,name="download_report"),
    path("email_report/",views.email_report,name="email_report"),
    path('test-email/', views.test_email),
    
]