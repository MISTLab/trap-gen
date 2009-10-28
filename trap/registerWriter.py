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

# List of the operators which are redefined inside the register classes to enable
# direct access to the registers themselves
assignmentOps = ['=', '+=', '-=', '*=', '/=', '|=', '&=', '^=', '<<=', '>>=']
binaryOps = ['+', '-', '*', '/', '|', '&', '^', '<<', '>>']
unaryOps = ['~']
comparisonOps = ['<', '>', '<=', '>=', '==', '!=']

# Helper variables use during register type conmputation
regMaxType = None

import cxx_writer

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

def getCPPRegClass(self, model, regType, namespace):
    # returns the class implementing the current register; I have to
    # define all the operators;
    emptyBody = cxx_writer.writer_code.Code('')
    regWidthType = regMaxType

    registerType = cxx_writer.writer_code.Type('Register')
    InnerFieldType = cxx_writer.writer_code.Type('InnerField')
    registerElements = []
    normalRegType = regType.makeNormal()

    # First of all I determine if there is the need to create a const element
    constReg = False
    if self.constValue != None and type(self.constValue) != type({}):
        assignValueItem = str(self.constValue)
        readValueItem = str(self.constValue)
        constReg = True
    elif model.startswith('acc') or type(self.delay) == type({}) or self.delay == 0:
        assignValueItem = 'this->value'
        readValueItem = 'this->value'
    else:
        assignValueItem = 'this->updateSlot[' + str(self.delay - 1) + '] = true;\nthis->values[' + str(self.delay - 1) + ']'
        readValueItem = 'this->value'

    if constReg and model.startswith('acc'):
        isLockedBody = cxx_writer.writer_code.Code('return false;')
        isLockedMethod = cxx_writer.writer_code.Method('isLocked', isLockedBody, cxx_writer.writer_code.boolType, 'pu', noException = True)
        registerElements.append(isLockedMethod)


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
    operatorDecl = cxx_writer.writer_code.MemberOperator('[]', operatorBody, InnerFieldType.makeRef(), 'pu', operatorParam, noException = True, inline = True)
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
        clockCycleMethod = cxx_writer.writer_code.Method('clockCycle', clockCycleBody, cxx_writer.writer_code.voidType, 'pu', inline = True, noException = True)
        registerElements.append(clockCycleMethod)
    elif model.startswith('acc'):
        if self.constValue == None or type(self.constValue) == type({}):
            forceValueBody = cxx_writer.writer_code.Code('this->value = value;')
        else:
            forceValueBody = cxx_writer.writer_code.Code('')
        forceValueParam = [cxx_writer.writer_code.Parameter('value', regMaxType.makeRef().makeConst())]
        forceValueMethod = cxx_writer.writer_code.Method('forceValue', forceValueBody, cxx_writer.writer_code.voidType, 'pu', forceValueParam, noException = True)
        registerElements.append(forceValueMethod)
    if self.constValue == None or type(self.constValue) == type({}):
        immediateWriteCode = 'this->value = value;\n'
        if not model.startswith('acc') and type(self.delay) != type({}) and self.delay > 0:
            for i in range(0, self.delay):
                immediateWriteCode += 'this->updateSlot[' + str(i) + '] = false;\n'
        elif model.startswith('acc'):
            immediateWriteCode += '*(this->hasToPropagate) = true;\nthis->timeStamp = sc_time_stamp();\n'
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
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', noException = True)
        registerElements.append(operatorDecl)
    # Now I have the three versions of the operators, depending whether they take
    # in input the integer value, the specific register or the base one
    # INTEGER
    for i in assignmentOps:
        if self.constValue != None and type(self.constValue) != type({}):
            operatorBody = cxx_writer.writer_code.Code('return *this;')
        elif model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code(assignValueItem + ' ' + i + ' other;\n*(this->hasToPropagate) = true;\nthis->timeStamp = sc_time_stamp();\nreturn *this;')
        else:
            operatorBody = cxx_writer.writer_code.Code(assignValueItem + ' ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regType.makeRef(), 'pu', [operatorParam], noException = True)
        registerElements.append(operatorDecl)
    # SPECIFIC REGISTER
    for i in binaryOps:
        if self.offset and not model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code('return ((' + readValueItem + '  + ' + str(self.offset) + ') ' + i + ' (other.value + ' + str(self.offset) + '));')
        else:
            operatorBody = cxx_writer.writer_code.Code('return (' + readValueItem + ' ' + i + ' other.value);')
        operatorParam = cxx_writer.writer_code.Parameter('other', regType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True, noException = True)
        registerElements.append(operatorDecl)
    for i in comparisonOps:
        if self.offset and not model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code('return ((' + readValueItem + ' + ' + str(self.offset) + ') ' + i + ' (other.value + ' + str(self.offset) + '));')
        else:
            operatorBody = cxx_writer.writer_code.Code('return (' + readValueItem + ' ' + i + ' other.value);')
        operatorParam = cxx_writer.writer_code.Parameter('other', regType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True, noException = True)
        registerElements.append(operatorDecl)
    for i in assignmentOps:
        if self.constValue != None and type(self.constValue) != type({}):
            operatorBody = cxx_writer.writer_code.Code('return *this;')
        elif model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code(assignValueItem + ' ' + i + ' other;\n*(this->hasToPropagate) = true;\nthis->timeStamp = sc_time_stamp();\nreturn *this;')
        else:
            operatorBody = cxx_writer.writer_code.Code(assignValueItem + ' ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', regType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regType.makeRef(), 'pu', [operatorParam], noException = True)
        registerElements.append(operatorDecl)
    # GENERIC REGISTER: this case is look more complicated; actually I simply used the
    # operators of parameter other
    for i in binaryOps:
        if self.offset and not model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code('return ((' + readValueItem + '  + ' + str(self.offset) + ') ' + i + ' other);')
        else:
            operatorBody = cxx_writer.writer_code.Code('return (' + readValueItem + ' ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True, noException = True)
        registerElements.append(operatorDecl)
    for i in comparisonOps:
        if self.offset and not model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code('return ((' + readValueItem + '  + ' + str(self.offset) + ') ' + i + ' other);')
        else:
            operatorBody = cxx_writer.writer_code.Code('return (' + readValueItem + ' ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True, noException = True)
        registerElements.append(operatorDecl)
    for i in assignmentOps:
        if self.constValue != None and type(self.constValue) != type({}):
            operatorBody = cxx_writer.writer_code.Code('return *this;')
        elif model.startswith('acc'):
            operatorBody = cxx_writer.writer_code.Code(assignValueItem + ' ' + i + ' other;\n*(this->hasToPropagate) = true;\nthis->timeStamp = sc_time_stamp();\nreturn *this;')
        else:
            operatorBody = cxx_writer.writer_code.Code(assignValueItem + ' ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regType.makeRef(), 'pu', [operatorParam], noException = True)
        registerElements.append(operatorDecl)
    # Scalar value cast operator
    if self.offset and not model.startswith('acc'):
        operatorBody = cxx_writer.writer_code.Code('return (' + readValueItem + '  + ' + str(self.offset) + ');')
    else:
        operatorBody = cxx_writer.writer_code.Code('return ' + readValueItem + ';')
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), operatorBody, cxx_writer.writer_code.Type(''), 'pu', const = True, noException = True, inline = True)
    registerElements.append(operatorIntDecl)

    # Constructors
    fieldInit = []
    if not model.startswith('acc') and type(self.delay) != type({}) and self.delay > 0:
        for field in self.bitMask.keys():
            fieldInit.append('field_' + field + '(this->value, this->values[' + str(self.delay - 1) + '], this->updateSlot[' + str(self.delay - 1) + '])')
    elif model.startswith('acc'):
        for field in self.bitMask.keys():
            fieldInit.append('field_' + field + '(this->value, this->timeStamp, this->hasToPropagate)')
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
    publicMainClassEmptyConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', initList = fieldInit)

    # Stream Operators
    outStreamType = cxx_writer.writer_code.Type('std::ostream', 'ostream')
    code = 'stream << std::hex << std::showbase << ' + readValueItem + ' << std::dec;\nreturn stream;'
    operatorBody = cxx_writer.writer_code.Code(code)
    operatorParam = cxx_writer.writer_code.Parameter('stream', outStreamType.makeRef())
    operatorDecl = cxx_writer.writer_code.MemberOperator('<<', operatorBody, outStreamType.makeRef(), 'pu', [operatorParam], const = True, noException = True)
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
        if model.startswith('acc'):
            operatorCode += '*(this->hasToPropagate) = true;\nthis->timeStamp = sc_time_stamp();\n'
        operatorCode += 'return *this;'
        operatorBody = cxx_writer.writer_code.Code(operatorCode)
        operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
        operatorEqualDecl = cxx_writer.writer_code.MemberOperator('=', operatorBody, cxx_writer.writer_code.Type('InnerField').makeRef(), 'pu', [operatorParam], noException = True)
        InnerFieldElems.append(operatorEqualDecl)
        operatorCode = 'return (this->value & ' + hex(int(mask, 2)) + ')'
        if length[0] > 0:
            operatorCode += ' >> ' + str(length[0])
        operatorCode += ';'
        operatorBody = cxx_writer.writer_code.Code(operatorCode)
        operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), operatorBody, cxx_writer.writer_code.Type(''), 'pu', const = True, noException = True, inline = True)
        InnerFieldElems.append(operatorIntDecl)
        fieldAttribute = cxx_writer.writer_code.Attribute('value', regMaxType.makeRef(), 'pri')
        InnerFieldElems.append(fieldAttribute)
        if not model.startswith('acc') and type(self.delay) != type({}) and self.delay > 0:
            fieldAttribute = cxx_writer.writer_code.Attribute('valueLast', regMaxType.makeRef(), 'pri')
            InnerFieldElems.append(fieldAttribute)
            fieldAttribute = cxx_writer.writer_code.Attribute('lastValid', cxx_writer.writer_code.boolType.makeRef(), 'pri')
            InnerFieldElems.append(fieldAttribute)
        elif model.startswith('acc'):
            timeStampAttribute = cxx_writer.writer_code.Attribute('timeStamp', cxx_writer.writer_code.sc_timeType.makeRef(), 'pri')
            InnerFieldElems.append(timeStampAttribute)
            propagateAttribute = cxx_writer.writer_code.Attribute('hasToPropagate', cxx_writer.writer_code.boolType.makePointer().makeRef(), 'pri')
            InnerFieldElems.append(propagateAttribute)
        constructorParams = [cxx_writer.writer_code.Parameter('value', regMaxType.makeRef())]
        constructorInit = ['value(value)']
        if not model.startswith('acc') and type(self.delay) != type({}) and self.delay > 0:
            constructorParams.append(cxx_writer.writer_code.Parameter('valueLast', regMaxType.makeRef()))
            constructorInit.append('valueLast(valueLast)')
            constructorParams.append(cxx_writer.writer_code.Parameter('lastValid', cxx_writer.writer_code.boolType.makeRef()))
            constructorInit.append('lastValid(lastValid)')
        elif model.startswith('acc'):
            constructorParams.append(cxx_writer.writer_code.Parameter('timeStamp', cxx_writer.writer_code.sc_timeType.makeRef()))
            constructorInit.append('timeStamp(timeStamp)')
            constructorParams.append(cxx_writer.writer_code.Parameter('hasToPropagate', cxx_writer.writer_code.boolType.makePointer().makeRef()))
            constructorInit.append('hasToPropagate(hasToPropagate)')
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
    operatorEqualDecl = cxx_writer.writer_code.MemberOperator('=', operatorBody, cxx_writer.writer_code.Type('InnerField').makeRef(), 'pu', [operatorParam], noException = True)
    operatorBody = cxx_writer.writer_code.Code('return 0;')
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), operatorBody, cxx_writer.writer_code.Type(''), 'pu', const = True, noException = True, inline = True)
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

    registerDecl = cxx_writer.writer_code.ClassDeclaration(regType.name, registerElements, [registerType], namespaces = [namespace])
    registerDecl.addConstructor(publicMainClassEmptyConstr)
    for i in innerClasses:
        registerDecl.addInnerClass(i)
    return registerDecl

