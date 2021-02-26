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
    'Cookie': '_ga=GA1.2.1714163244.1538059906; user_trace_token=20180927225145-dab89676-c264-11e8-bb60-5254005c3644; LGUID=20180927225145-dab8a02a-c264-11e8-bb60-5254005c3644; LG_HAS_LOGIN=1; smidV2=2020111122270356b5b6cd773f00293fe5fb053a36623f00458f122e11db710; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1606828510,1607003514; thirdDeviceIdInfo=%5B%7B%22channel%22%3A1%2C%22thirdDeviceId%22%3A%22WC39ZUyXRgdFtNzu21nJnRjD8suaWYPBLpSj1QtCf/n8I0QiOGxTXVkcK/U2WkGPE27COUkaIJNBBcCgdfqonG5XXGjdPfgJmtL/WmrP2Tav+DYF2YqyHqxIR05Q+ZmNnO7dVu22KtO4OuktY0c6Dw/bCeCS3dY9p8Ozw+p1E5euaKk0cJkZrpVM9+IKcP/xnQY+jhNjhw0bAdfRWw1vjteHHHFvUhFLQkXYTpZQUt2MorGmhc0xqaIo311gF9gMV1487577677129%22%7D%2C%7B%22channel%22%3A2%7D%5D; user-finger=6a422ca24ce4fd2a38dc3c9e4de2f993; LG_LOGIN_USER_ID=bf1aaf236e5fe780fa4ff001124e7de83d9dab21328111cf; EDUJSESSIONID=ABAAAECABCAAACDACBB9E00C6C58DE9770917E3FBC9CFE5; sensorsdata2015session=%7B%7D; _putrc=34C749CE011C29AB; login=true; unick=%E9%9F%A9%E5%86%AC%E5%86%AC; kw_login_authToken="Qm9p039JTrZOKXRFT9n/8DF3MhaFIQODcA1/kuUni/kohaJElwqZFRrQXqV96E95ZmA4LirwEpti4nZH3rpE9cdttBtS7+YycdiIviugDPPZsdPn6FSb7vv/beIASl4c8/ueRqrAOx7Lv2eCpf7sSsu4c7VRD+uwRKYfANmDLW54rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; gate_login_token=50dc5543e28179e1b1f19b2b33dd822d4a77358f1ad63131; JSESSIONID=B88A423C0C78DF22CFD14EA3FF3207BF; X_HTTP_TOKEN=85dfc7b21b5ddd19025992416178b2be389f7d4d5f; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229862931%22%2C%22%24device_id%22%3A%22168e171fe80a1e-07f627ced1772c-9393265-2073600-168e171fe8131c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22baidujava%22%2C%22%24latest_utm_medium%22%3A%22sspc%22%2C%22%24latest_utm_term%22%3A%22java3224%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2288.0.4324.190%22%7D%2C%22first_id%22%3A%22177dbb873d6695-040a886c821bc6-53e356a-1327104-177dbb873d7b7a%22%7D',
}


class Spider(object):

    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.semaphore = asyncio.Semaphore(CONCURRENCY)
        open("unreleased.txt", 'w').close()
        open("downloads.txt", 'w').close()

    def lessions_list(self):
        response = requests.get(url=COURSE_LIST_URL, headers=headers)
        lessions_all = []
        if response is not None:
            course_list = response.json()['content']['contentCardList']
            for courses in course_list:
                if courses['cardType'] == 201:
                    lessions_all = courses['courseList']
        return lessions_all

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
        downloaded_txt = 'downloads.txt'
        output_path = ''
        if lession_status:
            output_path = '/' + '已更新完/' + file_path
        else:
            f = 'unreleased.txt'
            with open(f, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                file.write(str(courceId) + "\n")
            output_path = '/' + '未更新完/' + file_path + '（未更新完）'
        print(output_path)
        # if not os.path.exists(output_path):
        #     scrape_detail_tasks = [asyncio.ensure_future(self.write_html(str(content['id']) + '.html',
        #                                                                  content['theme'], content['content'],
        #                                                                  output_path))
        #                            for content in contents]
        with open(downloaded_txt, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
            file.write(str(courceId) + "\n")
        # await asyncio.wait(scrape_detail_tasks)
        await self.session.close()


if __name__ == '__main__':
    spider = Spider()
    lessions = spider.lessions_list()
    pool = Pool(processes=5)
    for lession in lessions:
        if lession['tag'] != '上新优惠':
            lession_id = lession['id']
            spider = Spider()
            pool.apply_async(loop.run_until_complete(spider.main(lession_id)))
            print('======> 开始爬取专栏：{}，编号：{} <======'.format(lession['title'], lession_id))
    pool.close()
    pool.join()
