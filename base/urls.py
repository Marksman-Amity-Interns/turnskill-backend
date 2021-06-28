from django.urls import path
from django.urls.resolvers import URLPattern
from . import views


urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/register/',views.registerUser, name='register'),
    path('',views.getRoutes, name="routes"),
    path('courses/',views.getCourses, name="courses"),
    path('courses/<str:pk>/',views.getCourse, name ="course"),
    path('users/',views.getUsers, name ="users"),
    path('users/profile/',views.getUserProfile, name ="user-profile"),
    path('virtual-classroom/',views.getVirtualCourses, name="virtual-classroom"),
    path('virtual-classroom/<str:pk>/',views.getVirtualCourse, name ="virtual-classroom"),
    path('mentor/',views.getMentorCourses, name="mentor-courses"),
    path('mentor/<str:pk>/',views.getMentorCourse, name ="mentor-course"),
    path('video/<str:pk>/feedback/',views.registerFeedback, name ="register-feedback"),
    path('feedback/get/',views.getFeedbacks, name ="get-feedback"),
    path('sentiment/get/<str:pk>/',views.getSentiment, name ="get-sentiment"),
    path('feedbacks/get/<str:pk>/',views.getFeedbacks, name ="get-feedbacks"),
]