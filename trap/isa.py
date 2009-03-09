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

import re
import cxx_writer
import isaWriter

def resolveBitType(typeString):
    """Given a string representing a bit type it returns the more appropriate C++ type
    for the representation of such a type"""
    if not isinstance(typeString, type('')):
        raise Exception(str(typeString) + ' Wrong variable type')
    validBitType = '^( )*BIT( )*<( )*[0-9]+( )*>( )*$'
    if not re.match(validBitType, typeString):
        raise Exception(str(typeString) + ' Wrong variable type: the custom bit types must have the stucture \"BIT < BITWIDTH >\"')
    # Now I can finally get the bitwidth
    bitWidthRe = re.search('[0-9]+', typeString)
    if not bitWidthRe:
        raise Exception(str(typeString) + ' Wrong variable type: the custom bit types must have the stucture \"BIT < BITWIDTH >\"')
    bitWidth = int(typeString[bitWidthRe.start():bitWidthRe.end()])
    # Now I have to take decisions based on the bit-width and on the host machine in order
    # to generate the appropriate variable; performance reasons can also affect the decision.
    # In particular we decide that:
    # 32 BIT: unsigned int
    # 64 bit: unsigned long long
    # 1 bit: bool
    # 16 bit: unsigned short
    # the other bit-width are described using SystemC types; also in case the host machine
    # does not respect the cited convention I use SystemC types also for the basic bit width.
    if bitWidth == 32:
        return cxx_writer.writer_code.uintType
    elif bitWidth == 64:
        return cxx_writer.writer_code.sc_uint64Type
    elif bitWidth == 8:
        return cxx_writer.writer_code.ucharType
    elif bitWidth == 1:
        return cxx_writer.writer_code.boolType
    elif bitWidth == 16:
        return cxx_writer.writer_code.ushortType
    else:
        if bitWidth/8 <= tuple.__itemsize__:
            return cxx_writer.writer_code.TemplateType('sc_dt::sc_uint', str(bitWidth), 'systemc.h')
        else:
            return cxx_writer.writer_code.TemplateType('sc_dt::sc_biguint', str(bitWidth), 'systemc.h')

