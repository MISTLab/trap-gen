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
        print ('Please specify in file MICROBLAZEArch.py the path where the core TRAP files are located')

# It is nice to keep the ISA and the architecture separated
# so we use the import trick
import MICROBLAZEIsa

# Lets now start building the processor
#~ processor = trap.Processor('ARM7TDMI', version = '0.1', systemc = True, instructionCache = True, fastFetch = True)
#~ processor.setLittleEndian() #little endian
#~ processor.setWordsize(4, 8) #4 bytes per word, 8 bits per byte
#~ processor.setISA(ARMIsa.isa) #lets set the instruction set
processor = trap.Processor('MICROBLAZE', version = '0.1', systemc = False, instructionCache = True, fastFetch = True)
processor.setBigEndian() #big endian
processor.setWordsize(4, 8) #4 bytes per word, 8 bits per byte
processor.setISA(MICROBLAZEIsa.isa) #lets set the instruction set

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
#~ sprBank = trap.RegisterBank('SPR', 18, 32)
#~ processor.addRegBank(sprBank)

#~ msrBitMask = {'BE': (31,31), 'IE': (30,30), 'C': (29,29), 'BIP': (28,28), 'FSL': (27,27), 'ICE': (26,26), 'DZ': (25,25), 'DCE': (24,24), 'EE': (23,23), 'EIP': (22,22), 'PVR': (21,21), 'UM': (20,20), 'UMS': (19,19), 'VM': (18,18), 'VMS': (17,17), 'CC': (0,0)}
#~ MSR = trap.AliasRegister('MSR', 'SPR[1]',msrBitMask)
#~ processor.addAliasReg(MSR)

#~ ESR = trap.AliasRegister('ESR', 'SPR[5]')
#~ processor.addAliasReg(ESR)
#~ EAR = trap.AliasRegister('EAR', 'SPR[3]')
#~ processor.addAliasReg(EAR)
#~ FSR = trap.AliasRegister('FSR', 'SPR[7]')
#~ processor.addAliasReg(FSR)
# very strange register :)
#~ PVRx = trap.AliasRegister('PVR', 'SPR[8192+x]')
#~ processor.addAliasReg(PVRx)
#~ BTR = trap.AliasRegister('BTR', 'SPR[11]')
#~ processor.addAliasReg(BTR)
#~ PC = trap.AliasRegister('PC', 'SPR[0]')
#~ PC.setDefaultValue(('ENTRY_POINT',8))
#~ processor.addAliasReg(PC)

# We define each special register as a single isolated register
# PC = SPR[0]
pc = trap.Register('PC',32)
pc.setDefaultValue(('ENTRY_POINT',8))
processor.addRegister(pc)

# MSR = SPR[1]
msrBitMask = {'BE': (31,31), 'IE': (30,30), 'C': (29,29), 'BIP': (28,28), 'FSL': (27,27), 'ICE': (26,26), 'DZ': (25,25), 'DCE': (24,24), 'EE': (23,23), 'EIP': (22,22), 'PVR': (21,21), 'UM': (20,20), 'UMS': (19,19), 'VM': (18,18), 'VMS': (17,17), 'CC': (0,0)}
msr = trap.Register('MSR', 32, msrBitMask)
processor.addRegister(msr)

# ESR = SPR[5]
esr = trap.Register('ESR', 32)
processor.addRegister(esr)

# EAR = SPR[3]
ear = trap.Register('EAR', 32)
processor.addRegister(ear)

# FSR = SPR[7]
fsr = trap.Register('FSR', 32)
processor.addRegister(fsr)

# BTR = SPR[11]
btr = trap.Register('BTR', 32)
processor.addRegister(btr)

# At first, we simply define a pipeline with a single stage.
# All the operations of the instruction will be executed in this stage.
executeStage = trap.PipeStage('execute')
processor.addPipeStage(executeStage)

# Here we declare a memory for the MB (with size = 10MB)
processor.setMemory('dataMem', 10*1024*1024)

# The offset is '0', because we have a pipeline with a single stage.
# (I'm not sure about this)
processor.setFetchRegister('PC', 0)

# --->>>> WARNING <<<<---
# We are cheating! (temporarily, of course :D )
# The ABI is defined COMPLETELY RANDOM!
#abi = trap.ABI('GPR[0]', 'GPR[0-3]', 'PC', 'EAR', 'FSR', 'BTR')
#abi.addMemory('dataMem')
#processor.setABI(abi)

# Finally we can dump the processor on file
#processor.write(folder = 'processor', models = ['funcLT'], dumpDecoderName = 'decoder.dot')
#processor.write(folder = 'processor', models = ['funcLT'], trace = True)
processor.write(folder = 'processor', models = ['funcLT'])
#processor.write(folder = 'processor', models = ['funcAT'], trace = True)
#processor.write(folder = 'processor', models = ['accAT', 'funcLT'])
#processor.write(folder = 'processor', models = ['accAT'])
#processor.write(folder = 'processor', models = ['accAT','funcLT'], trace = True)
