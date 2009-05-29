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



# Lets first of all import the necessary files for the
# creation of the processor; note that if the trap modules are
# not in the default search path I have to manually specify the path
try:
    import trap
except ImportError:
    import sys, os
    sys.path.append(os.path.abspath(os.path.join('..', '..')))
    try:
        import trap
    except ImportError:
        print ('Please specify in file LEON3Arch.py the path where the core TRAP files are located')

import cxx_writer

# It is nice to keep the ISA and the architecture separated
# so we use the import trick
import LEON3Isa
import LEON3Tests

# Lets now start building the processor
processor = trap.Processor('LEON3', version = '0.0.1', systemc = True, instructionCache = True, fastFetch = False)
processor.setBigEndian() # big endian
processor.setWordsize(4, 8) # 4 bytes per word, 8 bits per byte
processor.setISA(LEON3Isa.isa) # lets set the instruction set

# Ok, now we move to the description of more complicated processor
# resources
# Number of register windows, between 2 and 32, default is 8 for LEON3
numRegWindows = 8

# Code used to move to a new register window
updateWinCode = """for(int i = 8; i < 32; i++){
    REGS[i].updateAlias(WINREGS[(newCwp*16 + i - 8) % (""" + str(16*numRegWindows) + """)]);
}
"""
#updateWinCode = ''
#for i in range(8, 32):
    #updateWinCode += 'REGS[' + str(i) + '].updateAlias(WINREGS[(newCwp*16 + ' + str(i - 8) + ') % (16*' + str(numRegWindows) + ')]);\n'

# Here I add a constant to the instruction set so that it can be used from the code implementing
# the various instructions
LEON3Isa.isa.addConstant(cxx_writer.writer_code.uintType, 'NUM_REG_WIN', numRegWindows)

# There are 8 global register, and a variable number of
# of 16-registers set; this number depends on the number of
# register windows
# global registers
globalRegs = trap.RegisterBank('GLOBAL', 8, 32)
globalRegs.setConst(0, 0)
processor.addRegBank(globalRegs)
# Register sets
windowRegs = trap.RegisterBank('WINREGS', 16*numRegWindows, 32)
processor.addRegBank(windowRegs)
# Program status register
psrBitMask = {'IMPL': (28, 31), 'VER': (24, 27), 'ICC_n': (23, 23), 'ICC_z': (22, 22), 'ICC_v': (21, 21), 'ICC_c': (20, 20), 'EC': (13, 13), 'EF': (12, 12), 'PIL': (8, 11), 'S': (7, 7), 'PS': (6, 6), 'ET': (5, 5), 'CWP': (0, 4)}
psrReg = trap.Register('PSR', 32, psrBitMask)
psrReg.setDefaultValue(0xF3000080)
psrReg.setDelay(3)
processor.addRegister(psrReg)
# Window Invalid Mask Register
wimBitMask = {}
for i in range(0, 32):
    wimBitMask['WIM_' + str(i)] = (i, i)
wimReg = trap.Register('WIM', 32, wimBitMask)
wimReg.setDefaultValue(0)
wimReg.setDelay(3)
processor.addRegister(wimReg)
# Trap Base Register
tbrBitMask = {'TBA' : (12, 31), 'TT' : (4, 11)}
tbrReg = trap.Register('TBR', 32, tbrBitMask)
tbrReg.setDefaultValue(0)
processor.addRegister(tbrReg)
# Multiply / Divide Register
yReg = trap.Register('Y', 32)
#yReg.setDelay(3)
processor.addRegister(yReg)
# Program Counter
pcReg = trap.Register('PC', 32)
pcReg.setDefaultValue('ENTRY_POINT')
pcReg.setOffset(4)
processor.addRegister(pcReg)
# Program Counter
npcReg = trap.Register('NPC', 32)
npcReg.setDefaultValue(('ENTRY_POINT', 4))
#npcReg.setOffset(4)
processor.addRegister(npcReg)
# Ancillary State Registers
# in the LEON3 processor some of them have a special meaning:
# 24-31 are used for hardware breakpoints
# 17 is the processor configuration register
asrRegs = trap.RegisterBank('ASR', 32, 32)
# here I set the default value for the processor configuration register
# (see page 24 of LEON3 preliminary datasheed)
asrRegs.setDefaultValue(0x00000300 + numRegWindows, 17)
asrRegs.setGlobalDelay(3)
processor.addRegBank(asrRegs)

