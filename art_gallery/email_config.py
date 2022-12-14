from redmail import EmailSender
from .contants import PORT, HOST

from .models import Account


# the first account the admin
admin = Account.objects.filter(pk=1).first()

# Configure an email sender
email_sender = EmailSender(
    host=HOST, port=PORT, 
    username=admin.email, 
    password=admin.gmail_smtp_key
    )
