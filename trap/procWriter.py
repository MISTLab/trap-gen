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

# This file contains the methods used to print on file the architectural
# elements; this includes the processor structure, the registers, the
# pipeline stages, etc..
# Note how these methods are in a separate file, but they are actually part of the
# processor class

import cxx_writer

try:
    import networkx as NX
except:
    import traceback
    traceback.print_exc()
    raise Exception('Error occurred during the import of module networkx, required for the creation of the decoder. Please correctly install the module')

assignmentOps = ['=', '+=', '-=', '*=', '/=', '|=', '&=', '^=']
binaryOps = ['+', '-', '*', '/', '|', '&', '^', '<<', '>>']
unaryOps = ['~']
comparisonOps = ['<', '>', '<=', '>=', '==', '!=', '<<=', '>>=']
regMaxType = None
resourceType = {}

def getCPPRegClass(self, model, regType):
    # returns the class implementing the current register; I have to
    # define all the operators;
    # TODO: think about the clocked registers
    regWidthType = regMaxType
    registerType = cxx_writer.writer_code.Type('Register')
    registerElements = []

    ####################### Lets declare the operators used to access the register fields ##############
    codeOperatorBody = ''
    for key in self.bitMask.keys():
        codeOperatorBody += 'if(bitField == \"' + key + '\"){\nreturn this->field_' + key + ';\n}\n'
    codeOperatorBody += 'return this->field_empty;'
    InnerFieldType = cxx_writer.writer_code.Type('InnerField')
    operatorBody = cxx_writer.writer_code.Code(codeOperatorBody)
    operatorParam = [cxx_writer.writer_code.Parameter('bitField', cxx_writer.writer_code.stringRefType.makeConst())]
    operatorDecl = cxx_writer.writer_code.MemberOperator('[]', operatorBody, InnerFieldType.makeRef(), 'pu', operatorParam)
    registerElements.append(operatorDecl)
    codeOperatorBody = ''
    for key in self.bitMask.keys():
        codeOperatorBody += 'if(strcmp(bitField, \"' + key + '\") == 0){\nreturn this->field_' + key + ';\n}\n'
    codeOperatorBody += 'return this->field_empty;'
    operatorBody = cxx_writer.writer_code.Code(codeOperatorBody)
    operatorBody.addInclude('cstring')
    operatorParam = [cxx_writer.writer_code.Parameter('bitField', cxx_writer.writer_code.charPtrType.makeConst())]
    operatorDecl = cxx_writer.writer_code.MemberOperator('[]', operatorBody, InnerFieldType.makeRef(), 'pu', operatorParam)
    registerElements.append(operatorDecl)
    
    #################### Lets declare the normal operators (implementation of the pure operators of the base class) ###########
    for i in unaryOps:
        operatorBody = cxx_writer.writer_code.Code('return ' + i + '(this->value);')
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu')
        registerElements.append(operatorDecl)
    # Now I have the three versions of the operators, depending whether they take
    # in input the integer value, the specific register or the base one
    # INTEGER
    for i in binaryOps:
        operatorBody = cxx_writer.writer_code.Code('return (this->value ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True)
        registerElements.append(operatorDecl)
    for i in comparisonOps:
        operatorBody = cxx_writer.writer_code.Code('return (this->value ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True)
        registerElements.append(operatorDecl)
    for i in assignmentOps:
        operatorBody = cxx_writer.writer_code.Code('this->value ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regType.makeRef(), 'pu', [operatorParam])
        registerElements.append(operatorDecl)        
    # SPECIFIC REGISTER
    for i in binaryOps:
        operatorBody = cxx_writer.writer_code.Code('return (this->value ' + i + ' other.value);')
        operatorParam = cxx_writer.writer_code.Parameter('other', regType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True)
        registerElements.append(operatorDecl)
    for i in comparisonOps:
        operatorBody = cxx_writer.writer_code.Code('return (this->value ' + i + ' other.value);')
        operatorParam = cxx_writer.writer_code.Parameter('other', regType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True)
        registerElements.append(operatorDecl)
    for i in assignmentOps:
        operatorBody = cxx_writer.writer_code.Code('this->value ' + i + ' other.value;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', regType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regType.makeRef(), 'pu', [operatorParam])
        registerElements.append(operatorDecl)        
    # GENERIC REGISTER: this case is look more complicated; actually I simply used the
    # operators of parameter other
    for i in binaryOps:
        operatorBody = cxx_writer.writer_code.Code('return (this->value ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True)
        registerElements.append(operatorDecl)
    for i in comparisonOps:
        operatorBody = cxx_writer.writer_code.Code('return (this->value ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True)
        registerElements.append(operatorDecl)
    for i in assignmentOps:
        operatorBody = cxx_writer.writer_code.Code('this->value ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regType.makeRef(), 'pu', [operatorParam])
        registerElements.append(operatorDecl)        
    # Scalar value cast operator
    operatorBody = cxx_writer.writer_code.Code('return this->value;')
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), operatorBody, cxx_writer.writer_code.Type(''), 'pu', const = True)
    registerElements.append(operatorIntDecl)

    # Constructors
    fieldInit = []
    for field in self.bitMask.keys():
        fieldInit.append('field_' + field + '(value)')
    constructorBody = cxx_writer.writer_code.Code('this->value = 0;')
    constructorParams = [cxx_writer.writer_code.Parameter('name', cxx_writer.writer_code.sc_module_nameType)]
    publicMainClassConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, ['Register(name, ' + str(self.bitWidth) + ')'] + fieldInit)
    publicMainClassEmptyConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', initList = ['Register(sc_gen_unique_name(\"' + regType.name + '\"), ' + str(self.bitWidth) + ')'] + fieldInit)
    
    # Stream Operators
    outStreamType = cxx_writer.writer_code.Type('std::ostream', 'ostream')
    code = 'stream << std::hex << std::showbase << this->value << std::dec;\nreturn stream;'
    operatorBody = cxx_writer.writer_code.Code(code)
    operatorParam = cxx_writer.writer_code.Parameter('stream', outStreamType.makeRef())
    operatorDecl = cxx_writer.writer_code.MemberOperator('<<', operatorBody, outStreamType.makeRef(), 'pu', [operatorParam], const = True)
    registerElements.append(operatorDecl)
    
    # Attributes and inner classes declarations
    attrs = []
    innerClasses = []
    for field, length in self.bitMask.items():
        # Here I have to define the classes that represent the different fields
        negatedMask = ''
        mask = ''
        for i in range(0, self.bitWidth):
            if(i >= length[0] and i <= length[1]):
                negatedMask = '0' + negatedMask
                mask = '1' + mask
            else:
                negatedMask = '1' + negatedMask
                mask = '0' + mask
        operatorCode = 'this->value &= ' + hex(int(negatedMask, 2)) + ';\nthis->value |= '
        if length[0] > 0:
            operatorCode += '(other << ' + str(length[0]) + ');\n'
        else:
            operatorCode += 'other;\n'
        operatorCode += 'return *this;'
        operatorBody = cxx_writer.writer_code.Code(operatorCode)
        operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
        operatorEqualDecl = cxx_writer.writer_code.MemberOperator('=', operatorBody, cxx_writer.writer_code.Type('InnerField').makeRef(), 'pu', [operatorParam])
        operatorCode = 'return (this->value & ' + hex(int(mask, 2)) + ')'
        if length[0] > 0:
            operatorCode += ' >> ' + str(length[0])
        operatorCode += ';'
        operatorBody = cxx_writer.writer_code.Code(operatorCode)
        operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), operatorBody, cxx_writer.writer_code.Type(''), 'pu', const = True)
        fieldAttribute = cxx_writer.writer_code.Attribute('value', regMaxType.makeRef(), 'pri')
        constructorParams = [cxx_writer.writer_code.Parameter('value', regMaxType.makeRef())]
        publicConstr = cxx_writer.writer_code.Constructor(cxx_writer.writer_code.Code(''), 'pu', constructorParams, ['value(value)'])
        InnerFieldClass = cxx_writer.writer_code.ClassDeclaration('InnerField_' + field, [operatorEqualDecl, operatorIntDecl, fieldAttribute], [cxx_writer.writer_code.Type('InnerField')])
        InnerFieldClass.addConstructor(publicConstr)
        innerClasses.append(InnerFieldClass)
        fieldAttribute = cxx_writer.writer_code.Attribute('field_' + field, InnerFieldClass.getType(), 'pri')
        attrs.append(fieldAttribute)
    operatorBody = cxx_writer.writer_code.Code('return *this;')
    operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
    operatorEqualDecl = cxx_writer.writer_code.MemberOperator('=', operatorBody, cxx_writer.writer_code.Type('InnerField').makeRef(), 'pu', [operatorParam])
    operatorBody = cxx_writer.writer_code.Code('return 0;')   
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), operatorBody, cxx_writer.writer_code.Type(''), 'pu', const = True)
    publicConstr = cxx_writer.writer_code.Constructor(cxx_writer.writer_code.Code(''), 'pu')
    InnerFieldClass = cxx_writer.writer_code.ClassDeclaration('InnerField_Empty', [operatorEqualDecl, operatorIntDecl], [cxx_writer.writer_code.Type('InnerField')])
    InnerFieldClass.addConstructor(publicConstr)
    innerClasses.append(InnerFieldClass)
    fieldAttribute = cxx_writer.writer_code.Attribute('field_empty', InnerFieldClass.getType(), 'pri')
    attrs.append(fieldAttribute)
    valueAttribute = cxx_writer.writer_code.Attribute('value', regWidthType, 'pri')
    attrs.append(valueAttribute)
    registerElements = attrs + registerElements
    
    registerDecl = cxx_writer.writer_code.ClassDeclaration(regType.name, registerElements, [registerType])
    registerDecl.addConstructor(publicMainClassConstr)
    registerDecl.addConstructor(publicMainClassEmptyConstr)
    for i in innerClasses:
        registerDecl.addInnerClass(i)
    return registerDecl

def getCPPRegBankClass(self, model, regType):
    # returns the class implementing the single register of
    # the register bank
    return getCPPRegClass(self, model, regType)

def getCPPRegisters(self, model):
    # This method creates all the classes necessary for declaring
    # the registers: in particular the register base class
    # and all the classes for the different bitwidths; in order to
    # do this I simply iterate over the registers
    regLen = 0
    for reg in self.regs + self.regBanks:
        # I have to determine the register with the longest width and
        # accordingly create the type
        if reg.bitWidth > regLen:
            regLen = reg.bitWidth

    # Now I create the base class for all the registers
    registerElements = []

    from isa import resolveBitType
    global regMaxType
    regMaxType = resolveBitType('BIT<' + str(regLen) + '>')
    registerType = cxx_writer.writer_code.Type('Register')
    emptyBody = cxx_writer.writer_code.Code('')

    ################ Constructor: it initializes the width of the register ######################
    widthAttribute = cxx_writer.writer_code.Attribute('bitWidth', cxx_writer.writer_code.uintType, 'pri')
    registerElements.append(widthAttribute)
    constructorBody = cxx_writer.writer_code.Code('this->bitWidth = bitWidth;\nend_module();')
    constructorParams = [cxx_writer.writer_code.Parameter('name', cxx_writer.writer_code.sc_module_nameRefType.makeConst()), 
                cxx_writer.writer_code.Parameter('bitWidth', cxx_writer.writer_code.uintType)]
    publicConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, ['sc_module(name)'])
    
    ################ Operators working with the base class, employed when polimorphism is used ##################
    # First lets declare the class which will be used to manipulate the
    # bitfields
    operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
    operatorEqualDecl = cxx_writer.writer_code.MemberOperator('=', emptyBody, cxx_writer.writer_code.Type('InnerField').makeRef(), 'pu', [operatorParam], pure = True)
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), emptyBody, cxx_writer.writer_code.Type(''), 'pu', const = True, pure = True)
    InnerFieldClass = cxx_writer.writer_code.ClassDeclaration('InnerField', [operatorEqualDecl, operatorIntDecl])
    
    # Now lets procede with the members of the main class
    operatorParam = cxx_writer.writer_code.Parameter('bitField', cxx_writer.writer_code.stringRefType.makeConst())
    operatorDecl = cxx_writer.writer_code.MemberOperator('[]', emptyBody, InnerFieldClass.getType().makeRef(), 'pu', [operatorParam], const = True, pure = True)
    registerElements.append(operatorDecl)
    operatorParam = cxx_writer.writer_code.Parameter('bitField', cxx_writer.writer_code.charPtrType.makeConst())
    operatorDecl = cxx_writer.writer_code.MemberOperator('[]', emptyBody, InnerFieldClass.getType().makeRef(), 'pu', [operatorParam], const = True, pure = True)
    registerElements.append(operatorDecl)
    for i in unaryOps:
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, emptyBody, regMaxType, 'pu', pure = True)
        registerElements.append(operatorDecl)
    pureDeclTypes = [regMaxType, registerType]
    for pureDecls in pureDeclTypes:
        for i in binaryOps:
            operatorParam = cxx_writer.writer_code.Parameter('other', pureDecls.makeRef().makeConst())
            operatorDecl = cxx_writer.writer_code.MemberOperator(i, emptyBody, regMaxType, 'pu', [operatorParam], const = True, pure = True)
            registerElements.append(operatorDecl)
        for i in comparisonOps:
            operatorParam = cxx_writer.writer_code.Parameter('other', pureDecls.makeRef().makeConst())
            operatorDecl = cxx_writer.writer_code.MemberOperator(i, emptyBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True, pure = True)
            registerElements.append(operatorDecl)
        for i in assignmentOps:
            operatorParam = cxx_writer.writer_code.Parameter('other', pureDecls.makeRef().makeConst())
            operatorDecl = cxx_writer.writer_code.MemberOperator(i, emptyBody, registerType.makeRef(), 'pu', [operatorParam], pure = True)
            registerElements.append(operatorDecl)        
    # Stream Operators
    outStreamType = cxx_writer.writer_code.Type('std::ostream', 'ostream')
    operatorParam = cxx_writer.writer_code.Parameter('other', outStreamType.makeRef())
    operatorDecl = cxx_writer.writer_code.MemberOperator('<<', emptyBody, outStreamType.makeRef(), 'pu', [operatorParam], pure = True)
    registerElements.append(operatorDecl)
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), emptyBody, cxx_writer.writer_code.Type(''), 'pu', const = True, pure = True)
    registerElements.append(operatorIntDecl)
    
    ################ Finally I put everything together and print if ##################
    global resourceType
    regTypes = []
    regTypesCount = {}
    for reg in self.regs + self.regBanks:
        if not reg.bitWidth in [i.bitWidth for i in regTypes]:
            regTypes.append(reg)
            regTypesCount[reg.bitWidth] = 1
        else:
            # There is already a register with this bitwidth
            # I add this one only if it has a different bitMask
            if not reg.bitMask in [i.bitMask for i in filter(lambda x: x.bitWidth == reg.bitWidth, regTypes)]:
                regTypes.append(reg)
                regTypesCount[reg.bitWidth] = regTypesCount[reg.bitWidth] + 1
        resourceType[reg.name] = cxx_writer.writer_code.Type('Reg' + str(reg.bitWidth) + '_' + str(regTypesCount[reg.bitWidth]), 'registers.hpp')
    realRegClasses = []
    for regType in regTypes:
        realRegClasses.append(regType.getCPPClass(model, resourceType[regType.name]))
    registerDecl = cxx_writer.writer_code.SCModule('Register', registerElements)
    registerDecl.addConstructor(publicConstr)
    classes = [InnerFieldClass, registerDecl] + realRegClasses

    return classes

