from __future__ import print_function
import sys
import subprocess
import itertools

def validate_pair(ob):
    try:
        if not (len(ob) == 2):
            print("Unexpected result:", ob, file=sys.stderr)
            raise ValueError
    except:
        return False
    return True

def consume(iter):
    try:
        while True: next(iter)
    except StopIteration:
        pass

def get_environment_from_batch_command(env_cmd, args=None, initial=None):
    """
    Take a command (either a single command or list of arguments)
    and return the environment created after running that command.
    Note that if the command must be a batch file or .cmd file, or the
    changes to the environment will not be captured.

    If initial is supplied, it is used as the initial environment passed
    to the child process.
    """
    result = {}
    arguments = ""
    if args is not None:
        arguments = "{0}".format(args[0])
        for arg in range(1, len(args)):
            arguments+=" {0}".format(args[arg])

    if not isinstance(env_cmd, (list, tuple)):
        env_cmd = [env_cmd]
    # construct the command that will alter the environment
    env_cmd = subprocess.list2cmdline(env_cmd)
    # create a tag so we can tell in the output when the proc is done
    tag = "Done running command"
    # construct a cmd.exe command to do accomplish this
    cmd = 'cmd.exe /s /c "{env_cmd} {arguments} && echo "{tag}" && set"'.format(**vars())
    # launch the process
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=initial).stdout.read()
    # parse the output sent to stdout
    line = proc.decode('utf8', 'ignore')
    lines = line.split("\r\n")
    
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
        result[pair[0]]=pair[1]
    return result

#env = get_environment_from_batch_command(vcvarsall)
#print(env)
#subprocess.Popen('proc2', env=env)

