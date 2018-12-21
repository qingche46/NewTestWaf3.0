# _*_ coding: utf-8 _*_
__author__ = 'leo'
__date__ = '2018/12/6 9:25'
import pytest
from ntw import testrunner,errors,logchecker,httprun
from test.conftest import  pytest_addoption
import time



def test_default(ruleset, test, destaddr, port, protocol):
    """
    Default tester with no logger obj. Useful for HTML contains and Status code
    Not useful for testing loggers
    """
    runner = testrunner.TestRunner()
    try:
        for stage in test.stages:
            if destaddr is not None:
                stage.input.dest_addr = destaddr
            if port is not None:
                stage.input.port = port
            if protocol is not None:
                stage.input.protocol = protocol
            runner.run_stage(stage, None)
    except errors.TestError as e:
        e.args[1]['meta'] = ruleset.meta
        pytest.fail('Failure! Message -> {0}, Context -> {1}'
                        .format(e.args[0],e.args[1]))