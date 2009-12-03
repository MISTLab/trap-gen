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
#   (a) Luca Fossati, fossati@elet.polimi.it
#   (b) Redwanur Rahman, md.rahman@mail.polimi.it
#   (c) Ashanka das, ashanka.das@mail.polimi.it
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
        print ('Please specify in file PPC405Arch.py the path where the core TRAP files are located')

##import cxx_writer

# It is nice to keep the ISA and the architecture separated
# so we use the import trick
import PPC405Isa
##import PPC405Tests

# Lets now start building the processor
processor = trap.Processor('PPC405', version = '0.0.1', systemc = False, instructionCache = True, fastFetch = True) # need to check this line
processor.setBigEndian() # big endian
processor.setWordsize(4, 8) # 4 bytes per word, 8 bits per byteprocessor.setISA(PPC405Isa.isa) # lets set the instruction set


##General 32 registers in PPC405
gprRegs = trap.RegisterBank('GPR', 32, 32)
##globalRegs.setConst(0, 0) # what should be the value
processor.addRegBank(gprRegs)

#Configure Register are 2 CCR0 & CCR1
# core Configure register 0
ccr0BitMask = {'CWS': (31, 31),'PRS': (28, 28),'CIS': (27, 27),'FWOA': (23, 23),'NCRS': (22, 22),'PFNC': (21, 21), 'PFC': (20, 20), 'TPE': (19, 19), 'IPE': (18, 18), 'LBDE': (15, 15), 'UOXE': (14, 14), 'DPP': (13, 13), 'DPE': (12, 12), 'IPP': (10, 11), 'DPP1': (9, 9), 'SWOA': (8, 8), 'LWOA': (7, 7), 'LWL': (6, 6)}
ccr0Reg = trap.Register('CCR0', 32, ccr0BitMask)
ccr0Reg.setDefaultValue(0x00700000) #  value as per page 79 
##ccr0Reg.setDelay(3)
processor.addRegister(ccr0Reg)
# core Configure register 1
ccr1BitMask = {'TLBE': (4, 4), 'DCDE': (3, 3), 'DCTE': (2, 2), 'ICDE': (1, 1), 'ICTE': (0, 0)}
ccr1Reg = trap.Register('CCR1', 32, ccr1BitMask)
##ccr1Reg.setDefaultValue(0x0) # need that value 
processor.addRegister(ccr1Reg)

#Branch Control registers CTR & LR
# Counter register CTR  
ctrReg = trap.Register('CTR', 32)
##ctrReg.setDefaultValue(0) # need that value 
processor.addRegister(ctrReg)
# Link register LR  Register
lrReg = trap.Register('LR', 32)
processor.addRegister(lrReg)

