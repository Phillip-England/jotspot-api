import os
import json

import requests


class TestInstance:

    def __init__(
        self,
        session,
        method,
        url,
        test_count,
        purpose,
        status_code_expected,
        data,
        pre_execution_callback,
        post_execution_callback
    ):
        self.session = session
        self.method = method
        self.url = url
        self.test_count = test_count
        self.purpose = purpose
        self.status_code_expected = status_code_expected
        self.response = None
        self.data = json.dumps(data) if data != None else None
        self.headers = {"Content-Type": "application/json"}
        self.pre_execution_callback = pre_execution_callback
        self.post_execution_callback = post_execution_callback

    def run(self):
        if self.pre_execution_callback != None:
            self.pre_execution_callback.outcome = self.pre_execution_callback.func()
        if self.method == "DELETE":
            self.run_delete()
        if self.method == "POST":
            self.run_post()
        if self.method == "GET":
            self.run_get()
        if self.post_execution_callback != None:
            self.post_execution_callback.outcome = self.post_execution_callback.func()

    def run_delete(self):
        self.response = self.session.delete(self.url)

    def run_post(self):
        self.response = self.session.post(
            self.url, data=self.data, headers=self.headers)

    def run_get(self):
        self.response = self.session.get(self.url)


class InjectedFunction:

    def __init__(self, func, expected_result, purpose, outcome=None):
        self.func = func
        self.expected_result = expected_result
        self.purpose = purpose
        self.outcome = outcome


class TestUnit:

    def __init__(self, session, method, path, description, print_results):
        self.env = os.getenv("ENV")
        self.dev_url = os.getenv("DEV_URL")
        self.prod_url = os.getenv("PROD_URL")
        self.session = session
        self.url = self.dev_url + path if self.env == 'dev' else self.prod_url + path
        self.method = method.upper()
        self.description = description.upper()
        self.print_results = print_results
        self.tests = []
        self.color_codes = {
            "red": "\033[0;31m",
            "purple": "\033[0;35m",
            "blue": "\033[0;34m",
            "yellow": "\033[0;33m",
            "orange": "\033[0;33m",
            "black": "\033[0;30m",
            "white": "\033[0;37m",
            "green": "\033[0;32m"
        }

    def build_test(self, purpose, status_code_expected, data=None, empty_session=False, pre_execution_callback=None, post_execution_callback=None):
        instance = TestInstance(
            session=self.session if empty_session == False else requests.Session(),
            method=self.method,
            url=self.url,
            test_count=len(self.tests)+1,
            purpose=purpose,
            status_code_expected=status_code_expected,
            data=data,
            pre_execution_callback=pre_execution_callback,
            post_execution_callback=post_execution_callback
        )
        self.tests.append(instance)

    def inject_function(self, func, expected_result, purpose):
        return InjectedFunction(func, expected_result, purpose)

    def print_color(self, color, text):
        print(f'{color}{text}{self.color_codes["white"]}')

    def print_intro(self):
        print('')
        self.print_color(
            self.color_codes['blue'], "=======================================")
        print(self.description)
        self.print_color(
            self.color_codes['blue'], '---------------------------------------')

    def print_response(self, test_instance):
        self.print_color(self.color_codes['green'] if test_instance.response.status_code == test_instance.status_code_expected else self.color_codes['red'],
                         f'  request result - {"pass" if test_instance.response.status_code == test_instance.status_code_expected else "fail"}')
        print(f'  expected status code - {test_instance.status_code_expected}')
        print(f'  actual status code - {test_instance.response.status_code}')
        print(f'  json response - {test_instance.response.json()}')
        if test_instance.pre_execution_callback != None:
            print(
                f'  pre callback purpose - {test_instance.pre_execution_callback.purpose}')
            self.print_color(self.color_codes['green'] if test_instance.pre_execution_callback.outcome == test_instance.pre_execution_callback.expected_result else self.color_codes['red'],
                             f'  pre callback result - {"pass" if test_instance.pre_execution_callback.outcome == test_instance.pre_execution_callback.expected_result else "fail"}')
        if test_instance.post_execution_callback != None:
            print(
                f'  post callback purpose - {test_instance.post_execution_callback.purpose}')
            self.print_color(self.color_codes['green'] if test_instance.post_execution_callback.outcome == test_instance.post_execution_callback.expected_result else self.color_codes['red'],
                             f'  post callback result - {"pass" if test_instance.post_execution_callback.outcome == test_instance.post_execution_callback.expected_result else "fail"}')
        self.print_color(
            self.color_codes['blue'], '---------------------------------------')

    def print_test_intro(self, test_instance):
        print(f"Request #{test_instance.test_count}")
        print(f'  purpose - {test_instance.purpose}')
        if test_instance.data != None:
            print(f'  request data - {test_instance.data}')

    def run_tests(self):
        if self.print_results:
            self.print_intro()
        for test in self.tests:
            if self.print_results:
                self.print_test_intro(test)
            test.run()
            if self.print_results:
                self.print_response(test)

    def drop_tests(self):
        self.tests = []
