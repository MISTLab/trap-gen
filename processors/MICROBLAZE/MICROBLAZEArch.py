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
        print ('Please specify in file ARMArch.py the path where the core TRAP files are located')

# It is nice to keep the ISA and the architecture separated
# so we use the import trick
import ARMIsa

# Lets now start building the processor
#~ processor = trap.Processor('ARM7TDMI', version = '0.1', systemc = True, instructionCache = True, fastFetch = True)
#~ processor.setLittleEndian() #little endian
#~ processor.setWordsize(4, 8) #4 bytes per word, 8 bits per byte
#~ processor.setISA(ARMIsa.isa) #lets set the instruction set
processor = trap.Processor('MICROBLAZE', version = '0.1', systemc = True, instructionCache = True, fastFetch = True)
processor.setBigEndian() #big endian
processor.setWordsize(4, 8) #4 bytes per word, 8 bits per byte
processor.setISA(ARMIsa.isa) #lets set the instruction set

# Ok, now we move to the description of more complicated processor
# resources

# A registry bank of 30 registers each one 32 bits wide:
# they are the normal registers and the banked one. In particular:

# TODO: general description of each register
#GPR = General Purpouse Registers
regBank = trap.RegisterBank('GPR', 30, 32) #GPR is the name, 30 registers of 32 bits
processor.addRegBank(regBank)

# A registry bank of 18 special purpouse registers each one 32 bits wide
#maybe we don't have to use a bit mask for this register bank
#spsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 3)}
sprBank = trap.RegisterBank('SPR', 18, 32)
processor.addRegBank(spsrBank)

# MicroBlaze doesn't have a processor status register (it is one of the special register)
# Current processor status register
#~ cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 3)}
#~ cpsr = trap.Register('CPSR', 32, cpsrBitMask)
#~ cpsr.setDefaultValue(0x000000D3)
#~ processor.addRegister(cpsr)

# Fake register (not presented in the architecture) indicating
# the processor ID: it is necessary in a multi-processor
# system
#~ mp_id = trap.Register('MP_ID', 32)
#~ processor.addRegister(mp_id)

# Now I set the alias: they can (and will) be used by the instructions
# to access the registers more easily. Note that, in general, it is
# responsibility of the programmer keeping the alias updated
#~ regs = trap.AliasRegBank('REGS', 16, 'RB[0-15]')
#~ regs.setOffset(15, 4)
#~ processor.addAliasRegBank(regs)
#~ FP = trap.AliasRegister('FP', 'REGS[12]')
#~ processor.addAliasReg(FP)
#~ SP = trap.AliasRegister('SPTR', 'REGS[13]')
#~ processor.addAliasReg(SP)
#~ LR = trap.AliasRegister('LINKR', 'REGS[14]')
#~ processor.addAliasReg(LR)
#~ SP_IRQ = trap.AliasRegister('SP_IRQ', 'RB[21]')
#~ processor.addAliasReg(SP_IRQ)
#~ LR_IRQ = trap.AliasRegister('LR_IRQ', 'RB[22]')
#~ processor.addAliasReg(LR_IRQ)
#~ SP_FIQ = trap.AliasRegister('SP_FIQ', 'RB[28]')
#~ processor.addAliasReg(SP_FIQ)
#~ LR_FIQ = trap.AliasRegister('LR_FIQ', 'RB[29]')
#~ processor.addAliasReg(LR_FIQ)
#~ PC = trap.AliasRegister('PC', 'REGS[15]')
# Special default value, others are PROGRAM_LIMIT ...
#~ PC.setDefaultValue('ENTRY_POINT')
#~ processor.addAliasReg(PC)
# Memory alias: registers which are memory mapped:
#~ idMap = trap.MemoryAlias(0xFFFFFFF0, 'MP_ID')
#~ processor.addMemAlias(idMap)
# register from which the instructions are fetched; note that in the
# functional model there is an offset between the PC and the actual
# fetch address (all of this is to take into account the fact that we do
# not have the pipeline)
#~ processor.setFetchRegister('PC', -4)


#~ SP = trap.AliasRegister('SPTR', 'REGS[13]')
#~ processor.addAliasReg(SP)
MSR = trap.AliasRegister('MSR', 'SPR[1]')
processor.addAliasReg(MSR)

# mask definition for MSR register
#~ cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 3)}
#~ cpsr = trap.Register('CPSR', 32, cpsrBitMask)
#~ cpsr.setDefaultValue(0x000000D3)
#~ processor.addRegister(cpsr)
msrBitMask = {'BE': (31,31), 'IE': (30,30), 'C': (29,29), 'BIP': (28,28), 'FSL': (27,27), 'ICE': (26,26), 'DZ': (25,25), 'DCE': (24,24), 'EE': (23,23), 'EIP': (22,22), 'PVR': (21,21), 'UM': (20,20), 'UMS': (19,19), 'VM': (18,18), 'VMS': (17,17), 'CC': (0,0)}
#?? how can we specify a bit mask for a single register that is already defined?
#?? (in fact we define MSR register as one of the special purpouse register bank!
# TODO: we have to associate msrBitMask with the MSR register!

