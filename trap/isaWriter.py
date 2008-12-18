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

def toBinStr(intNum):
    # Given an integer number it converts it to a bitstring
    bitStr = []
    while intNum > 0:
        bitStr.append(str(intNum % 2))
        intNum = intNum / 2
    bitStr.reverse()
    return bitStr

def getCppMethod(self):
    # Returns the code implementing a helper method
    for var in self.localvars:
        self.code.addVariable(var)
    self.code.addInclude('utils.hpp')
    methodDecl = cxx_writer.writer_code.Method(self.name, self.code, self.retType, 'pu', self.parameters)
    return methodDecl

def getCppOperation(self, parameters = False):
    # Returns the code implementing a helper operation
    aliasType = cxx_writer.writer_code.Type('Alias', 'alias.hpp')
    for var in self.localvars:
        self.code.addVariable(var)
    self.code.addInclude('utils.hpp')
    metodParams = []
    if parameters:
        for elem in self.archElems:
            metodParams.append(cxx_writer.writer_code.Parameter(elem, aliasType.makeRef()))
            metodParams.append(cxx_writer.writer_code.Parameter(elem + '_bit', cxx_writer.writer_code.uintRefType))
        for elem in self.archVars:
            metodParams.append(cxx_writer.writer_code.Parameter(elem, cxx_writer.writer_code.uintRefType))
        for var in self.instrvars:
            metodParams.append(cxx_writer.writer_code.Parameter(var.name, var.type.makeRef()))
    methodDecl = cxx_writer.writer_code.Method(self.name, self.code, cxx_writer.writer_code.voidType, 'pro', metodParams, inline = True)
    return methodDecl

def getCppOpClass(self):
    # Returns a class (directly deriving from instruction) implementing the
    # method corresponding to the current operation
    global baseInstrConstrParams
    from procWriter import baseInstrInitElement
    aliasType = cxx_writer.writer_code.Type('Alias', 'alias.hpp')
    instructionType = cxx_writer.writer_code.Type('Instruction', 'instructions.hpp')
    emptyBody = cxx_writer.writer_code.Code('')
    for var in self.localvars:
        self.code.addVariable(var)
    self.code.addInclude('utils.hpp')
    classElements = []
    # Now I also need to declare the instruction variables and referenced architectural elements
    metodParams = []
    for elem in self.archElems:
        metodParams.append(cxx_writer.writer_code.Parameter(elem, aliasType.makeRef()))
        metodParams.append(cxx_writer.writer_code.Parameter(elem + '_bit', cxx_writer.writer_code.uintRefType))
    for elem in self.archVars:
        metodParams.append(cxx_writer.writer_code.Parameter(elem, cxx_writer.writer_code.uintRefType))
    for var in self.instrvars:
        metodParams.append(cxx_writer.writer_code.Parameter(var.name, var.type.makeRef()))
    methodDecl = cxx_writer.writer_code.Method(self.name, self.code, cxx_writer.writer_code.voidType, 'pro', metodParams, inline = True)
    classElements.append(methodDecl)
    opConstr = cxx_writer.writer_code.Constructor(emptyBody, 'pu', baseInstrConstrParams, ['Instruction(' + baseInstrInitElement + ')'])
    opDecl = cxx_writer.writer_code.ClassDeclaration(self.name + '_op', classElements, virtual_superclasses = [instructionType])
    opDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    opDecl.addDestructor(opDestr)
    opDecl.addConstructor(opConstr)
    return opDecl

