from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.fields import IntegerField
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class UserFunction(models.Model):
    function_choices = {
        ('admin', 'admin'),
        ('sales', 'sales'),
        ('support', 'support')
    }
    function = models.CharField(_("function"), max_length=50,choices=function_choices)

    def __str__(self):
        return self.function


class EventStatus(models.Model):
    status_choices = {
        ('planning', 'planning'),
        ('running', 'running'),
        ('ended', 'ended'),
    }
    status = models.CharField(_("status"), max_length=50,choices=status_choices)

    def __str__(self):
        return self.status


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(_('first name'), max_length=25)
    last_name = models.CharField(_('last name'), max_length=25)
    email = models.EmailField(_('email address'), unique=True, max_length=100)
    function = models.ForeignKey(UserFunction, on_delete=models.DO_NOTHING, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Client(models.Model):
    first_name = models.CharField(_('first name'), max_length=25)
    last_name = models.CharField(_('last name'), max_length=25)
    email = models.EmailField(_('email address'), unique=True, max_length=100)
    phone = models.CharField(_("phone number"), max_length=20)
    mobile = models.CharField(_("mobile number"), max_length=20)
    compagny_name = models.CharField(_("compagny name"), max_length=250)
    sales_contact = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    propect = models.BooleanField(_("is prospect"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.compagny_name

class Event(models.Model):
    support_contact = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True, blank=True)
    event_status = models.ForeignKey(EventStatus, on_delete=models.DO_NOTHING)
    attendees = models.IntegerField(_("attendees"))
    event_date = models.DateTimeField(_("event date"), auto_now=False, auto_now_add=False)
    notes = models.TextField(_("notes"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.support_contact) + " - " + str(self.attendees)


class Contract(models.Model):
    sales_contact = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, blank=True, null=True)
    status = models.BooleanField('signed')
    amount = models.FloatField()
    payment_due = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.__str__() + ' - ' + self.event.__str__()