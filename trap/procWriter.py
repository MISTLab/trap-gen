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

try:
    nxVersion = float(NX.__version__)
except:
    import traceback
    traceback.print_exc()
    raise Exception('Error while determining the version of module networkx, try changing version, at least 0.36 required (newest non-development versions are usually ok)')

# map linking the name with the type of the resource
resourceType = {}

# Helper variables
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

# Computes the code defining the execution of an instruction and
# of the processor tools.
def getInstrIssueCode(self, trace, instrVarName):
    codeString = """try{
            #ifndef DISABLE_TOOLS
            if(!(this->toolManager.newIssue(curPC, """ + instrVarName + """))){
            #endif
            numCycles = """ + instrVarName + """->behavior();
    """
    if trace:
        codeString += instrVarName + '->printTrace();\n'
    codeString += '#ifndef DISABLE_TOOLS\n}\n'
    if trace:
        codeString += """else{
            std::cerr << "Not executed Instruction because Tools anulled it" << std::endl << std::endl;
        }
        """
    codeString +='#endif\n}\ncatch(annull_exception &etc){\n'
    if trace:
        codeString += instrVarName + """->printTrace();
                std::cerr << "Skipped Instruction " << """ + instrVarName + """->getInstructionName() << std::endl << std::endl;
        """
    codeString += """numCycles = 0;
        }
        """
    return codeString

# Computes the code for the fetch address
def computeFetchCode(self):
    fetchCode = str(self.bitSizes[1]) + ' bitString = this->'
    # Now I have to check what is the fetch: if there is a TLM port or
    # if I have to access local memory
    if self.memory:
        # I perform the fetch from the local memory
        fetchCode += self.memory[0]
    else:
        for name, isFetch  in self.tlmPorts.items():
            if isFetch:
                fetchCode += name
        if fetchCode.endswith('this->'):
            raise Exception('No TLM port was chosen for the instruction fetch and not internal memory defined')
    fetchCode += '.read_word(curPC);\n'
    return fetchCode

# Computes current program counter, in order to fetch
# instrutions from it
def computeCurrentPC(self, model):
    fetchAddress = 'this->' + self.fetchReg[0]
    if model.startswith('func'):
        if self.fetchReg[1] < 0:
            fetchAddress += str(self.fetchReg[1])
        else:
            fetchAddress += ' + ' + str(self.fetchReg[1])
    return fetchAddress

# Computes and prints the code necessary for dealing with interrupts
def getInterruptCode(self):
    interruptCode = ''
    orderedIrqList = sorted(self.irqs, lambda x,y: cmp(y.priority, x.priority))
    for irqPort in orderedIrqList:
        if irqPort != orderedIrqList[0]:
            interruptCode += 'else '
        interruptCode += 'if('
        if(irqPort.condition):
            interruptCode += '('
        interruptCode += irqPort.name + ' != -1'
        if(irqPort.condition):
            interruptCode += ') && (' + irqPort.condition + ')'
        interruptCode += '){\n'
        interruptCode += irqPort.operation + '\n}\n'
    if self.irqs:
        interruptCode += 'else{\n'
    return interruptCode

# Returns the code necessary for performing a standard instruction fetch: i.e.
# read from memory and set the instruction parameters
def standardInstrFetch(self, trace):
    codeString = """int instrId = this->decoder.decode(bitString);
    Instruction * instr = Processor::INSTRUCTIONS[instrId];
    instr->setParams(bitString);
    """
    codeString += getInstrIssueCode(self, trace, 'instr')
    return codeString

