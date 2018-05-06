from django.core.mail import send_mail
from django.conf import settings


def send_rest_password_email(code, email):
    subject = 'Password reset'
    message = "http://%s:8000/profile/resetPassword/%s" % (settings.ALLOWED_HOSTS[0], code)
    from_email = settings.EMAIL_HOST_USER
    to_emails = [email]
    send_mail(
        subject,
        message,
        from_email,
        to_emails,
        fail_silently=False,
    )