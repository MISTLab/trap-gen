#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import sys, Options

# configuration line for microsoft windows: python waf configure --with-systemc=C:\systemc-2.2.0 --with-bfd=C:\binutilsInstall --prefix=c:\trapInstall --boost-includes=C:\boost\boost_1_36_0 --boost-libs=C:\boost\boost_1_36_0\lib

# these variables are mandatory
srcdir = '.'
blddir = '_build_'
VERSION = '0.3'
APPNAME = 'trap'
import os

def build(bld):
    bld.add_subdirs('trap cxx_writer')

def configure(conf):
    # Check for standard tools
    usingMsvc = False
    try:
        conf.check_tool('gcc g++')
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

    ########################################
    # Check for special gcc flags
    ########################################
    if usingMsvc:
        conf.env.append_unique('LINKFLAGS','/FORCE:MULTIPLE')
        conf.env.append_unique('LINKFLAGS','/IGNORE:4006')
        conf.env.append_unique('STLINKFLAGS','/IGNORE:4006')
        conf.env.append_unique('CPPFLAGS','/D_CRT_SECURE_CPP_OVERLOAD_STANDARD_NAMES=1')
        conf.env.append_unique('CPPFLAGS','/D_CRT_SECURE_NO_WARNINGS=1')

    if conf.env['CPPFLAGS']:
        conf.check_cc(cflags=conf.env['CPPFLAGS'], mandatory=1)
    if conf.env['CCFLAGS']:
        conf.check_cc(cflags=conf.env['CCFLAGS'], mandatory=1)
    if conf.env['CXXFLAGS']:
        conf.check_cxx(cxxflags=conf.env['CXXFLAGS'], mandatory=1)
    if conf.env['LINKFLAGS']:
        conf.check_cxx(linkflags=conf.env['LINKFLAGS'], mandatory=1)
    if conf.env['STLINKFLAGS']:
        conf.check_cxx(linkflags=conf.env['STLINKFLAGS'], mandatory=1)

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
    conf.check_boost(lib=boostLibs, static='both', min_version='1.35.0', mandatory = 1, errmsg = 'Unable to find ' + boostLibs + ' boost libraries of at least version 1.35, please install them and specify their location with the --boost-includes and --boost-libs configuration options')

    ##################################################
    # Check for BFD library and header
    ##################################################
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
        localLibPath = os.path.join('/', 'usr','local','lib')
        if os.path.exists(localLibPath):
            searchDirs.append(os.path.abspath(localLibPath))
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
        if Options.options.bfddir:
            searchDirs.append(os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'lib')))))

        import glob
        foundStatic = []
        foundShared = []
        for directory in searchDirs:
            foundShared += glob.glob(os.path.join(directory, conf.env['shlib_PATTERN'].split('%s')[0] + 'bfd*' + conf.env['shlib_PATTERN'].split('%s')[1]))
            foundStatic += glob.glob(os.path.join(directory, conf.env['staticlib_PATTERN'].split('%s')[0] + 'bfd*' + conf.env['staticlib_PATTERN'].split('%s')[1]))
        if not foundStatic and not foundShared:
            conf.fatal('BFD library not found, install binutils development package for your distribution')
        tempLibs = []
        for bfdlib in foundStatic:
            tempLibs.append(os.path.basename(bfdlib)[3:os.path.basename(bfdlib).rfind('.')])
        foundStatic = tempLibs
        tempLibs = []
        for bfdlib in foundShared:
            tempLibs.append(os.path.basename(bfdlib)[3:os.path.basename(bfdlib).rfind('.')])
        foundShared = tempLibs
        bfd_lib_name = ''
        for bfdlib in foundStatic:
            if bfdlib in foundShared:
                bfd_lib_name = bfdlib
            break
        if not bfd_lib_name:
            if foundShared:
                bfd_lib_name = foundShared[0]
            else:
                bfd_lib_name = foundStatic[0]

        conf.check_cc(lib=bfd_lib_name, uselib_store='BFD', mandatory=1, libpath=searchDirs)
        if Options.options.bfddir:
            conf.check_cc(header_name='bfd.h', uselib_store='BFD', mandatory=1, includes=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'include'))))])
        else:
            conf.check_cc(header_name='bfd.h', uselib_store='BFD', mandatory=1)

    else:
        if not Options.options.bfddir:
            conf.fatal('Please specify the location of the BFD library using the --with-bfd configuration option')
        conf.check_cc(lib='bfd', uselib_store='BFD', mandatory=1, libpath=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'lib'))))])
        conf.check_cc(header_name='bfd.h', uselib_store='BFD', mandatory=1, includes=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'include'))))])

    ##################################################
    # Check for pthread library/flag
    ##################################################
    if not usingMsvc:
        if conf.check_cxx(linkflags='-pthread') is None or conf.check_cxx(cxxflags='-pthread') is None:
            conf.env.append_unique('LIB', 'pthread')
        else:
            conf.env.append_unique('LINKFLAGS', '-pthread')
            conf.env.append_unique('CXXFLAGS', '-pthread')
            conf.env.append_unique('CFLAGS', '-pthread')
            conf.env.append_unique('CCFLAGS', '-pthread')
            pthread_uselib = []
    else:
        pthread_uselib = []

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
    conf.check_cxx(lib='systemc', uselib_store='SYSTEMC', mandatory=1, libpath=sysclib)
    ######################################################
    # Check if systemc is compiled with quick threads or not
    ######################################################
    if not os.path.exists(os.path.join(syscpath[0] , 'sysc' , 'qt')):
        conf.env.append_unique('CPPFLAGS', '-DSC_USE_PTHREADS')

    ##################################################
    # Check for SystemC header and test the library
    ##################################################
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
    """, msg='Check for SystemC version (2.2.0 or greater required)', uselib='SYSTEMC', mandatory=1)

    if Options.options.pyinstalldir:
        conf.env['PYTHON_INSTALL_DIR'] = Options.options.pyinstalldir
    else:
        conf.env['PYTHON_INSTALL_DIR'] = conf.env['PYTHONDIR']

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