def fetchWithCacheCode(self, fetchCode, trace):
    codeString = ''
    if self.fastFetch:
        mapKey = 'curPC'
    else:
        mapKey = 'bitString'
    codeString += 'template_map< ' + str(self.bitSizes[1]) + ', CacheElem >::iterator cachedInstr = this->instrCache.find(' + mapKey + ');'
    # I have found the instruction in the cache
    codeString += """
    if(cachedInstr != instrCacheEnd){
        Instruction * &curInstrPtr = cachedInstr->second.instr;
        // I can call the instruction, I have found it
        if(curInstrPtr != NULL){
    """
    codeString += getInstrIssueCode(self, trace, 'curInstrPtr')

    # I have found the element in the cache, but not the instruction
    codeString += '}\nelse{\n'
    if self.fastFetch:
        codeString += fetchCode
    codeString += standardInstrFetch(self, trace)
    codeString += """unsigned int & curCount = cachedInstr->second.count;
        if(curCount < """ + str(self.cacheLimit) + """){
            curCount++;
        }
        else{
            // ... and then add the instruction to the cache
            curInstrPtr = instr;
            Processor::INSTRUCTIONS[instrId] = instr->replicate();
        }
    """

    # and now finally I have found nothing and I have to add everything
    codeString += """}
    }
    else{
        // The current instruction is not present in the cache:
        // I have to perform the normal decoding phase ...
    """
    if self.fastFetch:
        codeString += fetchCode
    codeString += standardInstrFetch(self, trace)
    codeString += """this->instrCache.insert(std::pair< unsigned int, CacheElem >(bitString, CacheElem()));
        instrCacheEnd = this->instrCache.end();
        }
    """
    return codeString

