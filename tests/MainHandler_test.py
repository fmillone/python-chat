from unittest.mock import Mock, MagicMock

from chat.handlers.MainHandler import MainHandler
from dateutil import parser
from tests.BaseHandlerTest import BaseHandlerTest
import re


def arg_should_contain(regex):
    def wrapper(arg):
        try:
            date = re.search(regex, arg)
            parser.parse(date.group(1))
        except (AttributeError, ValueError):
            raise Exception('invalid date format')

    return wrapper


class TestMainHandler(BaseHandlerTest):
    def setup(self):
        super().setup()
        self.handler = MainHandler(self.app, self.request)

    def test_should_return_a_message(self):
        # given
        self.setup()
        self.handler.write = arg_should_contain('Hello, world at (.*)')
        # when
        self.handler.get()
        # then
        # cleanup
        self.cleanup()
