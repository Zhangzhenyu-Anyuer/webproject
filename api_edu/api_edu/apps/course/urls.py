from django.urls import path

from course import views

urlpatterns = [
    path('category/',views.CourseListAPIView.as_view()),
    path('course/',views.CourseAPIView.as_view()),
    path('detail/<str:pk>/',views.CourseDetailAPIView.as_view()),
    path('chapter/',views.CourseLessonListAPIView.as_view()),
]