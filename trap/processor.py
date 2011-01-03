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
#   the Free Software Foundation; either version 3 of the License, or
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
#   (c) Luca Fossati, fossati@elet.polimi.it, fossati.l@gmail.com
#
####################################################################################

import cxx_writer
import procWriter, registerWriter, memWriter, interfaceWriter, portsWriter, pipelineWriter, irqWriter, licenses

validModels = ['funcLT', 'funcAT', 'accLT', 'accAT']

def extractRegInterval(regBankString):
    """Given a string, it check if it specifies an interval
    of registers of a register bank. In case it returns the
    interval, None otherwise. An exception is raised in case
    the string is malformed"""
    if ('[' in regBankString and not ']' in regBankString) or (']' in regBankString and not '[' in regBankString):
        raise Exception(regBankString + ': Malformed string: if there is an open bracket there should be a closing one and viceversa')
    if not '[' in regBankString:
        return None
    if not regBankString.endswith(']'):
        raise Exception(regBankString + ': represents a registry bank so it should end with ]')
    interval = regBankString[regBankString.index('[') + 1:-1].split('-')
    if len(interval) > 2:
        raise Exception(regBankString + ': Contains ' + str(len(interval)) + ' intervals')
    if len(interval) == 1:
        return (int(interval[0]), int(interval[0]))
    if int(interval[0]) > int(interval[1]):
        raise Exception(regBankString + ': The first index should never be bigger than the second')
    return (int(interval[0]), int(interval[1]))


class Register:
    """Register of a processor. It is identified by (a) the
    width in bits, (b) the name. It is eventually possible
    to associate names to the different register fields and
    then refer to them instead of having to use bit masks"""
    def __init__(self, name, bitWidth, bitMask = {}):
        self.name = name
        self.bitWidth = bitWidth
        if bitMask:
            for key, value in bitMask.items():
                if value[0] > value[1]:
                    raise Exception('The bit mask specified for register ' + self.name + ' for field ' + key + ' has the start value ' + str(value[0]) + ' bigger than the end value ' + str(value[1]))
                if value[1] >= bitWidth:
                    raise Exception('The bit mask specified for register ' + self.name + ' for field ' + key + ' is of size ' + str(value[1]) + ' while the register has size ' + str(bitWidth))
                for key1, value1 in bitMask.items():
                    if key1 != key:
                        if (value1[0] <= value[0] and value1[1] >= value[0]) or (value1[0] <= value[1] and value1[1] >= value[1]):
                            raise Exception('The bit mask specified for register ' + self.name + ' for field ' + key + ' intersects with the mask of field ' + key1)
        self.bitMask = bitMask
        self.defValue = 0
        self.offset = 0
        self.constValue = None
        self.delay = 0
        self.wbStageOrder = []

    def setDefaultValue(self, value):
        if self.defValue:
            raise Exception('Default value already set for register ' + self.name)
        try:
            if value > 0:
                import math
                if math.log(value, 2) > self.bitWidth:
                    raise Exception('Register ' + self.name + ' has a width of ' + str(self.bitWidth) + ' bits, but the default value ' + str(value) + ' needs ' + str(int(math.ceil(math.log(value, 2)))) + ' bits for being represented')
        except TypeError:
            pass
        self.defValue = value

    def setConst(self, value):
        if self.delay:
            raise Exception('Register ' + self.name + ' contains a delay assignment, so specifying it as constant does not make sense')
        self.constValue = value

    def setDelay(self, value):
        if self.constValue != None:
            raise Exception('Register ' + self.name + ' is specified as contant, so setting a delay assignment does not make sense')
        self.delay = value

    def setOffset(self, value):
        """TODO: eliminate this restriction"""
        if self.bitMask:
            raise Exception('For register ' + self.name + ' unable to set an offset since a bit mask is used')
        self.offset = value

    def setWbStageOrder(self, order):
        self.wbStageOrder = order

    def getCPPClass(self, model, regType, namespace):
        return registerWriter.getCPPRegClass(self, model, regType, namespace)

class RegisterBank:
    """Same thing of a register, it also specifies the
    number of registers in the bank. In case register
    fields are specified, they have to be the same for the
    whole bank"""
    def __init__(self, name, numRegs, bitWidth, bitMask = {}):
        self.name = name
        self.bitWidth = bitWidth
        totalBits = 0
        if bitMask:
            for key, value in bitMask.items():
                if value[0] > value[1]:
                    raise Exception('The bit mask specified for register bank ' + self.name + ' for field ' + key + ' has the start value ' + str(value[0]) + ' bigger than the end value ' + str(value[0]))
                if value[1] >= bitWidth:
                    raise Exception('The bit mask specified for register bank ' + self.name + ' for field ' + key + ' is of size ' + str(value[1]) + ' while the register has size ' + str(bitWidth))
                for key1, value1 in bitMask.items():
                    if key1 != key:
                        if (value1[0] <= value[0] and value1[1] >= value[0]) or (value1[0] <= value[1] and value1[1] >= value[1]):
                            raise Exception('The bit mask specified for register bank ' + self.name + ' for field ' + key + ' intersects with the mask of field ' + key1)
        self.bitMask = bitMask
        self.numRegs = numRegs
        self.defValues = [0 for i in range(0, numRegs)]
        self.offset = 0
        self.constValue = {}
        self.delay = {}

    def setConst(self, numReg, value):
        if self.delay.has_key(numReg):
            raise Exception('Register ' + str(numReg) + ' in register bank ' + self.name + ' contains a delay assignment, so specifying it as constant does not make sense')
        self.constValue[numReg] = value

    def getConstRegs(self):
        constRegs = []
        for key, constVal in self.constValue.items():
            fakeReg = Register(self.name + '[' + str(key) + ']', self.bitWidth, self.bitMask)
            fakeReg.setOffset(self.offset)
            if self.delay.has_key(key):
                fakeReg.setDelay(self.delay[key])
            fakeReg.setConst(constVal)
            constRegs.append(fakeReg)
        return constRegs

    def setDelay(self, numReg, value):
        if self.constValue.has_key(numReg):
            raise Exception('Register ' + str(numReg) + ' in register bank ' + self.name + ' is declared as constant, so specifying a delay assignment does not make sense')
        if value > 0:
            self.delay[numReg] = value

    def setGlobalDelay(self, value):
        if value > 0:
            for i in range(0, self.numRegs):
                if self.constValue.has_key(i):
                    raise Exception('Register ' + str(i) + ' in register bank ' + self.name + ' is declared as constant, so specifying a delay assignment does not make sense')
                self.delay[i] = value

    def getDelayRegs(self):
        delayRegs = []
        for key, delayVal in self.delay.items():
            fakeReg = Register(self.name + '[' + str(key) + ']', self.bitWidth, self.bitMask)
            fakeReg.setOffset(self.offset)
            fakeReg.setDelay(delayVal)
            if self.constValue.has_key(key):
                fakeReg.setConst(self.constValue[key])
            delayRegs.append(fakeReg)
        return delayRegs

    def setDefaultValues(self, values):
        for i in range(0, len(self.defValues)):
            if self.defValues[i]:
                raise Exception('Default value already set for register ' + str(i) + ' in register bank' + self.name)
            try:
                if values[i] > 0:
                    import math
                    if math.log(values[i], 2) > self.bitWidth:
                        raise Exception('Register ' + str(i) + ' in register bank ' + self.name + ' has a width of ' + str(self.bitWidth) + ' bits, but the default value ' + str(values[i]) + ' needs ' + str(int(math.ceil(math.log(values[i], 2)))) + ' bits for being represented')
            except TypeError:
                pass
        if len(values) != self.numRegs:
            raise Exception('The initialization values for register bank ' + self.name + ' are different, in number, from the number of registers')
        self.defValues = values

    def setDefaultValue(self, value, position):
        if position < 0 or position >= self.numRegs:
            raise Exception('The initialization value for register bank ' + self.name + ' position ' + position + ' is not valid: position out of range')
        if self.defValues[position]:
            raise Exception('Default value already set for register ' + str(position) + ' in register bank' + self.name)
        try:
            if value > 0:
                import math
                if math.log(value, 2) > self.bitWidth:
                    raise Exception('Register ' + str(position) + ' in register bank ' + self.name + ' has a width of ' + str(self.bitWidth) + ' bits, but the default value ' + str(value) + ' needs ' + str(int(math.ceil(math.log(value, 2)))) + ' bits for being represented')
        except TypeError:
            pass
        self.defValues[position] = value

    def getCPPClass(self, model, regType, namespace):
        return registerWriter.getCPPRegBankClass(self, model, regType, namespace)

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
        self.name = name
        # I make sure that there is just one registers specified for
        # the alias
        index = extractRegInterval(initAlias)
        if index:
            if index[0] != index[1]:
                raise Exception('Aliasing a single register, so ' + initAlias + ' cannot specify an interval of more than on register')
        self.initAlias = initAlias
        self.offset = offset
        self.defValue = None
        self.isFixed = False

    def setDefaultValue(self, value):
        self.defValue = value

    def setFixed(self):
        self.isFixed = True

