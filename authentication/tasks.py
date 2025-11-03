from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task

from root.settings import EMAIL_HOST_USER

@shared_task
def send_code_email(user_email: dict, code):
    subject = "Email Verification"
    from_email = EMAIL_HOST_USER
    to = [user_email.get('email')]
    context = {
        "code": code,
    }
    html_content = render_to_string("verification_email.html", context=context)
    text_content = f"Your verification code is {code}"
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
