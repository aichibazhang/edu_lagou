import requests


# 获取所有专栏并且一键订阅所有未购买专栏
def lessions_subscription():
    lession_url = 'https://gate.lagou.com/v1/neirong/edu/homepage/getCourseListV2?isPc=true'
    pay_url = 'https://gate.lagou.com/v1/neirong/edu/member/drawCourse?courseId={id}'
    headers = {
        'Host': 'gate.lagou.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': '50dc5543e28179e1b1f19b2b33dd822d4a77358f1ad63131',
        'X-L-REQ-HEADER': '{"deviceType":1,"userToken":"50dc5543e28179e1b1f19b2b33dd822d4a77358f1ad63131"}',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Origin': 'https://edu.lagou.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://edu.lagou.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'user_trace_token=20200910155152-128ed0c4-7d62-4ab7-a328-b735a82bc645; _ga=GA1.2.701951005.1599724320; LGUID=20200910155200-c3c0808f-8405-49c5-9497-689db3715dcf; smidV2=20201029105115a053f5d945964ea0124bfa6885bf193c0012bd57fd5ee8580; LG_HAS_LOGIN=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1612248973,1612248980,1612757652,1612757657; EDUJSESSIONID=ABAAAECABCAAACD14B8441FC06F7A215CD4D775D4B848EF; sensorsdata2015session=%7B%7D; thirdDeviceIdInfo=%5B%7B%22channel%22%3A1%2C%22thirdDeviceId%22%3A%22WHJMrwNw1k/FsYDZ/e1ZnoqaCMTk88AhJ2Zdl50fRFVQn/da97WD57RD5QRi6Ukv5O7zpgnOXyy423zADhTlc18EPJtx4NipwdCW1tldyDzmQI99+chXEijsI77PdA/Na9lCUKKcsmkTaFO8webhNijYmmmXo8LlTkQE5YcNLqNriNYPfoOP/bkHt+iuM33fONJlDQ5WpldjQqSN07G/tn+8Vg+5pExYXpcswOFwofickraLPl3U0KoQ9LjlG+zV3SBMZJRjFRB4%3D1487582755342%22%7D%2C%7B%22channel%22%3A2%2C%22thirdDeviceId%22%3A%22140%23e+soLRHLzzW60zo23z9Q4pN8s7aiAuzO3f6nGDqnHyA81mqDgrQSZM8XG5kkk78mwVTLr3hqzznTTjTkciszzXbLVaBqlQzx2DD3VthqzFcJL28+lpYazDrbV2QvoAjXONdOHaU+PEWDyAzajDgEKuWsxMOvg+iQqIQSVHn2hVpgkV5XwOGG9x+++79mHjX05iU1kzL0jTQeFD9RRPdc5P03A9trpq44T2045zXDk/WMvXISWElxRx0OaUGqXGdtmF3SPwPMzwejQnd9JKMKj/6HzPWEXrdUk+RQ4PpIr/5SG3urTuF42IqMCqi07xJzeSU6RqAA7c2mFpGDFFoIZLNrThrtY0i6iX50L2d+tnKPP6+M241HPWmB4gX2k8Z6FV2srqqWXhJWmd6E1fgl/q4WG5qUVI4ykeom6+TNr//oQh7i8JvLOnABZnhdMkSld3SiWt53+llzFtZl0CvyPg3EbgDIAg95htPV6TWQggijt87DiCWFqAd4GN75PLXAYecLxXABl1P6T7rzF+rnOE1g8/gfCe2cz9n1LEHWRsSzQV5UJJltI2qrRXdBG73jJ/5yEZRN1HUSbXey8vr+aFY+94+V6h0oWM6WMuz7CKDEn6l4vV3V4+T0OBNekVu1xC8m3s4Xm11PsgaZhKV71vFH/hRGD6Ddt3RB4OHsJAa1Zb28olDm5GEbqrJt2hpceo/uPobDj+mfsK4+Qu+uTKsDATx7oGTF0trm4x45JKlWykCrpO8L0j7u0dRoY2yLsF%3D%3D%2Cundefined%22%7D%5D; user-finger=10ba38f39916c0d1aca2c11b71bef6f9; LG_LOGIN_USER_ID=e97b9c2b19f04d5c237d624e60c8a63c1f6fed2abb87bcdc; _putrc=34C749CE011C29AB; login=true; unick=%E9%9F%A9%E5%86%AC%E5%86%AC; kw_login_authToken="Pc8LtTGF6hLdAHcxomQH1SNsWpfab3wizxUR+Wr+z0hcNdLuHFBoN7S89wbKM3vnDLqUnCG3SzoHEkXvMsunKLqiBdBZ1W6kfLjj+X4Y6cRi9k20a/uStFJmfLk2riw2ZJTh0jk5lZjioaJsroXeqwRHCLJJH/a9qJASvDUJBnN4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; gate_login_token=50dc5543e28179e1b1f19b2b33dd822d4a77358f1ad63131; JSESSIONID=F8E5A1F321FD6716483E969466CC20FE; X_HTTP_TOKEN=5b23063f5e550b672587086161e333a53ccfabe386; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229862931%22%2C%22%24device_id%22%3A%2217476fff4d166a-0bdc1337c84b9a-f7b1332-1445906-17476fff4d2cda%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22baidujava%22%2C%22%24latest_utm_medium%22%3A%22sspc%22%2C%22%24latest_utm_term%22%3A%22java7380%22%2C%22%24latest_utm_campaign%22%3A%22distribution%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2289.0.4389.90%22%7D%2C%22first_id%22%3A%221787133d164393-05e481f4d35636-5771031-1445906-1787133d165958%22%7D',
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
                    with open('downloads.txt', "a") as file:
                        file.write(str(lession['id']) + "\n")
                    print('课程', lession['title'], '订购成功！！！')
            else:
                lession_size = lession_size - 1
                print('课程', lession['title'], 'vip 暂时无法订购！！！')
        else:
            print('课程', lession['title'], '已订阅！！！')
    print('恭喜，拉钩专栏当前拥有{}，已经全部订阅！！！'.format(lession_size))


if __name__ == '__main__':
    lessions_subscription()
