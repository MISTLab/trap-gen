# -*- coding: iso-8859-1 -*-
####################################################################################
#         ___        ___           ___           ___
#        /  /\      /  /\         /  /\         /  /\
#       /  /:/     /  /::\       /  /::\       /  /::\
#      /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
#     /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
#    /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
#   /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
#   \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
#        \  \:\   \  \:\        \  \:\        \  \:\
#         \  \ \   \  \:\        \  \:\        \  \:\
#          \__\/    \__\/         \__\/         \__\/
#
#   This file is part of TRAP.
#
#   TRAP is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this TRAP; if not, write to the
#   Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA.
#   or see <http://www.gnu.org/licenses/>.
#
#   (c) Luca Fossati, fossati@elet.polimi.it, fossati.l@gmail.com
#
####################################################################################

import os
import Writer
from Writer import printOnFile

class FileDumper:
    """Dumps a file; a file is composed of members which are the ones described
    in SimpleDecls and ClassDecls"""
    license = ''
    license_text = ''
    developer_name = ''
    developer_email = ''
    banner = ''

    def __init__(self, name, isHeader):
        self.name = name
        self.members = []
        self.isHeader = isHeader
        self.includes = []

    def addMember(self, member):
        try:
            self.members += list(member)
        except TypeError:
            self.members.append(member)

    def addInclude(self, include):
        if not include in self.includes:
            self.includes.append(include)

    def write(self):
        #First I write the license, comments etc..
        #then the includes and finally the members,
        #in the same order in which they are contained
        #inside self.members

        if FileDumper.developer_name or FileDumper.developer_email:
            copyright = '(c) ' + FileDumper.developer_name + ', ' + FileDumper.developer_email
        else:
            copyright = ''

        fileHnd = open(self.name, 'wt')
        printOnFile('/***************************************************************************\\', fileHnd)
        printOnFile(' *', fileHnd)
        for line in FileDumper.banner.split('\n'):
            printOnFile(' *   ' + line, fileHnd)
        printOnFile(' *', fileHnd)
        printOnFile(' *', fileHnd)
        for line in FileDumper.license_text.split('\n'):
            printOnFile(' *   ' + line, fileHnd)
        printOnFile(' *', fileHnd)
        printOnFile(' *', fileHnd)
        for line in copyright.split('\n'):
            printOnFile(' *   ' + line, fileHnd)
        printOnFile(' *', fileHnd)
        printOnFile('\\***************************************************************************/\n\n', fileHnd)

        # Now I can start priting the actual code: lets create the writer
        writer = Writer.CodeWriter(fileHnd)
        if self.isHeader:
            writer.write('#ifndef ' + self.name.replace('.','_').upper() + '\n')
            writer.write('#define ' + self.name.replace('.','_').upper() + '\n')
        # as a first thing I compute the includes and print them
        for member in self.members:
            try:
                for include in member.getIncludes():
                    if include and not include in self.includes:
                        self.includes.append(include)
            except AttributeError:
                pass
        if self.includes:
            writer.write('\n')
        for include in self.includes:
            include = include.lstrip()
            if include.startswith('#'):
                writer.write(include + '\n')
            elif include != self.name:
                writer.write('#include <' + include + '>\n')
        writer.write('\n')
        # Now I simply have to print in order all the members
        for member in self.members:
            if self.isHeader:
                try:
                    member.writeDeclaration(writer)
                except AttributeError:
                    pass
            else:
                try:
                    member.writeImplementation(writer)
                except AttributeError:
                    pass
        if self.isHeader:
            writer.write('\n\n#endif')
        writer.write('\n')
        fileHnd.close()

