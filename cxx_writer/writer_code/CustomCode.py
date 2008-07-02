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


class Code:
    """Custom code element. it allows to add custom code in any place.
    This class is for example used to specify the behavior of a class method or
    of a function"""

    def __init__(self,  code,  includes = []):
        if type(code) == type([]):
            self.code = '\n'.join(code)
        else:
            self.code = code
        self.incudes = includes
        self.variables = []

    def addCode(self, code):
        if type(code) == type([]):
            self.code += '\n'.join(code)
        else:
            self.code += code

    def addInclude(self, include):
        if type(include) == type(''):
            self.incudes.append(include)
        else:
            self.incudes += include

    def addVariable(self, variable):
        self.variables.append(variable)

    def __str__(self):
        return self.code

    def writeDeclaration(self, writer):
        if self.variables:
            writer.write('{\n')
            for i in self.variables:
                i.writeDeclaration(writer)
        else:
            if self.code:
                self.code += '\n'
        writer.write(self.code)
        if self.variables:
            writer.write('}\n')

    def writeImplementation(self, writer):
        self.writeDeclaration(writer)

    def getIncludes(self):
        VarIncludes = self.includes
        for i in self.variables:
            for j in i.getIncludes():
                if not j in VarIncludes:
                    VarIncludes.append(j)
        return VarIncludes