class ISA:
    """This class represents the instruction set of a processor;
    it mainly contains a list of instructions (each one with the
    coding, the behavior ...). It also contains the methods for
    transforming the instructions into the C++ code which
    implements them"""
    def __init__(self):
        self.instructions = {}
        self.helperOps = []
        self.methods = []
        self.beginOp = None
        self.endOp = None
        self.subInstructions = {}
        self.constants = []

    def addConstant(self, varType, name, value):
        self.constants.append((varType, name, value))

    def addInstruction(self, instruction):
        if self.instructions.has_key(instruction.name):
            raise Exception('Instruction with name ' + instruction.name + ' already present in the ISA')
        instruction.id = len(self.instructions)
        self.instructions[instruction.name] = instruction

    def addOperation(self, operation):
        if operation.instrvars:
            raise Exception('Operation ' + operation.name + ' contains instruction variables, but this is not allowed for operations not assegned to a particular instruction')
        for i in self.helperOps + self.methods:
            if i.name == operation.name:
                raise Exception('Operation ' + operation.name + ' already added to the ISA')
        operation.numUsed += 1
        self.helperOps.append(operation)

    def addMethod(self, method):
        for i in self.methods + self.helperOps:
            if i.name == method.name:
                raise Exception('Method ' + method.name + ' already added to the ISA')
        self.methods.append(method)

    def addBeginOp(self, operation):
        # Operation executed at the beginning of every instruction
        # TODO: do we need to access the fields of the instructions? if so
        # which? the ones which have the same name and same position in all
        # the instructions?
        for i in self.helperOps + self.methods:
            if i.name == operation.name:
                raise Exception('Operation ' + operation.name + ' already added to the ISA')
        self.beginOp = operation

    def addEndOp(self, operation):
        # Operation executed at the end of every instruction
        # TODO: as for the begin op, do we need to access any
        # of the instruction fields?
        for i in self.helperOps + self.methods:
            if i.name == operation.name:
                raise Exception('Operation ' + operation.name + ' already added to the ISA')
        self.endOp = operation

    def computeCoding(self):
        # for each instruction it puts together the machine code
        # and the identifier bits to create the instruction bitstring
        for instr in self.instructions.values():
            for i in range(0, instr.machineCode.instrLen):
                instr.bitstring.append(None)
            for fieldName in instr.machineCode.bitFields:
                if instr.machineCode.bitValue.has_key(fieldName[0]):
                    curPos = 0
                    for i in instr.machineCode.bitValue[fieldName[0]]:
                        instr.bitstring[instr.machineCode.bitPos[fieldName[0]] + curPos] = i
                        curPos += 1
                elif instr.machineBits.has_key(fieldName[0]):
                    curPos = 0
                    for i in instr.machineBits[fieldName[0]]:
                        instr.bitstring[instr.machineCode.bitPos[fieldName[0]] + curPos] = i
                        curPos += 1

    def checkCoding(self):
        checked = []
        for i in self.instructions.values():
            for j in self.instructions.values():
                if i != j:
                    if not sorted((i.id,j.id)) in checked:
                        checked.append(sorted((i.id,j.id)))
                        minLen = min(len(i.bitstring), len(j.bitstring))
                        equal = True
                        for bit in range(0, minLen):
                            if i.bitstring[bit] != None and j.bitstring[bit] != None:
                                if i.bitstring[bit] != j.bitstring[bit]:
                                    equal = False
                                    break
                        if equal:
                            if i.subInstr and j.subInstr:
                                raise Exception('Instructions ' + i.name + ' and ' + j.name + ' have an ambiguous coding and both of them are classified as sub-instructions: hierarchical sub-instructions are not allowed')
                            if i.subInstr:
                                for bit in range(0, minLen):
                                    if j.bitstring[bit] != None and j.bitstring[bit] != i.bitstring[bit]:
                                        raise Exception('Instruction ' + str(i) + ' has a coding clash with ' + str(j) + ' but it is not a sub-instruction of it')
                                self.subInstructions[i.name] = i
                                j.subInstructions.append(i)
                            elif j.subInstr:
                                for bit in range(0, minLen):
                                    if i.bitstring[bit] != None and i.bitstring[bit] != j.bitstring[bit]:
                                        raise Exception('Instruction ' + str(j) + ' has a coding clash with ' + str(i) + ' but it is not a sub-instruction of it')
                                self.subInstructions[j.name] = j
                                i.subInstructions.append(j)
                            else:
                                raise Exception('Coding of instructions ' + str(i) + ' and ' + str(j) + ' is ambiguous')

    def checkRegisters(self, indexExtractor, checkerMethod):
        # Checks that all the registers used in the instruction encoding are
        # existing and part of the architecture. It also check that there are
        # no name collisions among the registers, aliases and instruction
        # variables
        toCheck = []
        for i in self.instructions.values():
            # check the machine code: the var fields must be existing registers
            for reg in i.machineCode.bitCorrespondence.values():
                if not reg in toCheck:
                    if isinstance(reg, type('')):
                        toCheck.append(reg)
                    else:
                        toCheck.append(reg[0] + '[' + str(reg[1]) + ']')
            # check the instruction variables: there must be no collision with
            # the register names
            for var in i.variables:
                if checkerMethod(var.name):
                    raise Exception('Variable ' + var.name + ' in insturction ' + i.name + ' has trhe same name of a processor register')
                if checkerMethod(var.name, (0, 0)):
                    raise Exception('Variable ' + var.name + ' in insturction ' + i.name + ' has trhe same name of a processor register bank')
        for reg in toCheck:
            index = indexExtractor(reg)
            if index:
                # I'm aliasing part of a register bank or another alias:
                # I check that it exists and that I am still within
                # boundaries
                refName = reg[:reg.find('[')]
                if not checkerMethod(refName, index):
                    raise Exception('Register Bank ' + reg + ' used in the MachineCode description does not exists')
            else:
                # Single register or alias: I check that it exists
                if not checkerMethod(reg):
                    raise Exception('Register ' + reg + ' used in the MachineCode description does not exists')

    def getCPPClasses(self, processor, model, trace):
        return isaWriter.getCPPClasses(self, processor, model, trace)

    def getCPPTests(self, processor, model):
        return isaWriter.getCPPTests(self, processor, model)

