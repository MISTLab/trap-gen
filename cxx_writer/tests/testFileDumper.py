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


import unittest
import writer_code
import os

class TestFileDumper(unittest.TestCase):

    def testDumpVariablesImpl(self):
        tempType = writer_code.TemplateType('std::map', [writer_code.intType, writer_code.stringType], 'map')
        tempVar = writer_code.Variable('pippo', tempType)
        dumper = writer_code.FileDumper('prova.cpp', False)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 4 + len(writer_code.banner.split('\n')) + len(writer_code.license.split('\n')) + len(writer_code.copyright.split('\n')) + 12)
        self.assertEqual(lines[44], '#include <map>\n')
        self.assertEqual(lines[45], '#include <string>\n')
        self.assertEqual(lines[47], 'std::map< int, std::string > pippo;\n')

    def testDumpVariablesHeader(self):
        tempType = writer_code.TemplateType('std::map', [writer_code.intType, writer_code.stringType], 'map')
        tempVar = writer_code.Variable('pippo', tempType)
        dumper = writer_code.FileDumper('prova.cpp', True)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 4 + len(writer_code.banner.split('\n')) + len(writer_code.license.split('\n')) + len(writer_code.copyright.split('\n')) + 16)
        self.assertEqual(lines[46], '#include <map>\n')
        self.assertEqual(lines[47], '#include <string>\n')
        self.assertEqual(lines[49], 'std::map< int, std::string > pippo;\n')

    def testDumpFunctionsHeader(self):
        tempType = writer_code.TemplateType('std::map', [writer_code.intType, writer_code.stringType], 'map')
        tempVar = writer_code.Function('pippo', writer_code.Code('std::map<int, std::string> myMap;\nmyMap[5] = \"ccc\";\nreturn myMap;'), tempType)
        dumper = writer_code.FileDumper('prova.cpp', True)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 4 + len(writer_code.banner.split('\n')) + len(writer_code.license.split('\n')) + len(writer_code.copyright.split('\n')) + 16)
        self.assertEqual(lines[46], '#include <map>\n')
        self.assertEqual(lines[47], '#include <string>\n')
        self.assertEqual(lines[49], 'std::map< int, std::string > pippo();\n')

    def testDumpFunctionsImpl(self):
        tempType = writer_code.TemplateType('std::map', [writer_code.intType, writer_code.stringType], 'map')
        tempVar = writer_code.Function('pippo', writer_code.Code('std::map<int, std::string> myMap;\nmyMap[5] = \"ccc\";\nreturn myMap;'), tempType)
        dumper = writer_code.FileDumper('prova.cpp', False)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 8 + len(writer_code.banner.split('\n')) + len(writer_code.license.split('\n')) + len(writer_code.copyright.split('\n')) + 12)
        self.assertEqual(lines[44], '#include <map>\n')
        self.assertEqual(lines[45], '#include <string>\n')
        self.assertEqual(lines[47], 'std::map< int, std::string > pippo(){\n')
        self.assertEqual(lines[48], '    std::map<int, std::string> myMap;\n')
        self.assertEqual(lines[49], '    myMap[5] = \"ccc\";\n')
        self.assertEqual(lines[50], '    return myMap;\n')
        self.assertEqual(lines[51], '}\n')

    def testTemplateFunctionsHeader(self):
        tempType = writer_code.TemplateType('std::map', [writer_code.intType, writer_code.stringType], 'map')
        tempVar = writer_code.Function('pippo', writer_code.Code('std::map<int, std::string> myMap;\nmyMap[5] = \"ccc\";\nreturn myMap;'), tempType, [], False, False, ['T'])
        dumper = writer_code.FileDumper('prova.cpp', True)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 8 + len(writer_code.banner.split('\n')) + len(writer_code.license.split('\n')) + len(writer_code.copyright.split('\n')) + 16)
        self.assertEqual(lines[46], '#include <map>\n')
        self.assertEqual(lines[47], '#include <string>\n')
        self.assertEqual(lines[49], 'template < typename T > std::map< int, std::string > pippo(){\n')
        self.assertEqual(lines[50], '    std::map<int, std::string> myMap;\n')
        self.assertEqual(lines[51], '    myMap[5] = \"ccc\";\n')
        self.assertEqual(lines[52], '    return myMap;\n')
        self.assertEqual(lines[53], '}\n')

    def testTemplateFunctionsImpl(self):
        tempType = writer_code.TemplateType('std::map', [writer_code.intType, writer_code.stringType], 'map')
        tempVar = writer_code.Function('pippo', writer_code.Code('std::map<int, std::string> myMap;\nmyMap[5] = \"ccc\";\nreturn myMap;'), tempType, [], False, ['T'])
        dumper = writer_code.FileDumper('prova.cpp', False)
        dumper.addMember(tempVar)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 3 + len(writer_code.banner.split('\n')) + len(writer_code.license.split('\n')) + len(writer_code.copyright.split('\n')) + 12)
        self.assertEqual(lines[44], '#include <map>\n')
        self.assertEqual(lines[45], '#include <string>\n')

    def testDumpClassHeader(self):
        intDecl = writer_code.intType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu')
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar])
        classDecl.addConstructor(publicConstr)
        dumper = writer_code.FileDumper('prova.cpp', True)
        dumper.addMember(classDecl)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 8 + len(writer_code.banner.split('\n')) + len(writer_code.license.split('\n')) + len(writer_code.copyright.split('\n')) + 16)
        self.assertEqual(lines[46], 'class MyClass{\n')
        self.assertEqual(lines[47], '    private:\n')
        self.assertEqual(lines[48], '    int pippo;\n')
        self.assertEqual(lines[49], '\n')
        self.assertEqual(lines[50], '    public:\n')
        self.assertEqual(lines[51], '    MyClass();\n')
        self.assertEqual(lines[52], '};\n')


    def testDumpClassImpl(self):
        intDecl = writer_code.intType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu')
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar])
        classDecl.addConstructor(publicConstr)
        dumper = writer_code.FileDumper('prova.cpp', False)
        dumper.addMember(classDecl)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 4 + len(writer_code.banner.split('\n')) + len(writer_code.license.split('\n')) + len(writer_code.copyright.split('\n')) + 12)
        self.assertEqual(lines[44], 'MyClass::MyClass(){\n')
        self.assertEqual(lines[45], '\n')
        self.assertEqual(lines[46], '}\n')


    def testDumpTemplateClassHeader(self):
        intDecl = writer_code.intType
        stringDecl = writer_code.stringType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu', [], ['std::string()'])
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar], [stringDecl], ['T'])
        classDecl.addConstructor(publicConstr)
        dumper = writer_code.FileDumper('prova.cpp', True)
        dumper.addMember(classDecl)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 12 + len(writer_code.banner.split('\n')) + len(writer_code.license.split('\n')) + len(writer_code.copyright.split('\n')) + 17)
        self.assertEqual(lines[48], 'template < typename T > class MyClass : public std::string{\n')
        self.assertEqual(lines[49], '    private:\n')
        self.assertEqual(lines[50], '    int pippo;\n')
        self.assertEqual(lines[51], '\n')
        self.assertEqual(lines[52], '    public:\n')
        self.assertEqual(lines[53], '    MyClass() : std::string(){\n')
        self.assertEqual(lines[54], '\n')
        self.assertEqual(lines[55], '    }\n')
        self.assertEqual(lines[56], '\n')
        self.assertEqual(lines[57], '};\n')

    def testDumpTemplateClassImpl(self):
        intDecl = writer_code.intType
        stringDecl = writer_code.stringType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu', [], ['std::string()'])
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar], [stringDecl], ['T'])
        classDecl.addConstructor(publicConstr)
        dumper = writer_code.FileDumper('prova.cpp', False)
        dumper.addMember(classDecl)
        dumper.write()
        testFile = open('prova.cpp', 'rt')
        lines = testFile.readlines()
        testFile.close()
        os.remove('prova.cpp')
        self.assertEqual(len(lines), 1 + len(writer_code.banner.split('\n')) + len(writer_code.license.split('\n')) + len(writer_code.copyright.split('\n')) + 13)

    def testEmptyFolder(self):
        folder = writer_code.Folder('')
        folder.create()
        os.remove('wscript')

    def testEmptyFolder(self):
        folder = writer_code.Folder('temp/try')
        folder.create()
        self.assert_(os.path.exists('temp/try/wscript'))
        os.remove('temp/try/wscript')
        import shutil
        shutil.rmtree('temp', True)

    def testDumpAll(self):
        folder = writer_code.Folder('temp')
        intDecl = writer_code.intType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu')
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar])
        classDecl.addConstructor(publicConstr)
        implFile = writer_code.FileDumper('prova.cpp', False)
        implFile.addMember(classDecl)
        headFile = writer_code.FileDumper('prova.hpp', True)
        headFile.addMember(classDecl)
        folder.addHeader(headFile)
        folder.addCode(implFile)
        folder.create()
        testImplFile = open('temp/prova.cpp', 'rt')
        lines = testImplFile.readlines()
        testImplFile.close()
        os.remove('temp/prova.cpp')
        self.assertEqual(len(lines), 4 + len(writer_code.banner.split('\n')) + len(writer_code.license.split('\n')) + len(writer_code.copyright.split('\n')) + 12)
        self.assertEqual(lines[44], 'MyClass::MyClass(){\n')
        self.assertEqual(lines[45], '\n')
        self.assertEqual(lines[46], '}\n')
        testHeadFile = open('temp/prova.hpp', 'rt')
        lines = testHeadFile.readlines()
        testHeadFile.close()
        os.remove('temp/prova.hpp')
        self.assertEqual(len(lines), 8 + len(writer_code.banner.split('\n')) + len(writer_code.license.split('\n')) + len(writer_code.copyright.split('\n')) + 16)
        self.assertEqual(lines[46], 'class MyClass{\n')
        self.assertEqual(lines[47], '    private:\n')
        self.assertEqual(lines[48], '    int pippo;\n')
        self.assertEqual(lines[49], '\n')
        self.assertEqual(lines[50], '    public:\n')
        self.assertEqual(lines[51], '    MyClass();\n')
        self.assertEqual(lines[52], '};\n')
        testWscriptFile = open('temp/wscript', 'rt')
        lines = testWscriptFile.readlines()
        testWscriptFile.close()
        os.remove('temp/wscript')
        self.assertEqual(len(lines), 14)
        self.assertEqual(lines[0], '#!/usr/bin/env python\n')
        self.assertEqual(lines[1], '\n')
        self.assertEqual(lines[2], 'import os\n')
        self.assertEqual(lines[3], '\n')
        self.assertEqual(lines[4], 'def build(bld):\n')
        self.assertEqual(lines[5], '    obj = bld.new_task_gen(\'cxx\', \'program\')\n')
        self.assertEqual(lines[6], '    obj.source=\"\"\"\n')
        self.assertEqual(lines[7], '        prova.cpp\n')
        self.assertEqual(lines[8], '    \"\"\"\n')
        self.assertEqual(lines[9], '    obj.uselib = \'BOOST BOOST_PROGRAM_OPTIONS BOOST_FILESYSTEM SYSTEMC TLM TRAP\'\n')
        self.assertEqual(lines[10], '    obj.includes = \'.\'\n')
        self.assertEqual(lines[11], '    obj.name = \'temp\'\n')
        self.assertEqual(lines[12], '    obj.target = \'temp\'\n')
        import shutil
        shutil.rmtree('temp', True)

    def testNestedDirs1(self):
        folder = writer_code.Folder('temp')
        nestFolder = writer_code.Folder('nested')
        folder.addSubFolder(nestFolder)
        folder.create()
        nestFolder.create()
        self.assert_(os.path.exists('temp/wscript'))
        self.assert_(os.path.exists('temp/nested/wscript'))
        os.remove('temp/wscript')
        os.remove('temp/nested/wscript')
        import shutil
        shutil.rmtree('temp', True)

    def testNestedDirs2(self):
        folder = writer_code.Folder('temp')
        nestFolder = writer_code.Folder('nested')
        folder.addSubFolder(nestFolder)
        nestFolder.create()
        folder.create()
        self.assert_(os.path.exists('temp/wscript'))
        self.assert_(os.path.exists('temp/nested/wscript'))
        os.remove('temp/wscript')
        os.remove('temp/nested/wscript')
        import shutil
        shutil.rmtree('temp', True)

    def testNestedDirsCommonPath(self):
        folder = writer_code.Folder('temp')
        nestFolder = writer_code.Folder('temp/nested')
        folder.addSubFolder(nestFolder)
        nestFolder.create()
        folder.create()
        os.remove('temp/wscript')
        os.remove('temp/nested/wscript')
        import shutil
        shutil.rmtree('temp', True)
