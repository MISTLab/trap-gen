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

assignmentOps = ['=', '+=', '-=', '*=', '/=', '|=', '&=', '^=', '<<=', '>>=']
binaryOps = ['+', '-', '*', '/', '|', '&', '^', '<<', '>>']
unaryOps = ['~']
comparisonOps = ['<', '>', '<=', '>=', '==', '!=']
regMaxType = None
resourceType = {}
baseInstrInitElement = ''
aliasGraph = None
testNames = []

hash_map_include = """
#ifdef __GNUC__
#ifdef __GNUC_MINOR__
#if (__GNUC__ >= 4 && __GNUC_MINOR__ >= 3)
#include <tr1/unordered_map>
#define template_map std::tr1::unordered_map
#else
#include <ext/hash_map>
#define  template_map __gnu_cxx::hash_map
#endif
#else
#include <ext/hash_map>
#define  template_map __gnu_cxx::hash_map
#endif
#else
#ifdef _WIN32
#include <hash_map>
#define  template_map stdext::hash_map
#else
#include <map>
#define  template_map std::map
#endif
#endif
"""

def getRegistersBitfields(self):
    addedKeys = []
    defineCode = ''
    numKeys = 0
    for reg in self.regs + self.regBanks:
        for key in reg.bitMask.keys():
            if not key in addedKeys:
                defineCode += '#define key_' + key + ' ' + str(numKeys) + '\n'
                addedKeys.append(key)
                numKeys += 1
    return cxx_writer.writer_code.Code(defineCode + '\n\n')

def getCPPRegClass(self, model, regType):
    # returns the class implementing the current register; I have to
    # define all the operators;
    emptyBody = cxx_writer.writer_code.Code('')
    regWidthType = regMaxType

    registerType = cxx_writer.writer_code.Type('Register')
    InnerFieldType = cxx_writer.writer_code.Type('InnerField')
    registerElements = []
    normalRegType = regType.makeNormal()

    # First of all I determine if there is the need to create a const element
    if self.constValue != None and type(self.constValue) != type({}):
        assignValueItem = str(self.constValue)
        readValueItem = str(self.constValue)
    elif model.startswith('acc') or type(self.delay) == type({}) or self.delay == 0:
        assignValueItem = 'this->value'
        readValueItem = 'this->value'
    else:
        assignValueItem = 'this->updateSlot[' + str(self.delay - 1) + '] = true;\nthis->values[' + str(self.delay - 1) + ']'
        readValueItem = 'this->value'


    ####################### Lets declare the operators used to access the register fields ##############
    if self.bitMask:
        codeOperatorBody = 'switch(bitField){\n'
        for key in self.bitMask.keys():
            codeOperatorBody += 'case key_' + key + ':{\nreturn this->field_' + key + ';\nbreak;\n}\n'
        codeOperatorBody += 'default:{\nreturn this->field_empty;\nbreak;\n}\n}\n'
    else:
        codeOperatorBody = 'return this->field_empty;'
    operatorBody = cxx_writer.writer_code.Code(codeOperatorBody)
    operatorParam = [cxx_writer.writer_code.Parameter('bitField', cxx_writer.writer_code.intType)]
    operatorDecl = cxx_writer.writer_code.MemberOperator('[]', operatorBody, InnerFieldType.makeRef(), 'pu', operatorParam, noException = True)
    registerElements.append(operatorDecl)

    ################ Methods used for the update of delayed registers ######################
    if not model.startswith('acc') and type(self.delay) != type({}) and self.delay > 0:
        clockCycleCode = """if(this->updateSlot[0]){
                    this->value = this->values[0];
                    this->updateSlot[0] = false;
                }
                """
        for i in range(1, self.delay):
            clockCycleCode += """if(this->updateSlot[""" + str(i) + """]){
                        this->values[""" + str(i - 1) + """] = this->values[""" + str(i) + """];
                        this->updateSlot[""" + str(i) + """] = false;
                        this->updateSlot[""" + str(i - 1) + """] = true;
                    }
                    """
        clockCycleBody = cxx_writer.writer_code.Code(clockCycleCode)
        clockCycleMethod = cxx_writer.writer_code.Method('clockCycle', clockCycleBody, cxx_writer.writer_code.voidType, 'pu', noException = True)
        registerElements.append(clockCycleMethod)
    if self.constValue == None or type(self.constValue) == type({}):
        immediateWriteCode = 'this->value = value;\n'
        if not model.startswith('acc') and type(self.delay) != type({}) and self.delay > 0:
            for i in range(0, self.delay):
                immediateWriteCode += 'this->updateSlot[' + str(i) + '] = false;\n'
    else:
        immediateWriteCode = ''
    immediateWriteBody = cxx_writer.writer_code.Code(immediateWriteCode)
    immediateWriteParam = [cxx_writer.writer_code.Parameter('value', regMaxType.makeRef().makeConst())]
    immediateWriteMethod = cxx_writer.writer_code.Method('immediateWrite', immediateWriteBody, cxx_writer.writer_code.voidType, 'pu', immediateWriteParam, noException = True)
    registerElements.append(immediateWriteMethod)

    if not model.startswith('acc') and type(self.delay) != type({}) and self.delay > 0:
        readNewValueCode = ''
        delays = range(0, self.delay)
        delays.reverse()
        if self.offset:
            for i in delays:
                readNewValueCode += """if(this->updateSlot[""" + str(i) + """]){
                            return this->values[""" + str(i) + """] + """ + str(self.offset) + """;
                        }
                        """
            readNewValueCode += 'return this->value + ' + str(self.offset) + ';\n'
        else:
            for i in delays:
                readNewValueCode += """if(this->updateSlot[""" + str(i) + """]){
                            return this->values[""" + str(i) + """];
                        }
                        """
            readNewValueCode += 'return this->value;\n'
    else:
        if not model.startswith('acc') and self.offset:
            readNewValueCode = 'return this->value + ' + str(self.offset) + ';\n'
        else:
            readNewValueCode = 'return this->value;\n'
        for i in range(0, self.delay):
            immediateWriteCode += 'this->updateSlot[' + str(i) + '] = false;\n'
    readNewValueBody = cxx_writer.writer_code.Code(readNewValueCode)
    readNewValueMethod = cxx_writer.writer_code.Method('readNewValue', readNewValueBody, regMaxType, 'pu', noException = True)
    registerElements.append(readNewValueMethod)

    #################### Lets declare the normal operators (implementation of the pure operators of the base class) ###########
    for i in unaryOps:
        if self.offset and not model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code('return ' + i + '(' + readValueItem + ' + ' + str(self.offset) + ');')
        else:
            operatorBody = cxx_writer.writer_code.Code('return ' + i + '(' + readValueItem + ');')
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu')
        registerElements.append(operatorDecl)
    # Now I have the three versions of the operators, depending whether they take
    # in input the integer value, the specific register or the base one
    # INTEGER
    for i in assignmentOps:
        if self.constValue != None and type(self.constValue) != type({}):
            operatorBody = cxx_writer.writer_code.Code('return *this;')
        else:
            operatorBody = cxx_writer.writer_code.Code(assignValueItem + ' ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regType.makeRef(), 'pu', [operatorParam])
        registerElements.append(operatorDecl)
    # SPECIFIC REGISTER
    for i in binaryOps:
        if self.offset and not model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code('return ((' + readValueItem + '  + ' + str(self.offset) + ') ' + i + ' (other.value + ' + str(self.offset) + '));')
        else:
            operatorBody = cxx_writer.writer_code.Code('return (' + readValueItem + ' ' + i + ' other.value);')
        operatorParam = cxx_writer.writer_code.Parameter('other', regType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True)
        registerElements.append(operatorDecl)
    for i in comparisonOps:
        if self.offset and not model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code('return ((' + readValueItem + ' + ' + str(self.offset) + ') ' + i + ' (other.value + ' + str(self.offset) + '));')
        else:
            operatorBody = cxx_writer.writer_code.Code('return (' + readValueItem + ' ' + i + ' other.value);')
        operatorParam = cxx_writer.writer_code.Parameter('other', regType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True)
        registerElements.append(operatorDecl)
    for i in assignmentOps:
        if self.constValue != None and type(self.constValue) != type({}):
            operatorBody = cxx_writer.writer_code.Code('return *this;')
        else:
            operatorBody = cxx_writer.writer_code.Code(assignValueItem + ' ' + i + ' other.value;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', regType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regType.makeRef(), 'pu', [operatorParam])
        registerElements.append(operatorDecl)
    # GENERIC REGISTER: this case is look more complicated; actually I simply used the
    # operators of parameter other
    for i in binaryOps:
        if self.offset and not model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code('return ((' + readValueItem + '  + ' + str(self.offset) + ') ' + i + ' other);')
        else:
            operatorBody = cxx_writer.writer_code.Code('return (' + readValueItem + ' ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True)
        registerElements.append(operatorDecl)
    for i in comparisonOps:
        if self.offset and not model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code('return ((' + readValueItem + '  + ' + str(self.offset) + ') ' + i + ' other);')
        else:
            operatorBody = cxx_writer.writer_code.Code('return (' + readValueItem + ' ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True)
        registerElements.append(operatorDecl)
    for i in assignmentOps:
        if self.constValue != None and type(self.constValue) != type({}):
            operatorBody = cxx_writer.writer_code.Code('return *this;')
        else:
            operatorBody = cxx_writer.writer_code.Code(assignValueItem + ' ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regType.makeRef(), 'pu', [operatorParam])
        registerElements.append(operatorDecl)
    # Scalar value cast operator
    if self.offset and not model.startswith('acc'):
        operatorBody = cxx_writer.writer_code.Code('return (' + readValueItem + '  + ' + str(self.offset) + ');')
    else:
        operatorBody = cxx_writer.writer_code.Code('return ' + readValueItem + ';')
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), operatorBody, cxx_writer.writer_code.Type(''), 'pu', const = True, noException = True)
    registerElements.append(operatorIntDecl)

    # Constructors
    fieldInit = []
    if not model.startswith('acc') and type(self.delay) != type({}) and self.delay > 0:
        for field in self.bitMask.keys():
            fieldInit.append('field_' + field + '(this->value, this->values[' + str(self.delay - 1) + '], this->updateSlot[' + str(self.delay - 1) + '])')
    else:
        for field in self.bitMask.keys():
            fieldInit.append('field_' + field + '(this->value)')
    if self.constValue != None and type(self.constValue) != type({}):
        constructorCode = 'this->value = ' + readValueItem + ';\n'
    else:
        constructorCode = 'this->value = 0;\n'
    if not model.startswith('acc') and type(self.delay) != type({}) and self.delay != 0:
        for i in range(0, self.delay):
            constructorCode += 'this->updateSlot[' + str(i) + '] = false;\n'
    constructorBody = cxx_writer.writer_code.Code(constructorCode)
    constructorParams = [cxx_writer.writer_code.Parameter('name', cxx_writer.writer_code.sc_module_nameType)]
    publicMainClassConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, ['Register(name, ' + str(self.bitWidth) + ')'] + fieldInit)
    publicMainClassEmptyConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', initList = ['Register(sc_gen_unique_name(\"' + regType.name + '\"), ' + str(self.bitWidth) + ')'] + fieldInit)

    # Stream Operators
    outStreamType = cxx_writer.writer_code.Type('std::ostream', 'ostream')
    code = 'stream << std::hex << std::showbase << ' + readValueItem + ' << std::dec;\nreturn stream;'
    operatorBody = cxx_writer.writer_code.Code(code)
    operatorParam = cxx_writer.writer_code.Parameter('stream', outStreamType.makeRef())
    operatorDecl = cxx_writer.writer_code.MemberOperator('<<', operatorBody, outStreamType.makeRef(), 'pu', [operatorParam], const = True)
    registerElements.append(operatorDecl)

    # Attributes and inner classes declarations
    attrs = []
    innerClasses = []
    for field, length in self.bitMask.items():
        InnerFieldElems = []
        # Here I have to define the classes that represent the different fields
        negatedMask = ''
        mask = ''
        fieldLenMask = ''
        onesMask = ''.join(['1' for i in range(0, self.bitWidth)])
        for i in range(0, self.bitWidth):
            if (i >= length[0]) and (i <= length[1]):
                negatedMask = '0' + negatedMask
                mask = '1' + mask
            else:
                negatedMask = '1' + negatedMask
                mask = '0' + mask
            if i <= (length[1] - length[0]):
                fieldLenMask = '1' + fieldLenMask
            else:
                fieldLenMask = '0' + fieldLenMask
        operatorCode = ''
        if not model.startswith('acc') and type(self.delay) != type({}) and self.delay > 0:
            operatorCode += 'this->lastValid = true;\n'
            if type(readValueItem) != type(0):
                if onesMask != negatedMask:
                    operatorCode += 'this->valueLast = (this->value & ' + hex(int(negatedMask, 2)) + ');\n'
                operatorCode += 'this->valueLast |= '
                if length[0] > 0:
                    operatorCode += '((other & ' + hex(int(fieldLenMask, 2)) + ') << ' + str(length[0]) + ');\n'
                else:
                    operatorCode += 'other;\n'
        else:
            if type(readValueItem) != type(0):
                if onesMask != negatedMask:
                    operatorCode += 'this->value &= ' + hex(int(negatedMask, 2)) + ';\n'
                operatorCode += 'this->value |= '
                if length[0] > 0:
                    operatorCode += '((other & ' + hex(int(fieldLenMask, 2)) + ') << ' + str(length[0]) + ');\n'
                else:
                    operatorCode += 'other;\n'
        operatorCode += 'return *this;'
        operatorBody = cxx_writer.writer_code.Code(operatorCode)
        operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
        operatorEqualDecl = cxx_writer.writer_code.MemberOperator('=', operatorBody, cxx_writer.writer_code.Type('InnerField').makeRef(), 'pu', [operatorParam])
        InnerFieldElems.append(operatorEqualDecl)
        operatorCode = 'return (this->value & ' + hex(int(mask, 2)) + ')'
        if length[0] > 0:
            operatorCode += ' >> ' + str(length[0])
        operatorCode += ';'
        operatorBody = cxx_writer.writer_code.Code(operatorCode)
        operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), operatorBody, cxx_writer.writer_code.Type(''), 'pu', const = True)
        InnerFieldElems.append(operatorIntDecl)
        fieldAttribute = cxx_writer.writer_code.Attribute('value', regMaxType.makeRef(), 'pri')
        InnerFieldElems.append(fieldAttribute)
        if not model.startswith('acc') and type(self.delay) != type({}) and self.delay > 0:
            fieldAttribute = cxx_writer.writer_code.Attribute('valueLast', regMaxType.makeRef(), 'pri')
            InnerFieldElems.append(fieldAttribute)
            fieldAttribute = cxx_writer.writer_code.Attribute('lastValid', cxx_writer.writer_code.boolType.makeRef(), 'pri')
            InnerFieldElems.append(fieldAttribute)
        constructorParams = [cxx_writer.writer_code.Parameter('value', regMaxType.makeRef())]
        constructorInit = ['value(value)']
        if not model.startswith('acc') and type(self.delay) != type({}) and self.delay > 0:
            constructorParams.append(cxx_writer.writer_code.Parameter('valueLast', regMaxType.makeRef()))
            constructorInit.append('valueLast(valueLast)')
            constructorParams.append(cxx_writer.writer_code.Parameter('lastValid', cxx_writer.writer_code.boolType.makeRef()))
            constructorInit.append('lastValid(lastValid)')
        publicConstr = cxx_writer.writer_code.Constructor(cxx_writer.writer_code.Code(''), 'pu', constructorParams, constructorInit)
        InnerFieldClass = cxx_writer.writer_code.ClassDeclaration('InnerField_' + field, InnerFieldElems, [cxx_writer.writer_code.Type('InnerField')])
        InnerFieldClass.addConstructor(publicConstr)
        publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
        InnerFieldClass.addDestructor(publicDestr)
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
    publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    InnerFieldClass.addDestructor(publicDestr)
    innerClasses.append(InnerFieldClass)
    fieldAttribute = cxx_writer.writer_code.Attribute('field_empty', InnerFieldClass.getType(), 'pri')
    attrs.append(fieldAttribute)
    valueAttribute = cxx_writer.writer_code.Attribute('value', regWidthType, 'pri')
    attrs.append(valueAttribute)
    if self.offset and not model.startswith('acc'):
        offsetAttribute = cxx_writer.writer_code.Attribute('offset', cxx_writer.writer_code.intType, 'pri')
        attrs.append(offsetAttribute)
    if not model.startswith('acc') and type(self.delay) != type({}) and self.delay != 0:
        delaySlotAttribute = cxx_writer.writer_code.Attribute('values[' + str(self.delay) + ']', regWidthType, 'pri')
        attrs.append(delaySlotAttribute)
        updateSlotAttribute = cxx_writer.writer_code.Attribute('updateSlot[' + str(self.delay) + ']', cxx_writer.writer_code.boolType, 'pri')
        attrs.append(updateSlotAttribute)
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
    constructorCode = 'this->bitWidth = bitWidth;\nend_module();'
    if model.startswith('acc'):
        constructorCode = 'this->locked = false;\n' + constructorCode
    constructorBody = cxx_writer.writer_code.Code(constructorCode)
    constructorParams = [cxx_writer.writer_code.Parameter('name', cxx_writer.writer_code.sc_module_nameRefType.makeConst()),
                cxx_writer.writer_code.Parameter('bitWidth', cxx_writer.writer_code.uintType)]
    publicConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, ['sc_module(name)'])

    ################ Lock and Unlock methods used for hazards detection ######################
    if model.startswith('acc'):
        lockedAttribute = cxx_writer.writer_code.Attribute('locked', cxx_writer.writer_code.boolType, 'pri')
        registerElements.append(lockedAttribute)
        lockBody = cxx_writer.writer_code.Code('this->locked = true;')
        lockMethod = cxx_writer.writer_code.Method('lock', lockBody, cxx_writer.writer_code.voidType, 'pu', inline = True, noException = True)
        registerElements.append(lockMethod)
        if not self.externalClock:
            unlockBody = cxx_writer.writer_code.Code('this->locked = false;\nthis->hazardEvent.notify();')
        else:
            unlockBody = cxx_writer.writer_code.Code('this->locked = false;')
        unlockMethod = cxx_writer.writer_code.Method('unlock', unlockBody, cxx_writer.writer_code.voidType, 'pu', inline = True, noException = True)
        registerElements.append(unlockMethod)
        isLockedBody = cxx_writer.writer_code.Code('return this->locked;')
        isLockedMethod = cxx_writer.writer_code.Method('isLocked', isLockedBody, cxx_writer.writer_code.boolType, 'pu', inline = True, noException = True)
        registerElements.append(isLockedMethod)
        if not self.externalClock:
            waitHazardBody = cxx_writer.writer_code.Code('wait(this->hazardEvent);')
            waitHazardMethod = cxx_writer.writer_code.Method('waitHazard', waitHazardBody, cxx_writer.writer_code.voidType, 'pu', inline = True, noException = True)
            registerElements.append(waitHazardMethod)
            hazardEventAttribute = cxx_writer.writer_code.Attribute('hazardEvent', cxx_writer.writer_code.sc_eventType, 'pri')
            registerElements.append(hazardEventAttribute)

    ################ Methods used for the management of delayed registers ######################
    if not model.startswith('acc'):
        clockCycleMethod = cxx_writer.writer_code.Method('clockCycle', emptyBody, cxx_writer.writer_code.voidType, 'pu', virtual = True, noException = True)
        registerElements.append(clockCycleMethod)
        immediateWriteParam = [cxx_writer.writer_code.Parameter('value', regMaxType.makeRef().makeConst())]
        immediateWriteMethod = cxx_writer.writer_code.Method('immediateWrite', emptyBody, cxx_writer.writer_code.voidType, 'pu', immediateWriteParam, pure = True, noException = True)
        registerElements.append(immediateWriteMethod)
        readNewValueMethod = cxx_writer.writer_code.Method('readNewValue', emptyBody, regMaxType, 'pu', pure = True, noException = True)
        registerElements.append(readNewValueMethod)

    ################ Operators working with the base class, employed when polimorphism is used ##################
    # First lets declare the class which will be used to manipulate the
    # bitfields
    InnerFieldType = cxx_writer.writer_code.Type('InnerField')
    operatorBody = cxx_writer.writer_code.Code('*this = (unsigned int)other;\nreturn *this;')
    operatorParam = cxx_writer.writer_code.Parameter('other', InnerFieldType.makeRef().makeConst())
    operatorEqualInnerDecl = cxx_writer.writer_code.MemberOperator('=', operatorBody, InnerFieldType.makeRef(), 'pu', [operatorParam])
    operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
    operatorEqualDecl = cxx_writer.writer_code.MemberOperator('=', emptyBody, InnerFieldType.makeRef(), 'pu', [operatorParam], pure = True)
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), emptyBody, cxx_writer.writer_code.Type(''), 'pu', const = True, pure = True)
    InnerFieldClass = cxx_writer.writer_code.ClassDeclaration('InnerField', [operatorEqualInnerDecl, operatorEqualDecl, operatorIntDecl])
    publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    InnerFieldClass.addDestructor(publicDestr)

    # Now lets procede with the members of the main class
    operatorParam = cxx_writer.writer_code.Parameter('bitField', cxx_writer.writer_code.intType)
    operatorDecl = cxx_writer.writer_code.MemberOperator('[]', emptyBody, InnerFieldClass.getType().makeRef(), 'pu', [operatorParam], pure = True, noException = True)
    registerElements.append(operatorDecl)
    for i in unaryOps:
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, emptyBody, regMaxType, 'pu', pure = True)
        registerElements.append(operatorDecl)
    for i in binaryOps:
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, emptyBody, regMaxType, 'pu', [operatorParam], const = True, pure = True)
        registerElements.append(operatorDecl)
    for i in comparisonOps:
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, emptyBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True, pure = True)
        registerElements.append(operatorDecl)

    pureDeclTypes = [regMaxType, registerType]
    for pureDecls in pureDeclTypes:
        for i in assignmentOps:
            operatorParam = cxx_writer.writer_code.Parameter('other', pureDecls.makeRef().makeConst())
            operatorDecl = cxx_writer.writer_code.MemberOperator(i, emptyBody, registerType.makeRef(), 'pu', [operatorParam], pure = True)
            registerElements.append(operatorDecl)
    # Stream Operators
    outStreamType = cxx_writer.writer_code.Type('std::ostream', 'ostream')
    operatorParam = cxx_writer.writer_code.Parameter('other', outStreamType.makeRef())
    operatorDecl = cxx_writer.writer_code.MemberOperator('<<', emptyBody, outStreamType.makeRef(), 'pu', [operatorParam], const = True, pure = True)
    registerElements.append(operatorDecl)
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), emptyBody, cxx_writer.writer_code.Type(''), 'pu', const = True, pure = True, noException = True)
    registerElements.append(operatorIntDecl)

    ################ Here we determine the different register types which have to be declared ##################
    customRegBanksElemens = []
    for i in self.regBanks:
        customRegBanksElemens += i.getConstRegs()
        customDelayElem = i.getDelayRegs()
        for j in customDelayElem:
            if not j.name in [rb.name for rb in customRegBanksElemens]:
                customRegBanksElemens.append(j)

    global resourceType
    regTypes = []
    regTypeNames = []
    bitFieldHash = {}
    for reg in self.regs + self.regBanks + customRegBanksElemens:
        bitFieldSig = ''
        for maskName, maskPos in reg.bitMask.items():
            bitFieldSig += maskName + str(maskPos[0]) + str(maskPos[1])
        if not bitFieldSig in bitFieldHash:
            bitFieldHash[bitFieldSig] = len(bitFieldHash)
        curName = str(reg.bitWidth) + '_' + str(bitFieldHash[bitFieldSig])
        if not model.startswith('acc'):
            curName += '_' + str(reg.offset)
        if type(reg.constValue) == type(0):
            curName += '_' + str(reg.constValue)
        if type(reg.delay) == type(0) and not model.startswith('acc') and reg.delay > 0:
            curName += '_' + str(reg.delay)
        if not curName in regTypeNames:
            regTypes.append(reg)
            regTypeNames.append(curName)
        regTypeName = 'Reg' + str(reg.bitWidth) + '_' + str(bitFieldHash[bitFieldSig])
        if reg.offset and not model.startswith('acc'):
            regTypeName += '_off_' + str(reg.offset)
        if type(reg.constValue) == type(0):
            regTypeName += '_const_' + str(reg.constValue)
        if type(reg.delay) == type(0) and not model.startswith('acc') and reg.delay > 0:
            regTypeName += '_delay_' + str(reg.delay)
        resourceType[reg.name] = cxx_writer.writer_code.Type(regTypeName, 'registers.hpp')
        if reg in self.regBanks:
            if reg.constValue or (reg.delay and not model.startswith('acc')):
                resourceType[reg.name + '_baseType'] = resourceType[reg.name]
                resourceType[reg.name] = cxx_writer.writer_code.Type('RegisterBankClass', 'registers.hpp')
            else:
                resourceType[reg.name] = resourceType[reg.name].makePointer()
    realRegClasses = []
    for regType in regTypes:
        realRegClasses.append(regType.getCPPClass(model, resourceType[regType.name]))
    ################ End of part where we determine the different register types which have to be declared ##################

    registerDecl = cxx_writer.writer_code.SCModule('Register', registerElements)
    registerDecl.addConstructor(publicConstr)

    ################ Finally I put everything together##################
    classes = [InnerFieldClass, registerDecl] + realRegClasses

    # I also need to declare a global RegisterBank Class in case there are register banks
    # with constant registers
    hasRegBankClass = False
    for reg in self.regBanks:
        if reg.constValue:
            hasRegBankClass = True
            break
    if hasRegBankClass:
        registerType = cxx_writer.writer_code.Type('Register', 'registers.hpp')
        regBankElements = []
        regBankElements.append(cxx_writer.writer_code.Attribute('registers', registerType.makePointer().makePointer(), 'pri'))
        regBankElements.append(cxx_writer.writer_code.Attribute('size', cxx_writer.writer_code.uintType, 'pri'))
        setNewRegisterBody = cxx_writer.writer_code.Code("""if(numReg > this->size - 1){
            THROW_EXCEPTION("Register number " << numReg << " is out of register bank boundaries");
        }
        else{
            this->registers[numReg] = newReg;
        }""")
        setNewRegisterBody.addInclude('utils.hpp')
        setNewRegisterParams = [cxx_writer.writer_code.Parameter('numReg', cxx_writer.writer_code.uintType), cxx_writer.writer_code.Parameter('newReg', registerType.makePointer())]
        setNewRegisterMethod = cxx_writer.writer_code.Method('setNewRegister', setNewRegisterBody, cxx_writer.writer_code.voidType, 'pu', setNewRegisterParams, inline = True)
        regBankElements.append(setNewRegisterMethod)
        setSizeBody = cxx_writer.writer_code.Code("""
            for(unsigned int i = 0; i < this->size; i++){
                if(this->registers[i] != NULL){
                    delete this->registers[i];
                }
            }
            if(this->registers != NULL){
                delete [] this->registers;
            }
            this->size = size;
            this->registers = new """ + str(registerType.makePointer()) + """[this->size];
            for(unsigned int i = 0; i < this->size; i++){
                this->registers[i] = NULL;
            }
        """)
        setSizeParams = [cxx_writer.writer_code.Parameter('size', cxx_writer.writer_code.uintType)]
        setSizeMethod = cxx_writer.writer_code.Method('setSize', setSizeBody, cxx_writer.writer_code.voidType, 'pu', setSizeParams, inline = True, noException = True)
        regBankElements.append(setSizeMethod)
        operatorBody = cxx_writer.writer_code.Code('return *(this->registers[numReg]);')
        operatorParam = [cxx_writer.writer_code.Parameter('numReg', cxx_writer.writer_code.uintType)]
        operatorDecl = cxx_writer.writer_code.MemberOperator('[]', operatorBody, registerType.makeRef(), 'pu', operatorParam)
        regBankElements.append(operatorDecl)
        regBankClass = cxx_writer.writer_code.ClassDeclaration('RegisterBankClass', regBankElements)
        constructorBody = cxx_writer.writer_code.Code("""this->size = size;
            this->registers = new """ + str(registerType.makePointer()) + """[this->size];
            for(unsigned int i = 0; i < this->size; i++){
                this->registers[i] = NULL;
            }
        """)
        constructorParams = [cxx_writer.writer_code.Parameter('size', cxx_writer.writer_code.uintType)]
        publicRegBankConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams)
        regBankClass.addConstructor(publicRegBankConstr)
        constructorBody = cxx_writer.writer_code.Code("""this->size = 0;
            this->registers = NULL;
        """)
        publicRegBankConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu')
        regBankClass.addConstructor(publicRegBankConstr)
        destructorBody = cxx_writer.writer_code.Code("""
            for(unsigned int i = 0; i < this->size; i++){
                if(this->registers[i] != NULL){
                    delete this->registers[i];
                }
            }
            if(this->registers != NULL){
                delete [] this->registers;
            }
        """)
        publicRegBankDestr = cxx_writer.writer_code.Destructor(destructorBody, 'pu', True)
        regBankClass.addDestructor(publicRegBankDestr)
        classes.append(regBankClass)

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
    operatorParam = [cxx_writer.writer_code.Parameter('bitField', cxx_writer.writer_code.intType)]
    operatorDecl = cxx_writer.writer_code.MemberOperator('[]', operatorBody, InnerFieldType.makeRef(), 'pu', operatorParam)
    aliasElements.append(operatorDecl)

    ################ Lock and Unlock methods used for hazards detection ######################
    if model.startswith('acc'):
        lockBody = cxx_writer.writer_code.Code('this->reg->lock();')
        lockMethod = cxx_writer.writer_code.Method('lock', lockBody, cxx_writer.writer_code.voidType, 'pu', inline = True, noException = True)
        aliasElements.append(lockMethod)
        unlockBody = cxx_writer.writer_code.Code('this->reg->unlock();')
        unlockMethod = cxx_writer.writer_code.Method('unlock', unlockBody, cxx_writer.writer_code.voidType, 'pu', inline = True, noException = True)
        aliasElements.append(unlockMethod)
        isLockedBody = cxx_writer.writer_code.Code('return this->reg->isLocked();')
        isLockedMethod = cxx_writer.writer_code.Method('isLocked', isLockedBody, cxx_writer.writer_code.boolType, 'pu', inline = True, noException = True)
        aliasElements.append(isLockedMethod)
        if not self.externalClock:
            waitHazardBody = cxx_writer.writer_code.Code('this->reg->waitHazard();')
            waitHazardMethod = cxx_writer.writer_code.Method('waitHazard', waitHazardBody, cxx_writer.writer_code.voidType, 'pu', inline = True, noException = True)
            aliasElements.append(waitHazardMethod)

    ################ Methods used for the management of delayed registers ######################
    if not model.startswith('acc'):
        immediateWriteBody = isLockedBody = cxx_writer.writer_code.Code('this->reg->immediateWrite(value);')
        immediateWriteParam = [cxx_writer.writer_code.Parameter('value', regMaxType.makeRef().makeConst())]
        immediateWriteMethod = cxx_writer.writer_code.Method('immediateWrite', immediateWriteBody, cxx_writer.writer_code.voidType, 'pu', immediateWriteParam, virtual = True, noException = True)
        aliasElements.append(immediateWriteMethod)
        readNewValueBody = isLockedBody = cxx_writer.writer_code.Code('return this->reg->readNewValue();')
        readNewValueMethod = cxx_writer.writer_code.Method('readNewValue', readNewValueBody, regMaxType, 'pu', virtual = True, noException = True)
        aliasElements.append(readNewValueMethod)

    #################### Lets declare the normal operators (implementation of the pure operators of the base class) ###########
    for i in unaryOps:
        if model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code('return ' + i + '*this->reg;')
        else:
            operatorBody = cxx_writer.writer_code.Code('return ' + i + '(*this->reg + this->offset);')
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu')
        aliasElements.append(operatorDecl)
    # Now I have the three versions of the operators, depending whether they take
    # in input the integer value, the specific register or the base one
    # INTEGER
