#!/usr/bin/env python

import sys, Options

# these variables are mandatory
srcdir = '.'
blddir = '_build_'
import os

def build(bld):
    bld.add_subdirs('trap cxx_writer')

def configure(conf):

    # I make sure that the search paths really exists and eliminates the non
    # existing ones (usefull in case your PC doesn't have the /usr/local/include
    # folder for example)
    import config_c

    incl_path = []
    for path in config_c.stdincpath:
        if os.path.exists(path):
            incl_path.append(path)
    config_c.stdincpath = incl_path
    lib_path = []

    config_c.stdlibpath += ['/usr/lib64/']
    for path in config_c.stdlibpath:
        if os.path.exists(path):
            lib_path.append(path)
    config_c.stdlibpath = lib_path

    # Set Optimized as the default compilation mode, enabled if no other is selected on the command line
    try:
        if Params.g_options.debug_level == '':
            Params.g_options.debug_level = "OPTIMIZED"
    except:
        pass

    # Check for standard tools
    conf.check_tool('g++ gcc misc')
    # Check for python
    conf.check_tool('python')
    conf.check_python_version((2,4))

    ########################################
    # Check for special gcc flags
    ########################################
    if not conf.check_flags(''):
        Params.fatal('gcc does not support the custom flags used. Please change the gcc version or the custom flags')

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
    boostconf = conf.create_boost_configurator()
    boostconf.lib = ['regex']
    boostconf.min_version = '1.35.0'
    boostconf.run()

    ##################################################
    # Check for BFD library and header
    ##################################################
    result = os.popen(conf.env['CXX'] + ' -print-search-dirs')
    curLine = result.readline()
    while curLine.find('libraries: =') == -1:
        curLine = result.readline()
        startFound = curLine.find('libraries: =')
        searchDirs = []
        if startFound != -1:
            curLine = curLine[startFound + 12:-1]
            searchDirs_ = curLine.split(':')
            for i in searchDirs_:
                if not os.path.abspath(i) in searchDirs:
                    searchDirs.append(os.path.abspath(i))
            break

    import glob
    foundStatic = []
    foundShared = []
    for directory in config_c.stdlibpath + searchDirs:
        foundShared += glob.glob(os.path.join(directory, conf.env['shlib_PATTERN'].split('%s')[0] + 'bfd*' + conf.env['shlib_PATTERN'].split('%s')[1]))
        foundStatic += glob.glob(os.path.join(directory, conf.env['staticlib_PATTERN'].split('%s')[0] + 'bfd*' + conf.env['staticlib_PATTERN'].split('%s')[1]))
    if not foundStatic and not foundShared:
        conf.fatal('BFD library not found')
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

    le = conf.create_library_enumerator()
    le.mandatory = 1
    le.uselib_store = 'BFD'
    le.name = bfd_lib_name
    le.message = 'BFD library not found'
    le.path = config_c.stdlibpath + searchDirs
    le.run()

    he = conf.create_header_configurator()
    he.mandatory = 1
    he.name = 'bfd.h'
    he.message = 'BFD header not found'
    he.uselib_store = 'BFD'
    he.run()

    ##################################################
    # Check for pthread library/flag
    ##################################################
    if conf.check_flags('-pthread'):
        conf.env.append_unique('LINKFLAGS', '-pthread')
        conf.env.append_unique('CXXFLAGS', '-pthread')
        conf.env.append_unique('CFLAGS', '-pthread')
        conf.env.append_unique('CCFLAGS', '-pthread')
        pthread_uselib = []
    else:
        le = conf.create_library_enumerator()
        le.mandatory = 1
        le.name = 'pthread'
        le.message = 'pthread library'
        pthread_uselib = ['pthread']
        conf.env.append_unique('LIB', le.run())

    ##################################################
    # Is SystemC compiled? Check for SystemC library
    # Notice that we can't rely on lib-linux, therefore I have to find the actual platform...
    ##################################################
    syscpath = None
    if Options.options.systemcdir:
        syscpath = ([os.path.abspath(os.path.join(Options.options.systemcdir, 'include'))])
    elif 'SYSTEMC' in os.environ:
        syscpath = ([os.path.abspath(os.path.join(os.environ['SYSTEMC'], 'include'))])

    le = conf.create_library_enumerator()
    le.mandatory = 1
    le.uselib_store = 'SYSTEMC'
    le.name = 'systemc'
    le.message = 'Library SystemC ver. 2.2.0 not found'
    le.nosystem = 1
    import glob
    if syscpath:
        sysclib = le.path = glob.glob(os.path.join(os.path.abspath(os.path.join(syscpath[0], '..')), 'lib-*'))
    le.run()
    ######################################################
    # Check if systemc is compiled with quick threads or not
    ######################################################
    if not os.path.exists(os.path.join(syscpath[0] , 'sysc' , 'qt')):
        conf.env.append_unique('CPPFLAGS', '-DSC_USE_PTHREADS')

    ##################################################
    # Check for SystemC header and test the library
    ##################################################
    he = conf.create_header_configurator()
    he.mandatory = 1
    he.header_code = """
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
    """
    he.path = syscpath
    he.name = "systemc.h"
    he.message = 'Library and Headers for SystemC ver. 2.2.0 or greater not found'
    he.uselib = 'SYSTEMC'
    he.uselib_store = 'SYSTEMC'
    he.lib_paths = sysclib
    he.run()

    ##################################################
    # Check for TLM header
    ##################################################
#    he = conf.create_header_configurator()
#    he.mandatory = 1
#    he.name = "tlm.h"
#    he.uselib = 'SYSTEMC'
#    he.lib_paths = sysclib
#    he.uselib_store = 'TLM'
#    he.header_code = """
#        #include <systemc.h>
#        #include <tlm.h>
#
#        #ifndef TLM_VERSION_MAJOR
#        #error TLM_VERSION_MAJOR undefined in the TLM library
#        #endif
#        #ifndef TLM_VERSION_MINOR
#        #error TLM_VERSION_MINOR undefined in the TLM library
#        #endif
#        #ifndef TLM_VERSION_PATCH
#        #error TLM_VERSION_PATCH undefined in the TLM library
#        #endif
#
#        #if TLM_VERSION_MAJOR < 2
#        #error Wrong TLM version; required 2.0
#        #endif
#
#        extern "C" int sc_main(int argc, char **argv){
#            return 0;
#        }
#    """
#    he.message = 'Library and Headers for TLM ver. 2.0 not found'
#    if Options.options.tlmdir:
#        he.path = [os.path.abspath(os.path.join(Options.options.tlmdir, 'tlm'))]
#    elif 'TLM' in os.environ:
#        he.path = [os.path.abspath(os.path.join(os.environ['TLM'], 'tlm'))]
#    he.run()


def set_options(opt):

    build_options = opt.add_option_group('General Build Options')
    opt.tool_options('python', option_group=build_options) # options for disabling pyc or pyo compilation
    opt.tool_options('gcc', option_group=build_options)
    opt.tool_options('g++', option_group=build_options)
    opt.tool_options('compiler_cc')
    opt.tool_options('compiler_cxx')
    opt.add_option('--py-install-dir', type='string', help='Folder where the python files will be installed', dest='pyinstalldir')
#    opt.tool_options('boost', option_group=build_options)
    # Specify SystemC and TLM path
    opt.add_option('--with-systemc', type='string', help='SystemC installation directory', dest='systemcdir' )
#    opt.add_option('--with-tlm', type='string', help='TLM installation directory', dest='tlmdir')
