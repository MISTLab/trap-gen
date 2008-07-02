####################################################################################
#                    ___           ___           ___
#        ___        /  /\         /  /\         /  /\
#       /  /\      /  /::\       /  /::\       /  /::\
#      /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
#     /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
#    /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
#   /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
#   \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
#        \  \:\   \  \:\        \  \:\        \  \:\
#         \__\/    \  \:\        \  \:\        \  \:\
#                   \__\/         \__\/         \__\/
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

class TestClassDecls(unittest.TestCase):
    def setUp(self):
        try:
            os.remove('prova.cpp')
        except:
            pass
        self.writer = writer_code.CodeWriter('prova.cpp')

    def tearDown(self):
        del self.writer
        os.remove('prova.cpp')

    def testEmptyClassImpl(self):
        classDecl = writer_code.ClassDeclaration('emptyClass')
        classDecl.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], 'class emptyClass{\n')
        self.assertEqual(lines[1], '};\n')

    def testEmptyClassDecl(self):
        classDecl = writer_code.ClassDeclaration('emptyClass')
        classDecl.writeImplementation(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 0)

    def testNormalDecl(self):
        intDecl = writer_code.intType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu')
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar])
        classDecl.addConstructor(publicConstr)
        classDecl.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0], 'class MyClass{\n')
        self.assertEqual(lines[1], '    private:\n')
        self.assertEqual(lines[2], '    int pippo;\n')
        self.assertEqual(lines[3], '\n')
        self.assertEqual(lines[4], '    public:\n')
        self.assertEqual(lines[5], '    MyClass();\n')
        self.assertEqual(lines[6], '};\n')

    def testNormalImpl(self):
        intDecl = writer_code.intType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu')
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar])
        classDecl.addConstructor(publicConstr)
        classDecl.writeImplementation(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], 'MyClass::MyClass(){\n')
        self.assertEqual(lines[1], '}\n')

    def testTemplateDecl(self):
        intDecl = writer_code.intType
        stringDecl = writer_code.stringType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu', [], ['std::string()'])
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar], [stringDecl], ['T'])
        classDecl.addConstructor(publicConstr)
        classDecl.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 8)
        self.assertEqual(lines[0], 'template < typename T > class MyClass : public std::string{\n')
        self.assertEqual(lines[1], '    private:\n')
        self.assertEqual(lines[2], '    int pippo;\n')
        self.assertEqual(lines[3], '\n')
        self.assertEqual(lines[4], '    public:\n')
        self.assertEqual(lines[5], '    MyClass() : std::string() {\n')
        self.assertEqual(lines[6], '    }\n')
        self.assertEqual(lines[7], '};\n')

    def testTemplateImpl(self):
        intDecl = writer_code.intType
        stringDecl = writer_code.stringType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu', [], ['std::string()'])
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar], [stringDecl], ['T'])
        classDecl.addConstructor(publicConstr)
        classDecl.writeImplementation(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 0)

    def testStaticAttrsDecl(self):
        intDecl = writer_code.intType
        stringDecl = writer_code.stringType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri', True, '0')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu', [], ['std::string()'])
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar], [stringDecl])
        classDecl.addConstructor(publicConstr)
        classDecl.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0], 'class MyClass : public std::string{\n')
        self.assertEqual(lines[1], '    private:\n')
        self.assertEqual(lines[2], '    static int pippo;\n')
        self.assertEqual(lines[3], '\n')
        self.assertEqual(lines[4], '    public:\n')
        self.assertEqual(lines[5], '    MyClass();\n')
        self.assertEqual(lines[6], '};\n')

    def testStaticAttrsImpl(self):
        intDecl = writer_code.intType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri', True, '0')
        emptyBody = writer_code.Code('')
        publicConstr = writer_code.Constructor(emptyBody, 'pu', [], ['std::string()'])
        classDecl = writer_code.ClassDeclaration('MyClass', [privateVar])
        classDecl.addConstructor(publicConstr)
        classDecl.writeImplementation(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], 'int MyClass::pippo = 0;\n')
        self.assertEqual(lines[1], 'MyClass::MyClass() : std::string() {\n')
        self.assertEqual(lines[2], '}\n')

    def testSCModuleDecl(self):
        intDecl = writer_code.intType
        stringDecl = writer_code.stringType
        module_nameDecl = writer_code.sc_module_nameType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('end_module();')
        publicConstr = writer_code.Constructor(emptyBody, 'pu', [writer_code.Parameter('name', module_nameDecl)], ['std::string()'])
        classDecl = writer_code.SCModule('MyClass', [privateVar], [stringDecl])
        classDecl.addConstructor(publicConstr)
        classDecl.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 8)
        self.assertEqual(lines[0], 'class MyClass : public std::string, public sc_module{\n')
        self.assertEqual(lines[1], '    private:\n')
        self.assertEqual(lines[2], '    int pippo;\n')
        self.assertEqual(lines[3], '\n')
        self.assertEqual(lines[4], '    public:\n')
        self.assertEqual(lines[5], '    SC_HAS_PROCESS( MyClass );\n')
        self.assertEqual(lines[6], '    MyClass( sc_module_name name );\n')
        self.assertEqual(lines[7], '};\n')

    def testSCModuleImpl(self):
        intDecl = writer_code.intType
        stringDecl = writer_code.stringType
        module_nameDecl = writer_code.sc_module_nameType
        privateVar = writer_code.Attribute('pippo', intDecl, 'pri')
        emptyBody = writer_code.Code('end_module();')
        publicConstr = writer_code.Constructor(emptyBody, 'pu', [writer_code.Parameter('name', module_nameDecl)], ['std::string()', 'sc_module(name)'])
        classDecl = writer_code.SCModule('MyClass', [privateVar], [stringDecl])
        classDecl.addConstructor(publicConstr)
        classDecl.writeImplementation(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], 'MyClass::MyClass( sc_module_name name ) : std::string(), sc_module(name) {\n')
        self.assertEqual(lines[1], '    end_module();\n')
        self.assertEqual(lines[2], '}\n')

    def testInlineMethodDecl(self):
        intDecl = writer_code.intType
        emptyBody = writer_code.Code('')
        inlineMethod = writer_code.Method('pippo', emptyBody, intDecl, 'pri', [], False, True)
        publicConstr = writer_code.Constructor(emptyBody, 'pu')
        classDecl = writer_code.ClassDeclaration('MyClass', [inlineMethod])
        classDecl.addConstructor(publicConstr)
        classDecl.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 8)
        self.assertEqual(lines[0], 'class MyClass{\n')
        self.assertEqual(lines[1], '    private:\n')
        self.assertEqual(lines[2], '    inline int pippo(){\n')
        self.assertEqual(lines[3], '    }\n')
        self.assertEqual(lines[4], '\n')
        self.assertEqual(lines[5], '    public:\n')
        self.assertEqual(lines[6], '    MyClass();\n')
        self.assertEqual(lines[7], '};\n')

    def testInlineMethodImpl(self):
        intDecl = writer_code.intType
        emptyBody = writer_code.Code('')
        inlineMethod = writer_code.Method('pippo', emptyBody, intDecl, 'pri', [], False, True)
        publicConstr = writer_code.Constructor(emptyBody, 'pu')
        classDecl = writer_code.ClassDeclaration('MyClass', [inlineMethod])
        classDecl.addConstructor(publicConstr)
        classDecl.writeImplementation(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], 'MyClass::MyClass(){\n')
        self.assertEqual(lines[1], '}\n')
