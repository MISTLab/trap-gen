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

def getCPPRegClass(self, model):
    # returns the class implementing the current register
    return None

def getCPPRegBankClass(self, model):
    # returns the class implementing the single register of
    # the register bank
    return None

def getCPPRegisters(self, model):
    # This method creates all the classes necessary for declaring
    # the registers: in particular the register base class
    # and all the classes for the different bitwidths; in order to
    # do this I simply iterate over the registers
    classes = []
    for regs in self.regs + self.regBanks:
        classes.append(regs.getCPPClass(model))
    return classes

def getCPPAlias(self, model):
    # This method creates the class describing a register
    # alias
    return None

def getCPPMemoryIf(self, model):
    # Creates the necessary structures for communicating with the memory; an
    # array in case of an internal memory, the TLM port for the use with TLM
    # etc.
    return None

def getCPPProc(self, model):
    # creates the class describing the processor
    from isa import resolveBitType
    fetchWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize) + '>')
    includes = fetchWordType.getIncludes()
    codeString = 'while(true){\n'
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
    decoderAttribute = cxx_writer.writer_code.Attribute('decoder', cxx_writer.writer_code.Type('Decoder', 'decoder.hpp'), 'pri')
    processorElements.append(decoderAttribute)
    if self.systemc or model.startswith('acc'):
        # Here we need to insert the quantum keeper etc.
        pass
    else:
        totCyclesAttribute = cxx_writer.writer_code.Attribute('totalCycles', cxx_writer.writer_code.uintType, 'pu')
        processorElements.append(totCyclesAttribute)
    IntructionType = cxx_writer.writer_code.Type('Instruction', include = 'instruction.hpp')
    IntructionTypePtr = IntructionType.makePointer()
    instructionsAttribute = cxx_writer.writer_code.Attribute('INSTRUCTIONS',
                            IntructionTypePtr, 'pri', True, 'NULL')
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
    if self.memory:
        # Here we need to create and instance of the memory
        constrCode += '//Creating the memory instance'
    # TODO: Finally we initialize the instances of the other architectural elements
    if self.systemc or model.startswith('acc'):
        # TODO: We also need to initialize the quantuum keeper etc
        constrCode += 'SC_THREAD(mainLoop);\n'
    else:
        constrCode += 'this->totalCycles = 0;'
    constrCode += 'end_module();'
    constructorBody = cxx_writer.writer_code.Code(constrCode)
    constructorParams = [cxx_writer.writer_code.Parameter('name', cxx_writer.writer_code.sc_module_nameType), 
                cxx_writer.writer_code.Parameter('latency', cxx_writer.writer_code.sc_timeType)]
    publicConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, ['sc_module(name)'])
    destrCode = """Processor::numInstances--;
    if(Processor::numInstances == 0){
        for(int i = 0; i < """ + str(maxInstrId + 1) + """; i++){
            delete Processor::INSTRUCTIONS[i];
        }
        delete [] Processor::INSTRUCTIONS;
        Processor::INSTRUCTIONS = NULL;
    }
    """
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

def getTestMainCode(self):
    # Returns the code for the file which contains the main
    # routine for the execution of the tests.
    # actually it is nothing but a file which includes
    # boost/test/auto_unit_test.hpp and defines
    # BOOST_AUTO_TEST_MAIN and BOOST_TEST_DYN_LINK
    code = '#define BOOST_AUTO_TEST_MAIN\n#define BOOST_TEST_DYN_LINK\n#include <boost/test/auto_unit_test.hpp>'
    mainCode = cxx_writer.writer_code.Code(code)
    return mainCode