def getCPPProc(self, model, trace, namespace):
    # creates the class describing the processor
    fetchWordType = self.bitSizes[1]
    includes = fetchWordType.getIncludes()
    if self.abi:
        interfaceType = cxx_writer.writer_code.Type(self.name + '_ABIIf', 'interface.hpp')
    ToolsManagerType = cxx_writer.writer_code.TemplateType('ToolsManager', [fetchWordType], 'ToolsIf.hpp')
    IntructionType = cxx_writer.writer_code.Type('Instruction', 'instructions.hpp')
    CacheElemType = cxx_writer.writer_code.Type('CacheElem')
    IntructionTypePtr = IntructionType.makePointer()
    emptyBody = cxx_writer.writer_code.Code('')
    processorElements = []
    codeString = ''

    # Here I declare the type which shall be contained in the cache
    if self.instructionCache:
        instrAttr = cxx_writer.writer_code.Attribute('instr', IntructionTypePtr, 'pu')
        countAttr = cxx_writer.writer_code.Attribute('count', cxx_writer.writer_code.uintType, 'pu')
        cacheTypeElements = [instrAttr, countAttr]
        cacheType = cxx_writer.writer_code.ClassDeclaration('CacheElem', cacheTypeElements, namespaces = [namespace])
        instrParam = cxx_writer.writer_code.Parameter('instr', IntructionTypePtr)
        countParam = cxx_writer.writer_code.Parameter('count', cxx_writer.writer_code.uintType)
        cacheTypeConstr = cxx_writer.writer_code.Constructor(emptyBody, 'pu', [instrParam, countParam], ['instr(instr)', 'count(count)'])
        cacheType.addConstructor(cacheTypeConstr)
        emptyCacheTypeConstr = cxx_writer.writer_code.Constructor(emptyBody, 'pu', [], ['instr(NULL)', 'count(1)'])
        cacheType.addConstructor(emptyCacheTypeConstr)

    ################################################
    # Start declaration of the main processor loop
    ###############################################
    # An here I start declaring the real processor content
    if not model.startswith('acc'):
        if self.instructionCache:
            # Declaration of the instruction buffer for speeding up decoding
            codeString += 'template_map< ' + str(self.bitSizes[1]) + ', CacheElem >::iterator instrCacheEnd = this->instrCache.end();'

        if self.externalClock:
            codeString += 'if(this->waitCycles > 0){\nthis->waitCycles--;\nreturn;\n}\n\n'
        else:
            codeString += 'while(true){\n'
        codeString += 'unsigned int numCycles = 0;\n'

        #Here is the code to deal with interrupts
        codeString += getInterruptCode(self)
        # computes the correct memory and/or memory port from which fetching the instruction stream
        fetchCode = computeFetchCode(self)
        # computes the address from which the nest instruction shall be fetched
        fetchAddress = computeCurrentPC(self, model)
        codeString += str(fetchWordType) + ' curPC = ' + fetchAddress + ';\n'
        # We need to fetch the instruction ... only if the cache is not used or if
        # the index of the cache is the current instruction
        if not (self.instructionCache and self.fastFetch):
            codeString += fetchCode
        if trace:
            codeString += 'std::cerr << \"Current PC: \" << std::hex << std::showbase << curPC << std::endl;\n'

        # Finally I declare the fetch, decode, execute loop, where the instruction is actually executed;
        # Note the possibility of performing it with the instruction fetch
        if self.instructionCache:
            codeString += fetchWithCacheCode(self, fetchCode, trace)
        else:
            codeString += standardInstrFetch(self, trace)

        if self.irqs:
            codeString += '}\n'
        if self.externalClock:
            codeString += 'this->waitCycles += numCycles;\n'
        elif len(self.tlmPorts) > 0 and model.endswith('LT'):
            codeString += 'this->quantKeeper.inc((numCycles + 1)*this->latency);\nif(this->quantKeeper.need_sync()) this->quantKeeper.sync();\n'
        elif model.startswith('acc') or self.systemc or model.endswith('AT'):
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
    ################################################
    # End declaration of the main processor loop
    ###############################################

    # Now I start declaring the other methods and attributes of the processor class

    ##########################################################################
    # Start declaration of begin, end, and reset operations (to be performed
    # at begin or end of simulation or to reset it)
    ##########################################################################
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

    for irqPort in self.irqs:
        initString += 'this->' + irqPort.name + ' = -1;\n'
    resetOpTemp.prependCode(initString)
    if self.beginOp:
        resetOpTemp.appendCode('//user-defined initialization\nthis->beginOp();\n')
    resetOpMethod = cxx_writer.writer_code.Method('resetOp', resetOpTemp, cxx_writer.writer_code.voidType, 'pu')
    processorElements.append(resetOpMethod)
    # Now I declare the end of elaboration method, called by systemc just before starting the simulation
    endElabCode = cxx_writer.writer_code.Code('this->resetOp();')
    endElabMethod = cxx_writer.writer_code.Method('end_of_elaboration', endElabCode, cxx_writer.writer_code.voidType, 'pu')
    processorElements.append(endElabMethod)
    ##########################################################################
    # END declaration of begin, end, and reset operations (to be performed
    # at begin or end of simulation or to reset it)
    ##########################################################################

    # Method for external instruction decoding
    decodeCode = cxx_writer.writer_code.Code("""int instrId = this->decoder.decode(bitString);
            if(instrId >= 0){
                Instruction * instr = Processor::INSTRUCTIONS[instrId];
                instr->setParams(bitString);
                return instr;
            }
            return NULL;
    """)
    decodeParams = [cxx_writer.writer_code.Parameter('bitString', fetchWordType)]
    decodeMethod = cxx_writer.writer_code.Method('decode', decodeCode, IntructionTypePtr, 'pu', decodeParams)
    processorElements.append(decodeMethod)
    if not model.startswith('acc'):
        decoderAttribute = cxx_writer.writer_code.Attribute('decoder', cxx_writer.writer_code.Type('Decoder', 'decoder.hpp'), 'pri')
        processorElements.append(decoderAttribute)
    if self.abi:
        interfaceAttribute = cxx_writer.writer_code.Attribute('abiIf', interfaceType.makePointer(), 'pu')
        processorElements.append(interfaceAttribute)
        interfaceMethodCode = cxx_writer.writer_code.Code('return *this->abiIf;')
        interfaceMethod = cxx_writer.writer_code.Method('getInterface', interfaceMethodCode, interfaceType.makeRef(), 'pu')
        processorElements.append(interfaceMethod)
    toolManagerAttribute = cxx_writer.writer_code.Attribute('toolManager', ToolsManagerType, 'pu')
    processorElements.append(toolManagerAttribute)

    #############################################################################
    # Declaration of all the attributes of the processor class, including, in
    # particular, registers, aliases, memories, etc. The code
    # for their initialization/destruction is also created.
    #############################################################################
    initElements = []
    bodyInits = ''
    bodyDestructor = ''
    aliasInit = {}
    bodyAliasInit = {}
    if self.abi:
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
        if self.abi:
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
        if (regB.constValue and len(regB.constValue) < regB.numRegs)  or ((regB.delay and len(regB.delay) < regB.numRegs) and not model.startswith('acc')):
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
        if self.abi:
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
        if self.abi:
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

        if self.abi:
            abiIfInit += 'this->' + aliasB.name
            if model.startswith('acc'):
                abiIfInit += '_' + checkToolPipeStage.name
            abiIfInit += ', '
        processorElements.append(attribute)
        if model.startswith('acc'):
            for pipeStage in self.pipes:
                attribute = cxx_writer.writer_code.Attribute(aliasB.name + '_' + pipeStage.name, resourceType[aliasB.name].makePointer(), 'pu')
                processorElements.append(attribute)
    if self.abi:
        abiIfInit = abiIfInit[:-2]
    # the initialization of the aliases must be chained (we should
    # create an initialization graph since an alias might depend on another one ...)
    global aliasGraph
    if nxVersion < 0.99:
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
        if nxVersion < 0.99:
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
        if self.memory[2] and not self.systemc and not model.startswith('acc') and not model.endswith('AT'):
            initMemCode += ', totalCycles'
        for memAl in self.memAlias:
            initMemCode += ', ' + memAl.alias
        if self.memory[2] and self.memory[3]:
            initMemCode += ', ' + self.memory[3]
        initMemCode += ')'
        if self.abi and self.memory[0] in self.abi.memories.keys():
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
        if self.abi and tlmPortName in self.abi.memories.keys():
            abiIfInit = 'this->' + tlmPortName + ', ' + abiIfInit
        initElements.append(initPortCode)
        processorElements.append(attribute)
    if self.systemc or model.startswith('acc') or model.endswith('AT'):
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
    if self.abi:
        abiIfInit = 'this->PROGRAM_LIMIT, ' + abiIfInit
    progStarttAttr = cxx_writer.writer_code.Attribute('PROGRAM_START', fetchWordType, 'pu')
    processorElements.append(progStarttAttr)
    bodyInits += 'this->PROGRAM_START = 0;\n'
    if self.abi:
        bodyInits += 'this->abiIf = new ' + str(interfaceType) + '(' + abiIfInit + ');\n'

    instructionsAttribute = cxx_writer.writer_code.Attribute('INSTRUCTIONS',
                            IntructionTypePtr.makePointer(), 'pri', True, 'NULL')
    processorElements.append(instructionsAttribute)
    if self.instructionCache:
        cacheAttribute = cxx_writer.writer_code.Attribute('instrCache',
                        cxx_writer.writer_code.TemplateType('template_map',
                            [fetchWordType, CacheElemType], hash_map_include), 'pri')
        processorElements.append(cacheAttribute)
    numProcAttribute = cxx_writer.writer_code.Attribute('numInstances',
                            cxx_writer.writer_code.intType, 'pri', True, '0')
    processorElements.append(numProcAttribute)

    # Iterrupt ports
    for irqPort in self.irqs:
        if irqPort.tlm:
            irqPortType = cxx_writer.writer_code.Type('IntrTLMPort_' + str(irqPort.portWidth), 'irqPorts.hpp')
        else:
            irqPortType = cxx_writer.writer_code.Type('IntrSysCPort_' + str(irqPort.portWidth), 'irqPorts.hpp')
        from isa import resolveBitType
        irqWidthType = resolveBitType('BIT<' + str(irqPort.portWidth) + '>')
        irqSignalAttr = cxx_writer.writer_code.Attribute(irqPort.name, irqWidthType, 'pri')
        irqPortAttr = cxx_writer.writer_code.Attribute(irqPort.name + '_port', irqPortType, 'pu')
        processorElements.append(irqSignalAttr)
        processorElements.append(irqPortAttr)
        initElements.append(irqPort.name + '_port(\"' + irqPort.name + '_IRQ\", ' + irqPort.name + ')')
    # Generic PIN ports
    for pinPort in self.pins:
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
        pinPortAttr = cxx_writer.writer_code.Attribute(pinPort.name, pinPortType, 'pu')
        processorElements.append(pinPortAttr)
        initElements.append(pinPort.name + '(\"' + pinPort.name + '_PIN\")')

    ####################################################################
    # Cycle accurate model, lets proceed with the declaration of the
    # pipeline stages
    ####################################################################
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
                    curPipeInit = ['this->instrCache'] + curPipeInit
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
    for pinPort in self.pins:
        if not pinPort.inbound:
            baseInstrInitElement += pinPort.name + ', '
    if trace and not self.systemc and not model.startswith('acc'):
        baseInstrInitElement += 'totalCycles, '
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
    if (self.systemc or model.startswith('acc') or len(self.tlmPorts) > 0 or model.endswith('AT')) and not self.externalClock:
        constructorParams.append(cxx_writer.writer_code.Parameter('latency', cxx_writer.writer_code.sc_timeType))
        constructorInit.append('latency(latency)')
    publicConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, constructorInit + initElements)
    destrCode = """Processor::numInstances--;
    if(Processor::numInstances == 0){
        for(int i = 0; i < """ + str(maxInstrId + 1) + """; i++){
            delete Processor::INSTRUCTIONS[i];
        }
        delete [] Processor::INSTRUCTIONS;
        Processor::INSTRUCTIONS = NULL;
    """
    if self.instructionCache:
        destrCode += """template_map< """ + str(fetchWordType) + """, CacheElem >::const_iterator cacheIter, cacheEnd;
        for(cacheIter = this->instrCache.begin(), cacheEnd = this->instrCache.end(); cacheIter != cacheEnd; cacheIter++){
            delete cacheIter->second.instr;
        }
        """
    if self.abi:
        destrCode += 'delete this->abiIf;\n'
    destrCode += '}\n'
    destrCode += bodyDestructor
    destructorBody = cxx_writer.writer_code.Code(destrCode)
    publicDestr = cxx_writer.writer_code.Destructor(destructorBody, 'pu')
    processorDecl = cxx_writer.writer_code.SCModule('Processor', processorElements, namespaces = [namespace])
    processorDecl.addConstructor(publicConstr)
    processorDecl.addDestructor(publicDestr)
    if self.instructionCache:
        return [cacheType, processorDecl]
    else:
        return [processorDecl]

