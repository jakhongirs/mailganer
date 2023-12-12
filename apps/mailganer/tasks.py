from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email_task(email, subject, message, recipient_list, user_fullname, user_birthdate):
    user_fullname = user_fullname if user_fullname else ""
    user_birthdate = user_birthdate.strftime("%d.%m.%Y") if user_birthdate else ""

    message = message.replace("{{ user_fullname }}", user_fullname)
    message = message.replace("{{ user_birthdate }}", user_birthdate)

    email_message = EmailMessage(subject, message, email, recipient_list)
    email_message.content_subtype = "html"
    email_message.send()