def getCPPAlias(self, model):
    # This method creates the class describing a register
    # alias: note that an alias simply holds a pointer to a register; the
    # operators are then redefined in order to call the corresponding operators
    # of the register. In addition there is the updateAlias operation which updates
    # the register this alias points to (and eventually the offset).
    regWidthType = regMaxType
    registerType = cxx_writer.writer_code.Type('Register', 'registers.hpp')
    aliasType = cxx_writer.writer_code.Type('Alias', 'alias.hpp')
    aliasElements = []
    global resourceType
    for i in self.aliasRegs + self.aliasRegBanks:
        resourceType[i.name] = aliasType

    ####################### Lets declare the operators used to access the register fields ##############
    codeOperatorBody = 'return (*this->reg)[bitField];'
    InnerFieldType = cxx_writer.writer_code.Type('InnerField')
    operatorBody = cxx_writer.writer_code.Code(codeOperatorBody)
    operatorParam = [cxx_writer.writer_code.Parameter('bitField', cxx_writer.writer_code.stringRefType.makeConst())]
    operatorDecl = cxx_writer.writer_code.MemberOperator('[]', operatorBody, InnerFieldType.makeRef(), 'pu', operatorParam)
    aliasElements.append(operatorDecl)
    
    #################### Lets declare the normal operators (implementation of the pure operators of the base class) ###########
    for i in unaryOps:
        operatorBody = cxx_writer.writer_code.Code('return ' + i + '(*this->reg);')
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu')
        aliasElements.append(operatorDecl)
    # Now I have the three versions of the operators, depending whether they take
    # in input the integer value, the specific register or the base one
    # INTEGER
    for i in binaryOps:
        operatorBody = cxx_writer.writer_code.Code('return (*this->reg ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True)
        aliasElements.append(operatorDecl)
    for i in comparisonOps:
        operatorBody = cxx_writer.writer_code.Code('return (*this->reg ' + i + ' (other - this->offset));')
        operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True)
        aliasElements.append(operatorDecl)
    for i in assignmentOps:
        operatorBody = cxx_writer.writer_code.Code('*this->reg ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, aliasType.makeRef(), 'pu', [operatorParam])
        aliasElements.append(operatorDecl)        
    # Alias Register
    for i in binaryOps:
        operatorBody = cxx_writer.writer_code.Code('return (*this->reg ' + i + ' *other.reg);')
        operatorParam = cxx_writer.writer_code.Parameter('other', aliasType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True)
        aliasElements.append(operatorDecl)
    for i in comparisonOps:
        operatorBody = cxx_writer.writer_code.Code('return (*this->reg + this->offset ' + i + ' *other.reg);')
        operatorParam = cxx_writer.writer_code.Parameter('other', aliasType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True)
        aliasElements.append(operatorDecl)
    for i in assignmentOps:
        operatorBody = cxx_writer.writer_code.Code('*this->reg ' + i + ' *other.reg;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', aliasType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, aliasType.makeRef(), 'pu', [operatorParam])
        aliasElements.append(operatorDecl)        
    # GENERIC REGISTER:
    for i in binaryOps:
        operatorBody = cxx_writer.writer_code.Code('return (*this->reg ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True)
        aliasElements.append(operatorDecl)
    for i in comparisonOps:
        operatorBody = cxx_writer.writer_code.Code('return (*this->reg + this->offset ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True)
        aliasElements.append(operatorDecl)
    for i in assignmentOps:
        operatorBody = cxx_writer.writer_code.Code('*this->reg ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, aliasType.makeRef(), 'pu', [operatorParam])
        aliasElements.append(operatorDecl)        
    # Scalar value cast operator
    operatorBody = cxx_writer.writer_code.Code('return *this->reg + this->offset;')
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), operatorBody, cxx_writer.writer_code.Type(''), 'pu', const = True)
    aliasElements.append(operatorIntDecl)

    # Constructor: takes as input the initial register
    constructorBody = cxx_writer.writer_code.Code('')
    constructorParams = [cxx_writer.writer_code.Parameter('reg', registerType.makePointer()), cxx_writer.writer_code.Parameter('offset', cxx_writer.writer_code.uintType, initValue = '0')]
    publicMainClassConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, ['reg(reg)', 'offset(offset)', 'defaultOffset(0)'])
    publicMainEmptyClassConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu')
    # Constructor: takes as input the initial alias
    constructorBody = cxx_writer.writer_code.Code('initAlias->referredAliases.insert(this);\ntihis->referringAliases.insert(initAlias);')
    constructorParams = [cxx_writer.writer_code.Parameter('initAlias', aliasType.makePointer()), cxx_writer.writer_code.Parameter('offset', cxx_writer.writer_code.uintType, initValue = '0')]
    publicAliasConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, ['reg(initAlias->reg)', 'offset(initAlias->offset + offset)', 'defaultOffset(offset)'])
    
    # Stream Operators
    outStreamType = cxx_writer.writer_code.Type('std::ostream', 'ostream')
    code = 'stream << *this->reg + this->offset;\nreturn stream;'
    operatorBody = cxx_writer.writer_code.Code(code)
    operatorParam = cxx_writer.writer_code.Parameter('stream', outStreamType.makeRef())
    operatorDecl = cxx_writer.writer_code.MemberOperator('<<', operatorBody, outStreamType.makeRef(), 'pu', [operatorParam], const = True)
    aliasElements.append(operatorDecl)

    # Update method: updates the register pointed by this alias
    updateCode = """this->reg = newAlias.reg;
    this->offset = newAlias.offset + newOffset;
    this->defaultOffset = newOffset;
    std::set<Alias *>::iterator referredIter, referredEnd;
    for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
        (*referredIter)->newReferredAlias(newAlias.reg, newAlias.offset + newOffset);
    }
    newAlias.referredAliases.insert(this);
    std::set<Alias *>::iterator referringIter, referringEnd;
    for(referringIter = this->referringAliases.begin(), referringEnd = this->referringAliases.end(); referringIter != referringEnd; referringIter++){
        (*referringIter)->referredAliases.erase(this);
    }    
    tihis->referringAliases.clear();
    tihis->referringAliases.insert(&newAlias);
    """
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam1 = cxx_writer.writer_code.Parameter('newAlias', aliasType.makeRef())
    updateParam2 = cxx_writer.writer_code.Parameter('newOffset', cxx_writer.writer_code.uintType, initValue = '0')
    updateDecl = cxx_writer.writer_code.Method('updateAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', [updateParam1, updateParam2])
    aliasElements.append(updateDecl)
    updateCode = """this->reg = &newAlias;
    this->offset = newOffset;
    this->defaultOffset = 0;
    std::set<Alias *>::iterator referredIter, referredEnd;
    for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
        (*referredIter)->newReferredAlias(&newAlias, newOffset);
    }
    std::set<Alias *>::iterator referringIter, referringEnd;
    for(referringIter = this->referringAliases.begin(), referringEnd = this->referringAliases.end(); referringIter != referringEnd; referringIter++){
        (*referringIter)->referredAliases.erase(this);
    }    
    tihis->referringAliases.clear();
    """
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam1 = cxx_writer.writer_code.Parameter('newAlias', registerType.makeRef())
    updateParam2 = cxx_writer.writer_code.Parameter('newOffset', cxx_writer.writer_code.uintType, initValue = '0')
    updateDecl = cxx_writer.writer_code.Method('updateAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', [updateParam1, updateParam2])
    aliasElements.append(updateDecl)
    updateCode = """this->reg = newAlias;
    this->offset = newOffset + this->defaultOffset;
    std::set<Alias *>::iterator referredIter, referredEnd;
    for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
        (*referredIter)->newReferredAlias(newAlias, newOffset);
    }
    """
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam1 = cxx_writer.writer_code.Parameter('newAlias', registerType.makePointer())
    updateParam2 = cxx_writer.writer_code.Parameter('newOffset', cxx_writer.writer_code.uintType)
    updateDecl = cxx_writer.writer_code.Method('newReferredAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', [updateParam1, updateParam2])
    aliasElements.append(updateDecl)
    
    # Finally I declare the class and pass to it all the declared members
    regAttribute = cxx_writer.writer_code.Attribute('reg', registerType.makePointer(), 'pri')
    aliasElements.append(regAttribute)
    offsetAttribute = cxx_writer.writer_code.Attribute('offset', cxx_writer.writer_code.uintType, 'pri')
    aliasElements.append(offsetAttribute)
    offsetAttribute = cxx_writer.writer_code.Attribute('defaultOffset', cxx_writer.writer_code.uintType, 'pri')
    aliasElements.append(offsetAttribute)
    aliasesAttribute = cxx_writer.writer_code.Attribute('referredAliases', cxx_writer.writer_code.TemplateType('std::set', [aliasType.makePointer()], 'set'), 'pri')
    aliasElements.append(aliasesAttribute)
    aliasesAttribute = cxx_writer.writer_code.Attribute('referringAliases', cxx_writer.writer_code.TemplateType('std::set', [aliasType.makePointer()], 'set'), 'pri')
    aliasElements.append(aliasesAttribute)
    aliasDecl = cxx_writer.writer_code.ClassDeclaration(aliasType.name, aliasElements)
    aliasDecl.addConstructor(publicMainClassConstr)
    aliasDecl.addConstructor(publicMainEmptyClassConstr)
    aliasDecl.addConstructor(publicAliasConstr)
    classes = [aliasDecl]
    return classes

