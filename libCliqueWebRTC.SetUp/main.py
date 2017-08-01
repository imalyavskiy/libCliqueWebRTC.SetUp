# -*- coding: utf-8 -*-

#TODO check if all the variables below are initialized before start doing anything
#TODO pass install target dir by argv
#TODO check all the pathes required before start
#TODO write the application long and the logs of instruments(commands) to the bit log file

install_dir     = "D:/TEMP/test_setup/"
vcvarsall_dir   = "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Auxiliary/Build/"
msbuild_dir     = "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Tools/MSVC/14.10.25017/bin/HostX64/x64/"
cmake_dir       = "C:/Program Files/CMake/bin/"

import log_tools
import os
import command

log = log_tools.Logger()

subdir_boost        = "boost/"
subdir_openssl      = "openssl/"
subdir_socketio     = "socket.io/"
subdir_curl         = "curl/"
subdir_depot_tools  = "depot_tools/"
subdir_webrtc       = "webrtc/"

activities = \
{
    subdir_boost[:-1]   : { 
          "clone"       : False,
          "build_Win32" : False,
          "build_Win64" : False,
          "clean"       : False,
    },
    subdir_openssl[:-1] : { 
          "clone"       : False,
          "build_Win32" : False,
          "build_Win64" : False,
          "clean"       : False,
    },
    subdir_socketio[:-1]: {
          "clone"       : False,
          "build_Win64" : False,
          "build_Win32" : False,
          "clean"       : False,
    },
    subdir_curl[:-1]    : {
          "clone"       : False,
          "build_Win64" : False,
          "build_Win32" : False,
          "clean"       : False,
    },
    subdir_depot_tools[:-1]: {
          "clone"       : True,
          "setup"       : True,
          "clean"       : False,
    },
    subdir_webrtc[:-1]  : {
          "clone"       : False,
          "build_Win32" : False,
          "build_Win64" : False,
          "clean"       : False,
    },
}

