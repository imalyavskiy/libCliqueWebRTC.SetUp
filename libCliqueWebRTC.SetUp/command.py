import subprocess
import os

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

    log.info("Call \"{0}\"... ".format(cmd_str)) #TODO: stay on the same line as it was with print
    output = subprocess.Popen(cmd_str,
                                shell=True,
                                stdin=pipe,
                                stdout=pipe,
                                stderr=subprocess.STDOUT,
                                cwd=cwd_str,
                                env=env).stdout.read()
    log.info("Done.")
    
    if 0 == len(output):
        log.error("Failed...")
        return ""

    log.success("Succeeded")
    return output.decode('utf8', 'ignore')

def git(log, cwd, args, **kwargs):
    return run(log, "git", args, env = None if "env" not in kwargs else kwargs["env"], cwd=cwd)

def b2(log, cwd, args, **kwargs):
    if not os.path.isfile(cwd+"/b2.bat"):
        return False
    run(log, "bootstrap.bat", args, env = None if "env" not in kwargs else kwargs["env"], cwd=cwd)
    pass

def bootstrap(log, cwd, args, **kwargs):
    if not os.path.isfile(cwd+"/bootstrap.bat"):
        return False
    run(log, "bootstrap.bat", args, env = None if "env" not in kwargs else kwargs["env"], cwd=cwd)
    pass

def copy(log, cwd, args, **kwargs):
    pass
