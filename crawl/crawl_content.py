import asyncio
import logging
import os
from multiprocessing import Pool

import aiohttp
import requests
from aiohttp import ContentTypeError
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
LESSION_URL = 'https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessons?courseId={id}'
INDEX_URL = 'https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessonDetail?lessonId={id}'
COURSE_LIST_URL = 'https://gate.lagou.com/v1/neirong/edu/homepage/getCourseListV2?isPc=true'
PAY_URL = 'https://gate.lagou.com/v1/neirong/edu/member/drawCourse?courseId={id}'
CONCURRENCY = 5

loop = asyncio.get_event_loop()

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


def lessions_list():
    response = requests.get(url=COURSE_LIST_URL, headers=headers)
    lessions_all = []
    if response is not None:
        course_list = response.json()['content']['contentCardList']
        for courses in course_list:
            if courses['cardType'] == 201:
                lessions_all = courses['courseList']
    return lessions_all


class Spider(object):

    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.semaphore = asyncio.Semaphore(CONCURRENCY)

    def scrape_lession_content(self, url, course_id):
        url = url.format(id=course_id)
        logging.info('scraping %s', url)
        param = {'courseId': course_id}
        r = requests.get(url, params=param, headers=headers)
        return r.json()

    async def scrape_api(self, url):
        async with self.semaphore:
            try:
                logging.info('scraping %s', url)
                params = {'lessonId': url.split('=')[1]}
                async with self.session.get(url, headers=headers, params=params) as response:
                    await asyncio.sleep(1)
                    return await response.json()
            except ContentTypeError as e:
                logging.error('error occurred while scraping %s', url, exc_info=True)

    async def scrape_detail(self, id):
        url = INDEX_URL.format(id=id)
        return await self.scrape_api(url)

    # html名称,目录名称,pdf内容,pdf所在文件夹
    async def write_html(self, file_name, theme, data, file_path):
        logging.info('saving data %s,%s', file_name, data)
        env = Environment(loader=FileSystemLoader('./'))
        template = env.get_template('template.htm')

        if data:
            xlsx_path = os.getcwd() + file_path
            if not os.path.exists(xlsx_path):
                os.makedirs(xlsx_path)
            with open(xlsx_path + '/' + file_name, 'w+', encoding='utf-8') as fout:
                html_content = template.render(theme=theme, body=data)
                fout.write(html_content)

    async def main(self, courceId):
        response = self.scrape_lession_content(LESSION_URL, course_id=courceId)
        course_section_list = response['content']['courseSectionList']
        lession_id = []
        lession_status = True
        file_path = response['content']['courseName']
        for course in course_section_list:
            for lession in course['courseLessons']:
                lession_status = lession['status']
                if lession_status == "RELEASE":
                    lession_id.append(lession['id'])
                elif lession_status == "UNRELEASE":
                    lession_status = False
        scrape_index_tasks = [asyncio.ensure_future(self.scrape_detail(page)) for page in lession_id]
        results = await asyncio.gather(*scrape_index_tasks)
        print('results', results)
        contents = []
        for index_data in results:
            content = index_data['content']
            if content is None:
                continue
            data = {'id': int(content['id']), 'theme': str(content['theme']),
                    'content': str(content['textContent'])}
            contents.append(data)

        output_path = ''
        if lession_status:
            output_path = '/' + '已更新完/' + file_path
        else:
            f = 'unreleased.txt'
            with open(f, "a") as file:
                file.write(str(courceId) + "\n")
            output_path = '/' + '未更新完/' + file_path + '（未更新完）'

        scrape_detail_tasks = [asyncio.ensure_future(self.write_html(str(content['id']) + '.html',
                                                                     content['theme'], content['content'],
                                                                     output_path))
                               for content in contents]
        await asyncio.wait(scrape_detail_tasks)
        await self.session.close()

    @classmethod
    def crawl_all(cls):
        # 全量爬取
        lessions = lessions_list()
        pool = Pool(processes=5)
        for lession in lessions:
            print(lession)
            if lession['tag'] != '上新优惠':
                lession_id = lession['id']
                spider = Spider()
                pool.apply_async(loop.run_until_complete(spider.main(lession_id)))
                print('======> 开始爬取专栏：{}，编号：{} <======'.format(lession['title'], lession_id))
        pool.join()
        pool.close()

    @classmethod
    def crawl_increase(cls):
        # 增量爬取
        unreleases = set([line.rstrip('\n') for line in open('unreleased.txt', 'r')])
        lessions = list(unreleases | set(
            [line.rstrip('\n') for line in open('downloads.txt', 'r')]))
        pool = Pool(processes=5)
        open("unreleased.txt", 'w').close()
        for lession_id in lessions:
            spider = Spider()
            print('======> 开始爬取编号：{} <======'.format(lession_id))
            pool.apply_async(loop.run_until_complete(spider.main(lession_id)))
        pool.close()
        pool.join()
        open("downloads.txt", 'w').close()
        updated_unreleased_course = set([line.rstrip('\n') for line in open('unreleased.txt', 'r')])
        print('部分专栏由未完成变为已完成{}'.format(list(unreleases - updated_unreleased_course)))
        unreleased_courses = list(unreleases & updated_unreleased_course)
        open("unreleased.txt", 'w').close()
        with open('unreleased.txt', "a") as file:
            for unreleased_course in unreleased_courses:
                file.write(str(unreleased_course) + "\n")


if __name__ == '__main__':
    spider = Spider()
    # 全量爬取
    # spider.crawl_all()
    # 增量爬取
    spider.crawl_increase()
