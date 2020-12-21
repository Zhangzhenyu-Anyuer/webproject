from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.generics import CreateAPIView
from rest_framework import status as http_status
from django_redis import get_redis_connection

from api_edu.utils.contastnt import COURSE_IMG_SRC
from course.models import Course, CourseExpire
from order.models import Order
from order.serializers import OrderModelSerializer


class CartTotalPriceViewSet(ViewSet):
    def get_total_price(self, request):
        """
        1. 获取购物车中勾选的课程
        2. 获取购物车中勾选后的价格
        3. 获取到价格之后计算总价，
        """
        # : 1. 获取购物车中勾选的课程
        user_id = request.user.id
        redis_connection = get_redis_connection('cart')
        cart_list_b = redis_connection.hgetall('cart_%s' % user_id)
        selected_list_b = redis_connection.smembers('selected_%s' % user_id)

        total_price = 0
        data = []
        for course_id_b, expire_id_b in cart_list_b.items():
            course_id = int(course_id_b)
            expire_id = int(expire_id_b)
            try:
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue

            print(course_id, '选择的课程有效期是', expire_id)
            # : 2. 获取购物车中勾选后的价格
            try:
                course_expire_obj = CourseExpire.objects.get(is_delete=False, is_show=True, pk=expire_id)
                course.price = course_expire_obj.price
                expire_text = course_expire_obj.expire_text
            except CourseExpire.DoesNotExist:
                course.price = course.price
                expire_text = '永久有效'

            # : 3. 获取到价格之后计算总价，
            if course_id_b in selected_list_b:
                total_price += course.real_price
                data.append({
                    'course_img': COURSE_IMG_SRC + course.course_img.url,
                    'name': course.name,
                    'final_price': course.real_price,
                    'expire_text': expire_text,
                    'price': course.price
                })
            if not data:
                return Response({'message': '未选择任何课程'}, status=http_status.HTTP_400_BAD_REQUEST)
        return Response({'message': '获取成功', 'total_price': total_price, 'courseList': data},
                        status=http_status.HTTP_200_OK)


class OrderAPIView(CreateAPIView):
    queryset = Order.objects.filter(is_delete=False, is_show=True)
    serializer_class = OrderModelSerializer
