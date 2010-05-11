#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import sys, Options

# configuration line for microsoft windows: python waf configure --with-systemc=C:\systemc-2.2.0 --with-bfd=C:\binutilsInstall --prefix=c:\trapInstall --boost-includes=C:\boost\boost_1_36_0 --boost-libs=C:\boost\boost_1_36_0\lib

# these variables are mandatory
srcdir = '.'
blddir = '_build_'
VERSION = '0.4.5'
APPNAME = 'trap'
import os

# Checks, on 64 bit systems, that a given static library and the objects contained in it can
# be linked creating a shared library out of them: this because, on 64 bit systems, shared libraries
# can be created only using objects compiled with the -fPIC -DPIC flags
def check_dyn_library(conf, libfile, libpaths):
    # Now I have to check that the object files in the library are compiled with -fPIC option.
    # actually this only seems to affect 64 bits systems, while compilation on 32 bits only
    # yields warnings, but perfectly usable libraries. So ... I simply have to check if we are on
    # 64 bits systems and in case, I issue the objdump -r command: if there are symbols of type
    # R_X86_64_32S, then the library was compiled without the -fPIC option and it is not possible
    # to create a shared library out of it.

    # Are we on 64 bit systems?
    import struct
    if struct.calcsize("P") > 4:
        # are we actually processing a static library?
        if os.path.splitext(libfile)[1] == conf.env['staticlib_PATTERN'].split('%s')[1]:
            # Now lets check for the presence of symbols of type R_X86_64_32S:
            # in case we have an error.
            for libpath in libpaths:
                if os.path.exists(os.path.join(libpath, libfile)):
                    libDump = os.popen('objdump -r ' + os.path.join(libpath, libfile)).readlines()
                    for line in libDump:
                        if 'R_X86_64_32S' in line:
                            return False
                    break
    return True

def build(bld):
    bld.add_subdirs('trap cxx_writer')

