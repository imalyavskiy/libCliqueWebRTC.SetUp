import subprocess
import os
import log_tools
import shutil
import re

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

    output = subprocess.Popen(cmd_str,
                                shell=True,
                                stdin=pipe,
                                stdout=pipe,
                                stderr=subprocess.STDOUT,
                                cwd=cwd_str,
                                env=env).stdout.read()
    log.info("Done.")

    return output.decode('utf8', 'ignore')

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
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()

    log.info("... Coping files ...")

    source_dir = context["dependency_dir"]+args[0]+"/"
    target_dir = context["dependency_dir"]+args[1]+"/"

    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    files = os.listdir(source_dir)
    for file in files:
        print(" ... Moving {0} from {1} to {2} ... ".format(file, source_dir, target_dir))
        shutil.move(source_dir+file, target_dir+file)

    os.rmdir(source_dir)

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

def args_parser(log, args, result):
    
    def strip_arg(arg):
        arg = arg[2:]
        res = arg.split("=")
        return res[0], res[1]

    parameters = {}
    for arg in args:
        match = re.match("^--[A-Za-z_0-9\-]*=[A-Za-z_0-9/#\"\-\:\s\.\(\)]*$", arg)
        if match is not None and match.group() == arg:
            key, val = strip_arg(arg)
            parameters[key] = val
        else:
            result+="[update_environment_variable] The \"{0}\" parameter is invalid".format(arg)+"\n"
            return None

    return parameters

def update_environment_variable(context, cwd, args, result, **kwargs):
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()

    log.info("... Updating environment variables ...")

    if context.get("environment") is None:
        return False

    parameters = args_parser(log, args, result)
    
    if parameters is None:
        return False

    if sorted(parameters.keys()) != sorted(["variable", "action", "value"]):
        result+="[update_environment_variable] invalid parameters set"+"\n"
        return False
    
    if parameters["value"][0] == "\"" and parameters["value"][-1] == "\"":
        parameters["value"] = parameters["value"][1:-1]

    if context["environment"].get(parameters["variable"]) is None:
        return False
    
    if parameters["action"] == "prepend":
        prepend = str()
        for item in args:
            prepend += item +";"
        context["environment"][parameters["variable"]] = prepend + context["environment"][parameters["variable"]]
    elif parameters["action"] == "append":
        if not context["environment"][parameters["variable"]].endswith(";"):
            context["environment"][parameters["variable"]] +=";"
        context["environment"][parameters["variable"]] += parameters["value"]
        if not context["environment"][parameters["variable"]].endswith(";"):
            context["environment"][parameters["variable"]] +=";"
    
    return True

def edit_file(context, cwd, args, result, **kwargs):
    log = context.get("logger")
    if log is None:
        log = log_tools.Logger()

    log.info("... Editing file ...")

    parameters = args_parser(log, args, result)
    
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
    
    return True
