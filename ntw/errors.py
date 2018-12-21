# _*_ coding: utf-8 _*_
__author__ = 'leo'
__date__ = '2018/12/3 15:53'

class TestError(Exception):
    def __init___(self, msg, context_args):
        Exception.__init__(self, "{0} {1}".format(msg, context_args))