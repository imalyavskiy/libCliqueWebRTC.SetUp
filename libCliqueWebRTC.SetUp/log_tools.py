import datetime

class Logger(object):
    """logger class"""
    def __init__(self, log_file_dir = "", log_file_name = ""):
        self.log_file_name = log_file_name
        self.log_file_dir = log_file_dir
        self.log_file = None
        if len(self.log_file_dir) > 0 and len(self.log_file_name) > 0:
            now = datetime.datetime.now()
            # [path][name]_[day][month][year]\[[hour].[minute].[second]\].log
            self.log_file = open(
                 "{0}{1}_{2}{3}{4}[{5}.{6}.{7}].log".format(self.log_file_dir, self.log_file_name, now.day, now.month, now.year, now.hour, now.minute, now.second), #filepath
                 "w",                                                                                                                                               #open mode
                 1                                                                                                                                                  #buffering policy - one line
                 )
        pass

    def __del__(self):
        self.log_file.close()
        pass

    def report(self, _header_text, _string_text, **kwargs):
        hide = False if kwargs.get("hide") is None or kwargs["hide"] == False else True

        if hide is False:
            print("{0} {1}".format(_header_text, _string_text))
        
        if self.log_file is not None:
            self.log_file.write("{0} {1}".format(_header_text, _string_text) + "\n" if not _string_text.endswith("\n") else "")

    def info(self, _string_text, **kwargs):
        self.report("[ INFO  ]", _string_text)
        pass

    def error(self, _string_text="", **kwargs):
        self.report("[FAILURE]", _string_text)
        pass

    def success(self, _string_text="", **kwargs):
        self.report("[SUCCESS]", _string_text)
        pass