def getCPPInstr(self, model, pipeline, trace):
    # Returns the code implementing the current instruction: we have to provide the
    # implementation of all the abstract methods and call from the behavior method
    # all the different behaviors contained in the type hierarchy of this class
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
            if behClass.has_key(beh.name):
                baseClasses.append(behClass[beh.name].getType())
                constrInitList.append(beh.name + '_op(' + baseInstrInitElement + ')')
            elif beh.inline and not beh.name in alreadyDeclared:
                classElements.append(beh.getCppOperation())
            elif not beh.name in alreadyDeclared:
                toInline.append(beh.name)
            for var in beh.instrvars:
                if not var.name in behVars:
                    classElements.append(cxx_writer.writer_code.Attribute(var.name, var.type, 'pro',  var.static))
                    behVars.append(var.name)
    if not baseClasses:
        baseClasses.append(instructionType)
    if not model.startswith('acc'):
        # This is not a cycle accurate processor, so pipeline is not modelled
        behaviorCode = 'this->totalInstrCycles = 0;\n'
        for behaviors in self.prebehaviors.values():
            for beh in behaviors:
                if beh.name in toInline:
                    behaviorCode += str(beh.code)
                elif behClass.has_key(beh.name) or beh.name in baseBehaviors:
                    behaviorCode += 'this->' + beh.name + '('
                    for elem in beh.archElems:
                        behaviorCode += 'this->' + elem + ', '
                        behaviorCode += 'this->' + elem + '_bit'
                        if beh.archVars or beh.instrvars or elem != beh.archElems[-1]:
                            behaviorCode += ', '
                    for elem in beh.archVars:
                        behaviorCode += 'this->' + elem
                        if beh.instrvars or elem != beh.archVars[-1]:
                            behaviorCode += ', '
                    for var in beh.instrvars:
                        behaviorCode += 'this->' + var.name
                        if var != beh.instrvars[-1]:
                            behaviorCode += ', '
                    behaviorCode += ');\n'
                else:
                    behaviorCode += 'this->' + beh.name + '();\n'
        for code in self.code.values():
            behaviorCode += str(code.code)
        for behaviors in self.postbehaviors.values():
            for beh in behaviors:
                if beh.name in toInline:
                    behaviorCode += str(beh.code)
                elif behClass.has_key(beh.name) or beh.name in baseBehaviors:
                    behaviorCode += 'this->' + beh.name + '('
                    for elem in beh.archElems:
                        behaviorCode += 'this->' + elem + ', '
                        behaviorCode += 'this->' + elem + '_bit'
                        if beh.archVars or beh.instrvars or elem != beh.archElems[-1]:
                            behaviorCode += ', '
                    for elem in beh.archVars:
                        behaviorCode += 'this->' + elem
                        if beh.instrvars or elem != beh.archVars[-1]:
                            behaviorCode += ', '
                    for var in beh.instrvars:
                        behaviorCode += 'this->' + var.name
                        if var != beh.instrvars[-1]:
                            behaviorCode += ', '
                    behaviorCode += ');\n'
                else:
                    behaviorCode += 'this->' + beh.name + '();\n'
        behaviorCode += 'return this->totalInstrCycles;'
        behaviorBody = cxx_writer.writer_code.Code(behaviorCode)
        behaviorDecl = cxx_writer.writer_code.Method('behavior', behaviorBody, cxx_writer.writer_code.uintType, 'pu')
        classElements.append(behaviorDecl)
    else:
        # cycle accurate model, I have to separate the behavior in the different pipeline stages
        for pipeStage in pipeline:
            behaviorCode = 'this->stageCycles = 0;\n'
            if self.prebehaviors.has_key(pipeStage):
                for beh in self.prebehaviors[pipeStage]:
                    if beh.name in toInline:
                        behaviorCode += str(beh.code)
                    elif behClass.has_key(beh.name) or beh.name in baseBehaviors:
                        behaviorCode += 'this->' + beh.name + '('
                        for elem in beh.archElems:
                            behaviorCode += 'this->' + elem + ', '
                            behaviorCode += 'this->' + elem + '_bit'
                            if beh.archVars or beh.instrvars or elem != beh.archElems[-1]:
                                behaviorCode += ', '
                        for elem in beh.archVars:
                            behaviorCode += 'this->' + elem
                            if beh.instrvars or elem != beh.archVars[-1]:
                                behaviorCode += ', '
                        for var in beh.instrvars:
                            behaviorCode += 'this->' + var.name
                            if var != beh.instrvars[-1]:
                                behaviorCode += ', '
                        behaviorCode += ');\n'
                    else:
                        behaviorCode += 'this->' + beh.name + '();\n'
            if self.code.has_key(pipeStage):
                behaviorCode += str(code[pipeStage].code)
            if self.postbehaviors.has_key(pipeStage):
                for beh in self.postbehaviors[pipeStage]:
                    if beh.name in toInline:
                        behaviorCode += str(beh.code)
                    elif behClass.has_key(beh.name) or beh.name in baseBehaviors:
                        behaviorCode += 'this->' + beh.name + '('
                        for elem in beh.archElems:
                            behaviorCode += 'this->' + elem + ', '
                            behaviorCode += 'this->' + elem + '_bit'
                            if beh.archVars or beh.instrvars or elem != beh.archElems[-1]:
                                behaviorCode += ', '
                        for elem in beh.archVars:
                            behaviorCode += 'this->' + elem
                            if beh.instrvars or elem != beh.archVars[-1]:
                                behaviorCode += ', '
                        for var in beh.instrvars:
                            behaviorCode += 'this->' + var.name
                            if var != beh.instrvars[-1]:
                                behaviorCode += ', '
                        behaviorCode += ');\n'
                    else:
                        behaviorCode += 'this->' + beh.name + '();\n'
            behaviorCode += 'return this->stageCycles;'
            behaviorBody = cxx_writer.writer_code.Code(behaviorCode)
            behaviorDecl = cxx_writer.writer_code.Method('behavior_' + pipeStage.name, behaviorBody, cxx_writer.writer_code.uintType, 'pu')
            classElements.append(behaviorDecl)

    replicateBody = cxx_writer.writer_code.Code('return new ' + self.name + '(' + baseInstrInitElement + ');')
    replicateDecl = cxx_writer.writer_code.Method('replicate', replicateBody, instructionType.makePointer(), 'pu', noException = True, const = True)
    classElements.append(replicateDecl)
    if trace:
        getIstructionNameBody = cxx_writer.writer_code.Code('return \"' + self.name + '\"\n;')
        getIstructionNameDecl = cxx_writer.writer_code.Method('getIstructionName', getIstructionNameBody, cxx_writer.writer_code.stringType, 'pu')
        classElements.append(getIstructionNameDecl)

    # We need to create the attribute for the variables referenced by the non-constant parts of the instruction;
    # they are the bitCorrespondence variable of the machine code (they establish the correspondence with either registers
    # or aliases); they other remaining undefined parts of the instruction are normal integer variables.
    # Note, anyway, that I add the integer variable also for the parts of the instructions specified in
    # bitCorrespondence.
    setParamsCode = ''
    for name, correspondence in self.machineCode.bitCorrespondence.items():
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
        setParamsCode += 'this->' + name + '.updateAlias(' + correspondence[0] + '[' + str(correspondence[1]) + ' + this->' + name + '_bit]);\n'
    # now I need to declare the fields for the variable parts of the
    # instruction
    for name, length in self.machineCode.bitFields:
        if name in self.machineBits.keys() + self.machineCode.bitValue.keys() + self.machineCode.bitCorrespondence.keys():
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
    setparamsParam = cxx_writer.writer_code.Parameter('bitString', archWordType.makeRef().makeConst())
    setparamsDecl = cxx_writer.writer_code.Method('setParams', setParamsBody, cxx_writer.writer_code.voidType, 'pu', [setparamsParam], noException = True)
    classElements.append(setparamsDecl)
    for var in self.variables:
        if not var.name in behVars:
            classElements.append(cxx_writer.writer_code.Attribute(var.name, var.type, 'pro',  var.static))
    # Now I have to declare the constructor
    from procWriter import baseInstrInitElement
    publicConstr = cxx_writer.writer_code.Constructor(emptyBody, 'pu', baseInstrConstrParams, constrInitList)
    instructionDecl = cxx_writer.writer_code.ClassDeclaration(self.name, classElements, superclasses = baseClasses)
    instructionDecl.addConstructor(publicConstr)
    publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    instructionDecl.addDestructor(publicDestr)
    return instructionDecl