def getCPPRegBankClass(self, model, regType, namespace):
    # returns the class implementing the single register of
    # the register bank
    return getCPPRegClass(self, model, regType, namespace)

def getCPPPipelineReg(self, trace, combinedTrace, namespace):
    # This method returns the pipeline registers, which is a special registers
    # containing both the value of the registres itself and all the pipeline
    # latches.
    # I also contains special methods to propagate registers values in the
    # pipeline.
    # Note that there are different kinds of such registers, one for the
    # normal latched registers and one for the registers which are immediately
    # visible to all the other stages (e.g. for LEON they are the PC and NPC
    # registers).

    # Lets start with the creation of the latched registers: they have exactly
    # the same methods of the base registers
    pipelineRegClasses = []
    registerElements = []
    registerType = cxx_writer.writer_code.Type('Register')

    ################ Constructor: it initializes the internal registers ######################
    fullConstructorParams = []
    innerConstrInit = ''
    fullConstructorCode = ''
    emptyConstructorCode = ''
    i = 0
    for pipeStage in self.pipes:
        fullConstructorCode += 'this->reg_stage[' + str(i) + '] = reg_' + pipeStage.name + ';\n'
        fullConstructorCode += 'this->reg_stage[' + str(i) + ']->hasToPropagate = &(this->hasToPropagate);\n'
        emptyConstructorCode += 'this->reg_stage[' + str(i) + '] = NULL;\n'
        fullConstructorParams.append(cxx_writer.writer_code.Parameter('reg_' + pipeStage.name, registerType.makePointer()))
        innerConstrInit += 'reg_' + pipeStage.name + ', '
        i += 1
    fullConstructorCode += 'this->reg_all = reg_all;\n'
    fullConstructorCode += 'this->reg_all->hasToPropagate = &(this->hasToPropagate);\n'
    fullConstructorCode += 'this->hasToPropagate = false;\n'
    emptyConstructorCode += 'this->reg_all = NULL;\n'
    emptyConstructorCode += 'this->hasToPropagate = false;\n'
    innerConstrInit += 'reg_all'
    fullConstructorParams.append(cxx_writer.writer_code.Parameter('reg_all', registerType.makePointer()))
    constructorBody = cxx_writer.writer_code.Code(fullConstructorCode)
    publicFullConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', fullConstructorParams)
    constructorBody = cxx_writer.writer_code.Code(emptyConstructorCode)
    publicEmptyConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu')

    stagesRegsAttribute = cxx_writer.writer_code.Attribute('reg_stage[' + str(len(self.pipes)) + ']', registerType.makePointer(), 'pro')
    registerElements.append(stagesRegsAttribute)
    generalRegAttribute = cxx_writer.writer_code.Attribute('reg_all', registerType.makePointer(), 'pro')
    registerElements.append(generalRegAttribute)
    propagateAttribute = cxx_writer.writer_code.Attribute('hasToPropagate', cxx_writer.writer_code.boolType, 'pu')
    registerElements.append(propagateAttribute)

    ################ Lock and Unlock methods used for hazards detection ######################
    # For the general register they have a particular behavior: they have to lock all versions of the
    # registers, unlock unlocks all of them; concerning isLocked method, it returns the status
    # of the general register. Note that isLocked takes an additional parameter: if specified
    # the locked status of the corresponding stage register (used for bypass operations, where
    # we do not wait for the WB, but we take the value from a pipeline register)

    lockBody = cxx_writer.writer_code.Code("""for(int i = 0; i < """ + str(len(self.pipes)) + """; i++){
        this->reg_stage[i]->lock();
    }
    this->reg_all->lock();""")
    lockMethod = cxx_writer.writer_code.Method('lock', lockBody, cxx_writer.writer_code.voidType, 'pu', virtual = True, noException = True)
    registerElements.append(lockMethod)
    unlockBody = cxx_writer.writer_code.Code("""for(int i = 0; i < """ + str(len(self.pipes)) + """; i++){
        this->reg_stage[i]->unlock();
    }
    this->reg_all->unlock();""")
    unlockMethod = cxx_writer.writer_code.Method('unlock', unlockBody, cxx_writer.writer_code.voidType, 'pu', virtual = True, noException = True)
    registerElements.append(unlockMethod)
    latencyParam = cxx_writer.writer_code.Parameter('wbLatency', cxx_writer.writer_code.intType)
    unlockMethod = cxx_writer.writer_code.Method('unlock', unlockBody, cxx_writer.writer_code.voidType, 'pu', [latencyParam], virtual = True, noException = True)
    registerElements.append(unlockMethod)
    isLockedBody = cxx_writer.writer_code.Code('return this->reg_all->isLocked();')
    isLockedMethod = cxx_writer.writer_code.Method('isLocked', isLockedBody, cxx_writer.writer_code.boolType, 'pu', noException = True)
    registerElements.append(isLockedMethod)
    stageIdParam = cxx_writer.writer_code.Parameter('stageId', cxx_writer.writer_code.intType)
    isLockedBody = cxx_writer.writer_code.Code('return this->reg_stage[stageId]->isLocked();')
    isLockedMethod = cxx_writer.writer_code.Method('isLocked', isLockedBody, cxx_writer.writer_code.boolType, 'pu', [stageIdParam], noException = True)
    registerElements.append(isLockedMethod)

    # Now some virtual methods inherited from the base class
    forceValueBody = cxx_writer.writer_code.Code('this->reg_all->forceValue(value);')
    forceValueParam = [cxx_writer.writer_code.Parameter('value', regMaxType.makeRef().makeConst())]
    forceValueMethod = cxx_writer.writer_code.Method('forceValue', forceValueBody, cxx_writer.writer_code.voidType, 'pu', forceValueParam, noException = True)
    registerElements.append(forceValueMethod)

    immediateWriteBody = cxx_writer.writer_code.Code('this->reg_all->immediateWrite(value);')
    immediateWriteParam = [cxx_writer.writer_code.Parameter('value', regMaxType.makeRef().makeConst())]
    immediateWriteMethod = cxx_writer.writer_code.Method('immediateWrite', immediateWriteBody, cxx_writer.writer_code.voidType, 'pu', immediateWriteParam, noException = True)
    registerElements.append(immediateWriteMethod)
    readNewValueBody = cxx_writer.writer_code.Code('return this->reg_all->readNewValue();')
    readNewValueMethod = cxx_writer.writer_code.Method('readNewValue', readNewValueBody, regMaxType, 'pu', noException = True)
    registerElements.append(readNewValueMethod)

    # Propagate method, used to move register values from one stage to the other; the default implementation of such
    # method proceeded from the last stage to the first one: wb copied in REGS_all, exec in wb, .... REGS_all in fetch
    regReadUpdate = ''
    firstStages = 0
    for pipeStage in self.pipes:
        regReadUpdate += 'if(this->reg_all->timeStamp > this->reg_stage[' + str(firstStages) + ']->timeStamp){\n'
        ######
        if trace and not combinedTrace:
            regReadUpdate += 'std::cerr << "Propagating stage all into stage ' + str(firstStages) + '" << std::endl;\n'
        ######
        regReadUpdate += 'hasChanges = true;\n'
        regReadUpdate += 'this->reg_stage[' + str(firstStages) + ']->timeStamp = this->reg_all->timeStamp;\n'
        regReadUpdate += 'this->reg_stage[' + str(firstStages) + ']->forceValue(*(this->reg_all));\n}\n'
        if pipeStage.checkHazard:
            break
        else:
            firstStages += 1
    propagateCode = 'bool hasChanges = false;\n'
    propagateCode += 'if(!this->hasToPropagate){\nreturn;\n}\n'
    propagateCode += 'if(this->reg_stage[' + str(len(self.pipes) - 1) + ']->timeStamp > this->reg_all->timeStamp){\n'
    ######
    if trace and not combinedTrace:
        propagateCode += 'std::cerr << "Propagating stage ' + str(len(self.pipes) - 1) + ' into reg_all" << std::endl;\n'
    ######
    propagateCode += 'hasChanges = true;\n'
    propagateCode += 'this->reg_all->timeStamp = this->reg_stage[' + str(len(self.pipes) - 1) + ']->timeStamp;\n'
    propagateCode += 'this->reg_all->forceValue(*(this->reg_stage[' + str(len(self.pipes) - 1) + ']));\n}\n'
    propagateCode += 'for(int i = ' + str(len(self.pipes) - 2) + '; i >= ' + str(firstStages) + '; i--){\n'
    propagateCode += 'if(this->reg_stage[i]->timeStamp > this->reg_stage[i + 1]->timeStamp){\n'
    ######
    if trace and not combinedTrace:
        propagateCode += 'std::cerr << "Propagating stage " << std::dec << i << " into stage " << std::dec << i + 1 << std::endl;\n'
    ######
    propagateCode += 'hasChanges = true;\n'
    propagateCode += 'this->reg_stage[i + 1]->timeStamp = this->reg_stage[i]->timeStamp;\n'
    propagateCode += 'this->reg_stage[i + 1]->forceValue(*(this->reg_stage[i]));\n}\n'
    propagateCode += '}\n'
    propagateCode += regReadUpdate
    propagateCode += 'this->hasToPropagate = hasChanges;\n'
    propagateBody = cxx_writer.writer_code.Code(propagateCode)
    propagateMethod = cxx_writer.writer_code.Method('propagate', propagateBody, cxx_writer.writer_code.voidType, 'pu', noException = True, virtual = True)
    registerElements.append(propagateMethod)

    # Now here I have to define the method to get/set the pointer to the various
    # registers
    regIndexParam = cxx_writer.writer_code.Parameter('regIndex', cxx_writer.writer_code.intType, initValue = '-1')
    getRegisterBody = cxx_writer.writer_code.Code("""if(regIndex < 0){
        return this->reg_all;
    }
    else{
        return this->reg_stage[regIndex];
    }""")
    getRegisterMethod = cxx_writer.writer_code.Method('getRegister', getRegisterBody, registerType.makePointer(), 'pu', [regIndexParam], inline = True, noException = True)
    registerElements.append(getRegisterMethod)
    regPointerParam = cxx_writer.writer_code.Parameter('regPtr', registerType.makePointer())
    getRegisterBody = cxx_writer.writer_code.Code("""if(regIndex < 0){
        if(this->reg_all != NULL){
            THROW_EXCEPTION("Error, trying to initialize main register after the pipeline register initialization has already completed");
        }
        this->reg_all = regPtr;
        this->reg_all->hasToPropagate = &(this->hasToPropagate);
    }
    else{
        if(this->reg_stage[regIndex] != NULL){
            THROW_EXCEPTION("Error, trying to initialize register " << regIndex << " after the pipeline register initialization has already completed");
        }
        this->reg_stage[regIndex] = regPtr;
        this->reg_stage[regIndex]->hasToPropagate = &(this->hasToPropagate);
    }""")
    setRegisterMethod = cxx_writer.writer_code.Method('setRegister', getRegisterBody, cxx_writer.writer_code.voidType, 'pu', [regPointerParam, regIndexParam])
    registerElements.append(setRegisterMethod)

    # Simple base methods used to access the general register operators: we simply perform a forward towards
    # the corresponding operator of the general register (reg_all)
    InnerFieldType = cxx_writer.writer_code.Type('InnerField')
    operatorParam = cxx_writer.writer_code.Parameter('bitField', cxx_writer.writer_code.intType)
    operatorBody = cxx_writer.writer_code.Code('return (*(this->reg_all))[bitField];')
    operatorDecl = cxx_writer.writer_code.MemberOperator('[]', operatorBody, InnerFieldType.makeRef(), 'pu', [operatorParam], noException = True)
    registerElements.append(operatorDecl)
    for i in unaryOps:
        operatorBody = cxx_writer.writer_code.Code('return ' + i + '(*(this->reg_all));')
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', noException = True)
        registerElements.append(operatorDecl)
    for i in binaryOps:
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorBody = cxx_writer.writer_code.Code('return (*(this->reg_all)) ' + i + ' other;')
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True, noException = True)
        registerElements.append(operatorDecl)
    for i in comparisonOps:
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorBody = cxx_writer.writer_code.Code('return (*(this->reg_all)) ' + i + ' other;')
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True, noException = True)
        registerElements.append(operatorDecl)

    pureDeclTypes = [regMaxType, registerType]
    for pureDecls in pureDeclTypes:
        for i in assignmentOps:
            operatorParam = cxx_writer.writer_code.Parameter('other', pureDecls.makeRef().makeConst())
            operatorBody = cxx_writer.writer_code.Code('return (*(this->reg_all)) ' + i + ' other;')
            operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, registerType.makeRef(), 'pu', [operatorParam], noException = True)
            registerElements.append(operatorDecl)
    # Stream Operators
    outStreamType = cxx_writer.writer_code.Type('std::ostream', 'ostream')
    operatorParam = cxx_writer.writer_code.Parameter('stream', outStreamType.makeRef())
    operatorBody = cxx_writer.writer_code.Code('return stream << (*(this->reg_all));')
    operatorDecl = cxx_writer.writer_code.MemberOperator('<<', operatorBody, outStreamType.makeRef(), 'pu', [operatorParam], const = True, noException = True)
    registerElements.append(operatorDecl)
    operatorBody = cxx_writer.writer_code.Code('return *(this->reg_all);')
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), operatorBody, cxx_writer.writer_code.Type(''), 'pu', const = True, noException = True)
    registerElements.append(operatorIntDecl)

    pipelineRegClass = cxx_writer.writer_code.ClassDeclaration('PipelineRegister', registerElements, [registerType], namespaces = [namespace])
    pipelineRegClass.addConstructor(publicFullConstr)
    pipelineRegClass.addConstructor(publicEmptyConstr)
    pipelineRegClasses.append(pipelineRegClass)
    PipelineRegisterType = pipelineRegClass.getType()

    ############################################################################
    # Now I have to examine all the registers with special write back conditions
    # and create a special propagate method for all of them
    # First I need to create correspondence pipeline stages, numbers
    pipeNumbers = {}
    i = 0
    for pipeStage in self.pipes:
        pipeNumbers[pipeStage.name] = i
        i += 1
    orders = []
    for reg in self.regs:
        if reg.wbStageOrder:
            if not reg.wbStageOrder in orders:
                orders.append(reg.wbStageOrder)
    for order in orders:
        registerElements = []
        propagateCode = 'bool hasChanges = false;\n'
        propagateCode += 'if(!this->hasToPropagate){\nreturn;\n}\n'
        for pipeStage in order:
            if pipeStage != order[0]:
                propagateCode += 'else '
            propagateCode += 'if(this->reg_stage[' + str(pipeNumbers[pipeStage]) + ']->timeStamp > this->reg_all->timeStamp){\n'
            ######
            if trace and not combinedTrace:
                propagateCode += 'std::cerr << "Propagating stage ' + str(pipeNumbers[pipeStage]) + ' into all stages" << std::endl;\n'
            ######
            propagateCode += 'hasChanges = true;\n'
            propagateCode += 'this->reg_all->forceValue(*(this->reg_stage[' + str(pipeNumbers[pipeStage]) + ']));\n'
            propagateCode += 'this->reg_all->timeStamp = this->reg_stage[' + str(pipeNumbers[pipeStage]) + ']->timeStamp;\n'
            propagateCode += 'for(int i = 0; i < ' + str(len(self.pipes)) + '; i++){\n'
            propagateCode += 'this->reg_stage[i]->forceValue(*(this->reg_stage[' + str(pipeNumbers[pipeStage]) + ']));\n'
            propagateCode += 'this->reg_stage[i]->timeStamp = this->reg_stage[' + str(pipeNumbers[pipeStage]) + ']->timeStamp;\n'
            propagateCode += '}\n}\n'
        propagateCode += 'this->hasToPropagate = hasChanges;\n'
        propagateBody = cxx_writer.writer_code.Code(propagateCode)
        propagateMethod = cxx_writer.writer_code.Method('propagate', propagateBody, cxx_writer.writer_code.voidType, 'pu', noException = True)
        registerElements.append(propagateMethod)

        emptyBody = cxx_writer.writer_code.Code('')
        publicFullConstr = cxx_writer.writer_code.Constructor(emptyBody, 'pu', fullConstructorParams, ['PipelineRegister(' + innerConstrInit + ')'])
        publicEmptyConstr = cxx_writer.writer_code.Constructor(emptyBody, 'pu', initList = ['PipelineRegister()'])
        pipelineRegClass = cxx_writer.writer_code.ClassDeclaration('PipelineRegister_' + str(order)[1:-1].replace(', ', '_').replace('\'', ''), registerElements, [PipelineRegisterType], namespaces = [namespace])
        pipelineRegClass.addConstructor(publicFullConstr)
        pipelineRegClass.addConstructor(publicEmptyConstr)
        pipelineRegClasses.append(pipelineRegClass)

    return pipelineRegClasses

