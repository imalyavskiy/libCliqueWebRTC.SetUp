# -*- coding: utf-8 -*-

#TODO make dry run
#TODO check if all the variables below are initialized before start doing anything
#TODO pass install target dir by argv
#TODO check all the pathes required before start
#TODO write the application long and the logs of instruments(commands) to the bit log file

log_file_name   = "set_up"

###########################################
install_dir     = "D:/TEMP/test_setup/"
vstudio_dir     = "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/" 
vcvarsall_dir   = "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Auxiliary/Build/"
msbuild_dir     = "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Tools/MSVC/14.10.25017/bin/HostX64/x64/"
cmake_dir       = "C:/Program Files/CMake/bin/"
##########################################
vstudio_ver     = "2017"
##########################################

import log_tools
import os
import command
import json
import sys

subdir_boost            = "boost/"
subdir_openssl          = "openssl/"
subdir_socketio         = "socket.io/"
subdir_curl             = "curl/"
subdir_json             = "json/"
subdir_depot_tools      = "depot_tools/"
subdir_libcliquewebrtc  = "libcliquewebrtc/"

activities = \
{
    subdir_boost[:-1]   : { 
          "clone"       : False,
          "build_Win64" : False,
          "build_Win32" : False,
          "clean"       : False,
    },
    subdir_openssl[:-1] : { 
          "clone"       : False,
          "build_Win64" : False,
          "build_Win32" : False,
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
    subdir_json[:-1]    : {
          "clone"       : False,
    },
    subdir_depot_tools[:-1]: {
          "clone"       : False,
          "setup"       : False,
          "build_Win64" : False,
          "build_Win32" : False,
          "clean"       : False,
    },
    "set_env_vars"         : {
          "setup"       : False,
    },
    subdir_libcliquewebrtc[:-1]: {
          "clone"       : False,
          "build_Win64" : False,
          "build_Win32" : False,
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
                      "args"    : [ "clone", "https://github.com/boostorg/boost", "./"]},
                    { "command" : command.git,
                      "args"    : [ "checkout", "-b", "branch_boost-1.64.0", "boost-1.64.0" ]},
                    { "command" : command.git,
                      "args"    : ["submodule", "update", "--init", "--"]},
                ]
            },
            { "name"  : "build_Win64",
              "active": activities[subdir_boost[:-1]]["build_Win64"],
              "steps" : 
                [
                    { "command" : command.read_env_vars,
                      "args"    : [ "\""+vcvarsall_dir+"vcvarsall.bat\"", "x64"]},
                    { "command" : command.git,
                      "args"    : [ "clean", "-fx", "-d"]},
                    { "command" : command.bootstrap,
                      "args"    : []},
                    { "command" : command.b2,
                      "args"    : [ "headers" ]},
                    { "command" : command.b2,
                      "args"    : ["--with-thread", "--with-system", "--with-date_time", "--with-random", "--with-regex", "link=static", "runtime-link=static", "threading=multi", "address-model=64"]},
                    { "command" : command.move,
                      "args"    : ["--src=\"stage/lib\"", "--dst=\"./../boost_libs/lib_Win64\"", "--filter=\"*.lib\""]},
                    { "command" : command.copy,
                      "args"    : ["--src=\"boost\"", "--dst=\"./../boost_libs/boost\"", "--filter=\"*.h;*.hpp;*.ipp\""]},
                    { "command" : command.git,
                      "args"    : [ "clean", "-fx", "-d"]},
                ]
            },
            { "name"  : "build_Win32",
              "active": activities[subdir_boost[:-1]]["build_Win32"],
              "steps" : 
                [
                    { "command" : command.read_env_vars,
                      "args"    : [ "\""+vcvarsall_dir+"vcvarsall.bat\"", "x86"]},
                    { "command" : command.git,
                      "args"    : [ "clean", "-fx", "-d"]},
                    { "command" : command.bootstrap,
                      "args"    : []},
                    { "command" : command.b2,
                      "args"    : [ "headers" ]},
                    { "command" : command.b2,
                      "args"    : ["--with-thread", "--with-system", "--with-date_time", "--with-random", "--with-regex", "link=static", "runtime-link=static", "threading=multi", "address-model=32"]},
                    { "command" : command.move,
                      "args"    : ["--src=\"stage/lib\"", "--dst=\"./../boost_libs/lib_Win32\"", "--filter=\"*.lib\""]},
                    { "command" : command.copy,
                      "args"    : ["--src=\"boost\"", "--dst=\"./../boost_libs/boost\"", "--filter=\"*.h;*.hpp;*.ipp\""]},
                    { "command" : command.git,
                      "args"    : [ "clean", "-fx", "-d"]},
                ]
            },
            { "name"  : "clean",
              "active": activities[subdir_boost[:-1]]["clean"],
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : [ "clean", "-fx", "-d"]}
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
                      "args"    : [ "clone", "git://git.openssl.org/openssl.git", "./"]},
                    { "command" : command.git,
                      "args"    : [ "checkout", "-b", "branch_OpenSSL_1_0_2l", "OpenSSL_1_0_2l" ]},
                    { "command" : command.git,
                      "args"    : ["submodule", "update", "--init", "--"]},
                ]
            },
            { "name"  : "build_Win32",
              "active": activities[subdir_openssl[:-1]]["build_Win32"],
              "steps" :
                [
                    { "command" : command.read_env_vars,
                      "args"    : [ "\""+vcvarsall_dir+"vcvarsall.bat\"", "x86"]},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"]},
                    { "command" : command.perl,
                      "args"    : ["Configure", "VC-WIN32", "no-asm", "--prefix=./../openssl_libs/Win32"]},
                    { "command" : command.cmd,
                      "args"    : ["/c", "ms/do_ms.bat"]},
                    { "command" : command.cmd,
                      "args"    : ["/c", "nmake", "-f", "ms/ntdll.mak"]},
                    { "command" : command.cmd,
                      "args"    : ["/c", "nmake", "-f", "ms/ntdll.mak install"]},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"]},
                ]
            },
            { "name"  : "build_Win64",
              "active": activities[subdir_openssl[:-1]]["build_Win64"],
              "steps" :
                [
                    { "command" : command.read_env_vars,
                      "args"    : [ "\""+vcvarsall_dir+"vcvarsall.bat\"", "x64"]},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=prepend", "--value="+msbuild_dir]},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"]},
                    { "command" : command.perl,
                      "args"    : ["Configure", "VC-WIN64A", "--prefix=./../openssl_libs/Win64"]},
                    { "command" : command.cmd,
                      "args"    : ["/c", "ms/do_win64a.bat"]},
                    { "command" : command.cmd,
                      "args"    : ["/c", "nmake", "-f", "ms/ntdll.mak"]},
                    { "command" : command.cmd,
                      "args"    : ["/c", "nmake", "-f", "ms/ntdll.mak", "install"]},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"]},
                ]
            },
            { "name"  : "clean",
              "active": activities[subdir_openssl[:-1]]["clean"],
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"]},
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
                      "args"    : [ "clone", "https://github.com/socketio/socket.io-client-cpp", "./"]},
                    { "command" : command.git,
                      "args"    : [ "checkout", "-b", "branch_1.6.1", "1.6.1" ]},
                    { "command" : command.git,
                      "args"    : ["submodule", "update", "--init", "--"]},
                ]
            },
            { "name"  : "build_Win64",
              "active": activities[subdir_socketio[:-1]]["build_Win64"],
              "steps" :
                [
                    { "command" : command.read_env_vars,
                      "args"    : []},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"]},
                    { "command" : command.edit_file,
                      "args"    : ["--file=CMakeLists.txt", "--action=remove", "--string=\"set(Boost_USE_STATIC_RUNTIME OFF)\""]},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=append", "--value=\"C:/Program Files/CMake/bin/\""]},
                    { "command" : command.cmake,
                      "args"    : [ "-G \"Visual Studio 15 2017 Win64\"", "./", "-DBOOST_ROOT=\"./../boost_libs/\"", "-DBOOST_LIBRARYDIR=\"./../boost_libs/lib_Win64/\"", "-DOPENSSL_ROOT_DIR=\"./../openssl_libs/Win64/\"", "-DCMAKE_CXX_FLAGS=/D_WEBSOCKETPP_NOEXCEPT_" , "-DBoost_USE_STATIC_RUNTIME=ON"]},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=append", "--value="+msbuild_dir]},
                    { "command" : command.msbuild,
                      "args"    : [ "sioclient.vcxproj", "/t:Rebuild", "/p:Configuration=Debug;Platform=x64;OutDir=./../socket.io_libs/Win64/Debug"]},
                    { "command" : command.msbuild,
                      "args"    : [ "sioclient.vcxproj", "/t:Rebuild", "/p:Configuration=Release;Platform=x64;OutDir=./../socket.io_libs/Win64/Release"]},
                    { "command" : command.msbuild,
                      "args"    : [ "sioclient_tls.vcxproj", "/t:Rebuild", "/p:Configuration=Debug;Platform=x64;OutDir=./../socket.io_libs/Win64/Debug"]},
                    { "command" : command.msbuild,
                      "args"    : [ "sioclient_tls.vcxproj", "/t:Rebuild", "/p:Configuration=Release;Platform=x64;OutDir=./../socket.io_libs/Win64/Release"]},
                ]
            },
            { "name"  : "build_Win32",
              "active": activities[subdir_socketio[:-1]]["build_Win32"],
              "steps" :
                [
                    { "command" : command.read_env_vars,
                      "args"    : []},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"]},
                    { "command" : command.edit_file,
                      "args"    : ["--file=CMakeLists.txt", "--action=remove", "--string=\"set(Boost_USE_STATIC_RUNTIME OFF)\""]},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=append", "--value=\"C:/Program Files/CMake/bin/\""]},
                    { "command" : command.cmake,
                      "args"    : [ "-G \"Visual Studio 15 2017\"", "./", "-DBOOST_ROOT=\"./../boost_libs/\"", "-DBOOST_LIBRARYDIR=\"./../boost_libs/lib_Win32/\"", "-DOPENSSL_ROOT_DIR=\"./../openssl_libs/Win32/\"", "-DCMAKE_CXX_FLAGS=/D_WEBSOCKETPP_NOEXCEPT_" , "-DBoost_USE_STATIC_RUNTIME=ON"]},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=append", "--value="+msbuild_dir]},
                    { "command" : command.msbuild,
                      "args"    : [ "sioclient.vcxproj", "/t:Rebuild", "/p:Configuration=Debug;Platform=x86;OutDir=./../socket.io_libs/Win32/Debug"]},
                    { "command" : command.msbuild,
                      "args"    : [ "sioclient.vcxproj", "/t:Rebuild", "/p:Configuration=Release;Platform=x86;OutDir=./../socket.io_libs/Win32/Release"]},
                    { "command" : command.msbuild,
                      "args"    : [ "sioclient_tls.vcxproj", "/t:Rebuild", "/p:Configuration=Debug;Platform=x86;OutDir=./../socket.io_libs/Win32/Debug"]},
                    { "command" : command.msbuild,
                      "args"    : [ "sioclient_tls.vcxproj", "/t:Rebuild", "/p:Configuration=Release;Platform=x86;OutDir=./../socket.io_libs/Win32/Release"]},
                ]
            },
            { "name"  : "clean",
              "active": activities[subdir_socketio[:-1]]["clean"],
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"]},
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
                      "args"    : [ "clone", "https://github.com/curl/curl", "./"]},
                    { "command" : command.git,
                      "args"    : [ "checkout", "-b", "branch_curl-7_54_0", "curl-7_54_0" ]},
                    { "command" : command.git,
                      "args"    : ["submodule", "update", "--init", "--"]},
                ]
            },
            { "name"  : "build_Win64",
              "active": activities[subdir_curl[:-1]]["build_Win64"],
              "steps" :
                [
                    { "command" : command.read_env_vars,
                      "args"    : []},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"]},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=append", "--value="+cmake_dir]},
                    { "command" : command.cmake,
                      "args"    : [ "-G \"Visual Studio 15 2017 Win64\"", "./"]},
                    { "command" : command.cmake,
                      "args"    : [ "--build", ".", "--config Release"]},
                    { "command" : command.cmake,
                      "args"    : [ "--build", ".", "--config Debug"]},
                    { "command" : command.move,
                      "args"    : ["--src=\"./lib/Release\"", "--dst=\"./../curl_libs/Win64/Release\"" , "--filter=\"*.lib;*.dll;*.ilk;*.pdb;*.exp\""]},
                    { "command" : command.move,
                      "args"    : ["--src=\"./lib/Debug\"", "--dst=\"./../curl_libs/Win64/Debug\"" , "--filter=\"*.lib;*.dll;*.ilk;*.pdb;*.exp\""]},
                    { "command" : command.copy,
                      "args"    : ["--src=\"./include/curl\"", "--dst=\"./../curl_libs/include/curl\"", "--filter=\"*.h;*.hpp\""]},
                ]
            },
            { "name"  : "build_Win32",
              "active": activities[subdir_curl[:-1]]["build_Win32"],
              "steps" :
                [
                    { "command" : command.read_env_vars,
                      "args"    : []},
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"]},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=append", "--value="+cmake_dir]},
                    { "command" : command.cmake,
                      "args"    : [ "-G \"Visual Studio 15 2017\"", "./"]},
                    { "command" : command.cmake,
                      "args"    : [ "--build", ".", "--config Release"]},
                    { "command" : command.cmake,
                      "args"    : [ "--build", ".", "--config Debug"]},
                    { "command" : command.move,
                      "args"    : ["--src=\"./lib/Release\"", "--dst=\"./../curl_libs/Win32/Release\"" , "--filter=\"*.lib;*.dll;*.ilk;*.pdb;*.exp\""]},
                    { "command" : command.move,
                      "args"    : ["--src=\"./lib/Debug\"", "--dst=\"./../curl_libs/Win32/Debug\"" , "--filter=\"*.lib;*.dll;*.ilk;*.pdb;*.exp\""]},
                    { "command" : command.copy,
                      "args"    : ["--src=\"./include/curl\"", "--dst=\"./../curl_libs/include/curl\"" , "--filter=\"*.h;*.hpp\""]},
                ]
            },
            { "name"  : "clean",
              "active": activities[subdir_curl[:-1]]["clean"],
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"]},
                ]
            },
        ]
    },
    { "name"          : subdir_json[:-1],
      "stages"        : [
            { "name"  : "clone",
              "active": activities[subdir_json[:-1]]["clone"],
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : [ "clone", "https://github.com/nlohmann/json.git", "./"]},
                    { "command" : command.git,
                      "args"    : [ "checkout", "develop" ]},
                    { "command" : command.git,
                      "args"    : ["submodule", "update", "--init", "--"]},
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
                      "args"    : [ "clone", "https://chromium.googlesource.com/chromium/tools/depot_tools.git", "./"]},
                ]
            },
            { "name"  : "setup",
              "active": activities[subdir_depot_tools[:-1]]["setup"],
              "steps" :
                [
                    { "command" : command.git,
                      "args"    : ["clean", "-fx", "-d"]},
                    { "command" : command.read_env_vars,
                      "args"    : []},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=prepend", "--value="+install_dir+subdir_depot_tools]},
                    { "command" : command.cmd,
                      "args"    : ["/c", "gclient"]},
                    { "command" : command.create_environment_variable,
                      "args"    : ["--variable=DEPOT_TOOLS_WIN_TOOLCHAIN", "--value=0"]},
                    { "command" : command.create_environment_variable,
                      "args"    : ["--variable=GYP_MSVS_OVERRIDE_PATH", "--value=\""+vstudio_dir+"\""]}, #TODO move to the beginning os the file
                    { "command" : command.create_environment_variable,
                      "args"    : ["--variable=GYP_MSVS_VERSION", "--value=2017"]},
                    # oprations below take about 3 hours to finish
                    { "command" : command.cmd,
                      "args"    : ["/c", "mkdir", "\"./../webrtc-checkout\""]},
                    { "command" : command.cd,
                      "args"    : ["./../webrtc-checkout"]},
                    { "command" : command.cmd,
                      "args"    : ["/c", "fetch.bat", "--nohooks", "webrtc"]},   #fetch that is fetch.bat and located at depot_tools/
                    { "command" : command.cmd,
                      "args"    : ["/c", "gclient", "sync"]},                    #gclient that is gclient.bat and located at depot_tools/
                ]
            },
            { "name"  : "build_Win64",
              "active": activities[subdir_depot_tools[:-1]]["build_Win64"],
              "steps" : 
                [
                    { "command" : command.read_env_vars,
                      "args"    : []},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=prepend", "--value="+install_dir+subdir_depot_tools]},
                    { "command" : command.create_environment_variable,
                      "args"    : ["--variable=DEPOT_TOOLS_WIN_TOOLCHAIN", "--value=0"]},
                    { "command" : command.create_environment_variable,
                      "args"    : ["--variable=GYP_MSVS_OVERRIDE_PATH", "--value="+vstudio_dir]},
                    { "command" : command.create_environment_variable,
                      "args"    : ["--variable=GYP_MSVS_VERSION", "--value="+vstudio_ver]},
                    { "command" : command.cd,
                      "args"    : ["./../webrtc-checkout/src"]},

                    { "command" : command.cmd,
                      "args"    : ["/c", "gn.bat", "gen \"../../webrtc_libs/Win64/Debug\" --args=\"is_debug=true target_cpu=\\\"x64\\\" rtc_include_tests=false\""]},
                    { "command" : command.cmd,
                      "args"    : ["/c", "ninja", "-C \"../../webrtc_libs/Win64/Debug\""]},

                    { "command" : command.cmd,
                      "args"    : ["/c", "gn.bat", "gen \"../../webrtc_libs/Win64/Release\" --args=\"is_debug=false target_cpu=\\\"x64\\\" rtc_include_tests=false\""]},
                    { "command" : command.cmd,
                      "args"    : ["/c", "ninja", "-C \"../../webrtc_libs/Win64/Release\""]},
                ]
            },
            { "name"  : "build_Win32",
              "active": activities[subdir_depot_tools[:-1]]["build_Win32"],
              "steps" : 
                [
                    { "command" : command.read_env_vars,
                      "args"    : []},
                    { "command" : command.update_environment_variable,
                      "args"    : ["--variable=Path", "--action=prepend", "--value="+install_dir+subdir_depot_tools]},
                    { "command" : command.create_environment_variable,
                      "args"    : ["--variable=DEPOT_TOOLS_WIN_TOOLCHAIN", "--value=0"]},
                    { "command" : command.create_environment_variable,
                      "args"    : ["--variable=GYP_MSVS_OVERRIDE_PATH", "--value="+vstudio_dir]},
                    { "command" : command.create_environment_variable,
                      "args"    : ["--variable=GYP_MSVS_VERSION", "--value="+vstudio_ver]},
                    { "command" : command.cd,
                      "args"    : ["./../webrtc-checkout/src"]},

                    { "command" : command.cmd,
                      "args"    : ["/c", "gn.bat", "gen \"../../webrtc_libs/Win32/Debug\" --args=\"is_debug=true target_cpu=\\\"x86\\\" rtc_include_tests=false\""]},
                    { "command" : command.cmd,
                      "args"    : ["/c", "ninja", "-C \"../../webrtc_libs/Win32/Debug\""]},

                    { "command" : command.cmd,
                      "args"    : ["/c", "gn.bat", "gen \"../../webrtc_libs/Win32/Release\" --args=\"is_debug=false target_cpu=\\\"x86\\\" rtc_include_tests=false\""]},
                    { "command" : command.cmd,
                      "args"    : ["/c", "ninja", "-C \"../../webrtc_libs/Win32/Release\""]},
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
    { "name"          : "set_env_vars",
      "stages"        : [
            { "name"  : "setup",
              "active": activities["set_env_vars"]["setup"],
              "steps" :
                [
                    { "command" : command.create_fixed_environment_variable,
                      "args"    : ["--variable=LIB_CLIQUE_DEPENDENCY_DIR", "--value="+install_dir]},
                ]
            },
        ]
    },
]

def check_required_paths(log):
    if not os.path.isdir(vstudio_dir):
        log.fatal("The \""+vstudio_dir+"\" not exists")
        return False
    else:
        log.info("Presence of \""+vstudio_dir+"\"")
        log.success("Ok!")

    if not os.path.isdir(vcvarsall_dir):
        log.fatal("The \""+vcvarsall_dir+"\" not exists")
        return False
    else:
        log.info("Presence of \""+vcvarsall_dir+"\"")
        log.success("Ok!")

    if not os.path.isdir(msbuild_dir):
        log.fatal("The \""+msbuild_dir+"\" not exists")
        return False
    else:
        log.info("Presence of \""+msbuild_dir+"\"")
        log.success("Ok!")

    if not os.path.isdir(cmake_dir):
        log.fatal("The \""+cmake_dir+"\" not exists")
        return False
    else:
        log.info("Presence of \""+cmake_dir+"\"")
        log.success("Ok!")

    return True

def main():
    log.info("Starting...")

    for cDep in range(0,len(dependencies)):
        if sorted(dependencies[cDep].keys()) != sorted(["name", "stages"]):
            log.error("Invalid dependency format")
            return False
        log.info("=== Processing dependency - \"{0}\"...".format(dependencies[cDep]["name"]))
        for cStage in range(0, len(dependencies[cDep]["stages"])):
            
            # the context
            context = {"logger"         : log,
                       "install_dir"    : install_dir,
                       "dependency_dir" : install_dir+dependencies[cDep]["name"]+"/",
                       "cwd"            : "{0}/{1}".format(install_dir, dependencies[cDep]["name"])} 

            if sorted(dependencies[cDep]["stages"][cStage].keys()) != sorted(["name", "active", "steps"]):
                log.error("Invalid stage format")
                return False
            log.info(">>> Processing stage - \"{0}\"...".format(dependencies[cDep]["stages"][cStage]["name"]))
            if dependencies[cDep]["stages"][cStage]["active"] is False:
                log.info("stage is inactive")
                continue
            for cStep in range(0, len(dependencies[cDep]["stages"][cStage]["steps"])):
                log.info("step[{0}/{1}]".format(cStep + 1, len(dependencies[cDep]["stages"][cStage]["steps"])))
                if sorted(dependencies[cDep]["stages"][cStage]["steps"][cStep].keys()) != sorted(["command", "args"]):
                    log.error("Invalid command format")
                    return False
                
                if not os.path.isdir(install_dir+"/"+dependencies[cDep]["name"]):
                    os.makedirs(install_dir+"/"+dependencies[cDep]["name"])
                
                result = dependencies[cDep]["stages"][cStage]["steps"][cStep]["command"](
                    context,                                                        # context
                    dependencies[cDep]["stages"][cStage]["steps"][cStep]["args"])   # arguments

            #clean up context
            context.clear() 
    return True

def create_install_dir():
    if not os.path.isdir(install_dir):
        print("The \"{0}\" does not exist...".format(install_dir))
        try:
            print("Creating directory \"{0}\"...".format(install_dir))
            os.makedirs(install_dir)
        except OSError:
            print("Oops! Cannot create \"{0}\"...".format(install_dir))
            print("\tcheck the path is accessible or may be there is unsufficient access rights")
            print("..! TERMINATING !..")
            exit()
    else:
        print("The install dir that is \"{0}\" already exist. Creating logger".format(install_dir))


if __name__ == "__main__":

    create_install_dir()

    log = log_tools.Logger(install_dir, log_file_name)
    
    log.delimeter()

    if not check_required_paths(log):
        exit()

    if command.check_access_rights(log) is False:
        exit()

    log.delimeter()
    
    log.info("=== SWITCHES")
    activities_text = json.dumps(activities, sort_keys=False, indent=4).split("\n")
    for line in activities_text:
        log.info(line)
    
    log.delimeter()

    if not main():
        log.error()
        exit()

    log.success()
    
    log.delimeter()

    exit()
