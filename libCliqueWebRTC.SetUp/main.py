# -*- coding: utf-8 -*-

# check does git available
# clone https://github.com/boostorg/boost
# clone git://git.openssl.org/openssl.git
# clone https://github.com/socketio/socket.io-client-cpp
# update submodules if any

install_dir="D:/test_setup"

import git_tools
import log_tools
import os
import shutil
import env_extractor

config = { 
    "boost" : # the feature
    { "active"       : False #does this feature enabled or not
    , "clone"        : False #does the "git clone" step enabled or not
    , "build"        : False #does the "build step" enabled or not
    , "url"          : "https://github.com/boostorg/boost" # git clone source url
    , "target_branch": "branch_boost-1.64.0"               # the branch to switch to(should exist) if brunch not exist but tag is provided then branch wiil be created from the tag below
    , "source_tag"   : "boost-1.64.0"                      # the tag for the branch to create from
    , "build_targets": # a set of build configurations
        [#targets
            { "args":"--with-system --with-date_time --with-random --with-regex link=static runtime-link=static threading=multi address-model=32" # how to build
            , "src": "stage/lib"                                                                                                                  # libraries are here
            , "dst": "stage/lib_Win32"}                                                                                                           # move them here
        ,   { "args":"--with-system --with-date_time --with-random --with-regex link=static runtime-link=shared threading=multi address-model=32" #
            , "src": "stage/lib"                                                                                                                  #
            , "dst": "stage/lib_Win32"}                                                                                                           #
        ,   { "args":"--with-system --with-date_time --with-random --with-regex link=static runtime-link=static threading=multi address-model=64" #
            , "src": "stage/lib"                                                                                                                  #
            , "dst": "stage/lib_Win64"}                                                                                                           #
        ,   { "args":"--with-system --with-date_time --with-random --with-regex link=static runtime-link=shared threading=multi address-model=64" #
            , "src": "stage/lib"                                                                                                                  #
            , "dst": "stage/lib_Win64"}                                                                                                           #
        ]
    },
    
    "openssl.org" : # the feature
    { "active"       : False #does this feature enabled or not
    , "clone"        : False #does the "git clone" step enabled or not
    , "build"        : False #does the "build step" enabled or not
    , "url"          : "git://git.openssl.org/openssl.git"  # git clone source url
    , "target_branch": "branch_OpenSSL_1_0_2l"              # the branch to switch to(should exist) if brunch not exist but tag is provided then branch wiil be created from the tag below
    , "source_tag"   : "OpenSSL_1_0_2l"                     # the tag for the branch to create from
    , "build_targets": # a set of targets
        [#targets
            [ #steps reqired to build certain turget
                { "env"     : "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Auxiliary/Build/vcvarsall.bat" 
                , "env_arg" : ["x86"]}, # run batch in "env" with key in "env_arg" in order to get proper evirinment variables
                { "command" : "git"
                , "args"    : "clean -fx -d"}, #clean up local git repo
                { "command" : "perl" 
                , "args"    : "Configure VC-WIN32 no-asm --prefix=./../openssl_libs/x86"}, # configure the feature in order to build the target
                { "command" : "cmd.exe" 
                , "args"    : "/c"
                , "rel_args": ["ms/do_ms.bat"]}, # another one configuration step
                { "command" : "cmd.exe"
                , "args"    : "/c nmake -f ms/ntdll.mak"}, # building step
                { "command" : "cmd.exe"
                , "args"    : "/c nmake -f ms/ntdll.mak install"}, # installing step the location of installation has been set previousely see --prefix at few lines above
            ],
            [#steps
                { "env"     : "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Auxiliary/Build/vcvarsall.bat"
                , "env_arg" : ["amd64"]}
            ,   { "upd_env" : "Path" # it is necessary to tell where is ml64.exe is located. The Path environment variable will be prended with the path in "prepend"(if "append" then the value pf append
                , "prepend" : "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Tools/MSVC/14.10.25017/bin/HostX64/x64"} #will be appended to Path
            ,   { "command" : "git"
                , "args"    : "clean -fx -d"}
            ,   { "command" : "perl"
                , "args"    : "Configure VC-WIN64A --prefix=./../openssl_libs/x64"}
            ,   { "command" : "cmd.exe"
                , "args"    : "/c"
                , "rel_args": ["ms/do_win64a.bat"]} # this step requires ml64.exe
            ,   { "command" : "cmd.exe"
                , "args"    : "/c nmake -f ms/ntdll.mak"}
            ,   { "command" : "cmd.exe"
                , "args"    : "/c nmake -f ms/ntdll.mak install"}
            ]
        ]
    },
    
    "socket.io-client-cpp" :
    { "active"       : False
    , "clone"        : False
    , "build"        : False
    , "url"          : "https://github.com/socketio/socket.io-client-cpp"
    , "target_branch": "branch_1.6.1"
    , "source_tag"   : "1.6.1"
    , "build_targets": []},

    "depot_tools" :
    { "active"       : False
    , "clone"        : True
    , "build"        : False
    , "url"          : "https://chromium.googlesource.com/chromium/tools/depot_tools.git"
    , "target_branch": None
    , "source_tag"   : None 
    , "build_targets": []},
}