# Now I declare some fake registers for the exclusive use
# in the bypass: they allow exchangin information between
# different pipeline stages before register is written back
# to the register file.
# PSR forwarding is done for ICC code towards BRANCH and
# ALU instruction which need it.
psrBypassReg = trap.Register('PSRbp', 32, psrBitMask)
processor.addRegister(psrBypassReg)
# The forwarding for the Y register is performed for
# all ALU operations which use Y.
yBypassReg = trap.Register('Ybp', 32)
processor.addRegister(yBypassReg)
# The forwarding for the ASR[18] register is performed for
# the MAC operation which use the ASR register
ASR18BypassReg = trap.Register('ASR18bp', 32)
processor.addRegister(ASR18BypassReg)

# Now I set the alias: they can (and will) be used by the instructions
# to access the registers more easily. Note that, in general, it is
# responsibility of the programmer keeping the aliases updated
regs = trap.AliasRegBank('REGS', 32, ('GLOBAL[0-7]', 'WINREGS[0-23]'))
processor.addAliasRegBank(regs)
FP = trap.AliasRegister('FP', 'REGS[30]')
processor.addAliasReg(FP)
LR = trap.AliasRegister('LR', 'REGS[31]')
processor.addAliasReg(LR)
SP = trap.AliasRegister('SP', 'REGS[14]')
processor.addAliasReg(SP)
PCR = trap.AliasRegister('PCR', 'ASR[17]')
PCR.setDefaultValue(0x00000300 + numRegWindows - 1)
processor.addAliasReg(PCR)

# Now I add the registers which I want to see printed in the instruction trace
LEON3Isa.isa.addTraceRegister(pcReg)
LEON3Isa.isa.addTraceRegister(npcReg)
LEON3Isa.isa.addTraceRegister(psrReg)
LEON3Isa.isa.addTraceRegister(regs)
LEON3Isa.isa.addTraceRegister(tbrReg)
LEON3Isa.isa.addTraceRegister(wimReg)

# Memory alias: registers which are memory mapped; we
# loose a lot of performance, should we really use them?? CHECK
#for j in range(0, 8):
#    regMap = trap.MemoryAlias(0x300000 + j, 'GLOBAL[' + str(j) + ']')
#    processor.addMemAlias(regMap)
#for i in range(0, numRegWindows):
#    for j in range(0, 16):
#        regMap = trap.MemoryAlias(0x300008 + i*16 + j, 'WINREGS[' + str(i*16 + j) + ']')
#        processor.addMemAlias(regMap)
#regMap = trap.MemoryAlias(0x400000, 'Y')
#processor.addMemAlias(regMap)
#regMap = trap.MemoryAlias(0x400004, 'PSR')
#processor.addMemAlias(regMap)
#regMap = trap.MemoryAlias(0x40000C, 'WIM')
#processor.addMemAlias(regMap)
#regMap = trap.MemoryAlias(0x400010, 'PC')
#processor.addMemAlias(regMap)
#regMap = trap.MemoryAlias(0x400014, 'NPC')
#processor.addMemAlias(regMap)
#for j in range(16, 32):
#    regMap = trap.MemoryAlias(0x400040 + j, 'ASR[' + str(j) + ']')
#    processor.addMemAlias(regMap)

# Register from which the instructions are fetched; note that in the
# functional model there is an offset between the PC and the actual
# fetch address (all of this is to take into account the fact that we do
# not have the pipeline)
processor.setFetchRegister('PC', -4)

# Lets now add details about the processor interconnection (i.e. memory ports,
# interrupt ports, pins, etc.)
processor.addTLMPort('instrMem', True)
processor.addTLMPort('dataMem')
#processor.setMemory('dataMem', 10*1024*1024)
#processor.setMemory('dataMem', 10*1024*1024, True, 'PC')

