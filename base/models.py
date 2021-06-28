from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.
class user(AbstractUser):
    isInstructor = models.BooleanField(default=False)
    count_course = models.IntegerField(null=True, blank=True, default=0)
    job = models.CharField(max_length=200, null=True, blank=True)
    username = None
    email = models.EmailField(unique=True, blank=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class course(models.Model):
    course_id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    count_videos = models.IntegerField(null=True, blank=True, default=0)
    instructor = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)
    islive = models.BooleanField(default=False)
    isonetoone = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title

class video(models.Model):
    video_id = models.AutoField(primary_key=True, editable=False)
    course_id = models.ForeignKey(course, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    video_url = models.FileField(null=True, verbose_name="")
    transcript_url = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class enrolment(models.Model):
    course_id = models.ForeignKey(course, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(user, related_name='user_id', on_delete=models.SET_NULL, null=True)



class skill(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)
    #course_id = models.ForeignKey(course, on_delete=models.SET_NULL, null=True)
    skill_title = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.skill_title


class feedback(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)
    video_id = models.ForeignKey(video, on_delete=models.SET_NULL, null=True)
    feedback_id = models.AutoField(primary_key=True, editable=False)
    text = models.CharField(max_length=200, null=True, blank=True)
    sentiment = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.text

class notes(models.Model):
    notes_id = models.AutoField(primary_key=True, editable=False)
    user_id = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)
    video_id = models.ForeignKey(video, on_delete=models.SET_NULL, null=True)
    notes_url = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.notes_id