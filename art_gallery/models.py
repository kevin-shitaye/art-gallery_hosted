from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, phone_number, gmail_smtp_key, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, phone_number, gmail_smtp_key=gmail_smtp_key, **other_fields)

    def create_user(self, email, user_name, password, phone_number, gmail_smtp_key, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, phone_number=phone_number, gmail_smtp_key=gmail_smtp_key, **other_fields)
        user.set_password(password)
        user.save()
        return user

class Account(AbstractUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True)
    phone_number = models.CharField(max_length=150, unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    
    
    #social links
    facebook = models.CharField(_('Facebook'),max_length=150, blank=True)
    telegram = models.CharField(_('Telegram'),max_length=150, blank=True)
    instagram = models.CharField(_('Instagram'),max_length=150, blank=True)
    tiktok = models.CharField(_('Tiktok'),max_length=150, blank=True)
    youtube = models.CharField(_('Youtube'),max_length=150, blank=True)
    twitter = models.CharField(_('Twitter'),max_length=150, blank=True)
    linkedin = models.CharField(_('Linkedin'),max_length=150, blank=True)
    
    email_notification = models.BooleanField(_("Email notification"), default=True)
    gmail_smtp_key = models.CharField(_("SMTP_KEY"), max_length=50)
    
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['phone_number', 'email', 'gmail_smtp_key']

    objects = CustomAccountManager()

class Art(models.Model):
    class Meta:
        verbose_name = _("Art")
        verbose_name_plural = _("Arts")

    id = models.CharField(_("Id"), primary_key=True, max_length=200)
    title = models.CharField(_("Title"), max_length=50, blank=False)
    image_url = models.CharField(_("Image"), max_length=50)
    category = models.ForeignKey("category", verbose_name=_(""), on_delete=models.CASCADE)
    tags = models.CharField(_("tags"), max_length=50, blank=True)
    description = models.CharField(_("description"), max_length=500)
    is_featured = models.BooleanField(_("Featured"), default=False)
    discount = models.FloatField(_("Discount"), default=0.0)
    available_copies = models.IntegerField(_("Number of copies available"), default=1)
    sold_amount = models.IntegerField(_("Sold amount"), default=0)
    number_of_views = models.IntegerField(_("Number of views"), default=0)
    
    def __str__(self):
        return self.title
    
class Category(models.Model):
    
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        
    name = models.CharField(_("name"), max_length=50, unique=True, blank=False)
        
    def __str__(self):
        return self.name
    
class Client(models.Model):

    class Meta:
        """Meta definition for Client."""
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        
    email = models.EmailField(_("Email"), max_length=254, primary_key=True)
    purchases_completed = models.ManyToManyField("art", verbose_name=_(""), related_name='purchased_arts', blank=True)
    # pending_orders = models.ManyToManyField("art", verbose_name=_(""), related_name='ordered_arts', blank=True)
    is_subscribed = models.BooleanField(_("Subscribed"), default=False)
    has_contacted = models.BooleanField(_("Has contacted"), default=False)
    has_purchased = models.BooleanField(_("Has purchased"), default=False)
    
    def __str__(self):
        return self.email

class Address(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    def __str__(self):
        return self.name
    

class Transaction(models.Model):
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        
    transaction_id = models.CharField(_("Transaction ID"), max_length=50, blank=False)
    client = models.ForeignKey("client", verbose_name=_(""), on_delete=models.DO_NOTHING)
    is_fulfilled = models.BooleanField(_("is_fulfilled"), default=False)
    art = models.ForeignKey("art", verbose_name=_(""), on_delete=models.DO_NOTHING)
    date = models.DateField(_("Date"), auto_now=True)
    quantity = models.IntegerField(_("Quantity"), default=1)
    address = models.ForeignKey("Address", verbose_name=_("Address"), on_delete=models.DO_NOTHING)
        
    def __str__(self):
        return self.transaction_id
        
        
class EmailMessage(models.Model):
    class Meta:
        verbose_name = "EmailMessage"
        verbose_name_plural = "EmailMessages"
        
    recipients = models.ManyToManyField("Client", verbose_name=_("Client"))
    subject = models.CharField(_("Subject"), max_length=100, default="No subject")
    body  = models.CharField(_("Body"), max_length=2000)
    attachement = models.FileField(_("Attachement"), upload_to=None, blank=True)
    template = models.CharField(_("Template"), max_length=50, default="general")
    
    def __str__(self):
        return self.subject
    
    

class EmailNotification(models.Model):
    class Meta:
        verbose_name = "EmailNotification"
        verbose_name_plural = "EmailNotification"
        
    recipients = models.ManyToManyField("Account", verbose_name=_("Account"))
    subject = models.CharField(_("Subject"), max_length=100, default="No subject")

    
    def __str__(self):
        return self.subject
    