# Now lets add the interrupt ports: TODO
# It PSR[ET] == 0 I do not do anything; else
# I check the interrupt level, if == 15 or > PSR[PIL] I service the interrupt,
# The interrupt level is carried by the value at the interrupt port
# Otherwise it is treated like a normal exception, to I jump to the
# TBR: we can use a routine for this ...
# At the end I have to acknowledge the interrupt, by writing on the ack
# port.
irqPort = trap.Interrupt('IRQ', 32)
irqPort.setOperation("""//Basically, what I have to do when
//an interrupt arrives is very simple: we check that interrupts
//are enabled and that the the processor can take this interrupt
//(valid interrupt level). The we simply raise an exception and
//acknowledge the IRQ on the irqAck port.
if(PSR[key_ET]){
    if(IRQ == 15 || IRQ > PSR[key_PIL]){
        // First of all I have to move to a new register window
        unsigned int newCwp = ((unsigned int)(PSR[key_CWP] - 1)) % """ + str(numRegWindows) + """;
        PSRbp = (PSR & 0xFFFFFFE0) | newCwp;
        PSR.immediateWrite(PSRbp);
        """ + updateWinCode + """
        // Now I set the TBR
        TBR[key_TT] = 0x10 + IRQ;
        // I have to jump to the address contained in the TBR register
        PC = TBR;
        NPC = TBR + 4;
        // finally I acknowledge the interrupt on the external pin port
        irqAck.send_pin_req(IRQ, 0);
    }
}
""")
irqPort.addTest({}, {})
#processor.addIrq(irqPort)

# I also need to add the external port which is used to acknowledge
# the interrupt
irqAckPin = trap.Pins('irqAck', 32, inbound = False)
processor.addPin(irqAckPin)

# Now it is time to add the pipeline stages
fetchStage = trap.PipeStage('fetch')
processor.addPipeStage(fetchStage)
decodeStage = trap.PipeStage('decode')
processor.addPipeStage(decodeStage)
regsStage = trap.PipeStage('regs')
regsStage.setHazard()
regsStage.setCheckUnknownInstr()
processor.addPipeStage(regsStage)
executeStage = trap.PipeStage('execute')
executeStage.setCheckTools()
processor.addPipeStage(executeStage)
memoryStage = trap.PipeStage('memory')
processor.addPipeStage(memoryStage)
exceptionStage = trap.PipeStage('exception')
processor.addPipeStage(exceptionStage)
wbStage = trap.PipeStage('wb')
wbStage.setWriteBack()
wbStage.setEndHazard()
processor.addPipeStage(wbStage)
processor.setWBOrder('NPC', ('decode', 'execute', 'wb'))
processor.setWBOrder('PC', ('decode', 'fetch', 'execute', 'wb'))
processor.setWBOrder('PSRbp', ('execute', 'wb'))
processor.setWBOrder('Ybp', ('execute', 'wb'))

# The ABI is necessary to emulate system calls, personalize the GDB stub and,
# eventually, retarget GCC
abi = trap.ABI('REGS[24]', 'REGS[24-29]', 'PC', 'LR', 'SP', 'FP')
abi.addVarRegsCorrespondence({'REGS[0-31]': (0, 31), 'Y': 64, 'PSR': 65, 'WIM': 66, 'TBR': 67, 'PC': 68, 'NPC': 69})
# ************* TODO ************ Do I need to check for register window over/under -flow even for
# systemcalls ?????
pre_code = """
unsigned int newCwp = ((unsigned int)(PSR[key_CWP] - 1)) % """ + str(numRegWindows) + """;
PSRbp = (PSR & 0xFFFFFFE0) | newCwp;
PSR.immediateWrite(PSRbp);
"""
pre_code += updateWinCode
post_code = """
unsigned int newCwp = ((unsigned int)(PSR[key_CWP] + 1)) % """ + str(numRegWindows) + """;
PSRbp = (PSR & 0xFFFFFFE0) | newCwp;
PSR.immediateWrite(PSRbp);
"""
post_code += updateWinCode
abi.setECallPreCode(pre_code)
abi.setECallPostCode(post_code)
abi.setOffset('PC', -4)
abi.returnCall([('PC', 'LR', 8), ('NPC', 'LR', 12)])
abi.addMemory('dataMem')
processor.setABI(abi)

# Finally we can dump the processor on file
#processor.write(folder = 'processor', models = ['funcLT'], dumpDecoderName = 'decoder.dot')
#processor.write(folder = 'processor', models = ['funcLT'], trace = True)
#processor.write(folder = 'processor', models = ['funcLT'], tests = False)
processor.write(folder = 'processor', models = ['funcLT'], trace = False, tests = False)
#processor.write(folder = 'processor', models = ['funcAT'], trace = False)
#processor.write(folder = 'processor', models = ['funcAT'])
#processor.write(folder = 'processor', models = ['funcAT', 'funcLT'], tests = False)
#processor.write(folder = 'processor', models = ['accAT'])
#processor.write(folder = 'processor', models = ['accAT','funcLT'], trace = True)
