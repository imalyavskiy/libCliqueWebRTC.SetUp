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
            { "command" : "b2"                                                                                                                     # this step is absolutely mandatory for modular boost
            , "args"    : "headers" }                                                                                                                  # i.e. taken from git directly
        ,   { "command" : "b2"
            , "args"    : "--with-system --with-date_time --with-random --with-regex link=static runtime-link=static threading=multi address-model=32" # how to build
            , "src"     : "stage/lib"                                                                                                                  # libraries are here
            , "dst"     : "stage/lib_Win32" }                                                                                                          # move them here
        ,   { "command" : "b2"
            , "args"    : "--with-system --with-date_time --with-random --with-regex link=static runtime-link=shared threading=multi address-model=32" #
            , "src"     : "stage/lib"                                                                                                                  #
            , "dst"     : "stage/lib_Win32" }                                                                                                          #
        ,   { "command" : "b2"
            , "args"    : "--with-system --with-date_time --with-random --with-regex link=static runtime-link=static threading=multi address-model=64" #
            , "src"     : "stage/lib"                                                                                                                  #
            , "dst"     : "stage/lib_Win64" }                                                                                                          #
        ,   { "command" : "b2"
            , "args"    : "--with-system --with-date_time --with-random --with-regex link=static runtime-link=shared threading=multi address-model=64" #
            , "src"     : "stage/lib"                                                                                                                  #
            , "dst"     : "stage/lib_Win64" }                                                                                                          #
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
            [ #steps reqired to build certain target
                { "env"     : "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Auxiliary/Build/vcvarsall.bat" 
                , "env_arg" : ["x86"]}, # run batch in "env" with key in "env_arg" in order to get proper evirinment variables
                { "command" : "git"
                , "args"    : "clean -fx -d"}, #clean up local git repo
                { "command" : "perl" 
                , "args"    : "Configure VC-WIN32 no-asm --prefix=./../openssl_libs/Win32"}, # configure the feature in order to build the target
                { "command" : "cmd" 
                , "args"    : "/c"
                , "rel_args": ["ms/do_ms.bat"]}, # another one configuration step
                { "command" : "cmd"
                , "args"    : "/c nmake -f ms/ntdll.mak"}, # building step
                { "command" : "cmd"
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
                , "args"    : "Configure VC-WIN64A --prefix=./../openssl_libs/Win64"}
            ,   { "command" : "cmd"
                , "args"    : "/c"
                , "rel_args": ["ms/do_win64a.bat"]} # this step requires ml64.exe
            ,   { "command" : "cmd"
                , "args"    : "/c nmake -f ms/ntdll.mak"}
            ,   { "command" : "cmd"
                , "args"    : "/c nmake -f ms/ntdll.mak install"}
            ]
        ]
    },
    
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
    def cleanup(target_dir, all=True):
        if all is True:
            for build_target in boost_config["build_targets"]:
                if "dst" in build_target:
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
            log.error("booststrap.bat at {0} does not exist".format(target_dir+"/boost"))
            return
        else:
            result = git_tools.run(log, target_dir+"/boost/bootstrap.bat", cwd=target_dir+"/boost")
    
    #check it is built    
    if not os.path.isfile(target_dir+"/boost/b2.exe"):
        log.error("b2.exe at {0} does not exist and did not build by booststrap.bat".format(target_dir+"\boost"))
        return

    #run through build targets and process them
    for build_target in boost_config["build_targets"]:
        target_dir_full = target_dir+"/boost/"
        source_dir_full = target_dir+"/boost/"
        
        if "dst" in build_target:
            target_dir_full += build_target["dst"]
        else: 
            target_dir_full = None

        if "src" in build_target:
            source_dir_full += build_target["src"]
        else:
            source_dir_full = None

        #the build itself
        result = git_tools.run(log, target_dir+"/boost/"+build_target["command"], build_target["args"], cwd=target_dir+"/boost")

        #TODO: check that everything built ok

        if target_dir_full is None or source_dir_full is None:
            continue

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
    
    cleanup(target_dir, False)
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
                        if not _env[step["upd_env"]].endswith(";"):
                            _env[step["upd_env"]] += ";"
                        _env[step["upd_env"]] += step["append"] + ";"
            elif "command" in step and "args" in step:
                args = step["args"]
                if "rel_args" in step:
                    rel_args = step["rel_args"]
                    for arg in rel_args:
                        args += " " + "{0}/{1}".format(openssl_root_dir, arg) 
                result = git_tools.run(log, step["command"], args, cwd=openssl_root_dir, env=_env)
            else:
                log.error("Uknown step")

def build_socketio(target_dir):
    socketio_config = config["socket.io-client-cpp"]
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

