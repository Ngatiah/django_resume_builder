from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True,blank=False)
    email = models.EmailField(unique=True, null=True,blank=False)
    avatar = models.ImageField(null=True, default="media/149071.png",upload_to='avatars/',blank=True)
 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Resume(models.Model): 
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='resumes',null=True)
    image = models.ImageField(upload_to='media/',default='media/149071.png',null=True,blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=15)
    address = models.TextField()
    summary_title = models.CharField(max_length=100)
    summary_of_qualifications = models.TextField()
    skills_title = models.CharField(max_length=100)
    skills_sub_topic = models.CharField(max_length=100)
    skills = models.TextField()
    experiences_title = models.CharField(max_length=100)
    experiences_sub_topic = models.CharField(max_length=100)
    experiences = models.TextField()
    education_title = models.CharField(max_length=100)
    education_sub_topic = models.CharField(max_length=100)
    education = models.TextField()

    def __str__(self):
        return self.name