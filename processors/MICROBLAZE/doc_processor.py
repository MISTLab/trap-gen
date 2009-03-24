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

## This is 'processor.py' file without the implementation of each method:
## there are only the headers with some comments.
## It can be useful for a quick reference.

import procWriter

validModels = ['funcLT', 'funcAT', 'accAT']

def extractRegInterval(regBankString):
    """Given a string, it check if it specifies an interval
    of registers of a register bank. In case it returns the
    interval, None otherwise. An exception is raised in case
    the string is malformed"""
    


class Register:
    """Register of a processor. It is identified by (a) the
    width in bits, (b) the name. It is eventually possible
    to associate names to the different register fields and
    then refer to them instead of having to use bit masks"""
    def __init__(self, name, bitWidth, bitMask = {}):
       

    def setDefaultValue(self, value):
        

    def setConst(self, value):
        

    def setDelay(self, value):
        

    def setOffset(self, value):
        # TODO: eliminate this restriction
        

    def getCPPClass(self, model, regType):
        

class RegisterBank:
    """Same thing of a register, it also specifies the
    number of registers in the bank. In case register
    fields are specified, they have to be the same for the
    whole bank"""
    def __init__(self, name, numRegs, bitWidth, bitMask = {}):
        

    def setConst(self, numReg, value):
        

    def getConstRegs(self):
        

    def setDelay(self, numReg, value):
        

    def setGlobalDelay(self, value):
        

    def getDelayRegs(self):
        

    def setDefaultValues(self, values):
        

    def setDefaultValue(self, value, position):
        

    def getCPPClass(self, model, regType):
        

class AliasRegister:
    """Alias for a register of the processor;
    actually this is a pointer to a register; this pointer
    might be updated during program execution to point to
    the right register; updating it is responsibility of
    the programmer; it is also possible to directly specify
    a target for the alias"""
    # TODO: it might be a good idea to introduce 0 offset aliases: they are aliases
    # for which it is not possible to use any offset by which are much faster than
    # normal aliases at runtime
    def __init__(self, name, initAlias, offset = 0):
        

    def setDefaultValue(self, value):
       

class MemoryAlias:
    """Alias for a register through a memory address: by reading and writing to the
    memory address we actually read/write to the register"""
    def __init__(self, address, alias):
        

class AliasRegBank:
    """Alias for a register of the processor;
    actually this is a pointer to a register; this pointer
    might be updated during program execution to point to
    the right register; updating it is responsibility of
    the programmer; it is also possible to directly specify
    a target for the alias: in this case the alias is fixed"""
    def __init__(self, name, numRegs, initAlias):
        

    def setOffset(self, regId, offset):

    def setDefaultValues(self, values):

    def setDefaultValue(self, value, position):

class Processor:
    """
    Defined by (a) name (b) endianess (c) wordsize (in terms of
    bytes) (d) bytesize (it is the minimum addressing quantity)
    (e) all the architectural elements here defined (f) the
    behavior for the received interrupt method; note that this
    has to be specified only if there are actually interrupts
    registered (this method is called at every cycle and the content,
    which has to be specified by the user, checks if there are
    interrupts, if they are not masked and takes the appropriate
    action) (g) if we are describing a processor or a coprocessor
    (the different with the coprocessor is that it is not active,
    instructions are passed to it and not actively fetched)
    Three special operations are defined, (1) begin, (2) end
    and (3) reset, used at the begining of the simulation (or
    after a reset), at the end of the simulation and to reset
    the processor.
    The systemc parameter in the constructor specifies whether systemc
    will be used for keeping time or not in the completely
    functional processor in case a local memory is used (in case TLM ports
    are used the systemc parameter is not taken into account)
    """
    def __init__(self, name, version, systemc = True, coprocessor = False, instructionCache = True, fastFetch = False, externalClock = False):
        
    def setISA(self, isa):

    def setMemory(self, name, memSize):

    def addTLMPort(self, portName, fetch = False):
        # Note that for the TLM port, if only one is specified and the it is the
        # port for the fetch, another port called portName + '_fetch' will be automatically
        # instantiated. the port called portName can be, instead, used for accessing normal
        # data

    def setBigEndian(self):

    def setLittleEndian(self):

    def setWordsize(self, wordSize, byteSize = 8):

    def addRegister(self, reg):

    def addRegBank(self, regBank):

    def addAliasReg(self, alias):

    def addAliasRegBank(self, alias):

    def setABI(self, abi):

    def addPipeStage(self, pipe):

    def setBeginOperation(self, code):
        # if is an instance of cxx_writer.CustomCode,
        # containing the code for the behavior
        # If no begin operation is specified, the default
        # values for the registers are used

    def setEndOperation(self, code):
        # if is an instance of cxx_writer.CustomCode,
        # containing the code for the behavior
        # If no end operation is specified, nothing
        # is done

    def setResetOperation(self, code):
        # if is an instance of cxx_writer.CustomCode,
        # containing the code for the behavior
        # if no reset operation is specified, the
        # begin operation is called

    def addIrq(self, irq):

    def addPin(self, pin):

    def setFetchRegister(self, fetchReg,  offset = 0):
        # Sets the correspondence between the fetch address
        # and a register inside the processor

    def addMemAlias(self, memAlias):

    def isRegExisting(self, name, index = None):

    def isBank(self, bankName):

    def setWBOrder(self, regName, order):

    def checkPipeStages(self):
    	
    def checkAliases(self):
        # checks that the declared aliases actually refer to
        # existing registers
        
    def checkISARegs(self):
        # Checks that registers declared in the instruction encoding and the ISA really exists
        
    def checkABI(self):
        # checks that the registers specified for the ABI interface
        # refer to existing registers
        

    def getCPPRegisters(self, model):
        # This method creates all the classes necessary for declaring
        # the registers: in particular the register base class
        # and all the classes for the different bitwidths

    def getRegistersBitfields(self):

    def getCPPAlias(self, model):
        # This method creates the class describing a register
        # alias

    def getCPPProc(self, model, trace):
        # creates the class describing the processor

    def getCPPMemoryIf(self, model):
        # creates the class describing the processor

    def getCPPIf(self, model):
        # creates the interface which is used by the tools
        # to access the processor core

    def getCPPExternalPorts(self, model):
        # creates the processor external ports used for the
        # communication with the external world (the memory port
        # is not among this ports, it is treated separately)

    def getTestMainCode(self):
        # Returns the code for the file which contains the main
        # routine for the execution of the tests.
        # actually it is nothing but a file which includes
        # boost/test/auto_unit_test.hpp and defines
        # BOOST_AUTO_TEST_MAIN and BOOST_TEST_DYN_LINK

    def getMainCode(self, model):
        # Returns the code which instantiate the processor
        # in order to execute simulations

    def getGetIRQPorts(self):
        # Returns the code implementing the interrupt ports

    def getGetPipelineStages(self, trace):
        # Returns the code implementing the pipeline stages

    def write(self, folder = '', models = validModels, dumpDecoderName = '', trace = False):
        # Ok: this method does two things: first of all it performs all
        # the possible checks to ensure that the processor description is
        # coherent. Second it actually calls the write method of the
        # processor components (registers, instructions, etc.) to create
        # the code of the simulator
       
        
