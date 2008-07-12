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


import CustomCode, Writer

class DumpElement:
    """Base element of all the elements which have to be dumped. All printable elements like
    classes, attributes, methods .... derive from this class"""

    def __init__(self,  name):
        self.name = name
        self.docstring = ''
    def addDoc(self, docstring):
        self.docstring = docstring
    def printDocString(self, writer):
        for line in self.docstring.split('\n'):
            if line:
                writer.write('/// ' + line + '\n')
    def __str__(self):
        try:
            stringWriter = Writer.StringWriter()
            self.writeDeclaration(stringWriter)
            return str(stringWriter)
        except:
            return self.name

class Type(DumpElement):
    """Represents a type; this is use for variable declaration, function parameter declaration ..."""

    def __init__(self, name, include = None):
        DumpElement.__init__(self, name)
        self.include = include
        self.modifiers = []

    def makePointer(self):
        import copy
        newType = copy.deepcopy(self)
        newType.modifiers.append('*')
        return newType
    def makeRef(self):
        import copy
        newType = copy.deepcopy(self)
        newType.modifiers.append('&')
        return newType
    def makeNormal(self):
        if not self.modifiers:
            raise Exception('Unable to create a normal copy of type ' + self.name + ': the type is not a pointer or a ref')
        import copy
        newType = copy.deepcopy(self)
        newType.modifiers.pop()
        return newType

    def writeDeclaration(self, writer):
        writer.write(self.name)
        for i in self.modifiers:
            writer.write(' ' + i)
    
    def getIncludes(self):
        if self.include:
            return [self.include]
        else:
            return []

class TemplateType(Type):
    """Represents a templated type; this is use for variable declaration, function parameter declaration ..."""

    def __init__(self, name, template = [], include = None):
        Type.__init__(self, name, include)
        if type(template) != type([]):
            self.template = [template]
        else:
            self.template = template

    def writeDeclaration(self, writer):
        Type.writeDeclaration(self, writer)
        if self.template:
            writer.write('< ')
            for i in self.template:
                try:
                    i.writeDeclaration(writer)
                except AttributeError:
                    writer.write(str(i))
                if i != self.template[-1]:
                    writer.write(', ')
            writer.write(' >')
        for i in self.modifiers:
            writer.write(' ' + i)

    def getIncludes(self):
        includes = Type.getIncludes(self)
        for i in self.template:
            try:
                for j in i.getIncludes():
                    if not j in includes:
                        includes.append(j)
            except AttributeError:
                pass
        return includes

intType = Type('int')
shortType = Type('short int')
ushortType = Type('unsigned short int')
uintType = Type('unsigned int')
floatType = Type('float')
doubleType = Type('double')
charType = Type('char')
ucharType = Type('unsigned char')
boolType = Type('bool')
sc_uint64Type = Type('sc_dt::uint64', 'systemc.h')
sc_moduleType = Type('sc_module', 'systemc.h')
sc_module_nameType = Type('sc_module_name', 'systemc.h')
sc_timeType = Type('sc_time', 'systemc.h')
stringType = Type('std::string', 'string')
voidType = Type('void')
intRefType = intType.makeRef()
shortRefType = shortType.makeRef()
ushortRefType = ushortType.makeRef()
uintRefType = uintType.makeRef()
floatRefType = floatType.makeRef()
doubleRefType = doubleType.makeRef()
charRefType = charType.makeRef()
ucharRefType = ucharType.makeRef()
boolRefType = boolType.makeRef()
sc_uint64RefType = sc_uint64Type.makeRef()
sc_moduleRefType = sc_moduleType.makeRef()
sc_module_nameRefType = sc_module_nameType.makeRef()
sc_timeRefType = sc_timeType.makeRef()
stringRefType = stringType.makeRef()
intPtrType = intType.makePointer()
uintPtrType = uintType.makePointer()
shortPrtType = shortType.makePointer()
ushortPrtType = ushortType.makePointer()
floatPtrType = floatType.makePointer()
doublePtrType = doubleType.makePointer()
charPtrType = charType.makePointer()
ucharPtrType = ucharType.makePointer()
boolPtrType = boolType.makePointer()
sc_uint64PtrType = sc_uint64Type.makePointer()
sc_modulePtrType = sc_moduleType.makePointer()
sc_module_namePtrType = sc_module_nameType.makePointer()
sc_timePtrType = sc_timeType.makeRef()
stringPtrType = stringType.makePointer()

class Parameter(DumpElement):
    """Represents a parameter of a function; this parameter can be either input or output
    (even though in C++ output parameters are not really used)"""

    def __init__(self, name, type, constant = False, restrict = False, input = True):
        DumpElement.__init__(self, name)
        self.type = type
        self.input = input
        self.restrict = restrict
        self.constant = constant

    def writeDeclaration(self, writer):
        if self.constant:
            writer.write('const ')
        self.type.writeDeclaration(writer)
        if self.input:
            if self.restrict:
                writer.write(' restrict')
            writer.write(' ' + self.name)

    def getIncludes(self):
        return self.type.getIncludes()