def getGetPipelineStages(self, trace, namespace):
    # Returns the code implementing the class representing a pipeline stage
    pipeCodeElements = []
    pipelineElements = []
    constructorCode = ''
    constructorParamsBase = []
    constructorInit = []
    baseConstructorInit = ''
    pipeType = cxx_writer.writer_code.Type('BasePipeStage')
    IntructionType = cxx_writer.writer_code.Type('Instruction', includes = ['instructions.hpp'])
    registerType = cxx_writer.writer_code.Type('Register', includes = ['registers.hpp'])

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
    pipelineDecl = cxx_writer.writer_code.ClassDeclaration('BasePipeStage', pipelineElements, namespaces = [namespace])
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
        fetchWordType = self.bitSizes[1]

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
        curPipeDecl = cxx_writer.writer_code.SCModule(pipeStage.name.upper() + '_PipeStage', curPipeElements, [pipeType], namespaces = [namespace])
        constructorBody = cxx_writer.writer_code.Code(constructorCode + 'end_module();')
        publicCurPipeConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, constructorInit)
        curPipeDecl.addConstructor(publicCurPipeConstr)
        pipeCodeElements.append(curPipeDecl)

    return pipeCodeElements

#########################################################################################
# Lets complete the declaration of the processor with the main files: one for the
# tests and one for the main file of the simulator itself
#########################################################################################

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

