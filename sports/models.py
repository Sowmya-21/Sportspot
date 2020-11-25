from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from phone_field import PhoneField
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class StudentRegisterForm(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200,null=True)
    usn = models.CharField(max_length=20,unique=True,blank=True)
    phone = PhoneNumberField(blank=True)
    branch = models.CharField(max_length=100)
    year = models.IntegerField()
    gender = models.CharField(max_length=10)
    password = models.CharField(max_length=300)

    def __str__(self):
        return self.name+"-"+self.usn  #returning the string value,this value comes in the admin panel interference.

class Mentor(models.Model):
    mentor = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    phone = PhoneNumberField(blank=True)
    img = models.ImageField(upload_to='mentor_imgs')
    experience = models.TextField(max_length=700)
    
    def __str__(self):
        return self.mentor


class Events(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateField(default=now)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    description=models.TextField(max_length=500)
    img = models.ImageField(upload_to='events_imgs')
    venue = models.TextField(max_length=200)
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, blank=True)
    deadline = models.DateField(default=now)
 
    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        return self.event_name

class Enrolment(models.Model):
    student = models.ForeignKey(StudentRegisterForm, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=True, blank=True)
    shortlist = models.BooleanField(default=False)
    
    def __str__(self):
        return self.student.name+"-"+self.student.usn+"-"+self.event.event_name
    

class Suggestion(models.Model):
    suggestion = models.TextField(max_length=600)        


class Gallery(models.Model):
    img = models.ImageField(upload_to="gallery_imgs")
    description = models.TextField(max_length=500)

    class Meta:
        verbose_name_plural = "Gallery"
