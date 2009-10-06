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

import cxx_writer

# Contains, for each behavior, the type corresponding to the class which defines
# it. If a behavior is not here it means that it must be explicitly inlined
# in the instruction itself
baseBehaviors = []
behClass = {}
archWordType = None
alreadyDeclared = []
baseInstrConstrParams = []

def getToUnlockRegs(self, processor, pipeStage, regStageName, delayedUnlock):
    code = ''
    regsToUnlock = []

    for ps in processor.pipes:
        if ps.checkHazard:
            checkHazardStage = ps.name

    # Now I have to insert the code to fill in the queue of registers to unlock
    if not regStageName:
        if self.specialOutRegsWB.has_key(pipeStage.name):
            for regToUnlock in self.specialOutRegsWB[pipeStage.name]:
                regsToUnlock.append(regToUnlock)
    else:
        for regToUnlockList in self.specialOutRegsWB.values():
            for regToUnlock in regToUnlockList:
                regsToUnlock.append(regToUnlock)
    if pipeStage.endHazard or regStageName:
        # Here I have to unlock all the registers for which a special unlock stage
        # was not specified
        for regToUnlock in self.machineCode.bitCorrespondence.keys():
            if 'out' in self.machineCode.bitDirection[regToUnlock] and not regToUnlock in regsToUnlock:
                regsToUnlock.append(regToUnlock)
        for regToUnlock in self.bitCorrespondence.keys():
            if 'out' in self.bitDirection[regToUnlock] and not regToUnlock in regsToUnlock:
                regsToUnlock.append(regToUnlock)
        for regToUnlock in self.specialOutRegs:
            if not regToUnlock in regsToUnlock:
                regsToUnlock.append(regToUnlock)

        # Now I have to add registers to the queue of registers to unlock; note that
        # only the register itself can be added to the queue, not aliases.
        regsNames = [i.name for i in processor.regBanks + processor.regs]
        for regToUnlock in regsToUnlock:
            if not regToUnlock in self.notLockRegs:
                realName = regToUnlock
                parenthesis = realName.find('[')
                if parenthesis > 0:
                    realName = realName[:parenthesis]
                if regStageName:
                    if parenthesis > 0:
                        realRegName = realName + '_' + checkHazardStage + regToUnlock[parenthesis:]
                    else:
                        realRegName = regToUnlock + '_' + checkHazardStage
                else:
                    realRegName = regToUnlock
                if delayedUnlock and self.delayedWb.has_key(regToUnlock):
                    if not realName in regsNames:
                        code += 'unlockQueue[' + str(self.delayedWb[regToUnlock]) + '].push_back(' + realRegName + '.getReg());\n'
                    else:
                        code += 'unlockQueue[' + str(self.delayedWb[regToUnlock]) + '].push_back(&' + realRegName + ');\n'
                else:
                    if not realName in regsNames:
                        code += 'unlockQueue[0].push_back(' + realRegName + '.getReg());\n'
                    else:
                        code += 'unlockQueue[0].push_back(&' + realRegName + ');\n'
    return code

def toBinStr(intNum, maxLen = -1):
    # Given an integer number it converts it to a bitstring; maxLen is used only
    # in case a negative number have to be converted
    bitStr = []
    negative = (intNum < 0)
    intNum = abs(intNum)
    if negative:
        intNum = intNum - 1
    while intNum > 0:
        bitStr.append(str(intNum % 2))
        intNum = intNum / 2
    if negative:
        if maxLen < 0:
            raise Exception('We are converting number ' + str(intNum) + ' which is a negative number: the maximum number of bits should be specified')
        if len(bitStr) >= maxLen:
            raise Exception('Not enough bits specified to convert negative number ' + str(intNum))
        for i in range(len(bitStr), maxLen):
            bitStr.append(0)
        for i in range(0, len(bitStr)):
            if bitStr[i] == '1':
                bitStr[i] = '0'
            else:
                bitStr[i] = '1'
    bitStr.reverse()
    return bitStr

def getCppMethod(self, model, processor):
    # Returns the code implementing a helper method
    for var in self.localvars:
        self.code.addVariable(var)
    self.code.addInclude('trap_utils.hpp')
    import copy
    codeTemp = copy.deepcopy(self.code)

    defineCode = ''
    if model.startswith('acc'):
        # now I have to take all the resources and create a define which
        # renames such resources so that their usage can be transparent
        # to the developer
        for reg in processor.regs + processor.regBanks + processor.aliasRegs + processor.aliasRegBanks:
            defineCode += '#define ' + reg.name + ' ' + reg.name + '_' + self.stage + '\n'
        defineCode += '\n'

    codeTemp.prependCode(defineCode)

    undefCode = ''
    if model.startswith('acc'):
        # now I have to take all the resources and create a define which
        # renames such resources so that their usage can be transparent
        # to the developer
        undefCode += '\n'
        for reg in processor.regs + processor.regBanks + processor.aliasRegs + processor.aliasRegBanks:
            undefCode += '#undef ' + reg.name + '\n'
        undefCode += '\n'

    codeTemp.appendCode(undefCode)

    methodDecl = cxx_writer.writer_code.Method(self.name, codeTemp, self.retType, 'pu', self.parameters, noException = not self.exception, const = self.const)

    return methodDecl

def getCppOperation(self, parameters = False):
    # Returns the code implementing a helper operation
    aliasType = cxx_writer.writer_code.Type('Alias', 'alias.hpp')
    for var in self.localvars:
        self.code.addVariable(var)
    self.code.addInclude('trap_utils.hpp')
    metodParams = []
    if parameters:
        for elem in self.archElems:
            metodParams.append(cxx_writer.writer_code.Parameter(elem, aliasType.makeRef()))
            metodParams.append(cxx_writer.writer_code.Parameter(elem + '_bit', cxx_writer.writer_code.uintRefType))
        for elem in self.archVars:
            metodParams.append(cxx_writer.writer_code.Parameter(elem, cxx_writer.writer_code.uintRefType))
        for var in self.instrvars:
            metodParams.append(cxx_writer.writer_code.Parameter(var.name, var.type.makeRef()))
    methodDecl = cxx_writer.writer_code.Method(self.name, self.code, cxx_writer.writer_code.voidType, 'pro', metodParams, inline = True, noException = not self.exception)
    return methodDecl

def getCppOpClass(self, namespace):
    # Returns a class (directly deriving from instruction) implementing the
    # method corresponding to the current operation
    global baseInstrConstrParams
    from procWriter import baseInstrInitElement
    aliasType = cxx_writer.writer_code.Type('Alias', 'alias.hpp')
    instructionType = cxx_writer.writer_code.Type('Instruction', 'instructions.hpp')
    emptyBody = cxx_writer.writer_code.Code('')
    for var in self.localvars:
        self.code.addVariable(var)
    self.code.addInclude('trap_utils.hpp')
    classElements = []
    # Now I also need to declare the instruction variables and referenced architectural elements
    metodParams = []
    for elem in self.archElems:
        metodParams.append(cxx_writer.writer_code.Parameter(elem, aliasType.makeRef()))
        metodParams.append(cxx_writer.writer_code.Parameter(elem + '_bit', cxx_writer.writer_code.uintRefType))
    for elem in self.archVars:
        metodParams.append(cxx_writer.writer_code.Parameter(elem, cxx_writer.writer_code.uintRefType))
    for var in self.instrvars:
        metodParams.append(cxx_writer.writer_code.Parameter(var.name, var.varType.makeRef()))
    methodDecl = cxx_writer.writer_code.Method(self.name, self.code, cxx_writer.writer_code.voidType, 'pro', metodParams, inline = True, noException = not self.exception)
    classElements.append(methodDecl)
    opConstr = cxx_writer.writer_code.Constructor(emptyBody, 'pu', baseInstrConstrParams, ['Instruction(' + baseInstrInitElement + ')'])
    opDecl = cxx_writer.writer_code.ClassDeclaration(self.name + '_op', classElements, virtual_superclasses = [instructionType], namespaces = [namespace])
    opDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    opDecl.addDestructor(opDestr)
    opDecl.addConstructor(opConstr)
    return opDecl

