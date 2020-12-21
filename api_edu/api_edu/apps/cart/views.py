from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status as http_status
from rest_framework.views import APIView

from api_edu.utils.contastnt import COURSE_IMG_SRC
from course.models import Course, CourseExpire


class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def add_cart(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        user_id = request.user.id
        print(user_id, '向购物车中添加商品', course_id)
        # 是否勾选
        select = True
        # 有效期
        expire = 0

        # 校验前端参数
        res = Course.objects.filter(pk=course_id, is_show=True, is_delete=False)
        if not res:
            return Response({
                'message': '参数有误，课程不存在'
            }, status=http_status.HTTP_400_BAD_REQUEST)

        try:
            redis_connection = get_redis_connection('cart')
            # 将数据通过管道保存到redis数据库中
            pipeline = redis_connection.pipeline()
            # 保存商品的信息，有效期
            pipeline.hset('cart_%s' % user_id, course_id, expire)
            # 保存商品的勾选状态
            pipeline.sadd('selected_%s' % user_id, course_id)
            # 执行管道操作
            pipeline.execute()
            # 获取购物车中的数量
            course_length = redis_connection.hlen('cart_%s' % user_id)
        except:
            return Response({'message': '参数有误，添加购物车失败'}, status=http_status.HTTP_400_BAD_REQUEST)

        return Response({'message': '添加购物车成功', 'cart_length': course_length}, status=http_status.HTTP_200_OK)

    def show_list(self, request):
        user_id = request.user.id
        # 从redis中拿出购物车中的课程
        redis_connection = get_redis_connection('cart')
        cart_list_b = redis_connection.hgetall('cart_%s' % user_id)
        selected_list_b = redis_connection.smembers('selected_%s' % user_id)
        # total_price = 0
        data = []
        for course_id_b, expire_id_b in cart_list_b.items():
            course_id = int(course_id_b)
            expire_id = int(expire_id_b)
            try:
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist or CourseExpire.DoesNotExist:
                continue

            print(course_id, '选择的课程有效期是', expire_id)
            try:
                course_expire_price = CourseExpire.objects.get(is_delete=False, is_show=True, pk=expire_id).price
                course.price = course_expire_price
            except CourseExpire.DoesNotExist:
                course.price = course.price

            data.append({
                'selected': True if course_id_b in selected_list_b else False,
                'course_img': COURSE_IMG_SRC + course.course_img.url,
                'id': course.id,
                'name': course.name,
                'price': course.real_price,
                'expire_time': course.expire_time,
                'expire_id': expire_id,
                'origin_price': course.price
            })
            # if course_id_b in selected_list_b:
            #     total_price += course.real_price
        return Response({'course_info': data})

    def del_course(self, request):
        course_id = request.data.get('course_id')
        user_id = request.user.id
        print(user_id, '删除课程', course_id)
        redis_connection = get_redis_connection('cart')
        if not redis_connection.hexists('cart_%s' % user_id, course_id):
            return Response({'message': '课程不存在'}, status=http_status.HTTP_400_BAD_REQUEST)
        redis_connection.hdel('cart_%s' % user_id, course_id)
        return Response({'message': '删除成功'}, status=http_status.HTTP_200_OK)


# 购物车的数量视图
class CartLengthAPIView(APIView):

    def get(self, request):
        user_id = request.user.id
        print(user_id, '的购物车数量')
        if user_id is not None:
            redis_connection = get_redis_connection('cart')
            course_length = redis_connection.hlen('cart_%s' % user_id)
            return Response({'cart_length': course_length}, status=http_status.HTTP_200_OK)
        return Response({'cart_length': 0}, status=http_status.HTTP_400_BAD_REQUEST)


class TotalPriceViewSet(ViewSet):
    def update_total_price(self, request):
        # TODO: 计算总价，当前端每次修改勾选状态，删除课程，修改有效期，然后改变总价
        # 获取到勾选的课程，获取到有效期后的价格，然后相加，最后得到总价格
        user_id = request.user.id
        redis_connection = get_redis_connection('cart')
        # 获取购物车中的课程
        cart_list_b = redis_connection.hgetall('cart_%s' % user_id)
        selected_list_b = redis_connection.smembers('selected_%s' % user_id)
        total_price = 0
        for course_id_b, expire_id_b in cart_list_b.items():
            course_id = int(course_id_b)
            expire_id = int(expire_id_b)
            try:
                course_obj = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue
            try:
                course_expire_price = CourseExpire.objects.get(is_delete=False, is_show=True, pk=expire_id).price
                course_obj.price = course_expire_price
            except CourseExpire.DoesNotExist:
                course_obj.price = course_obj.price
            if course_id_b in selected_list_b:
                total_price += course_obj.real_price
        return Response({'message': '获取总价格成功', 'total_price': total_price})


# 进行购物车中勾选状态的改变，前端改变后后端在redis中进行修改
class CartSelectedViewSet(ViewSet):
    def change_selected(self, request):
        user_id = request.user.id
        selected = request.data.get('selected')
        course_id = request.data.get('course_id')
        redis_connection = get_redis_connection('cart')
        print(user_id, '要改变勾选状态', selected, '课程是', course_id)
        if selected:
            # 如果改变为勾选状态
            redis_connection.sadd('selected_%s' % user_id, course_id)
        else:
            # 如果改变为不勾选状态
            redis_connection.srem('selected_%s' % user_id, course_id)
        return Response({'message': '改变成功'}, status=http_status.HTTP_200_OK)


# 进行购物车中有效期的更改，前端改变后后端在redis中进行修改
class CartExpireChangeViewSet(ViewSet):
    # TODO： 进行修改，只进行修改有效期，并且返回更改有效期后的每个课程的单价
    def change_expire(self, request):
        user_id = request.user.id
        course_id = request.data.get('course_id')
        expire_id = request.data.get('expire_id')
        print(user_id, '选择有效期为', expire_id, '的课程', course_id)
        # 查询操作的课程是否存在
        try:
            course = Course.objects.get(is_delete=False, is_show=True, pk=course_id)
            price = course.real_price
            # 如果前端传递的有效期的id不是0 则修改对应课程的有效期
            if expire_id > 0:
                try:
                    expire_obj = CourseExpire.objects.get(is_show=True, is_delete=False, pk=expire_id)
                except CourseExpire.DoesNotExist:
                    expire_obj = None
                if not expire_obj:
                    raise CourseExpire.DoesNotExist("课程有效期不存在")
        except Course.DoesNotExist:
            return Response({"message": "课程信息不存在"}, status=http_status.HTTP_400_BAD_REQUEST)
        redis_connection = get_redis_connection("cart")
        redis_connection.hset("cart_%s" % user_id, course_id, expire_id)
        try:
            course.price = expire_obj.price
            price = course.real_price
        except:
            print("出现了错误")
            return Response({"message": "有效期切换失败", 'price': price})
        return Response({'message': '有效期切换成功', 'price': price})


