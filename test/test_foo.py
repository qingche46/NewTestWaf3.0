# _*_ coding: utf-8 _*_
__author__ = 'leo'
__date__ = '2018/12/3 19:26'

import pytest
from ntw import testrunner,errors,logchecker,httprun
from test.conftest import  pytest_addoption
import time

def test_bar(ruleset,test):
    runner = testrunner.TestRunner()
    for stage in test.stages:
        runner.run_stage(stage)
        time.sleep(4)