def getCPPMemoryIf(self, model):
    # Creates the necessary structures for communicating with the memory; an
    # array in case of an internal memory, the TLM port for the use with TLM
    # etc.
    from isa import resolveBitType
    archWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize) + '>')
    archHWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize/2) + '>')
    archByteType = resolveBitType('BIT<' + str(self.byteSize) + '>')
    # First of all I create the memory base class
    classes = []
    memoryIfElements = []
    emptyBody = cxx_writer.writer_code.Code('')
    addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
    readDecl = cxx_writer.writer_code.Method('read_word', emptyBody, archWordType, 'pu', [addressParam], pure = True)
    memoryIfElements.append(readDecl)
    readDecl = cxx_writer.writer_code.Method('read_half', emptyBody, archHWordType, 'pu', [addressParam], pure = True)
    memoryIfElements.append(readDecl)
    readDecl = cxx_writer.writer_code.Method('read_byte', emptyBody, archByteType, 'pu', [addressParam], pure = True)
    memoryIfElements.append(readDecl)
    addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
    datumParam = cxx_writer.writer_code.Parameter('datum', archWordType.makeRef())
    writeDecl = cxx_writer.writer_code.Method('write_word', emptyBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], pure = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType.makeRef())
    writeDecl = cxx_writer.writer_code.Method('write_half', emptyBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], pure = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archByteType.makeRef())
    writeDecl = cxx_writer.writer_code.Method('write_byte', emptyBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], pure = True)
    memoryIfElements.append(writeDecl)
    lockDecl = cxx_writer.writer_code.Method('lock', emptyBody, cxx_writer.writer_code.voidType, 'pu', pure = True)
    memoryIfElements.append(lockDecl)
    unlockDecl = cxx_writer.writer_code.Method('unlock', emptyBody, cxx_writer.writer_code.voidType, 'pu', pure = True)
    memoryIfElements.append(unlockDecl)
    memoryIfDecl = cxx_writer.writer_code.ClassDeclaration('MemoryInterface', memoryIfElements)
    classes.append(memoryIfDecl)
    # Now I check if it is the case of creating a local memory
    readMemAliasCode = ''
    writeMemAliasCode = ''
    aliasAttrs = []
    aliasParams = []
    aliasInit = []
    for alias in self.memAlias:
        aliasAttrs.append(cxx_writer.writer_code.Attribute(alias.alias, resourceType[alias.alias].makeRef(), 'pri'))
        aliasParams.append(cxx_writer.writer_code.Parameter(alias.alias, resourceType[alias.alias].makeRef()))
        aliasInit.append(alias.alias + '(' + alias.alias + ')')
        readMemAliasCode += 'if(address == ' + str(alias.address) + '){\nreturn ' + alias.alias + ';\n}\n'
        writeMemAliasCode += 'if(address == ' + str(alias.address) + '){\n' + alias.alias + ' = datum;\nreturn;\n}\n'
    if self.memory:
        memoryElements = []
        emptyBody = cxx_writer.writer_code.Code('')
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + 'return *(' + str(archWordType.makePointer()) + ')(this->memory + (unsigned long)address);')
        addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
        readDecl = cxx_writer.writer_code.Method('read_word', readBody, archWordType, 'pu', [addressParam])
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + 'return *(' + str(archHWordType.makePointer()) + ')(this->memory + (unsigned long)address);')
        readDecl = cxx_writer.writer_code.Method('read_half', readBody, archHWordType, 'pu', [addressParam])
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + 'return *(' + str(archByteType.makePointer()) + ')(this->memory + (unsigned long)address);')
        readDecl = cxx_writer.writer_code.Method('read_byte', readBody, archByteType, 'pu', [addressParam])
        memoryElements.append(readDecl)
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + '*(' + str(archWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
        addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
        datumParam = cxx_writer.writer_code.Parameter('datum', archWordType.makeRef())
        writeDecl = cxx_writer.writer_code.Method('write_word', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam])
        memoryElements.append(writeDecl)
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + '*(' + str(archHWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
        datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType.makeRef())
        writeDecl = cxx_writer.writer_code.Method('write_half', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam])
        memoryElements.append(writeDecl)
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + '*(' + str(archByteType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
        datumParam = cxx_writer.writer_code.Parameter('datum', archByteType.makeRef())
        writeDecl = cxx_writer.writer_code.Method('write_byte', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam])
        memoryElements.append(writeDecl)
        lockDecl = cxx_writer.writer_code.Method('lock', emptyBody, cxx_writer.writer_code.voidType, 'pu')
        memoryElements.append(lockDecl)
        unlockDecl = cxx_writer.writer_code.Method('unlock', emptyBody, cxx_writer.writer_code.voidType, 'pu')
        memoryElements.append(unlockDecl)
        arrayAttribute = cxx_writer.writer_code.Attribute('memory', cxx_writer.writer_code.charPtrType, 'pri')
        memoryElements.append(arrayAttribute)
        memoryElements += aliasAttrs
        localMemDecl = cxx_writer.writer_code.ClassDeclaration('LocalMemory', memoryElements, [memoryIfDecl.getType()])
        constructorBody = cxx_writer.writer_code.Code('this->memory = new char[size];')
        constructorParams = [cxx_writer.writer_code.Parameter('size', cxx_writer.writer_code.uintType)]
        publicMemConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams + aliasParams, ['size(size)'] + aliasInit)
        localMemDecl.addConstructor(publicMemConstr)
        destructorBody = cxx_writer.writer_code.Code('delete [] this->memory;')
        publicMemDestr = cxx_writer.writer_code.Destructor(destructorBody, 'pu')
        localMemDecl.addDestructor(publicMemDestr)
        classes.append(localMemDecl)
    # Finally I create all the necessary TLM memory ports
    # TODO: create using all the newest TLM 2.0 the TLM ports; remember also
    # to consider endianess issues
    return classes