def getCPPRegisters(self, trace, combinedTrace, model, namespace):
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

    from procWriter import resourceType
    global resourceType

    from isa import resolveBitType
    global regMaxType
    regMaxType = resolveBitType('BIT<' + str(regLen) + '>')
    registerType = cxx_writer.writer_code.Type('Register')
    emptyBody = cxx_writer.writer_code.Code('')

    ################ Constructor: it initializes the width of the register ######################
    constructorCode = ''
    if model.startswith('acc'):
        constructorCode += 'this->numLocked = 0;\n'
        constructorCode += 'this->lockedLatency = -1;\n'
        constructorCode += 'this->hasToPropagate = NULL;\n'
        constructorCode += 'this->timeStamp = SC_ZERO_TIME;\n'
    constructorBody = cxx_writer.writer_code.Code(constructorCode)
    publicConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu')

    constructorCode = ''
    if model.startswith('acc'):
        constructorCode += 'this->numLocked = other.numLocked;\n'
        constructorCode += 'this->lockedLatency = other.lockedLatency;\n'
        constructorCode += 'this->hasToPropagate = other.hasToPropagate;\n'
        constructorCode += 'this->timeStamp = other.timeStamp;\n'
    copyConstrParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
    copyConstrBody = cxx_writer.writer_code.Code(constructorCode)
    copyConstr = cxx_writer.writer_code.Constructor(copyConstrBody, 'pu', [copyConstrParam])

    ################ Lock and Unlock methods used for hazards detection ######################
    if model.startswith('acc'):
        lockedLatencyAttribute = cxx_writer.writer_code.Attribute('lockedLatency', cxx_writer.writer_code.intType, 'pri')
        registerElements.append(lockedLatencyAttribute)
        lockedAttribute = cxx_writer.writer_code.Attribute('numLocked', cxx_writer.writer_code.intType, 'pri')
        registerElements.append(lockedAttribute)
        propagateAttribute = cxx_writer.writer_code.Attribute('hasToPropagate', cxx_writer.writer_code.boolType.makePointer(), 'pu')
        registerElements.append(propagateAttribute)
        timeStampAttribute = cxx_writer.writer_code.Attribute('timeStamp', cxx_writer.writer_code.sc_timeType, 'pu')
        registerElements.append(timeStampAttribute)
        lockBody = cxx_writer.writer_code.Code('this->lockedLatency = -1;\nthis->numLocked++;')
        lockMethod = cxx_writer.writer_code.Method('lock', lockBody, cxx_writer.writer_code.voidType, 'pu', virtual = True, noException = True)
        registerElements.append(lockMethod)
        unlockBody = cxx_writer.writer_code.Code('this->lockedLatency = -1;\nif(this->numLocked > 0){\nthis->numLocked--;\n}')
        unlockMethod = cxx_writer.writer_code.Method('unlock', unlockBody, cxx_writer.writer_code.voidType, 'pu', virtual = True, noException = True)
        registerElements.append(unlockMethod)
        latencyParam = cxx_writer.writer_code.Parameter('wbLatency', cxx_writer.writer_code.intType)
        unlockBody = cxx_writer.writer_code.Code("""if(wbLatency > 0){
            this->lockedLatency = wbLatency;
        }
        else{
            this->lockedLatency = -1;
            if(this->numLocked > 0){
                this->numLocked--;
            }
        }""")
        unlockMethod = cxx_writer.writer_code.Method('unlock', unlockBody, cxx_writer.writer_code.voidType, 'pu', [latencyParam], virtual = True, noException = True)
        registerElements.append(unlockMethod)
        isLockedBody = cxx_writer.writer_code.Code("""if(this->lockedLatency > 0){
            this->lockedLatency--;
            if(this->lockedLatency == 0){
                this->numLocked--;
            }
        }
        if(this->numLocked > 0){
            return true;
        }
        else{
            this->numLocked = 0;
            return false;
        }
        """)
        isLockedMethod = cxx_writer.writer_code.Method('isLocked', isLockedBody, cxx_writer.writer_code.boolType, 'pu', noException = True, virtual = True)
        registerElements.append(isLockedMethod)

    ################ Special Methods ######################
    immediateWriteParam = [cxx_writer.writer_code.Parameter('value', regMaxType.makeRef().makeConst())]
    immediateWriteMethod = cxx_writer.writer_code.Method('immediateWrite', emptyBody, cxx_writer.writer_code.voidType, 'pu', immediateWriteParam, pure = True, noException = True)
    registerElements.append(immediateWriteMethod)
    readNewValueMethod = cxx_writer.writer_code.Method('readNewValue', emptyBody, regMaxType, 'pu', pure = True, noException = True)
    registerElements.append(readNewValueMethod)
    if not model.startswith('acc'):
        clockCycleMethod = cxx_writer.writer_code.Method('clockCycle', emptyBody, cxx_writer.writer_code.voidType, 'pu', virtual = True, noException = True)
        registerElements.append(clockCycleMethod)
    else:
        forceValueParam = [cxx_writer.writer_code.Parameter('value', regMaxType.makeRef().makeConst())]
        forceValueMethod = cxx_writer.writer_code.Method('forceValue', emptyBody, cxx_writer.writer_code.voidType, 'pu', forceValueParam, pure = True, noException = True)
        registerElements.append(forceValueMethod)

    ################ Operators working with the base class, employed when polimorphism is used ##################
    # First lets declare the class which will be used to manipulate the
    # bitfields
    InnerFieldType = cxx_writer.writer_code.Type('InnerField')
    operatorBody = cxx_writer.writer_code.Code('*this = (unsigned int)other;\nreturn *this;')
    operatorParam = cxx_writer.writer_code.Parameter('other', InnerFieldType.makeRef().makeConst())
    operatorEqualInnerDecl = cxx_writer.writer_code.MemberOperator('=', operatorBody, InnerFieldType.makeRef(), 'pu', [operatorParam], noException = True)
    operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
    operatorEqualDecl = cxx_writer.writer_code.MemberOperator('=', emptyBody, InnerFieldType.makeRef(), 'pu', [operatorParam], pure = True, noException = True)
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), emptyBody, cxx_writer.writer_code.Type(''), 'pu', const = True, pure = True, noException = True)
    InnerFieldClass = cxx_writer.writer_code.ClassDeclaration('InnerField', [operatorEqualInnerDecl, operatorEqualDecl, operatorIntDecl], namespaces = [namespace])
    publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    InnerFieldClass.addDestructor(publicDestr)

    # Now lets procede with the members of the main class
    operatorParam = cxx_writer.writer_code.Parameter('bitField', cxx_writer.writer_code.intType)
    operatorDecl = cxx_writer.writer_code.MemberOperator('[]', emptyBody, InnerFieldClass.getType().makeRef(), 'pu', [operatorParam], pure = True, noException = True)
    registerElements.append(operatorDecl)
    for i in unaryOps:
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, emptyBody, regMaxType, 'pu', pure = True, noException = True)
        registerElements.append(operatorDecl)
    for i in binaryOps:
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, emptyBody, regMaxType, 'pu', [operatorParam], const = True, pure = True, noException = True)
        registerElements.append(operatorDecl)
    for i in comparisonOps:
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, emptyBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True, pure = True, noException = True)
        registerElements.append(operatorDecl)

    pureDeclTypes = [regMaxType, registerType]
    for pureDecls in pureDeclTypes:
        for i in assignmentOps:
            operatorParam = cxx_writer.writer_code.Parameter('other', pureDecls.makeRef().makeConst())
            operatorDecl = cxx_writer.writer_code.MemberOperator(i, emptyBody, registerType.makeRef(), 'pu', [operatorParam], pure = True, noException = True)
            registerElements.append(operatorDecl)
    # Stream Operators
    outStreamType = cxx_writer.writer_code.Type('std::ostream', 'ostream')
    operatorParam = cxx_writer.writer_code.Parameter('other', outStreamType.makeRef())
    operatorDecl = cxx_writer.writer_code.MemberOperator('<<', emptyBody, outStreamType.makeRef(), 'pu', [operatorParam], const = True, pure = True, noException = True)
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
            if (reg.constValue and len(reg.constValue) < reg.numRegs)  or ((reg.delay and len(reg.delay) < reg.numRegs) and not model.startswith('acc')):
                resourceType[reg.name + '_baseType'] = resourceType[reg.name]
                resourceType[reg.name] = cxx_writer.writer_code.Type('RegisterBankClass', 'registers.hpp')
            else:
                resourceType[reg.name] = resourceType[reg.name].makePointer()
    realRegClasses = []
    for regType in regTypes:
        realRegClasses.append(regType.getCPPClass(model, resourceType[regType.name], namespace))
    ################ End of part where we determine the different register types which have to be declared ##################

    registerDecl = cxx_writer.writer_code.ClassDeclaration('Register', registerElements, namespaces = [namespace])
    registerDecl.addConstructor(publicConstr)
    registerDecl.addConstructor(copyConstr)

    ################ Finally I put everything together##################
    classes = [InnerFieldClass, registerDecl] + realRegClasses

    ###################################################################################
    # I also need to declare a global RegisterBank Class in case there are register banks
    # containing registers of different types
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
        setNewRegisterBody.addInclude('trap_utils.hpp')
        setNewRegisterParams = [cxx_writer.writer_code.Parameter('numReg', cxx_writer.writer_code.uintType), cxx_writer.writer_code.Parameter('newReg', registerType.makePointer())]
        setNewRegisterMethod = cxx_writer.writer_code.Method('setNewRegister', setNewRegisterBody, cxx_writer.writer_code.voidType, 'pu', setNewRegisterParams)
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
        setSizeMethod = cxx_writer.writer_code.Method('setSize', setSizeBody, cxx_writer.writer_code.voidType, 'pu', setSizeParams, noException = True)
        regBankElements.append(setSizeMethod)
        operatorBody = cxx_writer.writer_code.Code('return *(this->registers[numReg]);')
        operatorParam = [cxx_writer.writer_code.Parameter('numReg', cxx_writer.writer_code.uintType)]
        operatorDecl = cxx_writer.writer_code.MemberOperator('[]', operatorBody, registerType.makeRef(), 'pu', operatorParam, inline = True, noException = True)
        regBankElements.append(operatorDecl)
        regBankClass = cxx_writer.writer_code.ClassDeclaration('RegisterBankClass', regBankElements, namespaces = [namespace])
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

    # Now I have to add the classes for the pipeline registers for the cycle accurate processor
    if model.startswith('acc'):
        classes += self.getCPPPipelineReg(trace, combinedTrace, namespace)

    return classes

