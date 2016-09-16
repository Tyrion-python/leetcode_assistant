# author: Tyrion
# created: 2016/8/30
# last modified: 2016/8/30
# encoding: utf-8
# Description: ascript that user can run

import sys
import os
import codecs

import code_spider.code_spider as cs
import auto_git.auto_git as ag

if __name__ == "__main__":
    config_handler = codecs.open('config.txt', 'r', 'utf-8')
    kwargs = dict()
    lines = config_handler.readlines()
    config_handler.close()
    for line in lines:
        line = line.strip('\r\n\t')
        values = line.split('=')
        kwargs[values[0]] = values[1]
    print(kwargs)
    if sys.argv[1] == "create":
        content = cs.crawl_html(sys.argv[2])
        cs.parse_content(url=sys.argv[2], content=content, folder=kwargs['source_folder'], suffix=kwargs['language'])
    elif sys.argv[1] == 'commit':
        filename = ag.get_filename(kwargs['source_folder'], sys.argv[2])
        ag.modify_readme(kwargs['source_folder'], kwargs['destination_folder'], filename, kwargs['relative_folder'],
                         kwargs['readme_addr'])
        ag.git_commit(kwargs['git_folder'], filename)



# python script.py https://leetcode.com/problems/nim-game/
# python script.py create file:///C:/Users/Tyrion/Desktop/1.html ./ .c
# python script.py commit F:/Leetcode F:/git/leetcode/algorithms/c 319 ./algorithm/c F:/git/leetcode/readme.md F:/git/leetcode/