class Instruction:
    """Represents an instruction of the processor. The instruction
    is characterized by (a) machine code (b) behavior (both in terms
    of explicit behavior and of helper operations); the behavior
    is separated among the pipeline stages (c) abstract
    behavior (as needed for the retargeting of gcc) (d) timing
    details for each pipeline stage (they can be expressed in
    function of the variables for that stage or of the global
    instruction variables) (e) if the instruction is for the
    coprocessor (f) if this instruction can modify the program
    counter. Optionally a documentation string
    can be provided, describing the instruction behavior.
    Note that also I have to specify which are the pipeline
    stage for which I stall waiting for hazards, where the wb
    occurs and where I can start the bypassing in case (this
    if the defaults for the pipeline are not used). Note that
    it is possible to specify some behaviors as being only present
    in the cycle accurate processor and not in the functional one
    (useful for branch prediction for example)
    Also forwardging can be disabled by the instruction"""
    def __init__(self, name, modifyPc = True, isCoprocessor = False, frequency = 1):
        self.name = name
        # Estimated frequency of the instruction. It is used to build the decoder.
        # the more the frequency repspects the real frequency of the instruction
        # in the better will be the decoder
        if frequency < 1:
            raise Exception('Error in the frequency value for instruction ' + name + ': it has to be a non-zero positive integer number')
        self.frequency = frequency
        # Instruction id; note that the ID is automatically assigned to
        # the instruction by the ISA class
        self.id = 0;
        # Note how the code and the behavior is specified
        # for each pipeline stage
        self.prebehaviors = {}
        self.postbehaviors = {}
        self.code = {}
        self.isCoprocessor = isCoprocessor
        self.modifyPc = modifyPc
        # List of variables which are global to this instruction
        # these variables are instances of the variables class as
        # contained in cxx_writer.SimpleDecls
        self.variables = []
        self.docString = ''
        self.machineCode = None
        self.machineBits = None
        # stages at which I check for hazards
        self.hazardStage = ''
        self.wbStage = ''
        # The bits of the machine code of the instruction; the elements of
        # this list can be 0, 1 or None (don't care)
        self.bitstring = []
        # Some testing information: each element of the list
        # represents a test. For each test there are three maps:
        # name of the instruction variables and their values,
        # name of the resource and value to set in the second map and name
        # of the resource and value that we expect to have in the third.
        # For cycle accurate models, we execute the whole behavior at once
        # (no timing test is done)
        # Among the resources, MEM[ADDR] representes the memory at a
        # particular address
        self.tests = []
        self.mnemonic = None
        # Finally, these information are used for
        # gcc retargeting:
        # This is the name of the pattern as recognized by
        # gcc. There is a fixed list of names recognized by gcc,
        # for more informations look http://gcc.gnu.org/onlinedocs/gccint/index.html#toc_Machine-Desc
        self.templateString = ''
        # In addition to the template string we need to know how each
        # templateString reflects in the assembly of the target
        # architecture. This information should be automatically derived
        # from the machineCode
        # Parts of the machine code which are valid only for this instrucion
        self.bitCorrespondence = {}
        self.bitDirection = {}
        # Registers which are read or written in addition to registers which are
        # part of the instruction econding (usually these are the special processor
        # registers)
        self.specialInRegs = []
        self.specialOutRegs = []
        # Specifies if the coding of this instruction is a special case of a more general
        # instruction
        self.subInstr = False
        # List of instruction which are subInstructions of the current one
        self.subInstructions = []
        # Specifies the list of behaviors that have to be printed respectively to the
        # functiona and cycle accurate models
        self.behaviorAcc = []
        self.behaviorFun = []


    def setMachineCode(self, machineCode, machineBits = {}, mnemonic = [], subInstr = False):
        # Sets the machine code for this instruction. Note that a machine
        # code may be generic for groups of instructions: the
        # machine bits are a specialization of it. machineBits
        # is a map: name of the field and bit string which
        # sets the value of that field
        self.subInstr = subInstr
        # Now I check that the mnemonic is valid all the parts starting with % must be existing in the current
        # machine code
        bitFieldNames = []
        for i in machineCode.bitFields:
            bitFieldNames.append(i[0])
        for i in mnemonic:
            if type(i) == type(''):
                if i.startswith('%'):
                    if not i[1:] in bitFieldNames:
                        raise Exception('The machine code for instruction ' + self.name + ' does not contain field ' + i[1:] + ' specified in the mnemonic')
            else:
                if not i[0].startswith('%'):
                    raise Exception('The mnemonic for instruction ' + self.name + ' have the first element ' + i[0][1:] + ' of a multi-variable mnemonic with does not start with %')
                if not i[0][1:] in bitFieldNames:
                    raise Exception('The machine code for instruction ' + self.name + ' does not contain field ' + i[0][1:] + ' specified in the mnemonic')
        self.mnemonic = mnemonic
        if self.machineCode or self.machineBits:
            raise Exception('The machine code for instruction ' + self.name + ' has already been added')
        for i in machineBits.keys():
            found = False
            for k in machineCode.bitFields:
                if k[0] == i:
                    found = True
                    break
            if not found:
                raise Exception('Field ' + i + ' not found in the machine code for instruction ' + self.name)
            if i in machineCode.bitValue.keys() or i in  machineCode.bitCorrespondence.keys():
                raise Exception('Field ' + i + ' already specified in the machine code for instruction ' + self.name)
        self.machineCode = machineCode
        self.machineBits = machineBits
        for behavior in self.postbehaviors.values() + self.prebehaviors.values():
            newProcElem = []
            for procElem in behavior.archElems:
                found = False
                for key, fieldLen in self.machineCode.bitFields:
                    if key == procElem:
                        found = True
                        break
                if not found:
                    raise Exception('Error, architectural element ' + procElem + ' specified in operation ' + behavior.name + ' is not present in the machine code of instruction ' + self.name)
                # Finally I separate the elements which are really constant from those which are, instead,
                # only variable parts of the instruction
                if procElem in self.machineCode.bitCorrespondence.keys():
                    newProcElem.append(procElem)
                elif not procElem in behavior.archVars:
                    behavior.archVars.append(procElem)
            behavior.archElems = newProcElem

    def addBehavior(self, behavior, stage, pre = True, accurateModel = True, functionalModel = True):
        # adds a behavior (an instance of the class HelperOperation)
        if accurateModel:
            self.behaviorAcc.append(behavior.name)
        if functionalModel:
            self.behaviorFun.append(behavior.name)
        if pre:
            if self.prebehaviors.has_key(stage):
                self.prebehaviors[stage].append(behavior)
            else:
                self.prebehaviors[stage] = [behavior]
        else:
            if self.postbehaviors.has_key(stage):
                self.postbehaviors[stage].append(behavior)
            else:
                self.postbehaviors[stage] = [behavior]

        behavior.numUsed += 1
        for var in behavior.instrvars:
            for instrVar in self.variables:
                if var.name == instrVar.name:
                    if var.type.name != instrVar.type.name:
                        raise Exception('A Helper Operation is trying to add variable ' + var.name + ' of type ' + var.type.name + ' to instruction ' + self.name + ' which already has a variable with such a name of type ' + instrVar.type.name)
                else:
                    self.variables.remove(instrVar)
                    break
        if self.machineCode:
            newProcElem = []
            for procElem in behavior.archElems:
                found = False
                for key, fieldLen in self.machineCode.bitFields:
                    if key == procElem:
                        found = True
                        break
                if not found:
                    raise Exception('Error, architectural element ' + procElem + ' specified in operation ' + behavior.name + ' is not present in the machine code of instruction ' + self.name)
                if procElem in self.machineCode.bitCorrespondence.keys():
                    newProcElem.append(procElem)
                elif not procElem in behavior.archVars:
                    behavior.archVars.append(procElem)
            behavior.archElems = newProcElem

    def setCode(self, code, stage):
        # code is simply a string containing the code
        # Code must be an instance of cxx_writer.CustomCode
        if self.code.has_key(stage):
            raise Exception('The code for instruction ' + self.name + ' for stage ' + stage + ' has already been added')
        self.code[stage] = code

    def addVariable(self, variable):
        # adds a variable global to the instruction; note that
        # variable has to be an instance of cxx_writer.Variable
        if isinstance(variable, type(())):
            variable = cxx_writer.writer_code.Variable(variable[0], resolveBitType(variable[1]))
        for instrVar in self.variables:
            if variable.name == instrVar.name:
                if variable.type.name != instrVar.type.name:
                    raise Exception('Trying to add variable ' + variable.name + ' of type ' + variable.type.name + ' to instruction ' + self.name + ' which already has a variable with such a name of type ' + instrVar.type.name)
        self.variables.append(variable)

    def setVarField(self, name, correspondence, bitDir = 'inout'):
        if not self.machineCode:
            raise Exception('The machine code for instruction ' + self.name + ' must be set before calling method ' + setVarField)
        found = False
        for i in self.machineCode.bitFields:
            if name == i[0]:
                found = True
                break
        if not found:
            raise Exception('Machine code for instruction ' + self.name + ' does not have field ' + name + '; error in trying to set the correspondencce with ' + str(correspondence))
        if self.machineCode.bitCorrespondence.has_key(name):
            raise Exception('Correspondence for field ' + name + ' already set in machine code, unable to set correspondence for instruction ' + self.name)
        if self.bitCorrespondence.has_key(name):
            raise Exception('Correspondence for field ' + name + ' already set in instruction ' + self.name)
        if self.machineCode.bitValue.has_key(name):
            raise Exception('Value for bitfield ' + name + ' already set in machine code, unable to set correspondence for instruction ' + self.name)
        self.bitCorrespondence[name] = correspondence
        self.bitDirection[name] = bitDir.lower()


    def addDocString(self, docString):
        self.docString += docString + '\n'

    def setPipeProperties(self, hazardStage = '', wbStage = ''):
        # Sets the stage in which the checks for hazards are performed,
        self.hazardStage = hazardStage
        self.wbStage = wbStage

    def setTemplateString(self, templateString):
        # This information is used for gcc retargeting.
        raise Exception('GCC Retargeting not yet supported')
        self.templateString = templateString

    def addSpecialRegister(self, regName, direction = 'inout'):
        if direction in ['inout', 'in']:
            self.specialInRegs.append(regName)
        if direction in ['inout', 'out']:
            self.specialOutRegs.append(regName)
        if not direction in ['inout', 'out', 'in']:
            raise Exception(str(direction) + ' is  not valid; valid values are: \'inout\', \'in\', and \'out\'')

    def addTest(self, variables, input, expOut):
        # input and expected output are two maps, each one containing the
        # register name and its value. if the name of the resource corresponds
        # to one one of the memories, then the value in brackets is the
        # address
        # TODO: think about the possbility of also changing what the aliases
        # point to
        self.tests.append((variables, input, expOut))

    def __repr__(self):
        return self.name + ' coding: ' + str(self.bitstring)

    def __str__(self):
        return repr(self)

    def getCPPClass(self, model, processor, trace):
        return isaWriter.getCPPInstr(self, model, processor, trace)

    def getCPPTest(self, processor, model):
        return isaWriter.getCPPInstrTest(self, processor, model)