def getCPPProc(self, model):
    # creates the class describing the processor
    from isa import resolveBitType
    fetchWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize) + '>')
    includes = fetchWordType.getIncludes()
    codeString = ''
    if self.beginOp:
        codeString += 'this->beginOp();\n'
    codeString += 'while(true){\n'
    codeString += 'unsigned int numCycles = 0;\n'
    codeString += str(fetchWordType) + ' bitString = '
    # Now I have to check what is the fetch: if there is a TLM port or
    # if I have to access local memory
    if self.memory:
        # I perform the fetch from the local memory
        codeString += self.memory[0]
    else:
        for name, isFetch  in self.tlmPorts.items():
            if isFetch:
                codeString += name
        if codeString.endswith('= '):
            raise Exception('No TLM port was chosen for the instruction fetch')
    codeString += '.read_word(this->' + self.fetchReg[0]
    if model.startswith('func'):
        if self.fetchReg[1] < 0:
            codeString += str(self.fetchReg[1])
        else:
            codeString += '+' + str(self.fetchReg[1])
    codeString += ');\n'
    if self.instructionCache:
        codeString += 'std::map< ' + str(fetchWordType) + ', Instruction * >::iterator cachedInstr = Processor::instrCache.find(bitstring);'
        codeString += """
        if(cachedInstr != Processor::instrCache.end()){
            // I can call the instruction, I have found it
            numCycles = cachedInstr->second->behavior();
        }
        else{
            // The current instruction is not present in the cache:
            // I have to perform the normal decoding phase ...
        """
    codeString += """int instrId = decoder.decode(bitString);
    Instruction * instr = Processor::INSTRUCTIONS[instrId];
    """
    if self.instructionCache:
        codeString += """instr->setParams(bitString);
            numCycles = instr->behavior();
            // ... and then add the instruction to the cache
        """
        codeString += 'instrCache.insert( std::pair< ' + str(fetchWordType) + ', Instruction * >(bitstring, instr) );'
        codeString += """
            Processor::INSTRUCTIONS[instrId] = instr->replicate();
        }
        """
        includes.append('map')
    else:
        codeString += 'instr->behavior(bitString)\n';
    if self.systemc or model.startswith('acc'):
        # Code for keeping time with systemc
        pass
    else:
        codeString += 'this->totalCycles += numCycles;\n'
    codeString += '}'

    processorElements = []
    mainLoopCode = cxx_writer.writer_code.Code(codeString, includes)
    mainLoopMethod = cxx_writer.writer_code.Method('mainLoop', mainLoopCode, cxx_writer.writer_code.voidType, 'pu')
    processorElements.append(mainLoopMethod)
    if self.beginOp:
        beginOpMethod = cxx_writer.writer_code.Method('beginOp', self.beginOp, cxx_writer.writer_code.voidType, 'pri')
        processorElements.append(beginOpMethod)
    if self.endOp:
        endOpMethod = cxx_writer.writer_code.Method('endOp', self.endOp, cxx_writer.writer_code.voidType, 'pri')
        processorElements.append(endOpMethod)
    if self.resetOp:
        resetOpMethod = cxx_writer.writer_code.Method('resetOp', self.resetOp, cxx_writer.writer_code.voidType, 'pu')
        processorElements.append(resetOpMethod)
    decoderAttribute = cxx_writer.writer_code.Attribute('decoder', cxx_writer.writer_code.Type('Decoder', 'decoder.hpp'), 'pri')
    processorElements.append(decoderAttribute)
    # Lets now add the registers, the reg banks, the aliases, etc.
    # We also need to add the memory
    initElements = []
    bodyInits = ''
    bodyDestructor = ''
    aliasInit = {}
    for reg in self.regs:
        attribute = cxx_writer.writer_code.Attribute(reg.name, resourceType[reg.name], 'pu')
        initElements.append(reg.name + '(\"' + reg.name + '\")')
        processorElements.append(attribute)
    for regB in self.regBanks:
        attribute = cxx_writer.writer_code.Attribute(regB.name, resourceType[regB.name].makePointer(), 'pu')
        bodyInits += 'this->' + regB.name + ' = new ' + str(resourceType[regB.name]) + '[' + str(regB.numRegs) + '];\n'
        bodyDestructor += 'delete [] this->' + regB.name + ';\n'
        processorElements.append(attribute)
    for alias in self.aliasRegs:
        attribute = cxx_writer.writer_code.Attribute(alias.name, resourceType[alias.name], 'pu')
        aliasInit[alias.name] = (alias.name + '(&' + alias.initAlias + ', ' + str(alias.offset) + ')')
        processorElements.append(attribute)
    for aliasB in self.aliasRegBanks:
        attribute = cxx_writer.writer_code.Attribute(aliasB.name, resourceType[aliasB.name].makePointer(), 'pu')
        bodyInits += 'this->' + aliasB.name + ' = new ' + str(resourceType[aliasB.name]) + '[' + str(aliasB.numRegs) + '];\n'
        bodyDestructor += 'delete [] this->' + aliasB.name + ';\n'
        # Lets now deal with the initialization of the single elements of the regBank
        from processor import extractRegInterval
        if isinstance(aliasB.initAlias, type('')):
            index = extractRegInterval(aliasB.initAlias)
            curIndex = index[0]
            for i in range(0, aliasB.numRegs):
                bodyInits += 'this->' + aliasB.name + '[' + str(i) + '].updateAlias(' + aliasB.initAlias[:aliasB.initAlias.find('[')] + '[' + str(curIndex) + ']);\n'
                curIndex += 1
        else:
            curIndex = 0
            for i in initAlias:
                index = extractRegInterval(i)
                for i in range(index[0], index[1] + 1):
                    bodyInits += 'this->' + aliasB.name + '[' + str(curIndex) + '].updateAlias(' + aliasB.initAlias[:aliasB.initAlias.find('[')] + '[' + str(i) + ']);\n'
                    curIndex += 1
        processorElements.append(attribute)
    # the initialization of the aliases must be chained (we should
    # create an initialization graph since an alias might depend on another one ...)
    aliasGraph = NX.XDiGraph()
    for alias in self.aliasRegs + self.aliasRegBanks:
        aliasGraph.add_node(alias)
    for alias in self.aliasRegs + self.aliasRegBanks:
        for initAlias in self.aliasRegs + self.aliasRegBanks:
            if alias.initAlias == initAlias.name:
                aliasGraph.add_edge(initAlias, alias)
    # TODO: now I have to check for loops, if there are then the alias assignment is not valid
    # TODO: I do a topological sort and take the elements in this ordes and I add them to the initialization;
    # note that the ones whose initialization depend on banks (either register or alias) have to be
    # postponed after the creation of the arrays
    if self.memory:
        attribute = cxx_writer.writer_code.Attribute(self.memory[0], cxx_writer.writer_code.Type('LocalMemory', 'memory.hpp'), 'pu')
        initMemCode = self.memory[0] + '(' + str(self.memory[1])
        for memAl in self.memAlias:
            initMemCode += ', ' + memAl.alias
        initMemCode += ')'
        initElements.append(initMemCode)
        processorElements.append(attribute)
    for tlmPortName in self.tlmPorts.keys():
        attribute = cxx_writer.writer_code.Attribute(tlmPortName, cxx_writer.writer_code.Type('TLMPORT', 'memory.hpp'), 'pu')
        processorElements.append(attribute)        
    if self.systemc or model.startswith('acc'):
        # Here we need to insert the quantum keeper etc.
        pass
    else:
        totCyclesAttribute = cxx_writer.writer_code.Attribute('totalCycles', cxx_writer.writer_code.uintType, 'pu')
        bodyInits += 'this->totalCycles = 0;\n'
        processorElements.append(totCyclesAttribute)
    IntructionType = cxx_writer.writer_code.Type('Instruction', include = 'instructions.hpp')
    IntructionTypePtr = IntructionType.makePointer()
    instructionsAttribute = cxx_writer.writer_code.Attribute('INSTRUCTIONS',
                            IntructionTypePtr.makePointer(), 'pri', True, 'NULL')
    cacheAttribute = cxx_writer.writer_code.Attribute('instrCache',
                        cxx_writer.writer_code.TemplateType('std::map',
                            [fetchWordType, IntructionTypePtr], 'map'), 'pri', True)
    numProcAttribute = cxx_writer.writer_code.Attribute('numInstances',
                            cxx_writer.writer_code.intType, 'pri', True, '0')
    processorElements += [cacheAttribute, instructionsAttribute, numProcAttribute]
    # Ok, here I have to create the code for the constructor: I have to
    # initialize the INSTRUCTIONS array, the local memory (if present)
    # the TLM ports
    constrCode = 'Processor::numInstances++;\nif(Processor::INSTRUCTIONS == NULL){\n'
    constrCode += '// Initialization of the array holding the initial instance of the instructions\n'
    maxInstrId = max([instr.id for instr in self.isa.instructions.values()]) + 1
    constrCode += 'Processor::INSTRUCTIONS = new Instruction *[' + str(maxInstrId + 1) + '];\n'
    for name, instr in self.isa.instructions.items():
        constrCode += 'Processor::INSTRUCTIONS[' + str(instr.id) + '] = new ' + name + '();\n'
    constrCode += 'Processor::INSTRUCTIONS[' + str(maxInstrId) + '] = new InvalidInstr();\n'
    constrCode += '}\n'
    constrCode += bodyInits
    # TODO: now I have to complete initializing the alias graph, print the remaining
    # nodes in topological order
    if self.systemc or model.startswith('acc'):
        # TODO: We also need to initialize the quantuum keeper etc
        constrCode += 'SC_THREAD(mainLoop);\n'
    else:
        constrCode += 'this->totalCycles = 0;'
    constrCode += 'end_module();'
    constructorBody = cxx_writer.writer_code.Code(constrCode)
    constructorParams = [cxx_writer.writer_code.Parameter('name', cxx_writer.writer_code.sc_module_nameType), 
                cxx_writer.writer_code.Parameter('latency', cxx_writer.writer_code.sc_timeType)]
    publicConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, ['sc_module(name)'] + initElements)
    destrCode = """Processor::numInstances--;
    if(Processor::numInstances == 0){
        for(int i = 0; i < """ + str(maxInstrId + 1) + """; i++){
            delete Processor::INSTRUCTIONS[i];
        }
        delete [] Processor::INSTRUCTIONS;
        Processor::INSTRUCTIONS = NULL;
        std::map< """ + str(fetchWordType) + """, Instruction * >::iterator cacheIter, cacheEnd;
        for(cacheIter = Processor::instrCache.begin(), cacheEnd = Processor::instrCache.end(); cacheIter != cacheEnd; cacheIter++){
            delete cacheIter->second;
        }
    }
    """
    destrCode += bodyDestructor
    destructorBody = cxx_writer.writer_code.Code(destrCode)
    publicDestr = cxx_writer.writer_code.Destructor(destructorBody, 'pu')
    processorDecl = cxx_writer.writer_code.SCModule('Processor', processorElements)
    processorDecl.addConstructor(publicConstr)
    processorDecl.addDestructor(publicDestr)
    return processorDecl

