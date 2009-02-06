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
        print 'Please specify in file LEON3Arch.py the path where the core TRAP files are located'

import cxx_writer

# It is nice to keep the ISA and the architecture separated
# so we use the import trick
import LEON3Isa

# Lets now start building the processor
processor = trap.Processor('LEON3', systemc = False, instructionCache = True, fastFetch = True)
processor.setBigEndian() # big endian
processor.setWordsize(4, 8) # 4 bytes per word, 8 bits per byte
processor.setISA(LEON3Isa.isa) # lets set the instruction set

# Ok, now we move to the description of more complicated processor
# resources
# Number of register windows, between 2 and 32, default is 8 for LEON3
numRegWindows = 8

LEON3Isa.isa.addConstant(cxx_writer.writer_code.uintType, 'NUM_REG_WIN', numRegWindows)

# There are 8 global register, and a variable number of
# of 16-registers set; this number depends on the number of
# register windows
# global registers
globalRegs = trap.RegisterBank('GLOBAL', 8, 32)
processor.addRegBank(globalRegs)
windowRegs = trap.RegisterBank('WINREGS', 16*numRegWindows, 32)
processor.addRegBank(windowRegs)
# Program status register
psrBitMask = {'IMPL': (31, 28), 'VER': (27, 24), 'ICC': (23, 20), 'EC': (13, 13), 'EF': (12, 12), 'PIL': (11, 8), 'S': (7, 7), 'PS': (6, 6), 'ET': (5, 5), 'CWP': (4, 0)}
psrReg = trap.Register('PSR', 32, psrBitMask)
# TODO: Check: should the CWP be the last (i.e. numRegWindows - 1) or fist (i.e. 0)
# register window????In case change also the initialization of the alias register windows
psrReg.setDefaultValue(0xF3000080 + numRegWindows - 1)
processor.addRegister(psrReg)
# Window Invalid Mask Register
wimBitMask = {}
for i in range(0, 32):
    wimBitMask['WIM_' + str(i)] = (i, i)
wimReg = trap.Register('WIM', 32, wimBitMask)
# TODO: CHECK: should this be init to 0 or not?????
wimReg.setDefaultValue(0xFFFFFFFF ^ (pow(2, numRegWindows) - 1))
processor.addRegister(wimReg)
# Trap Base Register
tbrBitMask = {'TBA' : (31, 12), 'TT' : (11, 4)}
tbrReg = trap.Register('TBR', 32, tbrBitMask)
processor.addRegister(tbrReg)
# Multiply / Divide Register
yReg = trap.Register('Y', 32)
processor.addRegister(yReg)
# Program Counter
pcReg = trap.Register('PC', 32)
pcReg.setDefaultValue('ENTRY_POINT')
pcReg.setOffset(4)
processor.addRegister(pcReg)
# Program Counter
npcReg = trap.Register('NPC', 32)
npcReg.setDefaultValue(('ENTRY_POINT', 4))
pcReg.setOffset(4)
processor.addRegister(npcReg)
# Ancillary State Registers
# in the LEON3 processor some of them have a special meaning:
# 24-31 are used for hardware breakpoints
# 17 is the processor configuration register
asrRegs = trap.RegisterBank('ASR', 32, 32)
processor.addRegBank(asrRegs)

# Now I set the alias: they can (and will) be used by the instructions
# to access the registers more easily. Note that, in general, it is
# responsibility of the programmer keeping the aliases updated
regs = trap.AliasRegBank('REGS', 32, ('GLOBAL[0-7]', 'WINREGS['  + str(16*(numRegWindows - 2) - 1) + '-' + str(16*numRegWindows - 1) + ']'))
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
#processor.addTLMPort('instrMem', True)
#processor.addTLMPort('dataMem')
processor.setMemory('dataMem', 10*1024*1024)

# Now lets add the interrupt ports: TODO
# It PSR[ET] == 0 I do not do anything; else
# I check the interrupt level, if == 15 or > PSR[PIL] I service the interrupt,
# otherwise I put it in a queue. The interrupt level depends on the interrupt line
# (actually I can have an external interrupt controller and a complex input line
# or a simple interrupt controller and just an input signal)
# Otherwise it is treated like a normal exception, to I jump to the 
# TBR: we can use a routine for this ...
# TODO: do we check for exceptions in the fetch or exception stage???
# TODO: SVT (Single vector trapping) must be configurable in the ASR[17]
# and we also have to behave accordingly when interrupts are found
irq = trap.Interrupt('IRQ', priority = 0)
irq.setOperation('/*TODO*/', """
Using the current interrupt request level (IRL) we
jump to the TBR (using also the request level to
complete the TBR address)
it pst[et] == 0 we ignore the request
We postpone the interrupt for later processing
in case the IRL > psr[pil] or IRL == 15
//TODO""")
#processor.addIrq(irq)

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
processor.setWBOrder('NPC', ('decode', 'execute'))

# The ABI is necessary to emulate system calls, personalize the GDB stub and,
# eventually, retarget GCC
abi = trap.ABI('REGS[24]', 'REGS[24-29]', 'PC', 'LR', 'SP', 'FP')
abi.addVarRegsCorrespondence({'REGS[0-31]': (0, 31), 'Y': 64, 'PSR': 65, 'WIM': 66, 'TBR': 67, 'PC': 68, 'NPC': 69})
abi.setOffset('PC', -4)
abi.setOffset('NPC', -4)
abi.addMemory('dataMem')
processor.setABI(abi)

# Finally we can dump the processor on file
#processor.write(folder = 'processor', models = ['funcLT'], dumpDecoderName = 'decoder.dot')
processor.write(folder = 'processor', models = ['funcLT'], trace = True)
#processor.write(folder = 'processor', models = ['funcLT'])
#processor.write(folder = 'processor', models = ['funcAT'], trace = True)
#processor.write(folder = 'processor', models = ['funcAT', 'funcLT'])
#processor.write(folder = 'processor', models = ['accAT'])
#processor.write(folder = 'processor', models = ['accAT','funcLT'], trace = True)
