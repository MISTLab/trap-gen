#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import sys, os

# these variables are mandatory
top = '.'
out = '_build_'
VERSION = '0.58'
APPNAME = 'trap'

# Checks, on 64 bit systems, that a given static library and the objects contained in it can
# be linked creating a shared library out of them: this because, on 64 bit systems, shared libraries
# can be created only using objects compiled with the -fPIC -DPIC flags
def check_dyn_library(ctx, libfile, libpaths):
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
        if os.path.splitext(libfile)[1] == ctx.env['cxxstlib_PATTERN'].split('%s')[1]:
            # Now lets check for the presence of symbols of type R_X86_64_32S:
            # in case we have an error.
            for libpath in libpaths:
                if os.path.exists(os.path.join(libpath, libfile)):
                    libDump = os.popen(ctx.env.OBJDUMP + ' -r ' + os.path.join(libpath, libfile)).readlines()
                    for line in libDump:
                        if 'R_X86_64_32S' in line:
                            return False
                    break
    return True

def build(ctx):
    ctx.recurse('cxx_writer')
    ctx.recurse('trap')

def configure(ctx):
    #############################################################
    # Validation of command line options
    #############################################################
    trap_license = ctx.options.trap_license.lower()
    if not trap_license in ['gpl', 'lgpl']:
        ctx.fatal('Specified ' + trap_license + ' TRAP license not valid: use either gpl or lgpl')
    ctx.env['LICENSE'] = trap_license

    if ctx.options.bfddir and trap_license == 'lgpl':
        ctx.fatal('--with-bfd option is not valid when lgpl license is specified')

    #############################################################
    # Small hack to adjust common usage of CPPFLAGS
    #############################################################
    for flag in ctx.env['CPPFLAGS']:
        if flag.startswith('-D'):
            ctx.env.append_unique('DEFINES', flag[2:])

    ctx.check_waf_version(mini='1.6.6')
    
    ctx.env['ENABLE_SHARED_64'] = True

    # Check for standard tools
    ctx.load('compiler_cxx')
    if ctx.env.CC_VERSION:
        if int(ctx.env.CC_VERSION[0]) > 3:
            ctx.msg('Checking for compiler version', 'ok - ' + '.'.join(ctx.env.CC_VERSION))
        else:
            ctx.fatal('Compiler Version ' + '.'.join(ctx.env.CC_VERSION) + ' too old: at least version 4.x required')
    ctx.find_program('objdump', mandatory=1, var='OBJDUMP')

    # Check for python
    ctx.load('python')
    ctx.check_python_version((2,4))

    #############################################################
    # Check support for profilers
    #############################################################
    if ctx.options.enable_gprof and ctx.options.enable_vprof:
        ctx.fatal('Only one profiler among gprof and vprof can be enabled at the same time')
    if ctx.options.enable_gprof:
        if not '-g' in ctx.env['CCFLAGS']:
            ctx.env.append_unique('CCFLAGS', '-g')
        if not '-g' in ctx.env['CXXFLAGS']:
            ctx.env.append_unique('CXXFLAGS', '-g')
        if '-fomit-frame-pointer' in ctx.env['CCFLAGS']:
            ctx.env['CCFLAGS'].remove('-fomit-frame-pointer')
        if '-fomit-frame-pointer' in ctx.env['CXXFLAGS']:
            ctx.env['CXXFLAGS'].remove('-fomit-frame-pointer')
        ctx.env.append_unique('CCFLAGS', '-pg')
        ctx.env.append_unique('CXXFLAGS', '-pg')
        ctx.env.append_unique('LINKFLAGS', '-pg')
        ctx.env.append_unique('STLINKFLAGS', '-pg')
    if ctx.options.enable_vprof:
        if not '-g' in ctx.env['CCFLAGS']:
            ctx.env.append_unique('CCFLAGS', '-g')
        if not '-g' in ctx.env['CXXFLAGS']:
            ctx.env.append_unique('CXXFLAGS', '-g')
        # I have to check for the vprof and papi libraries and for the
        # vmonauto_gcc.o object file
        vmonautoPath = ''
        if not ctx.options.vprofdir:
            ctx.check_cxx(lib='vmon', uselib_store='VPROF', mandatory=1)
            for directory in searchDirs:
                if 'vmonauto_gcc.o' in os.listdir(directory):
                    vmonautoPath = os.path.abspath(os.path.expanduser(os.path.expandvars(directory)))
                    break;
        else:
            ctx.check_cxx(lib='vmon', uselib_store='VPROF', mandatory=1, libpath = os.path.abspath(os.path.expanduser(os.path.expandvars(ctx.options.vprofdir))))
            ctx.env.append_unique('RPATH', ctx.env['LIBPATH_VPROF'])
            ctx.env.append_unique('LIBPATH', ctx.env['LIBPATH_VPROF'])
            vmonautoPath = ctx.env['LIBPATH_VPROF'][0]
        ctx.env.append_unique('LIB', 'vmon')

        if not ctx.options.papidir:
            ctx.check_cxx(lib='papi', uselib_store='PAPI', mandatory=1)
        else:
            ctx.check_cxx(lib='papi', uselib_store='PAPI', mandatory=1, libpath = os.path.abspath(os.path.expanduser(os.path.expandvars(ctx.options.papidir))))
            ctx.env.append_unique('RPATH', conf.env['LIBPATH_PAPI'])
            ctx.env.append_unique('LIBPATH', conf.env['LIBPATH_PAPI'])
        ctx.env.append_unique('LIB', 'papi')

        # now I check for the vmonauto_gcc.o object file
        taskEnv = ctx.env.copy()
        taskEnv.append_unique('LINKFLAGS', os.path.join(vmonautoPath, 'vmonauto_gcc.o'))
        ctx.check_cxx(fragment='int main(){return 0;}', uselib='VPROF', mandatory=1, env=taskEnv)
        ctx.env.append_unique('LINKFLAGS', os.path.join(vmonautoPath, 'vmonauto_gcc.o'))

    ##############################################################
    # Since I want to build fast simulators, if the user didn't
    # specify any flags I set optimized flags
    # NOTE: -march=native is available only for GCC > 4.2
    #############################################################
    if not ctx.env['CXXFLAGS'] and not ctx.env['CCFLAGS']:
        testFlags = ['-O2', '-pipe', '-finline-functions', '-ftracer', '-fomit-frame-pointer']
        if int(ctx.env['CC_VERSION'][0]) >= 4 and int(ctx.env['CC_VERSION'][1]) >= 2:
            testFlags.append('-march=native')
        if ctx.check_cxx(cxxflags=testFlags, msg='Checking for g++ optimization flags', mandatory=False) and ctx.check_cc(cflags=testFlags, msg='Checking for gcc optimization flags', mandatory=False):
            ctx.env.append_unique('CXXFLAGS', testFlags)
            ctx.env.append_unique('CCFLAGS', testFlags)
            ctx.env.append_unique('DEFINES', 'NDEBUG')
        else:
            testFlags = ['-O2', '-pipe', '-finline-functions', '-fomit-frame-pointer']
            if ctx.check_cxx(cxxflags=testFlags, msg='Checking for g++ optimization flags') and ctx.check_cc(cflags=testFlags, msg='Checking for gcc optimization flags'):
                ctx.env.append_unique('CXXFLAGS', testFlags)
                ctx.env.append_unique('CCFLAGS', testFlags)
                ctx.env.append_unique('DEFINES', 'NDEBUG')

        permissiveFlags = ['-fpermissive']
        if ctx.check_cxx(cxxflags=permissiveFlags, msg='Checking for g++ -fpermissive flag') and ctx.check_cc(cflags=permissiveFlags, msg='Checking for gcc -fpermissive flag'):
            ctx.env.append_unique('CXXFLAGS', permissiveFlags)
            ctx.env.append_unique('CCFLAGS', permissiveFlags)

    ########################################
    # Check for special gcc flags
    ########################################
    ctx.env.append_unique('CXXFLAGS', '-fstrict-aliasing')
    ctx.env.append_unique('CCFLAGS', '-fstrict-aliasing')
    ctx.env.append_unique('CXXFLAGS', '-fPIC')
    ctx.env.append_unique('CCFLAGS', '-fPIC')
    ctx.env.append_unique('DEFINES', 'PIC')
    ctx.env.append_unique('LINKFLAGS', '-fPIC')
    if sys.platform != 'darwin':
        ctx.env.append_unique('LINKFLAGS', '-Wl,-E')
    else:
        ctx.env.append_unique('LINKFLAGS', ['-undefined', 'suppress', '-flat_namespace'])

    if ctx.env['CFLAGS']:
        ctx.check_cc(cflags=ctx.env['CFLAGS'], mandatory=1, msg='Checking for C compilation flags')
    if ctx.env['CCFLAGS'] and ctx.env['CCFLAGS'] != ctx.env['CFLAGS']:
        ctx.check_cc(cflags=ctx.env['CCFLAGS'], mandatory=1, msg='Checking for C compilation flags')
    if ctx.env['CXXFLAGS']:
        ctx.check_cxx(cxxflags=ctx.env['CXXFLAGS'], mandatory=1, msg='Checking for C++ compilation flags')
    if ctx.env['LINKFLAGS']:
        ctx.check_cxx(linkflags=ctx.env['LINKFLAGS'], mandatory=1, msg='Checking for link flags')

    ########################################
    # Setting the host endianess
    ########################################
    if sys.byteorder == "little":
        ctx.env.append_unique('DEFINES', 'LITTLE_ENDIAN_BO')
        ctx.msg('Checking for host endianness', 'little')
    else:
        ctx.env.append_unique('DEFINES', 'BIG_ENDIAN_BO')
        ctx.msg('Checking for host endianness', 'big')

    ########################################
    # Check for boost libraries
    ########################################
    ctx.load('boost')
    boostLibs = 'regex thread program_options filesystem system'
    boostErrorMessage = 'Unable to find ' + boostLibs + ' boost libraries of at least version 1.35, please install them and/or specify their location with the --boost-includes and --boost-libs configuration options. It can also happen that you have more than one boost version installed in a system-wide location: in this case remove the unnecessary versions.'
    ctx.check_boost(lib=boostLibs, mandatory=True, errmsg = boostErrorMessage)
    if int(ctx.env.BOOST_VERSION.split('_')[1]) < 35:
        ctx.fatal(boostErrorMessage)

    #######################################################
    # Determining gcc search dirs
    #######################################################
    compilerExecutable = ''
    if len(ctx.env['CXX']):
        compilerExecutable = ctx.env['CXX'][0]
    elif len(ctx.env['CC']):
        compilerExecutable = ctx.env['CC'][0]
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
    ctx.msg('Determining gcc search path', 'ok')

    if trap_license == 'gpl':
        ###########################################################
        # Check for IBERTY library
        ###########################################################
        if ctx.options.bfddir:
            searchDirs = [os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(ctx.options.bfddir, 'lib'))))]

        import glob
        foundStatic = []
        foundShared = []
        for directory in searchDirs:
            foundShared += glob.glob(os.path.join(directory, ctx.env['cxxshlib_PATTERN'].split('%s')[0] + 'iberty*' + ctx.env['cxxshlib_PATTERN'].split('%s')[1]))
            foundStatic += glob.glob(os.path.join(directory, ctx.env['cxxstlib_PATTERN'].split('%s')[0] + 'iberty*' + ctx.env['cxxstlib_PATTERN'].split('%s')[1]))
        if not foundStatic and not foundShared:
            ctx.fatal('IBERTY library not found, install binutils development package for your distribution and/or specify its localtion with the --with-bfd option')
        tempLibs = []
        staticPaths = []
        for ibertylib in foundStatic:
            tempLibs.append(os.path.splitext(os.path.basename(ibertylib))[0][len(ctx.env['cxxstlib_PATTERN'].split('%s')[0]):])
            staticPaths.append(os.path.split(ibertylib)[0])
        foundStatic = tempLibs
        tempLibs = []
        sharedPaths = []
        for ibertylib in foundShared:
            tempLibs.append(os.path.splitext(os.path.basename(ibertylib))[0][len(ctx.env['cxxshlib_PATTERN'].split('%s')[0]):])
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

        ctx.check_cxx(lib=iberty_lib_name, uselib_store='ELF_LIB', mandatory=1, libpath=searchPaths, errmsg='not found, use --with-bfd option', okmsg='ok ' + iberty_lib_name)

        if not foundShared:
            if not check_dyn_library(ctx, ctx.env['cxxstlib_PATTERN'] % iberty_lib_name, searchPaths):
                ctx.msg(conf.env['cxxstlib_PATTERN'] % iberty_lib_name + ' relocabilty', 'Found position dependent code: shared libraries disabled', color='YELLOW')
                ctx.env['ENABLE_SHARED_64'] = False

        ###########################################################
        # Check for BFD library and header
        ###########################################################
        if ctx.options.bfddir:
            searchDirs = [os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(ctx.options.bfddir, 'lib'))))]

        import glob
        foundStatic = []
        foundShared = []
        for directory in searchDirs:
            foundShared += glob.glob(os.path.join(directory, ctx.env['cxxshlib_PATTERN'].split('%s')[0] + 'bfd*' + ctx.env['cxxshlib_PATTERN'].split('%s')[1]))
            foundStatic += glob.glob(os.path.join(directory, ctx.env['cxxstlib_PATTERN'].split('%s')[0] + 'bfd*' + ctx.env['cxxstlib_PATTERN'].split('%s')[1]))
        if not foundStatic and not foundShared:
            ctx.fatal('BFD library not found, install binutils development package for your distribution and/or specify its localtion with the --with-bfd option')
        staticPaths = []
        tempLibs = []
        for bfdlib in foundStatic:
            tempLibs.append(os.path.splitext(os.path.basename(bfdlib))[0][len(ctx.env['cxxstlib_PATTERN'].split('%s')[0]):])
            staticPaths.append(os.path.split(bfdlib)[0])
        foundStatic = tempLibs
        tempLibs = []
        sharedPaths = []
        for bfdlib in foundShared:
            tempLibs.append(os.path.splitext(os.path.basename(bfdlib))[0][len(ctx.env['cxxshlib_PATTERN'].split('%s')[0]):])
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

        ctx.check_cxx(lib=bfd_lib_name, use='ELF_LIB', uselib_store='ELF_LIB', mandatory=1, libpath=searchPaths, errmsg='not found, use --with-bfd option', okmsg='ok ' + bfd_lib_name)

        if not foundShared:
            if not check_dyn_library(ctx, ctx.env['cxxstlib_PATTERN'] % bfd_lib_name, searchPaths):
                ctx.msg(ctx.env['cxxstlib_PATTERN'] % bfd_lib_name + ' relocabilty', 'Found position dependent code: shared libraries disabled', color='YELLOW')
                ctx.env['ENABLE_SHARED_64'] = False

        if ctx.options.bfddir:
            ctx.check_cxx(header_name='bfd.h', use='ELF_LIB', uselib_store='ELF_LIB', mandatory=1, includes=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(ctx.options.bfddir, 'include'))))])
        else:
            ctx.check_cxx(header_name='bfd.h', use='ELF_LIB', uselib_store='ELF_LIB', mandatory=1)

        # Little hack now: I have to revert the ELF_LIB library order, so that libbfd comes
        # before libiberty
        ctx.env['LIB_ELF_LIB'].reverse()

        ###########################################################
        # Check for Binutils version
        ###########################################################
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
        ctx.check_cxx(fragment=binutilsVerCheck, msg='Checking for Binutils Version', use='ELF_LIB', mandatory=1, errmsg='Not supported version, use at least 2.16')

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
        if not ctx.check_cxx(fragment=binutilsDemangleCheck, msg='Checking for bfd_demangle', use='ELF_LIB', mandatory=0, okmsg='ok >= 2.18', errmsg='fail, reverting to cplus_demangle'):
            ctx.env.append_unique('DEFINES', 'OLD_BFD')

        #########################################################
        # Check for zlib and libintl, needed by binutils under
        # MAC-OSX
        #########################################################
        if sys.platform == 'darwin' or sys.platform == 'cygwin':
            ctx.check_cxx(lib='z', uselib_store='ELF_LIB', mandatory=1)
            ctx.check_cxx(lib='intl', uselib_store='ELF_LIB', mandatory=1, libpath=searchDirs)
    else:
        ###########################################################
        # Check for ELF library and headers
        ###########################################################
        ctx.check(header_name='cxxabi.h', features='cxx cprogram', mandatory=0)
        ctx.check_cxx(function_name='abi::__cxa_demangle', header_name="cxxabi.h", mandatory=0)
        if ctx.options.elfdir:
            elfIncPath=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(ctx.options.elfdir, 'include')))),
                        os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(ctx.options.elfdir, 'include', 'libelf'))))]
            elfLibPath=os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(ctx.options.elfdir, 'lib'))))
            if not os.path.exists(os.path.join(elfLibPath, ctx.env['cxxstlib_PATTERN'] % 'elf')) and  not os.path.exists(os.path.join(elfLibPath, ctx.env['cxxshlib_PATTERN'] % 'elf')):
                ctx.fatal('Unable to find libelf in specified path ' + elfLibPath)
            elfHeaderFound = False
            for path in elfIncPath:
                if os.path.exists(os.path.join(path, 'libelf.h')) and os.path.exists(os.path.join(path, 'gelf.h')):
                    elfHeaderFound = True
                    break
            if not elfHeaderFound:
                ctx.fatal('Unable to find libelf.h and/or gelf.h headers in specified path ' + str(elfIncPath))
            ctx.check_cxx(lib='elf', uselib_store='ELF_LIB', mandatory=1, libpath = elfLibPath, errmsg='no libelf found: either install it or use libfd, reverting to the GPL version of TRAP (--license=gpl configuration option), if allowed by your distribution')
            ctx.check(header_name='libelf.h', uselib='ELF_LIB', uselib_store='ELF_LIB', features='cxx cprogram', mandatory=1, includes = elfIncPath)
            ctx.check(header_name='gelf.h', uselib='ELF_LIB', uselib_store='ELF_LIB', features='cxx cprogram', mandatory=1, includes = elfIncPath)
        else:
            ctx.check_cxx(lib='elf', uselib_store='ELF_LIB', mandatory=1, errmsg='no libelf found: either install it or use libfd, reverting to the GPL version of TRAP (--license=gpl configuration option), if allowed by your distribution')
            ctx.check(header_name='libelf.h', uselib='ELF_LIB', uselib_store='ELF_LIB', features='cxx cprogram', mandatory=1)
            ctx.check(header_name='gelf.h', uselib='ELF_LIB', uselib_store='ELF_LIB', features='cxx cprogram', mandatory=1)
        ctx.check_cxx(fragment="""
            #include <libelf.h>

            int main(int argc, char *argv[]){
                void * funPtr = (void *)elf_getphdrnum;
                return 0;
            }
        """, msg='Checking for function elf_getphdrnum', use='ELF_LIB', mandatory=1, errmsg='Error, elf_getphdrnum not present in libelf; try to update to a newer version (e.g. at least version 0.144 of the libelf package distributed with Ubuntu)')
        

    #########################################################
    # Check for the winsock library
    #########################################################
    if sys.platform == 'cygwin':
        ctx.check_cxx(lib='ws2_32', uselib_store='WINSOCK', mandatory=1)

    ##################################################
    # Check for pthread library/flag
    ##################################################
    if not ctx.check_cxx(linkflags='-pthread') or not ctx.check_cc(cxxflags='-pthread') or sys.platform == 'cygwin':
        ctx.env.append_unique('LIB', 'pthread')
    else:
        ctx.env.append_unique('LINKFLAGS', '-pthread')
        ctx.env.append_unique('CXXFLAGS', '-pthread')
        ctx.env.append_unique('CFLAGS', '-pthread')
        ctx.env.append_unique('CCFLAGS', '-pthread')

    ##################################################
    # Is SystemC compiled? Check for SystemC library
    # Notice that we can't rely on lib-linux, therefore I have to find the actual platform...
    ##################################################
    syscpath = None
    if ctx.options.systemcdir:
        syscpath = ([os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(ctx.options.systemcdir, 'include'))))])
    elif 'SYSTEMC' in os.environ:
        syscpath = ([os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(os.environ['SYSTEMC'], 'include'))))])

    import glob
    sysclib = ''
    if syscpath:
        sysclib = glob.glob(os.path.join(os.path.abspath(os.path.join(syscpath[0], '..')), 'lib-*'))
    ctx.check_cxx(lib='systemc', uselib_store='SYSTEMC', mandatory=1, libpath=sysclib, errmsg='not found, use --with-systemc option')
    if not check_dyn_library(ctx, ctx.env['cxxstlib_PATTERN'] % 'systemc', sysclib):
        ctx.msg(ctx.env['cxxstlib_PATTERN'] % 'systemc' + ' relocabilty', 'Found position dependent code: shared libraries disabled', color='YELLOW')
        ctx.env['ENABLE_SHARED_64'] = False

    ######################################################
    # Check if systemc is compiled with quick threads or not
    ######################################################
    if not os.path.exists(os.path.join(syscpath[0] , 'sysc' , 'qt')):
        ctx.env.append_unique('DEFINES', 'SC_USE_PTHREADS')
    elif sys.platform == 'cygwin':
        ctx.fatal('SystemC under cygwin must be compiled with PThread support: recompile it using the "make pthreads" command')

    ##################################################
    # Check for SystemC header and test the library
    ##################################################
    if not sys.platform == 'cygwin':
        systemCerrmsg='Error, at least version 2.2.0 required'
    else:
        systemCerrmsg='Error, at least version 2.2.0 required.\nSystemC also needs patching under cygwin:\nplease controll that lines 175 and 177 of header systemc.h are commented;\nfor more details refer to http://www.ht-lab.com/howto/sccygwin/sccygwin.html\nhttp://www.dti.dk/_root/media/27325_SystemC_Getting_Started_artikel.pdf'
    ctx.check_cxx(fragment="""
        #include <systemc.h>
        int sc_main(int argc, char** argv){
            return 0;
        }
""", header_name='systemc.h', use='SYSTEMC', uselib_store='SYSTEMC', mandatory=1, includes=syscpath)
    ctx.check_cxx(fragment="""
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
""", msg='Checking for SystemC version', use='SYSTEMC', mandatory=1, errmsg=systemCerrmsg)

    if ctx.options.pyinstalldir:
       ctx.env['PYTHON_INSTALL_DIR'] = ctx.options.pyinstalldir
    if not ctx.env['PYTHONDIR'].startswith(ctx.env['PREFIX']):
        tempDir = ctx.env['PYTHONDIR'].split('/')
        try:
            tempDir.remove('')
        except:
            pass
        ctx.env['PYTHONDIR'] = os.path.sep.join(tempDir)
        ctx.env['PYTHONDIR'] = os.path.join(ctx.env['PREFIX'], ctx.env['PYTHONDIR'])