class HelperOperation:
    """Represents some code; this code can be shared among the
    instructions, in the sense that it can be part of more than
    one instruction. The code can reference its variables or the
    variables of the instructions it is associated to (note that
    all the instructions this piece of code is associated to must
    have the referenced variables)"""
    def __init__(self, name, code, inline = True, model = 'all'):
        # Code must be an instance of cxx_writer.CustomCode. Note
        # that even if inline is specified, in case this operation
        # is used only one, its code is directly put inside the
        # instruction itself and not in a separate function
        self.name = name
        self.code = code
        self.inline = inline
        self.numUsed = 0
        self.localvars = []
        self.instrvars = []
        self.archElems = []
        self.archVars = []
        validModel = ['all', 'func', 'acc']
        # Now we check which model has to include the operation
        if not model in validModel:
            raise Exception('Not valid model: it must be one of: ' + str(validModel))
        self.model = model

    def addVariable(self, variable):
        # adds a variable global to the operation; note that
        # variable has to be an instance of cxx_writer.Variable
        if isinstance(variable, type(())):
            variable = cxx_writer.writer_code.Variable(variable[0], resolveBitType(variable[1]))
        for instrVar in self.localvars + self.instrvars:
            if variable.name == instrVar.name:
                if variable.type.name != instrVar.type.name:
                    raise Exception('Trying to add variable ' + variable.name + ' of type ' + variable.type.name + ' to operation ' + self.name + ' which already has a variable with such a name of type ' + instrVar.type.name)
        self.localvars.append(variable)

    def addInstuctionVar(self, variable):
        # adds a variable global to the all instructions containig this operation;
        # note that variable has to be an instance of cxx_writer.Variable
        if isinstance(variable, type(())):
            variable = cxx_writer.writer_code.Variable(variable[0], resolveBitType(variable[1]))
        for instrVar in self.instrvars + self.localvars:
            if variable.name == instrVar.name:
                if variable.type.name != instrVar.type.name:
                    raise Exception('Trying to add variable ' + variable.name + ' of type ' + variable.type.name + ' to operation ' + self.name + ' which already has a variable with such a name of type ' + instrVar.type.name)
        self.instrvars.append(variable)

    def addUserInstructionElement(self, archElem):
        # adds an instruction element to this instruction: this is necessary in case
        # the current operation needs to access the field of a machine code
        self.archElems.append(archElem)

    def getCppOperation(self, parameters = False):
        # returns the cpp code implementing the current method
        return isaWriter.getCppOperation(self, parameters)

    def getCppOpClass(self):
        # Relturn a CPP class, deriving from Instruction,
        # implementing a method which defines the current
        # oepration
        return isaWriter.getCppOpClass(self)

    def __repr__(self):
        return self.name

    def __str__(self):
        return repr(self)

