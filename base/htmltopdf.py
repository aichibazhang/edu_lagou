import os
from functools import cmp_to_key

import pdfkit


def findAllHtmlFile(dir):
    fileNames = []
    for root, ds, fs in os.walk(dir):
        for f in fs:
            if '.html' in f:
                fileNames.append(f)

    return fileNames


def file_cmp(file1, file2: str) -> int:
    if int(str.split(file1, '.')[0]) > int(str.split(file2, '.')[0]):
        return 1
    elif int(str.split(file1, '.')[0]) < int(str.split(file2, '.')[0]):
        return -1
    else:
        return 0


if __name__ == '__main__':
    options = {
        'header-html': 'header.htm',
        'footer-spacing': 10,
        'header-spacing': 10,
        'default-header': '',
        'minimum-font-size': 28,
        'footer-line': '',
        'header-line': ''
    }
    html_files = findAllHtmlFile(os.getcwd())
    file_name = os.path.basename(os.getcwd()) + '.pdf'
    htmls = sorted(html_files, key=cmp_to_key(file_cmp))
    pdfkit.from_file(htmls, file_name, options=options, cover='statement.htm', cover_first=True)
