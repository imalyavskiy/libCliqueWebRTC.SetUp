# -*- coding: utf-8 -*-

# check does git available
# clone https://github.com/boostorg/boost
# clone git://git.openssl.org/openssl.git
# clone https://github.com/socketio/socket.io-client-cpp
# update submodules if any

#TODO check if all the variables below are initialized before start doing anything
install_dir     ="D:/TEMP/test_setup/"
vcvarsall_dir   ="C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Auxiliary/Build/"

import git_tools
import log_tools
import os
import shutil
import env_extractor
import command

#TODO redesign settings and code in order to comply to command+arguments style
# for now cloning is left aside

config_1_0 = { 
    "socket.io-client-cpp" :
    { "active"       : True
    , "clone"        : False
    , "build"        : True
    , "url"          : "https://github.com/socketio/socket.io-client-cpp"
    , "target_branch": "branch_1.6.1"
    , "source_tag"   : "1.6.1"
    , "build_targets": 
        [#targets
            [#steps
                { "command" : "git"
                , "args"    : ["clean -fx -d"]}, #clean up local git repo
                { "command" : "edit_file" 
                , "file"    : "CMakeLists.txt"
                , "rm_str"  : "set(Boost_USE_STATIC_RUNTIME OFF)"
                },
                { "command" : "cmake"
                , "args"    : 
                    [ "-G \"Visual Studio 15 2017 Win64\""
                    , "./", "-DBOOST_ROOT=\"./../boost/\""
                    , "-DBOOST_LIBRARYDIR=\"./../boost/stage/lib_Win64/\""
                    , "-DOPENSSL_ROOT_DIR=\"./../openssl_libs/Win64/\""
                    , "-DCMAKE_CXX_FLAGS=/D_WEBSOCKETPP_NOEXCEPT_"
                    , "-DBoost_USE_STATIC_RUNTIME=ON"
                    ] 
                },
                { "upd_env" : "Path"
                , "append"  : "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/MSBuild/15.0/Bin/amd64"},
                { "upd_env" : "PATH"
                , "append"  : "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/MSBuild/15.0/Bin/amd64"},
#                { "command" : "msbuild"
#                , "args"    : 
#                    [ "sioclient.vcxproj"
#                    , "/t:Rebuild"
#                    , "/p:Configuration=Debug;Platform=x64;OutDir=./../socket.io-client-cpp_libs/Win64/Debug"
#                    ]
#                },
                { "command" : "msbuild"
                , "args"    : 
                    [ "sioclient.vcxproj"
                    , "/t:Rebuild"
                    , "/p:Configuration=Release;Platform=x64;OutDir=./../socket.io-client-cpp_libs/Win64/Release"
                    ]
                },
#                { "command" : "msbuild"
#                , "args"    : 
#                    [ "sioclient_tls.vcxproj"
#                    , "/t:Rebuild"
#                    , "/p:Configuration=Debug;Platform=x64;OutDir=./../socket.io-client-cpp_libs/Win64/Debug"
#                    ]
#                },
                { "command" : "msbuild"
                , "args"    : 
                    [ "sioclient_tls.vcxproj"
                    , "/t:Rebuild"
                    , "/p:Configuration=Release;Platform=x64;OutDir=./../socket.io-client-cpp_libs/Win64/Release"
                    ]
                }
            ],
            [#steps
                { "command" : "git"
                , "args"    : ["clean -fx -d"]}, #clean up local git repo
                { "command" : "edit_file" 
                , "file"    : "CMakeLists.txt"
                , "rm_str"  : "set(Boost_USE_STATIC_RUNTIME OFF)"
                },
                { "command" : "cmake"
                , "args"    : 
                    [ "-G \"Visual Studio 15 2017\""
                    , "./", "-DBOOST_ROOT=\"./../boost/\""
                    , "-DBOOST_LIBRARYDIR=\"./../boost/stage/lib_Win32/\""
                    , "-DOPENSSL_ROOT_DIR=\"./../openssl_libs/Win32/\""
                    , "-DCMAKE_CXX_FLAGS=/D_WEBSOCKETPP_NOEXCEPT_"
                    , "-DBoost_USE_STATIC_RUNTIME=ON"
                    ] 
                },
                { "upd_env" : "Path"
                , "append"  : "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/MSBuild/15.0/Bin/amd64"},
                { "upd_env" : "PATH"
                , "append"  : "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/MSBuild/15.0/Bin/amd64"},
#                { "command" : "msbuild"
#                , "args"    : 
#                    [ "sioclient.vcxproj"
#                    , "/t:Rebuild"
#                    , "/p:Configuration=Debug;Platform=x86;OutDir=./../socket.io-client-cpp_libs/Win32/Debug"
#                    ]
#                },
                { "command" : "msbuild"
                , "args"    : 
                    [ "sioclient.vcxproj"
                    , "/t:Rebuild"
                    , "/p:Configuration=Release;Platform=x86;OutDir=./../socket.io-client-cpp_libs/Win32/Release"
                    ]
                },
#                { "command" : "msbuild"
#                , "args"    : 
#                    [ "sioclient_tls.vcxproj"
#                    , "/t:Rebuild"
#                    , "/p:Configuration=Debug;Platform=x86;OutDir=./../socket.io-client-cpp_libs/Win32/Debug"
#                    ]
#                },
                { "command" : "msbuild"
                , "args"    : 
                    [ "sioclient_tls.vcxproj"
                    , "/t:Rebuild"
                    , "/p:Configuration=Release;Platform=x86;OutDir=./../socket.io-client-cpp_libs/Win32/Release"
                    ]
                }            
            ],
            [#steps
                { "command" : "git"
                , "args"    : ["clean -fx -d"]} #clean up local git repo
            ]
        ]
    },

    "depot_tools" :
    { "active"       : False
    , "clone"        : False
    , "build"        : False
    , "url"          : "https://chromium.googlesource.com/chromium/tools/depot_tools.git"
    , "target_branch": None
    , "source_tag"   : None 
    , "build_targets": []},
}

