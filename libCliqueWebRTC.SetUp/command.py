import subprocess
import os
import log_tools
import shutil
import re

class ProgressBar(object):
    """progress bar class"""
    def __init__(self, width=10):
        self.width = width
        self.pos = 0
        self.eraser = str()
        for pos in range(0, self.width + 2):
            self.eraser += "\b"

    def cleanup(self):
        pass
        print(self.eraser, end="", flush=True)

    def display(self):
        bar = "["
        for _pos in range(0, self.width):
            if _pos == self.pos:
               bar += "*"
            else:
               bar += "-"
        else:
            bar += "]"

        if self.pos + 1 < self.width:
           self.pos = self.pos + 1
        else:
           self.pos = 0

        self.cleanup()

        print(bar, end="", flush=True)

def run(log, target, args=[], **kwargs):
    pipe = subprocess.PIPE
    
    cmd_str = target
    for arg in args:
        cmd_str += " " + arg

    cwd_str = os.getcwd()
    cwd = kwargs.get("cwd")
    if cwd is not None:
        cwd_str = cwd
    
    if "env" in kwargs:
        env = kwargs["env"]
    else:
        env = None

    log.info("Call \"{0}\"... ".format(cmd_str))

    proc = subprocess.Popen( cmd_str,
                             shell  = True,
                             stdin  = pipe,
                             stdout = pipe,
                             stderr = subprocess.STDOUT,
                             cwd    = cwd_str,
                             env    = env )
    
    result  = str()
    bar     = ProgressBar()

    loop = True
    while loop:
        line = proc.stdout.readline().decode('utf8', 'irnore')
        if len(line) == 0: 
            loop = False
            continue
        #sys.stdout.write(line)
        bar.display()
        result += line + "\r\n"
    else:
        bar.cleanup()
        pass

    log.info("Done.")

    return result

def git(context, cwd, args, result, **kwargs):
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()

    result = run(log, "git", args, env = None if context.get("environment") is None else context["environment"], cwd=cwd)

    return True

def b2(context, cwd, args, result, **kwargs):
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()
    
    if not os.path.isfile(cwd+"/b2.exe"):
        return False

    result = run(log, "b2", args, env = None if context.get("environment") is None else context["environment"], cwd=cwd)
    
    return True

def bootstrap(context, cwd, args, result, **kwargs):
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()

    if not os.path.isfile(cwd+"/bootstrap.bat"):
        return False

    result = run(log, "bootstrap.bat", args, env = None if context.get("environment") is None else context["environment"], cwd=cwd)
    
    return True

def copy(context, cwd, args, result, **kwargs):
    kwargs["keep"]=True
    return move(context, cwd, args, result, **kwargs)

