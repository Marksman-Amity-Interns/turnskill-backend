from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import course, feedback, user
from rest_framework_simplejwt.tokens import RefreshToken

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = course
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['id','first_name', 'last_name', 'count_course', 'job', 'email']

class UserForCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['email']

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = user
        fields = ['id', 'email', 'first_name','last_name','count_course', 'job', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = feedback
        fields = '__all__'