class MemoryAlias:
    """Alias for a register through a memory address: by reading and writing to the
    memory address we actually read/write to the register"""
    def __init__(self, address, alias):
        self.address = address
        self.alias = alias

class AliasRegBank:
    """Alias for a register of the processor;
    actually this is a pointer to a register; this pointer
    might be updated during program execution to point to
    the right register; updating it is responsibility of
    the programmer; it is also possible to directly specify
    a target for the alias: in this case the alias is fixed"""
    def __init__(self, name, numRegs, initAlias):
        self.name = name
        self.numRegs = numRegs
        # Now I have to make sure that the registers specified for the
        # alias have the same lenght of the alias width
        if isinstance(initAlias, type('')):
            index = extractRegInterval(initAlias)
            if index:
                if index[1] - index[0] + 1 != numRegs:
                    raise Exception('Aliasing a register bank of width ' + str(numRegs) + ', while ' + str(initAlias) + ' contains a different number of registers')
            else:
                if numRegs > 1:
                    raise Exception('Aliasing a register bank of width ' + str(numRegs) + ', while ' + str(initAlias) + ' contains only one register')
        else:
            totalRegs = 0
            for i in initAlias:
                index = extractRegInterval(i)
                if index:
                    totalRegs += index[1] - index[0] + 1
                else:
                    totalRegs += 1
            if totalRegs != numRegs:
                raise Exception('Aliasing a register bank of width ' + str(numRegs) + ', while ' + str(initAlias) + ' contains a different number of registers')
        self.initAlias = initAlias
        self.defValues = [None for i in range(0, numRegs)]
        self.offsets = {}
        self.fixedIndices = []
        self.checkGroup = False

    def setCheckGroup(self):
        self.checkGroup = True

    def setFixed(self, indices):
        for index in indices:
            if index >= self.numRegs:
                raise Exception('Alias bank ' + self.name + ' does not have index ' + str(index) + ' in setting fixed indices')
        for i in range(0, len(self.fixedIndices) - 1):
            if self.fixedIndices[i] > self.fixedIndices[i + 1]:
                raise Exception('Alias bank ' + self.name + ' have fixed indices not in acending order')
        self.fixedIndices = indices

    def setOffset(self, regId, offset):
        self.offsets[regId] = offset

    def setDefaultValues(self, values):
        if len(values) != self.numRegs:
            raise Exception('The initialization values for alias bank ' + self.name + ' are different, in number, from the number of registers')
        self.defValues = values

    def setDefaultValue(self, value, position):
        if position < 0 or position >= self.numRegs:
            raise Exception('The initialization value for alias bank ' + self.name + ' position ' + position + ' is not valid: position out of range')
        self.defValues[position] = value

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
    def __init__(self, name, version, systemc = True, coprocessor = False, instructionCache = True, fastFetch = False, externalClock = False, cacheLimit = 256):
        if coprocessor:
            raise Exception('Generation of co-processors not yet enabled')
        if externalClock:
            raise Exception('Use of an external signal as clock not yet supported')

        self.name = name
        self.version = version
        self.isBigEndian = None
        #self.alloc_buffer_size = alloc_buffer_size # Commented since preallocating instruction does not give any speedup
        self.wordSize = None
        self.byteSize = None
        self.bitSizes = None
        self.cacheLimit = cacheLimit
        self.regs = []
        self.regBanks = []
        self.aliasRegs = []
        self.aliasRegBanks = []
        self.abi = None
        self.pipes = []
        self.isa = None
        self.coprocessor = coprocessor
        self.beginOp = None
        self.endOp = None
        self.resetOp = None
        self.irqs = []
        self.pins = []
        self.fetchReg = None
        self.memory = None
        self.tlmPorts = {}
        #self.regOrder = {}
        self.memAlias = []
        self.systemc = systemc
        self.instructionCache = instructionCache
        self.fastFetch = fastFetch
        self.externalClock = externalClock
        self.preProcMacros = []
        self.tlmFakeMemProperties = ()
        self.license_text = licenses.create_gpl_license(self.name)
        self.license = 'gpl'
        self.developer_name = ''
        self.developer_email = ''
        self.banner = ''

    def setIpRights(self, license, developer_name = '', developer_email = '', banner = '', license_text = ''):
        validLicense = ['gpl', 'lgpl', 'esa', 'custom']
        if not license.lower() in validLicense:
            raise Exception('Unknown license ' + license + '; please use one of ' + ' '.join(validLicense))
        if license.lower() == 'custom':
            if not license_text:
                raise Exception('A custom license has been specified, but no text has been given with the license_text parameter')
            else:
                self.license_text = license_text
        else:
            self.license_text = getattr(licenses, 'create_' + license.lower() + '_license')(self.name)
        self.developer_name = developer_name
        self.developer_email = developer_email
        self.banner = banner
        self.license = license.lower()

    def setTLMMem(self, memSize, memLatency, sparse = False):
        """the memory latency is exrepssed in us"""
        self.tlmFakeMemProperties = (memSize, memLatency, sparse)

    def setPreProcMacro(self, wafOption, macro):
        self.preProcMacros.append( (wafOption, macro) )

    def setISA(self, isa):
        self.isa = isa

    def setMemory(self, name, memSize, debug = False, programCounter = ''):
        for name, isFetch  in self.tlmPorts.items():
            if isFetch:
                raise Exception('Cannot add internal memory since instructions will be fetched from port ' + name)
        self.memory = (name, memSize, debug, programCounter)

    def addTLMPort(self, portName, fetch = False):
        """Note that for the TLM port, if only one is specified and the it is the
        port for the fetch, another port called portName + '_fetch' will be automatically
        instantiated. the port called portName can be, instead, used for accessing normal
        data"""
        if not self.systemc:
            raise Exception('The processor must be created with SystemC enabled in order to be able to use TLM ports')
        if fetch and self.memory:
            raise Exception('An internal memory is specified, so the instruction fetch will be performed from that memory and not from port ' + portName)
        for name,isFetch  in self.tlmPorts.items():
            if name == portName:
                raise Exception('A Port with ' + portName + ' already exists')
            if fetch and isFetch:
                raise Exception('Cannot specify port ' + portName + ' as a fetch port since ' + name + ' has already been specified as a fetch port')
        self.tlmPorts[portName] = fetch

    def setBigEndian(self):
        self.isBigEndian = True

    def setLittleEndian(self):
        self.isBigEndian = False

    def setWordsize(self, wordSize, byteSize = 8):
        self.wordSize = wordSize
        self.byteSize = byteSize

    def addRegister(self, reg):
        for i in self.regs:
            if reg.name == i.name:
                raise Exception('A register with name ' + reg.name + ' conflicts with register ' + i.name + ' in processor ' + self.name)
        for i in self.regBanks:
            if reg.name == i.name:
                raise Exception('A register with name ' + reg.name + ' conflicts with register bank ' + i.name + ' in processor ' + self.name)
        for i in self.aliasRegs:
            if reg.name == i.name:
                raise Exception('A register with name ' + reg.name + ' conflicts with alias ' + i.name + ' in processor ' + self.name)
        for i in self.aliasRegBanks:
            if reg.name == i.name:
                raise Exception('A register with name ' + reg.name + ' conflicts with alias bank ' + i.name + ' in processor ' + self.name)
        self.regs.append(reg)

    def addRegBank(self, regBank):
        for i in self.regs:
            if regBank.name == i.name:
                raise Exception('A register bank with name ' + regBank.name + ' conflicts with register ' + i.name + ' in processor ' + self.name)
        for i in self.regBanks:
            if regBank.name == i.name:
                raise Exception('A register bank with name ' + regBank.name + ' conflicts with register bank ' + i.name + ' in processor ' + self.name)
        for i in self.aliasRegs:
            if regBank.name == i.name:
                raise Exception('An register bank with name ' + regBank.name + ' conflicts with alias ' + i.name + ' in processor ' + self.name)
        for i in self.aliasRegBanks:
            if regBank.name == i.name:
                raise Exception('An register bank with name ' + regBank.name + ' conflicts with alias bank ' + i.name + ' in processor ' + self.name)
        self.regBanks.append(regBank)

    def addAliasReg(self, alias):
        for i in self.regs:
            if alias.name == i.name:
                raise Exception('An alias with name ' + alias.name + ' conflicts with register ' + i.name + ' in processor ' + self.name)
        for i in self.regBanks:
            if alias.name == i.name:
                raise Exception('An alias with name ' + alias.name + ' conflicts with register bank ' + i.name + ' in processor ' + self.name)
        for i in self.aliasRegs:
            if alias.name == i.name:
                raise Exception('An alias with name ' + alias.name + ' conflicts with alias ' + i.name + ' in processor ' + self.name)
        for i in self.aliasRegBanks:
            if alias.name == i.name:
                raise Exception('An alias with name ' + alias.name + ' conflicts with alias bank ' + i.name + ' in processor ' + self.name)
        self.aliasRegs.append(alias)

    def addAliasRegBank(self, alias):
        for i in self.regs:
            if alias.name == i.name:
                raise Exception('An alias bank with name ' + alias.name + ' conflicts with register ' + i.name + ' in processor ' + self.name)
        for i in self.regBanks:
            if alias.name == i.name:
                raise Exception('An alias bank with name ' + alias.name + ' conflicts with register bank ' + i.name + ' in processor ' + self.name)
        for i in self.aliasRegs:
            if i.name in alias.name or alias.name in i.name:
                raise Exception('An alias bank with name ' + alias.name + ' conflicts with alias ' + i.name + ' in processor ' + self.name)
        for i in self.aliasRegBanks:
            if alias.name == i.name:
                raise Exception('An alias bank with name ' + alias.name + ' conflicts with alias bank ' + i.name + ' in processor ' + self.name)
        self.aliasRegBanks.append(alias)

    def setABI(self, abi):
        if self.coprocessor:
            print ('WARNING: processor ' + self.name + ' is a coprocessor, so there is not need to set the ABI')
        self.abi = abi

    def addPipeStage(self, pipe):
        for i in self.pipes:
            if i.name == pipe.name:
                raise Exception('A pipeline stage with name ' + pipe.name + ' already exists in processor ' + self.name)
        self.pipes.append(pipe)

    def setBeginOperation(self, code):
        """if is an instance of cxx_writer.CustomCode,
        containing the code for the behavior
        If no begin operation is specified, the default
        values for the registers are used"""
        self.beginOp = code

    def setEndOperation(self, code):
        """if is an instance of cxx_writer.CustomCode,
        containing the code for the behavior
        If no end operation is specified, nothing
        is done"""
        self.endOp = code

    def setResetOperation(self, code):
        """if is an instance of cxx_writer.CustomCode,
        containing the code for the behavior
        if no reset operation is specified, the
        begin operation is called"""
        self.resetOp = code

    def addIrq(self, irq):
        for i in self.irqs:
            if i.name == irq.name:
                raise Exception('An Interrupt port with name ' + i.name + ' already exists in processor ' + self.name)
        self.irqs.append(irq)

    def addPin(self, pin):
        for i in self.pins:
            if i.name == pin.name:
                raise Exception('An external pin with name ' + i.name + ' already exists in processor ' + self.name)
        self.pins.append(pin)

    def setFetchRegister(self, fetchReg,  offset = 0):
        """Sets the correspondence between the fetch address
        and a register inside the processor"""
        found = False
        for i in self.aliasRegs + self.regs:
            if i.name == fetchReg:
                found = True
                break
        if not found:
            index = extractRegInterval(fetchReg)
            if not index:
                raise Exception('Register ' + fetchReg + ' is not part of the processor architecture')
            if index[0] != index[1]:
                raise Exception('The fecth register must be a single register while ' + fetchReg + ' was specified')
            name = fetchReg[:regBankString.index('[')]
            for i in self.aliasRegBanks + self.regBanks:
                if i.name == name:
                    if index[0] < i.numRegs:
                        found = True
                        break
                    else:
                        raise Exception('Register ' + fetchReg + ' is not containe in register bank ' + name + ' which has only ' + str(i.numRegs) + ' registers')
        if not found:
            raise Exception('Register ' + fetchReg + ' is not part of the processor architecture')
        self.fetchReg = (fetchReg,  offset)

    def addMemAlias(self, memAlias):
        self.memAlias.append(memAlias)

    def isRegExisting(self, name, index = None):
        if index:
            # I have to check for a register bank
            for i in self.regBanks:
                if name == i.name:
                    if index[0] >= 0 and index[1] <= i.numRegs:
                        return i
                    else:
                        raise Exception('Register Bank ' + i.name + ' has width ' + str(i.numRegs) + ' but we are trying to access register ' + str(index[1]))
            for i in self.aliasRegBanks:
                if name == i.name:
                    if index[0] >= 0 and index[1] <= i.numRegs:
                        return i
                    else:
                        raise Exception('Alias Register Bank ' + i.name + ' has width ' + str(i.numRegs) + ' but we are trying to access register ' + str(index[1]))
        else:
            for i in self.regs:
                if name == i.name:
                    return i
            for i in self.aliasRegs:
                if name == i.name:
                    return i
        return None

    def isBank(self, bankName):
        for i in self.regBanks + self.aliasRegBanks:
            if bankName == i.name:
                return True
        return False

    #def setWBOrder(self, regName, order):
        #for i in order:
            #if not i in [curPipe.name for curPipe in self.pipes]:
                #raise Exception('Pipeline stage ' + i + ' specified for write back of register ' + regName + ' not present in the pipeline')
        #order = list(order)
        #for curPipe in self.pipes:
            #if not curPipe.name in order:
                #order.append(curPipe.name)
        #self.regOrder[regName] = order

    def checkPipeStages(self):
        for instrName, instr in self.isa.instructions.items():
            for stage, beh in instr.prebehaviors.items():
                if not stage in [i.name for i in self.pipes]:
                    raise Exception('Pipeline stage ' + stage + ' declared for behavior ' + beh.name + ' in instruction ' + instrName + ' does not exist')
            for stage, beh in instr.postbehaviors.items():
                if not stage in [i.name for i in self.pipes]:
                    raise Exception('Pipeline stage ' + stage + ' declared for behavior ' + beh.name + ' in instruction ' + instrName + ' does not exist')
            for stage in instr.code.keys():
                if not stage in [i.name for i in self.pipes]:
                    raise Exception('Pipeline stage ' + stage + ' declared for code in instruction ' + instrName + ' does not exist')
        wbStage = False
        checkHazardStage = False
        for pipeStage in self.pipes:
            if pipeStage.wb:
                wbStage = True
            if pipeStage.checkHazard:
                checkHazardStage = True
        if (wbStage and not checkHazardStage) or (not wbStage and checkHazardStage):
            raise Exception('Error, both the writeback and the check hazards stages must be specified')
        for method in self.isa.methods:
            if not method.stage in [i.name for i in self.pipes]:
                raise Exception('Pipeline stage ' + stage + ' declared for method ' + method.name + ' does not exist')

    def checkMemRegisters(self):
        if not self.memory and not self.tlmPorts:
            raise Exception("Memories are not specified; please specify either an internal memory (with the setMemory method) or a TLM memory port (with the addTLMPort method)")
        if not self.fetchReg:
            raise Exception('Please specify the register containing the address of the instructions to be fetched (usually the PC) using the setFetchRegister method')
        for memAliasReg in self.memAlias:
            index = extractRegInterval(memAliasReg.alias)
            if index:
                # I'm aliasing part of a register bank or another alias:
                # I check that it exists and that I am still within
                # boundaries
                regName = memAliasReg.alias[:memAliasReg.alias.find('[')]
                if self.isRegExisting(regName, index) is None:
                    raise Exception('Register ' + memAliasReg.alias + ' indicated in memory alias for address ' + memAliasReg.address)
            else:
                # Single register or alias: I check that it exists
                if self.isRegExisting(memAliasReg.alias) is None:
                    raise Exception('Register ' + memAliasReg.alias + ' indicated in memory alias for address ' + memAliasReg.address)
        if self.memory and self.memory[3]:
            index = extractRegInterval(self.memory[3])
            if index:
                # I'm aliasing part of a register bank or another alias:
                # I check that it exists and that I am still within
                # boundaries
                regName = self.memory[3][:self.memory[3].find('[')]
                if self.isRegExisting(regName, index) is None:
                    raise Exception('Register ' + self.memory[3] + ' indicated for program counter of local memory does not exists')
            else:
                # Single register or alias: I check that it exists
                if self.isRegExisting(self.memory[3]) is None:
                    raise Exception('Register ' + self.memory[3] + ' indicated for program counter of local memory does not exists')

    def checkTestRegs(self):
        """We check that the registers specifies in the tests are existing"""
        outPinPorts = []
        for pinPort in self.pins:
            if not pinPort.inbound:
                outPinPorts.append(pinPort.name)

        for instr in self.isa.instructions.values():
            for test in instr.tests:
                # Now I check the existence of the instruction fields
                for name, elemValue in test[0].items():
                    if not instr.machineCode.bitLen.has_key(name):
                        raise Exception('Field ' + name + ' in test of instruction ' + instr.name + ' is not present in the machine code of the instruction')
                for resource, value in test[1].items():
                    # Now I check the existence of the global resources
                    brackIndex = resource.find('[')
                    memories = self.tlmPorts.keys()
                    if self.memory:
                        memories.append(self.memory[0])
                    if not (brackIndex > 0 and resource[:brackIndex] in memories):
                        index = extractRegInterval(resource)
                        if index:
                            resourceName = resource[:brackIndex]
                            if self.isRegExisting(resourceName, index) is None:
                                raise Exception('Resource ' + resource + ' not found in test for instruction ' + instr.name)
                        else:
                            if self.isRegExisting(resource) is None:
                                raise Exception('Resource ' + resource + ' not found in test for instruction ' + instr.name)
                for resource, value in test[2].items():
                    brackIndex = resource.find('[')
                    memories = self.tlmPorts.keys()
                    if self.memory:
                        memories.append(self.memory[0])
                    if not (brackIndex > 0 and (resource[:brackIndex] in memories or resource[:brackIndex] in outPinPorts)):
                        index = extractRegInterval(resource)
                        if index:
                            resourceName = resource[:brackIndex]
                            if self.isRegExisting(resourceName, index) is None:
                                raise Exception('Resource ' + resource + ' not found in test for instruction ' + instr.name)
                        else:
                            if self.isRegExisting(resource) is None:
                                raise Exception('Resource ' + resource + ' not found in test for instruction ' + instr.name)
    def checkAliases(self):
        """checks that the declared aliases actually refer to
        existing registers"""
        for alias in self.aliasRegBanks:
            # I have to check that the registers alised by
            # this register bank actually exists and that
            # intervals, if used, are correct
            if isinstance(alias.initAlias, type('')):
                index = extractRegInterval(alias.initAlias)
                # I'm aliasing part of a register bank or another alias:
                # I check that it exists and that I am still within
                # boundaries
                refName = alias.initAlias[:alias.initAlias.find('[')]
                regInstance = self.isRegExisting(refName, index)
                if regInstance is None:
                    raise Exception('Register Bank ' + refName + ' referenced by alias ' + alias.name + ' does not exists')
                try:
                    try:
                        for value in alias.defValues:
                            if value != None and value > 0:
                                import math
                                if math.log(value, 2) > regInstance.bitWidth:
                                    raise Exception('Alias Bank ' + alias.name + ' points to a register of width of ' + str(regInstance.bitWidth) + ' bits, but the default value ' + str(value) + ' needs ' + str(int(math.ceil(math.log(value, 2)))) + ' bits for being represented')
                    except TypeError:
                        pass
                except AttributeError:
                    pass
            else:
                totalRegs = 0
                for i in range(0, len(alias.initAlias)):
                    index = extractRegInterval(alias.initAlias[i])
                    if index:
                        # I'm aliasing part of a register bank or another alias:
                        # I check that it exists and that I am still within
                        # boundaries
                        refName = alias.initAlias[i][:alias.initAlias[i].find('[')]
                        regInstance = self.isRegExisting(refName, index)
                        if regInstance is None:
                            raise Exception('Register Bank ' + alias.initAlias[i] + ' referenced by alias ' + alias.name + ' does not exists')
                        try:
                            try:
                                if alias.defValues[i] != None and alias.defValues[i] > 0:
                                    import math
                                    if math.log(alias.defValues[i], 2) > regInstance.bitWidth:
                                        raise Exception('Alias Bank ' + alias.name + ' points to a register of width of ' + str(regInstance.bitWidth) + ' bits, but the default value ' + str(alias.defValues[i]) + ' needs ' + str(int(math.ceil(math.log(alias.defValues[i], 2)))) + ' bits for being represented')
                            except TypeError:
                                pass
                        except AttributeError:
                            pass
                    else:
                        # Single register or alias: I check that it exists
                        regInstance = self.isRegExisting(alias.initAlias[i])
                        if regInstance is None:
                            raise Exception('Register ' + alias.initAlias[i] + ' referenced by alias ' + alias.name + ' does not exists')
                        try:
                            try:
                                if alias.defValues[i] != None and alias.defValues[i] > 0:
                                    import math
                                    if math.log(alias.defValues[i], 2) > regInstance.bitWidth:
                                        raise Exception('Alias Bank ' + alias.name + ' points to a register of width of ' + str(regInstance.bitWidth) + ' bits, but the default value ' + str(alias.defValues[i]) + ' needs ' + str(int(math.ceil(math.log(alias.defValues[i], 2)))) + ' bits for being represented')
                            except TypeError:
                                pass
                        except AttributeError:
                            pass
        for alias in self.aliasRegs:
            index = extractRegInterval(alias.initAlias)
            if index:
                # I'm aliasing part of a register bank or another alias:
                # I check that it exists and that I am still within
                # boundaries
                refName = alias.initAlias[:alias.initAlias.find('[')]
                regInstance = self.isRegExisting(refName, index)
                if regInstance is None:
                    raise Exception('Register Bank ' + alias.initAlias + ' referenced by alias ' + alias.name + ' does not exists')
                try:
                    try:
                        if alias.defValue != None and alias.defValue > 0:
                            import math
                            if math.log(alias.defValue, 2) > regInstance.bitWidth:
                                raise Exception('Alias Bank ' + alias.name + ' points to a register of width of ' + str(regInstance.bitWidth) + ' bits, but the default value ' + str(alias.defValue) + ' needs ' + str(int(math.ceil(math.log(alias.defValue, 2)))) + ' bits for being represented')
                    except TypeError:
                        pass
                except AttributeError:
                    pass
            else:
                # Single register or alias: I check that it exists
                regInstance = self.isRegExisting(refName, index)
                if regInstance is None:
                    raise Exception('Register ' + alias.initAlias + ' referenced by alias ' + alias.name + ' does not exists')
                try:
                    try:
                        if alias.defValue != None and alias.defValue > 0:
                            import math
                            if math.log(alias.defValue, 2) > regInstance.bitWidth:
                                raise Exception('Alias Bank ' + alias.name + ' points to a register of width of ' + str(regInstance.bitWidth) + ' bits, but the default value ' + str(alias.defValue) + ' needs ' + str(int(math.ceil(math.log(alias.defValue, 2)))) + ' bits for being represented')
                    except TypeError:
                        pass
                except AttributeError:
                    pass

    def checkISARegs(self):
        """Checks that registers declared in the instruction encoding and the ISA really exists"""
        architecturalNames = [archElem.name for archElem in self.regs + self.regBanks + self.aliasRegs + self.aliasRegBanks]
        for name, instruction in self.isa.instructions.items():
            # inside each instruction I have to check for registers defined in the machine code (bitCorrespondence),
            # the correspondence declared inside the instruction itself (bitCorrespondence), the input and output
            # special registers (specialInRegs, specialOutRegs)
            for regName in instruction.machineCode.bitCorrespondence.values():
                if not regName[0] in architecturalNames:
                    raise Exception('Architectural Element ' + str(regName[0]) + ' specified in machine code of instruction ' + name + ' does not exist')
            for regName in instruction.bitCorrespondence.values():
                if not regName[0] in architecturalNames:
                    raise Exception('Architectural Element ' + str(regName[0]) + ' specified in machine code of instruction ' + name + ' does not exist')
            outRegs = []
            for regList in instruction.specialOutRegs.values():
                outRegs += regList
            inRegs = []
            for regList in instruction.specialInRegs.values():
                inRegs += regList
            for regName in inRegs + outRegs:
                index = extractRegInterval(regName)
                if index:
                    # I'm aliasing part of a register bank or another alias:
                    # I check that it exists and that I am still within
                    # boundaries
                    refName = regName[:regName.find('[')]
                    if self.isRegExisting(refName, index) is None:
                        raise Exception('Register Bank ' + regName + ' referenced as spcieal register in insrtuction ' + name + ' does not exists')
                else:
                    # Single register or alias: I check that it exists
                    if self.isRegExisting(regName) is None:
                        raise Exception('Register ' + regName + ' referenced as spcieal register in insrtuction ' + name + ' does not exists')
            pipeStageName = [i.name for i in self.pipes] + ['default']
            beforeCheck = []
            wbStageName = 'default'
            hazardStageName = 'default'
            for i in self.pipes:
                if i.checkHazard:
                    hazardStageName = i.name
                elif i.endHazard:
                    wbStageName = i.name
            newOutRegs = {}
            for stage, regs in instruction.specialOutRegs.items():
                if stage == 'default':
                    stage = wbStageName
                if not stage in pipeStageName:
                    raise Exception('Stage ' + stage + ' specified for special register of instruction ' + name + ' does not exists')
                newOutRegs[stage] = regs
            instruction.specialOutRegs = newOutRegs
            newInRegs = {}
            for stage, regs in instruction.specialInRegs.items():
                if stage == 'default':
                    stage = hazardStageName
                if not stage in pipeStageName:
                    raise Exception('Stage ' + stage + ' specified for special register of instruction ' + name + ' does not exists')
                newInRegs[stage] = regs
            instruction.specialInRegs = newInRegs

    def checkABI(self):
        """checks that the registers specified for the ABI interface
        refer to existing registers"""
        index = extractRegInterval(self.abi.retVal)
        if index:
            regBound = self.abi.retVal[self.abi.retVal.find('['):self.abi.retVal.find(']')]
            if '-' in regBound:
                raise Exception('Only a single register can be specified in the ABI for the return value')
        toCheck = [self.abi.retVal, self.abi.PC]
        if self.abi.LR:
            toCheck.append(self.abi.LR)
        if self.abi.FP:
            toCheck.append(self.abi.FP)
        if self.abi.SP:
            toCheck.append(self.abi.SP)
        for reg in self.abi.stateIgnoreRegs:
            toCheck.append(reg)
        if isinstance(self.abi.args, type('')):
            toCheck.append(self.abi.args)
        else:
            for i in self.abi.args:
                toCheck.append(i)
        for i in self.abi.regCorrespondence.keys():
            toCheck.append(i)
        if self.abi.returnCallReg:
            for returnReg in self.abi.returnCallReg:
                toCheck.append(returnReg[0])
                toCheck.append(returnReg[1])
        # ok, now I finally perform the check
        for i in toCheck:
            index = extractRegInterval(i)
            if index:
                # I'm aliasing part of a register bank or another alias:
                # I check that it exists and that I am still within
                # boundaries
                refName = i[:i.find('[')]
                if self.isRegExisting(refName, index) is None:
                    raise Exception('Register Bank ' + i + ' used in the ABI does not exists')
            else:
                # Single register or alias: I check that it exists
                if self.isRegExisting(i) is None:
                    raise Exception('Register ' + i + ' used in the ABI does not exists')
        # warning in case details are not specified
        if not self.abi.returnCallInstr or not self.abi.callInstr:
            print('Warning: "returnCallInstr" or "callInstr" not specified in the ABI: the profiler may give uncorrect results')
        ################# TODO: check also the memories #######################

    def checkIRQPorts(self):
        """So far I only have to check that the stages of the IRQ operations are existing"""
        stageNames = [i.name for i in self.pipes]
        for irq in self.irqs:
            for stage in irq.operation.keys():
                if not stage in stageNames:
                    raise Exception('Pipeline stage ' + stage + ' declared for interrupt ' + irq.name + ' does not exist')

    def getCPPRegisters(self, trace, combinedTrace, model, namespace):
        """This method creates all the classes necessary for declaring
        the registers: in particular the register base class
        and all the classes for the different bitwidths"""
        return registerWriter.getCPPRegisters(self, trace, combinedTrace, model, namespace)

    def getCPPPipelineReg(self, trace, combinedTrace, namespace):
        return registerWriter.getCPPPipelineReg(self, trace, combinedTrace, namespace)

    def getRegistersBitfields(self):
        return registerWriter.getRegistersBitfields(self)

    def getCPPAlias(self, model, namespace):
        """This method creates the class describing a register
        alias"""
        if model.startswith('acc'):
            return registerWriter.getCPPPipelineAlias(self, namespace)
        else:
            return registerWriter.getCPPAlias(self, namespace)

    def getCPPProc(self, model, trace, combinedTrace, namespace):
        """creates the class describing the processor"""
        return procWriter.getCPPProc(self, model, trace, combinedTrace, namespace)

    def getCPPMemoryIf(self, model, namespace):
        """creates the class describing the processor"""
        return memWriter.getCPPMemoryIf(self, model, namespace)

    def getCPPIf(self, model, namespace):
        """creates the interface which is used by the tools
        to access the processor core"""
        return interfaceWriter.getCPPIf(self, model, namespace)

    def getCPPExternalPorts(self, model, namespace):
        """creates the processor external ports used for the
        communication with the external world (the memory port
        is not among this ports, it is treated separately)"""
        return portsWriter.getCPPExternalPorts(self, model, namespace)

    def getTestMainCode(self):
        """Returns the code for the file which contains the main
        routine for the execution of the tests.
        actually it is nothing but a file which includes
        boost/test/auto_unit_test.hpp and defines
        BOOST_AUTO_TEST_MAIN and BOOST_TEST_DYN_LINK"""
        return procWriter.getTestMainCode(self)

    def getMainCode(self, model, namespace):
        """Returns the code which instantiate the processor
        in order to execute simulations"""
        return procWriter.getMainCode(self, model, namespace)

    def getGetIRQPorts(self, namespace):
        """Returns the code implementing the interrupt ports"""
        return portsWriter.getGetIRQPorts(self, namespace)

    def getGetIRQInstr(self, model, trace, combinedTrace, namespace):
        """Returns the code implementing the fake interrupt instruction"""
        return irqWriter.getGetIRQInstr(self, model, trace, namespace)

    def getGetPINPorts(self, namespace):
        """Returns the code implementing the PIN ports"""
        return portsWriter.getGetPINPorts(self, namespace)

    def getIRQTests(self, trace, combinedTrace, namespace):
        """Returns the code implementing the tests for the
        interrupt lines"""
        return portsWriter.getIRQTests(self, trace, combinedTrace, namespace)

    def getGetPipelineStages(self, trace, combinedTrace, model, namespace):
        """Returns the code implementing the pipeline stages"""
        return pipelineWriter.getGetPipelineStages(self, trace, combinedTrace, model, namespace)

    def write(self, folder = '', models = validModels, namespace = '', dumpDecoderName = '', trace = False, combinedTrace = False, forceDecoderCreation = False, tests = True, memPenaltyFactor = 4):
        """Ok: this method does two things: first of all it performs all
        the possible checks to ensure that the processor description is
        coherent. Second it actually calls the write method of the
        processor components (registers, instructions, etc.) to create
        the code of the simulator"""
        print ('\tCREATING IMPLEMENTATION FOR PROCESSOR MODEL --> ' + self.name)
        print ('\t\tChecking the consistency of the specification')
        if ('funcAT' in models or 'accAT' in models or 'accLT' in models) and not self.tlmPorts:
            raise Exception('Only the creation of the funcLT model is suported without defining TLM ports. Please specify at least one')
        self.isa.computeCoding()
        self.isa.checkCoding()
        self.checkAliases()
        self.checkMemRegisters()
        self.checkPipeStages()
        self.checkTestRegs()
        if self.abi:
            self.checkABI()
        self.isa.checkRegisters(extractRegInterval, self.isRegExisting)
        self.checkISARegs()
        self.checkIRQPorts()

        # OK, checks done. Now I can start calling the write methods to
        # actually create the ISS code
        # First of all we have to create the decoder
        from isa import resolveBitType
        import decoder, os
        import cxx_writer
        # Now I declare a couple of variables used for keeping track of the size of each words and parts for them
        self.bitSizes = [resolveBitType('BIT<' + str(self.wordSize*self.byteSize*2) + '>'),
                        resolveBitType('BIT<' + str(self.wordSize*self.byteSize) + '>'),
                        resolveBitType('BIT<' + str(self.wordSize*self.byteSize/2) + '>'),
                        resolveBitType('BIT<' + str(self.byteSize) + '>')]

        cxx_writer.writer_code.FileDumper.license = self.license
        cxx_writer.writer_code.FileDumper.license_text = self.license_text
        cxx_writer.writer_code.FileDumper.developer_name = self.developer_name
        cxx_writer.writer_code.FileDumper.developer_email = self.developer_email
        cxx_writer.writer_code.FileDumper.banner = self.banner

        # Here we check if the decoder signature changed; in case it hasn't we create the decoder,
        # otherwise we load it from file
        instructionSignature = self.isa.getInstructionSig()
        if not forceDecoderCreation:
            if os.path.exists(os.path.join(os.path.expanduser(os.path.expandvars(folder)), '.decoderSig')) and os.path.exists(os.path.join(os.path.expanduser(os.path.expandvars(folder)), '.decoderDump.pickle')):
                # Now I have to compare the saved signature with the signature of the current
                # instructions
                try:
                    decSigFile = open(os.path.join(os.path.expanduser(os.path.expandvars(folder)), '.decoderSig'), 'r')
                    savedSig = decSigFile.read()
                    decSigFile.close()
                    if savedSig != instructionSignature:
                        forceDecoderCreation = True
                except:
                    try:
                        decSigFile.close()
                    except:
                        pass
                    forceDecoderCreation = True
            else:
                forceDecoderCreation = True
        if forceDecoderCreation:
            print ('\t\tCreating the decoder')
            dec = decoder.decoderCreator(self.isa.instructions, self.isa.subInstructions, memPenaltyFactor)
            import copy
            decCopy = copy.deepcopy(dec)
        else:
            try:
                print ('\t\tLoading the decoder from cache')
                import pickle
                decDumpFile = open(os.path.join(os.path.expanduser(os.path.expandvars(folder)), '.decoderDump.pickle'), 'r')
                dec = pickle.load(decDumpFile)
                decDumpFile.close()
            except:
                print ('\t\tError in loading the decoder')
                print ('\t\tRe-Creating the decoder')
                dec = decoder.decoderCreator(self.isa.instructions, self.isa.subInstructions, memPenaltyFactor)
                import copy
                decCopy = copy.deepcopy(dec)
                forceDecoderCreation = True
        if dumpDecoderName:
            dec.printDecoder(dumpDecoderName)
        mainFolder = cxx_writer.writer_code.Folder(os.path.expanduser(os.path.expandvars(folder)))
        for model in models:
            # Here I add the define code, definig the type of the current model;
            # such define code has to be added to each created header file
            defString = '#define ' + model[:-2].upper() + '_MODEL\n'
            defString += '#define ' + model[-2:].upper() + '_IF\n'
            defCode = cxx_writer.writer_code.Define(defString)

            # Now I also set the processor class name: note that even if each model has a
            # separate namespace, some buggy dynamic linkers complain, so we must also
            # use separate names for the processor class
            procWriter.processor_name = 'Processor_' + self.name.lower() + '_' + model.lower()

            print ('\t\tCreating the implementation for model ' + model)
            if not model in validModels:
                raise Exception(model + ' is not a valid model type')
            if not namespace:
                namespace = self.name.lower() + '_' + model.lower() + '_trap'
            namespaceUse = cxx_writer.writer_code.UseNamespace(namespace)
            namespaceTrapUse = cxx_writer.writer_code.UseNamespace('trap')
            decClasses = dec.getCPPClass(self.bitSizes[1], self.instructionCache, namespace)
            implFileDec = cxx_writer.writer_code.FileDumper('decoder.cpp', False)
            headFileDec = cxx_writer.writer_code.FileDumper('decoder.hpp', True)
            headFileDec.addMember(defCode)
            implFileDec.addMember(namespaceUse)
            for i in decClasses:
                implFileDec.addMember(i)
                headFileDec.addMember(i)
            implFileDec.addInclude('decoder.hpp')
            RegClasses = self.getCPPRegisters(trace, combinedTrace, model, namespace)
            AliasClass = self.getCPPAlias(model, namespace)
            ProcClass = self.getCPPProc(model, trace, combinedTrace, namespace)
            if self.abi:
                IfClass = self.getCPPIf(model, namespace)
            if model.startswith('acc'):
                pipeClass = self.getGetPipelineStages(trace, combinedTrace, model, namespace)
            MemClass = self.getCPPMemoryIf(model, namespace)
            ExternalIf = self.getCPPExternalPorts(model, namespace)
            PINClasses = []
            if self.pins:
                PINClasses += self.getGetPINPorts(namespace)
            ISAClasses = self.isa.getCPPClasses(self, model, trace, combinedTrace, namespace)
            IRQClasses = []
            if self.irqs:
                IRQClasses += self.getGetIRQPorts(namespace)
                ISAClasses += self.getGetIRQInstr(model, trace, combinedTrace, namespace)
            # Ok, now that we have all the classes it is time to write
            # them to file
            curFolder = cxx_writer.writer_code.Folder(os.path.join(folder, model))
            mainFolder.addSubFolder(curFolder)
            implFileRegs = cxx_writer.writer_code.FileDumper('registers.cpp', False)
            implFileRegs.addInclude('registers.hpp')
            headFileRegs = cxx_writer.writer_code.FileDumper('registers.hpp', True)
            headFileRegs.addMember(defCode)
            headFileRegs.addMember(self.getRegistersBitfields())
            implFileRegs.addMember(namespaceUse)
            for i in RegClasses:
                implFileRegs.addMember(i)
                headFileRegs.addMember(i)
            implFileAlias = cxx_writer.writer_code.FileDumper('alias.cpp', False)
            implFileAlias.addInclude('alias.hpp')
            headFileAlias = cxx_writer.writer_code.FileDumper('alias.hpp', True)
            headFileAlias.addMember(defCode)
            implFileAlias.addMember(namespaceUse)
            for i in AliasClass:
                implFileAlias.addMember(i)
                headFileAlias.addMember(i)
            implFileProc = cxx_writer.writer_code.FileDumper('processor.cpp', False)
            headFileProc = cxx_writer.writer_code.FileDumper('processor.hpp', True)
            implFileProc.addMember(namespaceUse)
            implFileProc.addMember(namespaceTrapUse)
            implFileProc.addMember(ProcClass)
            headFileProc.addMember(defCode)
            headFileProc.addMember(namespaceTrapUse)
            headFileProc.addMember(ProcClass)
            implFileProc.addInclude('processor.hpp')
            if model.startswith('acc'):
                implFilePipe = cxx_writer.writer_code.FileDumper('pipeline.cpp', False)
                headFilePipe = cxx_writer.writer_code.FileDumper('pipeline.hpp', True)
                headFilePipe.addMember(defCode)
                implFilePipe.addMember(namespaceUse)
                implFilePipe.addMember(namespaceTrapUse)
                headFilePipe.addMember(namespaceTrapUse)
                for i in pipeClass:
                    implFilePipe.addMember(i)
                    headFilePipe.addMember(i)
                implFilePipe.addInclude('pipeline.hpp')
            implFileInstr = cxx_writer.writer_code.FileDumper('instructions.cpp', False)
            headFileInstr = cxx_writer.writer_code.FileDumper('instructions.hpp', True)
            headFileInstr.addMember(defCode)
            implFileInstr.addMember(namespaceUse)
            for i in ISAClasses:
                implFileInstr.addMember(i)
                headFileInstr.addMember(i)
            if self.abi:
                implFileIf = cxx_writer.writer_code.FileDumper('interface.cpp', False)
                implFileIf.addInclude('interface.hpp')
                headFileIf = cxx_writer.writer_code.FileDumper('interface.hpp', True)
                headFileIf.addMember(defCode)
                implFileIf.addMember(namespaceUse)
                implFileIf.addMember(namespaceTrapUse)
                headFileIf.addMember(namespaceTrapUse)
                implFileIf.addMember(IfClass)
                headFileIf.addMember(IfClass)
            implFileMem = cxx_writer.writer_code.FileDumper('memory.cpp', False)
            implFileMem.addInclude('memory.hpp')
            headFileMem = cxx_writer.writer_code.FileDumper('memory.hpp', True)
            headFileMem.addMember(defCode)
            implFileMem.addMember(namespaceUse)
            implFileMem.addMember(namespaceTrapUse)
            headFileMem.addMember(namespaceTrapUse)
            for i in MemClass:
                implFileMem.addMember(i)
                headFileMem.addMember(i)
            if ExternalIf:
                implFileExt = cxx_writer.writer_code.FileDumper('externalPorts.cpp', False)
                implFileExt.addInclude('externalPorts.hpp')
                headFileExt = cxx_writer.writer_code.FileDumper('externalPorts.hpp', True)
                headFileExt.addMember(defCode)
                implFileExt.addMember(namespaceUse)
                implFileExt.addMember(ExternalIf)
                headFileExt.addMember(ExternalIf)
            if self.irqs:
                implFileIRQ = cxx_writer.writer_code.FileDumper('irqPorts.cpp', False)
                implFileIRQ.addInclude('irqPorts.hpp')
                headFileIRQ = cxx_writer.writer_code.FileDumper('irqPorts.hpp', True)
                headFileIRQ.addMember(defCode)
                implFileIRQ.addMember(namespaceUse)
                for i in IRQClasses:
                    implFileIRQ.addMember(i)
                    headFileIRQ.addMember(i)
            if self.pins:
                implFilePIN = cxx_writer.writer_code.FileDumper('externalPins.cpp', False)
                implFilePIN.addInclude('externalPins.hpp')
                headFilePIN = cxx_writer.writer_code.FileDumper('externalPins.hpp', True)
                headFilePIN.addMember(defCode)
                implFilePIN.addMember(namespaceUse)
                for i in PINClasses:
                    implFilePIN.addMember(i)
                    headFilePIN.addMember(i)
            mainFile = cxx_writer.writer_code.FileDumper('main.cpp', False)
            mainFile.addMember(self.getMainCode(model, namespace))

            if (model == 'funcLT') and (not self.systemc) and tests:
                testFolder = cxx_writer.writer_code.Folder('tests')
                curFolder.addSubFolder(testFolder)
                mainTestFile = cxx_writer.writer_code.FileDumper('main.cpp', False)
                decTestsFile = cxx_writer.writer_code.FileDumper('decoderTests.cpp', False)
                decTestsFile.addInclude('decoderTests.hpp')
                mainTestFile.addInclude('decoderTests.hpp')
                hdecTestsFile = cxx_writer.writer_code.FileDumper('decoderTests.hpp', True)
                decTests = dec.getCPPTests(namespace)
                decTestsFile.addMember(decTests)
                hdecTestsFile.addMember(decTests)
                irqTests = self.getIRQTests(trace, combinedTrace, namespace)
                if irqTests:
                    irqTestsFile = cxx_writer.writer_code.FileDumper('irqTests.cpp', False)
                    irqTestsFile.addInclude('irqTests.hpp')
                    if PINClasses:
                        irqTestsFile.addInclude('PINTarget.hpp')
                        irqTestsFile.addInclude('externalPins.hpp')
                    mainTestFile.addInclude('irqTests.hpp')
                    hirqTestsFile = cxx_writer.writer_code.FileDumper('irqTests.hpp', True)
                    irqTestsFile.addMember(namespaceUse)
                    irqTestsFile.addMember(namespaceTrapUse)
                    irqTestsFile.addMember(irqTests)
                    hirqTestsFile.addMember(irqTests)
                    testFolder.addCode(irqTestsFile)
                    testFolder.addHeader(hirqTestsFile)
                testFolder.addCode(decTestsFile)
                testFolder.addHeader(hdecTestsFile)
                ISATests = self.isa.getCPPTests(self, model, trace, combinedTrace, namespace)
                testPerFile = 100
                numTestFiles = len(ISATests)/testPerFile
                for i in range(0, numTestFiles):
                    ISATestsFile = cxx_writer.writer_code.FileDumper('isaTests' + str(i) + '.cpp', False)
                    ISATestsFile.addInclude('isaTests' + str(i) + '.hpp')
                    if PINClasses:
                        ISATestsFile.addInclude('PINTarget.hpp')
                        ISATestsFile.addInclude('externalPins.hpp')
                    mainTestFile.addInclude('isaTests' + str(i) + '.hpp')
                    hISATestsFile = cxx_writer.writer_code.FileDumper('isaTests' + str(i) + '.hpp', True)
                    ISATestsFile.addMember(namespaceUse)
                    ISATestsFile.addMember(namespaceTrapUse)
                    ISATestsFile.addMember(ISATests[testPerFile*i:testPerFile*(i+1)])
                    hISATestsFile.addMember(ISATests[testPerFile*i:testPerFile*(i+1)])
                    testFolder.addCode(ISATestsFile)
                    testFolder.addHeader(hISATestsFile)
                if testPerFile*numTestFiles < len(ISATests):
                    ISATestsFile = cxx_writer.writer_code.FileDumper('isaTests' + str(numTestFiles) + '.cpp', False)
                    ISATestsFile.addInclude('isaTests' + str(numTestFiles) + '.hpp')
                    if PINClasses:
                        ISATestsFile.addInclude('PINTarget.hpp')
                        ISATestsFile.addInclude('externalPins.hpp')
                    mainTestFile.addInclude('isaTests' + str(numTestFiles) + '.hpp')
                    hISATestsFile = cxx_writer.writer_code.FileDumper('isaTests' + str(numTestFiles) + '.hpp', True)
                    ISATestsFile.addMember(namespaceUse)
                    ISATestsFile.addMember(namespaceTrapUse)
                    ISATestsFile.addMember(ISATests[testPerFile*numTestFiles:])
                    hISATestsFile.addMember(ISATests[testPerFile*numTestFiles:])
                    testFolder.addCode(ISATestsFile)
                    testFolder.addHeader(hISATestsFile)

                mainTestFile.addMember(self.getTestMainCode())
                testFolder.addCode(mainTestFile)
                testFolder.addUseLib(os.path.split(curFolder.path)[-1] + '_objs')
            curFolder.addHeader(headFileInstr)
            curFolder.addCode(implFileInstr)
            curFolder.addHeader(headFileRegs)
            curFolder.addCode(implFileRegs)
            curFolder.addHeader(headFileAlias)
            curFolder.addCode(implFileAlias)
            curFolder.addHeader(headFileProc)
            curFolder.addCode(implFileProc)
            if model.startswith('acc'):
                curFolder.addHeader(headFilePipe)
                curFolder.addCode(implFilePipe)
            if self.abi:
                curFolder.addHeader(headFileIf)
                curFolder.addCode(implFileIf)
            curFolder.addHeader(headFileDec)
            curFolder.addCode(implFileDec)
            curFolder.addHeader(headFileMem)
            curFolder.addCode(implFileMem)
            if ExternalIf:
                curFolder.addHeader(headFileExt)
                curFolder.addCode(implFileExt)
            if IRQClasses:
                curFolder.addHeader(headFileIRQ)
                curFolder.addCode(implFileIRQ)
            if PINClasses:
                curFolder.addHeader(headFilePIN)
                curFolder.addCode(implFilePIN)
            curFolder.addCode(mainFile)
            curFolder.setMain(mainFile.name)
            curFolder.create()
            if (model == 'funcLT') and (not self.systemc) and tests:
                testFolder.create(configure = False, tests = True)
            print ('\t\tCreated in folder ' + os.path.expanduser(os.path.expandvars(folder)))
            namespace = ''
        # We create and print the main folder and also add a configuration
        # part to the wscript
        mainFolder.create(configure = True, projectName = self.name, version = self.version, customOptions = self.preProcMacros)
        if forceDecoderCreation:
            try:
                import pickle
                decDumpFile = open(os.path.join(os.path.expanduser(os.path.expandvars(folder)), '.decoderDump.pickle'), 'w')
                pickle.dump(decCopy, decDumpFile, pickle.HIGHEST_PROTOCOL)
                decDumpFile.close()
                # Now I have to save the instruction signature
                decSigFile = open(os.path.join(os.path.expanduser(os.path.expandvars(folder)), '.decoderSig'), 'w')
                decSigFile.write(instructionSignature)
                decSigFile.close()
            except:
                pass