#     for i in binaryOps:
#         operatorBody = cxx_writer.writer_code.Code('return (*this->reg ' + i + ' other);')
#         operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
#         operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True)
#         aliasElements.append(operatorDecl)
#     for i in comparisonOps:
#         operatorBody = cxx_writer.writer_code.Code('return (*this->reg ' + i + ' (other - this->offset));')
#         operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
#         operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True)
#         aliasElements.append(operatorDecl)
    for i in assignmentOps:
        operatorBody = cxx_writer.writer_code.Code('*this->reg ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, aliasType.makeRef(), 'pu', [operatorParam], inline = True)
        aliasElements.append(operatorDecl)
    # Alias Register
    for i in binaryOps:
        if model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code('return (*this->reg ' + i + ' *other.reg);')
        else:
            operatorBody = cxx_writer.writer_code.Code('return ((*this->reg + this->offset) ' + i + ' *other.reg);')
        operatorParam = cxx_writer.writer_code.Parameter('other', aliasType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True)
        aliasElements.append(operatorDecl)
#    for i in comparisonOps:
#        operatorBody = cxx_writer.writer_code.Code('return ((*this->reg + this->offset) ' + i + ' *other.reg);')
#        operatorParam = cxx_writer.writer_code.Parameter('other', aliasType.makeRef().makeConst())
#        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True)
#        aliasElements.append(operatorDecl)
    for i in assignmentOps:
        operatorBody = cxx_writer.writer_code.Code('*this->reg ' + i + ' *other.reg;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', aliasType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, aliasType.makeRef(), 'pu', [operatorParam])
        aliasElements.append(operatorDecl)
    # GENERIC REGISTER:
    for i in binaryOps:
        if model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code('return (*this->reg ' + i + ' other);')
        else:
            operatorBody = cxx_writer.writer_code.Code('return ((*this->reg + this->offset) ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True, inline = True)
        aliasElements.append(operatorDecl)
    for i in comparisonOps:
        if model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code('return (*this->reg ' + i + ' other);')
        else:
            operatorBody = cxx_writer.writer_code.Code('return ((*this->reg + this->offset) ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True)
        aliasElements.append(operatorDecl)
    for i in assignmentOps:
        operatorBody = cxx_writer.writer_code.Code('*this->reg ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, aliasType.makeRef(), 'pu', [operatorParam])
        aliasElements.append(operatorDecl)
    # Scalar value cast operator
    if model.startswith('acc'):
        operatorBody = cxx_writer.writer_code.Code('return *this->reg;')
    else:
        operatorBody = cxx_writer.writer_code.Code('return *this->reg + this->offset;')
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), operatorBody, cxx_writer.writer_code.Type(''), 'pu', const = True, noException = True, inline = True)
    aliasElements.append(operatorIntDecl)

    # Constructor: takes as input the initial register
    constructorBody = cxx_writer.writer_code.Code('')
    constructorParams = [cxx_writer.writer_code.Parameter('reg', registerType.makePointer())]
    constructorInit = ['reg(reg)']
    if not model.startswith('acc'):
        constructorParams.append(cxx_writer.writer_code.Parameter('offset', cxx_writer.writer_code.uintType, initValue = '0'))
        constructorInit += ['offset(offset)', 'defaultOffset(0)']
    publicMainClassConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, constructorInit)
    publicMainEmptyClassConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu')
    # Constructor: takes as input the initial alias
    constructorBody = cxx_writer.writer_code.Code('initAlias->referredAliases.insert(this);\nthis->referringAliases.insert(initAlias);')
    constructorParams = [cxx_writer.writer_code.Parameter('initAlias', aliasType.makePointer())]
    publicAliasConstrInit = ['reg(initAlias->reg)']
    if not model.startswith('acc'):
        constructorParams.append(cxx_writer.writer_code.Parameter('offset', cxx_writer.writer_code.uintType, initValue = '0'))
        publicAliasConstrInit += ['offset(initAlias->offset + offset)', 'defaultOffset(offset)']
    publicAliasConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, publicAliasConstrInit)

    # Stream Operators
    outStreamType = cxx_writer.writer_code.Type('std::ostream', 'ostream')
    if model.startswith('acc'):
        code = 'stream << *this->reg;\nreturn stream;'
    else:
        code = 'stream << *this->reg + this->offset;\nreturn stream;'
    operatorBody = cxx_writer.writer_code.Code(code)
    operatorParam = cxx_writer.writer_code.Parameter('stream', outStreamType.makeRef())
    operatorDecl = cxx_writer.writer_code.MemberOperator('<<', operatorBody, outStreamType.makeRef(), 'pu', [operatorParam], const = True)
    aliasElements.append(operatorDecl)

    # Update method: updates the register pointed by this alias
    if model.startswith('acc'):
        updateCode = """this->reg = newAlias.reg;
        std::set<Alias *>::iterator referredIter, referredEnd;
        for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
            (*referredIter)->newReferredAlias(newAlias.reg);
        }
        """
    else:
        updateCode = """this->reg = newAlias.reg;
        this->offset = newAlias.offset + newOffset;
        this->defaultOffset = newOffset;
        std::set<Alias *>::iterator referredIter, referredEnd;
        for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
            (*referredIter)->newReferredAlias(newAlias.reg, newAlias.offset + newOffset);
        }
        """
    updateCode += """newAlias.referredAliases.insert(this);
        std::set<Alias *>::iterator referringIter, referringEnd;
        for(referringIter = this->referringAliases.begin(), referringEnd = this->referringAliases.end(); referringIter != referringEnd; referringIter++){
            (*referringIter)->referredAliases.erase(this);
        }
        this->referringAliases.clear();
        this->referringAliases.insert(&newAlias);
        """
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam = [cxx_writer.writer_code.Parameter('newAlias', aliasType.makeRef())]
    if not model.startswith('acc'):
        updateParam.append(cxx_writer.writer_code.Parameter('newOffset', cxx_writer.writer_code.uintType, initValue = '0'))
    updateDecl = cxx_writer.writer_code.Method('updateAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', updateParam)
    aliasElements.append(updateDecl)
    if model.startswith('acc'):
        updateCode = """this->reg = &newAlias;
        std::set<Alias *>::iterator referredIter, referredEnd;
        for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
            (*referredIter)->newReferredAlias(&newAlias);
        }
        """
    else:
        updateCode = """this->reg = &newAlias;
        this->offset = newOffset;
        this->defaultOffset = 0;
        std::set<Alias *>::iterator referredIter, referredEnd;
        for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
            (*referredIter)->newReferredAlias(&newAlias, newOffset);
        }
        """
    updateCode += """std::set<Alias *>::iterator referringIter, referringEnd;
    for(referringIter = this->referringAliases.begin(), referringEnd = this->referringAliases.end(); referringIter != referringEnd; referringIter++){
        (*referringIter)->referredAliases.erase(this);
    }
    this->referringAliases.clear();
    """
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam = [cxx_writer.writer_code.Parameter('newAlias', registerType.makeRef())]
    if not model.startswith('acc'):
        updateParam.append(cxx_writer.writer_code.Parameter('newOffset', cxx_writer.writer_code.uintType, initValue = '0'))
    updateDecl = cxx_writer.writer_code.Method('updateAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', updateParam)
    aliasElements.append(updateDecl)
    if model.startswith('acc'):
        updateCode = """this->reg = newAlias;
        std::set<Alias *>::iterator referredIter, referredEnd;
        for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
            (*referredIter)->newReferredAlias(newAlias);
        }
        """
    else:
        updateCode = """this->reg = newAlias;
        this->offset = newOffset + this->defaultOffset;
        std::set<Alias *>::iterator referredIter, referredEnd;
        for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
            (*referredIter)->newReferredAlias(newAlias, newOffset);
        }
        """
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam = [cxx_writer.writer_code.Parameter('newAlias', registerType.makePointer())]
    if not model.startswith('acc'):
        updateParam.append(cxx_writer.writer_code.Parameter('newOffset', cxx_writer.writer_code.uintType))
    updateDecl = cxx_writer.writer_code.Method('newReferredAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', updateParam)
    aliasElements.append(updateDecl)

    # Finally I declare the class and pass to it all the declared members
    regAttribute = cxx_writer.writer_code.Attribute('reg', registerType.makePointer(), 'pri')
    aliasElements.append(regAttribute)
    if not model.startswith('acc'):
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
    archDWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize*2) + '>')
    archWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize) + '>')
    archHWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize/2) + '>')
    archByteType = resolveBitType('BIT<' + str(self.byteSize) + '>')
    # First of all I create the memory base class
    classes = []
    memoryIfElements = []
    emptyBody = cxx_writer.writer_code.Code('')
    addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
    readDecl = cxx_writer.writer_code.Method('read_dword', emptyBody, archDWordType, 'pu', [addressParam], pure = True, const = len(self.tlmPorts) == 0, noException = True)
    memoryIfElements.append(readDecl)
    readDecl = cxx_writer.writer_code.Method('read_word', emptyBody, archWordType, 'pu', [addressParam], pure = True, const = len(self.tlmPorts) == 0, noException = True)
    memoryIfElements.append(readDecl)
    readDecl = cxx_writer.writer_code.Method('read_half', emptyBody, archHWordType, 'pu', [addressParam], pure = True, const = len(self.tlmPorts) == 0, noException = True)
    memoryIfElements.append(readDecl)
    readDecl = cxx_writer.writer_code.Method('read_byte', emptyBody, archByteType, 'pu', [addressParam], pure = True, const = len(self.tlmPorts) == 0, noException = True)
    memoryIfElements.append(readDecl)
    readDeclDBGBody = cxx_writer.writer_code.Code('return this->read_dword(address);')
    readDecl = cxx_writer.writer_code.Method('read_dword_dbg', readDeclDBGBody, archDWordType, 'pu', [addressParam], virtual = True, const = len(self.tlmPorts) == 0, noException = True)
    memoryIfElements.append(readDecl)
    readDeclDBGBody = cxx_writer.writer_code.Code('return this->read_word(address);')
    readDecl = cxx_writer.writer_code.Method('read_word_dbg', readDeclDBGBody, archWordType, 'pu', [addressParam], virtual = True, const = len(self.tlmPorts) == 0, noException = True)
    memoryIfElements.append(readDecl)
    readDeclDBGBody = cxx_writer.writer_code.Code('return this->read_half(address);')
    readDecl = cxx_writer.writer_code.Method('read_half_dbg', readDeclDBGBody, archHWordType, 'pu', [addressParam], virtual = True, const = len(self.tlmPorts) == 0, noException = True)
    memoryIfElements.append(readDecl)
    readDeclDBGBody = cxx_writer.writer_code.Code('return this->read_byte(address);')
    readDecl = cxx_writer.writer_code.Method('read_byte_dbg', readDeclDBGBody, archByteType, 'pu', [addressParam], virtual = True, const = len(self.tlmPorts) == 0, noException = True)
    memoryIfElements.append(readDecl)

    datumParam = cxx_writer.writer_code.Parameter('datum', archDWordType)
    writeDecl = cxx_writer.writer_code.Method('write_dword', emptyBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], pure = True, noException = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archWordType)
    writeDecl = cxx_writer.writer_code.Method('write_word', emptyBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], pure = True, noException = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType)
    writeDecl = cxx_writer.writer_code.Method('write_half', emptyBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], pure = True, noException = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archByteType)
    writeDecl = cxx_writer.writer_code.Method('write_byte', emptyBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], pure = True, noException = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archDWordType)
    writeDeclDBGBody = cxx_writer.writer_code.Code('this->write_dword(address, datum);')
    writeDecl = cxx_writer.writer_code.Method('write_dword_dbg', writeDeclDBGBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], virtual = True, noException = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archWordType)
    writeDeclDBGBody = cxx_writer.writer_code.Code('this->write_word(address, datum);')
    writeDecl = cxx_writer.writer_code.Method('write_word_dbg', writeDeclDBGBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], virtual = True, noException = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType)
    writeDeclDBGBody = cxx_writer.writer_code.Code('this->write_half(address, datum);')
    writeDecl = cxx_writer.writer_code.Method('write_half_dbg', writeDeclDBGBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], virtual = True, noException = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archByteType)
    writeDeclDBGBody = cxx_writer.writer_code.Code('this->write_byte(address, datum);')
    writeDecl = cxx_writer.writer_code.Method('write_byte_dbg', writeDeclDBGBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], virtual = True, noException = True)
    memoryIfElements.append(writeDecl)

    lockDecl = cxx_writer.writer_code.Method('lock', emptyBody, cxx_writer.writer_code.voidType, 'pu', pure = True)
    memoryIfElements.append(lockDecl)
    unlockDecl = cxx_writer.writer_code.Method('unlock', emptyBody, cxx_writer.writer_code.voidType, 'pu', pure = True)
    memoryIfElements.append(unlockDecl)
    memoryIfDecl = cxx_writer.writer_code.ClassDeclaration('MemoryInterface', memoryIfElements)
    publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    memoryIfDecl.addDestructor(publicDestr)
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
        readMemAliasCode += 'if(address == ' + hex(long(alias.address)) + '){\nreturn this->' + alias.alias + ';\n}\n'
        writeMemAliasCode += 'if(address == ' + hex(long(alias.address)) + '){\n this->' + alias.alias + ' = datum;\nreturn;\n}\n'
    checkAddressCode = 'if(address >= this->size){\nTHROW_ERROR("Address " << std::hex << std::showbase << address << " out of memory");\n}\n'
    memoryElements = []
    emptyBody = cxx_writer.writer_code.Code('')
    addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + '\nreturn *(' + str(archDWordType.makePointer()) + ')(this->memory + (unsigned long)address);')
    readBody.addInclude('utils.hpp')
    readDecl = cxx_writer.writer_code.Method('read_dword', readBody, archDWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, inline = True, noException = True)
    memoryElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + 'return *(' + str(archWordType.makePointer()) + ')(this->memory + (unsigned long)address);')
    readBody.addInclude('utils.hpp')
    readDecl = cxx_writer.writer_code.Method('read_word', readBody, archWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, inline = True, noException = True)
    memoryElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + 'return *(' + str(archHWordType.makePointer()) + ')(this->memory + (unsigned long)address);')
    readDecl = cxx_writer.writer_code.Method('read_half', readBody, archHWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, noException = True)
    memoryElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + 'return *(' + str(archByteType.makePointer()) + ')(this->memory + (unsigned long)address);')
    readDecl = cxx_writer.writer_code.Method('read_byte', readBody, archByteType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, noException = True)
    memoryElements.append(readDecl)
    addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + '*(' + str(archDWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
    datumParam = cxx_writer.writer_code.Parameter('datum', archDWordType)
    writeDecl = cxx_writer.writer_code.Method('write_dword', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], inline = True, noException = True)
    memoryElements.append(writeDecl)
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + '*(' + str(archWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
    datumParam = cxx_writer.writer_code.Parameter('datum', archWordType)
    writeDecl = cxx_writer.writer_code.Method('write_word', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], inline = True, noException = True)
    memoryElements.append(writeDecl)
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + '*(' + str(archHWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
    datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType)
    writeDecl = cxx_writer.writer_code.Method('write_half', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    memoryElements.append(writeDecl)
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + '*(' + str(archByteType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
    datumParam = cxx_writer.writer_code.Parameter('datum', archByteType)
    writeDecl = cxx_writer.writer_code.Method('write_byte', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    memoryElements.append(writeDecl)
    lockDecl = cxx_writer.writer_code.Method('lock', emptyBody, cxx_writer.writer_code.voidType, 'pu')
    memoryElements.append(lockDecl)
    unlockDecl = cxx_writer.writer_code.Method('unlock', emptyBody, cxx_writer.writer_code.voidType, 'pu')
    memoryElements.append(unlockDecl)
    arrayAttribute = cxx_writer.writer_code.Attribute('memory', cxx_writer.writer_code.charPtrType, 'pri')
    memoryElements.append(arrayAttribute)
    sizeAttribute = cxx_writer.writer_code.Attribute('size', cxx_writer.writer_code.uintType, 'pri')
    memoryElements.append(sizeAttribute)
    memoryElements += aliasAttrs
    localMemDecl = cxx_writer.writer_code.ClassDeclaration('LocalMemory', memoryElements, [memoryIfDecl.getType()])
    constructorBody = cxx_writer.writer_code.Code('this->memory = new char[size];')
    constructorParams = [cxx_writer.writer_code.Parameter('size', cxx_writer.writer_code.uintType)]
    publicMemConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams + aliasParams, ['size(size)'] + aliasInit)
    localMemDecl.addConstructor(publicMemConstr)
    destructorBody = cxx_writer.writer_code.Code('delete [] this->memory;')
    publicMemDestr = cxx_writer.writer_code.Destructor(destructorBody, 'pu', True)
    localMemDecl.addDestructor(publicMemDestr)
    classes.append(localMemDecl)

    return classes

def getCPPProc(self, model, trace):
    # creates the class describing the processor
    from isa import resolveBitType
    fetchWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize) + '>')
    includes = fetchWordType.getIncludes()
    interfaceType = cxx_writer.writer_code.Type(self.name + '_ABIIf', 'interface.hpp')
    ToolsManagerType = cxx_writer.writer_code.TemplateType('ToolsManager', [fetchWordType], 'ToolsIf.hpp')
    processorElements = []
    codeString = ''

    if not model.startswith('acc'):
        if self.instructionCache:
            codeString += 'template_map< ' + str(fetchWordType) + ', Instruction * >::iterator instrCacheEnd = Processor::instrCache.end();\n'
        if self.externalClock:
            codeString += 'if(this->waitCycles > 0){\nthis->waitCycles--;\nreturn;\n}\n\n'
        else:
            codeString += 'while(true){\n'
        codeString += 'unsigned int numCycles = 0;\n'

        #Here is the code to deal with interrupts
        orderedIrqList = sorted(self.irqs, lambda x,y: cmp(y.priority, x.priority))
        for irqPort in orderedIrqList:
            if irqPort != orderedIrqList[0]:
                codeString += 'else '
            codeString += 'if('
            if not irqPort.high:
                codeString += '!'
            codeString += irqPort.name
            if(irqPort.condition):
                codeString += ' && (' + irqPort.condition + ')'
            codeString += '){\n'
            codeString += irqPort.operation + '\n}\n'

        fetchCode = str(fetchWordType) + ' bitString = this->'
        # Now I have to check what is the fetch: if there is a TLM port or
        # if I have to access local memory
        if self.memory:
            # I perform the fetch from the local memory
            fetchCode += self.memory[0]
        else:
            for name, isFetch  in self.tlmPorts.items():
                if isFetch:
                    fetchCode += name
            if codeString.endswith('= '):
                raise Exception('No TLM port was chosen for the instruction fetch')
        fetchCode += '.read_word('
        fetchAddress = 'this->' + self.fetchReg[0]
        if self.instructionCache and self.fastFetch:
            pcVar = 'curPC'
        else:
            pcVar = 'this->' + self.fetchReg[0]
        if model.startswith('func'):
            if self.fetchReg[1] < 0:
                fetchAddress += str(self.fetchReg[1])
                if not (self.instructionCache and self.fastFetch):
                    pcVar += str(self.fetchReg[1])
            else:
                fetchAddress += ' + ' + str(self.fetchReg[1])
                if not (self.instructionCache and self.fastFetch):
                    pcVar += ' + ' + str(self.fetchReg[1])
        fetchCode += pcVar + ');\n'
        if self.instructionCache and self.fastFetch:
            codeString += str(fetchWordType) + ' curPC = ' + fetchAddress + ';\n'
        else:
            codeString += fetchCode
        if trace:
            codeString += 'std::cerr << \"Current PC: \" << std::hex << std::showbase << ' + pcVar + ' << std::endl;\n'
        if self.instructionCache:
            codeString += 'template_map< ' + str(fetchWordType) + ', Instruction * >::iterator cachedInstr = Processor::instrCache.find('
            if self.fastFetch:
                codeString += 'curPC);'
            else:
                codeString += 'bitString);'
            codeString += """
            if(cachedInstr != instrCacheEnd){
                // I can call the instruction, I have found it
                try{
                    #ifndef DISABLE_TOOLS
                    if(!(this->toolManager.newIssue(""" + pcVar + """, cachedInstr->second))){
                    #endif
                    numCycles = cachedInstr->second->behavior();
            """
            if trace:
                codeString += """
                    cachedInstr->second->printTrace();
                """
            codeString += """
                    #ifndef DISABLE_TOOLS
                    }
                """
            if trace:
                codeString += """else{
                    std::cerr << "Not executed Instruction because Tools anulled it" << std::endl << std::endl;
                }"""
            codeString += """
                    #endif
                }
                catch(annull_exception &etc){
            """
            if trace:
                codeString += """
                        cachedInstr->second->printTrace();
                        std::cerr << "Skipped Instruction " << cachedInstr->second->getInstructionName() << std::endl << std::endl;
                """
            codeString += """
                    numCycles = 0;
                }
            }
            else{
                // The current instruction is not present in the cache:
                // I have to perform the normal decoding phase ...
            """
        if self.instructionCache and self.fastFetch:
            codeString += fetchCode
        codeString += """int instrId = decoder.decode(bitString);
        Instruction * instr = Processor::INSTRUCTIONS[instrId];
        """
        codeString += """instr->setParams(bitString);
            try{
                #ifndef DISABLE_TOOLS
                if(!(this->toolManager.newIssue(""" + pcVar + """, instr))){
                #endif
                numCycles = instr->behavior();
        """
        if trace:
            codeString += """
                instr->printTrace();
            """
        codeString += """
                #ifndef DISABLE_TOOLS
                }
            """
        if trace:
            codeString += """else{
                std::cerr << "Not executed Instruction because Tools anulled it" << std::endl << std::endl;
            }"""
        codeString += """
                #endif
            }
            catch(annull_exception &etc){
        """
        if trace:
            codeString += """
                    instr->printTrace();
                    std::cerr << "Skipped Instruction " << instr->getInstructionName() << std::endl << std::endl;
            """
        codeString += """
                numCycles = 0;
            }
            // ... and then add the instruction to the cache
        """
        if self.instructionCache:
            if self.fastFetch:
                codeString += 'instrCache[curPC] = instr;'
            else:
                codeString += 'instrCache[bitString] = instr;'
            if not self.externalClock:
                codeString += """
                    instrCacheEnd = Processor::instrCache.end();"""
            codeString += """
                Processor::INSTRUCTIONS[instrId] = instr->replicate();
            }
            """
        if self.externalClock:
            codeString += 'this->waitCycles += numCycles;\n'
        elif len(self.tlmPorts) > 0 and model.endswith('LT'):
            codeString += 'this->quantKeeper.inc((numCycles + 1)*this->latency);\nif(this->quantKeeper.need_sync()) this->quantKeeper.sync();\n'
        elif model.startswith('acc') or self.systemc:
            codeString += 'wait((numCycles + 1)*this->latency);\n'
        else:
            codeString += 'this->totalCycles += (numCycles + 1);\n'
        codeString += 'this->numInstructions++;\n\n'
        # Now I have to call the update method for all the delayed registers
        for reg in self.regs:
            if reg.delay:
                codeString += reg.name + '.clockCycle();\n'
        for reg in self.regBanks:
            for regNum in reg.delay.keys():
                codeString += reg.name + '[' + str(regNum) + '].clockCycle();\n'
        if not self.externalClock:
            codeString += '}'
        mainLoopCode = cxx_writer.writer_code.Code(codeString)
        mainLoopCode.addInclude(includes)
        mainLoopCode.addInclude('customExceptions.hpp')
        mainLoopMethod = cxx_writer.writer_code.Method('mainLoop', mainLoopCode, cxx_writer.writer_code.voidType, 'pu')
        processorElements.append(mainLoopMethod)

    if self.beginOp:
        beginOpMethod = cxx_writer.writer_code.Method('beginOp', self.beginOp, cxx_writer.writer_code.voidType, 'pri')
        processorElements.append(beginOpMethod)
    if self.endOp:
        endOpMethod = cxx_writer.writer_code.Method('endOp', self.endOp, cxx_writer.writer_code.voidType, 'pri')
        processorElements.append(endOpMethod)
    if not self.resetOp:
        resetOpTemp = cxx_writer.writer_code.Code('')
    else:
        import copy
        resetOpTemp = copy.deepcopy(self.resetOp)
    initString = ''
    for elem in self.regBanks + self.aliasRegBanks:
        curId = 0
        for defValue in elem.defValues:
            try:
                if curId in elem.constValue.keys():
                    curId += 1
                    continue
            except AttributeError:
                pass
            if defValue != None:
                try:
                    if not type(defValue) == type(''):
                        enumerate(defValue)
                        # ok, the element is iterable, so it is an initialization
                        # with a constant and an offset
                        initString += elem.name + '[' + str(curId) + ']'
                        if model.startswith('acc'):
                            initString += ' = '
                        else:
                            initString += '.immediateWrite('
                        initString += str(defValue[0]) + ' + ' + str(defValue[1])
                        if model.startswith('acc'):
                            initString += ';\n'
                        else:
                            initString += ');\n'
                        continue
                except TypeError:
                    pass
                initString += elem.name + '[' + str(curId) + ']'
                if model.startswith('acc'):
                    initString += ' = '
                else:
                    initString += '.immediateWrite('
                try:
                    initString += hex(defValue)
                except TypeError:
                    initString += str(defValue)
                if model.startswith('acc'):
                    initString += ';\n'
                else:
                    initString += ');\n'
            curId += 1
    for elem in self.regs + self.aliasRegs:
        try:
            if elem.constValue != None:
                continue
        except AttributeError:
            pass
        if elem.defValue != None:
            try:
                if not type(elem.defValue) == type(''):
                    enumerate(elem.defValue)
                    # ok, the element is iterable, so it is an initialization
                    # with a constant and an offset
                    initString += elem.name
                    if model.startswith('acc'):
                        initString += ' = '
                    else:
                        initString += '.immediateWrite('
                    initString += str(elem.defValue[0]) + ' + ' + str(elem.defValue[1])
                    if model.startswith('acc'):
                        initString += ';\n'
                    else:
                        initString += ');\n'
                    continue
            except TypeError:
                pass
            initString += elem.name
            if model.startswith('acc'):
                initString += ' = '
            else:
                initString += '.immediateWrite('
            try:
                initString += hex(elem.defValue)
            except TypeError:
                initString += str(elem.defValue)
            if model.startswith('acc'):
                initString += ';\n'
            else:
                initString += ');\n'
    if model.startswith('acc'):
        for reg in self.regs:
            for pipeStage in self.pipes:
                initString += reg.name + '_' + pipeStage.name + ' = ' + reg.name + ';\n'
        for regB in self.regBanks:
            initString += 'for(int i = 0; i < ' + str(regB.numRegs) + '; i++){\n'
            for pipeStage in self.pipes:
                initString += regB.name + '_' + pipeStage.name + '[i] = ' + regB.name + '[i];\n'
            initString += '}\n'

    resetOpTemp.prependCode(initString)
    if self.beginOp:
        resetOpTemp.appendCode('//user-defined initialization\nthis->beginOp();\n')
    resetOpMethod = cxx_writer.writer_code.Method('resetOp', resetOpTemp, cxx_writer.writer_code.voidType, 'pu')
    processorElements.append(resetOpMethod)
    # Now I declare the end of elaboration method, called by systemc just before starting the simulation
    endElabCode = cxx_writer.writer_code.Code('this->resetOp();')
    endElabMethod = cxx_writer.writer_code.Method('end_of_elaboration', endElabCode, cxx_writer.writer_code.voidType, 'pu')
    processorElements.append(endElabMethod)
    if not model.startswith('acc'):
        decoderAttribute = cxx_writer.writer_code.Attribute('decoder', cxx_writer.writer_code.Type('Decoder', 'decoder.hpp'), 'pri')
        processorElements.append(decoderAttribute)
    interfaceAttribute = cxx_writer.writer_code.Attribute('abiIf', interfaceType.makePointer(), 'pu')
    processorElements.append(interfaceAttribute)
    toolManagerAttribute = cxx_writer.writer_code.Attribute('toolManager', ToolsManagerType, 'pu')
    processorElements.append(toolManagerAttribute)

    initElements = []
    bodyInits = ''
    bodyDestructor = ''
    aliasInit = {}
    bodyAliasInit = {}
    abiIfInit = ''

    if model.endswith('LT') and len(self.tlmPorts) > 0 and not self.externalClock:
        quantumKeeperType = cxx_writer.writer_code.Type('tlm_utils::tlm_quantumkeeper', 'tlm_utils/tlm_quantumkeeper.h')
        quantumKeeperAttribute = cxx_writer.writer_code.Attribute('quantKeeper', quantumKeeperType, 'pri')
        processorElements.append(quantumKeeperAttribute)
        bodyInits += 'quantKeeper.set_global_quantum( this->latency*100 );\nquantKeeper.reset();\n'

    # Lets now add the registers, the reg banks, the aliases, etc.
    # We also need to add the memory
    checkToolPipeStage = self.pipes[-1]
    for pipeStage in self.pipes:
        if pipeStage.checkTools:
            checkToolPipeStage = pipeStage
            break
    from processor import extractRegInterval
    for reg in self.regs:
        attribute = cxx_writer.writer_code.Attribute(reg.name, resourceType[reg.name], 'pu')
        initElements.append(reg.name + '(\"' + reg.name + '\")')
        abiIfInit += 'this->' + reg.name
        if model.startswith('acc'):
            abiIfInit += '_' + checkToolPipeStage.name
        abiIfInit += ', '
        processorElements.append(attribute)
        if model.startswith('acc'):
            for pipeStage in self.pipes:
                attribute = cxx_writer.writer_code.Attribute(reg.name + '_' + pipeStage.name, resourceType[reg.name], 'pu')
                processorElements.append(attribute)
    for regB in self.regBanks:
        attribute = cxx_writer.writer_code.Attribute(regB.name, resourceType[regB.name], 'pu')
        if regB.constValue or (not model.startswith('acc') and regB.delay):
            # There are constant registers, so I have to declare the special register bank
            bodyInits += 'this->' + regB.name + '.setSize(' + str(regB.numRegs) + ');\n'
            for i in range(0, regB.numRegs):
                if regB.constValue.has_key(i) or regB.delay.has_key(i):
                    bodyInits += 'this->' + regB.name + '.setNewRegister(' + str(i) + ', new ' + str(resourceType[regB.name + '[' + str(i) + ']']) + '());\n'
                else:
                    bodyInits += 'this->' + regB.name + '.setNewRegister(' + str(i) + ', new ' + str(resourceType[regB.name + '_baseType']) + '());\n'
            if model.startswith('acc'):
                for pipeStage in self.pipes:
                    bodyInits += 'this->' + regB.name + '_' + pipeStage.name + '.setSize(' + str(regB.numRegs) + ');\n'
                    for i in range(0, regB.numRegs):
                        if regB.constValue.has_key(i):
                            bodyInits += 'this->' + regB.name + '_' + pipeStage.name + '.setNewRegister(' + str(i) + ', new ' + str(resourceType[regB.name + '[' + str(i) + ']']) + '());\n'
                        else:
                            bodyInits += 'this->' + regB.name + '_' + pipeStage.name + '.setNewRegister(' + str(i) + ', new ' + str(resourceType[regB.name + '_baseType']) + '());\n'
        else:
            bodyInits += 'this->' + regB.name + ' = new ' + str(resourceType[regB.name].makeNormal()) + '[' + str(regB.numRegs) + '];\n'
            bodyDestructor += 'delete [] this->' + regB.name + ';\n'
            if model.startswith('acc'):
                for pipeStage in self.pipes:
                    bodyInits += 'this->' + regB.name + '_' + pipeStage.name + ' = new ' + str(resourceType[regB.name].makeNormal()) + '[' + str(regB.numRegs) + '];\n'
                    bodyDestructor += 'delete [] this->' + regB.name + '_' + pipeStage.name + ';\n'
        abiIfInit += 'this->' + regB.name
        if model.startswith('acc'):
            abiIfInit += '_' + checkToolPipeStage.name
        abiIfInit += ', '
        processorElements.append(attribute)
        if model.startswith('acc'):
            for pipeStage in self.pipes:
                attribute = cxx_writer.writer_code.Attribute(regB.name + '_' + pipeStage.name, resourceType[regB.name], 'pu')
                processorElements.append(attribute)
    for alias in self.aliasRegs:
        attribute = cxx_writer.writer_code.Attribute(alias.name, resourceType[alias.name], 'pu')
        # first of all I have to make sure that the alias does not refer to a delayed or constant
        # register bank, otherwise I have to initialize it in the constructor body and not
        # inline in the constuctor
        hasToDeclareInit = True
        if alias.initAlias.find('[') > -1:
            referredName = alias.initAlias[:alias.initAlias.find('[')]
            for regB in self.regBanks:
                if regB.name == referredName:
                    if regB.constValue or (not model.startswith('acc') and regB.delay):
                        hasToDeclareInit = False
                        break
        if hasToDeclareInit:
            aliasInitStr = alias.name + '(&' + alias.initAlias
            if not model.startswith('acc'):
                aliasInitStr += ', ' + str(alias.offset)
            aliasInit[alias.name] = (aliasInitStr + ')')

        index = extractRegInterval(alias.initAlias)
        if index:
            # we are dealing with a member of a register bank
            curIndex = index[0]
            bodyAliasInit[alias.name] = 'this->' + alias.name + '.updateAlias(this->' + alias.initAlias[:alias.initAlias.find('[')] + '[' + str(curIndex) + ']'
            if not model.startswith('acc'):
                bodyAliasInit[alias.name] += ', ' + str(alias.offset)
            bodyAliasInit[alias.name] += ');\n'
            if model.startswith('acc'):
                for pipeStage in self.pipes:
                    bodyAliasInit[alias.name] += 'this->' + alias.name + '_' + pipeStage.name + '.updateAlias(this->' + alias.initAlias[:alias.initAlias.find('[')] + '_' + pipeStage.name + '[' + str(curIndex) + ']'
                    bodyAliasInit[alias.name] += ');\n'
        else:
            bodyAliasInit[alias.name] = 'this->' + alias.name + '.updateAlias(this->' + alias.initAlias
            if not model.startswith('acc'):
                bodyAliasInit[alias.name] += ', ' + str(alias.offset)
            bodyAliasInit[alias.name] += ');\n'
            if model.startswith('acc'):
                for pipeStage in self.pipes:
                    bodyAliasInit[alias.name] += 'this->' + alias.name + '_' + pipeStage.name + '.updateAlias(this->' + alias.initAlias + '_' + pipeStage.name
                    bodyAliasInit[alias.name] += ');\n'
        abiIfInit += 'this->' + alias.name
        if model.startswith('acc'):
            abiIfInit += '_' + checkToolPipeStage.name
        abiIfInit += ', '
        processorElements.append(attribute)
        if model.startswith('acc'):
            for pipeStage in self.pipes:
                attribute = cxx_writer.writer_code.Attribute(alias.name + '_' + pipeStage.name, resourceType[alias.name], 'pu')
                processorElements.append(attribute)
    for aliasB in self.aliasRegBanks:
        attribute = cxx_writer.writer_code.Attribute(aliasB.name, resourceType[aliasB.name].makePointer(), 'pu')
        bodyAliasInit[aliasB.name] = 'this->' + aliasB.name + ' = new ' + str(resourceType[aliasB.name]) + '[' + str(aliasB.numRegs) + '];\n'
        bodyDestructor += 'delete [] this->' + aliasB.name + ';\n'
        if model.startswith('acc'):
            for pipeStage in self.pipes:
                bodyAliasInit[aliasB.name] += 'this->' + aliasB.name + '_' + pipeStage.name + ' = new ' + str(resourceType[aliasB.name]) + '[' + str(aliasB.numRegs) + '];\n'
                bodyDestructor += 'delete [] this->' + aliasB.name + '_' + pipeStage.name + ';\n'
        # Lets now deal with the initialization of the single elements of the regBank
        if isinstance(aliasB.initAlias, type('')):
            index = extractRegInterval(aliasB.initAlias)
            curIndex = index[0]
            for i in range(0, aliasB.numRegs):
                bodyAliasInit[aliasB.name] += 'this->' + aliasB.name + '[' + str(i) + '].updateAlias(this->' + aliasB.initAlias[:aliasB.initAlias.find('[')] + '[' + str(curIndex) + ']'
                if aliasB.offsets.has_key(i) and not model.startswith('acc'):
                    bodyAliasInit[aliasB.name] += ', ' + str(aliasB.offsets[i])
                bodyAliasInit[aliasB.name] += ');\n'
                curIndex += 1
            if model.startswith('acc'):
                for pipeStage in self.pipes:
                    curIndex = index[0]
                    for i in range(0, aliasB.numRegs):
                        bodyAliasInit[aliasB.name] += 'this->' + aliasB.name + '_' + pipeStage.name + '[' + str(i) + '].updateAlias(this->' + aliasB.initAlias[:aliasB.initAlias.find('[')] + '_' + pipeStage.name + '[' + str(curIndex) + ']'
                        bodyAliasInit[aliasB.name] += ');\n'
                        curIndex += 1
        else:
            curIndex = 0
            for curAlias in aliasB.initAlias:
                index = extractRegInterval(curAlias)
                if index:
                    for curRange in range(index[0], index[1] + 1):
                        bodyAliasInit[aliasB.name] += 'this->' + aliasB.name + '[' + str(curIndex) + '].updateAlias(this->' + curAlias[:curAlias.find('[')] + '[' + str(curRange) + ']'
                        if aliasB.offsets.has_key(curIndex) and not model.startswith('acc'):
                            bodyAliasInit[aliasB.name] += ', ' + str(aliasB.offsets[curIndex])
                        bodyAliasInit[aliasB.name] += ');\n'
                        curIndex += 1
                else:
                    bodyAliasInit[aliasB.name] += 'this->' + aliasB.name + '[' + str(curIndex) + '].updateAlias(this->' + curAlias + ')'
                    if aliasB.offsets.has_key(curIndex) and not model.startswith('acc'):
                        bodyAliasInit[aliasB.name] += ', ' + str(aliasB.offsets[curIndex])
                    bodyAliasInit[aliasB.name] += ');\n'
                    curIndex += 1
            if model.startswith('acc'):
                for pipeStage in self.pipes:
                    curIndex = 0
                    for curAlias in aliasB.initAlias:
                        index = extractRegInterval(curAlias)
                        if index:
                            for curRange in range(index[0], index[1] + 1):
                                bodyAliasInit[aliasB.name] += 'this->' + aliasB.name + '_' + pipeStage.name + '[' + str(curIndex) + '].updateAlias(this->' + curAlias[:curAlias.find('[')] + '_' + pipeStage.name + '[' + str(curRange) + ']'
                                bodyAliasInit[aliasB.name] += ');\n'
                                curIndex += 1
                        else:
                            bodyAliasInit[aliasB.name] += 'this->' + aliasB.name + '_' + pipeStage.name + '[' + str(curIndex) + '].updateAlias(this->' + curAlias + '_' + pipeStage.name + ')'
                            bodyAliasInit[aliasB.name] += ');\n'
                            curIndex += 1

        abiIfInit += 'this->' + aliasB.name
        if model.startswith('acc'):
            abiIfInit += '_' + checkToolPipeStage.name
        abiIfInit += ', '
        processorElements.append(attribute)
        if model.startswith('acc'):
            for pipeStage in self.pipes:
                attribute = cxx_writer.writer_code.Attribute(aliasB.name + '_' + pipeStage.name, resourceType[aliasB.name].makePointer(), 'pu')
                processorElements.append(attribute)
    abiIfInit = abiIfInit[:-2]
    # the initialization of the aliases must be chained (we should
    # create an initialization graph since an alias might depend on another one ...)
    global aliasGraph
    if float(NX.__version__) < 0.99:
        aliasGraph = NX.XDiGraph()
    else:
        aliasGraph = NX.DiGraph()
    for alias in self.aliasRegs + self.aliasRegBanks:
        aliasGraph.add_node(alias)
    for alias in self.aliasRegs + self.aliasRegBanks:
        initAliases = []
        if isinstance(alias.initAlias, type('')):
            bracketIdx = alias.initAlias.find('[')
            if bracketIdx > 0:
                initAliases.append(alias.initAlias[:bracketIdx])
            else:
                initAliases.append(alias.initAlias)
        else:
            for curAlias in alias.initAlias:
                bracketIdx = curAlias.find('[')
                if bracketIdx > 0:
                    initAliases.append(curAlias[:bracketIdx])
                else:
                    initAliases.append(curAlias)
        for initAlias in initAliases:
            for targetInit in self.aliasRegs + self.aliasRegBanks:
                if initAlias == targetInit.name:
                    aliasGraph.add_edge(targetInit, alias)
                elif self.isBank(initAlias):
                    aliasGraph.add_edge('stop', alias)
    # now I have to check for loops, if there are then the alias assignment is not valid
    if not NX.is_directed_acyclic_graph(aliasGraph):
        raise Exception('There is a circular dependency in the aliases initialization')
    # I do a topological sort and take the elements in this ordes and I add them to the initialization;
    # note that the ones whose initialization depend on banks (either register or alias)
    # have to be postponned after the creation of the arrays
    orderedNodes = NX.topological_sort(aliasGraph)
    orderedNodesTemp = []
    for alias in orderedNodes:
        if alias == 'stop':
            continue
        if self.isBank(alias.name):
            break
        aliasGraphRev = aliasGraph.reverse()
        if float(NX.__version__) < 0.99:
            edgeType = aliasGraphRev.edges(alias)[0][0]
        else:
            edgeType = aliasGraphRev.edges(alias, data = True)[0][0]
        if edgeType == 'stop':
            break
        if aliasInit.has_key(alias.name):
            initElements.append(aliasInit[alias.name])
        else:
            break
        orderedNodesTemp.append(alias)
    for alias in orderedNodesTemp:
        orderedNodes.remove(alias)
    # Now I have the remaining aliases, I have to add their initialization after
    # the registers has been created
    for alias in orderedNodes:
        if alias == 'stop':
            continue
        bodyInits += bodyAliasInit[alias.name]
    if self.memory:
        attribute = cxx_writer.writer_code.Attribute(self.memory[0], cxx_writer.writer_code.Type('LocalMemory', 'memory.hpp'), 'pu')
        initMemCode = self.memory[0] + '(' + str(self.memory[1])
        for memAl in self.memAlias:
            initMemCode += ', ' + memAl.alias
        initMemCode += ')'
        if self.memory[0] in self.abi.memories.keys():
            abiIfInit = 'this->' + self.memory[0] + ', ' + abiIfInit
        initElements.append(initMemCode)
        processorElements.append(attribute)
    for tlmPortName in self.tlmPorts.keys():
        attribute = cxx_writer.writer_code.Attribute(tlmPortName, cxx_writer.writer_code.Type('TLMMemory', 'externalPorts.hpp'), 'pu')
        initPortCode = tlmPortName + '(\"' + tlmPortName + '\"'
        if self.systemc and model.endswith('LT'):
            if self.externalClock:
                initPortCode += ', this->waitCycles'
            else:
                initPortCode += ', this->quantKeeper'
        for memAl in self.memAlias:
            initPortCode += ', ' + memAl.alias
        initPortCode += ')'
        if tlmPortName in self.abi.memories.keys():
            abiIfInit = 'this->' + tlmPortName + ', ' + abiIfInit
        initElements.append(initPortCode)
        processorElements.append(attribute)
    if self.systemc or model.startswith('acc'):
        if self.externalClock:
            totCyclesAttribute = cxx_writer.writer_code.Attribute('waitCycles', cxx_writer.writer_code.uintType, 'pu')
            processorElements.append(totCyclesAttribute)
            if hasCheckHazard and pipeStage.checkHazard:
                if self.externalClock:
                    codeString += 'if(!this->curInstruction->checkHazard()){\nreturn\n}\n'
                else:
                    codeString += 'this->curInstruction->checkHazard();\n'

            bodyInits += 'this->waitCycles = 0;\n'
            clockAttribute = cxx_writer.writer_code.Attribute('clock', cxx_writer.writer_code.TemplateType('sc_in', [cxx_writer.writer_code.boolType], 'systemc.h'), 'pu')
            processorElements.append(clockAttribute)
        else:
            latencyAttribute = cxx_writer.writer_code.Attribute('latency', cxx_writer.writer_code.sc_timeType, 'pu')
            processorElements.append(latencyAttribute)
    else:
        totCyclesAttribute = cxx_writer.writer_code.Attribute('totalCycles', cxx_writer.writer_code.uintType, 'pu')
        processorElements.append(totCyclesAttribute)
        bodyInits += 'this->totalCycles = 0;\n'
    numInstructions = cxx_writer.writer_code.Attribute('numInstructions', cxx_writer.writer_code.uintType, 'pu')
    processorElements.append(numInstructions)
    bodyInits += 'this->numInstructions = 0;\n'
    # Now I have to declare some special constants used to keep track of the loaded executable file
    entryPointAttr = cxx_writer.writer_code.Attribute('ENTRY_POINT', fetchWordType, 'pu')
    processorElements.append(entryPointAttr)
    bodyInits += 'this->ENTRY_POINT = 0;\n'
    progLimitAttr = cxx_writer.writer_code.Attribute('PROGRAM_LIMIT', fetchWordType, 'pu')
    processorElements.append(progLimitAttr)
    bodyInits += 'this->PROGRAM_LIMIT = 0;\n'
    abiIfInit = 'this->PROGRAM_LIMIT, ' + abiIfInit
    progStarttAttr = cxx_writer.writer_code.Attribute('PROGRAM_START', fetchWordType, 'pu')
    processorElements.append(progStarttAttr)
    bodyInits += 'this->PROGRAM_START = 0;\n'
    bodyInits += 'this->abiIf = new ' + str(interfaceType) + '(' + abiIfInit + ');\n'

    IntructionType = cxx_writer.writer_code.Type('Instruction', include = 'instructions.hpp')
    IntructionTypePtr = IntructionType.makePointer()
    instructionsAttribute = cxx_writer.writer_code.Attribute('INSTRUCTIONS',
                            IntructionTypePtr.makePointer(), 'pri', True, 'NULL')
    processorElements.append(instructionsAttribute)
    if self.instructionCache:
        cacheAttribute = cxx_writer.writer_code.Attribute('instrCache',
                        cxx_writer.writer_code.TemplateType('template_map',
                            [fetchWordType, IntructionTypePtr], hash_map_include), 'pri', True)
        processorElements.append(cacheAttribute)
    numProcAttribute = cxx_writer.writer_code.Attribute('numInstances',
                            cxx_writer.writer_code.intType, 'pri', True, '0')
    processorElements.append(numProcAttribute)

    for irqPort in self.irqs:
        if irqPort.tlm:
            irqPortType = cxx_writer.writer_code.Type('IntrTLMPort', 'irqPorts.hpp')
        else:
            irqPortType = cxx_writer.writer_code.Type('IntrSysCPort', 'irqPorts.hpp')
        irqSignalAttr = cxx_writer.writer_code.Attribute(irqPort.name, cxx_writer.writer_code.boolType, 'pri')
        irqPortAttr = cxx_writer.writer_code.Attribute(irqPort.name + '_port', irqPortType, 'pu')
        processorElements.append(irqSignalAttr)
        processorElements.append(irqPortAttr)
        initElements.append(irqPort.name + '_port(\"' + irqPort.name + '_IRQ\", ' + irqPort.name + ')')

    if model.startswith('acc'):
        # I have to instantiate the pipeline and its stages ...
        prevStage = ''
        for pipeStage in self.pipes:
            pipelineType = cxx_writer.writer_code.Type(pipeStage.name.upper() + '_PipeStage', 'pipeline.hpp')
            curStageAttr = cxx_writer.writer_code.Attribute(pipeStage.name + '_stage', pipelineType, 'pu')
            processorElements.append(curStageAttr)
            curPipeInit = ['\"' + pipeStage.name + '\"']
            if self.externalClock:
                curPipeInit.append('clock')
            else:
                curPipeInit.append('latency')
            for otherPipeStage in self.pipes:
                if otherPipeStage != pipeStage:
                    curPipeInit.append('&' + otherPipeStage.name + '_stage')
            if prevStage:
                curPipeInit.append('&' + prevStage)
            else:
                curPipeInit.append('NULL')
            if self.pipes.index(pipeStage) + 1 < len(self.pipes):
                curPipeInit.append('&' + self.pipes[self.pipes.index(pipeStage) + 1].name + '_stage')
            else:
                curPipeInit.append('NULL')
            if pipeStage == self.pipes[0]:
                for reg in self.regs:
                    curPipeInit = [reg.name] + curPipeInit
                for regB in self.regBanks:
                    curPipeInit = [regB.name] + curPipeInit
                # It is the first stage, I also have to allocate the memory
                if self.memory:
                    # I perform the fetch from the local memory
                    memName = self.memory[0]
                else:
                    for name, isFetch  in self.tlmPorts.items():
                        if isFetch:
                            memName = name
                curPipeInit = [self.fetchReg[0], 'Processor::INSTRUCTIONS', memName] + curPipeInit
                curPipeInit = ['numInstructions'] + curPipeInit
                if self.instructionCache:
                    curPipeInit = ['Processor::instrCache'] + curPipeInit
            if pipeStage.checkTools:
                curPipeInit = [self.fetchReg[0], 'toolManager'] + curPipeInit
            initString += ')'
            initElements.append(pipeStage.name + '_stage(' + ', '.join(curPipeInit)  + ')')
            prevStage = pipeStage.name + '_stage'
        NOPIntructionType = cxx_writer.writer_code.Type('NOPInstruction', 'instructions.hpp')
        NOPinstructionsAttribute = cxx_writer.writer_code.Attribute('NOPInstrInstance', NOPIntructionType.makePointer(), 'pu', True)
        processorElements.append(NOPinstructionsAttribute)

    # Ok, here I have to create the code for the constructor: I have to
    # initialize the INSTRUCTIONS array, the local memory (if present)
    # the TLM ports
    global baseInstrInitElement
    baseInstrInitElement = ''
    if model.startswith('acc'):
        for pipeStage in self.pipes:
            for reg in self.regs:
                baseInstrInitElement += reg.name + '_' + pipeStage.name + ', '
            for regB in self.regBanks:
                baseInstrInitElement += regB.name + '_' + pipeStage.name + ', '
            for alias in self.aliasRegs:
                baseInstrInitElement += alias.name + '_' + pipeStage.name + ', '
            for aliasB in self.aliasRegBanks:
                baseInstrInitElement += aliasB.name + '_' + pipeStage.name + ', '
    else:
        for reg in self.regs:
            baseInstrInitElement += reg.name + ', '
        for regB in self.regBanks:
            baseInstrInitElement += regB.name + ', '
        for alias in self.aliasRegs:
            baseInstrInitElement += alias.name + ', '
        for aliasB in self.aliasRegBanks:
            baseInstrInitElement += aliasB.name + ', '
    if self.memory:
        baseInstrInitElement += self.memory[0] + ', '
    for tlmPorts in self.tlmPorts.keys():
        baseInstrInitElement += tlmPorts + ', '
    baseInstrInitElement = baseInstrInitElement[:-2]

    constrCode = 'Processor::numInstances++;\nif(Processor::INSTRUCTIONS == NULL){\n'
    constrCode += '// Initialization of the array holding the initial instance of the instructions\n'
    maxInstrId = max([instr.id for instr in self.isa.instructions.values()]) + 1
    constrCode += 'Processor::INSTRUCTIONS = new Instruction *[' + str(maxInstrId + 1) + '];\n'
    for name, instr in self.isa.instructions.items():
        constrCode += 'Processor::INSTRUCTIONS[' + str(instr.id) + '] = new ' + name + '(' + baseInstrInitElement +');\n'
    constrCode += 'Processor::INSTRUCTIONS[' + str(maxInstrId) + '] = new InvalidInstr(' + baseInstrInitElement + ');\n'
    if model.startswith('acc'):
        constrCode += 'Processor::NOPInstrInstance = new NOPInstruction(' + baseInstrInitElement + ');\n'
        for pipeStage in self.pipes:
            constrCode += pipeStage.name + '_stage.NOPInstrInstance = Processor::NOPInstrInstance;\n'
    constrCode += '}\n'
    constrCode += bodyInits
    if not model.startswith('acc'):
        if self.externalClock:
            constrCode += 'SC_METHOD(mainLoop);\nsensitive << this->clock.pos();\ndont_initialize();\n'
        else:
            constrCode += 'SC_THREAD(mainLoop);\n'
    if not self.systemc and not model.startswith('acc'):
        constrCode += 'this->totalCycles = 0;\n'
    constrCode += 'end_module();'
    constructorBody = cxx_writer.writer_code.Code(constrCode)
    constructorParams = [cxx_writer.writer_code.Parameter('name', cxx_writer.writer_code.sc_module_nameType)]
    constructorInit = ['sc_module(name)']
    if (self.systemc or model.startswith('acc') or len(self.tlmPorts) > 0) and not self.externalClock:
        constructorParams.append(cxx_writer.writer_code.Parameter('latency', cxx_writer.writer_code.sc_timeType))
        constructorInit.append('latency(latency)')
    publicConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, constructorInit + initElements)
    destrCode = """Processor::numInstances--;
    if(Processor::numInstances == 0){
        for(int i = 0; i < """ + str(maxInstrId + 1) + """; i++){
            delete Processor::INSTRUCTIONS[i];
        }
        delete [] Processor::INSTRUCTIONS;
    """
    if self.instructionCache:
        destrCode += """Processor::INSTRUCTIONS = NULL;
        template_map< """ + str(fetchWordType) + """, Instruction * >::const_iterator cacheIter, cacheEnd;
        for(cacheIter = Processor::instrCache.begin(), cacheEnd = Processor::instrCache.end(); cacheIter != cacheEnd; cacheIter++){
            delete cacheIter->second;
        }
        """
    destrCode += """
        delete this->abiIf;
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
    from isa import resolveBitType
    wordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize) + '>')
    includes = wordType.getIncludes()

    ifClassElements = []
    initElements = []
    baseInstrConstrParams = []
    # Lets first of all decalre the variables
    progLimitAttr = cxx_writer.writer_code.Attribute('PROGRAM_LIMIT', wordType.makeRef(), 'pri')
    ifClassElements.append(progLimitAttr)
    baseInstrConstrParams.append(cxx_writer.writer_code.Parameter('PROGRAM_LIMIT', wordType.makeRef()))
    initElements.append('PROGRAM_LIMIT(PROGRAM_LIMIT)')
    memIfType = cxx_writer.writer_code.Type('MemoryInterface', 'memory.hpp')
    for memName in self.abi.memories.keys():
        ifClassElements.append(cxx_writer.writer_code.Attribute(memName, memIfType.makeRef(), 'pri'))
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(memName, memIfType.makeRef()))
        initElements.append(memName + '(' + memName + ')')
    for reg in self.regs:
        attribute = cxx_writer.writer_code.Attribute(reg.name, resourceType[reg.name].makeRef(), 'pri')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(reg.name, resourceType[reg.name].makeRef()))
        initElements.append(reg.name + '(' + reg.name + ')')
        ifClassElements.append(attribute)
    for regB in self.regBanks:
        attribute = cxx_writer.writer_code.Attribute(regB.name, resourceType[regB.name].makeRef(), 'pri')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(regB.name, resourceType[regB.name].makeRef()))
        initElements.append(regB.name + '(' + regB.name + ')')
        ifClassElements.append(attribute)
    for alias in self.aliasRegs:
        attribute = cxx_writer.writer_code.Attribute(alias.name, resourceType[alias.name].makeRef(), 'pri')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(alias.name, resourceType[alias.name].makeRef()))
        initElements.append(alias.name + '(' + alias.name + ')')
        ifClassElements.append(attribute)
    for aliasB in self.aliasRegBanks:
        attribute = cxx_writer.writer_code.Attribute(aliasB.name, resourceType[aliasB.name].makePointer().makeRef(), 'pri')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(aliasB.name, resourceType[aliasB.name].makePointer().makeRef()))
        initElements.append(aliasB.name + '(' + aliasB.name + ')')
        ifClassElements.append(attribute)
    # Now lets declare the methods used to access the variables
    if self.isBigEndian:
        endianessCode = cxx_writer.writer_code.Code('return false;')
    else:
        endianessCode = cxx_writer.writer_code.Code('return true;')
    endianessCode.addInclude(includes)
    endianessMethod = cxx_writer.writer_code.Method('isLittleEndian', endianessCode, cxx_writer.writer_code.boolType, 'pu', noException = True, const = True)
    ifClassElements.append(endianessMethod)

    if self.abi.preCallCode:
        ifClassElements.append(cxx_writer.writer_code.Method('preCall', cxx_writer.writer_code.Code(self.abi.preCallCode), cxx_writer.writer_code.voidType, 'pu', noException = True))
    if self.abi.postCallCode:
        ifClassElements.append(cxx_writer.writer_code.Method('postCall', cxx_writer.writer_code.Code(self.abi.preCallCode), cxx_writer.writer_code.voidType, 'pu', noException = True))
    if self.abi.returnCallReg:
        returnCallCode = ''
        for returnReg in self.abi.returnCallReg:
            returnCallCode += returnReg[0] + '.immediateWrite(' + returnReg[1] + ' + ' + str(returnReg[2]) + ');\n'
        ifClassElements.append(cxx_writer.writer_code.Method('returnFromCall', cxx_writer.writer_code.Code(returnCallCode), cxx_writer.writer_code.voidType, 'pu', noException = True))

    codeLimitCode = cxx_writer.writer_code.Code('return this->PROGRAM_LIMIT;')
    codeLimitMethod = cxx_writer.writer_code.Method('getCodeLimit', codeLimitCode, wordType, 'pu')
    ifClassElements.append(codeLimitMethod)
    for elem in [self.abi.LR, self.abi.PC, self.abi.SP, self.abi.FP, self.abi.retVal]:
        if not elem:
            continue
        readElemBody = 'return this->' + elem
        if self.abi.offset.has_key(elem):
            readElemBody += ' + ' + str(self.abi.offset[elem])
        readElemBody += ';'
        readElemCode = cxx_writer.writer_code.Code(readElemBody)
        readElemCode.addInclude(includes)
        readElemMethod = cxx_writer.writer_code.Method('read' + self.abi.name[elem], readElemCode, wordType, 'pu', noException = True, const = True)
        ifClassElements.append(readElemMethod)
        setElemBody = 'this->' + elem + '.immediateWrite(newValue);'
        setElemCode = cxx_writer.writer_code.Code(setElemBody)
        setElemCode.addInclude(includes)
        setElemParam = cxx_writer.writer_code.Parameter('newValue', wordType.makeRef().makeConst())
        setElemMethod = cxx_writer.writer_code.Method('set' + self.abi.name[elem], setElemCode, cxx_writer.writer_code.voidType, 'pu', [setElemParam], noException = True)
        ifClassElements.append(setElemMethod)
    vectorType = cxx_writer.writer_code.TemplateType('std::vector', [wordType], 'vector')
    readArgsBody = str(vectorType) + ' args;\n'
    for arg in self.abi.args:
        readArgsBody += 'args.push_back(this->' + arg
        if self.abi.offset.has_key(arg) and not model.startswith('acc'):
            readArgsBody += ' + ' + str(self.abi.offset[arg])
        readArgsBody += ');\n'
    readArgsBody += 'return args;\n'
    readArgsCode = cxx_writer.writer_code.Code(readArgsBody)
    readArgsCode.addInclude(includes)
    readArgsMethod = cxx_writer.writer_code.Method('readArgs', readArgsCode, vectorType, 'pu', noException = True, const = True)
    ifClassElements.append(readArgsMethod)
    setArgsBody = 'if(args.size() > ' + str(len(self.abi.args)) + '){\nTHROW_EXCEPTION(\"ABI of processor supports up to ' + str(len(self.abi.args)) + ' arguments: \" << args.size() << \" given\");\n}\n'
    setArgsBody += str(vectorType) + '::const_iterator argIter = args.begin();\n'
    for arg in self.abi.args:
        setArgsBody += 'this->' + arg + '.immediateWrite(*argIter'
        if self.abi.offset.has_key(arg) and not model.startswith('acc'):
            setArgsBody += ' - ' + str(self.abi.offset[arg])
        setArgsBody += ');\nargIter++;\n'
    setArgsCode = cxx_writer.writer_code.Code(setArgsBody)
    setArgsParam = cxx_writer.writer_code.Parameter('args', vectorType.makeRef().makeConst())
    setArgsMethod = cxx_writer.writer_code.Method('setArgs', setArgsCode, cxx_writer.writer_code.voidType, 'pu', [setArgsParam], noException = True)
    ifClassElements.append(setArgsMethod)
    maxGDBId = 0
    readGDBRegBody = 'switch(gdbId){\n'
    for reg, gdbId in self.abi.regCorrespondence.items():
        if gdbId > maxGDBId:
            maxGDBId = gdbId
        readGDBRegBody += 'case ' + str(gdbId) + ':{\n'
        readGDBRegBody += 'return ' + reg
        if self.abi.offset.has_key(reg) and not model.startswith('acc'):
            readGDBRegBody += ' + ' + str(self.abi.offset[reg])
        readGDBRegBody += ';\nbreak;}\n'
    readGDBRegBody += 'default:{\nTHROW_EXCEPTION(\"No register corresponding to GDB id \" << gdbId);\nreturn 0;\n}\n}\n'
    readGDBRegCode = cxx_writer.writer_code.Code(readGDBRegBody)
    readGDBRegCode.addInclude(includes)
    readGDBRegParam = cxx_writer.writer_code.Parameter('gdbId', cxx_writer.writer_code.uintType.makeRef().makeConst())
    readGDBRegMethod = cxx_writer.writer_code.Method('readGDBReg', readGDBRegCode, wordType, 'pu', [readGDBRegParam], noException = True, const = True)
    ifClassElements.append(readGDBRegMethod)
    nGDBRegsCode = cxx_writer.writer_code.Code('return ' + str(maxGDBId) + ';')
    nGDBRegsMethod = cxx_writer.writer_code.Method('nGDBRegs', nGDBRegsCode, cxx_writer.writer_code.uintType, 'pu', noException = True, const = True)
    ifClassElements.append(nGDBRegsMethod)
    setGDBRegBody = 'switch(gdbId){\n'
    for reg, gdbId in self.abi.regCorrespondence.items():
        setGDBRegBody += 'case ' + str(gdbId) + ':{\n'
        setGDBRegBody += reg + '.immediateWrite(newValue'
        setGDBRegBody += ');\nbreak;}\n'
    setGDBRegBody += 'default:{\nTHROW_EXCEPTION(\"No register corresponding to GDB id \" << gdbId);\n}\n}\n'
    setGDBRegCode = cxx_writer.writer_code.Code(setGDBRegBody)
    setGDBRegCode.addInclude(includes)
    setGDBRegParam1 = cxx_writer.writer_code.Parameter('newValue', wordType.makeRef().makeConst())
    setGDBRegParam2 = cxx_writer.writer_code.Parameter('gdbId', cxx_writer.writer_code.uintType.makeRef().makeConst())
    setGDBRegMethod = cxx_writer.writer_code.Method('setGDBReg', setGDBRegCode, cxx_writer.writer_code.voidType, 'pu', [setGDBRegParam1, setGDBRegParam2], noException = True)
    ifClassElements.append(setGDBRegMethod)
    readMemBody = ''
    if not self.abi.memories:
        readMemBody += 'THROW_EXCEPTION(\"No memory accessible from the ABI or processor ' + self.name + '\");'
    else:
        if len(self.abi.memories) == 1:
            readMemBody += 'return this->' + self.abi.memories.keys()[0] + '.read_word_dbg(address);'
        else:
            for memName, range in self.abi.memories.items():
                readMemBody += 'if(address >= ' + hex(range[0]) + ' && address <= ' + hex(range[1]) + '){\n'
                readMemBody += 'return this->' + self.abi.memories.keys()[0] + '.read_word_dbg(address);\n}\nelse '
            readMemBody += '{\nTHROW_EXCEPTION(\"Address \" << std::hex << address << \" out of range\");\n}'
    readMemCode = cxx_writer.writer_code.Code(readMemBody)
    readMemParam1 = cxx_writer.writer_code.Parameter('address', wordType.makeRef().makeConst())
    readMemParam2 = cxx_writer.writer_code.Parameter('length', cxx_writer.writer_code.intType, initValue = 'sizeof(' + str(wordType) + ')')
    readMemMethod = cxx_writer.writer_code.Method('readMem', readMemCode, wordType, 'pu', [readMemParam1, readMemParam2])
    ifClassElements.append(readMemMethod)
    readByteMemBody = ''
    if not self.abi.memories:
        readByteMemBody += 'THROW_EXCEPTION(\"No memory accessible from the ABI or processor ' + self.name + '\");'
    else:
        if len(self.abi.memories) == 1:
            readByteMemBody += 'return this->' + self.abi.memories.keys()[0] + '.read_byte_dbg(address);'
        else:
            for memName, range in self.abi.memories.items():
                readByteMemBody += 'if(address >= ' + hex(range[0]) + ' && address <= ' + hex(range[1]) + '){\n'
                readByteMemBody += 'return this->' + self.abi.memories.keys()[0] + '.read_byte_dbg(address);\n}\nelse '
            readByteMemBody += '{\nTHROW_EXCEPTION(\"Address \" << std::hex << address << \" out of range\");\n}'
    readByteMemCode = cxx_writer.writer_code.Code(readByteMemBody)
    readByteMemParam = cxx_writer.writer_code.Parameter('address', wordType.makeRef().makeConst())
    readByteMemMethod = cxx_writer.writer_code.Method('readCharMem', readByteMemCode, cxx_writer.writer_code.ucharType, 'pu', [readByteMemParam])
    ifClassElements.append(readByteMemMethod)

    writeMemBody = ''
    if not self.abi.memories:
        writeMemBody += 'THROW_EXCEPTION(\"No memory accessible from the ABI or processor ' + self.name + '\");'
    else:
        if len(self.abi.memories) == 1:
            writeMemBody += 'this->' + self.abi.memories.keys()[0] + '.write_word_dbg(address, datum);'
        else:
            for memName, range in self.abi.memories.items():
                writeMemBody += 'if(address >= ' + hex(range[0]) + ' && address <= ' + hex(range[1]) + '){\n'
                writeMemBody += 'this->' + self.abi.memories.keys()[0] + '.write_word_dbg(address, datum);\n}\nelse '
            writeMemBody += '{\nTHROW_EXCEPTION(\"Address \" << std::hex << address << \" out of range\");\n}'
    writeMemCode = cxx_writer.writer_code.Code(writeMemBody)
    writeMemCode.addInclude('utils.hpp')
    writeMemParam1 = cxx_writer.writer_code.Parameter('address', wordType.makeRef().makeConst())
    writeMemParam2 = cxx_writer.writer_code.Parameter('datum', wordType)
    writeMemParam3 = cxx_writer.writer_code.Parameter('length', cxx_writer.writer_code.intType, initValue = 'sizeof(' + str(wordType) + ')')
    writeMemMethod = cxx_writer.writer_code.Method('writeMem', writeMemCode, cxx_writer.writer_code.voidType, 'pu', [writeMemParam1, writeMemParam2, writeMemParam3])
    ifClassElements.append(writeMemMethod)
    writeMemBody = ''
    if not self.abi.memories:
        writeMemBody += 'THROW_EXCEPTION(\"No memory accessible from the ABI or processor ' + self.name + '\");'
    else:
        if len(self.abi.memories) == 1:
            writeMemBody += 'this->' + self.abi.memories.keys()[0] + '.write_byte_dbg(address, datum);'
        else:
            for memName, range in self.abi.memories.items():
                writeMemBody += 'if(address >= ' + hex(range[0]) + ' && address <= ' + hex(range[1]) + '){\n'
                writeMemBody += 'this->' + self.abi.memories.keys()[0] + '.write_byte_dbg(address, datum);\n}\nelse '
            writeMemBody += '{\nTHROW_EXCEPTION(\"Address \" << std::hex << address << \" out of range\");\n}'
    writeMemCode = cxx_writer.writer_code.Code(writeMemBody)
    writeMemParam1 = cxx_writer.writer_code.Parameter('address', wordType.makeRef().makeConst())
    writeMemParam2 = cxx_writer.writer_code.Parameter('datum', cxx_writer.writer_code.ucharType)
    writeMemMethod = cxx_writer.writer_code.Method('writeCharMem', writeMemCode, cxx_writer.writer_code.voidType, 'pu', [writeMemParam1, writeMemParam2])
    ifClassElements.append(writeMemMethod)

    ABIIfType = cxx_writer.writer_code.TemplateType('ABIIf', [wordType], 'ABIIf.hpp')
    ifClassDecl = cxx_writer.writer_code.ClassDeclaration(self.name + '_ABIIf', ifClassElements, [ABIIfType])
    publicIfConstr = cxx_writer.writer_code.Constructor(cxx_writer.writer_code.Code(''), 'pu', baseInstrConstrParams, initElements)
    emptyBody = cxx_writer.writer_code.Code('')
    opDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    ifClassDecl.addDestructor(opDestr)
    ifClassDecl.addConstructor(publicIfConstr)
    return ifClassDecl

def getCPPExternalPorts(self, model):
    if len(self.tlmPorts) == 0:
        return None
    # creates the processor external ports used for the
    # communication with the external world (the memory port
    # is not among this ports, it is treated separately)
    from isa import resolveBitType
    archDWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize*2) + '>')
    archWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize) + '>')
    archHWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize/2) + '>')
    archByteType = resolveBitType('BIT<' + str(self.byteSize) + '>')

    memIfType = cxx_writer.writer_code.Type('MemoryInterface', 'memory.hpp')
    tlm_dmiType = cxx_writer.writer_code.Type('tlm::tlm_dmi', 'tlm.h')
    TLMMemoryType = cxx_writer.writer_code.Type('TLMMemory')
    tlminitsocketType = cxx_writer.writer_code.TemplateType('tlm_utils::simple_initiator_socket', [TLMMemoryType, self.wordSize], 'tlm_utils/simple_initiator_socket.h')
    payloadType = cxx_writer.writer_code.Type('tlm::tlm_generic_payload', 'tlm.h')
    phaseType = cxx_writer.writer_code.Type('tlm::tlm_phase', 'tlm.h')
    sync_enumType = cxx_writer.writer_code.Type('tlm::tlm_sync_enum', 'tlm.h')
    tlmPortInit = []
    constructorParams = []

    readMemAliasCode = ''
    writeMemAliasCode = ''
    aliasAttrs = []
    aliasParams = []
    aliasInit = []
    for alias in self.memAlias:
        aliasAttrs.append(cxx_writer.writer_code.Attribute(alias.alias, resourceType[alias.alias].makeRef(), 'pri'))
        aliasParams.append(cxx_writer.writer_code.Parameter(alias.alias, resourceType[alias.alias].makeRef()))
        aliasInit.append(alias.alias + '(' + alias.alias + ')')
        readMemAliasCode += 'if(address == ' + hex(long(alias.address)) + '){\nreturn this->' + alias.alias + ';\n}\n'
        writeMemAliasCode += 'if(address == ' + hex(long(alias.address)) + '){\n this->' + alias.alias + ' = datum;\nreturn;\n}\n'

    tlmPortElements = []
    emptyBody = cxx_writer.writer_code.Code('')

    for curType in [archDWordType, archWordType, archHWordType]:
        swapEndianessCode = str(archByteType) + """ helperByte = 0;
        for(int i = 0; i < sizeof(""" + str(curType) + """)/2; i++){
            helperByte = ((""" + str(archByteType) + """ *)datum)[i];
            ((""" + str(archByteType) + """ *)datum)[i] = ((""" + str(archByteType) + """ *)datum)[sizeof(""" + str(curType) + """) -1 -i];
            ((""" + str(archByteType) + """ *)datum)[sizeof(""" + str(curType) + """) -1 -i] = helperByte;
        }
        """
        swapEndianessBody = cxx_writer.writer_code.Code(swapEndianessCode)
        datumParam = cxx_writer.writer_code.Parameter('datum', curType.makeRef())
        swapEndianessDecl = cxx_writer.writer_code.Method('swapEndianess', swapEndianessBody, cxx_writer.writer_code.voidType, 'pu', [datumParam], inline = True, noException = True)
        tlmPortElements.append(swapEndianessDecl)

    if model.endswith('AT'):
        # Some helper methods used only in the Approximate Timed coding style
        helperCode = """// TLM-2 backward non-blocking transport method
            // The timing annotation must be honored
            m_peq.notify(trans, phase, delay);
            return tlm::TLM_ACCEPTED;
            """
        helperBody = cxx_writer.writer_code.Code(helperCode)
        transParam = cxx_writer.writer_code.Parameter('trans', payloadType.makeRef())
        phaseParam = cxx_writer.writer_code.Parameter('phase', phaseType.makeRef())
        delayParam = cxx_writer.writer_code.Parameter('delay', cxx_writer.writer_code.sc_timeType.makeRef())
        helperDecl = cxx_writer.writer_code.Method('nb_transport_bw', helperBody, sync_enumType, 'pu', [transParam, phaseParam, delayParam], inline = True, noException = True)
        tlmPortElements.append(helperDecl)

        helperCode = """// Payload event queue callback to handle transactions from target
            // Transaction could have arrived through return path or backward path
            if (phase == tlm::END_REQ || (&trans == request_in_progress && phase == tlm::BEGIN_RESP)){
                // The end of the BEGIN_REQ phase
                request_in_progress = NULL;
                end_request_event.notify();
            }
            else if (phase == tlm::BEGIN_REQ || phase == tlm::END_RESP){
                SC_REPORT_FATAL("TLM-2", "Illegal transaction phase received by initiator");
            }

            if (phase == tlm::BEGIN_RESP){
                if (trans.is_response_error()){
                    SC_REPORT_ERROR("TLM-2", ("Transaction returned with error, response status = " + trans.get_response_string()).c_str());
                }

                // Send final phase transition to target
                tlm::tlm_phase fw_phase = tlm::END_RESP;
                sc_time delay = SC_ZERO_TIME;
                initSocket->nb_transport_fw(trans, fw_phase, delay);
                if (trans.is_response_error()){
                    SC_REPORT_ERROR("TLM-2", ("Transaction returned with error, response status = " + \
                        trans.get_response_string()).c_str());
                }
                this->end_response_event.notify(delay);
            }
            """
        helperBody = cxx_writer.writer_code.Code(helperCode)
        phaseParam = cxx_writer.writer_code.Parameter('phase', phaseType.makeRef().makeConst())
        helperDecl = cxx_writer.writer_code.Method('peq_cb', helperBody, cxx_writer.writer_code.voidType, 'pu', [transParam, phaseParam])
        tlmPortElements.append(helperDecl)

        tlmPortElements.append(cxx_writer.writer_code.Attribute('request_in_progress', payloadType.makePointer(), 'pri'))
        tlmPortElements.append(cxx_writer.writer_code.Attribute('end_request_event', cxx_writer.writer_code.sc_eventType, 'pri'))
        tlmPortElements.append(cxx_writer.writer_code.Attribute('end_response_event', cxx_writer.writer_code.sc_eventType, 'pri'))

    if model.endswith('LT'):
        readCode = """ data = 0;
            if (this->dmi_ptr_valid){
                memcpy(&data, this->dmi_data.get_dmi_ptr() - this->dmi_data.get_start_address() + address, sizeof(data));
                this->quantKeeper.inc(this->dmi_data.get_read_latency());
            }
            else{
                sc_time delay = this->quantKeeper.get_local_time();
                tlm::tlm_generic_payload trans;
                trans.set_address(address);
                trans.set_read();
                trans.set_data_ptr(reinterpret_cast<unsigned char*>(&data));
                trans.set_data_length(sizeof(data));
                trans.set_byte_enable_ptr(0);
                trans.set_dmi_allowed(false);
                trans.set_response_status( tlm::TLM_INCOMPLETE_RESPONSE );
                this->initSocket->b_transport(trans, delay);

                if(trans.is_response_error()){
                    std::string errorStr("Error from b_transport, response status = " + trans.get_response_string());
                    SC_REPORT_ERROR("TLM-2", errorStr.c_str());
                }
                if(trans.is_dmi_allowed()){
                    this->dmi_data.init();
                    this->dmi_ptr_valid = this->initSocket->get_direct_mem_ptr(trans, this->dmi_data);
                }
                //Now lets keep track of time
                this->quantKeeper.set(delay);
            }
            //Now the code for endianess conversion: the processor is always modeled
            //with the host endianess; in case they are different, the endianess
            //is turned
            """
    else:
        readCode = """ data = 0;
        tlm::tlm_generic_payload trans;
        trans.set_address(address);
        trans.set_read();
        trans.set_data_ptr(reinterpret_cast<unsigned char*>(&data));
        trans.set_data_length(sizeof(data));
        trans.set_byte_enable_ptr(0);
        trans.set_dmi_allowed(false);
        trans.set_response_status(tlm::TLM_INCOMPLETE_RESPONSE);

        if(this->request_in_progress != NULL){
            wait(this->end_request_event);
        }
        request_in_progress = &trans;

        // Non-blocking transport call on the forward path
        sc_time delay = SC_ZERO_TIME;
        tlm::tlm_phase phase = tlm::BEGIN_REQ;
        tlm::tlm_sync_enum status;
        status = initSocket->nb_transport_fw(trans, phase, delay);

        if(trans.is_response_error()){
            std::string errorStr("Error from nb_transport_fw, response status = " + trans.get_response_string());
            SC_REPORT_ERROR("TLM-2", errorStr.c_str());
        }

        // Check value returned from nb_transport_fw
        if(status == tlm::TLM_UPDATED){
            // The timing annotation must be honored
            m_peq.notify(trans, phase, delay);
            wait(this->end_response_event);
        }
        else if(status == tlm::TLM_COMPLETED){
            // The completion of the transaction necessarily ends the BEGIN_REQ phase
            this->request_in_progress = NULL;
            // The target has terminated the transaction, I check the correctness
            if(trans.is_response_error()){
                SC_REPORT_ERROR("TLM-2", ("Transaction returned with error, response status = " + trans.get_response_string()).c_str());
            }
        }
        wait(this->end_response_event);
        """
    if self.isBigEndian:
        readCode += '#ifdef LITTLE_ENDIAN_BO\n'
    else:
        readCode += '#ifdef BIG_ENDIAN_BO\n'
    readCode += """swapEndianess(data);
        #endif
        return data;
        """
    addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + str(archDWordType) + readCode)
    readBody.addInclude('utils.hpp')
    readBody.addInclude('tlm.h')
    readDecl = cxx_writer.writer_code.Method('read_dword', readBody, archDWordType, 'pu', [addressParam], inline = True, noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + str(archWordType) + readCode)
    readDecl = cxx_writer.writer_code.Method('read_word', readBody, archWordType, 'pu', [addressParam], inline = True, noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + str(archHWordType) + readCode)
    readDecl = cxx_writer.writer_code.Method('read_half', readBody, archHWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + str(archByteType) + readCode)
    readDecl = cxx_writer.writer_code.Method('read_byte', readBody, archByteType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    if self.isBigEndian:
        writeCode = '#ifdef LITTLE_ENDIAN_BO\n'
    else:
        writeCode = '#ifdef BIG_ENDIAN_BO\n'
    writeCode += """swapEndianess(datum);
        #endif
        """
    if model.endswith('LT'):
        writeCode += """if(this->dmi_ptr_valid){
                memcpy(this->dmi_data.get_dmi_ptr() - this->dmi_data.get_start_address() + address, &datum, sizeof(datum));
                this->quantKeeper.inc(this->dmi_data.get_write_latency());
            }
            else{
                sc_time delay = this->quantKeeper.get_local_time();
                tlm::tlm_generic_payload trans;
                trans.set_address(address);
                trans.set_write();
                trans.set_data_ptr((unsigned char*)&datum);
                trans.set_data_length(sizeof(datum));
                trans.set_byte_enable_ptr(0);
                trans.set_dmi_allowed(false);
                trans.set_response_status(tlm::TLM_INCOMPLETE_RESPONSE);
                this->initSocket->b_transport(trans, delay);

                if(trans.is_response_error()){
                    std::string errorStr("Error from b_transport, response status = " + trans.get_response_string());
                    SC_REPORT_ERROR("TLM-2", errorStr.c_str());
                }
                if(trans.is_dmi_allowed()){
                    this->dmi_data.init();
                    this->dmi_ptr_valid = this->initSocket->get_direct_mem_ptr(trans, this->dmi_data);
                }
                //Now lets keep track of time
                this->quantKeeper.set(delay);
            }
        """
    else:
        writeCode += """tlm::tlm_generic_payload trans;
        trans.set_address(address);
        trans.set_write();
        trans.set_data_ptr((unsigned char*)&datum);
        trans.set_data_length(sizeof(datum));
        trans.set_byte_enable_ptr(0);
        trans.set_dmi_allowed(false);
        trans.set_response_status(tlm::TLM_INCOMPLETE_RESPONSE);

        if(this->request_in_progress != NULL){
            wait(this->end_request_event);
        }
        request_in_progress = &trans;

        // Non-blocking transport call on the forward path
        sc_time delay = SC_ZERO_TIME;
        tlm::tlm_phase phase = tlm::BEGIN_REQ;
        tlm::tlm_sync_enum status;
        status = initSocket->nb_transport_fw(trans, phase, delay);

        if(trans.is_response_error()){
            std::string errorStr("Error from nb_transport_fw, response status = " + trans.get_response_string());
            SC_REPORT_ERROR("TLM-2", errorStr.c_str());
        }

        // Check value returned from nb_transport_fw
        if(status == tlm::TLM_UPDATED){
            // The timing annotation must be honored
            m_peq.notify(trans, phase, delay);
            wait(this->end_response_event);
        }
        else if(status == tlm::TLM_COMPLETED){
            // The completion of the transaction necessarily ends the BEGIN_REQ phase
            this->request_in_progress = NULL;
            // The target has terminated the transaction, I check the correctness
            if(trans.is_response_error()){
                SC_REPORT_ERROR("TLM-2", ("Transaction returned with error, response status = " + trans.get_response_string()).c_str());
            }
        }
        wait(this->end_response_event);
        """
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + writeCode)
    datumParam = cxx_writer.writer_code.Parameter('datum', archDWordType)
    writeDecl = cxx_writer.writer_code.Method('write_dword', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], inline = True, noException = True)
    tlmPortElements.append(writeDecl)
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + writeCode)
    datumParam = cxx_writer.writer_code.Parameter('datum', archWordType)
    writeDecl = cxx_writer.writer_code.Method('write_word', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], inline = True, noException = True)
    tlmPortElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType)
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + writeCode)
    writeDecl = cxx_writer.writer_code.Method('write_half', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archByteType)
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + writeCode)
    writeDecl = cxx_writer.writer_code.Method('write_byte', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)

    readCode1 = """tlm::tlm_generic_payload trans;
        trans.set_address(address);
        trans.set_read();
        """
    readCode2 = """trans.set_data_ptr(reinterpret_cast<unsigned char *>(&data));
        this->initSocket->transport_dbg(trans);
        //Now the code for endianess conversion: the processor is always modeled
        //with the host endianess; in case they are different, the endianess
        //is turned
        """
    if self.isBigEndian:
        readCode2 += '#ifdef LITTLE_ENDIAN_BO\n'
    else:
        readCode2 += '#ifdef BIG_ENDIAN_BO\n'
    readCode2 += """swapEndianess(datum);
    #endif
    return data;
    """
    addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + readCode1 + 'trans.set_data_length(' + str(self.wordSize*2) + ');\n' + str(archDWordType) + ' data = 0;\n' + readCode2)
    readBody.addInclude('utils.hpp')
    readBody.addInclude('tlm.h')
    readDecl = cxx_writer.writer_code.Method('read_dword_dbg', readBody, archDWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + readCode1 + 'trans.set_data_length(' + str(self.wordSize) + ');\n' + str(archWordType) + ' data = 0;\n' + readCode2)
    readDecl = cxx_writer.writer_code.Method('read_word_dbg', readBody, archWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + readCode1 + 'trans.set_data_length(' + str(self.wordSize/2) + ');\n' + str(archHWordType) + ' data = 0;\n' + readCode2)
    readDecl = cxx_writer.writer_code.Method('read_half_dbg', readBody, archHWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + readCode1 + 'trans.set_data_length(1);\n' + str(archByteType) + ' data = 0;\n' + readCode2)
    readDecl = cxx_writer.writer_code.Method('read_byte_dbg', readBody, archByteType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    if self.isBigEndian:
        writeCode1 = '#ifdef LITTLE_ENDIAN_BO\n'
    else:
        writeCode1 = '#ifdef BIG_ENDIAN_BO\n'
    writeCode1 += """swapEndianess(datum);
        #endif
        """
    writeCode1 += """tlm::tlm_generic_payload trans;
        trans.set_address(address);
        trans.set_write();
        """
    writeCode2 = """trans.set_data_ptr((unsigned char *)&datum);
        this->initSocket->transport_dbg(trans);
        """
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + writeCode1 + 'trans.set_data_length(' + str(self.wordSize*2) + ');\n' + writeCode2)
    datumParam = cxx_writer.writer_code.Parameter('datum', archDWordType)
    writeDecl = cxx_writer.writer_code.Method('write_dword_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + writeCode1 + 'trans.set_data_length(' + str(self.wordSize) + ');\n' + writeCode2)
    datumParam = cxx_writer.writer_code.Parameter('datum', archWordType)
    writeDecl = cxx_writer.writer_code.Method('write_word_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType)
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + writeCode1 + 'trans.set_data_length(' + str(self.wordSize/2) + ');\n' + writeCode2)
    writeDecl = cxx_writer.writer_code.Method('write_half_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archByteType)
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + writeCode1 + 'trans.set_data_length(1);\n' + writeCode2)
    writeDecl = cxx_writer.writer_code.Method('write_byte_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)

    lockDecl = cxx_writer.writer_code.Method('lock', emptyBody, cxx_writer.writer_code.voidType, 'pu')
    tlmPortElements.append(lockDecl)
    unlockDecl = cxx_writer.writer_code.Method('unlock', emptyBody, cxx_writer.writer_code.voidType, 'pu')
    tlmPortElements.append(unlockDecl)

    constructorParams.append(cxx_writer.writer_code.Parameter('portName', cxx_writer.writer_code.sc_module_nameType))
    tlmPortInit.append('sc_module(portName)')
    initSockAttr = cxx_writer.writer_code.Attribute('initSocket', tlminitsocketType, 'pu')
    tlmPortElements.append(initSockAttr)
    constructorCode = ''
    if model.endswith('LT'):
        quantumKeeperType = cxx_writer.writer_code.Type('tlm_utils::tlm_quantumkeeper', 'tlm_utils/tlm_quantumkeeper.h')
        quantumKeeperAttribute = cxx_writer.writer_code.Attribute('quantKeeper', quantumKeeperType.makeRef(), 'pri')
        tlmPortElements.append(quantumKeeperAttribute)
        tlmPortInit.append('quantKeeper(quantKeeper)')
        constructorParams.append(cxx_writer.writer_code.Parameter('quantKeeper', quantumKeeperType.makeRef()))
        dmi_ptr_validAttribute = cxx_writer.writer_code.Attribute('dmi_ptr_valid', cxx_writer.writer_code.boolType, 'pri')
        tlmPortElements.append(dmi_ptr_validAttribute)
        dmi_dataAttribute = cxx_writer.writer_code.Attribute('dmi_data', tlm_dmiType, 'pri')
        tlmPortElements.append(dmi_dataAttribute)
        constructorCode += 'this->dmi_ptr_valid = false;\n'
    else:
        peqType = cxx_writer.writer_code.TemplateType('tlm_utils::peq_with_cb_and_phase', [TLMMemoryType], 'tlm_utils/peq_with_cb_and_phase.h')
        tlmPortElements.append(cxx_writer.writer_code.Attribute('m_peq', peqType, 'pri'))
        tlmPortInit.append('m_peq(this, &TLMMemory::peq_cb)')
        tlmPortInit.append('request_in_progress(NULL)')
        constructorCode += """// Register callbacks for incoming interface method calls
            this->initSocket.register_nb_transport_bw(this, &TLMMemory::nb_transport_bw);
            """

    tlmPortElements += aliasAttrs

    extPortDecl = cxx_writer.writer_code.ClassDeclaration('TLMMemory', tlmPortElements, [memIfType, cxx_writer.writer_code.sc_moduleType])
    constructorBody = cxx_writer.writer_code.Code(constructorCode + 'end_module();')
    publicExtPortConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams + aliasParams, tlmPortInit + aliasInit)
    extPortDecl.addConstructor(publicExtPortConstr)

    return extPortDecl

def getGetIRQPorts(self):
    # Returns the classes implementing the interrupt ports; there can
    # be two different kind of ports: systemc based or TLM based
    hasTLM = False
    hasSysC = False
    for i in self.irqs:
        if i.operation:
            if i.tlm:
                hasTLM = True
            else:
                hasSysC = True

    # Lets now create the ports:
    classes = []
    if hasTLM:
        # TLM ports: I declare a normal TLM slave
        tlmsocketType = cxx_writer.writer_code.TemplateType('tlm_utils::simple_target_socket', ['IntrTLMPort'], 'tlm_utils/simple_target_socket.h')
        payloadType = cxx_writer.writer_code.Type('tlm::tlm_generic_payload', 'tlm.h')
        tlmPortElements = []

        blockTransportCode = """tlm::tlm_command cmd = trans.get_command();
            unsigned char* ptr = trans.get_data_ptr();
            if(*ptr == 0){
                //Lower the interrupt
                this->irqSignal = false;
            }
            else{
                //Raise the interrupt
                this->irqSignal = true;
            }
            trans.set_response_status(tlm::TLM_OK_RESPONSE);
        """
        blockTransportBody = cxx_writer.writer_code.Code(blockTransportCode)
        payloadParam = cxx_writer.writer_code.Parameter('trans', payloadType.makeRef())
        delayParam = cxx_writer.writer_code.Parameter('delay', cxx_writer.writer_code.sc_timeType.makeRef())
        blockTransportDecl = cxx_writer.writer_code.Method('b_transport', blockTransportBody, cxx_writer.writer_code.voidType, 'pu', [payloadParam, delayParam])
        tlmPortElements.append(blockTransportDecl)
        socketAttr = cxx_writer.writer_code.Attribute('socket', tlmsocketType, 'pu')
        tlmPortElements.append(socketAttr)
        irqSignalAttr = cxx_writer.writer_code.Attribute('irqSignal', cxx_writer.writer_code.boolType.makeRef(), 'pu')
        tlmPortElements.append(irqSignalAttr)
        constructorCode = ''
        tlmPortInit = []
        constructorParams = []
        constructorParams.append(cxx_writer.writer_code.Parameter('portName', cxx_writer.writer_code.sc_module_nameType))
        constructorParams.append(cxx_writer.writer_code.Parameter('irqSignal', cxx_writer.writer_code.boolType.makeRef()))
        tlmPortInit.append('sc_module(portName)')
        tlmPortInit.append('irqSignal(irqSignal)')
        constructorCode += 'this->socket.register_b_transport(this, &IntrTLMPort::b_transport);\n'
        irqPortDecl = cxx_writer.writer_code.ClassDeclaration('IntrTLMPort', tlmPortElements, [cxx_writer.writer_code.sc_moduleType])
        constructorBody = cxx_writer.writer_code.Code(constructorCode + 'end_module();')
        publicExtPortConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, tlmPortInit)
        irqPortDecl.addConstructor(publicExtPortConstr)
        classes.append(irqPortDecl)
    if hasSysC:
        # SystemC ports: I simply have a method listening for a signal; depending on the triggering type, wither
        # wait on edge, level ... and raise or lower the boolean variable accordingly
        boolSignalType = cxx_writer.writer_code.TemplateType('sc_signal', [cxx_writer.writer_code.boolType], 'systemc.h')
        systemcPortElements = []
        sensitiveMethodCode = 'this->irqSignal = this->recvIntr.read();'
        sensitiveMethodBody = cxx_writer.writer_code.Code(sensitiveMethodCode)
        sensitiveMethodDecl = cxx_writer.writer_code.Method('irqRecvMethod', sensitiveMethodBody, cxx_writer.writer_code.voidType, 'pu')
        systemcPortElements.append(sensitiveMethodDecl)
        signalAttr = cxx_writer.writer_code.Attribute('recvIntr', boolSignalType, 'pu')
        systemcPortElements.append(signalAttr)
        irqSignalAttr = cxx_writer.writer_code.Attribute('irqSignal', cxx_writer.writer_code.boolType.makeRef(), 'pu')
        tlmPortElements.append(irqSignalAttr)
        constructorCode = ''
        tlmPortInit = []
        constructorParams = []
        constructorParams.append(cxx_writer.writer_code.Parameter('portName', cxx_writer.writer_code.sc_module_nameType))
        constructorParams.append(cxx_writer.writer_code.Parameter('irqSignal', cxx_writer.writer_code.boolType.makeRef()))
        tlmPortInit.append('sc_module(portName)')
        tlmPortInit.append('irqSignal(irqSignal)')
        constructorCode += 'SC_METHOD();\nsensitive << this->recvIntr;\n'
        irqPortDecl = cxx_writer.writer_code.ClassDeclaration('IntrSysCPort', systemcPortElements, [cxx_writer.writer_code.sc_moduleType])
        constructorBody = cxx_writer.writer_code.Code(constructorCode + 'end_module();')
        publicExtPortConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, tlmPortInit)
        irqPortDecl.addConstructor(publicExtPortConstr)
        classes.append(irqPortDecl)
    return classes

def getGetPipelineStages(self, trace):
    # Returns the code implementing the class representing a pipeline stage
    pipeCodeElements = []
    pipelineElements = []
    constructorCode = ''
    constructorParamsBase = []
    constructorInit = []
    baseConstructorInit = ''
    pipeType = cxx_writer.writer_code.Type('BasePipeStage')
    IntructionType = cxx_writer.writer_code.Type('Instruction', include = 'instructions.hpp')
    registerType = cxx_writer.writer_code.Type('Register', include = 'registers.hpp')

    stageEndedFlag = cxx_writer.writer_code.Attribute('stageEnded', cxx_writer.writer_code.boolType, 'pu')
    pipelineElements.append(stageEndedFlag)
    constructorCode += 'this->stageEnded = false;\n'
    stageBeginningFlag = cxx_writer.writer_code.Attribute('stageBeginning', cxx_writer.writer_code.boolType, 'pu')
    pipelineElements.append(stageBeginningFlag)
    constructorCode += 'this->stageBeginning = false;\n'
    hasToFlush = cxx_writer.writer_code.Attribute('hasToFlush', cxx_writer.writer_code.boolType, 'pu')
    pipelineElements.append(hasToFlush)
    constructorCode += 'this->hasToFlush = false;\n'
    if not self.externalClock:
        stageEndedEvent = cxx_writer.writer_code.Attribute('stageEndedEv', cxx_writer.writer_code.sc_eventType, 'pu')
        pipelineElements.append(stageEndedEvent)
        stageBeginningEvent = cxx_writer.writer_code.Attribute('stageBeginningEv', cxx_writer.writer_code.sc_eventType, 'pro')
        pipelineElements.append(stageBeginningEvent)


    NOPIntructionType = cxx_writer.writer_code.Type('NOPInstruction', 'instructions.hpp')
    NOPinstructionsAttribute = cxx_writer.writer_code.Attribute('NOPInstrInstance', NOPIntructionType.makePointer(), 'pu')
    pipelineElements.append(NOPinstructionsAttribute)

    if self.externalClock:
        sc_inBoolType = cxx_writer.writer_code.TemplateType('sc_in', [cxx_writer.writer_code.boolType], 'systemc.h')
        clockAttribute = cxx_writer.writer_code.Attribute('clock', sc_inBoolType.makeRef(), 'pu')
        pipelineElements.append(clockAttribute)
        clockParam = cxx_writer.writer_code.Parameter('clock', sc_inBoolType.makeRef())
        constructorParamsBase.append(clockParam)
        constructorInit.append('clock(clock)')
        baseConstructorInit += 'clock, '
        waitingForEndAttr = cxx_writer.writer_code.Attribute('waitingForEnd', cxx_writer.writer_code.boolType, 'pro')
        pipelineElements.append(waitingForEndAttr)
        constructorCode += 'this->waitingForEnd = false;\n'
        totCyclesAttribute = cxx_writer.writer_code.Attribute('waitCycles', cxx_writer.writer_code.uintType, 'pro')
        pipelineElements.append(totCyclesAttribute)
        constructorCode += 'this->waitCycles = 0;\n'
    else:
        latencyAttribute = cxx_writer.writer_code.Attribute('latency', cxx_writer.writer_code.sc_timeType, 'pro')
        pipelineElements.append(latencyAttribute)
        latencyParam = cxx_writer.writer_code.Parameter('latency', cxx_writer.writer_code.sc_timeType.makeRef())
        constructorParamsBase.append(latencyParam)
        constructorInit.append('latency(latency)')
        baseConstructorInit += 'latency, '

    curInstrAttr = cxx_writer.writer_code.Attribute('curInstruction', IntructionType.makePointer(), 'pu')
    pipelineElements.append(curInstrAttr)
    constructorCode += 'this->curInstruction = NULL;\n'
    nextInstrAttr = cxx_writer.writer_code.Attribute('nextInstruction', IntructionType.makePointer(), 'pu')
    pipelineElements.append(nextInstrAttr)
    constructorCode += 'this->nextInstruction = NULL;\n'

    flushCode = """this->hasToFlush = true;
    if(this->prevStage != NULL){
        this->prevStage->flush();
    }
    """
    flushBody = cxx_writer.writer_code.Code(flushCode)
    flushDecl = cxx_writer.writer_code.Method('flush', flushBody, cxx_writer.writer_code.voidType, 'pu', noException = True)
    pipelineElements.append(flushDecl)

    if self.externalClock:
        waitPipeBeginCode = """this->stageBeginning = true;"""
        for i in range(0, len(self.pipes) - 1):
            waitPipeBeginCode += """if(!this->stage_""" + str(i) + """->stageBeginning){
                return false;
            }
            """
        waitPipeBeginCode += 'this->stageEnded = false;\nreturn true;'
        returnType = cxx_writer.writer_code.boolType
    else:
        waitPipeBeginCode = """this->stageBeginning = true;
        this->stageBeginningEv.notify();
        """
        for i in range(0, len(self.pipes) - 1):
            waitPipeBeginCode += """if(!this->stage_""" + str(i) + """->stageBeginning){
                wait(this->stage_""" + str(i) + """->stageBeginningEv);
            }
            """
        waitPipeBeginCode += 'this->stageEnded = false;'
        returnType = cxx_writer.writer_code.voidType
    waitPipeBeginBody = cxx_writer.writer_code.Code(waitPipeBeginCode)
    waitPipeBeginDecl = cxx_writer.writer_code.Method('waitPipeBegin', waitPipeBeginBody, returnType, 'pu', noException = True)
    pipelineElements.append(waitPipeBeginDecl)

    if self.externalClock:
        waitPipeEndCode = """this->stageBeginning = false;
        this->stageEnded = true;
        """
        for i in range(0, len(self.pipes) - 1):
            waitPipeEndCode += """if(!this->stage_""" + str(i) + """->stageEnded){
                return false;
            }
            """
        waitPipeEndCode += 'return true;'
        returnType = cxx_writer.writer_code.boolType
    else:
        waitPipeEndCode = """this->stageBeginning = false;
        this->stageEnded = true;
        this->stageEndedEv.notify();
        """
        for i in range(0, len(self.pipes) - 1):
            waitPipeEndCode += """if(!this->stage_""" + str(i) + """->stageEnded){
                wait(this->stage_""" + str(i) + """->stageEndedEv);
            }
            """
        returnType = cxx_writer.writer_code.voidType
    waitPipeEndBody = cxx_writer.writer_code.Code(waitPipeEndCode)
    waitPipeEndDecl = cxx_writer.writer_code.Method('waitPipeEnd', waitPipeEndBody, cxx_writer.writer_code.voidType, 'pu', noException = True)
    pipelineElements.append(waitPipeEndDecl)

    for i in range(0, len(self.pipes) - 1):
        otherStageAttr = cxx_writer.writer_code.Attribute('stage_' + str(i), pipeType.makePointer(), 'pro')
        pipelineElements.append(otherStageAttr)
        otherStageParam = cxx_writer.writer_code.Parameter('stage_' + str(i), pipeType.makePointer())
        constructorParamsBase.append(otherStageParam)
        constructorInit.append('stage_' + str(i) + '(stage_' + str(i) + ')')
        baseConstructorInit += 'stage_' + str(i) + ', '

    stageAttr = cxx_writer.writer_code.Attribute('prevStage', pipeType.makePointer(), 'pro')
    pipelineElements.append(stageAttr)
    stageAttr = cxx_writer.writer_code.Attribute('succStage', pipeType.makePointer(), 'pro')
    pipelineElements.append(stageAttr)
    unlockQueueAttr = cxx_writer.writer_code.Attribute('unlockQueue', cxx_writer.writer_code.TemplateType('std::vector', [registerType.makePointer()], 'vector'), 'pro', static = True)
    pipelineElements.append(unlockQueueAttr)
    prevStageParam = cxx_writer.writer_code.Parameter('prevStage', pipeType.makePointer(), initValue = 'NULL')
    succStageParam = cxx_writer.writer_code.Parameter('succStage', pipeType.makePointer(), initValue = 'NULL')
    constructorParamsBase.append(prevStageParam)
    constructorParamsBase.append(succStageParam)
    constructorInit.append('prevStage(prevStage)')
    constructorInit.append('succStage(succStage)')
    baseConstructorInit += 'prevStage, '
    baseConstructorInit += 'succStage, '
    pipelineDecl = cxx_writer.writer_code.ClassDeclaration('BasePipeStage', pipelineElements)
    constructorBody = cxx_writer.writer_code.Code(constructorCode)
    publicPipelineConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParamsBase, constructorInit)
    pipelineDecl.addConstructor(publicPipelineConstr)
    pipeCodeElements.append(pipelineDecl)


    hasCheckHazard = False
    hasWb = False
    for pipeStage in self.pipes:
        if pipeStage.checkHazard:
            if self.pipes.index(pipeStage) + 1 < len(self.pipes):
                if not self.pipes[self.pipes.index(pipeStage) + 1].endHazard:
                    hasCheckHazard = True
        if pipeStage.endHazard:
            if self.pipes.index(pipeStage) - 1 >= 0:
                if not self.pipes[self.pipes.index(pipeStage) - 1].checkHazard:
                    hasWb = True

    # Now I have to actually declare the different pipeline stages, all of them being equal a part from
    # the fecth stage which have to fetch instructions and check interrupts before calling
    # the appropriate behavior method
    checkHazardsMet = False
    wbStage = self.pipes[-1]
    for pipeStage in self.pipes:
        if pipeStage.wb:
            wbStage = pipeStage
        from isa import resolveBitType
        fetchWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize) + '>')

        pipeNameParam = cxx_writer.writer_code.Parameter('pipeName', cxx_writer.writer_code.sc_module_nameType)
        curPipeElements = []
        constructorCode = ''
        constructorInit = []
        constructorParams = [pipeNameParam] + constructorParamsBase

        codeString = """this->curInstruction = this->NOPInstrInstance;
        this->nextInstruction = this->NOPInstrInstance;
        """
        if pipeStage == self.pipes[0]:
            # This is the fetch pipeline stage, I have to fetch instructions
            if self.instructionCache:
                codeString += 'template_map< ' + str(fetchWordType) + ', Instruction * >::iterator instrCacheEnd = ' + pipeStage.name.upper() + '_PipeStage::instrCache.end();\n'
            if self.externalClock:
                codeString += 'if(this->waitCycles > 0){\nthis->waitCycles--;\nreturn;\n}\n\n'
                codeString += """if(!this->waitingForEnd){
                // HERE WAIT FOR BEGIN OF ALL STAGES
                if(!this->waitPipeBegin()){
                    return;
                }
                """
            else:
                codeString += """while(true){
                // HERE WAIT FOR BEGIN OF ALL STAGES
                this->waitPipeBegin();

                """
            codeString += 'unsigned int numCycles = 0;\n'

            # Here is the code to deal with interrupts
            orderedIrqList = sorted(self.irqs, lambda x,y: cmp(y.priority, x.priority))
            for irqPort in orderedIrqList:
                if irqPort != orderedIrqList[0]:
                    codeString += 'else '
                codeString += 'if('
                if not irqPort.high:
                    codeString += '!'
                codeString += irqPort.name
                if(irqPort.condition):
                    codeString += ' && (' + irqPort.condition + ')'
                codeString += '){\n'
                codeString += irqPort.operation + '\n}\n'

            fetchCode = str(fetchWordType) + ' bitString = this->'
            # Now I have to check what is the fetch: if there is a TLM port or
            # if I have to access local memory
            if self.memory:
                # I perform the fetch from the local memory
                fetchCode += self.memory[0]
            else:
                for name, isFetch  in self.tlmPorts.items():
                    if isFetch:
                        fetchCode += name
                if codeString.endswith('= '):
                    raise Exception('No TLM port was chosen for the instruction fetch')
            fetchCode += '.read_word('
            if self.instructionCache and self.fastFetch:
                fetchAddress = 'curPC'
            else:
                fetchAddress = 'this->' + self.fetchReg[0]
            fetchCode += fetchAddress + ');\n'
            if self.instructionCache and self.fastFetch:
                codeString += str(fetchWordType) + ' curPC = this->' + self.fetchReg[0] + ';\n'
            else:
                codeString += fetchCode
            if trace:
                codeString += 'std::cerr << \"Current PC: \" << std::hex << std::showbase << '
                if self.fastFetch and self.instructionCache:
                    codeString += 'curPC'
                else:
                    codeString += fetchAddress
                codeString += ' << std::endl;\n'
            if self.instructionCache:
                codeString += 'template_map< ' + str(fetchWordType) + ', Instruction * >::iterator cachedInstr = ' + pipeStage.name.upper() + '_PipeStage::instrCache.find('
                if self.fastFetch:
                    codeString += 'curPC);'
                else:
                    codeString += 'bitString);'
                codeString += """
                if(cachedInstr != instrCacheEnd){
                    this->curInstruction = cachedInstr->second;
                    // I can call the instruction, I have found it
                """
                if hasCheckHazard and pipeStage.checkHazard:
                    if self.externalClock:
                        codeString += '//*****TODO***** Complete check\nif(!this->curInstruction->checkHazard()){\nreturn\n}\n'
                    else:
                        codeString += 'this->curInstruction->checkHazard();\n'
                    codeString += 'this->curInstruction->lockRegs();\n'
                codeString += 'try{\n'
                if pipeStage.checkTools:
                    codeString += """
                        #ifndef DISABLE_TOOLS
                        if(!(this->toolManager.newIssue(""" + fetchAddress + """, this->curInstruction))){
                        #endif"""
                codeString += """
                        numCycles = this->curInstruction->behavior_""" + pipeStage.name + """(BasePipeStage::unlockQueue);
                """
                if pipeStage.checkTools:
                    codeString += """
                        #ifndef DISABLE_TOOLS
                        }
                        #endif"""
                codeString += """
                    }
                    catch(annull_exception &etc){
                """
                if trace:
                    codeString += """std::cerr << "Stage: """ + pipeStage.name + """: Skipped Instruction " << this->curInstruction->getInstructionName() << std::endl << std::endl;
                    """
                codeString += """this->curInstruction = this->NOPInstrInstance;
                        numCycles = 0;
                    }
                }
                else{
                    // The current instruction is not present in the cache:
                    // I have to perform the normal decoding phase ...
                """
            if self.instructionCache and self.fastFetch:
                codeString += fetchCode
            codeString += """int instrId = decoder.decode(bitString);
            this->curInstruction = """ + pipeStage.name.upper() + """_PipeStage::INSTRUCTIONS[instrId];
            """
            codeString += 'this->curInstruction->setParams(bitString);\n'
            if hasCheckHazard and pipeStage.checkHazard:
                if self.externalClock:
                    codeString += '//*****TODO****** complete this code\nif(!this->curInstruction->checkHazard()){\nreturn\n}\n'
                else:
                    codeString += 'this->curInstruction->checkHazard();\n'
                codeString += 'this->curInstruction->lockRegs();\n'
            codeString += 'try{\n'
            if pipeStage.checkTools:
                codeString += """
                    #ifndef DISABLE_TOOLS
                    if(!(this->toolManager.newIssue(""" + fetchAddress + """, this->curInstruction))){
                    #endif"""
            codeString += """
                    numCycles = this->curInstruction->behavior_""" + pipeStage.name + """(BasePipeStage::unlockQueue);
            """
            if pipeStage.checkTools:
                codeString += """
                    #ifndef DISABLE_TOOLS
                    }
                    #endif"""
            codeString += """
                }
                catch(annull_exception &etc){
            """
            if trace:
                codeString += """std::cerr << "Stage """ + pipeStage.name + """: Skipped Instruction " << this->curInstruction->getInstructionName() << std::endl << std::endl;
                """
            codeString += """this->curInstruction = this->NOPInstrInstance;
                    numCycles = 0;
                }
                // ... and then add the instruction to the cache
            """
            if self.instructionCache:
                if self.fastFetch:
                    codeString += 'instrCache[curPC] = this->curInstruction;'
                else:
                    codeString += 'instrCache[bitString] = this->curInstruction;'
                if not self.externalClock:
                    codeString += """
                    instrCacheEnd = """ + pipeStage.name.upper() + """_PipeStage::instrCache.end();
                    """
                codeString += pipeStage.name.upper() + """_PipeStage::INSTRUCTIONS[instrId] = this->curInstruction->replicate();
                }
                """
            if self.externalClock:
                codeString += """this->waitCycles = numCycles;
                }
                // HERE WAIT FOR END OF ALL STAGES
                this->waitingForEnd = !this->waitPipeEnd();
                if(this->waitingForEnd){
                    return;
                }
                """
            else:
                codeString += """wait((numCycles + 1)*this->latency);
                // HERE WAIT FOR END OF ALL STAGES
                this->waitPipeEnd();

                """
            codeString += """
            // Now I have to propagate the instruction to the next cycle if
            // the next stage has completed elaboration
            if(this->hasToFlush){
                this->curInstruction = this->NOPInstrInstance;
                this->hasToFlush = false;
            }
            this->refreshRegisters();
            this->succStage->nextInstruction = this->curInstruction;
            this->numInstructions++;
            """
            if not self.externalClock:
                codeString += '}'
        else:
            # This is a normal pipeline stage
            if self.externalClock:
                codeString += 'if(this->waitCycles > 0){\nthis->waitCycles--;\nreturn;\n}\n\n'
                codeString += """if(!this->waitingForEnd){
                // HERE WAIT FOR BEGIN OF ALL STAGES
                if(!this->waitPipeBegin()){
                    return;
                }
                """
            else:
                codeString += """while(true){
                unsigned int numCycles = 0;
                // HERE WAIT FOR BEGIN OF ALL STAGES
                this->waitPipeBegin();

                """
            codeString += 'this->curInstruction = this->nextInstruction;\n'
            if hasCheckHazard and pipeStage.checkHazard:
                if self.externalClock:
                    codeString += '//*****TODO*******\nif(!this->curInstruction->checkHazard()){\nreturn\n}\n'
                else:
                    codeString += 'this->curInstruction->checkHazard();\n'
                codeString += 'this->curInstruction->lockRegs();\n'
            codeString += 'try{\n'
            if pipeStage.checkTools:
                codeString += """
                    #ifndef DISABLE_TOOLS
                    if(!(this->toolManager.newIssue(this->""" + self.fetchReg[0] + """, this->curInstruction))){
                    #endif
                """
            codeString += 'numCycles = this->curInstruction->behavior_' + pipeStage.name + '(BasePipeStage::unlockQueue);\n'
            if trace and pipeStage == self.pipes[-1]:
                codeString += """
                    this->curInstruction->printTrace();
                """
            if pipeStage.checkTools:
                codeString += """
                    #ifndef DISABLE_TOOLS
                    }
                    else{
                        this->curInstruction = this->NOPInstrInstance;
                        this->curInstruction->flushPipeline = true;
                    }
                    #endif
                """
            codeString += '}\n'
            codeString += 'catch(annull_exception &etc){\n'
            if trace:
                codeString += """std::cerr << "Stage """ + pipeStage.name + """: Skipped Instruction " << this->curInstruction->getInstructionName() << std::endl << std::endl;
                """
            if hasCheckHazard:
                codeString += 'this->curInstruction->getUnlock(BasePipeStage::unlockQueue);\n'
            codeString += """this->curInstruction = this->NOPInstrInstance;
                numCycles = 0;
            }
            """
            if self.externalClock:
                codeString += """this->waitCycles = numCycles;"""
            else:
                codeString += """wait((numCycles + 1)*this->latency);"""
            codeString += """// flushing current stage
            if(this->curInstruction->flushPipeline){
                this->curInstruction->flushPipeline = false;
                //Now I have to flush the preceding pipeline stages
                this->prevStage->flush();
            }
            """
            if self.externalClock:
                codeString += """}
                // HERE WAIT FOR END OF ALL STAGES
                this->waitingForEnd = !this->waitPipeEnd();
                if(this->waitingForEnd){
                    return;
                }
                """
            else:
                codeString += """// HERE WAIT FOR END OF ALL STAGES
                this->waitPipeEnd();

                """
            if pipeStage != self.pipes[-1]:
                codeString += """// Now I have to propagate the instruction to the next cycle if
                // the next stage has completed elaboration
                if(this->hasToFlush){
                    this->curInstruction = this->NOPInstrInstance;
                    this->hasToFlush = false;
                }
                this->succStage->nextInstruction = this->curInstruction;
                """
            if not self.externalClock:
                codeString += '}'
        if pipeStage.checkHazard:
            checkHazardsMet = True

        behaviorMethodBody = cxx_writer.writer_code.Code(codeString)
        behaviorMethodDecl = cxx_writer.writer_code.Method('behavior', behaviorMethodBody, cxx_writer.writer_code.voidType, 'pu')
        curPipeElements.append(behaviorMethodDecl)
        if self.externalClock:
            constructorCode += 'SC_METHOD(behavior);\nsensitive << this->clock.pos();\ndont_initialize();\n'
        else:
            constructorCode += 'SC_THREAD(behavior);\n'

        IntructionType = cxx_writer.writer_code.Type('Instruction', 'instructions.hpp')
        IntructionTypePtr = IntructionType.makePointer()
        if pipeStage == self.pipes[0]:
            # I create the refreshRegisters method; note that in order to update the registers
            # I just need to access any of the instructions, for instance I use the registers
            # if the NOP instruction. I have to see if the register values are different
            # from the registers in the wb stage: in case they are I update them with these
            # values, otherwise I go over the other stages and see if there is one different
            # and I update it. For each update I also update the other pipeline regs
            codeString = ''
            for reg in self.regs:
                if not reg.name in self.regOrder.keys():
                    codeString += 'if(this->' + reg.name + ' != this->NOPInstrInstance->' + reg.name + '_' + wbStage.name + '){\n'
                    codeString += 'this->' + reg.name + ' = this->NOPInstrInstance->' + reg.name + '_' + wbStage.name + ';\n'
                    for upPipe in self.pipes:
                        if upPipe != wbStage:
                            codeString += 'this->NOPInstrInstance->' + reg.name + '_' + upPipe.name + ' = this->' + reg.name + ';\n'
                    codeString += '}\n'
                    for checkPipe in self.pipes:
                        if checkPipe != wbStage:
                            codeString += 'else if(this->' + reg.name + ' != this->NOPInstrInstance->' + reg.name + '_' + checkPipe.name + '){\n'
                            codeString += 'this->' + reg.name + ' = this->NOPInstrInstance->' + reg.name + '_' + checkPipe.name + ';\n'
                            for upPipe in self.pipes:
                                if upPipe != checkPipe:
                                    codeString += 'this->NOPInstrInstance->' + reg.name + '_' + upPipe.name + ' = this->' + reg.name + ';\n'
                            codeString += '}\n'
                else:
                    for customWBStage in self.regOrder[reg.name]:
                        if customWBStage != self.regOrder[reg.name][0]:
                            codeString += 'else '
                        codeString += 'if(this->' + reg.name + ' != this->NOPInstrInstance->' + reg.name + '_' + customWBStage + '){\n'
                        codeString += 'this->' + reg.name + ' = this->NOPInstrInstance->' + reg.name + '_' + customWBStage + ';\n'
                        for upPipe in self.pipes:
                            if upPipe != wbStage:
                                codeString += 'this->NOPInstrInstance->' + reg.name + '_' + upPipe.name + ' = this->' + reg.name + ';\n'
                        codeString += '}\n'

            for regB in self.regBanks:
                codeString += 'for(int i = 0; i < ' + str(regB.numRegs) + '; i++){\n'
                if not regB.name in self.regOrder.keys():
                    codeString += 'if(this->' + regB.name + '[i] != this->NOPInstrInstance->' + regB.name + '_' + wbStage.name + '[i]){\n'
                    codeString += 'this->' + regB.name + '[i] = this->NOPInstrInstance->' + regB.name + '_' + wbStage.name + '[i];\n'
                    for upPipe in self.pipes:
                        if upPipe != wbStage:
                            codeString += 'this->NOPInstrInstance->' + regB.name + '_' + upPipe.name + '[i] = this->' + regB.name + '[i];\n'
                    codeString += '}\n'
                    for checkPipe in self.pipes:
                        if checkPipe != wbStage:
                            codeString += 'else if(this->' + regB.name + '[i] != this->NOPInstrInstance->' + regB.name + '_' + checkPipe.name + '[i]){\n'
                            codeString += 'this->' + regB.name + '[i] = this->NOPInstrInstance->' + regB.name + '_' + checkPipe.name + '[i];\n'
                            for upPipe in self.pipes:
                                if upPipe != checkPipe:
                                    codeString += 'this->NOPInstrInstance->' + regB.name + '_' + upPipe.name + '[i] = this->' + regB.name + '[i];\n'
                            codeString += '}\n'
                else:
                    for customWBStage in self.regOrder[regB.name]:
                        if customWBStage != self.regOrder[regB.name][0]:
                            codeString += 'else '
                        codeString += 'if(this->' + regB.name + '[i] != this->NOPInstrInstance->' + regB.name + '_' + customWBStage + '){\n'
                        codeString += 'this->' + regB.name + '[i] = this->NOPInstrInstance->' + regB.name + '_' + customWBStage + ';\n'
                        for upPipe in self.pipes:
                            if upPipe != wbStage:
                                codeString += 'this->NOPInstrInstance->' + regB.name + '_' + upPipe.name + '[i] = this->' + regB.name + '[i];\n'
                        codeString += '}\n'
                codeString += '}\n'
            # Now I have to produce the code for unlocking the registers in the unlockQueue
            codeString += """
            std::vector<Register *>::iterator unlockQueueIter, unlockQueueEnd;
            for(unlockQueueIter = BasePipeStage::unlockQueue.begin(), unlockQueueEnd = BasePipeStage::unlockQueue.end(); unlockQueueIter != unlockQueueEnd; unlockQueueIter++){
                (*unlockQueueIter)->unlock();
            }
            """
            refreshRegistersBody = cxx_writer.writer_code.Code(codeString)
            refreshRegistersDecl = cxx_writer.writer_code.Method('refreshRegisters', refreshRegistersBody, cxx_writer.writer_code.voidType, 'pu')
            curPipeElements.append(refreshRegistersDecl)
            # Here I declare the references to the real processor registers which I update at the
            # end of each cycle
            for reg in self.regs:
                attribute = cxx_writer.writer_code.Attribute(reg.name, resourceType[reg.name].makeRef(), 'pu')
                constructorParams = [cxx_writer.writer_code.Parameter(reg.name, resourceType[reg.name].makeRef())] + constructorParams
                constructorInit.append(reg.name + '(' + reg.name + ')')
                curPipeElements.append(attribute)
            for regB in self.regBanks:
                attribute = cxx_writer.writer_code.Attribute(regB.name, resourceType[regB.name].makeRef(), 'pu')
                constructorParams = [cxx_writer.writer_code.Parameter(regB.name, resourceType[regB.name].makeRef())] + constructorParams
                constructorInit.append(regB.name + '(' + regB.name + ')')
                curPipeElements.append(attribute)
            # I have to also instantiate the reference to the memories, in order to be able to
            # fetch instructions
            if self.memory:
                # I perform the fetch from the local memory
                memName = self.memory[0]
                memType = cxx_writer.writer_code.Type('LocalMemory', 'memory.hpp').makeRef()
            else:
                for name, isFetch  in self.tlmPorts.items():
                    if isFetch:
                        memName = name
                        memType = cxx_writer.writer_code.Type('TLMMemory', 'externalPorts.hpp').makeRef()
            constructorParams = [cxx_writer.writer_code.Parameter(memName, memType)] + constructorParams
            constructorInit.append(memName + '(' + memName + ')')
            memRefAttr = cxx_writer.writer_code.Attribute(memName, memType, 'pri')
            curPipeElements.append(memRefAttr)
            decoderAttribute = cxx_writer.writer_code.Attribute('decoder', cxx_writer.writer_code.Type('Decoder', 'decoder.hpp'), 'pri')
            curPipeElements.append(decoderAttribute)
            # I also have to add the map containig the ISA instructions to this stage
            instructionsAttribute = cxx_writer.writer_code.Attribute('INSTRUCTIONS', IntructionTypePtr.makePointer().makeRef(), 'pri')
            curPipeElements.append(instructionsAttribute)
            constructorParams = [cxx_writer.writer_code.Parameter('INSTRUCTIONS', IntructionTypePtr.makePointer().makeRef())] + constructorParams
            constructorInit.append('INSTRUCTIONS(INSTRUCTIONS)')
            fetchAttr = cxx_writer.writer_code.Attribute(self.fetchReg[0], resourceType[self.fetchReg[0]].makeRef(), 'pri')
            constructorParams = [cxx_writer.writer_code.Parameter(self.fetchReg[0], resourceType[self.fetchReg[0]].makeRef())] + constructorParams
            constructorInit.append(self.fetchReg[0] + '(' + self.fetchReg[0] + ')')
            curPipeElements.append(fetchAttr)
            numInstructions = cxx_writer.writer_code.Attribute('numInstructions', cxx_writer.writer_code.uintType.makeRef(), 'pri')
            constructorParams = [cxx_writer.writer_code.Parameter('numInstructions', cxx_writer.writer_code.uintType.makeRef())] + constructorParams
            constructorInit.append('numInstructions(numInstructions)')
            curPipeElements.append(numInstructions)
            if self.instructionCache:
                template_mapType = cxx_writer.writer_code.TemplateType('template_map', [fetchWordType, IntructionTypePtr], hash_map_include).makeRef()
                cacheAttribute = cxx_writer.writer_code.Attribute('instrCache', template_mapType, 'pri')
                curPipeElements.append(cacheAttribute)
                constructorParams = [cxx_writer.writer_code.Parameter('instrCache', template_mapType)] + constructorParams
                constructorInit.append('instrCache(instrCache)')

        if pipeStage.checkTools:
            ToolsManagerType = cxx_writer.writer_code.TemplateType('ToolsManager', [fetchWordType], 'ToolsIf.hpp')
            toolManagerAttribute = cxx_writer.writer_code.Attribute('toolManager', ToolsManagerType.makeRef(), 'pri')
            curPipeElements.append(toolManagerAttribute)
            constructorParams = [cxx_writer.writer_code.Parameter('toolManager', ToolsManagerType.makeRef())] + constructorParams
            constructorInit.append('toolManager(toolManager)')
            fetchAttr = cxx_writer.writer_code.Attribute(self.fetchReg[0], resourceType[self.fetchReg[0]].makeRef(), 'pri')
            constructorParams = [cxx_writer.writer_code.Parameter(self.fetchReg[0], resourceType[self.fetchReg[0]].makeRef())] + constructorParams
            constructorInit.append(self.fetchReg[0] + '(' + self.fetchReg[0] + ')')
            curPipeElements.append(fetchAttr)
            instructionsAttribute = cxx_writer.writer_code.Attribute('INSTRUCTIONS', IntructionTypePtr.makePointer().makeRef(), 'pri')
            constructorInit.append('INSTRUCTIONS(INSTRUCTIONS)')
            curPipeElements.append(instructionsAttribute)

        constructorInit = ['sc_module(pipeName)', 'BasePipeStage(' + baseConstructorInit[:-2] + ')'] + constructorInit
        curPipeDecl = cxx_writer.writer_code.SCModule(pipeStage.name.upper() + '_PipeStage', curPipeElements, [pipeType])
        constructorBody = cxx_writer.writer_code.Code(constructorCode + 'end_module();')
        publicCurPipeConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, constructorInit)
        curPipeDecl.addConstructor(publicCurPipeConstr)
        pipeCodeElements.append(curPipeDecl)

    return pipeCodeElements

def getTestMainCode(self):
    # Returns the code for the file which contains the main
    # routine for the execution of the tests.
    global testNames
    code = ''
    for test in testNames:
        code += 'boost::unit_test::framework::master_test_suite().add( BOOST_TEST_CASE( &' + test + ' ) );\n'
    code += '\nreturn 0;'
    initCode = cxx_writer.writer_code.Code(code)
    initCode.addInclude('boost/test/included/unit_test.hpp')
    parameters = [cxx_writer.writer_code.Parameter('argc', cxx_writer.writer_code.intType), cxx_writer.writer_code.Parameter('argv[]', cxx_writer.writer_code.charPtrType)]
    initFunction = cxx_writer.writer_code.Function('init_unit_test_suite', initCode, cxx_writer.writer_code.Type('boost::unit_test::test_suite').makePointer(), parameters)

    code = 'return boost::unit_test::unit_test_main( &init_unit_test_suite, argc, argv );'
    mainCode = cxx_writer.writer_code.Code(code)
    mainCode.addInclude('systemc.h')
    mainCode.addInclude('boost/test/included/unit_test.hpp')
    parameters = [cxx_writer.writer_code.Parameter('argc', cxx_writer.writer_code.intType), cxx_writer.writer_code.Parameter('argv', cxx_writer.writer_code.charPtrType.makePointer())]
    mainFunction = cxx_writer.writer_code.Function('sc_main', mainCode, cxx_writer.writer_code.intType, parameters)
    return [initFunction, mainFunction]

def getMainCode(self, model):
    # Returns the code which instantiate the processor
    # in order to execute simulations
    from isa import resolveBitType
    wordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize) + '>')
    code = """
    boost::program_options::options_description desc("Processor simulator for """ + self.name + """");
    desc.add_options()
        ("help,h", "produces the help message")
        ("debugger,d", "activates the use of the software debugger")
    """
    if self.systemc or model.startswith('acc'):
        code += """("frequency,f", boost::program_options::value<double>(), "processor clock frequency specified in MHz [Default 1MHz]")
        """
    code += """("application,a", boost::program_options::value<std::string>(), "application to be executed on the simulator")
    ;

    boost::program_options::variables_map vm;
    boost::program_options::store(boost::program_options::parse_command_line(argc, argv, desc), vm);
    boost::program_options::notify(vm);

    // Checking that the parameters are correctly specified
    if(vm.count("help") != 0){
        std::cout << desc << std::endl;
        return 0;
    }
    if(vm.count("application") == 0){
        std::cerr << "It is necessary to specify the application which has to be simulated using the --application command line option" << std::endl << std::endl;
        std::cerr << desc << std::endl;
        return -1;
    }"""
    if (self.systemc or model.startswith('acc')) and not self.externalClock:
        code += """double latency = 10e-6; // 1us
        if(vm.count("frequency") != 0){
            latency = 1/(vm["frequency"].as<double>());
        }
        //Now we can procede with the actual instantiation of the processor
        Processor procInst(\"""" + self.name + """\", sc_time(latency*10e9, SC_NS));
        """
    else:
        code += """
        //Now we can procede with the actual instantiation of the processor
        Processor procInst(\"""" + self.name + """\");
        """
    if self.externalClock:
        code += '//** Here we have to connect the external clock to procInst.clock input port **//\n'
        code += """sc_clock TestClk("TestClock", 10, SC_NS,0.5);
        procInst.clock(TestClk);
        """
    instrMemName = ''
    if len(self.tlmPorts) > 0:
        code += """//Here we instantiate the memory and connect it
        //wtih the processor
        """
        if model.endswith('LT'):
            code += """MemoryLT<""" + str(len(self.tlmPorts)) + """, """ + str(self.wordSize) + """> mem("procMem", 1024*1024*10, sc_time(latency*10e9*2, SC_NS));
            """
        else:
            code += """MemoryAT<""" + str(len(self.tlmPorts)) + """, """ + str(self.wordSize) + """> mem("procMem", 1024*1024*10, sc_time(latency*10e9*2, SC_NS));
            """
        numPort = 0
        for tlmPortName, fetch in self.tlmPorts.items():
            code += 'procInst.' + tlmPortName + '.initSocket.bind(*(mem.socket[' + str(numPort) + ']));\n'
            numPort += 1
            if fetch:
                instrMemName = 'mem'
    if instrMemName == '' and self.memory:
        instrMemName = 'procInst.' + self.memory[0]

    execOffset = 0
    for pipeStage in self.pipes:
        if pipeStage.checkTools:
            break
        execOffset += 1
    code += """
    //And with the loading of the executable code
    boost::filesystem::path fullPluginPath = boost::filesystem::system_complete(boost::filesystem::path(vm["application"].as<std::string>(), boost::filesystem::native));
    if ( !boost::filesystem::exists( fullPluginPath ) ){
        std::cerr << "ERROR: specified application " << vm["application"].as<std::string>() << " does not exist" << std::endl;
        return -1;
    }
    ExecLoader loader(vm["application"].as<std::string>(), false);
    //Lets copy the binary code into memory
    unsigned char * programData = loader.getProgData();
    for(unsigned int i = 0; i < loader.getProgDim(); i++){
        """ + instrMemName + """.write_byte_dbg(loader.getDataStart() + i, programData[i]);
    }
    //Finally I can set the processor variables
    procInst.ENTRY_POINT = loader.getProgStart();
    procInst.PROGRAM_LIMIT = loader.getProgDim() + loader.getDataStart();
    procInst.PROGRAM_START = loader.getDataStart();
    //Now I initialize the tools (i.e. debugger, os emulator, ...)
    """
    if model.startswith('acc'):
        code += 'OSEmulatorCA< ' + str(wordType) + ', -' + str(execOffset*self.wordSize) + ' > osEmu(*(procInst.abiIf), Processor::NOPInstrInstance, ' + str(self.abi.emulOffset) + ');\n'
    else:
        code += 'OSEmulator< ' + str(wordType) + ', 0 > osEmu(*(procInst.abiIf), ' + str(self.abi.emulOffset) + ');\n'
    code += """GDBStub< """ + str(wordType) + """ > gdbStub(*(procInst.abiIf));
    osEmu.initSysCalls(vm["application"].as<std::string>());
    procInst.toolManager.addTool(osEmu);
    if(vm.count("debugger") != 0){
        procInst.toolManager.addTool(gdbStub);
        gdbStub.initialize();
    }
    //Now we can start the execution
    boost::timer t;
    sc_start();
    double elapsedSec = t.elapsed();
    std::cout << "Elapsed " << elapsedSec << " sec." << std::endl;
    std::cout << "Executed " << procInst.numInstructions << " instructions" << std::endl;
    std::cout << "Execution Speed " << (double)procInst.numInstructions/(elapsedSec*1e6) << " MIPS" << std::endl;
    """
    if self.systemc or model.startswith('acc'):
        code += 'std::cout << \"Simulated time \" << sc_time_stamp()/10e3 << std::endl;\n'
    else:
        code += 'std::cout << \"Elapsed \" << procInst.totalCycles << \" cycles\" << std::endl;\n'
    if self.endOp:
        code += '//Ok, simulation has ended: lets call cleanup methods\nprocInst.endOp();\n'
    code += """
    return 0;
    """
    mainCode = cxx_writer.writer_code.Code(code)
    mainCode.addInclude("""#ifdef _WIN32
#pragma warning( disable : 4101 )
#endif""")

    mainCode.addInclude('#define WIN32_LEAN_AND_MEAN')
    if model.endswith('LT'):
        mainCode.addInclude('MemoryLT.hpp')
    else:
        mainCode.addInclude('MemoryAT.hpp')
    mainCode.addInclude('processor.hpp')
    mainCode.addInclude('utils.hpp')
    mainCode.addInclude('systemc.h')
    mainCode.addInclude('execLoader.hpp')
    mainCode.addInclude('GDBStub.hpp')
    if model.startswith('acc'):
        mainCode.addInclude('osEmulatorCA.hpp')
    else:
        mainCode.addInclude('osEmulator.hpp')
    mainCode.addInclude('boost/program_options.hpp')
    mainCode.addInclude('boost/timer.hpp')
    mainCode.addInclude('boost/filesystem/operations.hpp')
    mainCode.addInclude('boost/filesystem/fstream.hpp')
    mainCode.addInclude('boost/filesystem/convenience.hpp')
    mainCode.addInclude('boost/filesystem/path.hpp')
    parameters = [cxx_writer.writer_code.Parameter('argc', cxx_writer.writer_code.intType), cxx_writer.writer_code.Parameter('argv', cxx_writer.writer_code.charPtrType.makePointer())]
    function = cxx_writer.writer_code.Function('sc_main', mainCode, cxx_writer.writer_code.intType, parameters)
    return function