def getCPPAlias(self, namespace):
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
    from procWriter import resourceType

    for i in self.aliasRegs + self.aliasRegBanks:
        resourceType[i.name] = aliasType

    ####################### Lets declare the operators used to access the register fields ##############
    codeOperatorBody = 'return (*this->reg)[bitField];'
    InnerFieldType = cxx_writer.writer_code.Type('InnerField')
    operatorBody = cxx_writer.writer_code.Code(codeOperatorBody)
    operatorParam = [cxx_writer.writer_code.Parameter('bitField', cxx_writer.writer_code.intType)]
    operatorDecl = cxx_writer.writer_code.MemberOperator('[]', operatorBody, InnerFieldType.makeRef(), 'pu', operatorParam, noException = True, inline = True)
    aliasElements.append(operatorDecl)

    ################ Methods used for the management of delayed registers ######################
    immediateWriteBody = isLockedBody = cxx_writer.writer_code.Code('this->reg->immediateWrite(value);')
    immediateWriteParam = [cxx_writer.writer_code.Parameter('value', regMaxType.makeRef().makeConst())]
    immediateWriteMethod = cxx_writer.writer_code.Method('immediateWrite', immediateWriteBody, cxx_writer.writer_code.voidType, 'pu', immediateWriteParam, noException = True)
    aliasElements.append(immediateWriteMethod)
    readNewValueBody = isLockedBody = cxx_writer.writer_code.Code('return this->reg->readNewValue();')
    readNewValueMethod = cxx_writer.writer_code.Method('readNewValue', readNewValueBody, regMaxType, 'pu', noException = True)
    aliasElements.append(readNewValueMethod)

    getRegBody = cxx_writer.writer_code.Code('return this->reg;')
    getRegMethod = cxx_writer.writer_code.Method('getReg', getRegBody, registerType.makePointer(), 'pu', inline = True, noException = True)
    aliasElements.append(getRegMethod)

    #################### Lets declare the normal operators (implementation of the pure operators of the base class) ###########
    for i in unaryOps:
        operatorBody = cxx_writer.writer_code.Code('return ' + i + '(*this->reg + this->offset);')
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', noException = True)
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
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, aliasType.makeRef(), 'pu', [operatorParam], inline = True, noException = True)
        aliasElements.append(operatorDecl)
    # Alias Register
    for i in binaryOps:
        operatorBody = cxx_writer.writer_code.Code('return ((*this->reg + this->offset) ' + i + ' *other.reg);')
        operatorParam = cxx_writer.writer_code.Parameter('other', aliasType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True, noException = True)
        aliasElements.append(operatorDecl)
