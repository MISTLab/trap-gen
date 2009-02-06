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

class TestWriter(unittest.TestCase):
    def setUp(self):
        try:
            os.remove('prova.cpp')
        except:
            pass
        self.writer = writer_code.CodeWriter('prova.cpp')

    def tearDown(self):
        del self.writer
        os.remove('prova.cpp')

    def testLine(self):
        self.writer.write('ciao')
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], 'ciao')

    def testEmptyLine(self):
        self.writer.write('')
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 0)

    def testNewLines(self):
        self.writer.write('\n\n\n')
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], '\n')
        self.assertEqual(lines[1], '\n')
        self.assertEqual(lines[2], '\n')

    def testNormal(self):
        self.writer.write('first line\nsecond line{\nindented line\nother indented\n}\nnon indented')
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 6)
        self.assertEqual(lines[0], 'first line\n')
        self.assertEqual(lines[1], 'second line{\n')
        self.assertEqual(lines[2], '    indented line\n')
        self.assertEqual(lines[3], '    other indented\n')
        self.assertEqual(lines[4], '}\n')
        self.assertEqual(lines[5], 'non indented')

    def testUglyCode(self):
        self.writer.write('first line\nsecond line{indented line\nother indented}\nnon indented\n')
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 4)
        self.assertEqual(lines[0], 'first line\n')
        self.assertEqual(lines[1], 'second line{indented line\n')
        self.assertEqual(lines[2], 'other indented}\n')
        self.assertEqual(lines[3], 'non indented\n')

    def testJavaIndeting(self):
        self.writer.write('first line\nsecond line{\nindented line{\n \n}\nother indented\n}non indented')
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0], 'first line\n')
        self.assertEqual(lines[1], 'second line{\n')
        self.assertEqual(lines[2], '    indented line{\n')
        self.assertEqual(lines[3], '\n')
        self.assertEqual(lines[4], '    }\n')
        self.assertEqual(lines[5], '    other indented\n')
        self.assertEqual(lines[6], '}non indented')

    def testCIndeting(self):
        self.writer.write('first line\nsecond line\n{\nindented line\n{\n \n}\nother indented\n}non indented')
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 9)
        self.assertEqual(lines[0], 'first line\n')
        self.assertEqual(lines[1], 'second line\n')
        self.assertEqual(lines[2], '{\n')
        self.assertEqual(lines[3], '    indented line\n')
        self.assertEqual(lines[4], '    {\n')
        self.assertEqual(lines[5], '\n')
        self.assertEqual(lines[6], '    }\n')
        self.assertEqual(lines[7], '    other indented\n')
        self.assertEqual(lines[8], '}non indented')

    def testNoNewline(self):
        self.writer.write('{\n{\n')
        self.writer.write('ciao')
        self.writer.write('pippo')
        self.writer.write('\notherLine')
        self.writer.write('\n}\n}')
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 6)
        self.assertEqual(lines[0], '{\n')
        self.assertEqual(lines[1], '    {\n')
        self.assertEqual(lines[2], '        ciaopippo\n')
        self.assertEqual(lines[3], '        otherLine\n')
        self.assertEqual(lines[4], '    }\n')
        self.assertEqual(lines[5], '}')

    def testLineLength(self):
        self.writer.write('{\n{\n')
        self.writer.write('one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty')
        self.writer.write('pippo')
        self.writer.write('\notherLine')
        self.writer.write('\n}\n}')
        self.writer.flush()
        testFile = open('prova.cpp', 'r')
        lines = testFile.readlines()
        testFile.close()
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0], '{\n')
        self.assertEqual(lines[1], '    {\n')
        self.assertEqual(lines[2], '        one two three four five six seven eight nine ten eleven twelve thirteen fourteen \\\n')
        self.assertEqual(lines[3], '            fifteen sixteen seventeen eighteen nineteen twentypippo\n')
        self.assertEqual(lines[4], '        otherLine\n')
        self.assertEqual(lines[5], '    }\n')
        self.assertEqual(lines[6], '}')
