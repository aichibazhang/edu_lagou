import os
from functools import cmp_to_key

import pdfkit


def getAllSub(path):
    dir_list = []
    for home, dirs, files in os.walk(path):
        # 获得所有文件夹
        for dirname in dirs:
            dir_names = os.path.join(home, dirname)
            dir_flag = '.git' not in dir_names and '.idea' not in dir_names and 'venv' not in dir_names and 'login' not in dir_names and 'pdf' not in dir_names
            if dir_flag:
                dir_list.append(dir_names)
    return dir_list


def findAllHtmlFile(dir):
    fileNames = []
    for root, ds, fs in os.walk(dir):
        for f in fs:
            if '.html' in f:
                fileNames.append(root + '\\' + f)

    return fileNames


def file_cmp(file1, file2: str) -> int:
    if int(str.split(os.path.split(file1)[1], '.')[0]) > int(str.split(os.path.split(file2)[1], '.')[0]):
        return 1
    elif int(str.split(os.path.split(file1)[1], '.')[0]) > int(str.split(os.path.split(file2)[1], '.')[0]):
        return -1
    else:
        return 0


if __name__ == '__main__':
    options = {
        'header-html': 'header.htm',
    }
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    dir_list = getAllSub(parent_dir)
    for html_path in dir_list:
        html_files = findAllHtmlFile(html_path)
        file_name = html_path + '.pdf'
        if os.path.exists(file_name):
            os.remove(file_name)
        htmls = sorted(html_files, key=cmp_to_key(file_cmp))
        pdfkit.from_file(htmls, file_name, options=options, cover='statement.htm', cover_first=True)