dependencies =\
[
    { "name"          : "boost",
      "stages"        : [ 
            { "name"  : "clone",
              "active": False,
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : [ "clone", "https://github.com/boostorg/boost", "./"],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : [ "checkout", "-b", "branch_boost-1.64.0", "boost-1.64.0" ],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : ["submodule", "update", "--init", "--"],
                      "result"  : str()},
                ]
            },
            { "name"  : "build",
              "active": True,
              "steps" : 
                [
                    { "command" : command.git,
                      "args"    : [ "clean", "-fx", "-d"],
                      "result"  : str()},
                    { "command" : command.read_env_vars,
                      "args"    : [ "\""+vcvarsall_dir+"vcvarsall.bat\"", "x86"],
                      "result"  : {}},
                    { "command" : command.bootstrap,
                      "args"    : [],
                      "result"  : str()},
                    { "command" : command.b2,
                      "args"    : [ "headers" ],
                      "result"  : str()},
                    { "command" : command.b2,
                      "args"    : ["--with-system", "--with-date_time", "--with-random", "--with-regex", 
                                   "link=static", "runtime-link=static", "threading=multi", "address-model=32"],
                      "result"  : str()},
                    { "command" : command.copy,
                      "args"    : ["stage/lib", "stage/lib_Win32"],
                      "result"  : str()},
                    { "command" : command.b2,
                      "args"    : ["--with-system", "--with-date_time", "--with-random", "--with-regex", 
                                   "link=static", "runtime-link=static", "threading=multi", "address-model=64"],
                      "result"  : str()},
                    { "command" : command.copy,
                      "args"    : ["stage/lib", "stage/lib_Win64"],
                      "result"  : str()},
                ]
            },
#            { "name"  : "clean",
#              "active": False,
#              "steps" :
#                [
#                    { "command" : command.git,
#                      "args"    : [ "clean", "-fx", "-d"],
#                      "result"  : str()}
#                ]
#            },
        ]
    },
    { "name"          : "openssl",
      "stages"        : [
            { "name"  : "clone",
              "active": False,
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : [ "clone", "git://git.openssl.org/openssl.git", "./"],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : [ "checkout", "-b", "branch_OpenSSL_1_0_2l", "OpenSSL_1_0_2l" ],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : ["submodule", "update", "--init", "--"],
                      "result"  : str()},
                ]
            },
            { "name"  : "build_Win32",
              "active": False,
              "steps" :
                [
                    { "command" : command.read_env_vars,
                      "args"    : [ "\""+vcvarsall_dir+"vcvarsall.bat\"", "x86"],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"],
                      "result"  : str()},
                    { "command" : command.perl,
                      "args"    : ["Configure", "VC-WIN32", "no-asm", "--prefix=./../openssl_libs/Win32"],
                      "result"  : str()},
                    { "command" : command.cmd,
                      "args"    : ["/c", "ms/do_ms.bat"],
                      "result"  : str() },
                    { "command" : command.cmd,
                      "args"    : ["/c", "nmake", "-f", "ms/ntdll.mak"],
                      "result"  : str()},
                    { "command" : command.cmd,
                      "args"    : ["/c", "nmake", "-f", "ms/ntdll.mak install"],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"],
                      "result"  : str()},
                ]
            },
            { "name"  : "build_Win64",
              "active": False,
              "steps" :
                [
                    { "command" : command.read_env_vars,
                      "args"    : [ "\""+vcvarsall_dir+"vcvarsall.bat\"", "x64"],
                      "result"  : str()},
                    { "command" : command.prepend_path_with,
                      "args"    : ["C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Tools/MSVC/14.10.25017/bin/HostX64/x64"],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"],
                      "result"  : str()},
                    { "command" : command.perl,
                      "args"    : ["Configure", "VC-WIN64A", "--prefix=./../openssl_libs/Win64"],
                      "result"  : str()},
                    { "command" : command.cmd,
                      "args"    : ["/c", "ms/do_win64a.bat"],
                      "result"  : str() },
                    { "command" : command.cmd,
                      "args"    : ["/c", "nmake", "-f", "ms/ntdll.mak"],
                      "result"  : str()},
                    { "command" : command.cmd,
                      "args"    : ["/c", "nmake", "-f", "ms/ntdll.mak", "install"],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"],
                      "result"  : str()},
                ]
            },
            { "name"  : "clean",
              "active": False,
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"],
                      "result"  : str()},
                ]
            },
        ]
    },

    { "name"          : "socket.io",
      "stages"        : [
            { "name"  : "clone",
              "active": False,
              "steps" :
                [
                ]
            },
            { "name"  : "build",
              "active": False,
              "steps" :
                [
                ]
            },
            { "name"  : "clean",
              "active": False,
              "steps" :
                [
                ]
            },
        ]
    },

    { "name"          : "depot_tools",
      "stages"        : [
            { "name"  : "clone",
              "active": False,
              "steps" :
                [
                ]
            },
            { "name"  : "build",
              "active": False,
              "steps" :
                [
                ]
            },
            { "name"  : "clean",
              "active": False,
              "steps" :
                [
                ]
            },
        ]
    },

    { "name"          : "webrtc",
      "stages"        : [
            { "name"  : "clone",
              "active": False,
              "steps" :
                [
                ]
            },
            { "name"  : "build",
              "active": False,
              "steps" :
                [
                ]
            },
            { "name"  : "clean",
              "active": False,
              "steps" :
                [
                ]
            },
        ]
    }
]