class PipeStage:
    """Identified by (a) name (b) optional, if it is wb,
    the stage where the hazards are checked or where the
    bypassing is started. Note that this is just the default
    information which can be overridden by each instruction"""
    def __init__(self, name):
        self.wb = False
        self.checkHazard = False
        self.name = name
        self.checkUnknown = False
        self.endHazard = False

    def setWriteBack(self):
        self.wb = True

    def setHazard(self):
        self.checkHazard = True

    def setEndHazard(self):
        self.endHazard = True

    def setCheckUnknownInstr(self):
        self.checkUnknown = True

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
        """Specifies the name of the coprocessor variable in the
        processor. It also specifies its type"""
        self.name = name
        self.type = type
        self.isa = {}

    def addIsaCustom(self, name, code, idBits):
        """Specifies that ISA instruction with name name
        is a co-processor instruction and that
        custom code is provided if the instruction is for
        this coprocessor. idBits specifies what it the
        value of the bits which specify if the instruction
        is for this co-processor or not"""
        if self.isa.has_key(name):
            raise Exception('Instruction ' + name + ' has already been specified for coprocessor ' + self.name)
        self.isa[name] = (idBits, code)

    def addIsaCall(self, name, functionName, idBits):
        """Specifies that ISA instruction with name name
        is a co-processor instruction and that
        a function call is provided if the instruction is for
        this coprocessor. idBits specifies what it the
        value of the bits which specify if the instruction
        is for this co-processor or not"""
        if self.isa.has_key(name):
            raise Exception('Instruction ' + name + ' has already been specified for coprocessor ' + self.name)
        self.isa[name] = (idBits, functionName)

