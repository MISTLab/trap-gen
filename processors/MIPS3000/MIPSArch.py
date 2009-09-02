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

try:
    import trap
except ImportError:
    import sys, os
    sys.path.append(os.path.abspath(os.path.join('..', '..')))
    try:
        import trap
    except ImportError:
        print ('Please specify in file MIPSArch.py the path where the core TRAP files are located')

import MIPSIsa

# Lets now start building the processor
processor = trap.Processor('MIPS3000', version = '0.1', systemc = False, instructionCache = True, fastFetch = True)
processor.setLittleEndian() #little endian
processor.setWordsize(4, 8) #4 bytes per word, 8 bits per byte
processor.setISA(MIPSIsa.isa) #lets set the instruction set


# GENERAL PURPOSE REGISTERS FOR INTEGER OPERATIONS
GPR = trap.RegisterBank('GPR', 32, 32)
processor.addRegister(GPR)



#
#CP0 REGISTERS
#    
        
#CP0[0] 	Index		-- Reserved in the case of the 4Kp processor
#CP0[1] 	Random		-- Reserved in the case of the 4Kp processor
#CP0[2] 	EntryLo		-- Reserved in the case of the 4Kp processor
#CP0[3] 	EntryLo		-- Reserved in the case of the 4Kp processor
#CP0[4] 	Context		-- Reserved in the case of the 4Kp processor
#CP0[5] 	PageMask	-- Reserved in the case of the 4Kp processor
#CP0[6] 	Wired		-- Reserved in the case of the 4Kp processor          
#CP0[7] 	Reserved            
#CP0[8] 	BadVAddr
BadVAddr = trap.Register('BadVAddr',32)
processor.addRegister(BadVAddr)
#CP0[9] 	Count
Count = trap.Register('COUNT',32)
processor.addRegister(Count)
#CP0[10] 	EntryHi		-- Reserved in the case of the 4Kp processor
#CP0[11] 	Compare
Compare = trap.Register('COMPARE',32)
processor.addRegister(Compare)
#CP0[12] 	Status
StatusBits = {'CU':(28,31), 'RP':(27,27), 'R':(26,26), 'RE':(25,25), 'Z1':(23,24), 'BEV':(22,22), 'TS':(21,21), 'SR':(20,20), 'NMI':(19,19), 'Z2':(18,18), 'RES':(16,17), 'IM':(8,15), 'R':(5,7), 'UM':(4,4), 'R':(3,3), 'ERL':(2,2), 'EXL':(1,1), 'IE':(0,0)}
Status = trap.Register('STATUS',32,StatusBits)
Status.SetDefaultValue(0x000000000101100000000100)
processor.addRegister(Status)
#CP0[13] 	Cause
CauseBits = {'BD':(31,31), 'Z1':(30,30), 'CE':(28,29), 'Z2':(24,27), 'IV':(23,23), 'WP':(22,22), 'Z3':(16,21), 'IPHI':(10,15), 'IPLO':(8,9), 'Z4':(7,7), 'EXCCODE':(2,6), 'Z5':(1,0)}
Cause = trap.Register('CAUSE',32,CauseBits)
Cause.SetDefaultValue(0)
processor.addRegister(Cause)
#CP0[14] 	EPC
epc = trap.Register('EPC',32)
processor.addRegister(epc)
#CP0[15]    	PRId
prIdBits = {'R':(24,31), 'CompanyID':(16,23), 'ProcessorID':(8,15), 'Revision':(0,7)}
prId = trap.Register('PRID',32,StatusBits)
prId.SetDefaultValue(0x00000000111111110101001100000001)
processor.addRegister(prId)
#CP0[16]    	Config
Config0Bits = {'M':(31,31), 'K23':(28,30), 'KU':(25,27), 'ISP':(24,24), 'DSP':(23,23), 'Z1':(22,22), 'SB':(21,21), 'MDU':(20,20), 'R':(19,19), 'MM':(17,18), 'BM':(16,16), 'BE':(15,15), 'AT':(13,14), 'AR':(10,12), 'MT':(7,9), 'Z2':(3,6), 'K0':(0,2)}
Config0 = trap.Register('CONFIG0',32,Config0Bits)
Config0.SetDefaultValue(0x10100100000000000000000000010)
processor.addRegister(Config0)
#CP0[16]    	Config1
Config1Bits = {'M':(31,31), 'MMUSIZE':(25,30), 'IS':(22,24), 'IL':(19,21), 'IA':(16,18), 'DS':(13,15), 'DL':(10,12), 'DA':(7,9), 'Z1':(5,6), 'PC':(4,4), 'WR':(3,3), 'CA':(2,2), 'EP':(1,1), 'FP':(0,0)}
Config1 = trap.Register('CONFIG1',32,Config1Bits)
Config1.SetDefaultValue(0x00001011000000011000001010)
processor.addRegister(Config1)
#CP0[17]    	LLAddr
LLAddrBits = {'Z1':(28,31), 'PADDR':(0,27)}
LLAddr = trap.Register('LLADDR',32,LLAddrBits)
LLAddr.SetDefaultValue(0)
processor.addRegister(LLAddr)
#CP0[18]    	WatchLo
WatchLoBits = {'VADDR':(3,31), 'I':(2,2), 'R':(1,1), 'W':(0,0)}
WatchLo = trap.Register('WATCHLO',32,WatchLoBits)
WatchLo.SetDefaultValue(0)
processor.addRegister(WatchLo)
#CP0[19]    	WatchHi
WatchHiBits = {'z1':(31,31), 'G':(30,30), 'z1':(24,29), 'ASID':(16,23), 'Z2':(12,15), 'MASK':(3,11), 'Z3':(0,2)}
WatchHi = trap.Register('WATCHHI',32,WatchHiBits)
WatchHi.SetDefaultValue(0)
processor.addRegister(WatchHi)
#CP0[20 - 22] 	Reserved  
#CP0[23]    	Debug
DebugBits = {'DBD':(31,31) 'DM':(30,30) 'NoDCR':(29,29) 'LSNM':(28,28) 'Doze':(27,27) 'Halt':(26,26) 'CountDM':(25,25) 'IBusEP':(24,24) 'MCheckP':(23,23) 'CacheEP':(22,22) 'DBusEP':(21,21) 'IEXI':(20,20) 'DDBSImpr':(19,19) 'DDBLImpr':(18,18)  'Ver':(15,17), 'DExcCode':(10,14) 'NoSST':(9,9) 'SSt':(8,8)   'R':(6,7)   'DINT':(5,5) 'DIB':(4,4) 'DDBS':(3,3) 'DDBL':(2,2) 'DBp':(1,1) 'DSS':(0,0)}
Debug = trap.Register('DEBUG',32,DebugBits)
Debug.SetDefaultValue(0X00000010000000010000000000000000)
processor.addRegister(Debug)
#CP0[24]    	DEPC
Depc = trap.Register('DEPC',32)
processor.addRegister(Depc)
#CP0[25]    	Reserved                 
#CP0[26]    	ErrCtl
ErrCtlBits = {'R':(30,31), 'WST':(29,29), 'SPR':(28,28), 'R':(0,27)}
ErrCtl = trap.Register('ERRCTL',32,ErrCtlBits)
ErrCtl.SetDefaultValue(0)
processor.addRegister(ErrCtl)
#CP0[27]    	Reserved  
#CP0[28]    	TagLo
TagLoBits = {'PA':(10,31), 'R1':(8,9), 'VALID':(4,7), 'R2':(3,3), 'L':(2,2), 'LRF':(1,1), 'R3':(0,0)}
TagLo = trap.Register('TAGLO',32,TagLoBits)
TagLo.SetDefaultValue(0)
processor.addRegister(TagLo)
#CP0[28]    	DataLo
DataLo = trap.Register('DATALO',32)
processor.addRegister(DataLo)
#CP0[29]    	Reserved
#CP0[30]    	ErrorEPC
ErrorEPC = trap.Register('ERROREPC',32)
processor.addRegister(ErrorEPC)
#CP0[31]    	DESAVE
DESAVE = trap.Register('DESAVE',32)
processor.addRegister(DESAVE)
#ALIAS REGISTERS FOR CONFIG AND TAGLO & DATALO REGISTERS
Config = trap.AliasRegister('CONFIG', 'Config0', offset = 0)
processor.addAliasReg(Config)
LowOrderCache = trap.AliasRegister('LOWORDERCACHE', 'TagLo', offset = 0)
processor.addAliasReg(LowOrderCache)