log = log_tools.Logger()
git = git_tools.Client(log)

def is_executable(name, env=None):
    env_path = os.environ.get("Path")
    if env is not None and ("Path" in env or "PATH" in env):
        if "Path" in env:
            env_path = env["Path"]
        else:
            env_path = env["PATH"]
        
    if env_path is None:
        env_path = os.environ.get("PATH")
    
    if env_path is None:
        return False

    entries = env_path.split(";")
    for entry in entries:
        if not entry.endswith("\\") and not entry.endswith("/"):
            entry+="\\"
        
        path_to_check = []
        if name.endswith(".exe") or name.endswith(".bat") or name.endswith(".com"):
            path_to_check.append(entry+name)
        else:
            path_to_check.append(entry+name+".exe")
            path_to_check.append(entry+name+".com")
            path_to_check.append(entry+name+".bat")
        
        for path in path_to_check:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                return True
    return False

def edit_file(dir, params):
    if "file" not in params: 
        return False
    if "rm_str" not in params:
        return False

    in_file = open(dir+"/"+params["file"], "r")
    if in_file is None:
        return False

    out_file = open(dir+"/"+params["file"]+".tmp", "w")
    if out_file is None:
        return False

    while True:
        line = in_file.readline()
        if line == "":
            break
        elif params["rm_str"] in line:
            continue
        else:
            out_file.write(line)

    in_file.close()
    out_file.close()

    os.remove(dir+"/"+params["file"])
    os.rename(dir+"/"+params["file"]+".tmp", dir+"/"+params["file"])

functions = {"edit_file" : edit_file}

def is_function(name):
    if name in functions:
        return True
    return False

def get_function(name):
    if name in functions:
        return functions[name]
    return None