ESR = trap.AliasRegister('ESR', 'SPPR[5]')
processor.addAliasReg(ESR)
EAR = trap.AliasRegister('EAR', 'SPR[3]')
processor.addAliasReg(EAR)
FSR = trap.AliasRegister('FSR', 'SPR[7]')
processor.addAliasReg(FSR)
# very strange register :)
#~ PVRx = trap.AliasRegister('PVR', 'SPR[8192+x]')
#~ processor.addAliasReg(PVRx)
BTR = trap.AliasRegister('BTR', 'SPR[11]')
processor.addAliasReg(BTR)
PC = trap.AliasRegister('PC', 'SPR[0]')
processor.addAliasReg(PC)

# Lets now add details about the processor interconnection (i.e. memory ports,
# interrupt ports, pins, etc.)
#~ processor.addTLMPort('instrMem', True)
#~ processor.addTLMPort('dataMem')
#processor.setMemory('dataMem', 10*1024*1024)
# Now lets add the interrupt ports
#~ irq = trap.Interrupt('IRQ', priority = 0)
#~ irq.setOperation('CPSR[key_I] == 0', """
#~ //Save LR_irq
#~ LR_IRQ = PC;
#~ //Save the current PSR
#~ SPSR[1] = CPSR;
#~ //I switch the register bank (i.e. I update the
#~ //alias)
#~ REGS[13].updateAlias(RB[21]);
#~ REGS[14].updateAlias(RB[22]);
#~ //Create the new PSR
#~ CPSR = (CPSR & 0xFFFFFFD0) | 0x00000092;
#~ //Finally I update the PC
#~ PC = 0x18;""")
#~ #processor.addIrq(irq)
#~ fiq = trap.Interrupt('FIQ', priority = 1)
#~ fiq.setOperation('CPSR[key_F] == 0', """
#~ //Save LR_irq
#~ LR_FIQ = PC;
#~ //Save the current PSR
#~ SPSR[0] = CPSR;
#~ //I switch the register bank (i.e. I update the
#~ //alias)
#~ REGS[8].updateAlias(RB[23]);
#~ REGS[9].updateAlias(RB[24]);
#~ REGS[10].updateAlias(RB[25]);
#~ REGS[11].updateAlias(RB[26]);
#~ REGS[12].updateAlias(RB[27]);
#~ REGS[13].updateAlias(RB[28]);
#~ REGS[14].updateAlias(RB[29]);
#~ //Create the new PSR
#~ CPSR = (CPSR & 0xFFFFFFD0) | 0x000000D1;
#~ //Finally I update the PC
#~ PC = 0x1C;""")
#processor.addIrq(fiq)


#?? does user/special mode change alias of the registers?
#?? do we have to update alias for this reason in the ARM?


# Now it is time to add the pipeline stages
#~ fetchStage = trap.PipeStage('fetch')
#~ processor.addPipeStage(fetchStage)
#~ decodeStage = trap.PipeStage('decode')
#~ decodeStage.setHazard()
#~ processor.addPipeStage(decodeStage)
#~ executeStage = trap.PipeStage('execute')
#~ executeStage.setWriteBack()
#~ executeStage.setEndHazard()
#~ executeStage.setCheckUnknownInstr()
#~ executeStage.setCheckTools()
#~ processor.addPipeStage(executeStage)

# At first, we simply define a pipeline with a single stage.
# All the operations of the instruction will be executed in this stage.
executeStage = trap.PipeStage('execute')
processor.addPipeStage(executeStage)


#TODO: understand what is ABI and why is this important!
# The ABI is necessary to emulate system calls, personalize the GDB stub and,
# eventually, retarget GCC
#~ abi = trap.ABI('REGS[0]', 'REGS[0-3]', 'PC', 'LINKR', 'SPTR', 'FP')
#~ abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'CPSR': 16})
# Same consideration as above: this offset is valid just for the functional
# simulator
#~ abi.setOffset('PC', -4)
#~ abi.setOffset('REGS[15]', -4)
#~ abi.addMemory('dataMem')
#~ processor.setABI(abi)

# Finally we can dump the processor on file
#processor.write(folder = 'processor', models = ['funcLT'], dumpDecoderName = 'decoder.dot')
#processor.write(folder = 'processor', models = ['funcLT'], trace = True)
#processor.write(folder = 'processor', models = ['funcLT'])
#processor.write(folder = 'processor', models = ['funcAT'], trace = True)
processor.write(folder = 'processor', models = ['accAT', 'funcLT'])
#processor.write(folder = 'processor', models = ['accAT'])
#processor.write(folder = 'processor', models = ['accAT','funcLT'], trace = True)
