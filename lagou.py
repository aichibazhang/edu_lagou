import asyncio
import logging
import os

import aiohttp
import requests
from aiohttp import ContentTypeError
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
LESSION_URL = 'https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessons?courseId={id}'
INDEX_URL = 'https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessonDetail?lessonId={id}'
# 这里修改你要爬取的课程id
COURSE_ID = 257
CONCURRENCY = 5

loop = asyncio.get_event_loop()

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'application/json, text/plain, */*',
    'Authorization': '056a5a7d3dd1ea78216c37750f93a583709766340f709bde',
    'X-L-REQ-HEADER': '{deviceType:1}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'Origin': 'https://kaiwu.lagou.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://kaiwu.lagou.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': '_ga=GA1.2.1714163244.1538059906; user_trace_token=20180927225145-dab89676-c264-11e8-bb60-5254005c3644; LGUID=20180927225145-dab8a02a-c264-11e8-bb60-5254005c3644; LG_HAS_LOGIN=1; smidV2=2020111122270356b5b6cd773f00293fe5fb053a36623f00458f122e11db710; index_location_city=%E5%8C%97%E4%BA%AC; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1606828510,1607003514; X_HTTP_TOKEN=85dfc7b21b5ddd19526867806178b2be389f7d4d5f; sensorsdata2015session=%7B%7D; thirdDeviceIdInfo=%5B%7B%22channel%22%3A1%2C%22thirdDeviceId%22%3A%22WHJMrwNw1k/HPjaKNsnlIZv6ZQotyvf/drhQtqxiT6jPQGQsAR0CjO3XODL+BMdk6eSAbJLQn+rcPSHuda01Lp1ZxMuAkxN7Up3v5eHPbRcXGA6a3EEZRlIaHMOKM8qKVBJ7HANruhDjgssVEtOEyiJGebD4P9188MdzVDzvFXj8MGcNB6XAcm4UA0a8nehcQKei9dcuNh8ioRo7fyBt//6GOuRksqzVMJ4nyVWDkjb82kNF0emrW7C4Vc2T0mj05SBMZJRjFRB4%3D1487582755342%22%7D%2C%7B%22channel%22%3A2%2C%22thirdDeviceId%22%3A%22137%231eE9hE9o9AKkV3dLIBJXrJwWIr9CGujsIEwKgV68Dh9sBC/+5EeR6NkUHC8xuIxtr7shbBCx0cArbFJt8O3/nGflTZtGskBZE6wIIh8+rE5uuaZi9D/jVYS096ZbEkiLrXIxFE56YTakYifH6MCmNkKP1kBwUWP32RE/3vUwBbCD8H5y4P/V+XNIvv2G3Szxn2IBF1MnGJJxMmBdlKJm9LLtJvSflVJN+on5bAi38fh9a1Zo2mcUhf9m/HJbjogr4BZISWdx1f368L2RxlgLaCWWH/NFZEilAAzzT75YnpKsjctwXTQ/Eylwb3gbQbpVIuAj6XobnJAwl/eqkrJ2UnMPPwmhS6ZmQofJ+GXppRJE1Aey+tppYSUS1lQypXiwQonoBf6b5nVc1IBi+piVYSUx1lLyJdicQonJ+aQjSRJjDKKiuXPnYTJS1qQipppmQofJ+GXpVkJc1IBy+tpVYTUx1lgippiu91yo0fP9iIS2bQC7Bg9h/4RqJc3ijXVtu5G5p+sFF4Q+5oaqXYpHEDV8tDBbKnlTe0im5ObmC5k4Tlaxv3axEcHsyLrK7ky5uyVRNbsqtDCDLpJ1WQaRcUarhsDi5TW17Alh6gMG4QHIUyL5Tcfy9R1990M8DCzak0eWnkcyxmi2dzBwmUzqewGDBT7CVN9HT9apvX5upfvL1vTuq9PNwK8NUHSVPNERypvfyef2Zy3BKZzZRT7hbcna+SMmijaqxV7Mhtow+Bve4DGSZpgiIhAKk18KEhC1Nx4xAXQf4ARvXZwi43rcO7xqk8uuUdP%3D%2Cundefined%22%7D%5D; user-finger=6a422ca24ce4fd2a38dc3c9e4de2f993; LG_LOGIN_USER_ID=9060927b21f1a9868d48ba4c87300d6802e17b2adaa99e5c; _putrc=34C749CE011C29AB; login=true; unick=%E9%9F%A9%E5%86%AC%E5%86%AC; kw_login_authToken="Xh1+W88WAOV8rd+JOPx5/hNeelYZhGY/FpnprW1M2QqemLQC3y1IpLKllTgbv4jUDSG0kYi70693R7xF4cr3zLwxJJGvRT0AYxFHA2jr6yfyQT9cH5x7NUquAJolzJ/72ElYYPFhgBj2Y2pGD8dXYUdYnTFcL706fx893D9KqW94rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; gate_login_token=056a5a7d3dd1ea78216c37750f93a583709766340f709bde; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229862931%22%2C%22%24device_id%22%3A%22168e171fe80a1e-07f627ced1772c-9393265-2073600-168e171fe8131c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22baidujava%22%2C%22%24latest_utm_medium%22%3A%22sspc%22%2C%22%24latest_utm_term%22%3A%22java3224%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2286.0.4240.75%22%7D%2C%22first_id%22%3A%221769215222b7bb-0adb10abac1072-c781f38-1327104-1769215222ca3a%22%7D; JSESSIONID=246955E517423765BE9BF105A0296147'
}


class Spider(object):

    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.semaphore = asyncio.Semaphore(CONCURRENCY)

    def scrape_lession_content(self, url):
        url = url.format(id=COURSE_ID)
        logging.info('scraping %s', url)
        param = {'courseId': COURSE_ID}
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
        template = env.get_template('template.html')

        if data:
            xlsx_path = os.getcwd() + file_path
            if not os.path.exists(xlsx_path):
                os.makedirs(xlsx_path)
            with open(xlsx_path + '/' + file_name, 'w+', encoding='utf-8') as fout:
                html_content = template.render(theme=theme, body=data)
                fout.write(html_content)

    async def main(self):
        response = self.scrape_lession_content(LESSION_URL)
        course_section_list = response['content']['courseSectionList']
        lession_id = []
        file_path = response['content']['courseName']
        for course in course_section_list:
            for lession in course['courseLessons']:
                lession_id.append(lession['id'])
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

        scrape_detail_tasks = [asyncio.ensure_future(self.write_html(str(content['id']) + '.html',
                                                                     content['theme'], content['content'],
                                                                     '/' + file_path))
                               for content in contents]
        await asyncio.wait(scrape_detail_tasks)
        await self.session.close()


if __name__ == '__main__':
    spider = Spider()
    loop.run_until_complete(spider.main())