#    for i in comparisonOps:
#        operatorBody = cxx_writer.writer_code.Code('return ((*this->reg + this->offset) ' + i + ' *other.reg);')
#        operatorParam = cxx_writer.writer_code.Parameter('other', aliasType.makeRef().makeConst())
#        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True)
#        aliasElements.append(operatorDecl)
    for i in assignmentOps:
        operatorBody = cxx_writer.writer_code.Code('*this->reg ' + i + ' *other.reg;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', aliasType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, aliasType.makeRef(), 'pu', [operatorParam], noException = True)
        aliasElements.append(operatorDecl)
    # GENERIC REGISTER:
    for i in binaryOps:
        operatorBody = cxx_writer.writer_code.Code('return ((*this->reg + this->offset) ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True, inline = True, noException = True)
        aliasElements.append(operatorDecl)
    for i in comparisonOps:
        operatorBody = cxx_writer.writer_code.Code('return ((*this->reg + this->offset) ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True, noException = True)
        aliasElements.append(operatorDecl)
    for i in assignmentOps:
        operatorBody = cxx_writer.writer_code.Code('*this->reg ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, aliasType.makeRef(), 'pu', [operatorParam], noException = True)
        aliasElements.append(operatorDecl)
    # Scalar value cast operator
    operatorBody = cxx_writer.writer_code.Code('return *this->reg + this->offset;')
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), operatorBody, cxx_writer.writer_code.Type(''), 'pu', const = True, noException = True, inline = True)
    aliasElements.append(operatorIntDecl)

    ######### Constructor: takes as input the initial register #########
    constructorBody = cxx_writer.writer_code.Code('this->referringAliases = NULL;')
    constructorParams = [cxx_writer.writer_code.Parameter('reg', registerType.makePointer())]
    constructorInit = ['reg(reg)']
    constructorParams.append(cxx_writer.writer_code.Parameter('offset', cxx_writer.writer_code.uintType, initValue = '0'))
    constructorInit += ['offset(offset)', 'defaultOffset(0)']
    publicMainClassConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, constructorInit)
    constructorInit = ['offset(0)', 'defaultOffset(0)']
    publicMainEmptyClassConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', [], constructorInit)
    # Constructor: takes as input the initial alias
    constructorBody = cxx_writer.writer_code.Code('initAlias->referredAliases.insert(this);\nthis->referringAliases = initAlias;')
    constructorParams = [cxx_writer.writer_code.Parameter('initAlias', aliasType.makePointer())]
    publicAliasConstrInit = ['reg(initAlias->reg)']
    constructorParams.append(cxx_writer.writer_code.Parameter('offset', cxx_writer.writer_code.uintType, initValue = '0'))
    publicAliasConstrInit += ['offset(initAlias->offset + offset)', 'defaultOffset(offset)']
    publicAliasConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, publicAliasConstrInit)
    destructorBody = cxx_writer.writer_code.Code("""std::set<Alias *>::iterator referredIter, referredEnd;
        for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
            if((*referredIter)->referringAliases == this)
                (*referredIter)->referringAliases = NULL;
        }
        if(this->referringAliases != NULL){
            this->referringAliases->referredAliases.erase(this);
        }
        this->referringAliases = NULL;""")
    publicAliasDestr = cxx_writer.writer_code.Constructor(destructorBody, 'pu')

    # Stream Operators
    outStreamType = cxx_writer.writer_code.Type('std::ostream', 'ostream')
    code = 'stream << *this->reg + this->offset;\nreturn stream;'
    operatorBody = cxx_writer.writer_code.Code(code)
    operatorParam = cxx_writer.writer_code.Parameter('stream', outStreamType.makeRef())
    operatorDecl = cxx_writer.writer_code.MemberOperator('<<', operatorBody, outStreamType.makeRef(), 'pu', [operatorParam], const = True, noException = True)
    aliasElements.append(operatorDecl)

    # Update method: updates the register pointed by this alias: Standard Alias
    updateCode = """this->reg = newAlias.reg;
    this->offset = newAlias.offset + newOffset;
    this->defaultOffset = newOffset;
    std::set<Alias *>::iterator referredIter, referredEnd;
    for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
        (*referredIter)->newReferredAlias(newAlias.reg, newAlias.offset + newOffset);
    }
    if(this->referringAliases != NULL){
        this->referringAliases->referredAliases.erase(this);
    }
    this->referringAliases = &newAlias;
    newAlias.referredAliases.insert(this);
    """
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam = [cxx_writer.writer_code.Parameter('newAlias', aliasType.makeRef())]
    updateParam.append(cxx_writer.writer_code.Parameter('newOffset', cxx_writer.writer_code.uintType))
    updateDecl = cxx_writer.writer_code.Method('updateAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', updateParam, inline = True, noException = True)
    aliasElements.append(updateDecl)
    updateCode = """this->offset = newAlias.offset;
    this->defaultOffset = 0;
    """
    updateCode += """this->reg = newAlias.reg;
    std::set<Alias *>::iterator referredIter, referredEnd;
    for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
    """
    updateCode += '(*referredIter)->newReferredAlias(newAlias.reg, newAlias.offset);'
    updateCode += """
    }
    if(this->referringAliases != NULL){
        this->referringAliases->referredAliases.erase(this);
    }
    this->referringAliases = &newAlias;
    newAlias.referredAliases.insert(this);
    """
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam = [cxx_writer.writer_code.Parameter('newAlias', aliasType.makeRef())]
    updateDecl = cxx_writer.writer_code.Method('updateAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', updateParam, inline = True, noException = True)
    aliasElements.append(updateDecl)

    updateCode = """this->reg = &newAlias;
    this->offset = newOffset;
    this->defaultOffset = 0;
    std::set<Alias *>::iterator referredIter, referredEnd;
    for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
        (*referredIter)->newReferredAlias(&newAlias, newOffset);
    }
    if(this->referringAliases != NULL){
        this->referringAliases->referredAliases.erase(this);
    }
    this->referringAliases = NULL;
    """
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam = [cxx_writer.writer_code.Parameter('newAlias', registerType.makeRef())]
    updateParam.append(cxx_writer.writer_code.Parameter('newOffset', cxx_writer.writer_code.uintType))
    updateDecl = cxx_writer.writer_code.Method('updateAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', updateParam, inline = True, noException = True)
    aliasElements.append(updateDecl)

    updateCode = """this->offset = 0;
    this->defaultOffset = 0;
    """
    updateCode += """this->reg = &newAlias;
    std::set<Alias *>::iterator referredIter, referredEnd;
    for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
        (*referredIter)->newReferredAlias(&newAlias);
    }
    if(this->referringAliases != NULL){
        this->referringAliases->referredAliases.erase(this);
    }
    this->referringAliases = NULL;
    """
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam = [cxx_writer.writer_code.Parameter('newAlias', registerType.makeRef())]
    updateDecl = cxx_writer.writer_code.Method('updateAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', updateParam, inline = True, noException = True)
    aliasElements.append(updateDecl)

    directSetCode = 'this->reg = newAlias.reg;\n'
    directSetCode += 'this->offset = newAlias.offset;\n'
    directSetCode += """if(this->referringAliases != NULL){
        this->referringAliases->referredAliases.erase(this);
    }
    this->referringAliases = &newAlias;
    newAlias.referredAliases.insert(this);
    """
    directSetBody = cxx_writer.writer_code.Code(directSetCode)
    directSetParam = [cxx_writer.writer_code.Parameter('newAlias', aliasType.makeRef())]
    directSetDecl = cxx_writer.writer_code.Method('directSetAlias', directSetBody, cxx_writer.writer_code.voidType, 'pu', directSetParam, noException = True)
    aliasElements.append(directSetDecl)

    directSetBody = cxx_writer.writer_code.Code("""this->reg = &newAlias;
    if(this->referringAliases != NULL){
        this->referringAliases->referredAliases.erase(this);
    }
    this->referringAliases = NULL;""")
    directSetParam = [cxx_writer.writer_code.Parameter('newAlias', registerType.makeRef())]
    directSetDecl = cxx_writer.writer_code.Method('directSetAlias', directSetBody, cxx_writer.writer_code.voidType, 'pu', directSetParam, noException = True)
    aliasElements.append(directSetDecl)

    updateCode = """this->reg = newAlias;
    this->offset = newOffset + this->defaultOffset;
    std::set<Alias *>::iterator referredIter, referredEnd;
    for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
        (*referredIter)->newReferredAlias(newAlias, newOffset);
    }
    """
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam = [cxx_writer.writer_code.Parameter('newAlias', registerType.makePointer())]
    updateParam.append(cxx_writer.writer_code.Parameter('newOffset', cxx_writer.writer_code.uintType))
    updateDecl = cxx_writer.writer_code.Method('newReferredAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', updateParam, inline = True, noException = True)
    aliasElements.append(updateDecl)

    updateCode = 'this->offset = this->defaultOffset;\n'
    updateCode += """this->reg = newAlias;
    std::set<Alias *>::iterator referredIter, referredEnd;
    for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
        (*referredIter)->newReferredAlias(newAlias);
    }"""
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam = [cxx_writer.writer_code.Parameter('newAlias', registerType.makePointer())]
    updateDecl = cxx_writer.writer_code.Method('newReferredAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', updateParam, inline = True, noException = True)
    aliasElements.append(updateDecl)


    regAttribute = cxx_writer.writer_code.Attribute('reg', registerType.makePointer(), 'pri')
    aliasElements.append(regAttribute)
    offsetAttribute = cxx_writer.writer_code.Attribute('offset', cxx_writer.writer_code.uintType, 'pri')
    aliasElements.append(offsetAttribute)
    offsetAttribute = cxx_writer.writer_code.Attribute('defaultOffset', cxx_writer.writer_code.uintType, 'pri')
    aliasElements.append(offsetAttribute)

    # Finally I declare the class and pass to it all the declared members: Standard Alias
    aliasesAttribute = cxx_writer.writer_code.Attribute('referredAliases', cxx_writer.writer_code.TemplateType('std::set', [aliasType.makePointer()], 'set'), 'pri')
    aliasElements.append(aliasesAttribute)
    aliasesAttribute = cxx_writer.writer_code.Attribute('referringAliases', aliasType.makePointer(), 'pri')
    aliasElements.append(aliasesAttribute)
    aliasDecl = cxx_writer.writer_code.ClassDeclaration(aliasType.name, aliasElements, namespaces = [namespace])
    aliasDecl.addConstructor(publicMainClassConstr)
    aliasDecl.addConstructor(publicMainEmptyClassConstr)
    aliasDecl.addConstructor(publicAliasConstr)
    aliasDecl.addDestructor(publicAliasDestr)

    classes = [aliasDecl]
    return classes

