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

    @classmethod
    def file_cmp(cls, file1, file2: str) -> int:
        if int(str.split(os.path.split(file1)[1], '.')[0]) > int(str.split(os.path.split(file2)[1], '.')[0]):
            return 1
        elif int(str.split(os.path.split(file1)[1], '.')[0]) > int(str.split(os.path.split(file2)[1], '.')[0]):
            return -1
        else:
            return 0

    def html_pdf(self, html_path):
        str1 = os.path.realpath(html_path)
        str2 = '\\'
        pdf_path = str1[str1.rindex(str2) + 1:]
        if pdf_path != '已更新完' and pdf_path != '未更新完':
            html_files = self.get_html(html_path)
            file_name = 'pdf/' + pdf_path + '.pdf'
            print(file_name)
            if os.path.exists(file_name):
                os.remove(file_name)
            htmls = sorted(html_files, key=cmp_to_key(self.file_cmp))
            pdfkit.from_file(htmls, file_name, options=self.options, cover='statement.htm', cover_first=True)


if __name__ == '__main__':
    html_to_pdf = HtmlToPdf()
    dir_list = html_to_pdf.get_html_dir()
    for html_path in dir_list:
        html_to_pdf.html_pdf(html_path)