#
#EJTAG REGISTERS
#


# Debug Control Register - The PE has the same value as ProbEn of the EJTAG Control Register
dcrBits = {'Res1':(30,31), 'ENM': (29,29), 'Res2':(18,28), 'DB': (17,17), 'IB': (16,16), 'Res1':(5,15), 'INTE': (4,4), 'NMIE': (3,3), 'NMIP': (2,2), 'SRE': (1,1), 'PE': (0,0)}
dcr = trap.Register('DCR',32,dcrBits)
dcr.SetDefaultValue(0x00000000000000000000000000011011)
processor.addRegister(dcr)
# Registers for Instruction Breakpoints
ibsBits = {'RES':(31,31), 'ASIDSUP':(30,30), 'RES1':(28,29), 'BCN':(24,27), 'RES2':(4,23), 'BS':(0,3)}
ibs = trap.Register('IBS',32, ibsBits)
ibs.SetDefaultValue(0x00000100000000000000000000000000)
processor.addRegister(ibs)
iban = trap.Register('IBAN',1,32)
processor.addRegister(iban)
ibmn = trap.Register('IBMN',1,32)
processor.addRegister(ibmn)
ibcnBits = {'RES1':(24,31), 'ASIDUSE':(23,23), 'RES2':(3,22), 'TE':(2,2), 'RES3':(1,1), 'BE':(0,0)}
ibcn = trap.Register('IBCN',32, ibcnBits)
ibcn.SetDefaultValue(0)
processor.addRegister(ibcn)
# Registers for Data Breakpoints Setup
dbsBits ={'RES1':(31,31), 'ASIDSUP':(30,30), 'RES2':(28,29), 'BCN':(24,27), 'RES3':(2,23), 'BS':(0,1)}
dbs = trap.Register('DBS',32, dbsBits)
dbs.SetDefaultValue(0x00000100000000000000000000000000)
processor.addRegister(dbs)
dban = trap.Register('DBAN',1,32)
processor.addRegister(dban)
dbmn = trap.Register('DBMN',1,32)
processor.addRegister(dbmn)
dbcnBits = {'RE':(24,31), 'ASIDUSE':(23,23), 'RES1':(18,22), 'BAI':(14,17), 'NOSB':(13,13), 'NOLB':(12,12), 'RES2':(8,11), 'BLM':(4,7), 'RES3':(3,3), 'TE':(2,2), 'RES4':(1,1), 'BE':(0,0)}
dbcn = trap.Register('DBCN',32, dbcnBits)
dbcn.SetDefaultValue(0)
processor.addRegister(dbcn)
dbvn = trap.Register('DBVN',1,32)
processor.addRegister(dbvn)
#EJTAG TAP Registers pag 163
#EJTAG TAP Instruction Registers
iReg = trap.Register('EJTAGIR',1,5)
#EJTAG TAP Data Registers
bpr = trap.Register('BYPASS',1)
processor.addRegister(bpr)
idrBits = {'VERSION': (28,31), 'PARTNUMBER': (12,27), 'MANUFID': (1,11), 'Res1':(0,0)}
idr = trap.Register('ID',32,idrBits)
idr.setConst(1)
processor.addRegister(idr)
	#EJTAG Version 2.6