def move(context, cwd, args, result, **kwargs):
    keep = kwargs["keep"] if kwargs.get("keep") is not None else False
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()

    log.info("... Coping files ...")

    # checking and parsing parameters
    parameters = parse_args(log, args, result)
    if parameters is None:
        return False
    
    keys = parameters.keys()
    if not ("src" in keys and "dst" in keys):
        result+="[move] lack of mandatory parameters"+"\n"
        return False

    # stripping quoted string    
    if parameters["src"][0] == "\"" and parameters["src"][-1] == "\"":
        parameters["src"] = parameters["src"][1:-1]
        parameters["src"] += "/" if not (parameters["src"].endswith("/") or parameters["src"].endswith("\\")) else ""
    if parameters["dst"][0] == "\"" and parameters["dst"][-1] == "\"":
        parameters["dst"] = parameters["dst"][1:-1]
        parameters["dst"] += "/" if not (parameters["dst"].endswith("/") or parameters["dst"].endswith("\\")) else ""
    if parameters.get("filter") is not None:
        if parameters["filter"][0] == "\"" and parameters["filter"][-1] == "\"":
            parameters["filter"] = parameters["filter"][1:-1]
    
    filters =[]
    if parameters.get("filter") is not None:
        filters = parameters["filter"].split(";")
    
    for cFilter in range(0, len(filters)):
        filters[cFilter] = filters[cFilter].replace("*","^[A-Za-z0-9_]*")
        filters[cFilter]+="$"

    source_dir = context["dependency_dir"]+parameters["src"]
    target_dir = context["dependency_dir"]+parameters["dst"]

    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    dir_items = os.listdir(source_dir)
    for dir_item in dir_items:
        if os.path.isfile(source_dir+dir_item):
            if len(filters) > 0:
                for filter in filters:
                    res = re.match(filter, dir_item)
                    if res is not None:
                        print(" ... Moving {0} from {1} to {2} ... ".format(dir_item, source_dir, target_dir))
                        shutil.move(source_dir+dir_item, target_dir+dir_item) if keep is False \
                            else shutil.copy(source_dir+dir_item, target_dir+dir_item)
                        break
                    pass
            else:
                print(" ... Moving {0} from {1} to {2} ... ".format(dir_item, source_dir, target_dir))
                shutil.move(source_dir+dir_item, target_dir+dir_item) if keep is False \
                    else shutil.copy(source_dir+dir_item, target_dir+dir_item)
                pass
            pass
        elif os.path.isdir(source_dir+dir_item):
            newparameters = parameters.copy()
            newparameters["src"]+=dir_item+"/"
            newparameters["dst"]+=dir_item+"/"
            newargs = []
            for param in newparameters:
                newargs.append("--{0}={1}".format(param, "\""+newparameters[param]+"\""))
            move(context, cwd, newargs, result, **kwargs)
            pass
    
    if not keep:
        shutil.rmtree(source_dir, ignore_errors=True, onerror=print("Error: Cannot remove source directory"))

    return True

def read_env_vars(context, cwd, args, result, **kwargs):
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()

    log.info("... Reading environment variables ...")

    if args is None or len(args) == 0:
        context["environment"] = os.environ.copy()
        return True
    else:
        arguments = "{0}".format(args[0])
        for arg in range(1, len(args)):
            arguments+=" {0}".format(args[arg])

    # if context is not dict
    if not isinstance(context, (dict)):
        print("{0}\n{1}".format(result, "ERROR: Context is not a dictionary"))
        return False

    if context.get("environment") is not None:
        print("{0}\n{1}".format(result, "ERROR: Context already has the \"environment\" key"))
        return False

    initial = None if kwargs.get("initial") is None else kwargs["initial"]

    # create a tag so we can tell in the output when the proc is done
    tag = "__DONE_RUNNING_COMMAND_B8E5CB44_F797_447D_9901_EDA32D03BFEE__"

    # construct a cmd.exe command to do accomplish this
    cmd = '/s /c "{arguments} && echo "{tag}" && set"'.format(**vars())

    # launch the process
    result = proc = run(log, "cmd.exe", [cmd], environment_variables=initial)

    # parse the output sent to stdout
    lines = proc.split("\r\n")
    
    environment_variables={}
    #remove all lines prior tag inclusive
    loop = True
    while loop:
        if tag in lines[0]:
            loop = False
        lines.remove(lines[0])
    
    for line in lines:
        pair = line.split("=")
        if len(pair) != 2:
            continue
        environment_variables[pair[0]]=pair[1]

    if context.get("environment") is None:
        context["environment"] = environment_variables
    
    return True

def perl(context, cwd, args, result, **kwargs):
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()
    
    result = run(log, "perl", args, env = None if context.get("environment") is None else context["environment"], cwd=cwd)
    
    return True

def cmd(context, cwd, args, result, **kwargs):
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()

    for arg in range(0, len(args)):
        if args[arg].endswith(".bat") and not os.path.isabs(args[arg]):
            args[arg] = context["dependency_dir"]+args[arg]
    
    result = run(log, "cmd", args, env = None if context.get("environment") is None else context["environment"], cwd=cwd)
    
    return True

def parse_args(log, args, result):
    
    def strip_arg(arg):
        arg = arg[2:]
        res = arg.split("=")
        return res[0], res[1]

    parameters = {}
    for arg in args:
        match = re.match("^--filter=", arg)
        if match is not None:
            key, val = strip_arg(arg)
            parameters[key] = val
            continue
        match = re.match("^--[A-Za-z_0-9\-]*=[A-Za-z_0-9/#\"\-\:\s\.\(\)]*$", arg)
        if match is not None and match.group() == arg:
            key, val = strip_arg(arg)
            parameters[key] = val
        else:
            result+="[update_environment_variable] The \"{0}\" parameter is invalid".format(arg)+"\n"
            return None

    return parameters

