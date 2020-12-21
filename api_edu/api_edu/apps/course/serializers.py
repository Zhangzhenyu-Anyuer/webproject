from rest_framework.serializers import ModelSerializer

from course.models import Course, CourseCategory, Teacher, CourseChapter, CourseLesson


class CourseCategoryModelSerializer(ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ('id', 'name')


class TeacherModelSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'name', 'title', 'signature', 'image')


class CourseModelSerializer(ModelSerializer):
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ('id', 'name', 'course_img', "students", "lessons", "pub_lessons", "price",
                  'teacher', 'lesson_list', 'discount_name', 'real_price')


class CourseDetailModelSerializer(ModelSerializer):
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ('id', 'name', 'course_img', "students", "lessons", "pub_lessons", "price",
                  'teacher', 'level_name', 'active_time', 'course_video', 'real_price')


class CourseLessonModelSerializer(ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ('id', 'name', 'free_trail')


class CourseChapterModelSerializer(ModelSerializer):
    # 一对多的时候要记得加参数 many
    coursesections = CourseLessonModelSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ('id', 'name', 'chapter', 'coursesections')