def getCPPInstr(self, model, processor, trace, combinedTrace, namespace):
    # Returns the code implementing the current instruction: we have to provide the
    # implementation of all the abstract methods and call from the behavior method
    # all the different behaviors contained in the type hierarchy of this class
    pipeline = processor.pipes
    externalClock = processor.externalClock
    aliasType = cxx_writer.writer_code.Type('Alias', 'alias.hpp')
    instructionType = cxx_writer.writer_code.Type('Instruction', 'instructions.hpp')
    emptyBody = cxx_writer.writer_code.Code('')
    classElements = []
    baseClasses = []
    toInline = []
    behVars = []
    from procWriter import baseInstrInitElement
    global baseInstrConstrParams
    constrInitList = ['Instruction(' + baseInstrInitElement + ')']
    global alreadyDeclared
    global behClass
    for behaviors in self.postbehaviors.values() + self.prebehaviors.values():
        for beh in behaviors:
            if (model.startswith('acc') and beh.name in self.behaviorAcc) or (model.startswith('func') and beh.name in self.behaviorFun):
                if behClass.has_key(beh.name):
                    baseClasses.append(behClass[beh.name].getType())
                    constrInitList.append(beh.name + '_op(' + baseInstrInitElement + ')')
                elif beh.inline and not beh.name in alreadyDeclared and not model.startswith('acc'):
                    classElements.append(beh.getCppOperation())
                elif not beh.name in alreadyDeclared:
                    toInline.append(beh.name)
                for var in beh.instrvars:
                    if not var.name in behVars:
                        classElements.append(cxx_writer.writer_code.Attribute(var.name, var.varType, 'pro',  var.static))
                        behVars.append(var.name)
    if not baseClasses:
        baseClasses.append(instructionType)

    if model.startswith('acc'):
        # Now I have to add the code for checking data hazards
        hasCheckHazard = False
        hasWb = False
        for pipeStage in pipeline:
            if pipeStage.checkHazard:
                if pipeline.index(pipeStage) + 1 < len(pipeline):
                    if not pipeline[pipeline.index(pipeStage) + 1].wb:
                        hasCheckHazard = True
            if pipeStage.wb:
                if pipeline.index(pipeStage) - 1 >= 0:
                    if not pipeline[pipeline.index(pipeStage) - 1].checkHazard:
                        hasWb = True

    if not model.startswith('acc'):
        behaviorCode = 'this->totalInstrCycles = 0;\n'

    for pipeStage in pipeline:
        userDefineBehavior = ''
        if model.startswith('acc'):
            behaviorCode = 'this->stageCycles = 0;\n'

        # Now I start computing the actual user-defined behavior of this instruction
        if self.prebehaviors.has_key(pipeStage.name):
            for beh in self.prebehaviors[pipeStage.name]:
                if not ((model.startswith('acc') and beh.name in self.behaviorAcc) or (model.startswith('func') and beh.name in self.behaviorFun)):
                    continue
                if beh.name in toInline:
                    userDefineBehavior += '{\n'
                    for var in beh.localvars:
                        userDefineBehavior += str(var)
                    userDefineBehavior += str(beh.code)
                    userDefineBehavior += '}\n'
                elif behClass.has_key(beh.name) or beh.name in baseBehaviors:
                    userDefineBehavior += 'this->' + beh.name + '('
                    for elem in beh.archElems:
                        userDefineBehavior += 'this->' + elem + ', '
                        userDefineBehavior += 'this->' + elem + '_bit'
                        if beh.archVars or beh.instrvars or elem != beh.archElems[-1]:
                            userDefineBehavior += ', '
                    for elem in beh.archVars:
                        userDefineBehavior += 'this->' + elem
                        if beh.instrvars or elem != beh.archVars[-1]:
                            userDefineBehavior += ', '
                    for var in beh.instrvars:
                        userDefineBehavior += 'this->' + var.name
                        if var != beh.instrvars[-1]:
                            userDefineBehavior += ', '
                    userDefineBehavior += ');\n'
                else:
                    userDefineBehavior += 'this->' + beh.name + '();\n'
        if self.code.has_key(pipeStage.name):
            userDefineBehavior += str(self.code[pipeStage.name].code)
        if self.postbehaviors.has_key(pipeStage.name):
            for beh in self.postbehaviors[pipeStage.name]:
                if not ((model.startswith('acc') and beh.name in self.behaviorAcc) or (model.startswith('func') and beh.name in self.behaviorFun)):
                    continue
                if beh.name in toInline:
                    userDefineBehavior += str(beh.code)
                elif behClass.has_key(beh.name) or beh.name in baseBehaviors:
                    userDefineBehavior += 'this->' + beh.name + '('
                    for elem in beh.archElems:
                        userDefineBehavior += 'this->' + elem + ', '
                        userDefineBehavior += 'this->' + elem + '_bit'
                        if beh.archVars or beh.instrvars or elem != beh.archElems[-1]:
                            userDefineBehavior += ', '
                    for elem in beh.archVars:
                        userDefineBehavior += 'this->' + elem
                        if beh.instrvars or elem != beh.archVars[-1]:
                            userDefineBehavior += ', '
                    for var in beh.instrvars:
                        userDefineBehavior += 'this->' + var.name
                        if var != beh.instrvars[-1]:
                            userDefineBehavior += ', '
                    userDefineBehavior += ');\n'
                else:
                    userDefineBehavior += 'this->' + beh.name + '();\n'

        # Now I have to specify the code to manage data hazards in the pipeline; in particular to
        # add, if the current one is the writeBack stage, the registers locked in the read stage
        # to the unlock queue
        if model.startswith('acc'):
            if hasCheckHazard and pipeStage.endHazard:
                userDefineBehavior += getToUnlockRegs(self, processor, pipeStage, True, True)

            if userDefineBehavior:
                # now I have to take all the resources and create a define which
                # renames such resources so that their usage can be transparent
                # to the developer
                for reg in processor.regs + processor.regBanks + processor.aliasRegs + processor.aliasRegBanks:
                    behaviorCode += '#define ' + reg.name + ' ' + reg.name + '_' + pipeStage.name + '\n'
                for instrFieldName in self.machineCode.bitCorrespondence.keys() + self.bitCorrespondence.keys():
                    behaviorCode += '#define ' + instrFieldName + ' ' + instrFieldName + '_' + pipeStage.name + '\n'
                behaviorCode += '\n'

        behaviorCode += userDefineBehavior

        if model.startswith('acc'):
            if userDefineBehavior:
                for reg in processor.regs + processor.regBanks + processor.aliasRegs + processor.aliasRegBanks:
                    behaviorCode += '#undef ' + reg.name + '\n'
                for instrFieldName in self.machineCode.bitCorrespondence.keys() + self.bitCorrespondence.keys():
                    behaviorCode += '#undef ' + instrFieldName + '\n'

            behaviorCode += 'return this->stageCycles;\n\n'
            registerType = cxx_writer.writer_code.Type('Register')
            unlockQueueType = cxx_writer.writer_code.TemplateType('std::map', ['unsigned int', cxx_writer.writer_code.TemplateType('std::vector', [registerType.makePointer()], 'vector')], 'map')
            unlockQueueParam = cxx_writer.writer_code.Parameter('unlockQueue', unlockQueueType.makeRef())
            behaviorBody = cxx_writer.writer_code.Code(behaviorCode)
            behaviorDecl = cxx_writer.writer_code.Method('behavior_' + pipeStage.name, behaviorBody, cxx_writer.writer_code.uintType, 'pu', [unlockQueueParam])
            classElements.append(behaviorDecl)
    if not model.startswith('acc'):
        behaviorCode += 'return this->totalInstrCycles;'
        behaviorBody = cxx_writer.writer_code.Code(behaviorCode)
        behaviorDecl = cxx_writer.writer_code.Method('behavior', behaviorBody, cxx_writer.writer_code.uintType, 'pu')
        classElements.append(behaviorDecl)

    # Here we deal with the code for checking data hazards: three methods are used for this purpose:
    # --- checkHazard: is called at the beginning of the register read stage to check that the
    #     registers needed by the current instruction are not being written by a previous one in
    #     the pipeline; in case this happens, the method contains the code to halt the pipeline stage;
    #     I have to check for the in/inout registers and special registers as needed by the instruction
    # --- lockRegs: also called at the beginning of the register read pipeline stage to lock the out/inout
    #     registers needed by the instruction
    # --- getUnlock: called in every stage when the instruction is annulled: this means that it is substituted
    #     with a nop instruction: as such, registers which were previously locked are added to the unlock queue;
    #     since it can be called from any pipeline stage, we have a copy of this method for all the stages
    if model.startswith('acc'):
        from pipelineWriter import hasCheckHazard
        from pipelineWriter import wbStage
        from pipelineWriter import chStage

        if hasCheckHazard:
            for ps in processor.pipes:
                if ps.checkHazard:
                    checkHazardStage = ps.name

            # checkHazard
            regsToCheck = []
            checkHazardCode = 'bool regLocked = false;\n'
            for name, correspondence in self.machineCode.bitCorrespondence.items():
                if 'in' in self.machineCode.bitDirection[name]:
                    regsToCheck.append(name)
            for name, correspondence in self.bitCorrespondence.items():
                if 'in' in self.bitDirection[name]:
                    regsToCheck.append(name)
            for specialRegName in self.specialInRegs:
                regsToCheck.append(specialRegName)

            for regToCheck in regsToCheck:
                if not regToCheck in self.notLockRegs:
                    parenthesis = regToCheck.find('[')
                    if parenthesis > 0:
                        realRegName = regToCheck[:parenthesis] + '_' + checkHazardStage + regToCheck[parenthesis:]
                    else:
                        realRegName = regToCheck + '_' + checkHazardStage
                    checkHazardCode += 'regLocked = this->' + realRegName + '.isLocked() || regLocked;\n'
            checkHazardCode += 'return !regLocked;\n'

            checkHazardBody = cxx_writer.writer_code.Code(checkHazardCode)
            checkHazardDecl = cxx_writer.writer_code.Method('checkHazard', checkHazardBody, cxx_writer.writer_code.boolType, 'pu')
            classElements.append(checkHazardDecl)
            # lockRegs
            regsToLock = []
            lockCode = ''
            for name, correspondence in self.machineCode.bitCorrespondence.items():
                if 'out' in self.machineCode.bitDirection[name]:
                    regsToLock.append(name)
            for name, correspondence in self.bitCorrespondence.items():
                if 'out' in self.bitDirection[name]:
                    regsToLock.append(name)
            for specialRegName in self.specialOutRegs:
                regsToLock.append(specialRegName)
            for regToLock in regsToLock:
                if not regToLock in self.notLockRegs:
                    parenthesis = regToLock.find('[')
                    if parenthesis > 0:
                        realRegName = regToLock[:parenthesis] + '_' + checkHazardStage + regToLock[parenthesis:]
                    else:
                        realRegName = regToLock + '_' + checkHazardStage
                    lockCode += 'this->' + realRegName + '.lock();\n'
            lockBody = cxx_writer.writer_code.Code(lockCode)
            lockDecl = cxx_writer.writer_code.Method('lockRegs', lockBody, cxx_writer.writer_code.voidType, 'pu')
            classElements.append(lockDecl)
            # getUnlock
            unlockHazard = False
            for pipeStage in pipeline:
                if pipeStage.checkHazard:
                    unlockHazard = True
                if unlockHazard:
                    getUnlockCode = getToUnlockRegs(self, processor, pipeStage, True, False)
                    getUnlockBody = cxx_writer.writer_code.Code(getUnlockCode)
                    getUnlockDecl = cxx_writer.writer_code.Method('getUnlock_' + pipeStage.name, getUnlockBody, cxx_writer.writer_code.voidType, 'pu', [unlockQueueParam])
                    classElements.append(getUnlockDecl)

    replicateBody = cxx_writer.writer_code.Code('return new ' + self.name + '(' + baseInstrInitElement + ');')
    replicateDecl = cxx_writer.writer_code.Method('replicate', replicateBody, instructionType.makePointer(), 'pu', noException = True, const = True)
    classElements.append(replicateDecl)
    getIstructionNameBody = cxx_writer.writer_code.Code('return \"' + self.name + '\";')
    getIstructionNameDecl = cxx_writer.writer_code.Method('getInstructionName', getIstructionNameBody, cxx_writer.writer_code.stringType, 'pu', noException = True, const = True)
    classElements.append(getIstructionNameDecl)
    getIdBody = cxx_writer.writer_code.Code('return ' + str(self.id) + ';')
    getIdDecl = cxx_writer.writer_code.Method('getId', getIdBody, cxx_writer.writer_code.uintType, 'pu', noException = True, const = True)
    classElements.append(getIdDecl)

    # We need to create the attribute for the variables referenced by the non-constant parts of the instruction;
    # they are the bitCorrespondence variable of the machine code (they establish the correspondence with either registers
    # or aliases); they other remaining undefined parts of the instruction are normal integer variables.
    # Note, anyway, that I add the integer variable also for the parts of the instructions specified in
    # bitCorrespondence.
    setParamsCode = ''
    for name, correspondence in self.machineCode.bitCorrespondence.items() + self.bitCorrespondence.items():
        if model.startswith('acc'):
            for pipeStage in pipeline:
                classElements.append(cxx_writer.writer_code.Attribute(name + '_' + pipeStage.name, aliasType, 'pri'))
        else:
            classElements.append(cxx_writer.writer_code.Attribute(name, aliasType, 'pri'))
        classElements.append(cxx_writer.writer_code.Attribute(name + '_bit', cxx_writer.writer_code.uintType, 'pri'))
        mask = ''
        for i in range(0, self.machineCode.bitPos[name]):
            mask += '0'
        for i in range(0, self.machineCode.bitLen[name]):
            mask += '1'
        for i in range(0, self.machineCode.instrLen - self.machineCode.bitPos[name] - self.machineCode.bitLen[name]):
            mask += '0'
        shiftAmm = self.machineCode.instrLen - self.machineCode.bitPos[name] - self.machineCode.bitLen[name]
        setParamsCode += 'this->' + name + '_bit = (bitString & ' + hex(int(mask, 2)) + ')'
        if shiftAmm > 0:
            setParamsCode += ' >> ' + str(shiftAmm)
        setParamsCode += ';\n'
        #if processor.instructionCache:
            #updateMetodName = 'updateAlias'
        #else:
            #updateMetodName = 'directSetAlias'
        updateMetodName = 'directSetAlias'
        if correspondence[1]:
            if model.startswith('acc'):
                for pipeStage in pipeline:
                    setParamsCode += 'this->' + name + '_' + pipeStage.name + '.' + updateMetodName + '(this->' + correspondence[0] + '_' + pipeStage.name + '[' + str(correspondence[1]) + ' + this->' + name + '_bit]);\n'
            else:
                setParamsCode += 'this->' + name + '.' + updateMetodName + '(this->' + correspondence[0] + '[' + str(correspondence[1]) + ' + this->' + name + '_bit]);\n'
        else:
            if model.startswith('acc'):
                for pipeStage in pipeline:
                    setParamsCode += 'this->' + name + '_' + pipeStage.name + '.' + updateMetodName + '(this->' + correspondence[0] + '_' + pipeStage.name + '[this->' + name + '_bit]);\n'
            else:
                setParamsCode += 'this->' + name + '.' + updateMetodName + '(this->' + correspondence[0] + '[this->' + name + '_bit]);\n'
    # now I need to declare the fields for the variable parts of the
    # instruction
    for name, length in self.machineCode.bitFields:
        if name in self.machineBits.keys() + self.machineCode.bitValue.keys() + self.machineCode.bitCorrespondence.keys() + self.bitCorrespondence.keys():
            continue
        classElements.append(cxx_writer.writer_code.Attribute(name, cxx_writer.writer_code.uintType, 'pri'))
        mask = ''
        for i in range(0, self.machineCode.bitPos[name]):
            mask += '0'
        for i in range(0, self.machineCode.bitLen[name]):
            mask += '1'
        for i in range(0, self.machineCode.instrLen - self.machineCode.bitPos[name] - self.machineCode.bitLen[name]):
            mask += '0'
        shiftAmm = self.machineCode.instrLen - self.machineCode.bitPos[name] - self.machineCode.bitLen[name]
        setParamsCode += 'this->' + name + ' = (bitString & ' + hex(int(mask, 2)) + ')'
        if shiftAmm > 0:
            setParamsCode += ' >> ' + str(shiftAmm)
        setParamsCode += ';\n'
    setParamsBody = cxx_writer.writer_code.Code(setParamsCode)
    setparamsParam = cxx_writer.writer_code.Parameter('bitString', processor.bitSizes[1].makeRef().makeConst())
    setparamsDecl = cxx_writer.writer_code.Method('setParams', setParamsBody, cxx_writer.writer_code.voidType, 'pu', [setparamsParam], noException = True)
    classElements.append(setparamsDecl)

    # Here I declare the methods necessary to create the current instruction mnemonic given the current value of
    # the variable parts of the instruction
    getMnemonicCode = 'std::ostringstream oss (std::ostringstream::out);\n'
    for i in self.mnemonic:
        if type(i) == type(''):
            if i.startswith('%'):
                getMnemonicCode += 'oss << this->' + i[1:]
                if i[1:] in self.machineCode.bitCorrespondence.keys() + self.bitCorrespondence.keys():
                    getMnemonicCode += '_bit'
                getMnemonicCode += ';\n'
            else:
                getMnemonicCode += 'oss << "' + i + '";\n'
        else:
            # I have a switch
            if not i[0].startswith('%'):
                raise Exception('The first element of a multi-word mnemonic must start with %; error in instruction ' + self.name)
            getMnemonicCode += 'switch(this->' + i[0][1:]
            if i[0][1:] in self.machineCode.bitCorrespondence.keys() + self.bitCorrespondence.keys():
                getMnemonicCode += '_bit'
            getMnemonicCode += '){\n'
            for code, mnemValue in i[1].items():
                getMnemonicCode += 'case ' + str(code) + ':{\n'
                getMnemonicCode += 'oss << "' + mnemValue + '";\n'
                getMnemonicCode += 'break;}\n'
            getMnemonicCode += 'default:\nbreak;\n'
            getMnemonicCode += '}\n'
    getMnemonicCode += 'return oss.str();'
    getMnemonicBody = cxx_writer.writer_code.Code(getMnemonicCode)
    getMnemonicBody.addInclude('sstream')
    getMnemonicDecl = cxx_writer.writer_code.Method('getMnemonic', getMnemonicBody, cxx_writer.writer_code.stringType, 'pu', noException = True, const = True)
    classElements.append(getMnemonicDecl)

    # Now I declare the instruction variables
    for var in self.variables:
        if not var.name in behVars:
            classElements.append(cxx_writer.writer_code.Attribute(var.name, var.varType, 'pro',  var.static))

    # Finally now I have to override the basic new operator in
    # order to speed up memory allocation (***** Commented since it does not give any speedup ******)
    #num_allocated = processor.alloc_buffer_size*self.frequency
    #poolDecl = cxx_writer.writer_code.Variable(self.name + '_pool[' + str(num_allocated) + '*sizeof(' + self.name + ')]', cxx_writer.writer_code.ucharType, namespaces = [namespace])
    #operatorNewCode = """
    #if(""" + self.name + """::allocated < """ + str(num_allocated) + """){
        #""" + self.name + """::allocated++;
        #return """ + self.name + """_pool + (""" + self.name + """::allocated - 1)*sizeof(""" + self.name + """);
    #}
    #else{
        #void * newMem = ::malloc(bytesToAlloc);
        #if(newMem == NULL)
            #throw std::bad_alloc();
        #return newMem;
    #}
    #"""
    #operatorNewBody =  cxx_writer.writer_code.Code(operatorNewCode)
    #operatorNewBody.addInclude('cstddef')
    #operatorNewBody.addInclude('cstdlib')
    #operatorNewBody.addInclude('new')
    #operatorNewParams = [cxx_writer.writer_code.Parameter('bytesToAlloc', cxx_writer.writer_code.Type('std::size_t'))]
    #operatorNewDecl = cxx_writer.writer_code.MemberOperator('new', operatorNewBody, cxx_writer.writer_code.voidPtrType, 'pu', operatorNewParams)
    #classElements.append(operatorNewDecl)
    #operatorDelCode = """
        #if(m != NULL && (m < """ + self.name + """_pool || m > (""" + self.name + """_pool + """ + str(num_allocated - 1) + """*sizeof(""" + self.name + """)))){
            #::free(m);
        #}
    #"""
    #operatorDelBody =  cxx_writer.writer_code.Code(operatorDelCode)
    #operatorDelParams = [cxx_writer.writer_code.Parameter('m', cxx_writer.writer_code.voidPtrType)]
    #operatorDelDecl = cxx_writer.writer_code.MemberOperator('delete', operatorDelBody, cxx_writer.writer_code.voidType, 'pu', operatorDelParams)
    #classElements.append(operatorDelDecl)
    #num_allocatedAttribute = cxx_writer.writer_code.Attribute('allocated', cxx_writer.writer_code.uintType, 'pri', initValue = '0', static = True)
    #classElements.append(num_allocatedAttribute)

    ########################## TODO: to eliminate, only for statistics ####################
    #out_poolAttribute = cxx_writer.writer_code.Attribute('allocatedOut', cxx_writer.writer_code.uintType, 'pri', static = True)
    #classElements.append(out_poolAttribute)
    #returnStatsDecl = cxx_writer.writer_code.Method('getMyAllocCount', cxx_writer.writer_code.Code('return ' + self.name + '::allocated;'), cxx_writer.writer_code.uintType, 'pu')
    #classElements.append(returnStatsDecl)
    #returnStatsDecl = cxx_writer.writer_code.Method('getStdAllocCount', cxx_writer.writer_code.Code('return ' + self.name + '::allocatedOut;'), cxx_writer.writer_code.uintType, 'pu')
    #classElements.append(returnStatsDecl)
    ########################################################################################

    # Now I have to declare the constructor
    from procWriter import baseInstrInitElement
    publicConstr = cxx_writer.writer_code.Constructor(emptyBody, 'pu', baseInstrConstrParams, constrInitList)
    instructionDecl = cxx_writer.writer_code.ClassDeclaration(self.name, classElements, superclasses = baseClasses, namespaces = [namespace])
    instructionDecl.addConstructor(publicConstr)
    publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    instructionDecl.addDestructor(publicDestr)
    #return [poolDecl, instructionDecl] *** Again removed, related to the instruction pre-allocation
    return [instructionDecl]

