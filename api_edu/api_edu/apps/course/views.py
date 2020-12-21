from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from course.models import Course, CourseCategory, CourseChapter
from course import serializers
from course.pagination import MyPagination
from course.serializers import CourseDetailModelSerializer, CourseChapterModelSerializer

# 课程分类展示
class CourseListAPIView(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False)
    serializer_class = serializers.CourseCategoryModelSerializer

# 课程列表展示
class CourseAPIView(ListAPIView):
    queryset = Course.objects.filter(is_delete=False, is_show=True)
    serializer_class = serializers.CourseModelSerializer

    # 设置使用的过滤的包
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # 设置通过什么字段来查找
    filterset_fields = ('course_category',)

    # 设置按照什么字段排序
    ordering_fields = ("id", "students", "price")

    # 设置自己的分页规则
    pagination_class = MyPagination


# 课程详情
class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False)
    serializer_class = CourseDetailModelSerializer

# 课程小节
class CourseLessonListAPIView(ListAPIView):
    queryset = CourseChapter.objects.filter(is_delete=False,is_show=True).order_by('id')
    serializer_class = CourseChapterModelSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course']