def getCPPPipelineAlias(self, namespace):
    # This method creates the class describing a register
    # alias: note that an alias simply holds a pointer to a register; the
    # operators are then redefined in order to call the corresponding operators
    # of the register. In addition there is the updateAlias operation which updates
    # the register this alias points to (and eventually the offset).
    regWidthType = regMaxType
    # If the cycle accurate processor is used, then each alias contains also the pipeline
    # register, i.e. the registers with the copies (latches) for each pipeline stage
    pipeRegisterType = cxx_writer.writer_code.Type('PipelineRegister', 'registers.hpp')
    registerType = cxx_writer.writer_code.Type('Register', 'registers.hpp')
    aliasType = cxx_writer.writer_code.Type('Alias', 'alias.hpp')
    aliasElements = []
    global resourceType
    from procWriter import resourceType

    for i in self.aliasRegs + self.aliasRegBanks:
        resourceType[i.name] = aliasType

    ####################### Lets declare the operators used to access the register fields ##############
    codeOperatorBody = 'return (*this->pipelineReg->getRegister(this->pipeId))[bitField];'
    InnerFieldType = cxx_writer.writer_code.Type('InnerField')
    operatorBody = cxx_writer.writer_code.Code(codeOperatorBody)
    operatorParam = [cxx_writer.writer_code.Parameter('bitField', cxx_writer.writer_code.intType)]
    operatorDecl = cxx_writer.writer_code.MemberOperator('[]', operatorBody, InnerFieldType.makeRef(), 'pu', operatorParam, noException = True, inline = True)
    aliasElements.append(operatorDecl)

    ################ Lock and Unlock methods used for hazards detection ######################
    pipeIdParam = cxx_writer.writer_code.Parameter('pipeId', cxx_writer.writer_code.uintType)
    setpipeIdBody = cxx_writer.writer_code.Code('if(this->pipeId < 0){\nthis->pipeId = pipeId;\n}\nelse{\nTHROW_ERROR(\"Error, pipeline Id of alias can only be set during alias initialization; it already has value \" << this->pipeId);\n}')
    setpipeIdMethod = cxx_writer.writer_code.Method('setPipeId', setpipeIdBody, cxx_writer.writer_code.voidType, 'pu', [pipeIdParam])
    aliasElements.append(setpipeIdMethod)
    getPipeRegBody = cxx_writer.writer_code.Code('return this->pipelineReg;')
    getPipeRegMethod = cxx_writer.writer_code.Method('getPipeReg', getPipeRegBody, pipeRegisterType.makePointer(), 'pu', inline = True, noException = True)
    aliasElements.append(getPipeRegMethod)
    getRegBody = cxx_writer.writer_code.Code('return this->pipelineReg->getRegister(this->pipeId);')
    getRegMethod = cxx_writer.writer_code.Method('getReg', getRegBody, registerType.makePointer(), 'pu', inline = True, noException = True)
    aliasElements.append(getRegMethod)
    newPipelineRegParam = cxx_writer.writer_code.Parameter('newPipelineReg', pipeRegisterType.makePointer())
    #setPipeRegBody = cxx_writer.writer_code.Code('this->pipelineReg = newPipelineReg;')
    #setPipeRegMethod = cxx_writer.writer_code.Method('setPipeReg', setPipeRegBody, cxx_writer.writer_code.voidType, 'pu', [newPipelineRegParam], inline = True, noException = True)
    #aliasElements.append(setPipeRegMethod)
    lockBody = cxx_writer.writer_code.Code('this->pipelineReg->lock();')
    lockMethod = cxx_writer.writer_code.Method('lock', lockBody, cxx_writer.writer_code.voidType, 'pu', inline = True, noException = True)
    aliasElements.append(lockMethod)
    unlockBody = cxx_writer.writer_code.Code('this->pipelineReg->unlock();')
    unlockMethod = cxx_writer.writer_code.Method('unlock', unlockBody, cxx_writer.writer_code.voidType, 'pu', inline = True, noException = True)
    aliasElements.append(unlockMethod)
    latencyParam = cxx_writer.writer_code.Parameter('wbLatency', cxx_writer.writer_code.intType)
    unlockBody = cxx_writer.writer_code.Code('this->pipelineReg->unlock(wbLatency);')
    unlockMethod = cxx_writer.writer_code.Method('unlock', unlockBody, cxx_writer.writer_code.voidType, 'pu', [latencyParam], inline = True, noException = True)
    aliasElements.append(unlockMethod)
    isLockedBody = cxx_writer.writer_code.Code('return this->pipelineReg->isLocked();')
    isLockedMethod = cxx_writer.writer_code.Method('isLocked', isLockedBody, cxx_writer.writer_code.boolType, 'pu', inline = True, noException = True)
    aliasElements.append(isLockedMethod)

    #################### Lets declare the normal operators (implementation of the pure operators of the base class) ###########
    for i in unaryOps:
        operatorBody = cxx_writer.writer_code.Code('return ' + i + '*this->pipelineReg->getRegister(this->pipeId);')
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', noException = True)
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
        operatorBody = cxx_writer.writer_code.Code('*this->pipelineReg->getRegister(this->pipeId) ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', regMaxType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, aliasType.makeRef(), 'pu', [operatorParam], inline = True, noException = True)
        aliasElements.append(operatorDecl)
    # Alias Register