#Debug registers DAC1, DAC2, DBCR0, DBCR1,DBSR,DVC1,DVC2,IAC1,IAC2,IAC3,IAC4,ICDBDR
#Data Address Compare Registers register DAC1 & DAC2
dac1Reg = trap.Register('DAC1', 32)
processor.addRegister(dac1Reg)
dac2Reg = trap.Register('DAC2', 32)
processor.addRegister(dac2Reg)
#Debug Control Registers DBCR0, DBCR1
dbcr0BitMask = {'FT': (31, 31),'IA34T': (17, 17),'IA12T': (16, 16),'IA34X': (15, 15),'IA34': (14, 14),'IA4': (13, 13),'IA3': (12, 12),'IA12X': (11, 11),'IA12': (10, 10),'IA2': (9, 9),'IA1': (8, 8),'TDE': (7, 7),'EDE': (6, 6), 'BT': (5, 5), 'RST': (2, 3), 'IDM': (1, 1), 'EDM': (0, 0)}dbcr0Reg = trap.Register('BDCR0', 32, dbcr0BitMask)
dbcr0Reg.setDefaultValue(0) # value as per page 79
processor.addRegister(dbcr0Reg)
dbcr1BitMask = {'DB1BE': (20, 23),'DB1BE': (16, 19),'DV2M': (14, 15),'DV1M': (12, 13),'DA12X': (9, 9),'DA12': (8, 8),'D2S': (6, 7),'D1S': (4, 5), 'D2W': (3, 3), 'D1W': (2, 2), 'D2R': (1, 1), 'D1R': (0, 0)}dbcr1Reg = trap.Register('DBCR1', 32, dbcr1BitMask)
dbcr1Reg.setDefaultValue(0x00000000) #value as per page 79
processor.addRegister(dbcr1Reg)
# Debug Status Register DBSR
dbsrBitMask = {'MRR': (22, 23),'IA4': (13, 13),'IA3': (12, 12),'DIE': (11, 11),'DW2': (10, 10),'DR2': (9, 9),'DW1': (8, 8),'DR1': (7, 7),'IA2': (6, 6),'IA1': (5, 5),'UDE': (4, 4), 'TIE': (3, 3), 'EDE': (2, 2), 'BT': (1, 1), 'IC': (0, 0)}dbsrReg = trap.Register('DBSR', 32, dbsrBitMask)
##dbsrReg.setDefaultValue(11) # 01,10, 11 which one 
processor.addRegister(dbsrReg)
# Data Value Compare Registers (DVC1–DVC2)
dvc1Reg = trap.Register('DVC1', 32)
processor.addRegister(dvc1Reg)
dvc2Reg = trap.Register('DVC2', 32)
processor.addRegister(dvc2Reg)
#Instruction Address Compare Registers (IAC1–IAC4)
iacBitMask = {'IACwa': (0, 29)}
iacBank = trap.RegisterBank('IAC', 4, 32, iacBitMask) #it 3 or 4
processor.addRegBank(iacBank)
#Instruction Cache Debug Data Register (ICDBDR)
indbrdReg = trap.Register('ICDBRD', 32)
processor.addRegister(indbrdReg)

# Fixed-point Exception register XER
xerBitMask = {'TBC': (25, 31), 'CA': (2, 2), 'OV': (1, 1), 'SO': (0, 0)}xerReg = trap.Register('XER', 32, xerBitMask)
##xerReg.setDefaultValue(0x0) # need that value 
processor.addRegister(xerReg)

crBitMask = {'CR7': (28, 31),'CR6': (24, 27),'CR5': (20, 23),'CR4': (16, 19),'CR3': (12, 15), 'CR2': (8, 11), 'CR1': (4, 7), 'CRO': (0, 3)}crReg = trap.Register('CR', 32, crBitMask)
##xerReg.setDefaultValue(0x0) # need that value 
processor.addRegister(crReg)

# General-Purpose SPR - 1. Special Purpose Register General (SPRG0–SPRG7) & 2. USPRGO not deglered.
sprgBitMask = {'GD': (0, 31)}
sprgBank = trap.RegisterBank('SPRG', 8, 32, sprgBitMask)
processor.addRegBank(sprgBank)

usprgReg = trap.Register('USPRG', 32)
processor.addRegister(usprgReg)

#Interrupts and Exceptions register DEAR, ESR, EVPR,MCSR,SRR0,SRR1,SRR2,SRR3
#Data Exception Address Register (DEAR)
dearReg = trap.Register('DEAR', 32)
processor.addRegister(dearReg)
#Exception Vector Prefix Register (EVPR)
evprBitMask = {'EVP': (0, 15)}evprReg = trap.Register('EVPR', 32, evprBitMask)
##evprReg.setDefaultValue(0x0) # need that value 
processor.addRegister(evprReg)
#Exception Syndrome Register (ESR)
esrBitMask = {'UoF': (16, 16),'PAP': (13, 13),'PFP': (12, 12),'DIZ': (9, 9),'DST': (8, 8),'PEU': (7, 7), 'PTR': (6, 6), 'PPR': (5, 5), 'PIL': (4, 4), 'MCI': (0, 0)}esrReg = trap.Register('ESR', 32, esrBitMask)
esrReg.setDefaultValue(0x00000000) # value as per page 79
processor.addRegister(esrReg)
#Machine Check Syndrome Register (MCSR)
mcsrBitMask = {'TLBS': (9, 10),'IMCE': (8, 8),'DCFPE': (7, 7), 'DCLPE': (6, 6), 'ICDP': (5, 5), 'TLBE': (4, 4), 'DPLEB': (2, 2),'IPLEB': (1, 1),'MCS': (0, 0)}mcsrReg = trap.Register('MCSR', 32, mcsrBitMask)
mcsrReg.setDefaultValue(0x00000000) #value as per page 79
processor.addRegister(mcsrReg)
#Save/Restore Registers 0 and 1 (SRR0–SRR1)
srr02BitMask = {'SSR': (0, 29)}
srr02Bank = trap.RegisterBank('SRR02', 2, 32, srr02BitMask)
processor.addRegBank(srr02Bank)
srr13BitMask = {'DR': (27, 27),'IR': (26, 26),'FE1': (23, 23),'DE': (22, 22),'DWE': (21, 21),'FE0': (20, 20),'ME': (19, 19),'FP': (18, 18),'PR': (17, 17),'EE': (16, 16),'CE': (14, 14),'WE': (13, 13),'APE': (12, 12),'AP': (6, 6)}
srr13Bank = trap.RegisterBank('SRR13', 2, 32, srr13BitMask)
processor.addRegBank(srr13Bank)

