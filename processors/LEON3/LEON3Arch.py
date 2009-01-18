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
# Check: should the CWP be the last (i.e. numRegWindows - 1) or fist (i.e. 0)
# register window????
psrReg.setDefaultValue(0xF3000080 + numRegWindows - 1)
processor.addRegister(psrReg)
# Window Invalid Mask Register
wimBitMask = {}
for i in range(0, 32):
    wimBitMask['WIM_' + str(i)] = (i, i)
wimReg = trap.Register('WIM', 32, wimBitMask)
# CHECK: should this be init to 0 or not?????
wimReg.setDefaultValue(pow(2, numRegWindows - 1))
processor.addRegister(wimReg)
# Trap Base Register
tbrBitMask = {'TBA' : (31, 12), 'TT' : (11, 4)}
tbrReg = trap.Register('TBR', 32, tbrBitMask)
processor.addRegister(tbrReg)
# Multiply / Divide Register
yReg = trap.Register('Y', 32)
processor.addRegister(yReg)
# Program Counter, TODO: how do we offset a register? in functional we should offset the PC
pcReg = trap.Register('PC', 32)
pcReg.setDefaultValue('ENTRY_POINT')
processor.addRegister(pcReg)
# Program Counter, TODO: how do we offset a register? in functional we should offset the NPC
npcReg = trap.Register('NPC', 32)
npcReg.setDefaultValue(('ENTRY_POINT', 4))
processor.addRegister(npcReg)
# Ancillary State Registers
# in the LEON3 processor some of them have a special meaning:
# 24-31 are used for hardware breakpoints
# 17 is the processor configuration register
asrRegs = trap.RegisterBank('ASR', 32, 32)
processor.addRegBank(asrRegs)

## Now I set the alias: they can (and will) be used by the instructions
## to access the registers more easily. Note that, in general, it is
## responsibility of the programmer keeping the alias updated
#regs = trap.AliasRegBank('REGS', 16, 'RB[0-15]')
#regs.setOffset(15, 4)
#processor.addAliasRegBank(regs)
#FP = trap.AliasRegister('FP', 'REGS[12]')
#processor.addAliasReg(FP)
#SP = trap.AliasRegister('SPTR', 'REGS[13]')
#processor.addAliasReg(SP)
#LR = trap.AliasRegister('LINKR', 'REGS[14]')
#processor.addAliasReg(LR)
#SP_IRQ = trap.AliasRegister('SP_IRQ', 'RB[21]')
#processor.addAliasReg(SP_IRQ)
#LR_IRQ = trap.AliasRegister('LR_IRQ', 'RB[22]')
#processor.addAliasReg(LR_IRQ)
#SP_FIQ = trap.AliasRegister('SP_FIQ', 'RB[28]')
#processor.addAliasReg(SP_FIQ)
#LR_FIQ = trap.AliasRegister('LR_FIQ', 'RB[29]')
#processor.addAliasReg(LR_FIQ)
#PC = trap.AliasRegister('PC', 'REGS[15]')
## Special default value, others are PROGRAM_LIMIT ...
#PC.setDefaultValue('ENTRY_POINT')
#processor.addAliasReg(PC)
## Memory alias: registers which are memory mapped:
#idMap = trap.MemoryAlias(0xFFFFFFF0, 'MP_ID')
#processor.addMemAlias(idMap)
## register from which the instructions are fetched; note that in the
## functional model there is an offset between the PC and the actual
## fetch address (all of this is to take into account the fact that we do
## not have the pipeline)
#processor.setFetchRegister('PC', -4)

## Lets now add details about the processor interconnection (i.e. memory ports,
## interrupt ports, pins, etc.)
#processor.addTLMPort('instrMem', True)
#processor.addTLMPort('dataMem')
##processor.setMemory('dataMem', 10*1024*1024)
## Now lets add the interrupt ports
#irq = trap.Interrupt('IRQ', priority = 0)
#irq.setOperation('CPSR[key_I] == 0', """
#//Save LR_irq
#LR_IRQ = PC;
#//Save the current PSR
#SPSR[1] = CPSR;
#//I switch the register bank (i.e. I update the
#//alias)
#REGS[13].updateAlias(RB[21]);
#REGS[14].updateAlias(RB[22]);
#//Create the new PSR
#CPSR = (CPSR & 0xFFFFFFD0) | 0x00000092;
#//Finally I update the PC
#PC = 0x18;""")
##processor.addIrq(irq)
#fiq = trap.Interrupt('FIQ', priority = 1)
#fiq.setOperation('CPSR[key_F] == 0', """
#//Save LR_irq
#LR_FIQ = PC;
#//Save the current PSR
#SPSR[0] = CPSR;
#//I switch the register bank (i.e. I update the
#//alias)
#REGS[8].updateAlias(RB[23]);
#REGS[9].updateAlias(RB[24]);
#REGS[10].updateAlias(RB[25]);
#REGS[11].updateAlias(RB[26]);
#REGS[12].updateAlias(RB[27]);
#REGS[13].updateAlias(RB[28]);
#REGS[14].updateAlias(RB[29]);
#//Create the new PSR
#CPSR = (CPSR & 0xFFFFFFD0) | 0x000000D1;
#//Finally I update the PC
#PC = 0x1C;""")
##processor.addIrq(fiq)

# Now it is time to add the pipeline stages
fetchStage = trap.PipeStage('fetch')
processor.addPipeStage(fetchStage)
decodeStage = trap.PipeStage('decode')
processor.addPipeStage(decodeStage)
regsStage = trap.PipeStage('regs')
regsStage.setHazard()
executeStage.setCheckUnknownInstr()
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
processor.addPipeStage(wbStage)

## The ABI is necessary to emulate system calls, personalize the GDB stub and,
## eventually, retarget GCC
#abi = trap.ABI('REGS[0]', 'REGS[0-3]', 'PC', 'LINKR', 'SPTR', 'FP')
#abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'CPSR': 16})
## Same consideration as above: this offset is valid just for the functional
## simulator
#abi.setOffset('PC', -4)
#abi.setOffset('REGS[15]', -4)
#abi.addMemory('dataMem')
#processor.setABI(abi)

## Finally we can dump the processor on file
##processor.write(folder = 'processor', models = ['funcLT'], dumpDecoderName = 'decoder.dot')
##processor.write(folder = 'processor', models = ['funcLT'], trace = True)
##processor.write(folder = 'processor', models = ['funcLT'])
##processor.write(folder = 'processor', models = ['funcAT'], trace = True)
##processor.write(folder = 'processor', models = ['funcAT', 'funcLT'])
##processor.write(folder = 'processor', models = ['accAT'])
#processor.write(folder = 'processor', models = ['accAT','funcLT'], trace = True)
