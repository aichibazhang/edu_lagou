import requests


# 获取所有专栏并且一键订阅所有未购买专栏
def get_lessions():
    lession_url = 'https://gate.lagou.com/v1/neirong/edu/homepage/getCourseListV2?isPc=true'
    pay_url = 'https://gate.lagou.com/v1/neirong/edu/member/drawCourse?courseId={id}'
    headers = {
        'Host': 'gate.lagou.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': '78112f17c205afa411b8a3e263eea5823bedce8eaa6aa72c',
        'X-L-REQ-HEADER': '{deviceType:1}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
        'Origin': 'https://kaiwu.lagou.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://kaiwu.lagou.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'user_trace_token=20200910155152-128ed0c4-7d62-4ab7-a328-b735a82bc645; _ga=GA1.2.701951005.1599724320; LGUID=20200910155200-c3c0808f-8405-49c5-9497-689db3715dcf; smidV2=20201029105115a053f5d945964ea0124bfa6885bf193c0012bd57fd5ee8580; LG_HAS_LOGIN=1; LG_LOGIN_USER_ID=92502b49abb2cb140468b882372b15e6d5538b226f3100c4; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1612248973,1612248980,1612757652,1612757657; index_location_city=%E5%8C%97%E4%BA%AC; thirdDeviceIdInfo=%5B%7B%22channel%22%3A1%2C%22thirdDeviceId%22%3A%22WHJMrwNw1k/FsYDZ/e1ZnoqaCMTk88AhJ2Zdl50fRFVQn/da97WD57RD5QRi6Ukv5O7zpgnOXyy423zADhTlc18EPJtx4NipwdCW1tldyDzmQI99+chXEijsI77PdA/Na9lCUKKcsmkTaFO8webhNijYmmmXo8LlTkQE5YcNLqNriNYPfoOP/bs07fxsVzj6+X2EFB6G47hrP6KRdcW7dhziM5iSMAfwctJkh7lbVV6ugar+5yYEDgMjYdxE5oTt6F10/rPYNoNw%3D1487582755342%22%7D%2C%7B%22channel%22%3A2%2C%22thirdDeviceId%22%3A%22140%23rLXo4U2JzzWUKQo2+bsu4pN8s7O2giCtmRWl2dhK7zGwyuX097L3x/W265txT6iY4Q0Blp1zz/j0YO9MtFzxJLjr73h/zzrb22U3lp1xzBsSV2EqlaOz2PD+Vo13q/II1wba7X53zINjumva2UiX/wP1W3q00r/vzaaz8UY56S6viHk8Kx0YkFLiU+SeFcO+yvx7fqPiOjjSxiAo/+n8IG9xcUPKp8pBCvHEiz9vA0D2maeLmJn9KJ8UD8z63/J2YLbVTLWU3pJ7PlX8+OLJoobIRnYOa76Da9ONTafBFWhDpF2kAVf/IRC2ICzs7otk69L31TX1HzynwiCHMYTKT6N9A1PHSyxf5iUB+zppz/Pq8IuYhaHGRZFA1iirl0YL1Vl4kAs1p2OGB0GTZ8j6kk7TutfJ5C+Mb8i/aj6vn92qPhKslrSRqxqqDTpax2SPKeHar3PSWjYeS2CyAFjHX5MYkJ0qudfqk6OiCiUEYqnA/K6+jvgeamqWsG11t8Mze5WPkuPDrUhacmJo2YKWDC4rHm+aihtOCg7sRlT7FkyhEOgk00mGsGl45D0noJ0P5uxXBKd6Zb4brUlRL0QpGSXhBdY72LjC7m0YngvTr/fEy8y2MWQe4QBl/BG1hfVeKIr5UWm0uRJgj94j0pUkdHRvC48AipVXIttHop5gxpvGlRbicV9pl59KND2mukv4QMrt2eTLWkK0/kGBNV0LVGfC2nftkyGzImIhiAViTwncTdjqzQF%3D%2Cundefined%22%7D%5D; user-finger=10ba38f39916c0d1aca2c11b71bef6f9; sensorsdata2015session=%7B%7D; EDUJSESSIONID=ABAAAECABCAAACD8AC2CC9C7D150208F93ACDF30DD25ACD; kw_login_authToken="C6vYOj+pY1/pzPzrMoHDprODkAe13XVZuik2O7VH9x4jGiFZJehBaW54jzOd/jIS7MMBnziX6w4+obd5gIbzlO7R72v/YDrvqR/Mj9X+jwBvzh5kot0EAMDFyOg8Z6hnbQ4u9yH4OdLV/W8gYZQLtqdUowZsQaoOT3vv3RwoW5l4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; gate_login_token=78112f17c205afa411b8a3e263eea5823bedce8eaa6aa72c; JSESSIONID=C141578EABE5AF17E440FB69C89283E6; X_HTTP_TOKEN=5b23063f5e550b676372604161e333a53ccfabe386; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229862931%22%2C%22%24device_id%22%3A%2217476fff4d166a-0bdc1337c84b9a-f7b1332-1445906-17476fff4d2cda%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22baidujava%22%2C%22%24latest_utm_medium%22%3A%22sspc%22%2C%22%24latest_utm_term%22%3A%22java7380%22%2C%22%24latest_utm_campaign%22%3A%22distribution%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2288.0.4324.182%22%7D%2C%22first_id%22%3A%221777fd0bcb25d8-0f3f32dbcc0355-33e3567-1445906-1777fd0bcb36f5%22%7D'
    }
    response = requests.get(url=lession_url, headers=headers)
    if response is not None:
        lessions_all = response.json()['content']['contentCardList'][4]['courseList']
        lession_size = len(lessions_all)
        for lession in lessions_all:
            if not lession['hasBuy']:
                pay_response = requests.get(url=pay_url.format(id=lession['id']), headers=headers)
                if pay_response.json()['content']['drawStatus']:
                    print('课程', lession['title'], '订购成功！！！')
            else:
                print('课程', lession['title'], '已订阅！！！')
        print('恭喜，拉钩专栏当前拥有{}，已经全部订阅！！！'.format(lession_size))


if __name__ == '__main__':
    get_lessions()