class Interrupt:
    """Specifies an interrupt port for the processor.
    Note that I will render both systemc and TLM ports as systemc
    signals: there is a check interrupts routine which will be
    called every cycle, in which the user can check the IRQs and
    take the appropriate actions. The signal will be automatically
    raised, lowered etc... depending whether edge triggered, level etc.."""
    def __init__(self, name, portWidth, tlm = True, priority = 0):
        self.name = name
        self.tlm = tlm
        self.portWidth = portWidth
        self.priority = priority
        self.condition = ''
        self.tests = []
        self.operation = {}
        self.variables = []

    def addVariable(self, variable):
        """adds a variable global to the instruction; note that
        variable has to be an instance of cxx_writer.Variable"""
        if isinstance(variable, type(())):
            from isa import resolveBitType
            variable = cxx_writer.writer_code.Variable(variable[0], resolveBitType(variable[1]))
        for instrVar in self.variables:
            if variable.name == instrVar.name:
                if variable.varType.name != instrVar.varType.name:
                    raise Exception('Trying to add variable ' + variable.name + ' of type ' + variable.varType.name + ' to instruction ' + self.name + ' which already has a variable with such a name of type ' + instrVar.varType.name)
                else:
                    return
        self.variables.append(variable)

    def setOperation(self, operation, stage):
        self.operation[stage] = operation

    def setCondition(self, condition):
        self.condition = condition

    def addTest(self, inputState, expOut):
        """The test is composed of 2 parts: the status before the
        execution of the interrupt and the status after; note that
        in the status before execution of the interrupt we also have
        to specify the value of the interrupt line"""
        self.tests.append((inputState, expOut))

