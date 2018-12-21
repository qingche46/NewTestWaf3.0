# _*_ coding: utf-8 _*_
__author__ = 'leo'
__date__ = '2018/12/3 15:21'
#
# from __future__ import print_function

import yaml
import os
import sqlite3
from ntw import ruleset
from glob import glob




def get_files(directory, extension):
    """
    Take a directory and an extension and return the files
    that match the extension
    """
    return glob('%s/*.%s' % (directory, extension))


def extract_yaml(yaml_files):
    """
    Take a list of yaml_files and load them to return back
    to the testing program
    """
    loaded_yaml = []
    for yaml_file in yaml_files:
        try:
            #修改1：python3使用encoding='utf-8'打开yaml
            with open(yaml_file, 'r',encoding='utf-8') as fd:
                loaded_yaml.append(yaml.load(fd))
        except IOError as e:
            print('Error reading file', yaml_file)
            raise e
        except yaml.YAMLError as e:
            print('Error parsing file', yaml_file)
            raise e
        except Exception as e:
            print('General error')
            raise e
    return loaded_yaml


def get_rulesets(ruledir, recurse):
    """
    List of ruleset objects extracted from the yaml directory
    """
    if os.path.isdir(ruledir) and recurse:
        yaml_files = [y for x in os.walk(ruledir) for y in glob(os.path.join(x[0], '*.yaml'))]
        # print(yaml_files)
    elif os.path.isdir(ruledir) and not recurse:
        yaml_files = get_files(ruledir, 'yaml')

    elif os.path.isfile(ruledir):
        yaml_files = [ruledir]


    extracted_files = extract_yaml(yaml_files)
    rulesets = []
    for extracted_yaml in extracted_files:
        rulesets.append(ruleset.Ruleset(extracted_yaml))
    return rulesets


# if __name__ == '__main__':
#     get_rulesets("D:\\Python\\NewTestWaf\\yaml\\","")