class Variable(DumpElement):
    """Represents a variable of the program; this is a global variable, in the
    sense that it is not a member of a class; it can, anyway, be a variable
    of a method"""

    def __init__(self, name, type, static = False, initValue = ''):
        DumpElement.__init__(self, name)
        self.type = type
        self.static = static
        self.initValue = initValue

    def writeDeclaration(self, writer):
        if self.docstring:
            self.printDocString(writer)
        if self.static:
            writer.write('static ')
        self.type.writeDeclaration(writer)
        writer.write(' ' + self.name)
        if self.initValue:
            writer.write(' = ' + self.initValue)
        writer.write(';\n')

    def writeImplementation(self, writer):
        self.writeDeclaration(writer)

    def getIncludes(self):
        return self.type.getIncludes()

class Function(DumpElement):
    """Represents a function of the program; this function is not
    a method of a class"""

    def __init__(self, name, body, retType = Type('void'), parameters = [], static = False, inline = False, template = [], noException = False):
        DumpElement.__init__(self, name)
        self.body = body
        self.parameters = parameters
        self.retType = retType
        self.template = template
        self.static = static
        self.inline = inline
        self.noException = noException

    def writeDeclaration(self, writer):
        if self.docstring:
            self.printDocString(writer)
        if self.template:
            writer.write('template < typename ')
            for i in self.template:
                writer.write(i)
                if i != self.template[-1]:
                    writer.write(', ')
            writer.write(' > ')
        if self.static:
            writer.write('static ')
        if self.inline:
            writer.write('inline ')
        try:
            if self.virtual:
                if self.static or self.inline:
                    raise Exception('Operation ' + self.name + ' is virtual but also inline or static: this is not possible')
                writer.write('virtual ')
        except AttributeError:
            pass
        self.retType.writeDeclaration(writer)
        writer.write(' ' + self.name + '(')
        if self.parameters:
            writer.write(' ')
        for i in self.parameters:
            i.writeDeclaration(writer)
            if i != self.parameters[-1]:
                writer.write(', ')
            else:
                writer.write(' ')
        if self.template or self.inline:
            writer.write(')')
            if self.noException:
                writer.write(' throw()\n')
            writer.write('{\n')
            self.body.writeImplementation(writer)
            writer.write('}\n')
        else:
            writer.write(')')
            if self.noException:
                writer.write(' throw()\n')
            try:
                if self.pure:
                    writer.write(' = 0')
            except AttributeError:
                pass
            writer.write(';\n')

    def writeImplementation(self, writer):
        if self.docstring:
            self.printDocString(writer)

        if self.template or self.inline:
            return
        self.retType.writeDeclaration(writer)
        writer.write(' ' + self.name + '(')
        if self.parameters:
            writer.write(' ')
        for i in self.parameters:
            i.writeDeclaration(writer)
            if i != self.parameters[-1]:
                writer.write(', ')
            else:
                writer.write(' ')
        writer.write(')')
        if self.noException:
            writer.write(' throw()\n')
        writer.write('{\n')
        self.body.writeImplementation(writer)
        writer.write('}\n')

    def getIncludes(self):
        includes = self.retType.getIncludes()
        for i in self.parameters:
            for j in i.getIncludes():
                if not j in includes:
                    includes.append(j)
        for j in self.body.getIncludes():
            if not j in includes:
                includes.append(j)
        return includes

    def getRetValIncludes(self):
        return self.retType.getIncludes()

class Operator(Function):
    """Represents an operator of the program; this operator is not
    a method of a class"""

    def __init__(self, name, body, retType = Type('void'), parameters = [], static = False, inline = False, template = [], noException = False):
        Function.__init__(self, 'operator' + name, body, retType, parameters, static, inline, template, noException)

class Enum(DumpElement):
    """Represents the declaration of an enumeration type"""

    def __init__(self, name, values):
        DumpElement.__init__(self, name)
        self.values = values

    def addValue(self, name, value):
        self.values[name] = value

    def writeDeclaration(self, writer):
        if self.docstring:
            self.printDocString(writer)
        if not self.values:
            raise Exception('There must be elements inside the Enum before printing it')
        code = 'enum ' + self.name + ' {\n'
        for key, val in self.values.items():
            code += key + ' = ' + str(val) + ' \n,'
        writer.write(code[:-1] + '};\n')

class Union(DumpElement):
    """Represents a union"""

    def __init__(self, name, members = []):
        DumpElement.__init__(self, name)
        self.members = members

    def addMember(self, member):
        self.members.append(member)

    def writeDeclaration(self, writer):
        if self.docstring:
            self.printDocString(writer)
        if not self.members:
            raise Exception('There must be elements inside the Union before printing it')
        writer.write('union ' + self.name + ' {\n')
        for i in self.members:
            i.writeDeclaration(writer)
        writer.write('};\n')

    def getIncludes(self):
        includes = []
        for i in self.members:
            for j in i.getIncludes():
                if not j in includes:
                    includes.append(j)
        return includes

class Typedef(DumpElement):
    """Represents a typedef of an existing type"""

    def __init__(self, name, oldType):
        DumpElement.__init__(self, name)
        self.oldType = oldType

    def writeDeclaration(self, writer):
        if self.docstring:
            self.printDocString(writer)
        writer.write('typedef ' + self.name + ' ')
        self.oldType.writeDeclaration(writer)
        writer.write(';\n')

    def getIncludes(self):
        return self.oldType.getIncludes()