class PipeStage:
    """Identified by (a) name (b) optional, if it is wb,
    the stage where the hazards are checked or where the
    bypassing is started. Note that this is just the default
    information which can be overridden by each instruction"""
    def __init__(self, name):

    def setCheckTools(self):

    def setWriteBack(self):

    def setHazard(self):

    def setEndHazard(self):

    def setCheckUnknownInstr(self):

class Coprocessor:
    """Specifies the presence of a specific coprocessor; in particular
    it specifies what are the instructions of the ISA (already defined
    instructions) which are coprocessor instructions and for each of
    them it specifies what is the co-processor method which must be called
    note that also the necessary include file must be provided.
    it also specifies the bits which identify if the instruction if
    for this coprocessor or not.
    Alternatively a custom behavior can be provided, which will be
    executed instead of the method call.
    Note that the coprocessor name must be given: the processor will
    contain a variable with this name; this variable will have to
    be initialized to the instance of the coprocessor (by calling a
    special method addCoprocessor ....) Note that the coprocessor
    might need to access the Integer unit to read or set some registers.
    This can either be done by passing a reference to the Ingeter Unit
    registers to the coprocessor at construction or by using the custom
    behavior in each co-processor instruction"""
    # TODO: an accurate interface is also needed. This means that
    # we need to define control signals and pins for the communication
    # between the processor and the coprocessor
    def __init__(self, name, type):
        # Specifies the name of the coprocessor variable in the
        # processor. It also specifies its type

    def addIsaCustom(self, name, code, idBits):
        # Specifies that ISA instruction with name name
        # is a co-processor instruction and that
        # custom code is provided if the instruction is for
        # this coprocessor. idBits specifies what it the
        # value of the bits which specify if the instruction
        # is for this co-processor or not

    def addIsaCall(self, name, functionName, idBits):
        # Specifies that ISA instruction with name name
        # is a co-processor instruction and that
        # a function call is provided if the instruction is for
        # this coprocessor. idBits specifies what it the
        # value of the bits which specify if the instruction
        # is for this co-processor or not

class Interrupt:
    """Specifies an interrupt port for the processor. It is identified by
    (a) name (b) edge or level triggered (c) if systemC port or TLM
    port will be used (d) if rising edge or active on high or low level
    (e) also a priority is associated to the interrupt;
    the higher priprity have precedence over low priorities.
    Note that I will render both systemc and TLM ports as systemc
    signals: there is a check interrupts routine which will be
    called every cycle, in which the user can check the IRQs and
    take the appropriate actions. The signal will be automatically
    raised, lowered etc... depending whether edge triggered, level etc.."""
    def __init__(self, name, tlm = True, level = True, high = True, priority = 0):

    def setOperation(self, condition, operation):

class Pins:
    """Custom pins; checking them or writing to them is responsibility of
    the programmer. They are identified by (a) name (b) type. They are
    rendered with systemc ports"""
    def __init__(self, name, type):
        # Note how the type of the must be of class cxx_writer.Type; a
        # systemc port using this type as a template will be created

class ABI:
    """Defines the ABI for the processor: this is necessary both for
    the systemcalls implementation and for the gcc retargeting
    We need to specify in which register the return value is written,
    which are the registers holding the parameters of the call.
    I also have to specify the function prologue and epilogue, where
    the address of the previous execution path is saved, how to branch
    to a fixed address (here we can also reference instructions of
    the ISA).
    The correspondence between the real architectural elements
    and the variables of the simulator must be defined: I have to
    list all the registers as seen (for example) by GDB,
    so (0-n), and then to refer to variables I can either specify
    register name, registry bank with indexes, constants.
    I have to specify the program counter, sp, lr, fp.
    Note that for each of these correspondences I can also specify
    an offset (in the sense that PC can be r15 + 8 for ex).
    """
    def __init__(self, retVal, args, PC, LR = None, SP = None, FP = None):

    def addVarRegsCorrespondence(self, correspondence):

    def setOffset(self, register, offset):

    def addMemory(self, memory, addr = ()):

