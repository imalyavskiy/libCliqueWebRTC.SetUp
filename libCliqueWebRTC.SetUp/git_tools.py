# -*- coding: utf-8 -*-
import subprocess
import os

def run(log, target, args=None, **kwargs):
    pipe = subprocess.PIPE
    
    cmd_str = target
    if args is not None:
        cmd_str += " " + args

    cwd_str = os.getcwd()
    cwd = kwargs.get("cwd")
    if cwd is not None:
        cwd_str = cwd

    log.info("Call \"{0}\"... ".format(cmd_str)) #TODO: stay on the same line as it was with print
    output = subprocess.Popen(cmd_str,
                                shell=True,
                                stdin=pipe,
                                stdout=pipe,
                                stderr=subprocess.STDOUT,
                                cwd=cwd_str).stdout.read()
    log.info("Done.")
    
    if 0 == len(output):
        log.error("Failed...")
        return ""

    log.success("Succeeded")
    return output.decode('utf8', 'ignore')

class Client:
    def __init__(self, _log = None):
        self.log = _log
        pass

    def run(self, args, **kwargs): # TODO: remove this method
        return run(self.log, "git", args, **kwargs)

    def check(self):
        output = self.run("--version")
        if output.startswith("git version"):
            return True
        return False

    def clone(self, repository, path):
        return self.run(str("clone {0} {1}".format(repository, path)))

    def checkout(self, branch, **kwargs):
        #TODO: need to check does the branch aready exist
        string = str("checkout -b {0}".format(branch))

        path = kwargs.get("tag")
        if path is not None:
            string += " " + path

        return self.run(string, cwd=kwargs.get("cwd"))

    def status(self, path):
        return self.run("status " + path, cwd=path)