class Folder:
    """A collection of files; in addition to creating the
    specified folder and to populating it with files,
    it also creates the correct wscript for the compilation"""
    def __init__(self, path):
        if not path:
            path = '.'
        self.path = os.path.abspath(path)
        self.headers = []
        self.codeFiles = []
        self.subfolders = []
        self.mainFile = ''
        self.uselib_local = []

    def addHeader(self, header):
        self.headers.append(header)

    def addUseLib(self, library):
        self.uselib_local.append(library)

    def setMain(self, mainFile):
        self.mainFile = mainFile

    def addCode(self, codeFile):
        self.codeFiles.append(codeFile)

    def addSubFolder(self, subfolder):
        commonPart = os.path.commonprefix((subfolder.path, self.path))
        if commonPart == self.path:
            subfolder = subfolder.path[subfolder.path.find(commonPart) + 1:]
        else:
            subfolder.path = os.path.join(self.path, os.path.split(subfolder.path)[-1])
            subfolder = subfolder.path
        if subfolder and not subfolder in self.subfolders:
            self.subfolders.append(subfolder)

    def create(self, configure = False, tests = False, projectName = '', version = '', customOptions = []):
        # Creates the folder and populates it with files.
        # it also creates the appropriate wscript for the
        # compilation
        curDir = os.getcwd()
        curpath = os.path.split(self.path)
        for i in curpath:
            if not os.path.exists(i):
                os.mkdir(i)
            os.chdir(i)
        for header in self.headers:
            header.write()
        for codeFile in self.codeFiles:
            codeFile.write()
        # Now I can finally create the wscript for the compilation
        # of the current folder; note that event though the project is
        # small we need to create the configure part
        self.createWscript(configure, tests, projectName, version, customOptions)
        if configure:
            import shutil, sys
            wafPath = os.path.abspath(os.path.join(os.path.dirname(sys.modules['cxx_writer'].__file__), 'waf'))
            shutil.copy(wafPath, os.path.abspath(os.path.join('.', 'waf')))
        os.chdir(curDir)

    def createWscript(self, configure, tests, projectName, version, customOptions):
        wscriptFile = open('wscript', 'wt')
        printOnFile('#!/usr/bin/env python', wscriptFile)
        printOnFile('# -*- coding: iso-8859-1 -*-\n', wscriptFile)
        if configure:
            printOnFile('import sys, os\n', wscriptFile)
            printOnFile('# these variables are mandatory', wscriptFile)
            printOnFile('top = \'.\'', wscriptFile)
            printOnFile('out = \'_build_\'', wscriptFile)
            printOnFile('VERSION = \'' + version + '\'', wscriptFile)
            printOnFile('APPNAME = \'' + projectName + '\'', wscriptFile)
        else:
            printOnFile('import os\n', wscriptFile)
        if self.codeFiles or self.subfolders:
            printOnFile('\ndef build(bld):', wscriptFile)
            if self.subfolders:
                subFolds = []
                for fold in self.subfolders:
                    subFold = str(fold)[len(str(os.path.commonprefix([os.path.abspath(os.path.normpath(fold)),os.path.abspath(os.path.normpath(self.path))]))):]
                    if subFold.startswith(os.sep):
                        subFold = subFold[1:]
                    subFolds.append(subFold)
                printOnFile('    bld.recurse(\'' + ' '.join(subFolds) + '\')\n', wscriptFile)
            # The various build parameters
            if self.codeFiles:
                printOnFile('    sources = \"\"\"', wscriptFile)
                for codeFile in self.codeFiles:
                    if self.mainFile != codeFile.name:
                        printOnFile('        ' + codeFile.name, wscriptFile)
                printOnFile('    \"\"\"', wscriptFile)
                if tests:
                    printOnFile('    uselib = \'TRAP BOOST BOOST_UNIT_TEST_FRAMEWORK BOOST_PROGRAM_OPTIONS BOOST_THREAD BOOST_FILESYSTEM BOOST_SYSTEM ELF_LIB SYSTEMC TLM\'', wscriptFile)
                else:
                    printOnFile('    uselib = \'BOOST BOOST_THREAD BOOST_FILESYSTEM BOOST_SYSTEM SYSTEMC TLM TRAP\'', wscriptFile)
                if self.uselib_local:
                    printOnFile('    objects = \'' + ' '.join(self.uselib_local) + '\'', wscriptFile)
                    printOnFile('    includes = \'. ..\'', wscriptFile)
                else:
                    printOnFile('    objects = \'\'', wscriptFile)
                    printOnFile('    includes = \'.\'', wscriptFile)
                if self.mainFile:
                    printOnFile('    target = \'' + os.path.split(self.path)[-1] + '_objs\'\n', wscriptFile)
                else:
                    printOnFile('    target = \'' + os.path.split(self.path)[-1] + '\'\n', wscriptFile)
                # and here finally we build the code into program and/or objects
                buildArgumentString = 'source = sources, target = target, use = uselib + \' \' + objects, includes = includes)'
                if not self.mainFile:
                    printOnFile('    bld.program(' + buildArgumentString, wscriptFile)
                else:
                    printOnFile('    bld.objects(' + buildArgumentString, wscriptFile)

            if self.mainFile:
                printOnFile('    sources = \'' + self.mainFile + '\'', wscriptFile)
                printOnFile('    includes = \'.\'', wscriptFile)
                if tests:
                    printOnFile('    uselib = \'TRAP BOOST BOOST_UNIT_TEST_FRAMEWORK BOOST_THREAD BOOST_SYSTEM ELF_LIB SYSTEMC TLM\'', wscriptFile)
                else:
                    printOnFile('    uselib = \'TRAP BOOST BOOST_PROGRAM_OPTIONS BOOST_THREAD BOOST_FILESYSTEM BOOST_SYSTEM ELF_LIB SYSTEMC TLM\'', wscriptFile)
                printOnFile('    import sys', wscriptFile)
                printOnFile('    cppflags_custom = \'\'', wscriptFile)
                printOnFile('    if sys.platform == \'cygwin\':', wscriptFile)
                printOnFile('        cppflags_custom = \' -D__USE_W32_SOCKETS\'', wscriptFile)
                printOnFile('        uselib += \' WINSOCK\'', wscriptFile)
                printOnFile('    objects = \'' + ' '.join(self.uselib_local + [os.path.split(self.path)[-1]]) + '_objs\'', wscriptFile)
                printOnFile('    target = \'' + os.path.split(self.path)[-1] + '\'\n', wscriptFile)

                printOnFile('    bld.program(source = sources, target = target, use = uselib + \' \' + objects, includes = includes, defines = cppflags_custom)', wscriptFile)
        # Ok, here I need to insert the configure script if needed
        if configure:
            printOnFile('def check_trap_linking(ctx, libName, libPaths, symbol):', wscriptFile)
            printOnFile("""
    for libpath in libPaths:
        libFile = os.path.join(libpath, ctx.env['cxxshlib_PATTERN'].split('%s')[0] + 'libName' + ctx.env['cxxshlib_PATTERN'].split('%s')[1])
        if os.path.exists(libFile):
            libDump = os.popen(ctx.env.NM + ' -r ' + libFile).readlines()
            for line in libDump:
                if 'symbol' in line:
                    return True
            break
        libFile = os.path.join(libpath, ctx.env['cxxstlib_PATTERN'].split('%s')[0] + 'libName' + ctx.env['cxxstlib_PATTERN'].split('%s')[1])
        if os.path.exists(libFile):
            libDump = os.popen(ctx.env.NM + ' -r ' + libFile).readlines()
            for line in libDump:
                if 'symbol' in line:
                    return True
            break
    return False
""", wscriptFile)

            printOnFile('def configure(ctx):', wscriptFile)
            printOnFile("""
    ctx.find_program('nm', mandatory=1, var='NM')

    #############################################################
    # Small hack to adjust common usage of CPPFLAGS
    #############################################################
    for flag in ctx.env['CPPFLAGS']:
        if flag.startswith('-D'):
            ctx.env.append_unique('DEFINES', flag[2:])

    # Check for standard tools
    ctx.check_waf_version(mini='1.6.0')

    # Check for standard tools
    ctx.load('compiler_cxx')
    if ctx.env.CC_VERSION:
        if int(ctx.env.CC_VERSION[0]) > 3:
            ctx.msg('Checking for compiler version', 'ok - ' + '.'.join(ctx.env.CC_VERSION))
        else:
            ctx.fatal('Compiler Version' + '.'.join(ctx.env.CC_VERSION) + ' too old: at least version 4.x required')

    # Check for python
    ctx.load('python')

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
            ctx.env.append_unique('RPATH', ctx.env['LIBPATH_PAPI'])
            ctx.env.append_unique('LIBPATH', ctx.env['LIBPATH_PAPI'])
        ctx.env.append_unique('LIB', 'papi')

        # now I check for the vmonauto_gcc.o object file
        taskEnv = ctx.env.copy()
        taskEnv.append_unique('LINKFLAGS', os.path.join(vmonautoPath, 'vmonauto_gcc.o'))
        ctx.check_cxx(fragment='int main(){return 0;}', uselib='VPROF', mandatory=1, env=taskEnv)
        ctx.env.append_unique('LINKFLAGS', os.path.join(vmonautoPath, 'vmonauto_gcc.o'))

    ##############################################################
    # Since I want to build fast simulators, if the user didn't
    # specify any flags I set optimized flags
    #############################################################
    if not ctx.env['CXXFLAGS'] and not ctx.env['CCFLAGS']:
        testFlags = ['-O2', '-march=native', '-pipe', '-finline-functions', '-ftracer', '-fomit-frame-pointer']
        if ctx.check_cxx(cxxflags=testFlags, msg='Checking for g++ optimization flags') and ctx.check_cc(cflags=testFlags, msg='Checking for gcc optimization flags'):
            ctx.env.append_unique('CXXFLAGS', testFlags)
            ctx.env.append_unique('CCFLAGS', testFlags)
            ctx.env.append_unique('DEFINES', 'NDEBUG')
        else:
            testFlags = ['-O2', '-pipe', '-finline-functions', '-fomit-frame-pointer']
            if ctx.check_cxx(cxxflags=testFlags, msg='Checking for g++ optimization flags') and ctx.check_cc(cflags=testFlags, msg='Checking for gcc optimization flags'):
                ctx.env.append_unique('CXXFLAGS', testFlags)
                ctx.env.append_unique('CCFLAGS', testFlags)
                ctx.env.append_unique('DEFINES', 'NDEBUG')

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
    boostLibs = 'thread regex date_time program_options filesystem unit_test_framework system'
    ctx.check_boost(lib=boostLibs, static='both', mandatory=True, min_version='1.35.0', errmsg = 'Unable to find ' + boostLibs + ' boost libraries of at least version 1.35, please install them and/or specify their location with the --boost-includes and --boost-libs configuration options. It can also happen that you have more than one boost version installed in a system-wide location: in this case remove the unnecessary versions.')
    if not ctx.options.static_build:
        ctx.env.append_unique('RPATH', ctx.env['LIBPATH_BOOST_THREAD'])

    #######################################################
    # Determining gcc search dirs
    #######################################################
    compilerExecutable = ''
    if len(ctx.env['CXX']):
        compilerExecutable = ctx.env['CXX'][0]
    elif len(ctx.env['CC']):
        compilerExecutable = ctx.env['CC'][0]
    else:
        ctx.fatal('CC or CXX environment variables not defined: Error, is the compiler correctly detected?')

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

    ########################################
    # Parsing command options
    ########################################
    if not ctx.options.enable_tools:
        ctx.env.append_unique('DEFINES', 'DISABLE_TOOLS')
    if ctx.options.static_build:
        ctx.env['FULLSTATIC'] = True
    if ctx.options.enable_history:
        ctx.env.append_unique('DEFINES', 'ENABLE_HISTORY')

    ########################################
    # Adding the custom preprocessor macros
    ########################################
    """, wscriptFile)

    # Now I have to add the necessary definitions for each custon option
            for option in customOptions:
                printOnFile("    if ctx.options.define_" + option[1].lower() + ":", wscriptFile)
                printOnFile("        ctx.env.append_unique('DEFINES', '" + option[1] + "')", wscriptFile)
            if FileDumper.license == 'gpl':
                printOnFile("""

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

    if ctx.options.bfddir:
        ctx.check_cxx(header_name='bfd.h', use='ELF_LIB', uselib_store='ELF_LIB', mandatory=1, includes=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(ctx.options.bfddir, 'include'))))])
    else:
        ctx.check_cxx(header_name='bfd.h', use='ELF_LIB', uselib_store='ELF_LIB', mandatory=1)

    ###########################################################
    # Check for Binutils version
    ###########################################################
    # mandatory version checks
    binutilsVerCheck = '''
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
'''
    ctx.check_cxx(fragment=binutilsVerCheck, msg='Checking for Binutils Version', uselib='ELF_LIB', mandatory=1, errmsg='Not supported version, use at least 2.16')

    # bfd_demangle only appears in 2.18
    binutilsDemangleCheck = '''
        #include <cstdlib>
        extern "C" {
            #include <bfd.h>
        }

        int main(int argc, char** argv) {
            char * tempRet = bfd_demangle(NULL, NULL, 0);
            return 0;
        };
'''
    if not ctx.check_cxx(fragment=binutilsDemangleCheck, msg='Checking for bfd_demangle', use='ELF_LIB', mandatory=0, okmsg='ok >= 2.18', errmsg='fail, reverting to cplus_demangle'):
        ctx.env.append_unique('DEFINES', 'OLD_BFD')

    #########################################################
    # Check for zlib and libintl, needed by binutils under
    # MAC-OSX
    #########################################################
    if sys.platform == 'darwin' or sys.platform == 'cygwin':
        ctx.check_cxx(lib='z', uselib_store='ELF_LIB', mandatory=1)
        ctx.check_cxx(lib='intl', uselib_store='ELF_LIB', mandatory=1, libpath=searchDirs)
""", wscriptFile)
            else:
                printOnFile("""
    ###########################################################
    # Check for ELF library and headers
    ###########################################################
    ctx.check(header_name='cxxabi.h', features='cxx cprogram', mandatory=0)
    ctx.check_cxx(function_name='abi::__cxa_demangle', header_name="cxxabi.h", mandatory=0)
    if ctx.options.elfdir:
        elfIncPath=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(ctx.options.elfdir, 'include'))))]
        elfLibPath=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(ctx.options.elfdir, 'lib'))))]
        ctx.check_cxx(lib='elf', uselib_store='ELF_LIB', mandatory=1, libpath = elfLibPath)
        ctx.check(header_name='libelf.h', uselib='ELF_LIB', uselib_store='ELF_LIB', features='cxx cprogram', mandatory=1, includes = elfIncPath)
        ctx.check(header_name='gelf.h', uselib='ELF_LIB', uselib_store='ELF_LIB', features='cxx cprogram', mandatory=1, includes = elfIncPath)
    else:
        ctx.check_cxx(lib='elf', uselib_store='ELF_LIB', mandatory=1)
        ctx.check(header_name='libelf.h', uselib='ELF_LIB', uselib_store='ELF_LIB', features='cxx cprogram', mandatory=1)
        ctx.check(header_name='gelf.h', uselib='ELF_LIB', uselib_store='ELF_LIB', features='cxx cprogram', mandatory=1)
    ctx.check_cxx(fragment='''
        #include <libelf.h>

        int main(int argc, char *argv[]){
            void * funPtr = (void *)elf_getphdrnum;
            return 0;
        }
    ''', msg='Checking for elf_getphdrnum function', use='ELF_LIB', mandatory=1, errmsg='Error, elf_getphdrnum not present in libelf; try to update to a newest version')
""", wscriptFile)

            printOnFile("""

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
    # First I set the clafgs needed by TLM 2.0 for including systemc dynamic process
    # creation
    ctx.env.append_unique('DEFINES','SC_INCLUDE_DYNAMIC_PROCESSES')
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
        systemCerrmsg='Error, at least version 2.2.0 required.\\nSystemC also needs patching under cygwin:\\nplease controll that lines 175 and 177 of header systemc.h are commented;\\nfor more details refer to http://www.ht-lab.com/howto/sccygwin/sccygwin.html\\nhttp://www.dti.dk/_root/media/27325_SystemC_Getting_Started_artikel.pdf'
    ctx.check_cxx(header_name='systemc.h', use='SYSTEMC', uselib_store='SYSTEMC', mandatory=1, includes=syscpath)
    ctx.check_cxx(fragment='''
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
''', msg='Checking for SystemC version', use='SYSTEMC', mandatory=1, errmsg=systemCerrmsg)

    ##################################################
    # Check for TLM header
    ##################################################
    tlmPath = ''
    if ctx.options.tlmdir:
        tlmPath = os.path.normpath(os.path.abspath(os.path.expanduser(os.path.expandvars(ctx.options.tlmdir))))
    elif 'TLM' in os.environ:
        tlmPath = os.path.normpath(os.path.abspath(os.path.expanduser(os.path.expandvars(os.environ['TLM']))))
    if not tlmPath.endswith('include'):
        tlmPath = os.path.join(tlmPath, 'include')
    tlmPath = [os.path.join(tlmPath, 'tlm')]

    ctx.check_cxx(header_name='tlm.h', use='SYSTEMC', uselib_store='TLM', mandatory=1, includes=tlmPath, errmsg='not found, use --with-tlm option')
    ctx.check_cxx(fragment='''
        #include <systemc.h>
        #include <tlm.h>

        #ifndef TLM_VERSION_MAJOR
        #error TLM_VERSION_MAJOR undefined in the TLM library
        #endif
        #ifndef TLM_VERSION_MINOR
        #error TLM_VERSION_MINOR undefined in the TLM library
        #endif
        #ifndef TLM_VERSION_PATCH
        #error TLM_VERSION_PATCH undefined in the TLM library
        #endif

        #if TLM_VERSION_MAJOR < 2
        #error Wrong TLM version; required 2.0
        #endif

        extern "C" int sc_main(int argc, char **argv){
            return 0;
        }
''', msg='Check for TLM version', use='SYSTEMC TLM', mandatory=1, errmsg='Error, at least version 2.0 required')

    ##################################################
    # Check for TRAP runtime libraries and headers
    ##################################################
    trapRevisionNum = 772
    trapDirLib = ''
    trapDirInc = ''
    trapLibErrmsg = 'not found, use --with-trap option. It might also be that the trap library is compiled '
    trapLibErrmsg += 'against libraries (bfd/libelf, boost, etc.) different from the ones being used now; in case '
    trapLibErrmsg += 'try recompiling trap library.'
    if ctx.options.trapdir:
        trapDirLib = os.path.abspath(os.path.expandvars(os.path.expanduser(os.path.join(ctx.options.trapdir, 'lib'))))
        trapDirInc = os.path.abspath(os.path.expandvars(os.path.expanduser(os.path.join(ctx.options.trapdir, 'include'))))
        ctx.check_cxx(lib='trap', use='BOOST_FILESYSTEM BOOST_THREAD BOOST_SYSTEM ELF_LIB SYSTEMC', uselib_store='TRAP', mandatory=1, libpath=trapDirLib, errmsg=trapLibErrmsg)
        foundShared = glob.glob(os.path.join(trapDirLib, ctx.env['cxxshlib_PATTERN'].split('%s')[0] + 'trap' + ctx.env['cxxshlib_PATTERN'].split('%s')[1]))
        if foundShared:
            ctx.env.append_unique('RPATH', ctx.env['LIBPATH_TRAP'])
""", wscriptFile)
            if FileDumper.license == 'gpl':
                printOnFile("""
        if not check_trap_linking(ctx, 'trap', ctx.env['LIBPATH_TRAP'], 'bfd_init'):
            ctx.fatal('TRAP library not linked with BFD library, probably not using the TRAP GPL version: properly recompile TRAP library')
""", wscriptFile)
            if not FileDumper.license == 'gpl':
                printOnFile("""
        if not check_trap_linking(ctx, 'trap', ctx.env['LIBPATH_TRAP'], 'elf_begin'):
            ctx.fatal('TRAP library not linked with libelf library, probably not using the TRAP LGPL version: properly recompile TRAP library')
""", wscriptFile)
            printOnFile("""

        ctx.check_cxx(header_name='trap.hpp', use='TRAP BOOST_FILESYSTEM BOOST_THREAD BOOST_SYSTEM ELF_LIB SYSTEMC', uselib_store='TRAP', mandatory=1, includes=trapDirInc)
        ctx.check_cxx(fragment='''
            #include "trap.hpp"

            #ifndef TRAP_REVISION
            #error TRAP_REVISION not defined in file trap.hpp
            #endif

            #if TRAP_REVISION < ''' + str(trapRevisionNum) + '''
            #error Wrong version of the TRAP runtime: too old
            #endif

            int main(int argc, char * argv[]){return 0;}
''', msg='Check for TRAP version', use='TRAP BOOST_FILESYSTEM BOOST_THREAD BOOST_SYSTEM ELF_LIB SYSTEMC', mandatory=1, includes=trapDirInc, errmsg='Error, at least revision ' + str(trapRevisionNum) + ' required')
    else:
        ctx.check_cxx(lib='trap', use='BOOST_FILESYSTEM BOOST_THREAD BOOST_SYSTEM ELF_LIB SYSTEMC', uselib_store='TRAP', mandatory=1, errmsg=trapLibErrmsg)
""", wscriptFile)
            if FileDumper.license == 'gpl':
                printOnFile("""
        if not check_trap_linking(ctx, 'trap', ctx.env['LIBPATH_TRAP'], 'bfd_init'):
            ctx.fatal('TRAP library not linked with BFD library, probably not using the TRAP GPL version: properly recompile TRAP library')
""", wscriptFile)
            if not FileDumper.license == 'gpl':
                printOnFile("""
        if not check_trap_linking(ctx, 'trap', ctx.env['LIBPATH_TRAP'], 'elf_begin'):
            ctx.fatal('TRAP library not linked with libelf library, probably not using the TRAP LGPL version: properly recompile TRAP library')
""", wscriptFile)
            printOnFile("""
        ctx.check_cxx(header_name='trap.hpp', use='TRAP BOOST_FILESYSTEM BOOST_THREAD BOOST_SYSTEM ELF_LIB SYSTEMC', uselib_store='TRAP', mandatory=1)
        ctx.check_cxx(fragment='''
            #include "trap.hpp"

            #ifndef TRAP_REVISION
            #error TRAP_REVISION not defined in file trap.hpp
            #endif

            #if TRAP_REVISION < ''' + str(trapRevisionNum) + '''
            #error Wrong version of the TRAP runtime: too old
            #endif

            int main(int argc, char * argv[]){return 0;}
''', msg='Check for TRAP version', use='TRAP ELF_LIB BOOST_FILESYSTEM BOOST_THREAD BOOST_SYSTEM SYSTEMC', mandatory=1, errmsg='Error, at least revision ' + str(trapRevisionNum) + ' required')

""", wscriptFile)
            # Finally now I can add the options
            printOnFile('def options(ctx):', wscriptFile)
            printOnFile("""
    build_options = ctx.add_option_group('General Build Options')
    ctx.load('python', option_group=build_options)
    ctx.load('compiler_c', option_group=build_options)
    ctx.load('compiler_cxx', option_group=build_options)
    ctx.load('boost', option_group=build_options)

    # Specify SystemC and TLM options
    ctx.add_option('--with-systemc', type='string', help='SystemC installation directory', dest='systemcdir' )
    ctx.add_option('--with-tlm', type='string', help='TLM installation directory', dest='tlmdir')
    ctx.add_option('--with-trap', type='string', help='TRAP libraries and headers installation directory', dest='trapdir')
""", wscriptFile)
            if FileDumper.license == 'gpl':
                printOnFile("""
    # Specify BFD and IBERTY libraries path
    ctx.add_option('--with-bfd', type='string', help='BFD installation directory', dest='bfddir' )
""", wscriptFile)
            else:
                printOnFile("""
    # Specify libELF library path
    ctx.add_option('--with-elf', type='string', help='libELF installation directory', dest='elfdir' )
""", wscriptFile)
            printOnFile("""
    ctx.add_option('--static', default=False, action="store_true", help='Triggers a static build, with no dependences from any dynamic library', dest='static_build')
    # Specify if OS emulation support should be compiled inside processor models
    ctx.add_option('-T', '--disable-tools', default=True, action="store_false", help='Disables support for support tools (debuger, os-emulator, etc.) (switch)', dest='enable_tools')
    # Specify if instruction history has to be kept
    ctx.add_option('-s', '--enable-history', default=False, action='store_true', help='Enables the history of executed instructions', dest='enable_history')
    # Specify support for the profilers: gprof, vprof
    ctx.add_option('-P', '--gprof', default=False, action='store_true', help='Enables profiling with gprof profiler', dest='enable_gprof')
    ctx.add_option('-V', '--vprof', default=False, action='store_true', help='Enables profiling with vprof profiler', dest='enable_vprof')
    ctx.add_option('--with-vprof', type='string', help='vprof installation folder', dest='vprofdir')
    ctx.add_option('--with-papi', type='string', help='papi installation folder', dest='papidir')""", wscriptFile)

            # Now I add the custom options, in case there are any
            if customOptions:
                printOnFile("    # Custom Options", wscriptFile)
            for option in customOptions:
                printOnFile("    ctx.add_option('--" + option[0] + "', default=False, action='store_true', help='Defines the " + option[1] + " directive', dest='define_" + option[1].lower() + "')", wscriptFile)

        wscriptFile.close()