def configure(conf):
    conf.env['ENABLE_SHARED_64'] = True

    # Check for standard tools
    usingMsvc = False
    try:
        conf.check_tool('gcc g++ osx')
	conf.find_program('objdump', mandatory=1)
    except:
        conf.check_message_2('Error in GCC compiler detection, reverting to Microsoft CL')
        conf.check_tool('msvc')
        usingMsvc = True
    conf.check_tool('misc')
    # Check for python
    conf.check_tool('python')
    conf.check_python_version((2,4))

    ##################################################################
    # Correcting custom environment vars to lists as required by waf
    ##################################################################
    if type(conf.env['CXX']) == type(''):
        conf.env['CXX'] = conf.env['CXX'].split(' ')
    if type(conf.env['CC']) == type(''):
        conf.env['CC'] = conf.env['CC'].split(' ')
    if type(conf.env['CCFLAGS']) == type(''):
        conf.env['CCFLAGS'] = conf.env['CCFLAGS'].split(' ')
    if type(conf.env['CXXFLAGS']) == type(''):
        conf.env['CXXFLAGS'] = conf.env['CXXFLAGS'].split(' ')
    if type(conf.env['CPPFLAGS']) == type(''):
        conf.env['CPPFLAGS'] = conf.env['CPPFLAGS'].split(' ')
    if type(conf.env['LINKFLAGS']) == type(''):
        conf.env['LINKFLAGS'] = conf.env['LINKFLAGS'].split(' ')
    if type(conf.env['STLINKFLAGS']) == type(''):
        conf.env['STLINKFLAGS'] = conf.env['STLINKFLAGS'].split(' ')

    #############################################################
    # Check support for profilers
    #############################################################
    if usingMsvc and (Options.options.enable_gprof or Options.options.enable_vprof):
        conf.fatal('vprof and gprof profilers can be enabled only under unix environments')
    if Options.options.enable_gprof and Options.options.enable_vprof:
        conf.fatal('Only one profiler among gprof and vprof can be enabled')
    if Options.options.enable_gprof:
        if not '-g' in conf.env['CCFLAGS']:
            conf.env.append_unique('CCFLAGS', '-g')
        if not '-g' in conf.env['CXXFLAGS']:
            conf.env.append_unique('CXXFLAGS', '-g')
        if '-fomit-frame-pointer' in conf.env['CCFLAGS']:
            conf.env['CCFLAGS'].remove('-fomit-frame-pointer')
        if '-fomit-frame-pointer' in conf.env['CXXFLAGS']:
            conf.env['CXXFLAGS'].remove('-fomit-frame-pointer')
        conf.env.append_unique('CCFLAGS', '-pg')
        conf.env.append_unique('CXXFLAGS', '-pg')
        conf.env.append_unique('LINKFLAGS', '-pg')
        conf.env.append_unique('STLINKFLAGS', '-pg')
    if Options.options.enable_vprof:
        if not '-g' in conf.env['CCFLAGS']:
            conf.env.append_unique('CCFLAGS', '-g')
        if not '-g' in conf.env['CXXFLAGS']:
            conf.env.append_unique('CXXFLAGS', '-g')
        # I have to check for the vprof and papi libraries and for the
        # vmonauto_gcc.o object file
        vmonautoPath = ''
        if not Options.options.vprofdir:
            conf.check_cxx(lib='vmon', uselib_store='VPROF', mandatory=1)
            for directory in searchDirs:
                if 'vmonauto_gcc.o' in os.listdir(directory):
                    vmonautoPath = os.path.abspath(os.path.expanduser(os.path.expandvars(directory)))
                    break;
        else:
            conf.check_cxx(lib='vmon', uselib_store='VPROF', mandatory=1, libpath = os.path.abspath(os.path.expanduser(os.path.expandvars(Options.options.vprofdir))))
            conf.env.append_unique('RPATH', conf.env['LIBPATH_VPROF'])
            conf.env.append_unique('LIBPATH', conf.env['LIBPATH_VPROF'])
            vmonautoPath = conf.env['LIBPATH_VPROF'][0]
        conf.env.append_unique('LIB', 'vmon')

        if not Options.options.papidir:
            conf.check_cxx(lib='papi', uselib_store='PAPI', mandatory=1)
        else:
            conf.check_cxx(lib='papi', uselib_store='PAPI', mandatory=1, libpath = os.path.abspath(os.path.expanduser(os.path.expandvars(Options.options.papidir))))
            conf.env.append_unique('RPATH', conf.env['LIBPATH_PAPI'])
            conf.env.append_unique('LIBPATH', conf.env['LIBPATH_PAPI'])
        conf.env.append_unique('LIB', 'papi')

        # now I check for the vmonauto_gcc.o object file
        taskEnv = conf.env.copy()
        taskEnv.append_unique('LINKFLAGS', os.path.join(vmonautoPath, 'vmonauto_gcc.o'))
        conf.check_cxx(fragment='int main(){return 0;}', uselib='VPROF', mandatory=1, env=taskEnv)
        conf.env.append_unique('LINKFLAGS', os.path.join(vmonautoPath, 'vmonauto_gcc.o'))

    ##############################################################
    # Since I want to build fast simulators, if the user didn't
    # specify any flags I set optimized flags
    #############################################################
    if not conf.env['CXXFLAGS'] and not conf.env['CCFLAGS']:
        testFlags = ['-O2', '-march=native', '-pipe', '-finline-functions', '-ftracer', '-fomit-frame-pointer']
        if conf.check_cxx(cxxflags=testFlags, msg='Checking for g++ optimization flags') and conf.check_cc(cflags=testFlags, msg='Checking for gcc optimization flags'):
            conf.env.append_unique('CXXFLAGS', testFlags)
            conf.env.append_unique('CCFLAGS', testFlags)
            conf.env.append_unique('CPPFLAGS', '-DNDEBUG')
        else:
            testFlags = ['-O2', '-pipe', '-finline-functions', '-fomit-frame-pointer']
            if conf.check_cxx(cxxflags=testFlags, msg='Checking for g++ optimization flags') and conf.check_cc(cflags=testFlags, msg='Checking for gcc optimization flags'):
                conf.env.append_unique('CXXFLAGS', testFlags)
                conf.env.append_unique('CCFLAGS', testFlags)
                conf.env.append_unique('CPPFLAGS', '-DNDEBUG')

    ########################################
    # Check for special gcc flags
    ########################################
    if usingMsvc:
        conf.env.append_unique('LINKFLAGS','/FORCE:MULTIPLE')
        conf.env.append_unique('LINKFLAGS','/IGNORE:4006')
        conf.env.append_unique('STLINKFLAGS','/IGNORE:4006')
        conf.env.append_unique('CPPFLAGS','/D_CRT_SECURE_CPP_OVERLOAD_STANDARD_NAMES=1')
        conf.env.append_unique('CPPFLAGS','/D_CRT_SECURE_NO_WARNINGS=1')
    else:
        conf.env.append_unique('CXXFLAGS', '-fstrict-aliasing')
        conf.env.append_unique('CCFLAGS', '-fstrict-aliasing')
        conf.env.append_unique('CXXFLAGS', '-fPIC')
        conf.env.append_unique('CCFLAGS', '-fPIC')
        conf.env.append_unique('CPPFLAGS', '-DPIC')
        conf.env.append_unique('LINKFLAGS', '-fPIC')
        if sys.platform != 'darwin':
            conf.env.append_unique('LINKFLAGS', '-Wl,-E')
        else:
            conf.env.append_unique('LINKFLAGS', ['-undefined', 'suppress', '-flat_namespace'])

    conf.check_cc(cflags=conf.env['CFLAGS'], mandatory=1, msg='Checking for C compilation flags')
    conf.check_cc(cflags=conf.env['CCFLAGS'], mandatory=1, msg='Checking for C compilation flags')
    conf.check_cxx(cxxflags=conf.env['CXXFLAGS'], mandatory=1, msg='Checking for G++ compilation flags')
    conf.check_cxx(linkflags=conf.env['LINKFLAGS'], mandatory=1, msg='Checking for link flags')

    ########################################
    # Setting the host endianess
    ########################################
    if sys.byteorder == "little":
        conf.env.append_unique('CPPFLAGS','-DLITTLE_ENDIAN_BO')
        conf.check_message_custom('endianness', '', 'little')
    else:
        conf.env.append_unique('CPPFLAGS','-DBIG_ENDIAN_BO')
        conf.check_message_custom('endianness', '', 'big')

    ########################################
    # Check for boost libraries
    ########################################
    conf.check_tool('boost')
    boostLibs = 'regex thread program_options filesystem system'
    conf.check_boost(lib=boostLibs, static='both', min_version='1.35.0', mandatory = 1, errmsg = 'Unable to find ' + boostLibs + ' boost libraries of at least version 1.35, please install them and/or specify their location with the --boost-includes and --boost-libs configuration options. It can also happen that you have more than one boost version installed in a system-wide location: in this case remove the unnecessary versions.')

    #######################################################
    # Determining gcc search dirs
    #######################################################
    if not usingMsvc:
        compilerExecutable = ''
        if len(conf.env['CXX']):
            compilerExecutable = conf.env['CXX'][0]
        elif len(conf.env['CC']):
            compilerExecutable = conf.env['CC'][0]
        else:
            conf.fatal('CC or CXX environment variables not defined: Error, is the compiler correctly detected?')

        result = os.popen(compilerExecutable + ' -print-search-dirs')
        searchDirs = []
        localLibPath = os.path.join('/', 'usr', 'lib64')
        if os.path.exists(localLibPath):
            searchDirs.append(localLibPath)
        localLibPath = os.path.join('/', 'usr', 'local', 'lib')
        if os.path.exists(localLibPath):
            searchDirs.append(localLibPath)
        localLibPath = os.path.join('/', 'sw', 'lib')
        if os.path.exists(localLibPath):
            searchDirs.append(localLibPath)
        gccLines = result.readlines()
        for curLine in gccLines:
            startFound = curLine.find('libraries: =')
            if startFound != -1:
                curLine = curLine[startFound + 12:-1]
                searchDirs_ = curLine.split(':')
                for i in searchDirs_:
                    if os.path.exists(i) and not os.path.abspath(i) in searchDirs:
                        searchDirs.append(os.path.abspath(i))
                break
        conf.check_message_custom('gcc search path', '', 'ok')

    ###########################################################
    # Check for BFD library and header
    ###########################################################
    if not usingMsvc:
        if Options.options.bfddir:
            searchDirs = [os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'lib'))))]

        import glob
        foundStatic = []
        foundShared = []
        for directory in searchDirs:
            foundShared += glob.glob(os.path.join(directory, conf.env['shlib_PATTERN'].split('%s')[0] + 'bfd*' + conf.env['shlib_PATTERN'].split('%s')[1]))
            foundStatic += glob.glob(os.path.join(directory, conf.env['staticlib_PATTERN'].split('%s')[0] + 'bfd*' + conf.env['staticlib_PATTERN'].split('%s')[1]))
        if not foundStatic and not foundShared:
            conf.fatal('BFD library not found, install binutils development package for your distribution and/or specify its localtion with the --with-bfd option')
        staticPaths = []
        tempLibs = []
        for bfdlib in foundStatic:
            tempLibs.append(os.path.splitext(os.path.basename(bfdlib))[0][len(conf.env['staticlib_PATTERN'].split('%s')[0]):])
            staticPaths.append(os.path.split(bfdlib)[0])
        foundStatic = tempLibs
        tempLibs = []
        sharedPaths = []
        for bfdlib in foundShared:
            tempLibs.append(os.path.splitext(os.path.basename(bfdlib))[0][len(conf.env['shlib_PATTERN'].split('%s')[0]):])
            sharedPaths.append(os.path.split(bfdlib)[0])
        foundShared = tempLibs
        bfd_lib_name = ''
        for bfdlib in foundStatic:
            if bfdlib in foundShared:
                bfd_lib_name = bfdlib
                searchPaths = sharedPaths + staticPaths
                break
        if not bfd_lib_name:
            if foundShared:
                bfd_lib_name = foundShared[0]
                searchPaths = sharedPaths
            else:
                for bfdlib in foundStatic:
                    bfd_lib_name = bfdlib
                    if 'pic' in bfdlib:
                        break
                searchPaths = staticPaths

        conf.check_cc(lib=bfd_lib_name, uselib='BFD', uselib_store='BFD', mandatory=1, libpath=searchPaths, errmsg='not found, use --with-bfd option', okmsg='ok ' + bfd_lib_name)

        if not foundShared:
            if not check_dyn_library(conf, conf.env['staticlib_PATTERN'] % bfd_lib_name, searchPaths):
                conf.check_message_custom(conf.env['staticlib_PATTERN'] % bfd_lib_name + ' relocabilty', '', 'Found position dependent code: shared libraries disabled', color='YELLOW')
                conf.env['ENABLE_SHARED_64'] = False

        if Options.options.bfddir:
            conf.check_cc(header_name='bfd.h', uselib='BFD', uselib_store='BFD', mandatory=1, includes=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'include'))))])
        else:
            conf.check_cc(header_name='bfd.h', uselib='BFD', uselib_store='BFD', mandatory=1)

    ###########################################################
    # Check for IBERTY library
    ###########################################################
    if not usingMsvc:
        if Options.options.bfddir:
            searchDirs = [os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'lib'))))]

        import glob
        foundStatic = []
        foundShared = []
        for directory in searchDirs:
            foundShared += glob.glob(os.path.join(directory, conf.env['shlib_PATTERN'].split('%s')[0] + 'iberty*' + conf.env['shlib_PATTERN'].split('%s')[1]))
            foundStatic += glob.glob(os.path.join(directory, conf.env['staticlib_PATTERN'].split('%s')[0] + 'iberty*' + conf.env['staticlib_PATTERN'].split('%s')[1]))
        if not foundStatic and not foundShared:
            conf.fatal('IBERTY library not found, install binutils development package for your distribution and/or specify its localtion with the --with-bfd option')
        tempLibs = []
        staticPaths = []
        for ibertylib in foundStatic:
            tempLibs.append(os.path.splitext(os.path.basename(ibertylib))[0][len(conf.env['staticlib_PATTERN'].split('%s')[0]):])
            staticPaths.append(os.path.split(ibertylib)[0])
        foundStatic = tempLibs
        tempLibs = []
        sharedPaths = []
        for ibertylib in foundShared:
            tempLibs.append(os.path.splitext(os.path.basename(ibertylib))[0][len(conf.env['shlib_PATTERN'].split('%s')[0]):])
            sharedPaths.append(os.path.split(ibertylib)[0])
        foundShared = tempLibs
        iberty_lib_name = ''
        for ibertylib in foundStatic:
            if ibertylib in foundShared:
                iberty_lib_name = ibertylib
                searchPaths = sharedPaths + staticPaths
                break
        if not iberty_lib_name:
            if foundShared:
                iberty_lib_name = foundShared[0]
                searchPaths = sharedPaths
            else:
                for ibertylib in foundStatic:
                    iberty_lib_name = ibertylib
                    if 'pic' in ibertylib:
                        break
                searchPaths = staticPaths

        conf.check_cc(lib=iberty_lib_name, uselib_store='BFD', mandatory=1, libpath=searchPaths, errmsg='not found, use --with-bfd option', okmsg='ok ' + iberty_lib_name)

        if not foundShared:
            if not check_dyn_library(conf, conf.env['staticlib_PATTERN'] % iberty_lib_name, searchPaths):
                conf.check_message_custom(conf.env['staticlib_PATTERN'] % iberty_lib_name + ' relocabilty', '', 'Found position dependent code: shared libraries disabled', color='YELLOW')
                conf.env['ENABLE_SHARED_64'] = False

    ###########################################################
    # Check for Binutils version
    ###########################################################
    if not usingMsvc:
        # mandatory version checks
        binutilsVerCheck = """
            #include <cstdlib>
            extern "C" {
                #include <bfd.h>
            }

            int main(int argc, char** argv) {
                bfd_section *p = NULL;
                #ifndef bfd_is_target_special_symbol
                #error "too old BFD library"
                #endif
                return 0;
            };
"""
        conf.check_cxx(fragment=binutilsVerCheck, msg='Check for Binutils Version', uselib='BFD', mandatory=1, errmsg='Not supported version, use at least 2.16')

        # bfd_demangle only appears in 2.18
        binutilsDemangleCheck = """
            #include <cstdlib>
            extern "C" {
                #include <bfd.h>
            }

            int main(int argc, char** argv) {
                char * tempRet = bfd_demangle(NULL, NULL, 0);
                return 0;
            };
"""
        if not conf.check_cxx(fragment=binutilsDemangleCheck, msg='Check for bfd_demangle', uselib='BFD', mandatory=0, okmsg='ok >= 2.18', errmsg='fail, reverting to cplus_demangle'):
            conf.env.append_unique('CPPFLAGS', '-DOLD_BFD')            

    #########################################################
    # Check for zlib and libintl, needed by binutils under
    # MAC-OSX
    #########################################################
    if sys.platform == 'darwin' or sys.platform == 'cygwin':
        conf.check_cc(lib='z', uselib_store='BFD', mandatory=1)
        conf.check_cc(lib='intl', uselib_store='BFD', mandatory=1, libpath=searchDirs)

    #########################################################
    # Check for the winsock library
    #########################################################
    if sys.platform == 'cygwin':
        conf.check_cc(lib='ws2_32', uselib_store='WINSOCK', mandatory=1)

    ##################################################
    # Check for pthread library/flag
    ##################################################
    if not usingMsvc:
        if not conf.check_cxx(linkflags='-pthread') or not conf.check_cxx(cxxflags='-pthread') or sys.platform == 'cygwin':
            conf.env.append_unique('LIB', 'pthread')
        else:
            conf.env.append_unique('LINKFLAGS', '-pthread')
            conf.env.append_unique('CXXFLAGS', '-pthread')
            conf.env.append_unique('CFLAGS', '-pthread')
            conf.env.append_unique('CCFLAGS', '-pthread')

    ##################################################
    # Is SystemC compiled? Check for SystemC library
    # Notice that we can't rely on lib-linux, therefore I have to find the actual platform...
    ##################################################
    syscpath = None
    if Options.options.systemcdir:
        if usingMsvc:
            syscpath = ([os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.systemcdir, 'src'))))])
        else:
            syscpath = ([os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.systemcdir, 'include'))))])
    elif 'SYSTEMC' in os.environ:
        syscpath = ([os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(os.environ['SYSTEMC'], 'include'))))])

    import glob
    sysclib = ''
    if syscpath:
        if usingMsvc:
            sysclib = [os.path.abspath(os.path.join(syscpath[0], '..', 'msvc71', 'SystemC', 'Release'))]
        else:
            sysclib = glob.glob(os.path.join(os.path.abspath(os.path.join(syscpath[0], '..')), 'lib-*'))
    conf.check_cxx(lib='systemc', uselib_store='SYSTEMC', mandatory=1, libpath=sysclib, errmsg='not found, use --with-systemc option')
    if not check_dyn_library(conf, conf.env['staticlib_PATTERN'] % 'systemc', sysclib):
        conf.check_message_custom(conf.env['staticlib_PATTERN'] % 'systemc' + ' relocabilty', '', 'Found position dependent code: shared libraries disabled', color='YELLOW')
        conf.env['ENABLE_SHARED_64'] = False
    ######################################################
    # Check if systemc is compiled with quick threads or not
    ######################################################
    if not os.path.exists(os.path.join(syscpath[0] , 'sysc' , 'qt')):
        conf.env.append_unique('CPPFLAGS', '-DSC_USE_PTHREADS')
    elif sys.platform == 'cygwin':
        conf.fatal('SystemC under cygwin must be compiled with PThread support: recompile it using the "make pthreads" command')

    ##################################################
    # Check for SystemC header and test the library
    ##################################################
    if not sys.platform == 'cygwin':
        systemCerrmsg='Error, at least version 2.2.0 required'
    else:
        systemCerrmsg='Error, at least version 2.2.0 required.\nSystemC also needs patching under cygwin:\nplease controll that lines 175 and 177 of header systemc.h are commented;\nfor more details refer to http://www.ht-lab.com/howto/sccygwin/sccygwin.html\nhttp://www.dti.dk/_root/media/27325_SystemC_Getting_Started_artikel.pdf'
    conf.check_cxx(header_name='systemc.h', uselib='SYSTEMC', uselib_store='SYSTEMC', mandatory=1, includes=syscpath)
    conf.check_cxx(fragment="""
        #include <systemc.h>

        #ifndef SYSTEMC_VERSION
        #error SYSTEMC_VERSION not defined in file sc_ver.h
        #endif

        #if SYSTEMC_VERSION < 20070314
        #error Wrong SystemC version
        #endif

        extern "C" {
            int sc_main(int argc, char** argv) {
                wif_trace_file trace("");
                trace.set_time_unit(1, SC_NS);
                return 0;
            };
        }
""", msg='Check for SystemC version', uselib='SYSTEMC', mandatory=1, errmsg=systemCerrmsg)

    if Options.options.pyinstalldir:
        conf.env['PYTHON_INSTALL_DIR'] = Options.options.pyinstalldir
    if not conf.env['PYTHONDIR'].startswith(conf.env['PREFIX']):
        tempDir = conf.env['PYTHONDIR'].split('/')
        try:
            tempDir.remove('')
        except:
            pass
        conf.env['PYTHONDIR'] = os.path.sep.join(tempDir)
        conf.env['PYTHONDIR'] = os.path.join(conf.env['PREFIX'], conf.env['PYTHONDIR'])

def set_options(opt):

    build_options = opt.add_option_group('General Build Options')
    opt.tool_options('python', option_group=build_options) # options for disabling pyc or pyo compilation
    opt.tool_options('gcc', option_group=build_options)
    opt.tool_options('g++', option_group=build_options)
    opt.tool_options('compiler_cc')
    opt.tool_options('compiler_cxx')
    opt.add_option('--py-install-dir', type='string', help='Folder where the python files will be installed', dest='pyinstalldir')
    opt.tool_options('boost', option_group=build_options)
    # Specify SystemC path
    opt.add_option('--with-systemc', type='string', help='SystemC installation directory', dest='systemcdir' )
    # Specify BFD library path
    opt.add_option('--with-bfd', type='string', help='BFD installation directory', dest='bfddir' )
    # Specify support for profilers
    opt.add_option('-P', '--gprof', default=False, action='store_true', help='Enables profiling with gprof profiler', dest='enable_gprof')
    opt.add_option('-V', '--vprof', default=False, action='store_true', help='Enables profiling with vprof profiler', dest='enable_vprof')
    opt.add_option('--with-vprof', type='string', help='vprof installation folder', dest='vprofdir')
    opt.add_option('--with-papi', type='string', help='papi installation folder', dest='papidir')
