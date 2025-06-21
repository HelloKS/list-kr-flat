#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import urllib.request
import datetime
import os

uBO_filter_URL = 'https://raw.githubusercontent.com/List-KR/List-KR/master/filter-uBlockOrigin.txt'

print("Filter update triggered at " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

with urllib.request.urlopen(uBO_filter_URL) as response:
    filter = response.read()
    header = ''
    sub_filters = []
   
    filter_lines = filter.decode('utf-8').splitlines()

    for line in filter_lines:
        if line.startswith('!#include'):
            sub_filters.append(line.split(" ")[1])
        elif line.startswith('! '):
            header += line + '\n'
            if "Version: " in line:
                with open('CHANGELOG.md', 'w', encoding="UTF-8") as f:
                    f.write("Updated at: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
                    f.write("Filter version: " + line.replace("! Version: ", "") + "\n")
                with open('VERSION', 'w', encoding="UTF-8") as f:
                    f.write(line.replace("! Version: ", ""))

    flattened_filter = header + '\n'

    for sub_filter in sub_filters:
        with urllib.request.urlopen('https://raw.githubusercontent.com/List-KR/List-KR/master/' + sub_filter) as response:
            sub_filter_content = response.read().decode('utf-8')
            flattened_filter += '!\n! Filter: ' + sub_filter + '\n!\n' + sub_filter_content + '\n'

    os.makedirs("./dist")

    with open('./dist/list-kr-flat.txt', 'w', encoding="UTF-8") as f:
       f.write(flattened_filter)