def getCPPInstrTest(self, processor, model, trace, combinedTrace, namespace = ''):
    # Returns the code testing the current instruction: note that a test
    # consists in setting the instruction variables, performing the instruction
    # behavior and then comparing the registers with what we expect.
    archElemsDeclStr = ''
    baseInitElement = '('
    destrDecls = ''
    from procWriter import resourceType
    for reg in processor.regs:
        archElemsDeclStr += namespace + '::' + str(resourceType[reg.name]) + ' ' + reg.name + ';\n'
        baseInitElement += reg.name + ', '
    for regB in processor.regBanks:
        if (regB.constValue and len(regB.constValue) < regB.numRegs)  or (regB.delay and len(regB.delay) < regB.numRegs):
            archElemsDeclStr += str(resourceType[regB.name]) + ' ' + regB.name + '(' + str(regB.numRegs) + ');\n'
            for i in range(0, regB.numRegs):
                if regB.constValue.has_key(i) or regB.delay.has_key(i):
                    archElemsDeclStr += regB.name + '.setNewRegister(' + str(i) + ', new ' + str(resourceType[regB.name + '[' + str(i) + ']']) + '());\n'
                else:
                    archElemsDeclStr += regB.name + '.setNewRegister(' + str(i) + ', new ' + str(resourceType[regB.name + '_baseType']) + '());\n'
        else:
            archElemsDeclStr += str(resourceType[regB.name]) + ' ' + regB.name + ' = new ' + str(resourceType[regB.name].makeNormal()) + '[' + str(regB.numRegs) + '];\n'
            destrDecls += 'delete [] ' + regB.name + ';\n'
        baseInitElement += regB.name + ', '
    for alias in processor.aliasRegs:
        archElemsDeclStr += namespace + '::' + str(resourceType[alias.name]) + ' ' + alias.name + ';\n'
        baseInitElement += alias.name + ', '
    for aliasB in processor.aliasRegBanks:
        archElemsDeclStr += namespace + '::' + str(resourceType[aliasB.name].makePointer()) + ' ' + aliasB.name + ' = new ' + namespace + '::' + str(resourceType[aliasB.name]) + '[' + str(aliasB.numRegs) + '];\n'
        baseInitElement += aliasB.name + ', '
        destrDecls += 'delete [] ' + aliasB.name + ';\n'
    memAliasInit = ''
    for alias in processor.memAlias:
        memAliasInit += ', ' + alias.alias

    if (trace or (processor.memory and processor.memory[2])) and not processor.systemc:
        archElemsDeclStr += 'unsigned int totalCycles;\n'
    if processor.memory:
        memDebugInit = ''
        if processor.memory[2]:
            memDebugInit += ', totalCycles'
        if processor.memory[3]:
            memDebugInit += ', ' + processor.memory[3]
        archElemsDeclStr += namespace + '::LocalMemory ' + processor.memory[0] + '(' + str(processor.memory[1]) + memDebugInit + memAliasInit + ');\n'
        baseInitElement += processor.memory[0] + ', '
    # Note how I declare local memories even for TLM ports. I use 1MB as default dimension
    for tlmPorts in processor.tlmPorts.keys():
        archElemsDeclStr += namespace + '::LocalMemory ' + tlmPorts + '(' + str(1024*1024) + memAliasInit + ');\n'
        baseInitElement += tlmPorts + ', '
    # Now I declare the PIN stubs for the outgoing PIN ports
    # and alts themselves
    outPinPorts = []
    for pinPort in processor.pins:
        if not pinPort.inbound:
            outPinPorts.append(pinPort.name)
            pinPortTypeName = 'Pin'
            if pinPort.systemc:
                pinPortTypeName += 'SysC_'
            else:
                pinPortTypeName += 'TLM_'
            if pinPort.inbound:
                pinPortTypeName += 'in_'
            else:
                pinPortTypeName += 'out_'
            pinPortTypeName += str(pinPort.portWidth)
            archElemsDeclStr += namespace + '::' + pinPortTypeName + ' ' + pinPort.name + '(sc_core::sc_gen_unique_name(\"' + pinPort.name + '_PIN\"));\n'
            archElemsDeclStr += 'PINTarget<' + str(pinPort.portWidth) + '> ' + pinPort.name + '_target(sc_core::sc_gen_unique_name(\"' + pinPort.name + '_PIN\"));\n'
            archElemsDeclStr += pinPort.name + '.initSocket.bind(' + pinPort.name + '_target.socket);\n'
            baseInitElement += pinPort.name + ', '

    if trace and not processor.systemc:
        baseInitElement += 'totalCycles, '
    baseInitElement = baseInitElement[:-2] + ')'
    # Now we perform the alias initialization; note that they need to be initialized according to the initialization graph
    # (there might be dependences among the aliases)
    aliasInit = ''
    import networkx as NX
    from procWriter import aliasGraph
    from processor import extractRegInterval
    orderedNodes = NX.topological_sort(aliasGraph)
    for alias in orderedNodes:
        if alias == 'stop':
            continue
        if isinstance(alias.initAlias, type('')):
            index = extractRegInterval(alias.initAlias)
            if index:
                curIndex = index[0]
                try:
                    for i in range(0, alias.numRegs):
                        aliasInit += alias.name + '[' + str(i) + '].updateAlias(' + alias.initAlias[:alias.initAlias.find('[')] + '[' + str(curIndex) + ']);\n'
                        curIndex += 1
                except AttributeError:
                    aliasInit += alias.name + '.updateAlias(' + alias.initAlias[:alias.initAlias.find('[')] + '[' + str(curIndex) + '], ' + str(alias.offset) + ');\n'
            else:
                aliasInit += alias.name + '.updateAlias(' + alias.initAlias + ', ' + str(alias.offset) + ');\n'
        else:
            curIndex = 0
            for curAlias in alias.initAlias:
                index = extractRegInterval(curAlias)
                if index:
                    for curRange in range(index[0], index[1] + 1):
                        aliasInit += alias.name + '[' + str(curIndex) + '].updateAlias(' + curAlias[:curAlias.find('[')] + '[' + str(curRange) + ']);\n'
                        curIndex += 1
                else:
                    aliasInit += alias.name + '[' + str(curIndex) + '].updateAlias(' + curAlias + ');\n'
                    curIndex += 1
    tests = []
    for test in self.tests:
        # First of all I create the instance of the instruction and of all the
        # processor elements
        code = archElemsDeclStr + '\n' + aliasInit + '\n'
        code += self.name + ' toTest' + baseInitElement + ';\n'
        # Now I set the value of the instruction fields
        instrCode = ['0' for i in range(0, self.machineCode.instrLen)]
        for name, elemValue in test[0].items():
            if self.machineCode.bitLen.has_key(name):
                curBitCode = toBinStr(elemValue, self.machineCode.bitLen[name])
                curBitCode.reverse()
                if len(curBitCode) > self.machineCode.bitLen[name]:
                    raise Exception('Value ' + hex(elemValue) + ' set for field ' + name + ' in test of instruction ' + self.name + ' cannot be represented in ' + str(self.machineCode.bitLen[name]) + ' bits')
                for i in range(0, len(curBitCode)):
                    instrCode[self.machineCode.bitLen[name] + self.machineCode.bitPos[name] - i -1] = curBitCode[i]
            else:
                raise Exception('Field ' + name + ' in test of instruction ' + self.name + ' is not present in the machine code of the instruction')
        for resource, value in test[1].items():
            # I set the initial value of the global resources
            brackIndex = resource.find('[')
            memories = processor.tlmPorts.keys()
            if processor.memory:
                memories.append(processor.memory[0])
            if brackIndex > 0 and resource[:brackIndex] in memories:
                try:
                    code += resource[:brackIndex] + '.write_word_dbg(' + hex(int(resource[brackIndex + 1:-1])) + ', ' + hex(value) + ');\n'
                except ValueError:
                    code += resource[:brackIndex] + '.write_word_dbg(' + hex(int(resource[brackIndex + 1:-1], 16)) + ', ' + hex(value) + ');\n'
            else:
                code += resource + '.immediateWrite(' + hex(value) + ');\n'
        code += 'toTest.setParams(' + hex(int(''.join(instrCode), 2)) + ');\n'
        code += 'try{\n'
        code += 'toTest.behavior();'
        code += '\n}\ncatch(annull_exception &etc){\n}\n\n'
        for resource, value in test[2].items():
            # I check the value of the listed resources to make sure that the
            # computation executed correctly
            code += 'BOOST_CHECK_EQUAL('
            brackIndex = resource.find('[')
            memories = processor.tlmPorts.keys()
            if processor.memory:
                memories.append(processor.memory[0])
            if brackIndex > 0 and resource[:brackIndex] in memories:
                try:
                    code += resource[:brackIndex] + '.read_word_dbg(' + hex(int(resource[brackIndex + 1:-1])) + ')'
                except ValueError:
                    code += resource[:brackIndex] + '.read_word_dbg(' + hex(int(resource[brackIndex + 1:-1], 16)) + ')'
            elif brackIndex > 0 and resource[:brackIndex] in outPinPorts:
                try:
                    code += resource[:brackIndex] + '_target.readPIN(' + hex(int(resource[brackIndex + 1:-1])) + ')'
                except ValueError:
                    code += resource[:brackIndex] + '_target.readPIN(' + hex(int(resource[brackIndex + 1:-1], 16)) + ')'
            else:
                code += resource + '.readNewValue()'
            code += ', (' + str(processor.bitSizes[1]) + ')' + hex(value) + ');\n\n'
        code += destrDecls
        curTest = cxx_writer.writer_code.Code(code)
        wariningDisableCode = '#ifdef _WIN32\n#pragma warning( disable : 4101 )\n#endif\n'
        includeUnprotectedCode = '#define private public\n#define protected public\n#include \"instructions.hpp\"\n#include \"registers.hpp\"\n#include \"memory.hpp\"\n#undef private\n#undef protected\n'
        curTest.addInclude(['boost/test/test_tools.hpp', 'customExceptions.hpp', wariningDisableCode, includeUnprotectedCode, 'alias.hpp'])
        curTestFunction = cxx_writer.writer_code.Function(self.name + '_' + str(len(tests)), curTest, cxx_writer.writer_code.voidType)
        from procWriter import testNames
        testNames.append(self.name + '_' + str(len(tests)))
        tests.append(curTestFunction)
    return tests

