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

def getCPPIf(self, model, namespace):
    # creates the interface which is used by the tools
    # to access the processor core
    if not self.abi:
        return

    if model.startswith('acc'):
        regWriteCode = ' = '
        regReadCode = ''
    else:
        regWriteCode = '.immediateWrite'
        regReadCode = '.readNewValue()'

    from procWriter import resourceType

    wordType = self.bitSizes[1]
    includes = wordType.getIncludes()
    pipeRegisterType = cxx_writer.writer_code.Type('PipelineRegister', 'registers.hpp')

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
        if model.startswith('acc'):
            curRegBType = pipeRegisterType
        else:
            curRegBType = resourceType[reg.name]
        attribute = cxx_writer.writer_code.Attribute(reg.name, curRegBType.makeRef(), 'pri')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(reg.name, curRegBType.makeRef()))
        initElements.append(reg.name + '(' + reg.name + ')')
        ifClassElements.append(attribute)
    for regB in self.regBanks:
        if (regB.constValue and len(regB.constValue) < regB.numRegs)  or ((regB.delay and len(regB.delay) < regB.numRegs) and not model.startswith('acc')):
            if model.startswith('acc'):
                curRegBType = pipeRegisterType.makePointer()
            else:
                curRegBType = resourceType[regB.name].makeRef()
        else:
            if model.startswith('acc'):
                curRegBType = pipeRegisterType.makePointer()
            else:
                curRegBType = resourceType[regB.name]
        attribute = cxx_writer.writer_code.Attribute(regB.name, curRegBType, 'pri')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(regB.name, curRegBType))
        initElements.append(regB.name + '(' + regB.name + ')')
        ifClassElements.append(attribute)
    for alias in self.aliasRegs:
        attribute = cxx_writer.writer_code.Attribute(alias.name, resourceType[alias.name].makeRef(), 'pri')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(alias.name, resourceType[alias.name].makeRef()))
        initElements.append(alias.name + '(' + alias.name + ')')
        ifClassElements.append(attribute)
    for aliasB in self.aliasRegBanks:
        attribute = cxx_writer.writer_code.Attribute(aliasB.name, resourceType[aliasB.name].makePointer(), 'pri')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(aliasB.name, resourceType[aliasB.name].makePointer()))
        initElements.append(aliasB.name + '(' + aliasB.name + ')')
        ifClassElements.append(attribute)

    if self.isBigEndian:
        endianessCode = cxx_writer.writer_code.Code('return false;')
    else:
        endianessCode = cxx_writer.writer_code.Code('return true;')
    endianessMethod = cxx_writer.writer_code.Method('isLittleEndian', endianessCode, cxx_writer.writer_code.boolType, 'pu', noException = True, const = True)
    ifClassElements.append(endianessMethod)

    # Here are the methods used to discriminate when an instruction is executing or not
    attribute = cxx_writer.writer_code.Attribute('instrExecuting', cxx_writer.writer_code.boolType.makeRef(), 'pri')
    baseInstrConstrParams.append(cxx_writer.writer_code.Parameter('instrExecuting', cxx_writer.writer_code.boolType.makeRef()))
    initElements.append('instrExecuting(instrExecuting)')
    ifClassElements.append(attribute)
    if self.abi.procIdCode:
        processorIDCode = cxx_writer.writer_code.Code('return (' + self.abi.procIdCode + ');\n')
        processorIDMethod = cxx_writer.writer_code.Method('getProcessorID', processorIDCode, cxx_writer.writer_code.intType, 'pu', noException = True, const = True)
        ifClassElements.append(processorIDMethod)
    instrExecutingCode = cxx_writer.writer_code.Code('return this->instrExecuting;')
    instrExecutingMethod = cxx_writer.writer_code.Method('isInstrExecuting', instrExecutingCode, cxx_writer.writer_code.boolType, 'pu', noException = True, const = True)
    ifClassElements.append(instrExecutingMethod)
    if self.systemc:
        attribute = cxx_writer.writer_code.Attribute('instrEndEvent', cxx_writer.writer_code.sc_eventType.makeRef(), 'pri')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter('instrEndEvent', cxx_writer.writer_code.sc_eventType.makeRef()))
        initElements.append('instrEndEvent(instrEndEvent)')
        ifClassElements.append(attribute)
        waitInstrEndCode = cxx_writer.writer_code.Code('if(this->instrExecuting){\nwait(this->instrEndEvent);\n}\n')
        waitInstrEndCode.addInclude('systemc.h')
    else:
        waitInstrEndCode = cxx_writer.writer_code.Code('while(this->instrExecuting){\n;\n}\n')
    waitInstrEndMethod = cxx_writer.writer_code.Method('waitInstrEnd', waitInstrEndCode, cxx_writer.writer_code.voidType, 'pu', noException = True, const = True)
    ifClassElements.append(waitInstrEndMethod)

    if self.abi.preCallCode:
        ifClassElements.append(cxx_writer.writer_code.Method('preCall', cxx_writer.writer_code.Code(self.abi.preCallCode), cxx_writer.writer_code.voidType, 'pu', noException = True))
    if self.abi.postCallCode:
        ifClassElements.append(cxx_writer.writer_code.Method('postCall', cxx_writer.writer_code.Code(self.abi.postCallCode), cxx_writer.writer_code.voidType, 'pu', noException = True))
    if self.abi.returnCallReg:
        returnCallCode = ''
        for returnReg in self.abi.returnCallReg:
            returnCallCode += returnReg[0] + regWriteCode + '(' + returnReg[1] + ' + ' + str(returnReg[2]) + ');\n'
        ifClassElements.append(cxx_writer.writer_code.Method('returnFromCall', cxx_writer.writer_code.Code(returnCallCode), cxx_writer.writer_code.voidType, 'pu', noException = True))

    # Here is the code for recognizing if we are in the routine entry or
    # exit; we behave like a state machine,moving to the beginning when
    # an instruction out of the sequence is met
    entryStateAttribute = cxx_writer.writer_code.Attribute('routineEntryState', cxx_writer.writer_code.intType, 'pri')
    ifClassElements.append(entryStateAttribute)
    exitStateAttribute = cxx_writer.writer_code.Attribute('routineExitState', cxx_writer.writer_code.intType, 'pri')
    ifClassElements.append(exitStateAttribute)
    vector_strType = cxx_writer.writer_code.TemplateType('std::vector', [cxx_writer.writer_code.stringType], 'vector')
    vector_v_strType = cxx_writer.writer_code.TemplateType('std::vector', [vector_strType], 'vector')
    entrySequenceAttribute = cxx_writer.writer_code.Attribute('routineEntrySequence', vector_v_strType, 'pri')
    ifClassElements.append(entrySequenceAttribute)
    exitSequenceAttribute = cxx_writer.writer_code.Attribute('routineExitSequence', vector_v_strType, 'pri')
    ifClassElements.append(exitSequenceAttribute)
    routineStatesInit = """this->routineExitState = 0;
    this->routineEntryState = 0;
    std::vector<std::string> tempVec;
    """
    from isa import Instruction
    for instrList in self.abi.callInstr:
        routineStatesInit += 'tempVec.clear();\n'
        if not instrList:
            routineStatesInit += 'tempVec.push_back("");\n'
        elif isinstance(instrList, Instruction):
            routineStatesInit += 'tempVec.push_back("' + instrList.name + '");\n'
        else:
            for instr in instrList:
                routineStatesInit += 'tempVec.push_back("' + instr.name + '");\n'
        routineStatesInit += 'this->routineEntrySequence.push_back(tempVec);\n'
    for instrList in self.abi.returnCallInstr:
        routineStatesInit += 'tempVec.clear();\n'
        if not instrList:
            routineStatesInit += 'tempVec.push_back("");\n'
        elif isinstance(instrList, Instruction):
            routineStatesInit += 'tempVec.push_back("' + instrList.name + '");\n'
        else:
            for instr in instrList:
                routineStatesInit += 'tempVec.push_back("' + instr.name + '");\n'
        routineStatesInit += 'this->routineExitSequence.push_back(tempVec);\n'
    instructionBaseType = cxx_writer.writer_code.Type('InstructionBase', 'instructionBase.hpp')
    baseInstrParam = cxx_writer.writer_code.Parameter('instr', instructionBaseType.makePointer().makeConst())
    isRoutineEntryBody = """std::vector<std::string> nextNames = this->routineEntrySequence[this->routineEntryState];
    std::vector<std::string>::const_iterator namesIter, namesEnd;
    std::string curName = instr->getInstructionName();
    for(namesIter = nextNames.begin(), namesEnd = nextNames.end(); namesIter != namesEnd; namesIter++){
        if(curName == *namesIter || *namesIter == ""){
            if(this->routineEntryState == """ + str(len(self.abi.callInstr) -1) + """){
                this->routineEntryState = 0;
                return true;
            }
            this->routineEntryState++;
            return false;
        }
    }
    this->routineEntryState = 0;
    return false;
    """
    isRoutineEntryCode = cxx_writer.writer_code.Code(isRoutineEntryBody)
    isRoutineEntryMethod = cxx_writer.writer_code.Method('isRoutineEntry', isRoutineEntryCode, cxx_writer.writer_code.boolType, 'pu', [baseInstrParam], noException = True)
    ifClassElements.append(isRoutineEntryMethod)
    isRoutineExitBody = """std::vector<std::string> nextNames = this->routineExitSequence[this->routineExitState];
    std::vector<std::string>::const_iterator namesIter, namesEnd;
    std::string curName = instr->getInstructionName();
    for(namesIter = nextNames.begin(), namesEnd = nextNames.end(); namesIter != namesEnd; namesIter++){
        if(curName == *namesIter || *namesIter == ""){
            if(this->routineExitState == """ + str(len(self.abi.returnCallInstr) -1) + """){
                this->routineExitState = 0;
                return true;
            }
            this->routineExitState++;
            return false;
        }
    }
    this->routineExitState = 0;
    return false;
    """
    isRoutineExitCode = cxx_writer.writer_code.Code(isRoutineExitBody)
    isRoutineExitMethod = cxx_writer.writer_code.Method('isRoutineExit', isRoutineExitCode, cxx_writer.writer_code.boolType, 'pu', [baseInstrParam], noException = True)
    ifClassElements.append(isRoutineExitMethod)

    # Here I add the methods mecessary to save and restore the complete
    # processor status (useful, for example, to implement hardware context-switches,
    # or simulation chepointing)
    totalStateSize = 0
    for reg in self.regs:
        totalStateSize += reg.bitWidth/self.byteSize
    for regB in self.regBanks:
        totalStateSize += (regB.bitWidth*regB.numRegs)/self.byteSize
    getStateBody = 'unsigned char * curState = new unsigned char[' + str(totalStateSize) + '];\n'
    getStateBody += 'unsigned char * curStateTemp = curState;\n'
    from isa import resolveBitType
    for reg in self.regs:
        regWType = resolveBitType('BIT<' + str(reg.bitWidth) + '>')
        getStateBody += '*((' + str(regWType.makePointer()) + ')curStateTemp) = this->' + reg.name + regReadCode + ';\ncurStateTemp += ' + str(reg.bitWidth/self.byteSize) + ';\n'
    for regB in self.regBanks:
        regWType = resolveBitType('BIT<' + str(regB.bitWidth) + '>')
        for i in range(0, regB.numRegs):
            getStateBody += '*((' + str(regWType.makePointer()) + ')curStateTemp) = this->' + regB.name + '[' + str(i) + ']' + regReadCode + ';\ncurStateTemp += ' + str(regB.bitWidth/self.byteSize) + ';\n'
    getStateBody += 'return curState;'
    getStateCode = cxx_writer.writer_code.Code(getStateBody)
    getStateMethod = cxx_writer.writer_code.Method('getState', getStateCode, cxx_writer.writer_code.ucharPtrType, 'pu', noException = True, const = True)
    ifClassElements.append(getStateMethod)
    setStateBody = 'unsigned char * curStateTemp = state;\n'
    for reg in self.regs:
        regWType = resolveBitType('BIT<' + str(reg.bitWidth) + '>')
        setStateBody += 'this->' + reg.name + regWriteCode + '(*((' + str(regWType.makePointer()) + ')curStateTemp));\ncurStateTemp += ' + str(reg.bitWidth/self.byteSize) + ';\n'
    for regB in self.regBanks:
        regWType = resolveBitType('BIT<' + str(regB.bitWidth) + '>')
        for i in range(0, regB.numRegs):
            setStateBody += 'this->' + regB.name + '[' + str(i) + ']' + regWriteCode + '(*((' + str(regWType.makePointer()) + ')curStateTemp));\ncurStateTemp += ' + str(regB.bitWidth/self.byteSize) + ';\n'
    setStateCode = cxx_writer.writer_code.Code(setStateBody)
    stateParam = cxx_writer.writer_code.Parameter('state', cxx_writer.writer_code.ucharPtrType)
    setStateMethod = cxx_writer.writer_code.Method('setState', setStateCode, cxx_writer.writer_code.voidType, 'pu', [stateParam], noException = True)
    ifClassElements.append(setStateMethod)

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
        setElemBody = 'this->' + elem + regWriteCode + '(newValue);'
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
    setArgsBody += str(vectorType) + '::const_iterator argIter = args.begin(), argEnd = args.end();\n'
    for arg in self.abi.args:
        setArgsBody += 'if(argIter != argEnd){\n'
        setArgsBody += 'this->' + arg + regWriteCode + '(*argIter'
        if self.abi.offset.has_key(arg) and not model.startswith('acc'):
            setArgsBody += ' - ' + str(self.abi.offset[arg])
        setArgsBody += ');\nargIter++;\n}\n'
    setArgsCode = cxx_writer.writer_code.Code(setArgsBody)
    setArgsParam = cxx_writer.writer_code.Parameter('args', vectorType.makeRef().makeConst())
    setArgsMethod = cxx_writer.writer_code.Method('setArgs', setArgsCode, cxx_writer.writer_code.voidType, 'pu', [setArgsParam], noException = True)
    ifClassElements.append(setArgsMethod)
    maxGDBId = 0
    readGDBRegBody = 'switch(gdbId){\n'
    sortedGDBRegs = sorted(self.abi.regCorrespondence.items(), lambda x,y: cmp(x[1], y[1]))
    for reg, gdbId in sortedGDBRegs:
        if gdbId > maxGDBId:
            maxGDBId = gdbId
        readGDBRegBody += 'case ' + str(gdbId) + ':{\n'
        readGDBRegBody += 'return ' + reg
        if self.abi.offset.has_key(reg) and not model.startswith('acc'):
            readGDBRegBody += ' + ' + str(self.abi.offset[reg])
        readGDBRegBody += ';\nbreak;}\n'
    readGDBRegBody += 'default:{\nreturn 0;\n}\n}\n'
    readGDBRegCode = cxx_writer.writer_code.Code(readGDBRegBody)
    readGDBRegCode.addInclude(includes)
    readGDBRegParam = cxx_writer.writer_code.Parameter('gdbId', cxx_writer.writer_code.uintType.makeRef().makeConst())
    readGDBRegMethod = cxx_writer.writer_code.Method('readGDBReg', readGDBRegCode, wordType, 'pu', [readGDBRegParam], noException = True, const = True)
    ifClassElements.append(readGDBRegMethod)
    nGDBRegsCode = cxx_writer.writer_code.Code('return ' + str(maxGDBId + 1) + ';')
    nGDBRegsMethod = cxx_writer.writer_code.Method('nGDBRegs', nGDBRegsCode, cxx_writer.writer_code.uintType, 'pu', noException = True, const = True)
    ifClassElements.append(nGDBRegsMethod)
    setGDBRegBody = 'switch(gdbId){\n'
    for reg, gdbId in sortedGDBRegs:
        setGDBRegBody += 'case ' + str(gdbId) + ':{\n'
        setGDBRegBody += reg + regWriteCode + '(newValue'
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
            for memName, mem_range in self.abi.memories.items():
                readMemBody += 'if(address >= ' + hex(mem_range[0]) + ' && address <= ' + hex(mem_range[1]) + '){\n'
                readMemBody += 'return this->' + self.abi.memories.keys()[0] + '.read_word_dbg(address);\n}\nelse '
            readMemBody += '{\nTHROW_EXCEPTION(\"Address \" << std::hex << address << \" out of range\");\n}'
    readMemCode = cxx_writer.writer_code.Code(readMemBody)
    readMemParam1 = cxx_writer.writer_code.Parameter('address', wordType.makeRef().makeConst())
    readMemMethod = cxx_writer.writer_code.Method('readMem', readMemCode, wordType, 'pu', [readMemParam1])
    ifClassElements.append(readMemMethod)

    readByteMemBody = ''
    if not self.abi.memories:
        readByteMemBody += 'THROW_EXCEPTION(\"No memory accessible from the ABI or processor ' + self.name + '\");'
    else:
        if len(self.abi.memories) == 1:
            readByteMemBody += 'return this->' + self.abi.memories.keys()[0] + '.read_byte_dbg(address);'
        else:
            for memName, mem_range in self.abi.memories.items():
                readByteMemBody += 'if(address >= ' + hex(mem_range[0]) + ' && address <= ' + hex(mem_range[1]) + '){\n'
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
            for memName, mem_range in self.abi.memories.items():
                writeMemBody += 'if(address >= ' + hex(mem_range[0]) + ' && address <= ' + hex(mem_range[1]) + '){\n'
                writeMemBody += 'this->' + self.abi.memories.keys()[0] + '.write_word_dbg(address, datum);\n}\nelse '
            writeMemBody += '{\nTHROW_EXCEPTION(\"Address \" << std::hex << address << \" out of range\");\n}'
    writeMemCode = cxx_writer.writer_code.Code(writeMemBody)
    writeMemCode.addInclude('trap_utils.hpp')
    writeMemParam1 = cxx_writer.writer_code.Parameter('address', wordType.makeRef().makeConst())
    writeMemParam2 = cxx_writer.writer_code.Parameter('datum', wordType)
    writeMemMethod = cxx_writer.writer_code.Method('writeMem', writeMemCode, cxx_writer.writer_code.voidType, 'pu', [writeMemParam1, writeMemParam2])
    ifClassElements.append(writeMemMethod)
    writeMemBody = ''
    if not self.abi.memories:
        writeMemBody += 'THROW_EXCEPTION(\"No memory accessible from the ABI or processor ' + self.name + '\");'
    else:
        if len(self.abi.memories) == 1:
            writeMemBody += 'this->' + self.abi.memories.keys()[0] + '.write_byte_dbg(address, datum);'
        else:
            for memName, mem_range in self.abi.memories.items():
                writeMemBody += 'if(address >= ' + hex(mem_range[0]) + ' && address <= ' + hex(mem_range[1]) + '){\n'
                writeMemBody += 'this->' + self.abi.memories.keys()[0] + '.write_byte_dbg(address, datum);\n}\nelse '
            writeMemBody += '{\nTHROW_EXCEPTION(\"Address \" << std::hex << address << \" out of range\");\n}'
    writeMemCode = cxx_writer.writer_code.Code(writeMemBody)
    writeMemParam1 = cxx_writer.writer_code.Parameter('address', wordType.makeRef().makeConst())
    writeMemParam2 = cxx_writer.writer_code.Parameter('datum', cxx_writer.writer_code.ucharType)
    writeMemMethod = cxx_writer.writer_code.Method('writeCharMem', writeMemCode, cxx_writer.writer_code.voidType, 'pu', [writeMemParam1, writeMemParam2])
    ifClassElements.append(writeMemMethod)

    ABIIfType = cxx_writer.writer_code.TemplateType('ABIIf', [wordType], 'ABIIf.hpp')
    ifClassDecl = cxx_writer.writer_code.ClassDeclaration(self.name + '_ABIIf', ifClassElements, [ABIIfType], namespaces = [namespace])
    publicIfConstr = cxx_writer.writer_code.Constructor(cxx_writer.writer_code.Code(routineStatesInit), 'pu', baseInstrConstrParams, initElements)
    emptyBody = cxx_writer.writer_code.Code('')
    opDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    ifClassDecl.addDestructor(opDestr)
    ifClassDecl.addConstructor(publicIfConstr)
    return ifClassDecl
