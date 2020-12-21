import requests


class SendMessage(object):

    def __init__(self,api_key):
        # 账号的唯一表示
        self.api_key = api_key
        # 单挑发送短信的接口
        self.send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_message(self,phone,code):
        """
        发送短信
        :param phone: 要发送的手机号
        :param code: 验证码
        :return: 返回请求的结果
        """
        data = {
            'apikey': self.api_key,
            'mobile': phone,
            'text': "【张振宇test】您的验证码是{}。如非本人操作，请忽略本短信".format(code)
        }
        print('发送信息')
        requests.post(self.send_url, data=data)

if __name__ == '__main__':
    msg = SendMessage('40d6180426417bfc57d0744a362dc108')
    msg.send_message('13293585128', '5210')
