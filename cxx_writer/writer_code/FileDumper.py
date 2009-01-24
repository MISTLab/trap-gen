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
        print >> fileHnd, '/***************************************************************************\\'
        print >> fileHnd, ' *'
        for line in banner.split('\n'):
            print >> fileHnd, ' *   ' + line
        print >> fileHnd, ' *'
        print >> fileHnd, ' *'
        for line in license.split('\n'):
            print >> fileHnd, ' *   ' + line
        print >> fileHnd, ' *'
        print >> fileHnd, ' *'
        for line in copyright.split('\n'):
            print >> fileHnd, ' *   ' + line
        print >> fileHnd, ' *'
        print >> fileHnd, '\\***************************************************************************/\n\n'
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

    def create(self, configure = False, tests = False):
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
        self.createWscript(configure, tests)
        if configure:
            import shutil, sys
            wafPath = os.path.abspath(os.path.join(os.path.dirname(sys.modules['cxx_writer'].__file__), 'waf'))
            shutil.copy(wafPath, os.path.abspath(os.path.join('.', 'waf')))
        os.chdir(curDir)

    def createWscript(self, configure, tests):
        wscriptFile = open('wscript', 'wt')
        print >> wscriptFile, '#!/usr/bin/env python\n'
        if configure:
            print >> wscriptFile, 'import sys, Options\n'
            print >> wscriptFile, '# these variables are mandatory'
            print >> wscriptFile, 'srcdir = \'.\''
            print >> wscriptFile, 'blddir = \'_build_\''
        print >> wscriptFile, 'import os\n'
        if self.codeFiles or self.subfolders:
            print >> wscriptFile, 'def build(bld):'
            if self.subfolders:
                print >> wscriptFile, '    bld.add_subdirs(\'' + ' '.join([str(fold)[len(str(self.path)):] for fold in self.subfolders]) + '\')\n'
            if self.codeFiles:
                if not self.mainFile:
                    print >> wscriptFile, '    obj = bld.new_task_gen(\'cxx\', \'program\')'
                else:
                    print >> wscriptFile, '    obj = bld.new_task_gen(\'cxx\', \'staticlib\')'
                print >> wscriptFile, '    obj.source=\"\"\"'
                for codeFile in self.codeFiles:
                    if self.mainFile != codeFile.name:
                        print >> wscriptFile, '        ' + codeFile.name
                print >> wscriptFile, '    \"\"\"'
                if tests:
                    print >> wscriptFile, '    obj.uselib = \'BOOST BOOST_UNIT_TEST_FRAMEWORK BOOST_PROGRAM_OPTIONS BOOST_FILESYSTEM BOOST_THREAD SYSTEMC TLM TRAP\''
                else:
                    print >> wscriptFile, '    obj.uselib = \'BOOST BOOST_FILESYSTEM BOOST_THREAD SYSTEMC TLM TRAP\''
                print >> wscriptFile, '    obj.includes = \'.\''
                if self.uselib_local:
                    print >> wscriptFile, '    obj.uselib_local = \'' + ' '.join(self.uselib_local) + '\''
                if self.mainFile:
                    print >> wscriptFile, '    obj.export_incdirs = \'.\''
                print >> wscriptFile, '    obj.name = \'' + os.path.split(self.path)[-1] + '\''
                print >> wscriptFile, '    obj.target = \'' + os.path.split(self.path)[-1] + '\'\n'
            if self.mainFile:
                print >> wscriptFile, '    obj = bld.new_task_gen(\'cxx\', \'program\')'
                print >> wscriptFile, '    obj.source=\'' + self.mainFile + '\''
                if tests:
                    print >> wscriptFile, '    obj.uselib = \'BOOST BOOST_UNIT_TEST_FRAMEWORK BOOST_THREAD BOOST_SYSTEM SYSTEMC TLM TRAP BFD LIBERTY\''
                else:
                    print >> wscriptFile, '    obj.uselib = \'BOOST BOOST_PROGRAM_OPTIONS BOOST_THREAD BOOST_SYSTEM SYSTEMC TLM TRAP BFD LIBERTY\''
                print >> wscriptFile, '    obj.uselib_local = \'' + ' '.join(self.uselib_local + [os.path.split(self.path)[-1]]) + '\''
                print >> wscriptFile, '    obj.name = \'' + os.path.split(self.path)[-1] + '_main\''
                print >> wscriptFile, '    obj.target = \'' + os.path.split(self.path)[-1] + '\'\n'
        # Ok, here I need to insert the configure script if needed
        if configure:
            print >> wscriptFile, 'def configure(conf):'
            print >> wscriptFile, """
    # Check for standard tools
    conf.check_tool('g++ gcc misc')
    # Check for python
    conf.check_tool('python')
    conf.check_python_version((2,4))

    ########################################
    # Check for special gcc flags
    ########################################
    if conf.env['CPPFLAGS']:
        conf.check_cc(cflags=conf.env['CPPFLAGS'])
    if conf.env['CFLAGS']:
        conf.check_cc(cflags=conf.env['CFLAGS'])
    if conf.env['CXXFLAGS']:
        conf.check_cxx(cxxflags=conf.env['CXXFLAGS'])
    if conf.env['LINKFLAGS']:
        conf.check_cxx(linkflags=conf.env['LINKFLAGS'])

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
    conf.check_boost(lib='thread regex date_time program_options filesystem unit_test_framework', kind='STATIC_NOSTATIC', min_version='1.35.0')

    ###########################################################
    # Check for BFD library and header and for LIBERTY library
    ###########################################################
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
    for directory in searchDirs:
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

    if Options.options.static_build:
        conf.check_cc(lib='iberty', uselib_store='LIBERTY', mandatory=1, libpath=searchDirs)
    conf.check_cc(lib=bfd_lib_name, uselib='LIBERTY', uselib_store='BFD', mandatory=1, libpath=searchDirs)
    conf.check_cc(header_name='bfd.h', uselib='LIBERTY', uselib_store='BFD', mandatory=1)

    ##################################################
    # Check for pthread library/flag
    ##################################################
    if conf.check_cxx(linkflags='-pthread') is None or conf.check_cxx(cxxflags='-pthread') is None:
        conf.env.append_unique('LIB', 'pthread')
    else:
        conf.env.append_unique('LINKFLAGS', '-pthread')
        conf.env.append_unique('CXXFLAGS', '-pthread')
        conf.env.append_unique('CFLAGS', '-pthread')
        conf.env.append_unique('CCFLAGS', '-pthread')
        pthread_uselib = []

    ##################################################
    # Check for TRAP runtime libraries and headers
    ##################################################
    trapDirLib = ''
    trapDirInc = ''
    if Options.options.trapdir:
        trapDirLib = os.path.expandvars(os.path.expanduser(os.path.join(Options.options.trapdir, 'lib')))
        trapDirInc = os.path.expandvars(os.path.expanduser(os.path.join(Options.options.trapdir, 'include')))
    conf.check_cxx(lib='trap', uselib_store='TRAP', mandatory=1, libpath=trapDirLib)
    conf.check_cxx(header_name='trap.hpp', uselib='TRAP', uselib_store='TRAP', mandatory=1, includes=trapDirInc)
    conf.check_cxx(fragment='''
        #include "trap.hpp"

        #ifndef TRAP_REVISION
        #error TRAP_REVISION not defined in file trap.hpp
        #endif

        #if TRAP_REVISION < 63
        #error Wrong version of the TRAP runtime: too old
        #endif
        int main(int argc, char * argv[]){return 0;}
    ''', msg='Check for TRAP version', uselib='TRAP', mandatory=1)

    ##################################################
    # Is SystemC compiled? Check for SystemC library
    # Notice that we can't rely on lib-linux, therefore I have to find the actual platform...
    ##################################################
    # First I set the clafgs needed by TLM 2.0 for including systemc dynamic process
    # creation
    conf.env.append_unique('CPPFLAGS','-DSC_INCLUDE_DYNAMIC_PROCESSES')
    syscpath = None
    if Options.options.systemcdir:
        syscpath = ([os.path.abspath(os.path.join(Options.options.systemcdir, 'include'))])
    elif 'SYSTEMC' in os.environ:
        syscpath = ([os.path.abspath(os.path.join(os.environ['SYSTEMC'], 'include'))])

    import glob
    sysclib = ''
    if syscpath:
        sysclib = glob.glob(os.path.join(os.path.abspath(os.path.join(syscpath[0], '..')), 'lib-*'))
    conf.check_cxx(lib='systemc', uselib_store='SYSTEMC', mandatory=1, libpath=sysclib)

    if not os.path.exists(os.path.join(syscpath[0] , 'sysc' , 'qt')):
        conf.env.append_unique('CPPFLAGS', '-DSC_USE_PTHREADS')

    ##################################################
    # Check for SystemC header and test the library
    ##################################################
    conf.check_cxx(header_name='systemc.h', uselib='SYSTEMC', uselib_store='SYSTEMC', mandatory=1, includes=syscpath)
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
    ''', msg='Check for SystemC version (2.2.0 or greater required)', uselib='SYSTEMC', mandatory=1)

    ##################################################
    # Check for TLM header
    ##################################################
    tlmPath = ''
    if Options.options.tlmdir:
        tlmPath = [os.path.abspath(os.path.join(Options.options.tlmdir, 'tlm'))]
    elif 'TLM' in os.environ:
        tlmPath = [os.path.abspath(os.path.join(os.environ['TLM'], 'tlm'))]

    conf.check_cxx(header_name='tlm.h', uselib='SYSTEMC', uselib_store='TLM', mandatory=1, includes=tlmPath)
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
    ''', msg='Check for TLM version (2.0 or greater required)', uselib='SYSTEMC TLM', mandatory=1)

"""
            # Finally now I can add the options
            print >> wscriptFile, 'def set_options(opt):'
            print >> wscriptFile, """
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
    opt.add_option('--static', default=False, action="store_true", help='Triggers a static build, with no dependences from any dynamic library', dest='static_build')
    # Specify the options for the processor creation
    # Specify if OS emulation support should be compiled inside processor models
    opt.add_option('-T', '--disable-tools', default=True, action="store_false", help='Disables support for support tools (debuger, os-emulator, etc.) (switch)', dest='enable_tools')
"""
        wscriptFile.close()