def getCPPIf(self, model):
    # creates the interface which is used by the tools
    # to access the processor core
    return None

def getCPPExternalPorts(self, model):
    # creates the processor external ports used for the
    # communication with the external world (the memory port
    # is not among this ports, it is treated separately)
    return None

def getTestMainCode(self):
    # Returns the code for the file which contains the main
    # routine for the execution of the tests.
    # actually it is nothing but a file which includes
    # boost/test/auto_unit_test.hpp and defines
    # BOOST_AUTO_TEST_MAIN and BOOST_TEST_DYN_LINK
    code = '#define BOOST_AUTO_TEST_MAIN\n#define BOOST_TEST_DYN_LINK\n#include <boost/test/auto_unit_test.hpp>'
    mainCode = cxx_writer.writer_code.Code(code)
    return mainCode

def getMainCode(self, model):
    # Returns the code which instantiate the processor
    # in order to execute simulations
    code = 'return 0;'
    mainCode = cxx_writer.writer_code.Code(code)
    parameters = [cxx_writer.writer_code.Parameter('argc', cxx_writer.writer_code.intType), cxx_writer.writer_code.Parameter('argv', cxx_writer.writer_code.charPtrType.makePointer())]
    function = cxx_writer.writer_code.Function('main', code, cxx_writer.writer_code.intType, parameters)
    return mainCode