def getCPPClasses(self, processor, model, trace, combinedTrace, namespace):
    # I go over each instruction and print the class representing it
    memoryType = cxx_writer.writer_code.Type('MemoryInterface', 'memory.hpp')
    registerType = cxx_writer.writer_code.Type('Register')
    unlockQueueType = cxx_writer.writer_code.TemplateType('std::map', ['unsigned int', cxx_writer.writer_code.TemplateType('std::vector', [registerType.makePointer()], 'vector')], 'map')

    classes = []
    # Here I add the define code, definig the type of the current model
    defString = '#define ' + model[:-2].upper() + '_MODEL\n'
    defString += '#define ' + model[-2:].upper() + '_IF\n'
    defCode = cxx_writer.writer_code.Define(defString)
    classes.append(defCode)
    # Now I add the custon definitions
    for i in self.defines:
        classes.append(cxx_writer.writer_code.Define(i + '\n'))

    # First of all I create the base instruction type: note that it contains references
    # to the architectural elements
    instructionType = cxx_writer.writer_code.Type('Instruction')
    instructionElements = []
    emptyBody = cxx_writer.writer_code.Code('')
    if not model.startswith('acc'):
        behaviorDecl = cxx_writer.writer_code.Method('behavior', emptyBody, cxx_writer.writer_code.uintType, 'pu', pure = True)
        instructionElements.append(behaviorDecl)
    else:
        unlockQueueParam = cxx_writer.writer_code.Parameter('unlockQueue', unlockQueueType.makeRef())
        for pipeStage in processor.pipes:
            behaviorDecl = cxx_writer.writer_code.Method('behavior_' + pipeStage.name, emptyBody, cxx_writer.writer_code.uintType, 'pu', [unlockQueueParam], pure = True)
            instructionElements.append(behaviorDecl)
    replicateDecl = cxx_writer.writer_code.Method('replicate', emptyBody, instructionType.makePointer(), 'pu', pure = True, noException = True, const = True)
    instructionElements.append(replicateDecl)
    setparamsParam = cxx_writer.writer_code.Parameter('bitString', processor.bitSizes[1].makeRef().makeConst())
    setparamsDecl = cxx_writer.writer_code.Method('setParams', emptyBody, cxx_writer.writer_code.voidType, 'pu', [setparamsParam], pure = True, noException = True)
    instructionElements.append(setparamsDecl)

    ########################## TODO: to eliminate, only for statistics ####################
    #returnStatsDecl = cxx_writer.writer_code.Method('getMyAllocCount', emptyBody, cxx_writer.writer_code.uintType, 'pu', virtual = True)
    #instructionElements.append(returnStatsDecl)
    #returnStatsDecl = cxx_writer.writer_code.Method('getStdAllocCount', emptyBody, cxx_writer.writer_code.uintType, 'pu', virtual = True)
    #instructionElements.append(returnStatsDecl)
    ########################################################################################

    if model.startswith('acc'):
        # Now I have to add the code for checking data hazards
        hasCheckHazard = False
        hasWb = False
        for pipeStage in processor.pipes:
            if pipeStage.checkHazard:
                if processor.pipes.index(pipeStage) + 1 < len(processor.pipes):
                    if not processor.pipes[processor.pipes.index(pipeStage) + 1].wb:
                        hasCheckHazard = True
            if pipeStage.wb:
                if processor.pipes.index(pipeStage) - 1 >= 0:
                    if not processor.pipes[processor.pipes.index(pipeStage) - 1].checkHazard:
                        hasWb = True
        if hasCheckHazard:
            checkHazardDecl = cxx_writer.writer_code.Method('checkHazard', emptyBody, cxx_writer.writer_code.boolType, 'pu', pure = True)
            instructionElements.append(checkHazardDecl)
            lockDecl = cxx_writer.writer_code.Method('lockRegs', emptyBody, cxx_writer.writer_code.voidType, 'pu', pure = True)
            instructionElements.append(lockDecl)
            unlockHazard = False
            for pipeStage in processor.pipes:
                if pipeStage.checkHazard:
                    unlockHazard = True
                if unlockHazard:
                    getUnlockDecl = cxx_writer.writer_code.Method('getUnlock_' + pipeStage.name, emptyBody, cxx_writer.writer_code.voidType, 'pu', [unlockQueueParam], pure = True)
                    instructionElements.append(getUnlockDecl)

    if trace:
        if not combinedTrace:
            traceStage = processor.pipes[-1]
        else:
            for pipeStage in processor.pipes:
                if pipeStage.checkTools:
                    traceStage = pipeStage
                    break

        # I have to print the value of all the registers in the processor
        printTraceCode = ''
        if model.startswith('acc'):
            # now I have to take all the resources and create a define which
            # renames such resources so that their usage can be transparent
            # to the developer
            for reg in processor.regs:
                printTraceCode += '#define ' + reg.name + ' ' + reg.name + '_' + traceStage.name + '\n'
            for regB in processor.regBanks:
                printTraceCode += '#define ' + regB.name + ' ' + regB.name + '_' + traceStage.name + '\n'
            for alias in processor.aliasRegs:
                printTraceCode += '#define ' + alias.name + ' ' + alias.name + '_' + traceStage.name + '\n'
            for aliasB in processor.aliasRegBanks:
                printTraceCode += '#define ' + aliasB.name + ' ' + aliasB.name + '_' + traceStage.name + '\n'
            printTraceCode += '\n'

        if not combinedTrace:
            if not processor.systemc and not model.startswith('acc') and not model.endswith('AT'):
                printTraceCode += 'std::cerr << \"Simulated time \" << std::dec << this->totalCycles << std::endl;\n'
            else:
                printTraceCode += 'std::cerr << \"Simulated time \" << sc_time_stamp().to_double() << std::endl;\n'
        printTraceCode += 'std::cerr << \"Instruction: \" << this->getInstructionName() << std::endl;\n'
        printTraceCode += 'std::cerr << \"Mnemonic: \" << this->getMnemonic() << std::endl;\n'
        if self.traceRegs:
            bankNames = [i.name for i in processor.regBanks + processor.aliasRegBanks]
            for reg in self.traceRegs:
                if reg.name in bankNames:
                    printTraceCode += 'for(int regNum = 0; regNum < ' + str(reg.numRegs) + '; regNum++){\n'
                    printTraceCode += 'std::cerr << \"' + reg.name + '[\" << std::dec << regNum << \"] = \" << std::hex << std::showbase << this->' + reg.name + '[regNum] << std::endl;\n}\n'
                else:
                    printTraceCode += 'std::cerr << \"' + reg.name + ' = \" << std::hex << std::showbase << this->' + reg.name + ' << std::endl;\n'
        else:
            for reg in processor.regs:
                printTraceCode += 'std::cerr << \"' + reg.name + ' = \" << std::hex << std::showbase << this->' + reg.name + ' << std::endl;\n'
            for regB in processor.regBanks:
                printTraceCode += 'for(int regNum = 0; regNum < ' + str(regB.numRegs) + '; regNum++){\n'
                printTraceCode += 'std::cerr << \"' + regB.name + '[\" << std::dec << regNum << \"] = \" << std::hex << std::showbase << this->' + regB.name + '[regNum] << std::endl;\n}\n'
        printTraceCode += 'std::cerr << std::endl;\n'
        if model.startswith('acc'):
            # now I have to take all the resources and create a define which
            # renames such resources so that their usage can be transparent
            # to the developer
            for reg in processor.regs:
                printTraceCode += '#undef ' + reg.name + '\n'
            for regB in processor.regBanks:
                printTraceCode += '#undef ' + regB.name + '\n'
            for alias in processor.aliasRegs:
                printTraceCode += '#undef ' + alias.name + '\n'
            for aliasB in processor.aliasRegBanks:
                printTraceCode += '#undef ' + aliasB.name + '\n'
        printTraceBody = cxx_writer.writer_code.Code(printTraceCode)
        printTraceDecl = cxx_writer.writer_code.Method('printTrace', printTraceBody, cxx_writer.writer_code.voidType, 'pu')
        instructionElements.append(printTraceDecl)

    getIstructionNameDecl = cxx_writer.writer_code.Method('getInstructionName', emptyBody, cxx_writer.writer_code.stringType, 'pu', noException = True, const = True, pure = True)
    instructionElements.append(getIstructionNameDecl)
    getMnemonicDecl = cxx_writer.writer_code.Method('getMnemonic', emptyBody, cxx_writer.writer_code.stringType, 'pu', noException = True, const = True, pure = True)
    instructionElements.append(getMnemonicDecl)
    getIdDecl = cxx_writer.writer_code.Method('getId', emptyBody, cxx_writer.writer_code.uintType, 'pu', noException = True, const = True, pure = True)
    instructionElements.append(getIdDecl)

    # Note how the annull operation stops the execution of the current operation
    annullCode = 'throw annull_exception();'
    annullBody = cxx_writer.writer_code.Code(annullCode)
    annullBody.addInclude('customExceptions.hpp')
    annullDecl = cxx_writer.writer_code.Method('annull', annullBody, cxx_writer.writer_code.voidType, 'pu', inline = True)
    instructionElements.append(annullDecl)

    if not model.startswith('acc'):
        flushCode = ''
    else:
        flushCode = 'this->flushPipeline = true;'
    flushBody = cxx_writer.writer_code.Code(flushCode)
    flushDecl = cxx_writer.writer_code.Method('flush', flushBody, cxx_writer.writer_code.voidType, 'pu', inline = True)
    instructionElements.append(flushDecl)

    stallParam = cxx_writer.writer_code.Parameter('numCycles', processor.bitSizes[1].makeRef().makeConst())
    if not model.startswith('acc'):
        stallBody = cxx_writer.writer_code.Code('this->totalInstrCycles += numCycles;')
    else:
        stallBody = cxx_writer.writer_code.Code('this->stageCycles += numCycles;')
    stallDecl = cxx_writer.writer_code.Method('stall', stallBody, cxx_writer.writer_code.voidType, 'pu', [stallParam], inline = True)
    instructionElements.append(stallDecl)
    # we now have to check if there is a non-inline behavior common to all instructions:
    # in this case I declare it here in the base instruction class
    global alreadyDeclared
    alreadyDeclared = []
    global baseBehaviors
    baseBehaviors = []
    if not model.startswith('acc'):
        for instr in self.instructions.values():
            for behaviors in instr.postbehaviors.values() + instr.prebehaviors.values():
                for beh in behaviors:
                    if beh.numUsed == len(self.instructions) and not beh.name in alreadyDeclared:
                        # This behavior is present in all the instructions: I declare it in
                        # the base instruction class
                        alreadyDeclared.append(beh.name)
                        instructionElements.append(beh.getCppOperation(True))
                        baseBehaviors.append(beh.name)
    # Ok, now I add the generic helper methods and operations
    for helpOp in self.helperOps + [self.beginOp, self.endOp]:
        if helpOp and not helpOp.name in alreadyDeclared:
            instructionElements.append(helpOp.getCppOperation(True))
    for helpMeth in self.methods:
        if helpMeth:
            instructionElements.append(helpMeth.getCppMethod(model, processor))
    # Now create references to the architectural elements contained in the processor and
    # initialize them through the constructor
    initElements = []
    global baseInstrConstrParams
    baseInstrConstrParams = []
    baseInitElement = 'Instruction('
    from procWriter import resourceType
    if not model.startswith('acc'):
        for reg in processor.regs:
            attribute = cxx_writer.writer_code.Attribute(reg.name, resourceType[reg.name].makeRef(), 'pro')
            baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(reg.name, resourceType[reg.name].makeRef()))
            initElements.append(reg.name + '(' + reg.name + ')')
            baseInitElement += reg.name + ', '
            instructionElements.append(attribute)
        for regB in processor.regBanks:
            attribute = cxx_writer.writer_code.Attribute(regB.name, resourceType[regB.name].makeRef(), 'pro')
            baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(regB.name, resourceType[regB.name].makeRef()))
            initElements.append(regB.name + '(' + regB.name + ')')
            baseInitElement += regB.name + ', '
            instructionElements.append(attribute)
        for alias in processor.aliasRegs:
            attribute = cxx_writer.writer_code.Attribute(alias.name, resourceType[alias.name].makeRef(), 'pro')
            baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(alias.name, resourceType[alias.name].makeRef()))
            initElements.append(alias.name + '(' + alias.name + ')')
            baseInitElement += alias.name + ', '
            instructionElements.append(attribute)
        for aliasB in processor.aliasRegBanks:
            attribute = cxx_writer.writer_code.Attribute(aliasB.name, resourceType[aliasB.name].makePointer().makeRef(), 'pro')
            baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(aliasB.name, resourceType[aliasB.name].makePointer().makeRef()))
            initElements.append(aliasB.name + '(' + aliasB.name + ')')
            baseInitElement += aliasB.name + ', '
            instructionElements.append(attribute)
    else:
        for pipeStage in processor.pipes:
            for reg in processor.regs:
                attribute = cxx_writer.writer_code.Attribute(reg.name + '_' + pipeStage.name, resourceType[reg.name].makeRef(), 'pu')
                baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(reg.name + '_' + pipeStage.name, resourceType[reg.name].makeRef()))
                initElements.append(reg.name + '_' + pipeStage.name + '(' + reg.name + '_' + pipeStage.name + ')')
                baseInitElement += reg.name + '_' + pipeStage.name + ', '
                instructionElements.append(attribute)
            for regB in processor.regBanks:
                attribute = cxx_writer.writer_code.Attribute(regB.name + '_' + pipeStage.name, resourceType[regB.name].makeRef(), 'pu')
                baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(regB.name + '_' + pipeStage.name, resourceType[regB.name].makeRef()))
                initElements.append(regB.name + '_' + pipeStage.name + '(' + regB.name + '_' + pipeStage.name + ')')
                baseInitElement += regB.name + '_' + pipeStage.name + ', '
                instructionElements.append(attribute)
            for alias in processor.aliasRegs:
                attribute = cxx_writer.writer_code.Attribute(alias.name + '_' + pipeStage.name, resourceType[alias.name].makeRef(), 'pu')
                baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(alias.name + '_' + pipeStage.name, resourceType[alias.name].makeRef()))
                initElements.append(alias.name + '_' + pipeStage.name + '(' + alias.name + '_' + pipeStage.name + ')')
                baseInitElement += alias.name + '_' + pipeStage.name + ', '
                instructionElements.append(attribute)
            for aliasB in processor.aliasRegBanks:
                attribute = cxx_writer.writer_code.Attribute(aliasB.name + '_' + pipeStage.name, resourceType[aliasB.name].makePointer().makeRef(), 'pu')
                baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(aliasB.name + '_' + pipeStage.name, resourceType[aliasB.name].makePointer().makeRef()))
                initElements.append(aliasB.name + '_' + pipeStage.name + '(' + aliasB.name + '_' + pipeStage.name + ')')
                baseInitElement += aliasB.name + '_' + pipeStage.name + ', '
                instructionElements.append(attribute)
    if processor.memory:
        attribute = cxx_writer.writer_code.Attribute(processor.memory[0], cxx_writer.writer_code.Type('LocalMemory', 'memory.hpp').makeRef(), 'pro')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(processor.memory[0], cxx_writer.writer_code.Type('LocalMemory', 'memory.hpp').makeRef()))
        initElements.append(processor.memory[0] + '(' + processor.memory[0] + ')')
        baseInitElement += processor.memory[0] + ', '
        instructionElements.append(attribute)
    for tlmPorts in processor.tlmPorts.keys():
        attribute = cxx_writer.writer_code.Attribute(tlmPorts, cxx_writer.writer_code.Type('TLMMemory', 'externalPorts.hpp').makeRef(), 'pro')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(tlmPorts, cxx_writer.writer_code.Type('TLMMemory', 'externalPorts.hpp').makeRef()))
        initElements.append(tlmPorts + '(' + tlmPorts + ')')
        baseInitElement += tlmPorts + ', '
        instructionElements.append(attribute)
    for pinPort in processor.pins:
        if not pinPort.inbound:
            pinPortName = 'Pin'
            if pinPort.systemc:
                pinPortName += 'SysC_'
            else:
                pinPortName += 'TLM_'
            if pinPort.inbound:
                pinPortName += 'in_'
            else:
                pinPortName += 'out_'
            pinPortType = cxx_writer.writer_code.Type(pinPortName + str(pinPort.portWidth), 'externalPins.hpp')
            attribute = cxx_writer.writer_code.Attribute(pinPort.name, pinPortType.makeRef(), 'pro')
            baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(pinPort.name, pinPortType.makeRef()))
            initElements.append(pinPort.name + '(' + pinPort.name + ')')
            baseInitElement += pinPort.name + ', '
            instructionElements.append(attribute)
    if trace and not processor.systemc and not model.startswith('acc'):
        attribute = cxx_writer.writer_code.Attribute('totalCycles', cxx_writer.writer_code.uintType.makeRef(), 'pro')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter('totalCycles', cxx_writer.writer_code.uintType.makeRef()))
        initElements.append('totalCycles(totalCycles)')
        baseInitElement += 'totalCycles, '
        instructionElements.append(attribute)
    baseInitElement = baseInitElement[:-2]
    baseInitElement += ')'
    if not model.startswith('acc'):
        instructionElements.append(cxx_writer.writer_code.Attribute('totalInstrCycles', cxx_writer.writer_code.uintType, 'pu'))
        constrBody = 'this->totalInstrCycles = 0;'
    else:
        instructionElements.append(cxx_writer.writer_code.Attribute('flushPipeline', cxx_writer.writer_code.boolType, 'pu'))
        instructionElements.append(cxx_writer.writer_code.Attribute('stageCycles', cxx_writer.writer_code.uintType, 'pro'))
        constrBody = 'this->stageCycles = 0;\nthis->flushPipeline = false;'

    for constant in self.constants:
        instructionElements.append(cxx_writer.writer_code.Attribute(constant[1], constant[0].makeConst(), 'pro'))
        initElements.append(constant[1] + '(' + str(constant[2]) + ')')

    publicConstr = cxx_writer.writer_code.Constructor(cxx_writer.writer_code.Code(constrBody), 'pu', baseInstrConstrParams, initElements)
    instructionBaseType = cxx_writer.writer_code.Type('InstructionBase', 'instructionBase.hpp')
    instructionDecl = cxx_writer.writer_code.ClassDeclaration('Instruction', instructionElements, [instructionBaseType], namespaces = [namespace])
    instructionDecl.addConstructor(publicConstr)
    publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    instructionDecl.addDestructor(publicDestr)
    classes.append(instructionDecl)

    # we now have to check all the operation and the behaviors of the instructions and create
    # the classes for each shared non-inline behavior
    global behClass
    behClass = {}
    if not model.startswith('acc'):
        for instr in self.instructions.values():
            for behaviors in instr.postbehaviors.values() + instr.prebehaviors.values():
                for beh in behaviors:
                    if not behClass.has_key(beh.name) and beh.inline and beh.numUsed > 1 and not beh.name in alreadyDeclared:
                        behClass[beh.name] = beh.getCppOpClass(namespace)
                        classes.append(behClass[beh.name])

    #########################################################################
    ############### Now I print the INVALID instruction #####################

    invalidInstrElements = []
    behaviorReturnBody = cxx_writer.writer_code.Code('return 0;')
    codeString = 'THROW_EXCEPTION(\"Unknown Instruction at PC: \" << this->' + processor.fetchReg[0]
    if model.startswith('func'):
        if processor.fetchReg[1] < 0:
            codeString += str(processor.fetchReg[1])
        else:
            codeString += '+' + str(processor.fetchReg[1])
    codeString += ');\nreturn 0;'
    behaviorBody = cxx_writer.writer_code.Code(codeString)
    if model.startswith('acc'):
        for pipeStage in processor.pipes:
            if pipeStage.checkUnknown:
                behaviorBody.prependCode('#define ' + processor.fetchReg[0] + ' ' + processor.fetchReg[0] + '_' + pipeStage.name + '\n')
                behaviorBody.appendCode('\n#undef ' + processor.fetchReg[0])
                behaviorDecl = cxx_writer.writer_code.Method('behavior_' + pipeStage.name, behaviorBody, cxx_writer.writer_code.uintType, 'pu', [unlockQueueParam])
            else:
                behaviorDecl = cxx_writer.writer_code.Method('behavior_' + pipeStage.name, behaviorReturnBody, cxx_writer.writer_code.uintType, 'pu', [unlockQueueParam])
            invalidInstrElements.append(behaviorDecl)
    else:
        behaviorDecl = cxx_writer.writer_code.Method('behavior', behaviorBody, cxx_writer.writer_code.uintType, 'pu')
        invalidInstrElements.append(behaviorDecl)
    from procWriter import baseInstrInitElement
    replicateBody = cxx_writer.writer_code.Code('return new InvalidInstr(' + baseInstrInitElement + ');')
    replicateDecl = cxx_writer.writer_code.Method('replicate', replicateBody, instructionType.makePointer(), 'pu', noException = True, const = True)
    invalidInstrElements.append(replicateDecl)
    setparamsParam = cxx_writer.writer_code.Parameter('bitString', processor.bitSizes[1].makeRef().makeConst())
    setparamsDecl = cxx_writer.writer_code.Method('setParams', emptyBody, cxx_writer.writer_code.voidType, 'pu', [setparamsParam], noException = True)
    invalidInstrElements.append(setparamsDecl)
    getIstructionNameBody = cxx_writer.writer_code.Code('return \"InvalidInstruction\";')
    getIstructionNameDecl = cxx_writer.writer_code.Method('getInstructionName', getIstructionNameBody, cxx_writer.writer_code.stringType, 'pu', noException = True, const = True)
    invalidInstrElements.append(getIstructionNameDecl)
    getMnemonicBody = cxx_writer.writer_code.Code('return \"invalid\";')
    getMnemonicDecl = cxx_writer.writer_code.Method('getMnemonic', getMnemonicBody, cxx_writer.writer_code.stringType, 'pu', noException = True, const = True)
    invalidInstrElements.append(getMnemonicDecl)
    getIdBody = cxx_writer.writer_code.Code('return ' + str(len(self.instructions)) + ';')
    getIdDecl = cxx_writer.writer_code.Method('getId', getIdBody, cxx_writer.writer_code.uintType, 'pu', noException = True, const = True)
    invalidInstrElements.append(getIdDecl)
    if model.startswith('acc'):
        if hasCheckHazard:
            checkHazardDecl = cxx_writer.writer_code.Method('checkHazard', cxx_writer.writer_code.Code('return false;'), cxx_writer.writer_code.boolType, 'pu')
            invalidInstrElements.append(checkHazardDecl)
            lockDecl = cxx_writer.writer_code.Method('lockRegs', emptyBody, cxx_writer.writer_code.voidType, 'pu')
            invalidInstrElements.append(lockDecl)
            unlockHazard = False
            for pipeStage in processor.pipes:
                if pipeStage.checkHazard:
                    unlockHazard = True
                if unlockHazard:
                    getUnlockDecl = cxx_writer.writer_code.Method('getUnlock_' + pipeStage.name, emptyBody, cxx_writer.writer_code.voidType, 'pu', [unlockQueueParam])
                    invalidInstrElements.append(getUnlockDecl)
    from procWriter import baseInstrInitElement
    publicConstr = cxx_writer.writer_code.Constructor(emptyBody, 'pu', baseInstrConstrParams, ['Instruction(' + baseInstrInitElement + ')'])
    invalidInstrDecl = cxx_writer.writer_code.ClassDeclaration('InvalidInstr', invalidInstrElements, [instructionDecl.getType()], namespaces = [namespace])
    invalidInstrDecl.addConstructor(publicConstr)
    publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    invalidInstrDecl.addDestructor(publicDestr)
    classes.append(invalidInstrDecl)

    #########################################################################
    ############### Now I print the NOP instruction #####################

    if model.startswith('acc'):
        # finally I print the NOP instruction, which I put in the pipeline when flushes occurr
        NOPInstructionElements = []
        for pipeStage in processor.pipes:
            if self.nopBeh.has_key(pipeStage.name):
                defineCode = ''
                for reg in processor.regs:
                    defineCode += '#define ' + reg.name + ' ' + reg.name + '_' + pipeStage.name + '\n'
                for regB in processor.regBanks:
                    defineCode += '#define ' + regB.name + ' ' + regB.name + '_' + pipeStage.name + '\n'
                for alias in processor.aliasRegs:
                    defineCode += '#define ' + alias.name + ' ' + alias.name + '_' + pipeStage.name + '\n'
                for aliasB in processor.aliasRegBanks:
                    defineCode += '#define ' + aliasB.name + ' ' + aliasB.name + '_' + pipeStage.name + '\n'
                undefineCode = ''
                for reg in processor.regs:
                    undefineCode += '#undef ' + reg.name + '\n'
                for regB in processor.regBanks:
                    undefineCode += '#undef ' + regB.name + '\n'
                for alias in processor.aliasRegs:
                    undefineCode += '#undef ' + alias.name + '\n'
                for aliasB in processor.aliasRegBanks:
                    undefineCode += '#undef ' + aliasB.name + '\n'
                behaviorBody = cxx_writer.writer_code.Code(defineCode + '\n' + self.nopBeh[pipeStage.name] + '\n' + undefineCode)
            else:
                behaviorBody = behaviorReturnBody
            behaviorDecl = cxx_writer.writer_code.Method('behavior_' + pipeStage.name, behaviorBody, cxx_writer.writer_code.uintType, 'pu', [unlockQueueParam])
            NOPInstructionElements.append(behaviorDecl)
        from procWriter import baseInstrInitElement
        replicateBody = cxx_writer.writer_code.Code('return new NOPInstruction(' + baseInstrInitElement + ');')
        replicateDecl = cxx_writer.writer_code.Method('replicate', replicateBody, instructionType.makePointer(), 'pu', noException = True, const = True)
        NOPInstructionElements.append(replicateDecl)
        setparamsParam = cxx_writer.writer_code.Parameter('bitString', processor.bitSizes[1].makeRef().makeConst())
        setparamsDecl = cxx_writer.writer_code.Method('setParams', emptyBody, cxx_writer.writer_code.voidType, 'pu', [setparamsParam], noException = True)
        NOPInstructionElements.append(setparamsDecl)
        getIstructionNameBody = cxx_writer.writer_code.Code('return \"NOPInstruction\";')
        getIstructionNameDecl = cxx_writer.writer_code.Method('getInstructionName', getIstructionNameBody, cxx_writer.writer_code.stringType, 'pu', noException = True, const = True)
        NOPInstructionElements.append(getIstructionNameDecl)
        getMnemonicBody = cxx_writer.writer_code.Code('return \"nop\";')
        getMnemonicDecl = cxx_writer.writer_code.Method('getMnemonic', getMnemonicBody, cxx_writer.writer_code.stringType, 'pu', noException = True, const = True)
        NOPInstructionElements.append(getMnemonicDecl)
        getIdBody = cxx_writer.writer_code.Code('return (unsigned int)-1;')
        getIdDecl = cxx_writer.writer_code.Method('getId', getIdBody, cxx_writer.writer_code.uintType, 'pu', noException = True, const = True)
        NOPInstructionElements.append(getIdDecl)

        if hasCheckHazard:
            checkHazardDecl = cxx_writer.writer_code.Method('checkHazard', emptyBody, cxx_writer.writer_code.boolType, 'pu')
            NOPInstructionElements.append(checkHazardDecl)
            lockDecl = cxx_writer.writer_code.Method('lockRegs', emptyBody, cxx_writer.writer_code.voidType, 'pu')
            NOPInstructionElements.append(lockDecl)
            unlockHazard = False
            for pipeStage in processor.pipes:
                if pipeStage.checkHazard:
                    unlockHazard = True
                if unlockHazard:
                    getUnlockDecl = cxx_writer.writer_code.Method('getUnlock_' + pipeStage.name, emptyBody, cxx_writer.writer_code.voidType, 'pu', [unlockQueueParam])
                    NOPInstructionElements.append(getUnlockDecl)
        from procWriter import baseInstrInitElement
        publicConstr = cxx_writer.writer_code.Constructor(emptyBody, 'pu', baseInstrConstrParams, ['Instruction(' + baseInstrInitElement + ')'])
        NOPInstructionClass = cxx_writer.writer_code.ClassDeclaration('NOPInstruction', NOPInstructionElements, [instructionDecl.getType()], namespaces = [namespace])
        NOPInstructionClass.addConstructor(publicConstr)
        publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
        NOPInstructionClass.addDestructor(publicDestr)
        classes.append(NOPInstructionClass)
    # Now I go over all the other instructions and I declare them
    for instr in self.instructions.values():
        classes += instr.getCPPClass(model, processor, trace, combinedTrace, namespace)
    return classes

def getCPPTests(self, processor, modelType, trace, combinedTrace, namespace):
    if not processor.memory:
        return None
    # for each instruction I print the test: I do have to add some custom
    # code at the beginning in order to being able to access the private
    # part of the instructions
    tests = []
    for instr in self.instructions.values():
        tests += instr.getCPPTest(processor, modelType, trace, combinedTrace, namespace)
    return tests