dependencies =\
[
    { "name"          : subdir_boost[:-1],
      "stages"        : [ 
            { "name"  : "clone",
              "active": activities[subdir_boost[:-1]]["clone"],
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
            { "name"  : "build_Win64",
              "active": activities[subdir_boost[:-1]]["build_Win64"],
              "steps" : 
                [
                    { "command" : command.read_env_vars,
                      "args"    : [ "\""+vcvarsall_dir+"vcvarsall.bat\"", "x64"],
                      "result"  : {}},
                    { "command" : command.git,
                      "args"    : [ "clean", "-fx", "-d"],
                      "result"  : str()},
                    { "command" : command.bootstrap,
                      "args"    : [],
                      "result"  : str()},
                    { "command" : command.b2,
                      "args"    : [ "headers" ],
                      "result"  : str()},
                    { "command" : command.b2,
                      "args"    : ["--with-system", "--with-date_time", "--with-random", "--with-regex", 
                                   "link=static", "runtime-link=static", "threading=multi", "address-model=64"],
                      "result"  : str()},
                    { "command" : command.move,
                      "args"    : ["--src=\"stage/lib\"", "--dst=\"./../boost_libs/lib_Win64\""],
                      "result"  : str()},
                    { "command" : command.copy,
                      "args"    : ["--src=\"boost\"", "--dst=\"./../boost_libs/boost\""],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : [ "clean", "-fx", "-d"],
                      "result"  : str()},
                ]
            },
            { "name"  : "build_Win32",
              "active": activities[subdir_boost[:-1]]["build_Win32"],
              "steps" : 
                [
                    { "command" : command.read_env_vars,
                      "args"    : [ "\""+vcvarsall_dir+"vcvarsall.bat\"", "x86"],
                      "result"  : {}},
                    { "command" : command.git,
                      "args"    : [ "clean", "-fx", "-d"],
                      "result"  : str()},
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
                    { "command" : command.move,
                      "args"    : ["--src=\"stage/lib\"", "--dst=\"./../boost_libs/lib_Win32\"", "--filter=\"\""],
                      "result"  : str()},
                    { "command" : command.copy,
                      "args"    : ["--src=\"boost\"", "--dst=\"./../boost_libs/boost\"", "--filter=\"\""],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : [ "clean", "-fx", "-d"],
                      "result"  : str()},
                ]
            },
            { "name"  : "clean",
              "active": activities[subdir_boost[:-1]]["clean"],
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : [ "clean", "-fx", "-d"],
                      "result"  : str()}
                ]
            },
        ]
    },
    { "name"          : subdir_openssl[:-1],
      "stages"        : [
            { "name"  : "clone",
              "active": activities[subdir_openssl[:-1]]["clone"],
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
              "active": activities[subdir_openssl[:-1]]["build_Win32"],
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
              "active": activities[subdir_openssl[:-1]]["build_Win64"],
              "steps" :
                [
                    { "command" : command.read_env_vars,
                      "args"    : [ "\""+vcvarsall_dir+"vcvarsall.bat\"", "x64"],
                      "result"  : str()},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=prepend", "--value="+msbuild_dir],
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
              "active": activities[subdir_openssl[:-1]]["clean"],
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"],
                      "result"  : str()},
                ]
            },
        ]
    },
    { "name"          : subdir_socketio[:-1],
      "stages"        : [
            { "name"  : "clone",
              "active": activities[subdir_socketio[:-1]]["clone"],
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : [ "clone", "https://github.com/socketio/socket.io-client-cpp", "./"],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : [ "checkout", "-b", "branch_1.6.1", "1.6.1" ],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : ["submodule", "update", "--init", "--"],
                      "result"  : str()},
                ]
            },
            { "name"  : "build_Win64",
              "active": activities[subdir_socketio[:-1]]["build_Win64"],
              "steps" :
                [
                    { "command" : command.read_env_vars,
                      "args"    : [],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"],
                      "result"  : str()},
                    { "command" : command.edit_file,
                      "args"    : ["--file=CMakeLists.txt", "--action=remove", "--string=\"set(Boost_USE_STATIC_RUNTIME OFF)\""],
                      "result"  : str()},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=append", "--value=\"C:/Program Files/CMake/bin/\""],
                      "result"  : str()},
                    { "command" : command.cmake,
                      "args"    : [ "-G \"Visual Studio 15 2017 Win64\"", "./", "-DBOOST_ROOT=\"./../boost_libs/\"", "-DBOOST_LIBRARYDIR=\"./../boost_libs/lib_Win64/\"", 
                                    "-DOPENSSL_ROOT_DIR=\"./../openssl_libs/Win64/\"", "-DCMAKE_CXX_FLAGS=/D_WEBSOCKETPP_NOEXCEPT_" , "-DBoost_USE_STATIC_RUNTIME=ON"],
                      "result"  : str()},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=append", "--value="+msbuild_dir],
                      "result"  : str()},
                    { "command" : command.msbuild,
                      "args"    : 
                        [ "sioclient.vcxproj"
                        , "/t:Rebuild"
                        , "/p:Configuration=Debug;Platform=x64;OutDir=./../socket.io_libs/Win64/Debug"
                        ],
                      "result"  : str()},
                    { "command" : command.msbuild,
                      "args"    : 
                        [ "sioclient.vcxproj"
                        , "/t:Rebuild"
                        , "/p:Configuration=Release;Platform=x64;OutDir=./../socket.io_libs/Win64/Release"
                        ],
                      "result"  : str()},
                    { "command" : command.msbuild,
                      "args"    : 
                        [ "sioclient_tls.vcxproj"
                        , "/t:Rebuild"
                        , "/p:Configuration=Debug;Platform=x64;OutDir=./../socket.io_libs/Win64/Debug"
                        ],
                      "result"  : str()},
                    { "command" : command.msbuild,
                      "args"    : 
                        [ "sioclient_tls.vcxproj"
                        , "/t:Rebuild"
                        , "/p:Configuration=Release;Platform=x64;OutDir=./../socket.io_libs/Win64/Release"
                        ],
                      "result"  : str()},
                ]
            },
            { "name"  : "build_Win32",
              "active": activities[subdir_socketio[:-1]]["build_Win32"],
              "steps" :
                [
                    { "command" : command.read_env_vars,
                      "args"    : [],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"],
                      "result"  : str()},
                    { "command" : command.edit_file,
                      "args"    : ["--file=CMakeLists.txt", "--action=remove", "--string=\"set(Boost_USE_STATIC_RUNTIME OFF)\""],
                      "result"  : str()},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=append", "--value=\"C:/Program Files/CMake/bin/\""],
                      "result"  : str()},
                    { "command" : command.cmake,
                      "args"    : [ "-G \"Visual Studio 15 2017\"", "./", "-DBOOST_ROOT=\"./../boost_libs/\"", "-DBOOST_LIBRARYDIR=\"./../boost_libs/lib_Win32/\"", 
                                    "-DOPENSSL_ROOT_DIR=\"./../openssl_libs/Win32/\"", "-DCMAKE_CXX_FLAGS=/D_WEBSOCKETPP_NOEXCEPT_" , "-DBoost_USE_STATIC_RUNTIME=ON"],
                      "result"  : str()},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=append", "--value="+msbuild_dir],
                      "result"  : str()},
                    { "command" : command.msbuild,
                      "args"    : 
                        [ "sioclient.vcxproj"
                        , "/t:Rebuild"
                        , "/p:Configuration=Debug;Platform=x86;OutDir=./../socket.io_libs/Win32/Debug"
                        ],
                      "result"  : str()},
                    { "command" : command.msbuild,
                      "args"    : 
                        [ "sioclient.vcxproj"
                        , "/t:Rebuild"
                        , "/p:Configuration=Release;Platform=x86;OutDir=./../socket.io_libs/Win32/Release"
                        ],
                      "result"  : str()},
                    { "command" : command.msbuild,
                      "args"    : 
                        [ "sioclient_tls.vcxproj"
                        , "/t:Rebuild"
                        , "/p:Configuration=Debug;Platform=x86;OutDir=./../socket.io_libs/Win32/Debug"
                        ],
                      "result"  : str()},
                    { "command" : command.msbuild,
                      "args"    : 
                        [ "sioclient_tls.vcxproj"
                        , "/t:Rebuild"
                        , "/p:Configuration=Release;Platform=x86;OutDir=./../socket.io_libs/Win32/Release"
                        ],
                      "result"  : str()},
                ]
            },
            { "name"  : "clean",
              "active": activities[subdir_socketio[:-1]]["clean"],
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"],
                      "result"  : str()},
                ]
            },
        ]
    },
    { "name"          : subdir_curl[:-1],
      "stages"        : [
            { "name"  : "clone",
              "active": activities[subdir_curl[:-1]]["clone"],
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : [ "clone", "https://github.com/curl/curl", "./"],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : [ "checkout", "-b", "branch_curl-7_54_0", "curl-7_54_0" ],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : ["submodule", "update", "--init", "--"],
                      "result"  : str()},
                ]
            },
            { "name"  : "build_Win64",
              "active": activities[subdir_curl[:-1]]["build_Win64"],
              "steps" :
                [
                    { "command" : command.read_env_vars,
                      "args"    : [],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"],
                      "result"  : str()},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=append", "--value="+cmake_dir],
                      "result"  : str()},
                    { "command" : command.cmake,
                      "args"    : [ "-G \"Visual Studio 15 2017 Win64\"", "./"],
                      "result"  : str()},
                    { "command" : command.cmake,
                      "args"    : [ "--build", ".", "--config Release"],
                      "result"  : str()},
                    { "command" : command.cmake,
                      "args"    : [ "--build", ".", "--config Debug"],
                      "result"  : str()},
                    { "command" : command.move,
                      "args"    : ["--src=\"./lib/Release\"", "--dst=\"./../curl_libs/Win64/Release\"" , "--filter=\"*.lib;*.dll;*.ilk;*.pdb;*.exp\""],
                      "result"  : str()},
                    { "command" : command.move,
                      "args"    : ["--src=\"./lib/Debug\"", "--dst=\"./../curl_libs/Win64/Debug\"" , "--filter=\"*.lib;*.dll;*.ilk;*.pdb;*.exp\""],
                      "result"  : str()},
                    { "command" : command.copy,
                      "args"    : ["--src=\"./include/curl\"", "--dst=\"./../curl_libs/include\"" , "--filter=\"*.h;*.hpp\""],
                      "result"  : str()},
                ]
            },
            { "name"  : "build_Win32",
              "active": activities[subdir_curl[:-1]]["build_Win32"],
              "steps" :
                [
                    { "command" : command.read_env_vars,
                      "args"    : [],
                      "result"  : str()},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"],
                      "result"  : str()},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=append", "--value="+cmake_dir],
                      "result"  : str()},
                    { "command" : command.cmake,
                      "args"    : [ "-G \"Visual Studio 15 2017\"", "./"],
                      "result"  : str()},
                    { "command" : command.cmake,
                      "args"    : [ "--build", ".", "--config Release"],
                      "result"  : str()},
                    { "command" : command.cmake,
                      "args"    : [ "--build", ".", "--config Debug"],
                      "result"  : str()},
                    { "command" : command.move,
                      "args"    : ["--src=\"./lib/Release\"", "--dst=\"./../curl_libs/Win32/Release\"" , "--filter=\"*.lib;*.dll;*.ilk;*.pdb;*.exp\""],
                      "result"  : str()},
                    { "command" : command.move,
                      "args"    : ["--src=\"./lib/Debug\"", "--dst=\"./../curl_libs/Win32/Debug\"" , "--filter=\"*.lib;*.dll;*.ilk;*.pdb;*.exp\""],
                      "result"  : str()},
                    { "command" : command.copy,
                      "args"    : ["--src=\"./include/curl\"", "--dst=\"./../curl_libs/include\"" , "--filter=\"*.h;*.hpp\""],
                      "result"  : str()},
                ]
            },
            { "name"  : "clean",
              "active": activities[subdir_curl[:-1]]["clean"],
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"],
                      "result"  : str()},
                ]
            },
        ]
    },
    { "name"          : subdir_depot_tools[:-1],
      "stages"        : [
            { "name"  : "clone",
              "active": activities[subdir_depot_tools[:-1]]["clone"],
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : [ "clone", "https://chromium.googlesource.com/chromium/tools/depot_tools.git", "./"],
                      "result"  : str()},
                ]
            },
            { "name"  : "setup",
              "active": activities[subdir_depot_tools[:-1]]["setup"],
              "steps" :
                [
#                    { "command" : command.git,
#                      "args"    : ["clean", "-fx", "-d"],
#                      "result"  : str()},
                    { "command" : command.read_env_vars,
                      "args"    : [],
                      "result"  : str()},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=prepend", "--value="+install_dir+subdir_depot_tools],
                      "result"  : str()},
#                    { "command" : command.gclient,
#                      "args"    : [],
#                      "result"  : str()},
#                    { "command" : command.gclient,
#                      "args"    : ["sync"],
#                      "result"  : str()},
                    { "command" : command.create_environment_variable,
                      "args"    : ["--variable=DEPOT_TOOLS_WIN_TOOLCHAIN", "--value=0"],
                      "result"  : str()},
                ]
            },
            { "name"  : "clean",
              "active": activities[subdir_depot_tools[:-1]]["clean"],
              "steps" :
                [
                ]
            },
        ]
    },
    { "name"          : subdir_webrtc[:-1],
      "stages"        : [
            { "name"  : "clone",
              "active": activities[subdir_webrtc[:-1]]["clone"],
              "steps" :
                [
                ]
            },
            { "name"  : "build_Win64",
              "active": activities[subdir_webrtc[:-1]]["build_Win64"],
              "steps" :
                [
                ]
            },
            { "name"  : "build_Win32",
              "active": activities[subdir_webrtc[:-1]]["build_Win32"],
              "steps" :
                [
                ]
            },
            { "name"  : "clean",
              "active": activities[subdir_webrtc[:-1]]["clean"],
              "steps" :
                [
                ]
            },
        ]
    }
]