class HelperMethod:
    """Represents a fucntion which can be shared among the
    instructions. This function can be called from all
    the instructions and other helper operations"""
    def __init__(self, name, code, stage):
        # Code must be an instance of cxx_writer.CustomCode.
        self.name = name
        self.code = code
        self.stage = stage
        self.localvars = []
        self.parameters = []
        self.retType = cxx_writer.writer_code.Type('void')

    def addVariable(self, variable):
        # adds a variable global to the operation; note that
        # variable has to be an instance of cxx_writer.Variable
        if isinstance(variable, type(())):
            variable = cxx_writer.writer_code.Variable(variable[0], resolveBitType(variable[1]))
        for instrVar in self.localvars:
            if variable.name == instrVar.name:
                if variable.type.name != instrVar.type.name:
                    raise Exception('Trying to add variable ' + variable.name + ' of type ' + variable.type.name + ' to operation ' + self.name + ' which already has a variable with such a name of type ' + instrVar.type.name)
        for param in self.parameters:
            if variable.name == param.name:
                raise Exception('Trying to add parameter ' + param.name + ' to operation ' + self.name + ' which already has a variable with such a name')
        self.localvars.append(variable)

    def setSignature(self, retType = cxx_writer.writer_code.Type('void'), parameters = []):
        # sets the signature for the method; the return type has to be an instance of
        # cxx_writer.Type or a string representing a bit type, while the parameters
        #  can either be cxx_writer.Parameter or a string representing a bit type
        if isinstance(retType, type('')):
            self.retType = resolveBitType(retType)
        else:
            self.retType = retType
        for param in parameters:
            if isinstance(param, type(())):
                param = cxx_writer.writer_code.Parameter(param[0], resolveBitType(param[1]))

            for instrVar in self.localvars:
                if param.name == instrVar.name:
                    raise Exception('Trying to add parameter ' + param.name + ' to operation ' + self.name + ' which already has a variable with such a name')
            for lparam in self.parameters:
                if param.name == lparam.name:
                    raise Exception('Trying to add parameter ' + param.name + ' to operation ' + self.name + ' which already has a parameter with such a name')
            self.parameters.append(param)

    def getCppMethod(self, model, processor):
        # returns the cpp code implementing the current method
        return isaWriter.getCppMethod(self, model, processor)

    def __repr__(self):
        return self.name

    def __str__(self):
        return repr(self)

