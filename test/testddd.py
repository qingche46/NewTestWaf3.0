
import yaml
import os
import sqlite3
from ntw import ruleset
from glob import glob
import http.cookies

# def get_files(directory, extension):
#     """
#     Take a directory and an extension and return the files
#     that match the extension
#     """
#     return glob('%s/*.%s' % (directory, extension))
#
#
# def extract_yaml(yaml_files):
#     """
#     Take a list of yaml_files and load them to return back
#     to the testing program
#     """
#     loaded_yaml = []
#     for yaml_file in yaml_files:
#         try:
#             with open(yaml_file, 'r',encoding='utf-8') as fd:
#                 loaded_yaml.append(yaml.load(fd))
#         except IOError as e:
#             print('Error reading file', yaml_file)
#             raise e
#         except yaml.YAMLError as e:
#             print('Error parsing file', yaml_file)
#             raise e
#         except Exception as e:
#             print('General error')
#             raise e
#     return loaded_yaml
#
#
# def get_rulesets(ruledir, recurse):
#     """
#     List of ruleset objects extracted from the yaml directory
#     """
#     if os.path.isdir(ruledir) and recurse:
#         yaml_files = [y for x in os.walk(ruledir) for y in glob(os.path.join(x[0], '*.yaml'))]
#         # print(yaml_files)
#     elif os.path.isdir(ruledir) and not recurse:
#         yaml_files = get_files(ruledir, 'yaml')
#
#     elif os.path.isfile(ruledir):
#         yaml_files = [ruledir]
#
#
#     extracted_files = extract_yaml(yaml_files)
#
#     print(extracted_files)
#
# if __name__ == '__main__':
#     print(get_rulesets("D:\\Python\\NewTestWaf\\yaml",""))

import pytest
from ntw import ruleset
from ntw import util
import os


d = {'name':"Tom", 'age':10, 'Tel':110}
#打印返回值，其中d.keys()是列出字典所有的key
print ('name' in d.keys())
print ('name' in d)

