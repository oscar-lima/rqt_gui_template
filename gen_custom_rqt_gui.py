#!/usr/bin/env python3

'''
script to automate the creation of gui's in ROS1
'''

import os
import yaml
import stat
from jinja2 import Environment, FileSystemLoader

def read_yaml(yaml_path):
    with open(yaml_path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return

def get_param(param_name):
    if param_name in params_dic:
        return params_dic[param_name]
    else:
        print(f'error: param {param_name} not found in config.yaml')
        exit(0)

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def create_folders(root_folder, folder_names):
    print(f'creating folders: {folder_names}')
    create_folder(f'{root_folder}')
    for folder in folder_names:
        create_folder(f'{root_folder}/{folder}')

def create_files_from_template(root_folder, template_names, file_names, context):
    env = Environment(loader=FileSystemLoader('.'))

    for template_name, file_name in zip(template_names, file_names):
        template = env.get_template(template_name)
        file_path = os.path.join(root_folder, file_name)
        with open(file_path, 'w') as f:
            f.write(template.render(context))

# read parameters from yaml file
params_dic = read_yaml('config.yaml')

if not params_dic:
    print(f'error while reading config.yaml params, program will exit')
    exit(0)

new_rqt_name = get_param('new_rqt_name')
class_name = get_param('class_name')
author_mail = get_param('author_mail')
author_name = get_param('author_name')
description = get_param('description')
license = get_param('license')
category = get_param('category')

root_folder = f'../{new_rqt_name}'
template_names = ['CMakeLists.txt',
                  'package.xml',
                  'plugin.xml',
                  'jinja_readme.txt',
                  'setup.py',
                  'config/rqt_gui_template.ui',
                  'launch/rqt_gui_template.launch',
                  'scripts/rqt_gui_template_node',
                  'src/rqt_gui_template/__init__.py',
                  'src/rqt_gui_template/rqt_gui_template.py']

# list of file names to be created
new_file_names = ['CMakeLists.txt',
                  'package.xml',
                  'plugin.xml',
                  'README.md',
                  'setup.py',
                  f'config/{new_rqt_name}.ui',
                  f'launch/{new_rqt_name}.launch',
                  f'scripts/{new_rqt_name}_node',
                  f'src/{new_rqt_name}/__init__.py',
                  f'src/{new_rqt_name}/{new_rqt_name}.py']

# dictionary of jinja variables to be replaced
context = {'rqt_gui_template': new_rqt_name,
           'author_mail': author_mail,
           'author_name': author_name,
           'description': description,
           'license': license,
           'class_name': class_name,
           'category': category }

# print msg to signal start of pkg creation
print(f'Making pkg: {new_rqt_name}\n===')

# creating the folders
folders = ['config', 'launch', 'scripts', f'src/{new_rqt_name}']
create_folders(root_folder, folders)

# creating files from template
print(f'creating files : {new_file_names}')
create_files_from_template(root_folder, template_names, new_file_names, context)

# make node executable
print(f'making node {new_rqt_name}_node executable')
node_path = f'../{new_rqt_name}/scripts/{new_rqt_name}_node'
st = os.stat(node_path)
os.chmod(node_path, st.st_mode | stat.S_IEXEC)

print(f'===\nDone, your pkg can be found under: ../{new_rqt_name}')
