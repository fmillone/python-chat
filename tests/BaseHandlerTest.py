from unittest.mock import Mock, MagicMock


class BaseHandlerTest:
    def setup(self):
        self.app = Mock()
        self.app.ui_methods = MagicMock(return_value={})
        self.request = Mock()

    def cleanup(self):
        self.app = None
        self.request = None
        self.handler = None