class Pins:
    """Custom pins; checking them or writing to them is responsibility ofnon
    the programmer. They are identified by (a) name (b) type. They are
    rendered with systemc or TLM ports. The type of the port should also
    be specified, as is the direction. For outgoing TLM ports, the requested
    type and the content of the payload are insignificant and only the
    address is important"""
    def __init__(self, name, portWidth, inbound = False, systemc = False):
        """Note how the type of the must be of class cxx_writer.Type; a
        systemc port using this type as a template will be created"""
        self.name = name
        self.portWidth = portWidth
        self.systemc = systemc
        self.inbound = inbound
        self.operation = None

    def setOperation(self, operation):
        if not self.inbound:
            raise Exception('Error, port ' + self.name + ' is out-going, so not operation can be specified')
        self.operation = operation

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
        """Regsiter for the return value (either a register or a tuple
        regback, index)"""
        self.retVal = retVal
        # Register cprrespondence (offsets should also be specified)
        self.LR = LR
        self.PC = PC
        self.SP = SP
        self.FP = FP
        # A list of the registers for the I argument, II arg etc.
        self.args = []
        if isinstance(args, type('')):
            index = extractRegInterval(args)
            if index:
                # I'm aliasing part of a register bank or another alias:
                refName = args[:args.find('[')]
                for i in range(index[0], index[1] + 1):
                    self.args.append(refName + '[' + str(i) + ']')
            else:
                # Single register or alias
                self.args.append(args)
        else:
            for j in args:
                index = extractRegInterval(j)
                if index:
                    # I'm aliasing part of a register bank or another alias:
                    refName = j[:j.find('[')]
                    for i in range(index[0], index[1] + 1):
                        self.args.append(refName + '[' + str(i) + ']')
                else:
                    # Single register or alias
                    self.args.append(j)
        # Correspondence between regs as seen by GDB and the architectural
        # variables
        self.regCorrespondence = {}
        # offsets which must be taken into consideration when dealing with the
        # functional model
        self.offset = {}
        # set the names: to the PC register the name PC, etc.
        self.name = {self.PC: 'PC'}
        if self.LR:
            self.name[self.LR] = 'LR'
        if self.SP:
            self.name[self.SP] = 'SP'
        if self.FP:
            self.name[self.FP] = 'FP'
        if self.retVal:
            self.name[self.retVal] = 'RetVal'
        # Specifies the memories which can be accessed; if more than one memory is specified,
        # we have to associate the address range to each of them
        self.memories = {}
        # C++ Code which has to be executed during emulation of system calls in order to
        # correctly enter a and return from a system call
        self.preCallCode = None
        self.postCallCode = None
        # Registers which have to be updated in order to correctly return from a function call
        self.returnCallReg = None
        # Sequences of instructions which identify a call to a routine and the return from the call
        # to a routine; such sequences are in the form [a, b, (c, d)] which means that, for example,
        # we enter in a new routine when instructions a, b, and c or d are executed in sequence
        self.callInstr = []
        self.returnCallInstr = []
        # Code used to determine the processor ID in a multi-processor environment
        self.procIdCode = None
        # Registers which do not need to be included when saving and restoring the
        # state
        self.stateIgnoreRegs = []

    def addIgnoreStateReg(self, toIgnore):
        self.stateIgnoreRegs.append(toIgnore)

    def processorID(self, procIdCode):
        self.procIdCode = procIdCode

    def setCallInstr(self, instrList):
        self.callInstr = instrList

    def setReturnCallInstr(self, instrList):
        self.returnCallInstr = instrList

    def returnCall(self, regList):
        self.returnCallReg = regList

    def setECallPreCode(self, code):
        self.preCallCode = code

    def setECallPostCode(self, code):
        self.postCallCode = code

    def addVarRegsCorrespondence(self, correspondence):
        for key, value in correspondence.items():
            try:
                value[0]
                value[1]
            except:
                value = (value, value)
            index = extractRegInterval(key)
            if index:
                if index[1] - index[0] != value[1] - value[0]:
                    raise Exception('specifying correspondence for ' + str(value) + ', while ' + str(key) + ' contains a different number of registers')
            else:
                if value[1] - value[0]:
                    raise Exception('specifying correspondence for ' + str(value) + ', while ' + str(key) + ' contains a different number of registers')
            for i in range(value[0], value[1] + 1):
                if i in self.regCorrespondence.values():
                    raise Exception('Correspondence for register ' + str(i) + ' already specified')
                if index:
                    self.regCorrespondence[key[:key.find('[')] + '[' + str(index[0] + i - value[0]) + ']'] = i
                else:
                    self.regCorrespondence[key] = value[0]

    def setOffset(self, register, offset):
        if not register in [self.LR, self.PC, self.SP, self.FP, self.retVal, self.args] + self.regCorrespondence.keys():
            # Ok, the offset register specified does not encode a single register
            # I try to see if it is part of a register bank
            index = extractRegInterval(register)
            if not index:
                raise Exception('Register ' + register + ' of which we are specifying the offset is not part of the ABI')
            rangeToCheck = self.corrReg
            argsIndex = extractRegInterval(self.args)
            if argsIndex:
                for i in range(argsIndex[0], argsIndex[1] + 1):
                    rangeToCheck.append(i)
            for i in range(index[0], index[1] + 1):
                if not i in rangeToCheck:
                    raise Exception('Register ' + register + ' of which we are specifying the offset is not part of the ABI')
        self.offset[register] = offset

    def addMemory(self, memory, addr = ()):
        if self.memories and not addr:
            raise Exception('More than one memory specified in the ABI: an address range must be specified for memory ' + memory)
        for name, savedAddr in self.memories.items():
            if not savedAddr:
                raise Exception('More than one memory specified in the ABI: an address range must be specified for memory ' + name)
            else:
                if (savedAddr[0] <= addr[0] and savedAddr[1] >= addr[0]) or (savedAddr[0] <= addr[1] and savedAddr[1] >= addr[1]):
                    raise Exception('Clash between address ranges of memory ' + name + ' and ' + memory)
        self.memories[memory] = addr