def options(ctx):

    build_options = ctx.add_option_group('General Build Options')

    # Generic Build Options
    ctx.load('python', option_group=build_options)
    ctx.load('compiler_c', option_group=build_options)
    ctx.load('compiler_cxx', option_group=build_options)
    ctx.load('boost', option_group=build_options)

    # Specify which type of license should be applied to TRAP library;
    # note that if GPL then libbfd shall we used, otherwise libelf, and
    # TRAP will be licensed LGPL
    ctx.add_option('--license', type='string', default='lgpl', help='Spcifies the License with which TRAP will be built [gpl, lgpl]', dest='trap_license' )

    # Python installation folder
    ctx.add_option('--py-install-dir', type='string', help='Folder where the python files will be installed', dest='pyinstalldir')

    # Specify SystemC path
    ctx.add_option('--with-systemc', type='string', help='SystemC installation directory', dest='systemcdir' )
    # Specify BFD library path
    ctx.add_option('--with-bfd', type='string', help='BFD installation directory', dest='bfddir' )
    # Specify libELF library path
    ctx.add_option('--with-elf', type='string', help='libELF installation directory', dest='elfdir' )
    # Specify support for profilers
    ctx.add_option('-P', '--gprof', default=False, action='store_true', help='Enables profiling with gprof profiler', dest='enable_gprof')
    ctx.add_option('-V', '--vprof', default=False, action='store_true', help='Enables profiling with vprof profiler', dest='enable_vprof')
    ctx.add_option('--with-vprof', type='string', help='vprof installation folder', dest='vprofdir')
    ctx.add_option('--with-papi', type='string', help='papi installation folder', dest='papidir')
