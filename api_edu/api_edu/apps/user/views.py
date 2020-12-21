import json
import random
import re
import string

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status
from rest_framework.generics import CreateAPIView
from django_redis import get_redis_connection
from api_edu.libs.geetest import GeetestLib

# 请在官网申请ID使用，示例ID不可使用
from api_edu.utils import contastnt
from api_edu.utils.send_msg import SendMessage
from user.models import UserInfo
from user.serializers import UserModelSerializer
from user.utils import get_user_by_account


class CaptchaAPIView(APIView):
    user_id = 0
    status = ''

    # pc端获取验证码的方法
    def get(self, request):
        username = request.query_params.get('username')
        user = get_user_by_account(username)
        if user is None:
            return Response({'message': '用户不存在'}, status=http_status.HTTP_400_BAD_REQUEST)

        user_id = user.id
        gt = GeetestLib(contastnt.PC_GEETEST_ID, contastnt.PC_GEETEST_KEY)
        status = gt.pre_process(user_id)
        self.status = status
        self.user_id = user_id
        response_str = gt.get_response_str()
        return Response(response_str)

    # pc端基于前后端分离校验验证码
    def post(self, request):
        print(request.data)
        gt = GeetestLib(contastnt.PC_GEETEST_ID, contastnt.PC_GEETEST_KEY)
        challenge = request.data.get(gt.FN_CHALLENGE, '')
        validate = request.data.get(gt.FN_VALIDATE, '')
        seccode = request.data.get(gt.FN_SECCODE, '')
        status = self.status
        user_id = self.user_id
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        print(result)
        return Response(json.dumps(result))


class RegisterAPIView(CreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer


class CheckPhoneAPIView(APIView):
    def get(self, request, *args, **kwargs):
        phone = request.query_params.get('phone')
        print('进行手机验证！')
        # 验证手机号码格式
        if not re.match(r'1[35789]\d{9}', phone):
            return Response({'message': '手机格式错误'},
                            status=http_status.HTTP_400_BAD_REQUEST)
        user = get_user_by_account(phone)
        # 格式正确手机号存在
        if user is not None:
            return Response({'message': '手机号已经被注册'},
                            status=http_status.HTTP_400_BAD_REQUEST)
        # 手机号不存在
        return Response({'message': '注册成功'},
                        status=http_status.HTTP_200_OK)


class SendMessageAPIView(APIView):
    """
        实现发送短信的接口
        1. 前端请求获取验证码
        2. 生成随机验证码，并将验证码保存在redis中
        3. 向短信平台请求验证码
        4. 返回结构
    """

    def get(self, request, *args, **kwargs):
        phone = request.query_params.get('phone')
        if not phone:
            return Response({'message': '请输入手机号'}, status=http_status.HTTP_400_BAD_REQUEST)

        redis_connection = get_redis_connection('default')
        mobile_code = redis_connection.get('sms_%s' % phone)
        # 如果redis中存在code说明在60s内发送过验证码
        if mobile_code is not None:
            return Response({
                'message': '您在60s内发送过短信，请稍等',
            }, status=http_status.HTTP_400_BAD_REQUEST)
        #         1.  前端请求获取验证码,判断是否60s内发送过验证码
        #         2.  生成随机验证码，并将验证码保存在redis中
        code = ''.join(random.sample([_ for _ in string.digits], 6))
        print('生成验证码%s' % code)
        redis_connection.setex('sms_%s' % phone, contastnt.MESSAGE_EXPIRE_TIME, code)
        #         3.  向短信平台请求验证码
        try:
            SendMessage(contastnt.API_KEY).send_message(phone, code)
        except:
            return Response({
                'message': '获取验证码失败'
            }, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)
        #         4.  返回结果
        return Response({
            'message': '获取验证码成功'
        }, status=http_status.HTTP_200_OK)
