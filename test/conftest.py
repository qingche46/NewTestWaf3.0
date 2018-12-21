# _*_ coding: utf-8 _*_
__author__ = 'leo'
__date__ = '2018/12/3 19:23'


import sys




import pytest
from ntw import ruleset
from ntw import util
import os


def get_testdata(rulesets):
    """
    In order to do test-level parametrization (is this a word?), we have to
    bundle the test data from rulesets into tuples so py.test can understand
    how to run tests across the whole suite of rulesets
    """
    testdata = []
    for ruleset in rulesets:
        for test in ruleset.tests:
            if test.enabled:
                testdata.append((ruleset, test))

    return testdata

def test_id(val):
    """
    Dynamically names tests, useful for when we are running dozens to hundreds
    of tests
    """
    if isinstance(val, (dict,ruleset.Test)):
        # We must be carful here because errors are swallowed and defaults returned
        if 'name' in val.ruleset_meta.keys():
            #修改9：新增pytest-html报告的payload的uri显示
            if "uri" in val.test_dict["stages"][0]["stage"]["input"]:
                uri=val.test_dict["stages"][0]["stage"]["input"]["uri"]
            else:
                uri="post or upload"
            return '-- %s -- %s--%s--Payload_uri:::::%s ' % (val.ruleset_meta['name'],val.test_title,val.ruleset_meta["description"],uri)
        else:
            return '-- %s -- %s -- %s' % ("Unnamed_Test",val.test_title, val.ruleset_meta["description"])


@pytest.fixture
def destaddr(request):
    """
    Destination address override for tests
    """
    return request.config.getoption('--destaddr')

@pytest.fixture
def port(request):
    """
    Destination port override for tests
    """

    return request.config.getoption('--port')

@pytest.fixture
def protocol(request):
    """
    Destination protocol override for tests
    """

    return request.config.getoption('--protocol')

@pytest.fixture
def http_serv_obj():
    """
    Return an HTTP object listening on localhost port 80 for testing
    """
    return HTTPServer(('localhost', 80), SimpleHTTPRequestHandler)

@pytest.fixture
def with_journal(request):
    """
    Return full path of the testing journal
    """
    return request.config.getoption('--with-journal')

@pytest.fixture
def tablename(request):
    """
    Set table name for journaling
    """
    return request.config.getoption('--tablename')

def pytest_addoption(parser):
    """
    Adds command line options to py.test
    """
    parser.addoption('--ruledir', action='store', default=None,
        help='rule directory that holds YAML files for testing')
    parser.addoption('--destaddr', action='store', default=None,
        help='destination address to direct tests towards')
    parser.addoption('--rule', action='store', default=None,
        help='fully qualified path to one rule')
    parser.addoption('--ruledir_recurse', action='store', default=None,
        help='walk the directory structure finding YAML files')
    parser.addoption('--with-journal', action='store', default=None,
        help='pass in a journal database file to test')
    parser.addoption('--tablename', action='store', default=None,
        help='pass in a tablename to parse journal results')
    parser.addoption('--port', action='store', default=None,
        help='destination port to direct tests towards', choices=range(1,65536),
        type=int)
    parser.addoption('--protocol', action='store',default=None,
        help='destination protocol to direct tests towards', choices=['http','https'])

def pytest_generate_tests(metafunc):
    """
    Pre-test configurations, mostly used for parametrization
    """
    options = ['ruledir','ruledir_recurse','rule','port']
    args = metafunc.config.option.__dict__
    # Check if we have any arguments by creating a list of supplied args we want
    if [i for i in options if i in args and args[i] != None] :
        if metafunc.config.option.port:
            ruleset.Input.port=metafunc.config.option.port
            rulesets=ruleset.Input.port
        if metafunc.config.option.ruledir:
            rulesets = util.get_rulesets(metafunc.config.option.ruledir, False)
        if metafunc.config.option.ruledir_recurse:
            rulesets = util.get_rulesets(metafunc.config.option.ruledir_recurse, True)
        if metafunc.config.option.rule:
            rulesets = util.get_rulesets(metafunc.config.option.rule, False)
        if 'ruleset' in metafunc.fixturenames and 'test' in metafunc.fixturenames:
            metafunc.parametrize('ruleset,test', get_testdata(rulesets),
                ids=test_id)