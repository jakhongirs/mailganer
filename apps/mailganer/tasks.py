from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email_task(email, subject, message, recipient_list, user_fullname, user_birthdate):
    # Replace placeholders with actual values
    message = message.replace("{{ user_fullname }}", user_fullname)
    message = message.replace("{{ user_birthdate }}", user_birthdate)

    email_message = EmailMessage(subject, message, email, recipient_list)
    email_message.content_subtype = "html"  # Set the content type to HTML
    email_message.send()
