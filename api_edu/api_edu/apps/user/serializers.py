import re

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from user.models import UserInfo
from user.utils import get_user_by_account


class UserModelSerializer(ModelSerializer):
    token = serializers.CharField(max_length=1024, read_only=True)
    # 用户输入的验证码
    code = serializers.CharField(max_length=12, write_only=True)

    class Meta:
        model = UserInfo
        fields = ('phone', 'username', 'password', 'id', 'token', 'code')

        extra_kwargs = {
            'phone': {
                'write_only': True
            },
            'username': {
                'read_only': True
            },
            'password': {
                'write_only': True
            },
        }

    def validate(self, attrs):
        """完成用户数据的校验"""
        print('进行用户数据校验')

        # 从前端传递来phone、password
        phone = attrs.get('phone')
        password = attrs.get('password')
        code = attrs.get('code')
        # 1. : 验证手机号格式，是否存在
        # 2. : 校验密码的格式。
        if not re.match(r'1[35789]\d{9}', phone):
            raise serializers.ValidationError('手机号格式错误')
        user = get_user_by_account(phone)
        if user is not None:
            raise serializers.ValidationError('该手机号已经被注册~')
        # 3. : 进行校验密码
        if not re.match(r'\S', password):
            raise serializers.ValidationError('密码过于简单')
        # 4. : 用户名不存在后
        print('对验证码进行校验')
        redis_connection = get_redis_connection('default')
        mobile_code = redis_connection.get('sms_%s' % phone)
        if mobile_code.decode() != code:
            raise serializers.ValidationError('验证码不一致')
        return attrs

    def create(self, validated_data):
        """
        保存数据的操作。
        :param validated_data: 验证后的数据
        :return:
        """
        # 1.对密码进行加密后存储
        print(validated_data, '进行保存数据')
        phone = validated_data.get('phone')
        password = validated_data.get('password')
        # 2.处理用户名，随机字符串或者是phone
        user = UserInfo.objects.create(username=phone, password=make_password(password))
        # 3.为注册的用户进行手动生成token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user
