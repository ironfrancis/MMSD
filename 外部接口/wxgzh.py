import json

import requests

appId = 'wx29e6aea17dae404a'
appSecret = '34c89d8a841c5e5a71f799fcec177f95'
url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(appId, appSecret)
token = requests.get(url).json()['access_token']

# industry = requests.get(url='https://api.weixin.qq.com/cgi-bin/template/get_industry?access_token=' + token).json()
# print(industry)

# model_list = requests.get(
#     url='https://api.weixin.qq.com/cgi-bin/template/get_all_private_template?access_token=' + token).json()
# print(json.dumps(model_list, indent=5, ensure_ascii=False))


# userList = requests.get(url='https://api.weixin.qq.com/cgi-bin/user/get?access_token=' + token).json()
# print(json.dumps(userList, indent=5, ensure_ascii=False))

# for openId in userList['data']['openid']:
#     print(openId)
#     print(requests.get(url='https://api.weixin.qq.com/cgi-bin/user/info?access_token={}&openid={}&lang=zh_CN'.format(token, openId)).json())

manager = ['oOezu5-H4wl5TVsKNvv31FfDQVWo', ]


def send_template(openId, templateId, data):
    _url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(token)
    _data = {
        'touser': openId,
        'template_id': templateId,
        'data': data
    }
    return print(requests.post(_url, data=json.dumps(_data, )).json())


data = {
    "first": {
        "value": "恭喜你购买成功！",
    },
    "keyword1": {
        "value": "i love you",
    },
    "keyword2": {
        "value": "1314520",
    },
    "remark": {
        "value": "欢迎再次购买！",
    }
}

# send_template(openId=manager[0], templateId='Wx3ZbAdzdcfW6-QZgUkskLaR3FV04N35BrpgRZ5gudU', data=data)
