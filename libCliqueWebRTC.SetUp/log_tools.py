class Logger(object):
    """logger class"""
    def __init__(self):
        pass

    def report(self, _header_text, _string_text, **kwargs):
        print("{0} {1}".format(_header_text, _string_text))

    def info(self, _string_text, **kwargs):
        self.report("[ INFO  ]", _string_text)
        pass

    def error(self, _string_text="", **kwargs):
        self.report("[FAILURE]", _string_text)
        pass

    def success(self, _string_text="", **kwargs):
        self.report("[SUCCESS]", _string_text)
        pass




