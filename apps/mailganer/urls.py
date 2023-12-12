from django.urls import path

from .views import track_email_open

app_name = "mailganer"

urlpatterns = [
    path("tracking/<str:tracking_id>/", track_email_open, name="track_email_open"),
]
