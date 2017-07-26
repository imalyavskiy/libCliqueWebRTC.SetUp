class Logger(object):
    """logger class"""
    def __init__(self):
        pass

    def report(self, _header, _string):
        print("{0} {1}".format(_header, _string))
        pass

    def info(self, _string):
        self.report("[ INFO  ]", _string)
        pass

    def error(self, _string=""):
        self.report("[FAILURE]", _string)
        pass

    def success(self, string=""):
        self.report("[SUCCESS]", string)
        pass




