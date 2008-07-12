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
    import sys
    sys.path.append('/home/luke/SVN/trap-gen/')
    try:
        import trap
    except ImportError:
        print 'Please specify in file ARMArch.py the path where the core TRAP files are located'

# It is nice to keep the ISA and the architecture separated
# so we use the import trick
import ARMIsa

# Lets now start building the processor
processor = trap.Processor('ARM7TDMI')
processor.setLittleEndian() #little endian
processor.setWordsize(4, 8) #4 bytes per word, 8 bits per byte
processor.setISA(ARMIsa.isa) #lets set the instruction set

# Ok, now we move to the description of more complicated processor
# resources

# A registry bank of 22 registers each one 32 bits wide:
# they are the normal registers and the banked one. In particular:
# RB[0-7]: registers shared among all the modes
# RB[8-12]: registers shared among all modes but FIQ
# RB[13-14]: sp_user, lr_user
# RB[15-16]: sp_svc, lr_svc
# RB[17-18]: sp_abt, lr_abt
# RB[19-20]: sp_und, lr_und
# RB[21-22]: sp_irq, lr_irq
# RB[23-29]: r8_fiq, r14_fiq
regBank = trap.RegisterBank('RB', 30, 32)
processor.addRegBank(regBank)
# A registry bank of 5 registers each one 32 bits wide
# they are the saved processor status registers for the different
# execution modes; note that a bit mask for easily accessing
# the different fields is provided
# SPSR[0] = spsr_fiq, SPSR[1] = spsr_irq, SPSR[2] = spsr_svc,
# SPSR[3] = spsr_abt, SPSR[4] = spsr_und
spsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 3)}
spsrBank = trap.RegisterBank('SPSR', 5, 32, spsrBitMask)
processor.addRegBank(spsrBank)
# Current processor status register
cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 3)}
cpsr = trap.Register('CPSR', 32, cpsrBitMask)
cpsr.setDefaultValue(0x000000D3)
processor.addRegister(cpsr)
# Fake register (not presented in the architecture) indicating
# the processor ID: it is necessary in a multi-processor
# system
mp_id = trap.Register('MP_ID', 32)
processor.addRegister(mp_id)
# Now I set the alias: they can (and will) be used by the instructions
# to access the registers more easily. Note that, in general, it is
# responsibility of the programmer keeping the alias updated
regs = trap.AliasRegBank('REGS', 16, 32, 'RB[0-15]')
processor.addAliasRegBank(regs)
FP = trap.AliasRegister('FP', 32, 'REGS[12]')
processor.addAliasReg(FP)
SP = trap.AliasRegister('SP', 32, 'REGS[13]')
processor.addAliasReg(SP)
LR = trap.AliasRegister('LR', 32, 'REGS[14]')
processor.addAliasReg(LR)
SP_IRQ = trap.AliasRegister('SP_IRQ', 32, 'RB[21]')
processor.addAliasReg(SP_IRQ)
LR_IRQ = trap.AliasRegister('LR_IRQ', 32, 'RB[22]')
processor.addAliasReg(LR_IRQ)
SP_FIQ = trap.AliasRegister('SP_FIQ', 32, 'RB[28]')
processor.addAliasReg(SP_FIQ)
LR_FIQ = trap.AliasRegister('LR_FIQ', 32, 'RB[29]')
processor.addAliasReg(LR_FIQ)
PC = trap.AliasRegister('PC', 32, 'REGS[15]')
# Special default value, others are PROGRAM_LIMIT ...
# I also set the offset
PC.setDefaultValue(('ENTRY_POINT', 8))
processor.addAliasReg(PC)
# Memory alias: registers which are memory mapped:
idMap = trap.MemoryAlias(0xFFFFFFF0, 'MP_ID')
processor.addMemAlias(idMap)
# register from which the instructions are fetched; note that in the
# functional model there is an offset between the PC and the actual
# fetch address (all of this is to take into account the fact that we do
# not have the pipeline)
processor.setFetchRegister('PC', -8)

# Lets now add details about the processor interconnection (i.e. memory ports,
# interrupt ports, pins, etc.)
processor.addTLMPort('memPort', True)
#processor.setMemSize(10*1024*1024)
irq = trap.Interrupt('IRQ', priority = 0)
processor.addIrq(irq)
fiq = trap.Interrupt('FIQ', priority = 1)
processor.addIrq(fiq)
# I also have to set the behavior method which is called to check for the
# interrupts and take the appropriate action. This method is
# called before every instruction is issued.
# TODO: I do not like it too much ... any better ideas?; is there
# a way of making this more automatic?
processor.setIRQOperation(ARMIsa.IRQOperation)

# Now it is time to add the pipeline stages
fetchStage = trap.PipeStage('fetch')
processor.addPipeStage(fetchStage)
decodeStage = trap.PipeStage('decode')
processor.addPipeStage(decodeStage)
executeStage = trap.PipeStage('execute')
processor.addPipeStage(executeStage)

# The ABI is necessary to emulate system calls, personalize the GDB stub and,
# eventually, retarget GCC
abi = trap.ABI('REGS[0]', 'REGS[0-3]', 'PC', 'LR', 'SP', 'FP')
abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'CPSR': (25, 25)})
# Same consideration as above: this offset is valid just for the functional
# simulator
abi.setOffset('PC', -8)
abi.setOffset('REGS[15]', -8)
processor.setABI(abi)

# Finally we can dump the processor on file
#processor.write(folder = 'processor', models = ['funcLT'], dumpDecoderName = 'decoder.dot')
processor.write(folder = 'processor', models = ['funcLT'])