"""
Сборка webrtc:
Release_x64:
	>gn gen out/Release_x64 --args="is_debug=false target_cpu=\"x64\""
	>gn clean out/Release_x64
	>gm -C out/Release_x64

Debug_x64:
	>gn gen out/Debug_x64 --args="is_debug=true target_cpu=\"x64\""
	>gn clean out/Debug_x64
	>gm -C out/Debug_x64

Release_x86:
	>gn gen out/Release_x86 --args="is_debug=false target_cpu=\"x86\""
	>gn clean out/Release_x86
	>gm -C out/Release_x86

Debug_x86
	>gn gen out/Debug_x86 --args="is_debug=true target_cpu=\"x86\""
	>gn clean out/Debug_x86
	>gm -C out/Debug_x86

"""

def main():
    for dependency in dependencies:
        if sorted(dependency.keys()) != sorted(["name", "stages"]):
            log.error("Invalid dependency format")
            return False
        log.info("Processing dependency - \"{0}\"...".format(dependency["name"]))
        for stage in dependency["stages"]:
            
            # the context
            context = {"logger"         : log,
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
                
                step["command"](context, "{0}/{1}".format(install_dir, dependency["name"]), step["args"], step["result"])

            #clean up context
            context.clear() 
    return True

if __name__ == "__main__":
    if not main():
        log.error()
        exit()
    log.success()
    exit()