log = log_tools.Logger()
git = git_tools.Client(log)

def clone_one(target_dir, resource_name, source_url, target_branch=None, source_tag=None):
    location = target_dir+"/"+resource_name
    git.clone(repository=source_url, path=location)
    if target_branch is not None and source_tag is not None:
        git.checkout(branch=target_branch, tag=source_tag, cwd=location)
    if os.path.isfile(location+"/.gitmodules"):
        git.run("submodule update --init --", cwd=location)

def clone_all(target_dir):
    for target in config:
        target_config = config[target]
        if target_config["active"] is True:
            if target_config["clone"] is True:
                log.info("Cloning \"{0}\"...".format(target))
                clone_one(target_dir, target, target_config["url"], target_config["target_branch"], target_config["source_tag"])
            else:
                log.info("\"{0}\" skipped - clone disabled...".format(target))
        else:
            log.info("\"{0}\" skipped - turned off...".format(target))

def build_boost(target_dir):
    def cleanup(target_dir):
        for build_target in boost_config["build_targets"]:
            target_dir_full = target_dir+"/boost/"+build_target["dst"]
            if os.path.isdir(target_dir_full):
                shutil.rmtree(target_dir_full)
        temp_build_dir = target_dir+"/boost/bin.v2"
        if os.path.isdir(temp_build_dir):
            shutil.rmtree(temp_build_dir)
        temp_lib_dir = target_dir+"/boost/stage/lib"
        if os.path.isdir(temp_lib_dir):
            shutil.rmtree(temp_lib_dir)

    boost_config = config["boost"]
    if boost_config is None:
        return
    
    cleanup(target_dir)

    #build b2.exe and bjam.exe at boost folder if necessary
    if not os.path.isfile(target_dir+"/boost/bjam.exe"):
        if not os.path.isfile(target_dir+"/boost/bootstrap.bat"):
            log.error("booststrap.bat at {0} does not exist".format(target_dir+"\boost"))
            return
        else:
            git_tools.run(log, target_dir+"/boost/bootstrap.bat", cwd=target_dir+"/boost")
    
    #check it is built    
    if not os.path.isfile(target_dir+"/boost/bjam.exe"):
        log.error("bjam.exe at {0} does not exist and did not build by booststrap.bat".format(target_dir+"\boost"))
        return

    #run through build targets and process them
    for build_target in boost_config["build_targets"]:
        target_dir_full = target_dir+"/boost/"+build_target["dst"]
        source_dir_full = target_dir+"/boost/"+build_target["src"]

        #the build itself
        git_tools.run(log, target_dir+"/boost/bjam.exe", build_target["args"], cwd=target_dir+"/boost")

        #TODO: check that everything built ok

        #check presence of the target directory. If not - create
        if not os.path.isdir(target_dir_full):
            os.mkdir(target_dir_full)
            if not os.path.isdir(target_dir_full):
                log.error("Cannot create output directory while building boost")
                return

        #move from source to target
        files = os.listdir(source_dir_full)
        for file in files:
            shutil.move(source_dir_full+"/"+file, target_dir_full+"/"+file)
    
    cleanup(target_dir)
    return

def build_openssl(target_dir):
    openssl_config = config["openssl.org"]
    openssl_root_dir = target_dir + "/openssl.org"
    
    for build_target in openssl_config["build_targets"]:
        _env = {}
        for step in build_target:
            if "env" in step and "env_arg" in step:
                _env = env_extractor.get_environment_from_batch_command(step["env"], step["env_arg"])
            elif "upd_env" in step:
                if step["upd_env"] in _env:
                    if "prepend" in step:
                        _env[step["upd_env"]] = "{0};{1}".format(step["prepend"], _env[step["upd_env"]]) 
                    if "append" in step:
                        if _env[step["upd_env"]].endswith(";"):
                            _env[step["upd_env"]] += step["append"]
                        _env[step["upd_env"]] += step["append"] + ";"
            elif "command" in step and "args" in step:
                args = step["args"]
                if "rel_args" in step:
                    rel_args = step["rel_args"]
                    for arg in rel_args:
                        args += " " + "{0}/{1}".format(openssl_root_dir, arg) 
                str_result = git_tools.run(log, step["command"], args, cwd=openssl_root_dir, env=_env)
            else:
                log.error("Uknown step")

def build_socketio(target_dir):
    pass

def build_all(target_dir):
    for target in config:
        target_config = config[target]
        if target_config["active"] is True:
            if target_config["build"] is True:
                if target == "boost":
                    build_boost(target_dir)
                elif target == "openssl.org":
                    build_openssl(target_dir)
                elif target == "socket.io-client-cpp":
                    build_socketio(target_dir)
            else:
                log.info("\"{0}\" skipped - build disabled...".format(target))
        else:
            log.info("\"{0}\" skipped - turned off...".format(target))

def check_binaries():
    if not git.check():
        log.info("Git client does not installed.\nOr not added to \"path\" environment variable.")
        return False
    else:
        log.success("Git status - installed")

    return True

def main():
    if not check_binaries():
        return False

    clone_all(install_dir)
    
    build_all(install_dir)

    return True

if __name__ == "__main__":
    if not main():
        log.error()
        exit()
    log.success()
    exit()