#    for i in binaryOps:
#        operatorBody = cxx_writer.writer_code.Code('return (*this->pipelineReg->getRegister(this->pipeId) ' + i + ' *other.pipelineReg->getRegister(other.pipeId));')
#        operatorParam = cxx_writer.writer_code.Parameter('other', aliasType.makeRef().makeConst())
#        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True, noException = True)
#        aliasElements.append(operatorDecl)
#    for i in comparisonOps:
#        operatorBody = cxx_writer.writer_code.Code('return ((*this->reg + this->offset) ' + i + ' *other.reg);')
#        operatorParam = cxx_writer.writer_code.Parameter('other', aliasType.makeRef().makeConst())
#        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True)
#        aliasElements.append(operatorDecl)
    for i in assignmentOps:
        operatorBody = cxx_writer.writer_code.Code('*this->pipelineReg->getRegister(this->pipeId) ' + i + ' *other.pipelineReg->getRegister(other.pipeId);\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', aliasType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, aliasType.makeRef(), 'pu', [operatorParam], noException = True)
        aliasElements.append(operatorDecl)
    # GENERIC REGISTER:
    for i in binaryOps:
        operatorBody = cxx_writer.writer_code.Code('return  (*this->pipelineReg->getRegister(this->pipeId) ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, regMaxType, 'pu', [operatorParam], const = True, inline = True, noException = True)
        aliasElements.append(operatorDecl)
    for i in comparisonOps:
        operatorBody = cxx_writer.writer_code.Code('return (*this->pipelineReg->getRegister(this->pipeId) ' + i + ' other);')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, cxx_writer.writer_code.boolType, 'pu', [operatorParam], const = True, noException = True)
        aliasElements.append(operatorDecl)
    for i in assignmentOps:
        operatorBody = cxx_writer.writer_code.Code('*this->pipelineReg->getRegister(this->pipeId) ' + i + ' other;\nreturn *this;')
        operatorParam = cxx_writer.writer_code.Parameter('other', registerType.makeRef().makeConst())
        operatorDecl = cxx_writer.writer_code.MemberOperator(i, operatorBody, aliasType.makeRef(), 'pu', [operatorParam], noException = True)
        aliasElements.append(operatorDecl)
    # Scalar value cast operator
    operatorBody = cxx_writer.writer_code.Code('return *this->pipelineReg->getRegister(this->pipeId);')
    operatorIntDecl = cxx_writer.writer_code.MemberOperator(str(regMaxType), operatorBody, cxx_writer.writer_code.Type(''), 'pu', const = True, noException = True, inline = True)
    aliasElements.append(operatorIntDecl)

    ######### Constructor: takes as input the initial register #########
    constructorBody = cxx_writer.writer_code.Code('this->referringAliases = NULL;')
    pipeRegParam = cxx_writer.writer_code.Parameter('pipelineReg', pipeRegisterType.makePointer())
    pipeIdParam = cxx_writer.writer_code.Parameter('pipeId', cxx_writer.writer_code.intType)
    publicMainClassConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', [pipeRegParam, pipeIdParam], ['pipelineReg(pipelineReg), pipeId(pipeId)'])
    publicMainEmptyClassConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', [pipeIdParam], ['pipelineReg(NULL), pipeId(pipeId)'])
    publicMainEmpty2ClassConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', initList = ['pipelineReg(NULL), pipeId(-1)'])
    # Constructor: takes as input the initial alias
    constructorBody = cxx_writer.writer_code.Code('initAlias->referredAliases.insert(this);\nthis->referringAliases = initAlias;')
    constructorParams = [cxx_writer.writer_code.Parameter('initAlias', aliasType.makePointer())]
    constructorParams.append(cxx_writer.writer_code.Parameter('pipeId', cxx_writer.writer_code.intType, initValue = '-1'))
    publicAliasConstrInit = ['pipelineReg(initAlias->pipelineReg), pipeId(pipeId)']
    publicAliasConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, publicAliasConstrInit)
    destructorBody = cxx_writer.writer_code.Code("""std::set<Alias *>::iterator referredIter, referredEnd;
        for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
            if((*referredIter)->referringAliases == this)
                (*referredIter)->referringAliases = NULL;
        }
        if(this->referringAliases != NULL){
            this->referringAliases->referredAliases.erase(this);
        }
        this->referringAliases = NULL;""")
    publicAliasDestr = cxx_writer.writer_code.Constructor(destructorBody, 'pu')

    # Stream Operators
    outStreamType = cxx_writer.writer_code.Type('std::ostream', 'ostream')
    code = 'stream << *this->pipelineReg->getRegister(this->pipeId);\nreturn stream;'
    operatorBody = cxx_writer.writer_code.Code(code)
    operatorParam = cxx_writer.writer_code.Parameter('stream', outStreamType.makeRef())
    operatorDecl = cxx_writer.writer_code.MemberOperator('<<', operatorBody, outStreamType.makeRef(), 'pu', [operatorParam], const = True, noException = True)
    aliasElements.append(operatorDecl)

    # Update method: updates the register pointed by this alias: Standard Alias
    updateCode = """this->pipelineReg = newAlias.pipelineReg;
    std::set<Alias *>::iterator referredIter, referredEnd;
    for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
    """
    updateCode += '(*referredIter)->newReferredAlias(newAlias.pipelineReg);'
    updateCode += """
    }
    if(this->referringAliases != NULL){
        this->referringAliases->referredAliases.erase(this);
    }
    this->referringAliases = &newAlias;
    newAlias.referredAliases.insert(this);
    """
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam = [cxx_writer.writer_code.Parameter('newAlias', aliasType.makeRef())]
    updateDecl = cxx_writer.writer_code.Method('updateAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', updateParam, inline = True, noException = True)
    aliasElements.append(updateDecl)

    updateCode = """this->pipelineReg = &newAlias;
    std::set<Alias *>::iterator referredIter, referredEnd;
    for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
        (*referredIter)->newReferredAlias(&newAlias);
    }
    if(this->referringAliases != NULL){
        this->referringAliases->referredAliases.erase(this);
    }
    this->referringAliases = NULL;
    """
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam = [cxx_writer.writer_code.Parameter('newAlias', pipeRegisterType.makeRef())]
    updateDecl = cxx_writer.writer_code.Method('updateAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', updateParam, inline = True, noException = True)
    aliasElements.append(updateDecl)

    directSetCode = """this->pipelineReg = newAlias.pipelineReg;
    this->pipeId = newAlias.pipeId;
    if(this->referringAliases != NULL){
        this->referringAliases->referredAliases.erase(this);
    }
    this->referringAliases = &newAlias;
    newAlias.referredAliases.insert(this);
    """
    directSetBody = cxx_writer.writer_code.Code(directSetCode)
    directSetParam = [cxx_writer.writer_code.Parameter('newAlias', aliasType.makeRef())]
    directSetDecl = cxx_writer.writer_code.Method('directSetAlias', directSetBody, cxx_writer.writer_code.voidType, 'pu', directSetParam, noException = True)
    aliasElements.append(directSetDecl)

    directSetBody = cxx_writer.writer_code.Code("""this->pipelineReg = &newAlias;
    if(this->referringAliases != NULL){
        this->referringAliases->referredAliases.erase(this);
    }
    this->referringAliases = NULL;""")
    directSetParam = [cxx_writer.writer_code.Parameter('newAlias', pipeRegisterType.makeRef())]
    directSetDecl = cxx_writer.writer_code.Method('directSetAlias', directSetBody, cxx_writer.writer_code.voidType, 'pu', directSetParam, noException = True)
    aliasElements.append(directSetDecl)

    updateCode = """this->pipelineReg = newAlias;
    std::set<Alias *>::iterator referredIter, referredEnd;
    for(referredIter = this->referredAliases.begin(), referredEnd = this->referredAliases.end(); referredIter != referredEnd; referredIter++){
        (*referredIter)->newReferredAlias(newAlias);
    }"""
    updateBody = cxx_writer.writer_code.Code(updateCode)
    updateParam = [cxx_writer.writer_code.Parameter('newAlias', pipeRegisterType.makePointer())]
    updateDecl = cxx_writer.writer_code.Method('newReferredAlias', updateBody, cxx_writer.writer_code.voidType, 'pu', updateParam, inline = True, noException = True)
    aliasElements.append(updateDecl)

    regAttribute = cxx_writer.writer_code.Attribute('pipelineReg', pipeRegisterType.makePointer(), 'pri')
    aliasElements.append(regAttribute)
    pipelineIdAttribute = cxx_writer.writer_code.Attribute('pipeId', cxx_writer.writer_code.intType, 'pri')
    aliasElements.append(pipelineIdAttribute)

    # Finally I declare the class and pass to it all the declared members: Standard Alias
    aliasesAttribute = cxx_writer.writer_code.Attribute('referredAliases', cxx_writer.writer_code.TemplateType('std::set', [aliasType.makePointer()], 'set'), 'pri')
    aliasElements.append(aliasesAttribute)
    aliasesAttribute = cxx_writer.writer_code.Attribute('referringAliases', aliasType.makePointer(), 'pri')
    aliasElements.append(aliasesAttribute)
    aliasDecl = cxx_writer.writer_code.ClassDeclaration(aliasType.name, aliasElements, namespaces = [namespace])
    aliasDecl.addConstructor(publicMainClassConstr)
    aliasDecl.addConstructor(publicMainEmptyClassConstr)
    aliasDecl.addConstructor(publicMainEmpty2ClassConstr)
    aliasDecl.addConstructor(publicAliasConstr)
    aliasDecl.addDestructor(publicAliasDestr)

    classes = [aliasDecl]
    return classes