impBits = {'EJTAGVersion': (29,31), 'RES1':(25,28), 'DINTsup': (24,24), 'ASIDsize': (21,23), 'RES2':(15,20), 'NoDMA' : (14,14), 'RES3':(0,13)}
imp = trap.Register('IMP',32,impBits)
imp.SetDefaultValue(0x01000001000000000100000000000000)
processor.addRegister(imp)
ecrBits = {'Rocc':(31,31), 'Psz':(29,30), 'Doze':(22,22), 'Halt':(21,21) 'PerRst':(20,20) 'PRnW':(19,19) 'PrAcc':(18,18) 'PrRst':(16,16) 'ProbEn':(15,15) 'ProbTrap':(14,14) 'EjtagBrk':(12,12) 'DM':(3,3)}
ecr = trap.Register('ECR',32,ecrBits)
ecr.SetDefaultValue(0x10000000000000001101000000000000)
processor.addRegister(ecr)
paa = trap.Register('PAA',32)
pad = trap.Register('PAD',32) # p.169       so the value in the PAD register matches data on the internal bus.
processor.addRegister(pad)
fast = trap.Resgister('SprAcc',1)
processor.addRegister(fast)


# HI-LO register for multiplication and division
hi = trap.Register('HI',32)
processor.addRegister(hi)
lo = trap.Register('LO',32)
processor.addRegister(lo)


#Register from which the instructions are fetched
pc = trap.Register('PC',32)
pc.setDefaultValue('ENTRY_POINT')
processor.addRegister(pc)
processor.setFetchRegister('PC', -4)


#Internal Memory for the Processor
processor.setMemory('dataMem', 2048000000)


#Interrupts
irq = trap.Interrupt('IRQ', priority = 0)
processor.addIrq(irq)
processor.setIRQOperation(MIPSIsa.IRQOperation)



# The ABI is necessary to emulate system calls, personalize the GDB stub and,
# eventually, retarget GCC
abi = trap.ABI('GPR[0]', 'GPR[0-3]', 'PC')
abi.addVarRegsCorrespondence({'GPR[0-32]': (0, 32)})
abi.setOffset('PC', -4)
abi.setOffset('GPR[32]', -4)
abi.addMemory('dataMem')
processor.setABI(abi)


#Creating the C++ files implementing the simulator
processor.write(folder = 'processor', models = ['funcLT'])
