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
processor = trap.Processor('MICROBLAZE', version = '0.1', systemc = False, instructionCache = True, fastFetch = True)
processor.setBigEndian() #big endian
processor.setWordsize(4, 8) #4 bytes per word, 8 bits per byte
processor.setISA(MICROBLAZEIsa.isa) #lets set the instruction set

# Ok, now we move to the description of more complicated processor
# resources

# A registry bank of 32 registers each one 32 bits wide:
# they are the normal registers and the banked one. In particular:

# TODO: general description of each register
#GPR = General Purpouse Registers
regBank = trap.RegisterBank('GPR', 32, 32) #GPR is the name, 32 registers of 32 bits
processor.addRegBank(regBank)

# We define each special register as a single isolated register
# PC = SPR[0x0000]
pc = trap.Register('PC',32)
pc.setDefaultValue(('ENTRY_POINT',8))
processor.addRegister(pc)

# MSR = SPR[0x0001]
msrBitMask = {'BE': (31,31), 'IE': (30,30), 'C': (29,29), 'BIP': (28,28), 'FSL': (27,27), 'ICE': (26,26), 'DZ': (25,25), 'DCE': (24,24), 'EE': (23,23), 'EIP': (22,22), 'PVR': (21,21), 'UM': (20,20), 'UMS': (19,19), 'VM': (18,18), 'VMS': (17,17), 'CC': (0,0)}
msr = trap.Register('MSR', 32, msrBitMask)
processor.addRegister(msr)

# EAR = SPR[0x0003]
ear = trap.Register('EAR', 32)
processor.addRegister(ear)

# ESR = SPR[0x0005]
esrBitMask = {'DS': (19,19), 'W': (20,20), 'S': (21,21), 'Rx': (22,26), 'EC': (27,31)}
esr = trap.Register('ESR', 32, esrBitMask)
processor.addRegister(esr)

# BTR = SPR[0x000b]
btr = trap.Register('BTR', 32)
processor.addRegister(btr)

# FSR = SPR[0x0007]
fsrBitMask = {'IO': (27,27), 'DZ': (28,28), 'OF': (29,29), 'UF': (30,30), 'DO': (31,31)}
fsr = trap.Register('FSR', 32, fsrBitMask)
processor.addRegister(fsr)

# EDR = SPR[0x000d]
edr = trap.Register('EDR', 32)
processor.addRegister(edr)

# PID = SPR[0x1000]
pidBitMask = {'PID': (24,31)}
pid = trap.Register('PID', 32)
processor.addRegister(pid)

# ZPR = SPR[0x1001]
zpr = trap.Register('ZPR',32)
processor.addRegister(zpr)

# TLBLO = SPR[0x1003]
tlblo = trap.Register('TLBLO',32)
processor.addRegister(tlblo)

# TLBHI = SPR[0x1004]
tlbhi = trap.Register('TLBHI',32)
processor.addRegister(tlbhi)

# TLBX = SPR[0x1002]
tlbx = trap.Register('TLBX',32)
processor.addRegister(tlbx)

# TLBSX = SPR[0x1005]
tlbsx = trap.Register('TLBSX',32)
processor.addRegister(tlbsx)

# PVRs registers.
pvrBank = trap.RegisterBank('PVR',12,32);
processor.addRegBank(pvrBank);

#Now, we declare some fake registers.

#IMMREG register is useful in order to describe the IMM instruction.
immreg = trap.Register('IMMREG', 32)
immreg.setDefaultValue(0x00000000)
processor.addRegister(immreg)

#TARGET register is useful to modelize all the instruction with a delay slot.
target = trap.Register('TARGET', 32)
target.setDefaultValue(0xffffffff)
processor.addRegister(target)

#DSFLAG bit is a flag that indicates if the current instruction is in a delay slot.
dsflag = trap.Register('DSFLAG', 1)
dsflag.setDefaultValue(0x0)
processor.addRegister(dsflag)

#FAKE: this register will be removed soon.
fake = trap.Register('FAKE',32)
processor.addRegister(fake)

# At first, we simply define a pipeline with a single stage.
# All the operations of the instruction will be executed in this stage.
executeStage = trap.PipeStage('execute')
processor.addPipeStage(executeStage)

# Here we declare a memory for the MB (with size = 10MB)
processor.setMemory('dataMem', 10*1024*1024)

# Here we set the register from which we will fetch the next instruction
processor.setFetchRegister('PC', 0)

#TODO: remove the FAKE register ASAP!
abi = trap.ABI('GPR[3-4]', 'GPR[5-10]', 'PC', 'GPR[15]', 'GPR[1]')
abi.setOffset('PC', 0)
abi.addMemory('dataMem')
processor.setABI(abi)

# Finally we can dump the processor on file
#processor.write(folder = 'processor', models = ['funcLT'], dumpDecoderName = 'decoder.dot')
#processor.write(folder = 'processor', models = ['funcLT'], trace = True)
processor.write(folder = 'processor', models = ['funcLT'])
#processor.write(folder = 'processor', models = ['funcAT'], trace = True)
#processor.write(folder = 'processor', models = ['accAT', 'funcLT'])
#processor.write(folder = 'processor', models = ['accAT'])
#processor.write(folder = 'processor', models = ['accAT','funcLT'], trace = True)
