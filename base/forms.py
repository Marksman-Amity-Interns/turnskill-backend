from django.contrib.auth.models import User
from django.forms import fields
from backend.base.models import user
from django import forms
from django.contrib.auth.forms import UserCreationForm


class usercreationform(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = user
        fields = ['isInstructor','count_course', 'job', 'first_name', 'last_name', 'email', 'password']

