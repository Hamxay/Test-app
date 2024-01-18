from django.db import models
from django.utils.translation import gettext_lazy as _
from dashboard.messages import (EMAIL_ALREADY_REGISTERED)
# Create your models here.

class TimeStampModel(models.Model):
    '''
    Base model for all models
    '''
    create_date = models.DateTimeField(_('Date Created'), auto_now_add=True)
    modify_date = models.DateTimeField(_('Date Modified'), auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Contacts(models.Model):
    name  = models.CharField(max_length=800,blank=True,null=True)
    email= models.CharField(max_length=800,blank=True,null=True)
    

class Crushesdb(models.Model):
    submitter_name  = models.CharField(max_length=800,blank=True,null=True)
    submitter_email= models.CharField(max_length=800,blank=True,null=True)
    crush_name= models.CharField(max_length=800,blank=True,null=True)
    crush_email= models.CharField(max_length=800,blank=True,null=True)


class OTPAttempts(TimeStampModel):
    '''
    The model records the every user login attempts
    '''
    email = models.EmailField(_('Email Address'), unique=True, db_index=True, error_messages={'unique': EMAIL_ALREADY_REGISTERED})
    attempts = models.IntegerField(default=0)
    first_attempt_time = models.DateTimeField(null=True, blank=True)
    latest_timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "OTP Attempt"
        verbose_name_plural = "OTP Attempts"

    