def getCPPInstrTest(self, processor, model):
    # Returns the code testing the current instruction: note that a test
    # consists in setting the instruction variables, performing the instruction
    # behavior and then comparing the registers with what we expect.
    archElemsDeclStr = ''
    baseInitElement = '('
    destrDecls = ''
    from procWriter import resourceType
    for reg in processor.regs:
        archElemsDeclStr += str(resourceType[reg.name]) + ' ' + reg.name + ';\n'
        baseInitElement += reg.name + ', '
    for regB in processor.regBanks:
        archElemsDeclStr += str(resourceType[regB.name].makePointer()) + ' ' + regB.name + ' = new ' + str(resourceType[regB.name]) + '[' + str(regB.numRegs) + '];\n'
        baseInitElement += regB.name + ', '
        destrDecls += 'delete [] ' + regB.name + ';\n'
    for alias in processor.aliasRegs:
        archElemsDeclStr += str(resourceType[alias.name]) + ' ' + alias.name + ';\n'
        baseInitElement += alias.name + ', '
    for aliasB in processor.aliasRegBanks:
        archElemsDeclStr += str(resourceType[aliasB.name].makePointer()) + ' ' + aliasB.name + ' = new ' + str(resourceType[aliasB.name]) + '[' + str(aliasB.numRegs) + '];\n'
        baseInitElement += aliasB.name + ', '
        destrDecls += 'delete [] ' + aliasB.name + ';\n'
    memAliasInit = ''
    for alias in processor.memAlias:
        memAliasInit += ', ' + alias.alias
    if processor.memory:
        archElemsDeclStr += 'LocalMemory ' + processor.memory[0] + '(' + str(processor.memory[1]) + memAliasInit + ');\n'
        baseInitElement += processor.memory[0] + ', '
    # Note how I declare local memories even for TLM ports. I use 1MB as default dimension
    for tlmPorts in processor.tlmPorts.keys():
        archElemsDeclStr += 'LocalMemory ' + tlmPorts + '(' + str(1024*1024) + memAliasInit + ');\n'
        baseInitElement += tlmPorts + ', '
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
        code = 'BOOST_AUTO_TEST_CASE( test_' + self.name + '_' + str(len(tests)) + ' ){\n'
        # First of all I create the instance of the instruction and of all the
        # processor elements
        code += archElemsDeclStr + '\n' + aliasInit + '\n'
        code += self.name + ' toTest' + baseInitElement + ';\n'
        # Now I set the value of the instruction fields
        instrCode = ['0' for i in range(0, self.machineCode.instrLen)]
        for name, elemValue in test[0].items():
            if self.machineCode.bitLen.has_key(name):
                curBitCode = toBinStr(elemValue)
                curBitCode.reverse()
                #print 'element ' + name + ' int value ' + str(elemValue) + ' bits ' + str(curBitCode)
                if len(curBitCode) > self.machineCode.bitLen[name]:
                    raise Exception('Value ' + hex(elemValue) + ' set for field ' + name + ' in test of instruction ' + self.name + ' cannot be represented in ' + str(self.machineCode.bitLen[name]) + ' bits')
                for i in range(0, len(curBitCode)):
                    instrCode[self.machineCode.bitLen[name] + self.machineCode.bitPos[name] - i -1] = curBitCode[i]
        for resource, value in test[1].items():
            # I set the initial value of the global resources
            brackIndex = resource.find('[')
            memories = processor.tlmPorts.keys()
            if processor.memory:
                memories.append(processor.memory[0])
            if brackIndex > 0 and resource[:brackIndex] in memories:
                try:
                    code += resource[:brackIndex] + '.write_word(' + hex(int(resource[brackIndex + 1:-1])) + ', ' + str(value) + ');\n'
                except ValueError:
                    code += resource[:brackIndex] + '.write_word(' + hex(int(resource[brackIndex + 1:-1], 16)) + ', ' + str(value) + ');\n'
            else:
                code += resource + ' = ' + str(value) + ';\n'
        code += 'toTest.setParams(' + hex(int(''.join(instrCode), 2)) + ');\n'
        code += 'try{\n'
        if not model.startswith('acc'):
            code += 'toTest.behavior();'
        else:
            for pipeStage in processor.pipes:
                code += 'toTest.behavior_' + pipeStage + '();'
        code += '\n}\ncatch(flush_exception &etc){\n}\n\n'
        for resource, value in test[2].items():
            # I check the value of the listed resources to make sure that the
            # computation executed correctly
            code += 'BOOST_CHECK_EQUAL('
            brackIndex = resource.find('[')
            memories = processor.tlmPorts.keys()
            if processor.memory:
                memories.append(processor.memory[0])
            if brackIndex > 0 and resource[:brackIndex] in memories:
                code += resource + '.read_word(' + hex(value) + ', ' + hex(resource[brackIndex + 1:-1]) + ')'
            else:
                code += resource
            global archWordType
            code += ', (' + str(archWordType) + ')' + hex(value) + ');\n\n'
        code += destrDecls + '\n}\n\n'
        curTest = cxx_writer.writer_code.Code(code)
        curTest.addInclude(['boost/test/auto_unit_test.hpp', 'boost/test/test_tools.hpp', 'memory.hpp', 'customExceptions.hpp'])
        tests.append(curTest)
    return tests