def clone_one(target_dir, resource_name, source_url, target_branch=None, source_tag=None):
    location = target_dir+"/"+resource_name
    git.clone(repository=source_url, path=location)
    if target_branch is not None and source_tag is not None:
        git.checkout(branch=target_branch, tag=source_tag, cwd=location)
    if os.path.isfile(location+"/.gitmodules"):
        git.run("submodule update --init --", cwd=location)

def clone_all(target_dir):
    for target in config_1_0:
        target_config = config_1_0[target]
        if target_config["active"] is True:
            if target_config["clone"] is True:
                log.info("Cloning \"{0}\"...".format(target))
                clone_one(target_dir, target, target_config["url"], target_config["target_branch"], target_config["source_tag"])
            else:
                log.info("\"{0}\" skipped - clone disabled...".format(target))
        else:
            log.info("\"{0}\" skipped - turned off...".format(target))

def build_socketio(target_dir):
    socketio_config = config_1_0["socket.io-client-cpp"]
    socketio_root_dir = target_dir + "/socket.io-client-cpp"
    _env = os.environ.copy()
    for build_target in socketio_config["build_targets"]:
        for step in build_target:
            if "command" in step and is_executable(step["command"], _env):
                arguments = ""
                for arg in step["args"]:
                    if len(arguments) != 0:
                        arguments+=" "
                    arguments += arg
                result = git_tools.run(log, step["command"], arguments, cwd=socketio_root_dir, env=_env)
            elif "command" in step and is_function(step["command"]):
                fun = get_function(step["command"])
                fun(socketio_root_dir, step)
                pass
            elif "upd_env" in step and step["upd_env"] in _env:
                if "prepend" in step:
                    _env[step["upd_env"]] = "{0};{1}".format(step["prepend"], _env[step["upd_env"]]) 
                if "append" in step:
                    if not _env[step["upd_env"]].endswith(";"):
                        _env[step["upd_env"]] += ";"
                    _env[step["upd_env"]] += step["append"] + ";"
            pass
        pass
    pass

def build_depot_tools(target_dir):
    #TODO implement depot tools building
    pass

def build_webrtc(target_dir):
    #TODO implement webrtc building
    pass

def build_libCliqueWebRTC(target_dir):
    #TODO implement libCliqueWebRTC building
    pass

def build_all(target_dir):
    for target in config_1_0:
        target_config = config_1_0[target]
        if target_config["active"] is True:
            if target_config["build"] is True:
                if target == "boost":
                    build_boost(target_dir)
                elif target == "openssl.org":
                    build_openssl(target_dir)
                elif target == "socket.io-client-cpp":
                    build_socketio(target_dir)
                elif target == "depot_tools":
                    build_depot_tools(target_dir)
                elif target == "webrtc":
                    build_webrtc(target_dir)
                elif target == "libCliqueWebRTC":
                    build_libCliqueWebRTC(target_dir)
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

def set_env_variables():
    #TODO : set nesessary environment variables to the windows registry
    pass

def main_1_0():
    if not check_binaries():
        return False

    clone_all(install_dir)
    
    build_all(install_dir)

    set_env_variables()

    return True

def main_2_0():
    for dependency in dependencies:
        if sorted(dependency.keys()) != sorted(["name", "stages"]):
            log.error("Invalid dependency format")
            return False
        log.info("Processing dependency - \"{0}\"...".format(dependency["name"]))
        for stage in dependency["stages"]:
            
            context = {"logger"         : log,              #the context
                       "install_dir"    : install_dir,
                       "dependency_dir" : install_dir+dependency["name"]+"/",} 

            if sorted(stage.keys()) != sorted(["name", "active", "steps"]):
                log.error("Invalid stage format")
                return False
            log.info("Processing stage - \"{0}\"...".format(stage["name"]))
            if stage["active"] is False:
                log.info("stage is inactive")
                continue
            for index in range(0, len(stage["steps"])):
                step = stage["steps"][index]
                log.info("step[{0}/{1}]".format(index + 1, len(stage["steps"])))
                if sorted(stage["steps"][index].keys()) != sorted(["command", "args", "result"]):
                    log.error("Invalid command format")
                    return False
                if not os.path.isdir(install_dir+"/"+dependency["name"]):
                    os.makedirs(install_dir+"/"+dependency["name"])
                step["command"](
                    context,
                    install_dir+"/"+dependency["name"],
                    step["args"],
                    step["result"]
                    )
            context.clear() #clean up context
    return True

if __name__ == "__main__":
#    if not main_1_0():
    if not main_2_0():
        log.error()
        exit()
    log.success()
    exit()

