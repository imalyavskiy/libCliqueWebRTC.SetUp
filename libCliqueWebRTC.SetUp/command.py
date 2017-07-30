import subprocess
import os
import log_tools
import shutil

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

    log.info("Call \"{0}\"... ".format(cmd_str), end="", flash=True)
    output = subprocess.Popen(cmd_str,
                                shell=True,
                                stdin=pipe,
                                stdout=pipe,
                                stderr=subprocess.STDOUT,
                                cwd=cwd_str,
                                env=env).stdout.read()
    log.info("-> Done.", print_header=False)

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

    if args is not None:
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
#    result = proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=initial).stdout.read()
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

def prepend_path_with(context, cwd, args, result, **kwargs):
    if context.get("environment") is None:
        return False
    environment_variables = context["environment"]
    path = str()
    if environment_variables.get("Path") is None and environment_variables.get("PATH") is None:
        return False
    if environment_variables.get("Path") is not None:
        path = environment_variables["Path"]
    else:
        path = environment_variables["PATH"]
    
    prepend = str()
    for item in args:
        prepend += item +";"

    path = prepend + path
    