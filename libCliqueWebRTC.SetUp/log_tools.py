class Logger(object):
    """logger class"""
    def __init__(self):
        pass

    def report(self, _header_text, _string_text, **kwargs):
        string = ""
        
        if kwargs.get("header") is not None and kwargs["header"] is True:
            string += _header_text
        
        string += " " + _string_text
        
        print( string,
               end = None if kwargs.get("end") is None else kwargs["end"],
               flush = None if kwargs.get("flush") is None else kwargs["flush"],
               )

    def info(self, _string_text, **kwargs):
        self.report("[ INFO  ]", _string_text, 
                    header = None if kwargs.get("header") is None else kwargs["header"],
                    end = None if kwargs.get("end") is None else kwargs["end"],
                    flush = None if kwargs.get("flush") is None else kwargs["flush"],
                    )
        pass

    def error(self, _string_text="", **kwargs):
        self.report("[FAILURE]", _string_text, 
                    header = None if kwargs.get("header") is None else kwargs["header"],
                    end = None if kwargs.get("end") is None else kwargs["end"],
                    flush = None if kwargs.get("flush") is None else kwargs["flush"],
                    )
        pass

    def success(self, _string_text="", **kwargs):
        self.report("[SUCCESS]", _string_text, 
                    header = None if kwargs.get("header") is None else kwargs["header"],
                    end = None if kwargs.get("end") is None else kwargs["end"],
                    flush = None if kwargs.get("flush") is None else kwargs["flush"],
                    )
        pass




