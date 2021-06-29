from django.http.response import HttpResponse
from .models import course, enrolment, user, video, skill, feedback
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializer import CourseSerializer, UserForCourseSerializer, UserSerializer, UserSerializerWithToken, FeedbackSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import status
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user_data = UserSerializerWithToken(self.user).data
        for k, v in user_data.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/users/',
        '/api/users/login/',
        '/api/users/register/',
        '/api/users/profile/',
        '/api/user/<str:pk>/',

        '/api/courses/',
        '/api/courses/<id>',

        '/api/virtual-classroom/',
        '/api/virtual-classroom/<id>',

        '/api/mentor/',
        '/api/mentor/<id>',

        'video/<str:pk>/feedback/',
        'feedback/get/',
        'sentiment/get/<str:pk>/',
        'feedbacks/get/<str:pk>/',
    ]

    return Response(routes)


@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user_obj = user.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            job=data['job'],
            email=data['email'],
            password=make_password(data['password']),
        )
        serializer = UserSerializerWithToken(user_obj, many=False)
        return Response(serializer.data)
    except:
        message = {
            'detail': 'User with this email already exists'
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
#@permission_classes([IsAdminUser])
def getUsers(request):
    users = user.objects.all()
    users_data = UserSerializer(users, many=True)
    return Response(users_data.data)

@api_view(['GET'])
def getUser(request, pk):
    user_obj = user.objects.get(id = pk)
    user_details = UserSerializer(user_obj, many=False)
    course_ids = enrolment.objects.filter(user_id=user_obj.id)
    user_skills_query = skill.objects.filter(
        user_id=user_obj.id).values('skill_title')
    user_skills = dict()
    for i in range(0, len(user_skills_query)):
        user_skills[i] = user_skills_query[i]['skill_title']
    course_details = dict()
    for c in range(0, len(course_ids)):
        course_details[c] = course.objects.filter(
            title=course_ids[c].course_id).values()[0]
    return Response({'user_details': user_details.data, 'courses_details': course_details, 'user_skills': user_skills})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user_obj = request.user
    user_details = UserSerializer(user_obj, many=False)
    course_ids = enrolment.objects.filter(user_id=user_obj.id)
    user_skills_query = skill.objects.filter(
        user_id=user_obj.id).values('skill_title')
    user_skills = dict()
    for i in range(0, len(user_skills_query)):
        user_skills[i] = user_skills_query[i]['skill_title']
    course_details = dict()
    for c in range(0, len(course_ids)):
        course_details[c] = course.objects.filter(
            title=course_ids[c].course_id).values()[0]
    return Response({'user_details': user_details.data, 'courses_details': course_details, 'user_skills': user_skills})


@api_view(['GET'])
def getCourses(request):
    courses = course.objects.filter(islive=False)
    courses_data = CourseSerializer(courses, many=True)
    return Response(courses_data.data)


@api_view(['GET'])
def getCourse(request, pk):
    course_obj = course.objects.filter(course_id=pk, islive=False)
    instructor_obj = course_obj[0].instructor
    instructor_data = UserForCourseSerializer(instructor_obj)
    instructor_skills_query = skill.objects.filter(
        user_id=instructor_obj.id).values('skill_title')
    instructor_skills = dict()
    for i in range(0, len(instructor_skills_query)):
        instructor_skills[i] = instructor_skills_query[i]['skill_title']
    courses_data = CourseSerializer(course_obj[0], many=False)
    video_ids = video.objects.filter(course_id=pk)
    video_details = dict()
    for c in range(0, len(video_ids)):
        video_details[c] = video.objects.filter(
            video_id=video_ids[c].video_id).values()[0]
    return Response({'courses_details': courses_data.data, 'instructor_details': instructor_data.data, 'video_details': video_details, 'instructor_skills': instructor_skills})


@api_view(['GET'])
def getVirtualCourses(request):
    courses = course.objects.filter(islive=True, isonetoone=False)
    courses_data = CourseSerializer(courses, many=True)
    print(courses)
    return Response(courses_data.data)


@api_view(['GET'])
def getVirtualCourse(request, pk):
    course_obj = course.objects.filter(
        course_id=pk, islive=True, isonetoone=False)
    instructor_obj = course_obj[0].instructor
    instructor_data = UserForCourseSerializer(instructor_obj)
    instructor_skills_query = skill.objects.filter(
        user_id=instructor_obj.id).values('skill_title')
    instructor_skills = dict()
    for i in range(0, len(instructor_skills_query)):
        instructor_skills[i] = instructor_skills_query[i]['skill_title']
    courses_data = CourseSerializer(course_obj[0], many=False)
    video_ids = video.objects.filter(course_id=pk)
    video_details = dict()
    for c in range(0, len(video_ids)):
        video_details[c] = video.objects.filter(
            video_id=video_ids[c].video_id).values()[0]
    return Response({'courses_details': courses_data.data, 'instructor_details': instructor_data.data, 'video_details': video_details, 'instructor_skills': instructor_skills})


@api_view(['GET'])
def getMentorCourses(request):
    courses = course.objects.filter(islive=True, isonetoone=True)
    courses_data = CourseSerializer(courses, many=True)
    print(courses)
    return Response(courses_data.data)


@api_view(['GET'])
def getMentorCourse(request, pk):
    course_obj = course.objects.filter(
        course_id=pk, islive=True, isonetoone=True)
    instructor_obj = course_obj[0].instructor
    instructor_data = UserForCourseSerializer(instructor_obj)
    instructor_skills_query = skill.objects.filter(
        user_id=instructor_obj.id).values('skill_title')
    instructor_skills = dict()
    for i in range(0, len(instructor_skills_query)):
        instructor_skills[i] = instructor_skills_query[i]['skill_title']
    courses_data = CourseSerializer(course_obj[0], many=False)
    video_ids = video.objects.filter(course_id=pk)
    video_details = dict()
    for c in range(0, len(video_ids)):
        video_details[c] = video.objects.filter(
            video_id=video_ids[c].video_id).values()[0]
    return Response({'courses_details': courses_data.data, 'instructor_details': instructor_data.data, 'video_details': video_details, 'instructor_skills': instructor_skills})


@api_view(['POST'])
def registerFeedback(request, pk):
    user_obj = request.user
    video_obj = video.objects.get(video_id=pk)
    data = request.data

    # Calculating Sentiment
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(data['text'])
    if sentiment_dict['compound'] >= 0.05:
        overallans = 1
    elif sentiment_dict['compound'] <= - 0.05:
        overallans = -1
    else:
        overallans = 0

    try:
        feedback_obj = feedback.objects.create(
            user_id=user_obj,
            video_id=video_obj,
            text=data['text'],
            sentiment=overallans
        )
        serializer = FeedbackSerializer(feedback_obj, many=False)
        return Response(serializer.data)
    except:
        message = {
            'detail': 'Feedback is not registered'
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getFeedbacks(request):
    feedbacks = feedback.objects.all()
    serializer = FeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getSentiment(request, pk):
    feedbacks_query = feedback.objects.filter(video_id=pk).values('sentiment')
    sentiments = dict()
    for i in range(0, len(feedbacks_query)):
        sentiments[i+1] = feedbacks_query[i]['sentiment']
    return Response(sentiments)

@api_view(['GET'])
#@permission_classes([IsAdminUser])
def getFeedbacks(request,pk):
    feedbacks_query = feedback.objects.filter(video_id=pk).values()
    print(feedbacks_query)
    feedbacks = dict()
    for i in range(0, len(feedbacks_query)):
        feedbacks[i+1] = feedbacks_query[i]
    print(feedbacks)
    return Response(feedbacks)