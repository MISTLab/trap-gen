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

class StringWriter:
    def __init__(self):
        self.code = ''

    def write(self, code):
        self.code += code

    def __str__(self):
        return self.code

class CodeWriter:
    """This class is simply used to write strings to an output file; the added value is that we do not
    need to care about indenting since this is automatically managed"""

    def __init__(self, file, indentSize = 4, lineWidth = 90):
        if type(file) == type(''):
            self.file = open(file, 'at')
            self.opened = True
        else:
            file.flush()
            self.file = file
            self.opened = False
        self.curIndent = 0
        self.indentSize = indentSize
        self.codeBuffer = ''
        if lineWidth < 20:
            raise Exception('A minimum line length of at least 20 characters should be specified')
        self.lineWidth = lineWidth

    def __del__(self):
        if self.opened:
            self.file.close()

    def write(self, code):
        # (After/Before) each delimiter start ({) I have to increment
        # the size of the current indent. Before each delimiter
        # end (}) I have to decrement it
        # Note that after each newline I have to print the current indenting
        self.codeBuffer += code.expandtabs(self.indentSize)
        if not '\n' in code:
            return
        for line in self.codeBuffer.split('\n')[:-1]:
            line = line.strip()
            # I check if it is the case to unindent
            if (line.endswith('}') or line.startswith('}')) and self.curIndent >= self.indentSize:
                self.curIndent -= self.indentSize
            # Now I print the current line, making sure that It is not too long
            # in case I send it to a new line
            if line:
                for i in range(0, self.curIndent):
                    self.file.write(' ')
                print >> self.file, self.go_new_line(line)
            else:
                print >> self.file, ''
            # Finally I compute the nesting level for the next lines
            if line.endswith('{'):
                self.curIndent += self.indentSize
        lastLine = self.codeBuffer.split('\n')[-1]
        if not lastLine.endswith('\n'):
            self.codeBuffer = lastLine

    def go_new_line(self, toModify):
        """Given a string the function introduces newline characters to
        respect the line width constraint"""
        singleIndent = ''
        for i in range(0, self.indentSize):
            singleIndent += ' '
        totalIndent = ''
        for i in range(0, self.curIndent):
            totalIndent += ' '
        # first of all I have to get the nearest white space character
        if len(toModify) < self.lineWidth:
            return toModify
        endToCheck = toModify.find('\n')
        if endToCheck < 0:
            endToCheck = len(toModify)
        i = endToCheck
        for i in range(self.lineWidth - 10, endToCheck):
            if toModify[i] == ' ':
                break
        if i < endToCheck - 1:
            return toModify[:i] + ' \\\n' + singleIndent + totalIndent + self.go_new_line(toModify[(i + 1):endToCheck])
        else:
            if i < len(toModify) - 1:
                return toModify[:(endToCheck + 1)] + self.go_new_line(toModify[(endToCheck + 1):])
            else:
                return toModify


    def flush(self):
        self.file.write(self.codeBuffer)
        self.codeBuffer = ''
        self.file.flush()
