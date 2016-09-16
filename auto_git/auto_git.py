# author: Tyrion
# created: 2016/8/31
# last modified: 
# encoding: utf-8
# Description: an auto git tool ,it can modify the readme, add and commit

import os
import shutil
import codecs

# get filename from source folder according to problem id
def get_filename(source_folder, problem_id):
    for filename in os.listdir(source_folder):
        if filename.split('.')[0].split('_')[-1] == problem_id:
            return filename


# modify readme file, add problem info
def modify_readme(source_folder, destination_folder, filename, relative_folder, readme_file):
    shutil.copy('/'.join([source_folder, filename]), '/'.join([destination_folder, filename]))
    file_handler = codecs.open('/'.join([source_folder, filename]), 'r', 'utf-8')
    lines = file_handler.readlines()
    file_handler.close()

    file_handler = codecs.open(readme_file, 'a+', 'utf-8')
    content = []
    id = lines[2].split(':')[1][1:-1]
    content.append(''.join(['|', id]))

    name = lines[1].split(':')[1][1:-1]
    source = lines[0].split(' ')[-1][:-1]
    content.append("".join(['[', name, '](', source, ')']))
    language = filename.split('.')[-1].upper()

    position = '/'.join([relative_folder, filename])
    content.append(''.join([' [', language,'](', position, ')']))

    difficulty = lines[3].split(':')[1][1:-1]
    content.append(''.join([difficulty, '|\n']))

    file_handler.write('|'.join(content))
    file_handler.close()

#git add commit push
def git_commit(git_folder, filename):
    os.chdir(git_folder)
    os.system("git add ./")
    os.system(''.join(['git commit -m "add file: ', filename, '"']))