def getCPPClasses(self, processor, model, trace):
    # I go over each instruction and print the class representing it
    from isa import resolveBitType
    global archWordType
    archWordType = resolveBitType('BIT<' + str(processor.wordSize*processor.byteSize) + '>')
    memoryType = cxx_writer.writer_code.Type('MemoryInterface', 'memory.hpp')
    classes = []
    # First of all I create the base instruction type: note that it contains references
    # to the architectural elements
    instructionType = cxx_writer.writer_code.Type('Instruction')
    instructionElements = []
    emptyBody = cxx_writer.writer_code.Code('')
    if not model.startswith('acc'):
        behaviorDecl = cxx_writer.writer_code.Method('behavior', emptyBody, cxx_writer.writer_code.uintType, 'pu', pure = True)
        instructionElements.append(behaviorDecl)
    else:
        for pipeStage in processor.pipes:
            behaviorDecl = cxx_writer.writer_code.Method('behavior_' + pipeStage, emptyBody, cxx_writer.writer_code.uintType, 'pu', pure = True)
            instructionElements.append(behaviorDecl)
    replicateDecl = cxx_writer.writer_code.Method('replicate', emptyBody, instructionType.makePointer(), 'pu', pure = True, noException = True, const = True)
    instructionElements.append(replicateDecl)
    setparamsParam = cxx_writer.writer_code.Parameter('bitString', archWordType.makeRef().makeConst())
    setparamsDecl = cxx_writer.writer_code.Method('setParams', emptyBody, cxx_writer.writer_code.voidType, 'pu', [setparamsParam], pure = True, noException = True)
    instructionElements.append(setparamsDecl)
    if trace:
        getIstructionNameDecl = cxx_writer.writer_code.Method('getIstructionName', emptyBody, cxx_writer.writer_code.stringType, 'pu', pure = True)
        instructionElements.append(getIstructionNameDecl)
        # I have to print the value of all the registers in the processor
        printTraceCode = 'std::cerr << \"Instruction: \" << this->getIstructionName() << std::endl;\n'
        for reg in processor.regs:
            printTraceCode += 'std::cerr << \"' + reg.name + ' = \" << std::hex << std::showbase << this->' + reg.name + ' << std::endl;\n'
        for regB in processor.regBanks:
            printTraceCode += 'for(int regNum = 0; regNum < ' + str(regB.numRegs) + '; regNum++){\n'
            printTraceCode += 'std::cerr << \"' + regB.name + '[\" << std::dec << regNum << \"] = \" << std::hex << std::showbase << this->' + regB.name + '[regNum] << std::endl;\n}\n'
        printTraceBody = cxx_writer.writer_code.Code(printTraceCode + 'std::cerr << std::endl;\n')
        printTraceDecl = cxx_writer.writer_code.Method('printTrace', printTraceBody, cxx_writer.writer_code.voidType, 'pu')
        instructionElements.append(printTraceDecl)

    # Note how the flush operation also stops the execution of the current operation
    flushCode = 'throw flush_exception();'
    flushBody = cxx_writer.writer_code.Code(flushCode)
    flushBody.addInclude('customExceptions.hpp')
    flushDecl = cxx_writer.writer_code.Method('flush', flushBody, cxx_writer.writer_code.voidType, 'pu', inline = True)
    instructionElements.append(flushDecl)
    stallParam = cxx_writer.writer_code.Parameter('numCycles', archWordType.makeRef().makeConst())
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
            instructionElements.append(helpMeth.getCppMethod())
    # Now create references to the architectural elements contained in the processor and
    # initialize them through the constructor
    initElements = []
    global baseInstrConstrParams
    baseInstrConstrParams = []
    baseInitElement = 'Instruction('
    from procWriter import resourceType
    for reg in processor.regs:
        attribute = cxx_writer.writer_code.Attribute(reg.name, resourceType[reg.name].makeRef(), 'pro')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(reg.name, resourceType[reg.name].makeRef()))
        initElements.append(reg.name + '(' + reg.name + ')')
        baseInitElement += reg.name + ', '
        instructionElements.append(attribute)
    for regB in processor.regBanks:
        attribute = cxx_writer.writer_code.Attribute(regB.name, resourceType[regB.name].makePointer().makeRef(), 'pro')
        baseInstrConstrParams.append(cxx_writer.writer_code.Parameter(regB.name, resourceType[regB.name].makePointer().makeRef()))
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
    baseInitElement = baseInitElement[:-2]
    baseInitElement += ')'
    if not model.startswith('acc'):
        instructionElements.append(cxx_writer.writer_code.Attribute('totalInstrCycles', cxx_writer.writer_code.uintType, 'pro'))
        constrBody = 'this->totalInstrCycles = 0;'
    else:
        instructionElements.append(cxx_writer.writer_code.Attribute('stageCycles', cxx_writer.writer_code.uintType, 'pro'))
        constrBody = 'this->stageCycles = 0;'
    publicConstr = cxx_writer.writer_code.Constructor(cxx_writer.writer_code.Code(constrBody), 'pu', baseInstrConstrParams, initElements)
    instructionDecl = cxx_writer.writer_code.ClassDeclaration('Instruction', instructionElements)
    instructionDecl.addConstructor(publicConstr)
    publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    instructionDecl.addDestructor(publicDestr)
    classes.append(instructionDecl)

    # we now have to check all the operation and the behaviors of the instructions and create
    # the classes for each shared non-inline behavior
    global behClass
    behClass = {}
    for instr in self.instructions.values():
        for behaviors in instr.postbehaviors.values() + instr.prebehaviors.values():
            for beh in behaviors:
                if not behClass.has_key(beh.name) and beh.inline and beh.numUsed > 1 and not beh.name in alreadyDeclared:
                    behClass[beh.name] = beh.getCppOpClass()
                    classes.append(behClass[beh.name])

    # Now I print the invalid instruction
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
                behaviorDecl = cxx_writer.writer_code.Method('behavior_' + pipeStage.name, behaviorBody, cxx_writer.writer_code.uintType, 'pu')
            else:
                behaviorDecl = cxx_writer.writer_code.Method('behavior_' + pipeStage.name, behaviorReturnBody, cxx_writer.writer_code.uintType, 'pu')
            invalidInstrElements.append(behaviorDecl)
    else:
        behaviorDecl = cxx_writer.writer_code.Method('behavior', behaviorBody, cxx_writer.writer_code.uintType, 'pu')
        invalidInstrElements.append(behaviorDecl)
    from procWriter import baseInstrInitElement
    replicateBody = cxx_writer.writer_code.Code('return new InvalidInstr(' + baseInstrInitElement + ');')
    replicateDecl = cxx_writer.writer_code.Method('replicate', replicateBody, instructionType.makePointer(), 'pu', noException = True, const = True)
    invalidInstrElements.append(replicateDecl)
    setparamsParam = cxx_writer.writer_code.Parameter('bitString', archWordType.makeRef().makeConst())
    setparamsDecl = cxx_writer.writer_code.Method('setParams', emptyBody, cxx_writer.writer_code.voidType, 'pu', [setparamsParam], noException = True)
    invalidInstrElements.append(setparamsDecl)
    if trace:
        getIstructionNameBody = cxx_writer.writer_code.Code('return \"InvalidInstruction\"\n;')
        getIstructionNameDecl = cxx_writer.writer_code.Method('getIstructionName', getIstructionNameBody, cxx_writer.writer_code.stringType, 'pu')
        invalidInstrElements.append(getIstructionNameDecl)
    from procWriter import baseInstrInitElement
    publicConstr = cxx_writer.writer_code.Constructor(emptyBody, 'pu', baseInstrConstrParams, ['Instruction(' + baseInstrInitElement + ')'])
    invalidInstrDecl = cxx_writer.writer_code.ClassDeclaration('InvalidInstr', invalidInstrElements, [instructionDecl.getType()])
    invalidInstrDecl.addConstructor(publicConstr)
    publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    invalidInstrDecl.addDestructor(publicDestr)
    classes.append(invalidInstrDecl)
    if model.startswith('acc'):
        # finally I print the NOP instruction, which I put in the pipeline when flushes occurr
        NOPInstructionElements = []
        for pipeStage in processor.pipes:
            behaviorDecl = cxx_writer.writer_code.Method('behavior_' + pipeStage.name, behaviorReturnBody, cxx_writer.writer_code.uintType, 'pu')
            NOPInstructionElements.append(behaviorDecl)
        from procWriter import baseInstrInitElement
        replicateBody = cxx_writer.writer_code.Code('return new NOPInstruction(' + baseInstrInitElement + ');')
        replicateDecl = cxx_writer.writer_code.Method('replicate', replicateBody, instructionType.makePointer(), 'pu', noException = True, const = True)
        NOPInstructionElements.append(replicateDecl)
        setparamsParam = cxx_writer.writer_code.Parameter('bitString', archWordType.makeRef().makeConst())
        setparamsDecl = cxx_writer.writer_code.Method('setParams', emptyBody, cxx_writer.writer_code.voidType, 'pu', [setparamsParam], noException = True)
        NOPInstructionElements.append(setparamsDecl)
        if trace:
            getIstructionNameBody = cxx_writer.writer_code.Code('return \"InvalidInstruction\"\n;')
            getIstructionNameDecl = cxx_writer.writer_code.Method('getIstructionName', getIstructionNameBody, cxx_writer.writer_code.stringType, 'pu')
            NOPInstructionElements.append(getIstructionNameDecl)
        from procWriter import baseInstrInitElement
        publicConstr = cxx_writer.writer_code.Constructor(emptyBody, 'pu', baseInstrConstrParams, ['Instruction(' + baseInstrInitElement + ')'])
        NOPInstructionElements = cxx_writer.writer_code.ClassDeclaration('NOPInstructionElements', NOPInstructionElements, [instructionDecl.getType()])
        NOPInstructionElements.addConstructor(publicConstr)
        publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
        NOPInstructionElements.addDestructor(publicDestr)
        classes.append(NOPInstructionElements)
    # Now I go over all the other instructions and I declare them
    for instr in self.instructions.values():
        classes.append(instr.getCPPClass(model, processor.pipes, trace))
    return classes

def getCPPTests(self, processor, modelType):
    if not processor.memory:
        return None
    # for each instruction I print the test: I do have to add some custom
    # code at the beginning in order to being able to access the private
    # part of the instructions
    tests = []
    includeCode = cxx_writer.writer_code.Code('#define private public\n#define protected public\n#include \"instructions.hpp\"\n#undef private\n#undef protected\n')
    tests.append(includeCode)
    for instr in self.instructions.values():
        tests += instr.getCPPTest(processor, modelType)
    return tests
