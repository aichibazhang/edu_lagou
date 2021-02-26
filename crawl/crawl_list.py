import requests


# 获取所有专栏并且一键订阅所有未购买专栏
def lessions_subscription():
    lession_url = 'https://gate.lagou.com/v1/neirong/edu/homepage/getCourseListV2?isPc=true'
    pay_url = 'https://gate.lagou.com/v1/neirong/edu/member/drawCourse?courseId={id}'
    headers = {
        'Host': 'gate.lagou.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': '50dc5543e28179e1b1f19b2b33dd822d4a77358f1ad63131',
        'X-L-REQ-HEADER': '{deviceType:1}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Origin': 'https://edu.lagou.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://edu.lagou.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': '_ga=GA1.2.1714163244.1538059906; user_trace_token=20180927225145-dab89676-c264-11e8-bb60-5254005c3644; LGUID=20180927225145-dab8a02a-c264-11e8-bb60-5254005c3644; LG_HAS_LOGIN=1; smidV2=2020111122270356b5b6cd773f00293fe5fb053a36623f00458f122e11db710; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1606828510,1607003514; thirdDeviceIdInfo=%5B%7B%22channel%22%3A1%2C%22thirdDeviceId%22%3A%22WC39ZUyXRgdFtNzu21nJnRjD8suaWYPBLpSj1QtCf/n8I0QiOGxTXVkcK/U2WkGPE27COUkaIJNBBcCgdfqonG5XXGjdPfgJmtL/WmrP2Tav+DYF2YqyHqxIR05Q+ZmNnO7dVu22KtO4OuktY0c6Dw/bCeCS3dY9p8Ozw+p1E5euaKk0cJkZrpVM9+IKcP/xnQY+jhNjhw0bAdfRWw1vjteHHHFvUhFLQkXYTpZQUt2MorGmhc0xqaIo311gF9gMV1487577677129%22%7D%2C%7B%22channel%22%3A2%7D%5D; user-finger=6a422ca24ce4fd2a38dc3c9e4de2f993; LG_LOGIN_USER_ID=bf1aaf236e5fe780fa4ff001124e7de83d9dab21328111cf; EDUJSESSIONID=ABAAAECABCAAACDACBB9E00C6C58DE9770917E3FBC9CFE5; sensorsdata2015session=%7B%7D; _putrc=34C749CE011C29AB; login=true; unick=%E9%9F%A9%E5%86%AC%E5%86%AC; kw_login_authToken="Qm9p039JTrZOKXRFT9n/8DF3MhaFIQODcA1/kuUni/kohaJElwqZFRrQXqV96E95ZmA4LirwEpti4nZH3rpE9cdttBtS7+YycdiIviugDPPZsdPn6FSb7vv/beIASl4c8/ueRqrAOx7Lv2eCpf7sSsu4c7VRD+uwRKYfANmDLW54rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; gate_login_token=50dc5543e28179e1b1f19b2b33dd822d4a77358f1ad63131; JSESSIONID=B88A423C0C78DF22CFD14EA3FF3207BF; X_HTTP_TOKEN=85dfc7b21b5ddd19025992416178b2be389f7d4d5f; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229862931%22%2C%22%24device_id%22%3A%22168e171fe80a1e-07f627ced1772c-9393265-2073600-168e171fe8131c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22baidujava%22%2C%22%24latest_utm_medium%22%3A%22sspc%22%2C%22%24latest_utm_term%22%3A%22java3224%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2288.0.4324.190%22%7D%2C%22first_id%22%3A%22177dbb873d6695-040a886c821bc6-53e356a-1327104-177dbb873d7b7a%22%7D'
    }
    response = requests.get(url=lession_url, headers=headers)
    lessions_all = []
    if response is not None:
        print(response.json())
        lessions_all = []
        course_list = response.json()['content']['contentCardList']
        for courses in course_list:
            if courses['cardType'] == 201:
                lessions_all = courses['courseList']
    lession_size = len(lessions_all)
    print(lessions_all)
    for lession in lessions_all:
        if not lession['hasBuy']:
            pay_response = requests.get(url=pay_url.format(id=lession['id']), headers=headers)
            if lession['tag'] != '上新优惠':
                if pay_response.json()['content']['drawStatus']:
                    print('课程', lession['title'], '订购成功！！！')
            else:
                lession_size = lession_size - 1
                print('课程', lession['title'], 'vip 暂时无法订购！！！')
        else:
            print('课程', lession['title'], '已订阅！！！')
    print('恭喜，拉钩专栏当前拥有{}，已经全部订阅！！！'.format(lession_size))


if __name__ == '__main__':
    lessions_subscription()