class MachineCode:
    """Represents the coding of a group of instruction; it contains
    (b) the value of the bits which identify this
    instruction (or group of) (c) correspondence between instruction
    elements and processor components (e.g. the bits which identify registers
    in the register bank, immediate values) (d) variables of the
    instruction (i.e. we associate variable names to part of the
    machine code) (e) if immediates are offset
    (f) mode (for example the ARM has normal and thumb
    mode). Node that, for each mode, the instruction length has to
    be the same."""
    # We can identify two types of correspondences between processors
    # elements and instruction fields: index (as for reg banks) and
    # switch. Note that the index access may also have offsets
    def __init__(self, bitFields, mode = ''):
        self.mode = mode
        self.bitFields = []
        self.bitValue = {}
        self.bitPos = {}
        self.bitLen = {}
        self.bitDirection = {}
        self.instrLen = 0
        curPosition = 0
        for key, fieldLen in bitFields:
            if key.lower() in ['zero', 'one']:
                while self.bitPos.has_key(key):
                    key = key + '_d'
            if self.bitPos.has_key(key):
                raise Exception('Machine code cannot contain duplicate fields (a part from zero and one fields.). ' + key + ' is duplicatede')
            self.bitLen[key] = fieldLen
            self.bitFields.append((key, fieldLen))
            self.bitPos[key] = curPosition
            curPosition += fieldLen
            self.instrLen += fieldLen
            if key.lower().startswith('zero'):
                fieldVal = []
                for i in range(0, fieldLen):
                    fieldVal.append(0)
                self.bitValue[key] = fieldVal
            elif key.lower().startswith('one'):
                fieldVal = []
                for i in range(0, fieldLen):
                    fieldVal.append(1)
                self.bitValue[key] = fieldVal
        self.bitCorrespondence = {}

    def setBitfield(self, name, value):
        # Sets the value of the bits which uniquely identify this instruction
        found = None
        for i in self.bitFields:
            if name == i[0]:
                found = i
                break
        if not found:
            raise Exception('Machine code does not have bitfield ' + name)
        if self.bitValue.has_key(name):
            raise Exception('Value for bitfield ' + name + ' already set in machine code')
        if self.bitCorrespondence.has_key(name):
            raise Exception('Correspondence for field ' + name + ' already set in machine code, unable to set bitfield')
        if len(value) != found[1]:
            raise Exception('Value ' + str(value) + ' for bitfield ' + name + ' in machine code has length ' + str(len(value)) + ' while ' + str(found[1]) + ' was expected')
        for i in value:
            if i and i != 0 and i != 1:
                raise Exception('Value ' + str(value) + ' for bitfield ' + name + ' in machine code is invalid: only binary values (0 or 1) are allowed')
        self.bitValue[name] = value

    def setVarField(self, name, correspondence, bitDir = 'inout'):
        # Set the correspondence between the variable parts of this
        # instruction and the architectural components (registers, reg_banks)
        # part of the instruction for which do not identify the
        # instruction itself and for which a correspondence
        # with the processor elements has not been specified are
        # treated as immediates
        #
        # The correspondence can either be an index (so I have a list:
        # register bank, offset) of a switch, so I have a dictionary
        # (value of the switch, register or register bank). In case
        # it is a direct correspondence with a register I can just
        # set the string for the name of the register
        found = False
        for i in self.bitFields:
            if name == i[0]:
                found = True
                break
        if not found:
            raise Exception('Machine code does not have field ' + name + '; error in trying to set the correspondencce with ' + str(correspondence))
        if self.bitCorrespondence.has_key(name):
            raise Exception('Correspondence for field ' + name + ' already set in machine code')
        if self.bitValue.has_key(name):
            raise Exception('Value for bitfield ' + name + ' already set in machine code, unable to set correspondence')
        self.bitCorrespondence[name] = correspondence
        self.bitDirection[name] = bitDir.lower()

class VLIW:
    """There can be two types of VLIW architectures: the one which
    simply puts more codewords next to each other and the one which
    mixes all the fields together.
    Represents a combination of the machine code just
    identified. When such a vliw is identified, the instructions
    associated with the different machine codes are executed.
    A priority is given to the different machine codes,
    in a same vliw: instructions are executed according to the
    priority, lower first."""
    def __init__(self):
        raise Exception('Description of VLIW architectures not yet supported')
