from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import UserEmailDistribution


def track_email_open(request, tracking_id):
    # Retrieve the UserEmailDistribution instance based on the tracking_id
    user_email_distribution = get_object_or_404(
        UserEmailDistribution, tracking_pixel_url=f"http://localhost:8000/api/v1/mailganer/tracking/{tracking_id}/"
    )

    # Mark the email as read
    user_email_distribution.is_read = True
    user_email_distribution.save()

    pixel = "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    return HttpResponse(pixel, content_type="image/gif")