#Processor Version PVR register
pvrReg = trap.Register('PVR', 32)
processor.addRegister(pvrReg)

#Timer Facilities register TBL TBU, PIT, TCR,TSR
#Time Base Lower (TBL)
tblReg = trap.Register('TBL', 32)
processor.addRegister(tblReg)
#Time Base Upper (TBU)
tbuReg = trap.Register('TBU', 32)
processor.addRegister(tbuReg)
#Programmable Interval Timer (PIT)
pitReg = trap.Register('PIT', 32)
processor.addRegister(pitReg)
#Timer Control Register (TCR)
tcrBitMask = {'ARE': (9, 9),'FIE': (8, 8),'FP': (6, 7),'PIE': (5, 5),'WIE': (4, 4),'WRC': (2, 3),'WP': (0, 1)}
tcrReg = trap.Register('TCR', 32, tcrBitMask)
tcrReg.setDefaultValue(00) # value as per page 79
processor.addRegister(tcrReg)
#Timer Status Register (TSR)
tsrBitMask = {'FIS': (5, 5),'PIS': (4, 4),'WRS': (2, 3),'WIS': (1, 1),'ENW': (0, 0)}
tsrReg = trap.Register('TSR', 32, tsrBitMask)
##tsrReg.setDefaultValue(0x0) # need that value 
processor.addRegister(tsrReg)

#Zone Protection register ZPR
zprBitMask = {'Z15': (30, 31),'Z14': (28, 29),'Z13': (26, 27),'Z12': (24, 25),'Z11': (22, 23),'Z10': (20, 21),'Z9': (18, 19),'Z8': (16, 17),'Z7': (14, 15),'Z6': (12, 13),'Z5': (10, 11),'Z4': (8, 9),'Z3': (6, 7),'Z2': (4,5),'Z1': (2, 3),'Z0': (0, 1)}
zprReg = trap.Register('ZPR', 32, zprBitMask)
##zprReg.setDefaultValue(0x0) # need that value 
processor.addRegister(zprReg)


#FP = trap.AliasRegister('FP', 'GPR[30]')
#processor.addAliasReg(FP)#SP = trap.AliasRegister('SP', 'GPR[29]')
#processor.addAliasReg(SP)

pcReg = trap.Register('PC', 32)
pcReg.setDefaultValue('ENTRY_POINT')
processor.addRegister(pcReg)



processor.setMemory('dataMem', 10*1024*1024)

executeStage = trap.PipeStage('execute')
processor.addPipeStage(executeStage)
processor.setFetchRegister('PC', 0)

abi = trap.ABI('GPR[3]', 'GPR[5-10]', 'PC')
abi.setOffset('PC', 0)abi.addMemory('dataMem')
#abi.addVarRegsCorrespondence({'GPR[0-31]': (0,31), 'PC': 32, 'MSR': 33, 'EAR': 34, 'ESR': 35, 'FSR': 36})
#abi.returnCall([('PC', 'GPR[15]', 8)])
processor.setABI(abi)
processor.write(folder = 'PowerProcessor405', models = ['funcLT'])
##processor.write(folder = 'PowerProcessor405', models = ['funcLT'], trace = True)

