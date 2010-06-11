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


import unittest
import writer_code
import os

class TestSimpleDecls(unittest.TestCase):
    def setUp(self):
        try:
            os.remove('prova.cpp')
        except:
            pass
        self.writer = writer_code.CodeWriter('prova.cpp')

    def tearDown(self):
        del self.writer
        os.remove('prova.cpp')

    def testSimpleTemplateType(self):
        innerType = writer_code.stringType
        templ = writer_code.TemplateType('std::vector', [innerType])
        templ.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], 'std::vector< std::string >')

    def testDoubleTemplateType(self):
        innerType1 = writer_code.stringType
        innerType2 = writer_code.intType
        templ = writer_code.TemplateType('std::map', [innerType1, innerType2])
        templ.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], 'std::map< std::string, int >')

    def testNestedTemplateType(self):
        innerType1 = writer_code.stringType
        innerType2 = writer_code.intType
        innerType3 = writer_code.doubleType
        templ1 = writer_code.TemplateType('std::map', [innerType2, innerType3])
        templ2 = writer_code.TemplateType('std::map', [innerType1, templ1])
        templ2.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], 'std::map< std::string, std::map< int, double > >')

    def testSimpleVariable(self):
        type = writer_code.stringType
        var = writer_code.Variable('pippo', type)
        var.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 0)

    def testVariableInit(self):
        type = writer_code.stringType
        var = writer_code.Variable('pippo', type, False, '\"pippa\"')
        var.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 0)

    def testTemplatedVariable(self):
        innerType1 = writer_code.stringType
        innerType2 = writer_code.intType
        innerType3 = writer_code.doubleType
        templ1 = writer_code.TemplateType('std::map', [innerType2, innerType3])
        type = writer_code.TemplateType('std::map', [innerType1, templ1])
        var = writer_code.Variable('pippo', type)
        var.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 0)

    def testEnum(self):
        enumInst = writer_code.Enum('myEnum', {'ONE':1, 'TWO':2, 'THREE':3})
        enumInst.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 5)
        self.assertEqual(lines[0], 'enum myEnum {\n')
        self.assertEqual(lines[1], '    THREE = 3\n')
        self.assertEqual(lines[2], '    ,TWO = 2\n')
        self.assertEqual(lines[3], '    ,ONE = 1\n')
        self.assertEqual(lines[4], '};\n')

    def testUnion(self):
        unionInst = writer_code.Union('myUnion')
        type = writer_code.stringType
        var = writer_code.Variable('pippo', type)
        unionInst.addMember(var)
        type = writer_code.intType
        var = writer_code.Variable('duck', type)
        unionInst.addMember(var)
        unionInst.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 4)
        self.assertEqual(lines[0], 'union myUnion {\n')
        self.assertEqual(lines[1], '    std::string pippo;\n')
        self.assertEqual(lines[2], '    int duck;\n')
        self.assertEqual(lines[3], '};\n')

    def testTypedef(self):
        type = writer_code.intType
        typedef = writer_code.Typedef('duck', type)
        typedef.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], 'typedef duck int;\n')

    def testSimpleFunction(self):
        code = writer_code.Code('printf(\"Wow\");')
        function = writer_code.Function('dummyFun', code)
        function.writeImplementation(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], 'void dummyFun(){\n')
        self.assertEqual(lines[1], '    printf(\"Wow\");\n')
        self.assertEqual(lines[2], '}\n')

    def testReturnFunction(self):
        code = writer_code.Code('if(works){\nprintf(\"hummm\\n\");\nreturn 1;\n}\nelse{\nreturn 0;\n}')
        retType = writer_code.intType
        function = writer_code.Function('dummyFun', code, retType)
        function.writeImplementation(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 9)
        self.assertEqual(lines[0], 'int dummyFun(){\n')
        self.assertEqual(lines[1], '    if(works){\n')
        self.assertEqual(lines[2], '        printf(\"hummm\\n\");\n')
        self.assertEqual(lines[3], '        return 1;\n')
        self.assertEqual(lines[4], '    }\n')
        self.assertEqual(lines[5], '    else{\n')
        self.assertEqual(lines[6], '        return 0;\n')
        self.assertEqual(lines[7], '    }\n')
        self.assertEqual(lines[8], '}\n')

    def testParameterFunction(self):
        code = writer_code.Code('if(works){\nprintf(\"hummm\\n\");\nreturn 1;\n}\nelse{\nreturn 0;\n}')
        intType = writer_code.intType
        parameters = [writer_code.Parameter('param1', intType)]
        function = writer_code.Function('dummyFun', code, intType, parameters)
        function.writeImplementation(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 9)
        self.assertEqual(lines[0], 'int dummyFun( int param1 ){\n')
        self.assertEqual(lines[1], '    if(works){\n')
        self.assertEqual(lines[2], '        printf(\"hummm\\n\");\n')
        self.assertEqual(lines[3], '        return 1;\n')
        self.assertEqual(lines[4], '    }\n')
        self.assertEqual(lines[5], '    else{\n')
        self.assertEqual(lines[6], '        return 0;\n')
        self.assertEqual(lines[7], '    }\n')
        self.assertEqual(lines[8], '}\n')

    def testTemplateFunction(self):
        code = writer_code.Code('if(works){\nprintf(\"hummm\\n\");\nreturn 1;\n}\nelse{\nreturn 0;\n}')
        intType = writer_code.intType
        parameters = [writer_code.Parameter('param1', intType)]
        function = writer_code.Function('dummyFun', code, intType, parameters, template = ['A'])
        function.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 9)
        self.assertEqual(lines[0], 'template < typename A > int dummyFun( int param1 ){\n')
        self.assertEqual(lines[1], '    if(works){\n')
        self.assertEqual(lines[2], '        printf(\"hummm\\n\");\n')
        self.assertEqual(lines[3], '        return 1;\n')
        self.assertEqual(lines[4], '    }\n')
        self.assertEqual(lines[5], '    else{\n')
        self.assertEqual(lines[6], '        return 0;\n')
        self.assertEqual(lines[7], '    }\n')
        self.assertEqual(lines[8], '}\n')

    def testInlineFunction(self):
        code = writer_code.Code('if(works){\nprintf(\"hummm\\n\");\nreturn 1;\n}\nelse{\nreturn 0;\n}')
        intType = writer_code.intType
        parameters = [writer_code.Parameter('param1', intType)]
        function = writer_code.Function('dummyFun', code, intType, parameters, inline = True)
        function.writeDeclaration(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 9)
        self.assertEqual(lines[0], 'inline int dummyFun( int param1 ){\n')
        self.assertEqual(lines[1], '    if(works){\n')
        self.assertEqual(lines[2], '        printf(\"hummm\\n\");\n')
        self.assertEqual(lines[3], '        return 1;\n')
        self.assertEqual(lines[4], '    }\n')
        self.assertEqual(lines[5], '    else{\n')
        self.assertEqual(lines[6], '        return 0;\n')
        self.assertEqual(lines[7], '    }\n')
        self.assertEqual(lines[8], '}\n')

    def testFunctionDoc(self):
        intType = writer_code.intType
        code = writer_code.Code('')
        parameters = [writer_code.Parameter('param1', intType)]
        function = writer_code.Function('dummyFun', code, intType, parameters)
        function.addDoc('Documentation test\nanother line\n')
        function.writeImplementation(self.writer)
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 5)
        self.assertEqual(lines[0], '/// Documentation test\n')
        self.assertEqual(lines[1], '/// another line\n')
        self.assertEqual(lines[2], 'int dummyFun( int param1 ){\n')
        self.assertEqual(lines[3], '\n')
        self.assertEqual(lines[4], '}\n')
