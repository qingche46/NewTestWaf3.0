# _*_ coding: utf-8 _*_
__author__ = 'leo'
__date__ = '2018/12/3 19:39'

import datetime
# from dateutil import parser
from ntw import errors
from ntw import httprun
import pytest
from ntw import ruleset
from ntw import util
import re
import sqlite3
# import allure

class TestRunner(object):
    """
    Runner that accepts stages of a test and verifies expected and actual
    responses
    @TODO
    Accept logger objects for assertions
    """

    def test_status(self, expected_status, actual_status):
        """
        Compares the expected output against actual output of test and stage
        In a separate function to make debugging easy with py.test
        """
        # assert expected_status == actual_status
        if expected_status == actual_status:
            print("actual_status=%s"%actual_status)
        else:
            print("actual_status=%s"%actual_status,"expected_status=%s"%expected_status)

    def test_log(self, lines, log_contains, negate):
        """
        Checks if a series of log lines contains a regex specified in the
        output stage. It will flag true on the first log_contains regex match
        and then assert on the flag at the end of the function
        """
        found = False
        for line in lines:
            if log_contains.search(line):
                found = True
                break
        if negate:
            assert not found
        else:
            assert found
        # print(log_contains)


    def test_response(self, response_object, regex):
        """
        Checks if the response response contains a regex specified in the
        output stage. It will assert that the regex is present.
        """
        if response_object is None:
            raise errors.TestError(
                'Searching before response received',
                {
                    'regex': regex,
                    'response_object': response_object,
                    'function': 'testrunner.TestRunner.test_response'
                })
        if regex.search(response_object):
            # raise errors.TestError("tongguo")
            assert True
            # raise (response_object)
            print(response_object)
        else:
            # print(response_object)
            # assert False
            raise errors.TestError(response_object)


        # b=re.compile(r'HTTP Error 400. The request is badly formed.')
        # a=b.search(response_object)
        # print a.group()



    def test_response_str(self, response, regex):
        """
        Checks if the response response contains a regex specified in the
        output stage. It will assert that the regex is present.
        """

        if regex.search(response):
            assert True
        else:
            assert False




    def run_stage(self, stage, logger_obj=None, http_ua=None):
        """
        Runs a stage in a test by building an httpua object with the stage
        input, waits for output then compares expected vs actual output
        http_ua can be passed in to persist cookies
        通过使用该阶段构建httpua对象，在测试中运行一个阶段
        输入，等待输出，然后比较预期和实际输出
        可以传入http_ua来持久化cookie
        """

        # Send our request (exceptions caught as needed)
        if stage.output.expect_error:
            with pytest.raises(errors.TestError) as excinfo:
                if not http_ua:
                    http_ua = httprun.HttpUA()
                start = datetime.datetime.now()
                http_ua.send_request(stage.input)

                end = datetime.datetime.now()
            print ('\nExpected Error: %s' % str(excinfo))
        else:
            if not http_ua:
                http_ua = httprun.HttpUA()
            start = datetime.datetime.now()
            http_ua.send_request(stage.input)
            end = datetime.datetime.now()
        if (stage.output.log_contains_str or stage.output.no_log_contains_str) \
        and logger_obj is not None:
            logger_obj.set_times(start, end)
            lines = logger_obj.get_logs()
            if stage.output.log_contains_str:
                self.test_log(lines, stage.output.log_contains_str, False)
            if stage.output.no_log_contains_str:
                # The last argument means that we should negate the resp
                self.test_log(lines, stage.output.no_log_contains_str, True)
        if stage.output.response_contains_str:
            self.test_response(http_ua.response_object.response,
                               stage.output.response_contains_str)
        if stage.output.status:
            self.test_status(stage.output.status,
                             http_ua.response_object.status)
            # print(http_ua.request_object.status)