def getMainCode(self, model, namespace):
    # Returns the code which instantiate the processor
    # in order to execute simulations
    wordType = self.bitSizes[1]
    code = 'using namespace ' + namespace + ';\nusing namespace trap;\n\n'
    code += """
    boost::program_options::options_description desc("Processor simulator for """ + self.name + """", 120);
    desc.add_options()
        ("help,h", "produces the help message")
    """
    if self.abi:
        code += """("debugger,d", "activates the use of the software debugger")
        ("profiler,p", boost::program_options::value<std::string>(),
            "activates the use of the software profiler, specifying the name of the output file")
        """
    if self.systemc or model.startswith('acc') or model.endswith('AT'):
        code += """("frequency,f", boost::program_options::value<double>(),
                    "processor clock frequency specified in MHz [Default 1MHz]")
        """
    code += """("application,a", boost::program_options::value<std::string>(),
                                    "application to be executed on the simulator")
               ("disassembler,i", "prints the disassembly of the application")
            """
    if self.abi:
        code += """("arguments,r", boost::program_options::value<std::string>(),
                    "command line arguments (if any) of the application being simulated")
            ("environment,e", boost::program_options::value<std::string>(),
                "environmental variables (if any) visible to the application being simulated")
            ("sysconf,s", boost::program_options::value<std::string>(),
                    "configuration information (if any) visible to the application being simulated")
        """
    code += """;

    std::cerr << std::endl;

    boost::program_options::variables_map vm;
    try{
        boost::program_options::store(boost::program_options::parse_command_line(argc, argv, desc), vm);
    }
    catch(...){
        std::cerr << "ERROR in parsing the command line parametrs" << std::endl << std::endl;
        std::cerr << desc << std::endl;
        return -1;
    }
    boost::program_options::notify(vm);

    // Checking that the parameters are correctly specified
    if(vm.count("help") != 0){
        std::cout << desc << std::endl;
        return 0;
    }
    if(vm.count("application") == 0){
        std::cerr << "It is necessary to specify the application which has to be simulated" << " using the --application command line option" << std::endl << std::endl;
        std::cerr << desc << std::endl;
        return -1;
    }"""
    if (self.systemc or model.startswith('acc') or model.endswith('AT')) and not self.externalClock:
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
    instrDissassName = ''
    if len(self.tlmPorts) > 0:
        code += """//Here we instantiate the memory and connect it
        //wtih the processor
        """
        if model.endswith('LT'):
            code += """MemoryLT<""" + str(len(self.tlmPorts)) + """, """ + str(self.wordSize*self.byteSize) + """> mem("procMem", 1024*1024*10, sc_time(latency*10e9*2, SC_NS));
            """
        else:
            code += """MemoryAT<""" + str(len(self.tlmPorts)) + """, """ + str(self.wordSize*self.byteSize) + """> mem("procMem", 1024*1024*10, sc_time(latency*10e9*2, SC_NS));
            """
        numPort = 0
        for tlmPortName, fetch in self.tlmPorts.items():
            code += 'procInst.' + tlmPortName + '.initSocket.bind(*(mem.socket[' + str(numPort) + ']));\n'
            numPort += 1
            if fetch:
                instrMemName = 'mem'
                instrDissassName = 'procInst.' + tlmPortName
    if instrMemName == '' and self.memory:
        instrMemName = 'procInst.' + self.memory[0]
        instrDissassName = instrMemName

    execOffset = 0
    for pipeStage in self.pipes:
        if pipeStage.checkTools:
            break
        execOffset += 1
    code += """
    //And with the loading of the executable code
    boost::filesystem::path applicationPath = boost::filesystem::system_complete(boost::filesystem::path(vm["application"].as<std::string>(), boost::filesystem::native));
    if ( !boost::filesystem::exists( applicationPath ) ){
        std::cerr << "ERROR: specified application " << vm["application"].as<std::string>() << " does not exist" << std::endl;
        return -1;
    }
    ExecLoader loader(vm["application"].as<std::string>());
    //Lets copy the binary code into memory
    unsigned char * programData = loader.getProgData();
    for(unsigned int i = 0; i < loader.getProgDim(); i++){
        """ + instrMemName + """.write_byte_dbg(loader.getDataStart() + i, programData[i]);
    }
    if(vm.count("disassembler") != 0){
        std:cout << "Entry Point: " << std::hex << std::showbase << loader.getProgStart() << std::endl << std::endl;
        for(unsigned int i = 0; i < loader.getProgDim(); i+= """ + str(self.wordSize) + """){
            Instruction * curInstr = procInst.decode(""" + instrDissassName + """.read_word_dbg(loader.getDataStart() + i));
            std::cout << std::hex << std::showbase << loader.getDataStart() + i << ":    " << """ + instrDissassName + """.read_word_dbg(loader.getDataStart() + i);
            if(curInstr != NULL){
                 std::cout << "    " << curInstr->getMnemonic();
            }
            std::cout << std::endl;
        }
        return 0;
    }
    //Finally I can set the processor variables
    procInst.ENTRY_POINT = loader.getProgStart();
    procInst.PROGRAM_LIMIT = loader.getProgDim() + loader.getDataStart();
    procInst.PROGRAM_START = loader.getDataStart();
    """
    if self.abi:
        code += """
        //Now I initialize the tools (i.e. debugger, os emulator, ...)
        """
        if model.startswith('acc'):
            code += 'OSEmulatorCA< ' + str(wordType) + ', -' + str(execOffset*self.wordSize) + ' > osEmu(*(procInst.abiIf), Processor::NOPInstrInstance, ' + str(self.abi.emulOffset) + ');\n'
        else:
            code += 'OSEmulator< ' + str(wordType) + ', 0 > osEmu(*(procInst.abiIf), ' + str(self.abi.emulOffset) + ');\n'
        code += """GDBStub< """ + str(wordType) + """ > gdbStub(*(procInst.abiIf));
        Profiler< """ + str(wordType) + """ > profiler(*(procInst.abiIf), vm["application"].as<std::string>());

        osEmu.initSysCalls(vm["application"].as<std::string>());
        std::vector<std::string> options;
        options.push_back(vm["application"].as<std::string>());
        if(vm.count("arguments") > 0){
            //Here we have to parse the command line program arguments; they are
            //in the form option,option,option ...
            std::string packedOpts = vm["arguments"].as<std::string>();
            while(packedOpts.size() > 0){
                std::size_t foundComma = packedOpts.find(',');
                if(foundComma != std::string::npos){
                    options.push_back(packedOpts.substr(0, foundComma));
                    packedOpts = packedOpts.substr(foundComma + 1);
                }
                else{
                    options.push_back(packedOpts);
                    break;
                }
            }
        }
        OSEmulatorBase::set_program_args(options);
        if(vm.count("environment") > 0){
            //Here we have to parse the environment; they are
            //in the form option=value,option=value .....
            std::string packedEnv = vm["environment"].as<std::string>();
            while(packedEnv.size() > 0){
                std::size_t foundComma = packedEnv.find(',');
                std::string curEnv;
                if(foundComma != std::string::npos){
                    curEnv = packedEnv.substr(0, foundComma);
                    packedEnv = packedEnv.substr(foundComma + 1);
                }
                else{
                    curEnv = packedEnv;
                    packedEnv = "";
                }
                // Now I have to split the current environment
                std::size_t equalPos = curEnv.find('=');
                if(equalPos == std::string::npos){
                    std::cerr << "Error in the command line environmental options: = not found in option " << curEnv << std::endl;
                    return -1;
                }
                OSEmulatorBase::set_environ(curEnv.substr(0, equalPos), curEnv.substr(equalPos + 1));
            }
        }
        if(vm.count("sysconf") > 0){
            //Here we have to parse the environment; they are
            //in the form option=value,option=value .....
            std::string packedEnv = vm["sysconf"].as<std::string>();
            while(packedEnv.size() > 0){
                std::size_t foundComma = packedEnv.find(',');
                std::string curEnv;
                if(foundComma != std::string::npos){
                    curEnv = packedEnv.substr(0, foundComma);
                    packedEnv = packedEnv.substr(foundComma + 1);
                }
                else{
                    curEnv = packedEnv;
                    packedEnv = "";
                }
                // Now I have to split the current environment
                std::size_t equalPos = curEnv.find('=');
                if(equalPos == std::string::npos){
                    std::cerr << "Error in the command line sysconf options: = not found in option " << curEnv << std::endl;
                    return -1;
                }
                try{
                    OSEmulatorBase::set_sysconf(curEnv.substr(0, equalPos), boost::lexical_cast<int>(curEnv.substr(equalPos + 1)));
                }
                catch(...){
                    std::cerr << "Error in the command line sysconf options: error in option " << curEnv << std::endl;
                    return -1;
                }
            }
        }
        procInst.toolManager.addTool(osEmu);
        if(vm.count("debugger") != 0){
            procInst.toolManager.addTool(gdbStub);
            gdbStub.initialize();
    """
        for tlmPortName in self.tlmPorts.keys():
            code += 'procInst.' + tlmPortName + '.setDebugger(&gdbStub);\n'
        if self.memory:
            code += 'procInst.' + self.memory[0] + '.setDebugger(&gdbStub);\n'
        code += '}\n'
    code += """if(vm.count("profiler") != 0){
                std::set<std::string> toIgnoreFuns = osEmu.getRegisteredFunctions();
                toIgnoreFuns.erase("main");
                profiler.addIgnoredFunctions(toIgnoreFuns);
                procInst.toolManager.addTool(profiler);
            }

    //Now we can start the execution
    boost::timer t;
    sc_start();
    double elapsedSec = t.elapsed();
    if(vm.count("profiler") != 0){
        profiler.printCsvStats(vm["profiler"].as<std::string>());
    }
    std::cout << "Elapsed " << elapsedSec << " sec." << std::endl;
    std::cout << "Executed " << procInst.numInstructions << " instructions" << std::endl;
    std::cout << "Execution Speed " << (double)procInst.numInstructions/(elapsedSec*1e6) << " MIPS" << std::endl;
    """
    if self.systemc or model.startswith('acc') or model.endswith('AT'):
        code += 'std::cout << \"Simulated time \" << ((sc_time_stamp().to_default_time_units())/(sc_time(1, SC_NS).to_default_time_units())) << " ns" << std::endl;\n'
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
    mainCode.addInclude('instructions.hpp')
    mainCode.addInclude('trap_utils.hpp')
    mainCode.addInclude('systemc.h')
    mainCode.addInclude('execLoader.hpp')
    if self.abi:
        mainCode.addInclude('GDBStub.hpp')
        mainCode.addInclude('profiler.hpp')
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
    mainCode.addInclude('string')
    mainCode.addInclude('vector')
    mainCode.addInclude('set')
    parameters = [cxx_writer.writer_code.Parameter('argc', cxx_writer.writer_code.intType), cxx_writer.writer_code.Parameter('argv', cxx_writer.writer_code.charPtrType.makePointer())]
    function = cxx_writer.writer_code.Function('sc_main', mainCode, cxx_writer.writer_code.intType, parameters)
    return function