def update_environment_variable(context, cwd, args, result, **kwargs):
    # strinpping logger
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()

    # reporting the command short description
    log.info("... Updating environment variables ...")

    # checking context exists
    if context.get("environment") is None:
        return False

    # checking and parsing parameters
    parameters = parse_args(log, args, result)
    if parameters is None:
        return False
    if sorted(parameters.keys()) != sorted(["variable", "action", "value"]):
        result+="[update_environment_variable] invalid parameters set"+"\n"
        return False
    # stripping quoted string    
    if parameters["value"][0] == "\"" and parameters["value"][-1] == "\"":
        parameters["value"] = parameters["value"][1:-1]
    
    # checking if target environment variable present in the list
    
    variable_key = None
    for key in context["environment"]:
        if key.upper() ==  parameters["variable"].upper():
            variable_key = key
            break
    if variable_key is None:
        return False
    
    # check if the value already exist
    value = parameters["value"] if not parameters["value"].endswith("/") and not parameters["value"].endswith("\\") \
                                else parameters["value"][:-1]

    if value in context["environment"][variable_key] \
        or value.replace("/", "\\") in context["environment"][variable_key] \
            or value.replace("\\", "/") in context["environment"][variable_key]:
        return True

    # executing certain action
    if parameters["action"] == "prepend":
        prepend = str()
        for item in args:
            prepend += item +";"
        context["environment"][variable_key] = prepend + context["environment"][variable_key]
    elif parameters["action"] == "append":
        if not context["environment"][variable_key].endswith(";"):
            context["environment"][variable_key] +=";"
        context["environment"][variable_key] += parameters["value"]
        if not context["environment"][variable_key].endswith(";"):
            context["environment"][variable_key] +=";"
    
    return True

def edit_file(context, cwd, args, result, **kwargs):
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()

    log.info("... Editing file ...")

    parameters = parse_args(log, args, result)
    
    if parameters is None:
        return False

    if sorted(parameters.keys()) != sorted(["file", "action", "string"]):
        result+="[edit_file] invalid parameters set"+"\n"
        return False

    if parameters["string"][0] == "\"" and parameters["string"][-1] == "\"":
        parameters["string"] = parameters["string"][1:-1]

    in_file = open(context["dependency_dir"]+parameters["file"], "r")
    if in_file is None:
        return False

    out_file = open(context["dependency_dir"]+parameters["file"]+".tmp", "w")
    if out_file is None:
        return False

    while True:
        line = in_file.readline()
        if line == "":
            break
        elif parameters["string"] in line:
            continue
        else:
            out_file.write(line)

    in_file.close()
    out_file.close()

    os.remove(context["dependency_dir"]+parameters["file"])
    os.rename(context["dependency_dir"]+parameters["file"]+".tmp", context["dependency_dir"]+parameters["file"])

    return True

def cmake(context, cwd, args, result, **kwargs):
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()

    for arg in range(0, len(args)):
        if args[arg].endswith(".bat") and not os.path.isabs(args[arg]):
            args[arg] = context["dependency_dir"]+args[arg]
    
    result = run(log, "cmake", args, env = None if context.get("environment") is None else context["environment"], cwd=cwd)
    
    return True

def msbuild(context, cwd, args, result, **kwargs):
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()

    for arg in range(0, len(args)):
        if args[arg].endswith(".bat") and not os.path.isabs(args[arg]):
            args[arg] = context["dependency_dir"]+args[arg]
    
    result = run(log, "msbuild", args, env = None if context.get("environment") is None else context["environment"], cwd=cwd)
    if result.endswith("\n"):
        result = result[:-1]
    result = result.replace("\r", "");
    result_lines = result.split("\n");
    
    if "\'msbuild\' is not recognized as an internal or external command," in result_lines[0]:
        return False

    return True
