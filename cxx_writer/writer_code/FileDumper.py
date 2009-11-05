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
#   the Free Software Foundation; either version 2 of the License, or
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
#   (c) Luca Fossati, fossati@elet.polimi.it
#
####################################################################################


banner = r"""
         ___        ___           ___           ___
        /  /\      /  /\         /  /\         /  /\
       /  /:/     /  /::\       /  /::\       /  /::\
      /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
     /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
    /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
   /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
   \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
        \  \:\   \  \:\        \  \:\        \  \:\
         \  \ \   \  \:\        \  \:\        \  \:\
          \__\/    \__\/         \__\/         \__\/
"""

license = r"""
This file is part of TRAP.

TRAP is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program; if not, write to the
Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
or see <http://www.gnu.org/licenses/>.
"""

copyright = """(c) Luca Fossati, fossati@elet.polimi.it"""

import os
import Writer
from Writer import printOnFile

class FileDumper:
    """Dumps a file; a file is composed of members which are the ones described
    in SimpleDecls and ClassDecls"""
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
        fileHnd = open(self.name, 'wt')
        printOnFile('/***************************************************************************\\', fileHnd)
        printOnFile(' *', fileHnd)
        for line in banner.split('\n'):
            printOnFile(' *   ' + line, fileHnd)
        printOnFile(' *', fileHnd)
        printOnFile(' *', fileHnd)
        for line in license.split('\n'):
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

    def create(self, configure = False, tests = False, projectName = '', version = ''):
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
        self.createWscript(configure, tests, projectName, version)
        if configure:
            import shutil, sys
            wafPath = os.path.abspath(os.path.join(os.path.dirname(sys.modules['cxx_writer'].__file__), 'waf'))
            shutil.copy(wafPath, os.path.abspath(os.path.join('.', 'waf')))
        os.chdir(curDir)

    def createWscript(self, configure, tests, projectName, version):
        wscriptFile = open('wscript', 'wt')
        printOnFile('#!/usr/bin/env python', wscriptFile)
        printOnFile('# -*- coding: iso-8859-1 -*-\n', wscriptFile)
        if configure:
            printOnFile('import sys, Options\n', wscriptFile)
            printOnFile('# these variables are mandatory', wscriptFile)
            printOnFile('srcdir = \'.\'', wscriptFile)
            printOnFile('blddir = \'_build_\'', wscriptFile)
            printOnFile('VERSION = \'' + version + '\'', wscriptFile)
            printOnFile('APPNAME = \'' + projectName + '\'', wscriptFile)
        printOnFile('import os\n', wscriptFile)
        if self.codeFiles or self.subfolders:
            printOnFile('def build(bld):', wscriptFile)
            if self.subfolders:
                subFolds = []
                for fold in self.subfolders:
                    subFold = str(fold)[len(str(os.path.commonprefix([os.path.abspath(os.path.normpath(fold)),os.path.abspath(os.path.normpath(self.path))]))):]
                    if subFold.startswith(os.sep):
                        subFold = subFold[1:]
                    subFolds.append(subFold)
                printOnFile('    bld.add_subdirs(\'' + ' '.join(subFolds) + '\')\n', wscriptFile)
            if self.codeFiles:
                if not self.mainFile:
                    printOnFile('    obj = bld.new_task_gen(\'cxx\', \'program\')', wscriptFile)
                else:
                    printOnFile('    obj = bld.new_task_gen(\'cxx\')', wscriptFile)
                printOnFile('    obj.source=\"\"\"', wscriptFile)
                for codeFile in self.codeFiles:
                    if self.mainFile != codeFile.name:
                        printOnFile('        ' + codeFile.name, wscriptFile)
                printOnFile('    \"\"\"', wscriptFile)
                if tests:
                    printOnFile('    obj.uselib = \'BOOST BOOST_UNIT_TEST_FRAMEWORK BOOST_PROGRAM_OPTIONS BOOST_FILESYSTEM BOOST_SYSTEM BOOST_THREAD SYSTEMC TLM TRAP BFD LIBERTY\'', wscriptFile)
                else:
                    printOnFile('    obj.uselib = \'BOOST BOOST_FILESYSTEM BOOST_SYSTEM BOOST_THREAD SYSTEMC TLM TRAP\'', wscriptFile)

                if self.uselib_local:
                    printOnFile('    obj.add_objects = \'' + ' '.join(self.uselib_local) + '\'', wscriptFile)
                    printOnFile('    obj.includes = \'. ..\'', wscriptFile)
                else:
                    printOnFile('    obj.includes = \'.\'', wscriptFile)

                if self.mainFile:
                    printOnFile('    obj.export_incdirs = \'.\'', wscriptFile)
                printOnFile('    obj.name = \'' + os.path.split(self.path)[-1] + '\'', wscriptFile)
                printOnFile('    obj.target = \'' + os.path.split(self.path)[-1] + '\'\n', wscriptFile)
            if self.mainFile:
                printOnFile('    obj = bld.new_task_gen(\'cxx\', \'program\')', wscriptFile)
                printOnFile('    obj.source=\'' + self.mainFile + '\'', wscriptFile)
                printOnFile('    obj.includes = \'.\'', wscriptFile)
                if tests:
                    printOnFile('    obj.uselib = \'BOOST BOOST_UNIT_TEST_FRAMEWORK BOOST_THREAD BOOST_SYSTEM SYSTEMC TLM TRAP BFD LIBERTY\'', wscriptFile)
                else:
                    printOnFile('    obj.uselib = \'BOOST BOOST_PROGRAM_OPTIONS BOOST_THREAD BOOST_FILESYSTEM BOOST_SYSTEM SYSTEMC TLM TRAP BFD LIBERTY\'', wscriptFile)
                printOnFile('    obj.add_objects = \'' + ' '.join(self.uselib_local + [os.path.split(self.path)[-1]]) + '\'', wscriptFile)
                printOnFile('    obj.name = \'' + os.path.split(self.path)[-1] + '_main\'', wscriptFile)
                printOnFile('    obj.target = \'' + os.path.split(self.path)[-1] + '\'\n', wscriptFile)
        # Ok, here I need to insert the configure script if needed
        if configure:
            printOnFile('def configure(conf):', wscriptFile)
            printOnFile("""
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
    if type(conf.env['RPATH']) == type(''):
        conf.env['RPATH'] = conf.env['RPATH'].split(' ')

    ##############################################################
    # Since I want to build fast simulators, if the user didn't
    # specify any flags I set optimized flags
    #############################################################
    if not conf.env['CXXFLAGS'] and not conf.env['CCFLAGS']:
        testFlags = ['-O2', '-march=native', '-pipe', '-finline-functions', '-ftracer', '-fomit-frame-pointer']
        if conf.check_cxx(cxxflags=testFlags, msg='Checking for optimization flags') and conf.check_cc(cflags=testFlags, msg='Checking for optimization flags'):
            conf.env.append_unique('CXXFLAGS', testFlags)
            conf.env.append_unique('CCFLAGS', testFlags)
            conf.env.append_unique('CPPFLAGS', '-DNDEBUG')
        else:
            testFlags = ['-O2', '-pipe', '-finline-functions', '-fomit-frame-pointer']
            if conf.check_cxx(cxxflags=testFlags, msg='Checking for optimization flags') and conf.check_cc(cflags=testFlags, msg='Checking for optimization flags'):
                conf.env.append_unique('CXXFLAGS', testFlags)
                conf.env.append_unique('CCFLAGS', testFlags)
                conf.env.append_unique('CPPFLAGS', '-DNDEBUG')

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
        localLibPath = os.path.join('/', 'usr','local','lib')
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

    ########################################
    # Check for special gcc flags
    ########################################
    if usingMsvc:
        conf.env.append_unique('LINKFLAGS','/FORCE:MULTIPLE')
        conf.env.append_unique('LINKFLAGS','/IGNORE:4006')
        conf.env.append_unique('STLINKFLAGS','/IGNORE:4006')
        conf.env.append_unique('CPPFLAGS','/D_CRT_SECURE_CPP_OVERLOAD_STANDARD_NAMES=1')
        conf.env.append_unique('CPPFLAGS','/D_CRT_SECURE_NO_WARNINGS=1')

    conf.check_cc(cflags=conf.env['CFLAGS'], mandatory=1, msg='Checking for C compilation flags')
    conf.check_cc(cflags=conf.env['CCFLAGS'], mandatory=1, msg='Checking for C compilation flags')
    conf.check_cxx(cxxflags=conf.env['CXXFLAGS'], mandatory=1, msg='Checking for G++ compilation flags')
    conf.check_cxx(linkflags=conf.env['LINKFLAGS'], mandatory=1, msg='Checking for link flags')
    if conf.env['STLINKFLAGS']:
        conf.check_cxx(linkflags=conf.env['STLINKFLAGS'], mandatory=1, msg='Checking for link flags')

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
    # Pasring command options
    ########################################
    if not Options.options.enable_tools:
        conf.env.append_unique('CPPFLAGS','-DDISABLE_TOOLS')
    if Options.options.static_build:
        conf.env['FULLSTATIC'] = True

    ########################################
    # Check for boost libraries
    ########################################
    conf.check_tool('boost')
    conf.check_boost(lib='thread regex date_time program_options filesystem unit_test_framework system', static='both', min_version='1.35.0', mandatory = 1, errmsg = 'Unable to find boost libraries boost of at least version 1.35, please install them and specify their location with the --boost-includes and --boost-libs configuration options')
    if not Options.options.static_build:
        conf.env.append_unique('RPATH', conf.env['LIBPATH_BOOST_THREAD'])

    ###########################################################
    # Check for BFD library and header and for LIBERTY library
    ###########################################################
    if not usingMsvc:
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

        if Options.options.static_build:
            conf.check_cc(lib='iberty', uselib_store='LIBERTY', mandatory=1, libpath=searchDirs, errmsg='not found, use --with-bfd option')
        conf.check_cc(lib=bfd_lib_name, uselib_store='BFD', mandatory=1, libpath=searchDirs, errmsg='not found, use --with-bfd option')
        if Options.options.bfddir and foundShared:
            conf.env.append_unique('RPATH', os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'lib')))))
        if Options.options.bfddir:
            conf.check_cc(header_name='bfd.h', uselib_store='BFD', mandatory=1, includes=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'include'))))])
        else:
            conf.check_cc(header_name='bfd.h', uselib_store='BFD', mandatory=1)

    else:
        if not Options.options.bfddir:
            conf.fatal('Please specify the location of the BFD and IBERTY libraries using the --with-bfd configuration option')
        conf.check_cc(lib='iberty', uselib_store='LIBERTY', mandatory=1, libpath=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'lib'))))])
        conf.check_cc(lib='bfd', uselib_store='BFD', mandatory=1, libpath=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'lib'))))])
        conf.check_cc(lib='gcc', uselib_store='BFD', mandatory=1, libpath=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'lib'))))])
        conf.check_cc(lib='mingwex', uselib_store='BFD', mandatory=1, libpath=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'lib'))))])
        conf.check_cc(lib='user32', uselib_store='BFD', mandatory=1, libpath=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'lib'))))])
        conf.check_cc(lib='msvcr90', uselib_store='BFD', mandatory=1, libpath=[os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(Options.options.bfddir, 'lib'))))])
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
    # First I set the clafgs needed by TLM 2.0 for including systemc dynamic process
    # creation
    conf.env.append_unique('CPPFLAGS','-DSC_INCLUDE_DYNAMIC_PROCESSES')
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

    if not os.path.exists(os.path.join(syscpath[0] , 'sysc' , 'qt')):
        conf.env.append_unique('CPPFLAGS', '-DSC_USE_PTHREADS')

    ##################################################
    # Check for SystemC header and test the library
    ##################################################
    conf.check_cxx(header_name='systemc.h', uselib='SYSTEMC', uselib_store='SYSTEMC', mandatory=1, includes=syscpath, errmsg='not found, use --with-systemc option')
    conf.check_cxx(fragment='''
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
    ''', msg='Check for SystemC version', uselib='SYSTEMC', mandatory=1, errmsg='Error, at least version 2.2.0 required')

    ##################################################
    # Check for TLM header
    ##################################################
    tlmPath = ''
    if Options.options.tlmdir:
        tlmPath = os.path.normpath(os.path.abspath(os.path.expanduser(os.path.expandvars(Options.options.tlmdir))))
    elif 'TLM' in os.environ:
        tlmPath = os.path.normpath(os.path.abspath(os.path.expanduser(os.path.expandvars(os.environ['TLM']))))
    if not tlmPath.endswith('include'):
        tlmPath = os.path.join(tlmPath, 'include')
    tlmPath = [os.path.join(tlmPath, 'tlm')]

    conf.check_cxx(header_name='tlm.h', uselib='SYSTEMC', uselib_store='TLM', mandatory=1, includes=tlmPath, errmsg='not found, use --with-tlm option')
    conf.check_cxx(fragment='''
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
    ''', msg='Check for TLM version', uselib='SYSTEMC TLM', mandatory=1, errmsg='Error, at least version 2.0 required')

    ##################################################
    # Check for TRAP runtime libraries and headers
    ##################################################
    trapDirLib = ''
    trapDirInc = ''
    if Options.options.trapdir:
        trapDirLib = os.path.abspath(os.path.expandvars(os.path.expanduser(os.path.join(Options.options.trapdir, 'lib'))))
        trapDirInc = os.path.abspath(os.path.expandvars(os.path.expanduser(os.path.join(Options.options.trapdir, 'include'))))
        conf.check_cxx(lib='trap', uselib='BOOST_FILESYSTEM BOOST_THREAD BOOST_SYSTEM BFD SYSTEMC', uselib_store='TRAP', mandatory=1, libpath=trapDirLib, errmsg='not found, use --with-trap option')
        foundShared = glob.glob(os.path.join(trapDirLib, conf.env['shlib_PATTERN'].split('%s')[0] + 'trap' + conf.env['shlib_PATTERN'].split('%s')[1]))
        if foundShared:
            conf.env.append_unique('RPATH', conf.env['LIBPATH_TRAP'])
        conf.check_cxx(header_name='trap.hpp', uselib='TRAP BOOST_FILESYSTEM BOOST_THREAD BOOST_SYSTEM BFD SYSTEMC', uselib_store='TRAP', mandatory=1, includes=trapDirInc)
        conf.check_cxx(fragment='''
            #include "trap.hpp"

            #ifndef TRAP_REVISION
            #error TRAP_REVISION not defined in file trap.hpp
            #endif

            #if TRAP_REVISION < 420
            #error Wrong version of the TRAP runtime: too old
            #endif
            int main(int argc, char * argv[]){return 0;}
        ''', msg='Check for TRAP version', uselib='TRAP BOOST_FILESYSTEM BOOST_THREAD BOOST_SYSTEM BFD SYSTEMC', mandatory=1, includes=trapDirInc, errmsg='Error, at least revision 420 required')
    else:
        conf.check_cxx(lib='trap', uselib='BOOST_FILESYSTEM BOOST_THREAD BOOST_SYSTEM BFD SYSTEMC', uselib_store='TRAP', mandatory=1, errmsg='not found, use --with-trap option')
        conf.check_cxx(header_name='trap.hpp', uselib='BOOST_FILESYSTEM BOOST_THREAD BOOST_SYSTEM BFD SYSTEMC TRAP', uselib_store='TRAP', mandatory=1)
        conf.check_cxx(fragment='''
            #include "trap.hpp"

            #ifndef TRAP_REVISION
            #error TRAP_REVISION not defined in file trap.hpp
            #endif

            #if TRAP_REVISION < 420
            #error Wrong version of the TRAP runtime: too old
            #endif
            int main(int argc, char * argv[]){return 0;}
        ''', msg='Check for TRAP version', uselib='TRAP BOOST_FILESYSTEM BOOST_THREAD BOOST_SYSTEM BFD SYSTEMC', mandatory=1, errmsg='Error, at least revision 420 required')

""", wscriptFile)
            # Finally now I can add the options
            printOnFile('def set_options(opt):', wscriptFile)
            printOnFile("""
    build_options = opt.add_option_group('General Build Options')
    opt.tool_options('python', option_group=build_options) # options for disabling pyc or pyo compilation
    opt.tool_options('gcc', option_group=build_options)
    opt.tool_options('g++', option_group=build_options)
    opt.tool_options('compiler_cc')
    opt.tool_options('compiler_cxx')
    opt.tool_options('boost', option_group=build_options)
    # Specify SystemC and TLM path
    opt.add_option('--with-systemc', type='string', help='SystemC installation directory', dest='systemcdir' )
    opt.add_option('--with-tlm', type='string', help='TLM installation directory', dest='tlmdir')
    opt.add_option('--with-trap', type='string', help='TRAP libraries and headers installation directory', dest='trapdir')
    # Specify BFD and IBERTY libraries path
    opt.add_option('--with-bfd', type='string', help='BFD installation directory', dest='bfddir' )
    opt.add_option('--static', default=False, action="store_true", help='Triggers a static build, with no dependences from any dynamic library', dest='static_build')
    # Specify if OS emulation support should be compiled inside processor models
    opt.add_option('-T', '--disable-tools', default=True, action="store_false", help='Disables support for support tools (debuger, os-emulator, etc.) (switch)', dest='enable_tools')
    # Specify support for the profilers: gprof, vprof
    opt.add_option('-P', '--gprof', default=False, action="store_true", help='Enables profiling with gprof profiler', dest='enable_gprof')
    opt.add_option('-V', '--vprof', default=False, action="store_true", help='Enables profiling with vprof profiler', dest='enable_vprof')
    opt.add_option('--with-vprof', type='string', help='vprof installation folder', dest='vprofdir')
    opt.add_option('--with-papi', type='string', help='papi installation folder', dest='papidir')
""", wscriptFile)
        wscriptFile.close()
