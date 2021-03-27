# 概述
拉钩专栏 vip 账号爬取相关专栏
# 使用方式
1. 登陆拉钩教育
2. 复制登陆成功后的 cookies
3. 爬取：

   3.1 一键订阅：运行`crawl/crawl_list.py` 订阅并记录需要下载的专栏id到`downloads.txt` 文件中
   3.2 全量爬取：运行`crawl/crawl_content.py` 中 `spider.crawl_all()` 方法
   3.3 增量爬取：运行`crawl/crawl_content.py` 中 `spider.cral_increase()`方法   
   3.4 转换为 pdf：运行`htmltopdf.py`
# 项目说明
1. 第一次运行使用全量爬取，后续如果拉钩更新，项目会记录未下载和未更新完的专栏。
2. 增量更新为未更新专栏的更新功能
3. 目前需要手动在百度云网盘维护 pdf
4. 增量更新时需要观看日志，并修改转换pdf文件夹，`pdf_paths = []`根据日志中更新的id,通过查看
`https://kaiwu.lagou.com/course/courseInfo.htm?courseId=#{id}`并修改更新id到需要更新的文件夹中
# 项目完成度
- [x] 爬取拉勾课程
- [x] 生成pdf
- [x] 一键获取所有vip专栏订阅
- [x] 一键下载所有专栏
- [x] 多线程爬取专栏 
- [x] 全量爬取专栏
- [x] 增量爬取专栏
- [x] 更新未更新完得专栏并记录由未更新完变为更新完的专栏
# 项目运行示例
![动态演示](https://video-aiqiyi-1253626516.cos.ap-beijing.myqcloud.com/edu.gif)

