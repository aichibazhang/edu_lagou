import os
from functools import cmp_to_key
from multiprocessing.dummy import Pool

import pdfkit


class HtmlToPdf(object):
    def __init__(self):
        self.html_dir = os.path.dirname(os.path.realpath(__file__))
        self.options = {
            'header-html': 'header.htm',
        }

    def get_html_dir(self):
        dir_list = []
        for home, dirs, files in os.walk(self.html_dir):
            # 获得所有文件夹
            for dirname in dirs:
                dir_names = os.path.join(home, dirname)
                dir_flag = '未更新完' in dir_names or '已更新完' in dir_names
                if dir_flag:
                    dir_list.append(dir_names)
        return dir_list

    @classmethod
    def get_html(cls, html_path):
        fileNames = []
        for root, ds, fs in os.walk(html_path):
            for f in fs:
                if '.html' in f:
                    fileNames.append(root + '\\' + f)
        return fileNames

    # def html_pdf(self, html_path,dir_paths):
    def html_pdf(self, html_path):
        str1 = os.path.realpath(html_path)
        str2 = '\\'
        pdf_path = str1[str1.rindex(str2) + 1:]
        # for pdf_path in dir_paths:
        if pdf_path != '已更新完' and pdf_path != '未更新完':
            html_files = self.get_html(html_path)
            file_name = 'pdf/' + pdf_path + '.pdf'
            print(file_name)
            if os.path.exists(file_name):
                os.remove(file_name)
            htmls = sorted(html_files, key=lambda x: int(str.split(os.path.split(x)[1], '.')[0]))
            try:
                pdfkit.from_file(htmls, file_name, options=self.options, cover='statement.htm', cover_first=True)
            except IOError:
                print("Error: 获取部分网页失败")


if __name__ == '__main__':
    html_to_pdf = HtmlToPdf()
    dir_list = html_to_pdf.get_html_dir()
    # pdf_paths=['专栏1','专栏2']
    for html_path in dir_list:
        html_to_pdf.html_pdf(html_path)
        # html_to_pdf.html_pdf(html_path,pdf_paths)
