# author: Tyrion
# created: 2016/8/30
# last modified: 2016/8/30
# encoding: utf-8
# Description: this file crawl the leetcode page, and extract the needed info to build a source code file header

import time

from lxml import etree
from urllib import request
import codecs

line = 90  # the char that a line can put


# crawl a leetcode problem html
def crawl_html(url):
    response = request.urlopen(url)
    content_bytes = response.read().decode("utf-8")
    content = etree.HTML(content_bytes)
    return content


# parse the html content and wirte the need content to source code file
def parse_content(url, content, folder, suffix):
    title = content.xpath("//div[@class='question-title clearfix']/h3/text()")[0]
    filename, name, id = generate_filename(title)
    difficulty = content.xpath("//div[@class='question-info text-info']/ul/li[3]/strong/text()")[0]
    file_handler = codecs.open(folder + '.'.join([filename, suffix]), 'w', "utf-8")
    write_first_part(file_handler, url, name, id,difficulty)
    write_second_part(file_handler, content)
    file_handler.close()


# generate filename, problem name problem id from the problem title
def generate_filename(title):
    values = title.split(' ')
    number = values[0][:-1]
    values = values[1:]
    name = " ".join(values)
    values.append(number)
    filename = '_'.join(values)
    return filename.lower(),name,number


# write the first part of the source code file, include source, author and date
def write_first_part(file_handler, url, name, id, difficulty):
    file_handler.write("".join(["// Source       : ", url, "\n"]))
    file_handler.write("".join(["// Problem name : ", name, "\n"]))
    file_handler.write("".join(["// Problem ID   : ", id, "\n"]))
    file_handler.write("".join(["// difficulty   : ", difficulty, "\n"]))
    file_handler.write("// Author       : Tyrion\n")
    date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    file_handler.write("".join(["// Date         : ", date, "\n\n"]))


# write the description of the problem
def write_second_part(file_handler, content):
    file_handler.write(''.join(["/", '*' * (line - 3), '\n']))
    vals = " ".join(content.xpath("//div[@class='question-content']/*/text()"))
    values = vals.split("\r\n")
    for val in values:
        val = val.strip(" \r\n\t")
        if len(val) == 0 or "Special thanks" in val:
            continue
        res = format_val(val)
        file_handler.write(res)
    file_handler.write(''.join([" ", '*' * (line - 3), '/\n\n']))

    file_handler.write(''.join(["/", '*' * (line - 3), '\n']))
    file_handler.write(" * \n * solution:\n")
    file_handler.write(''.join([" ", '*' * (line - 3), '/\n\n']))
    file_handler.close()

# format single paragraph
def format_val(val):
    val = ''.join([" * ", val])
    i = line - 1
    while i < len(val):
        if i == len(val) - 1:
            val = "".join([val, "\n * \n"])
        while val[i] != ' ':
            i -= 1
        val = "".join([val[:i], "\n * ", val[i + 1:]])
        i += line-1
    val = ''.join([val, "\n * \n"])
    return val
