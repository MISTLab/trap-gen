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
# creation of the processor
import trap
import cxx_writer
from MIPSCoding import *
from MIPSMethods import *

# ISA declaration: it is the container for all the single instructions
isa = trap.ISA()

# Now I add to the ISA all the helper methods and operations which will be
# called from the instructions
isa.addMethod(SignExtend_method)
isa.addMethod(RaiseException_method)
isa.addMethod(SimpleBranch_method)
isa.addMethod(LikelyBranch_method)

# Now I add some useful definitions to be used inside the instructions; they will be
# inserted as defines in the hpp and file of the instructions
isa.addDefines("""

#define RESET 1
#define SOFT_RESET 2
#define DSS 3			//Debug
#define DINT 4			//Debug
#define NMI 5			//Non Maskable Interruption
#define MACHINE_CHECK 6
#define INT 7			//Interrupt
#define DEFERRED_WATCH 8
#define DIB 9			//Debug
#define WATCH_FETCH 10
#define ADEL_FETCH 11
#define IBE 12			//Instruction Fetch Bus Error
#define DBP 13			//Debug
#define SYS 14
#define BP 15
#define CPU 16
#define RI 17
#define OV 18			//Overflow
#define TR 19
#define DDBLad 20		//Degub
#define DDBS 21			//Debug
#define WATCH_DATA 22
#define ADEL 23
#define ADES 24
#define DBE 25
#define DDBL 26			//Debug



#define SIGNAL_DEBUG_BREAKPOINT
#define SIGNAL_DEBUG_MODE_BREAKPOINT
""")

#-------------------------------------------------------------------------------------
# Let's now procede to set the behavior of the instructions
#-------------------------------------------------------------------------------------
#
# Note the special operations:
#
# -- annull(): transforms the current instruction in a NOP; if we are
# in the middle of the execution of some code, it also terminates the
# execution of that part of code (it is like an exception)
# -- flush(): flushes the pipeline stages preceding the one in which
# the flush method has been called
# -- stall(n): stalls the current stage and the preceding ones for n clock
# cycles. If we issue this operation in the middle of the execution of an
# instruction, anyway the execution of that code finished before the stall
# operation has any effect; if that code contains another call to stall(m),
# the pipeline stages are stalled for a total of n+m
# -- THROW_EXCEPTION: a macro for throwing C++ exceptions
#

#____________________________________________________________________________________________________
#----------------------------------------------------------------------------------------------------
# Now using all the defined operations, instruction codings, etc
# I can actually declare the processor instructions
#----------------------------------------------------------------------------------------------------
#____________________________________________________________________________________________________

#
# ADD instruction family
#

opCode = cxx_writer.writer_code.Code("""
long long opr1 = (rs & 0x80000000);
opr1 = opr1<<1 |rs;
long long opr2 = (rt & 0x80000000);
opr2 = opr2<<1 |rt;
long long temp32 = opr1+opr2;
long long temp31 = rs + rt;
if (((temp32 & 0x100000000)>>32) != ((temp31 & 0x80000000)>>31)){
	RaiseException(OV);
}else{
	rd = temp31;
}
""")
add_reg_Instr = trap.Instruction('ADD', True)
add_reg_Instr.setMachineCode(register_format,{'opcode': [0,0,0,0,0,0], 'function':[1,0,0,0,0,0]},('add r','%rd', ',',' r','%rs', ',',' r','%rt'))
add_reg_Instr.setCode(opCode, 'execution')
add_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(add_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
long long opr1 = (rs & 0x80000000);
opr1 = opr1<<1 |rs;
long long opr2 = (SignExtend(immediate,16) & 0x80000000);
opr2 = opr2<<1 |SignExtend(immediate,16);
long long temp32 = opr1+opr2;
long long temp31 = rs + SignExtend(immediate,16);

if (((temp32 & 0x100000000)>>32) != ((temp31 & 0x80000000)>>31)){
	RaiseException(OV);
}else{
	rt = temp31;
}
""")
addi_imm_Instr = trap.Instruction('ADDI', True)
addi_imm_Instr.setMachineCode(immediate_format,{'opcode': [0,0,1,0,0,0]},('addi r','%rt', ',',' r','%rs', ',',' r','%immediate'))
addi_imm_Instr.setCode(opCode, 'execution')
addi_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(addi_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
rt = rs + SignExtend(immediate,16);
""")
addiu_imm_Instr = trap.Instruction('ADDIU', True)
addiu_imm_Instr.setMachineCode(immediate_format,{'opcode': [0,0,1,0,0,1]},('addiu r','%rt', ',',' r','%rs', ',',' r','%immediate'))
addiu_imm_Instr.setCode(opCode, 'execution')
addiu_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(addiu_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
rd = rs + rt;
""")
addu_reg_Instr = trap.Instruction('ADDU', True)
addu_reg_Instr.setMachineCode(register_format,{'opcode': [0,0,0,0,0,0],'function':[1,0,0,0,0,1]},('addu r','%rd', ',',' r','%rs', ',',' r','%rt'))
addu_reg_Instr.setCode(opCode, 'execution')
addu_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(addu_reg_Instr)



#
#AND instruction family
#

opCode = cxx_writer.writer_code.Code("""
rd = rs & rt;
""")
and_reg_Instr = trap.Instruction('AND', True)
and_reg_Instr.setMachineCode(register_format,{'opcode': [0,0,0,0,0,0],'function':[1,0,0,1,0,0]},('and r','%rd', ',',' r','%rs', ',',' r','%rt'))
and_reg_Instr.setCode(opCode, 'execution')
and_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(and_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
rt = rs & (0x0000 | immediate);
""")
andi_imm_Instr = trap.Instruction('ANDI', True)
andi_imm_Instr.setMachineCode(immediate_format,{'opcode': [0,0,1,1,0,0]},('andi r','%rt', ',',' r','%rs', ',',' r','%immediate'))
andi_imm_Instr.setCode(opCode, 'execution')
andi_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(andi_imm_Instr)


#
#BRANCH instruction family
#See what happens with the instructions B and BAL

opCode = cxx_writer.writer_code.Code("""
bool br = ( (rs == rt && op4 == 0) || (rs != rt && op4 == 0x1) );
	if (op2 == 0){
		PC = SimpleBranch(br,(int)SignExtend(immediate<<2,18));
	}else{
		PC = LikelyBranch(br,(int)SignExtend(immediate<<2,18));
	}
""")	#Specify correctly the jump instruction
b2r_imm_Instr = trap.Instruction('BRANCH2REGISTERS', True)
b2r_imm_Instr.setMachineCode(b_format1,{'op3': [0,1,0]}, 
('b', ('%op4', {int('1',2):'ne', int('0',2):'eq'}), ('%op2', {int('1',2):'l'}),
 ' r', '%rs', ',', ' r', '%rt', ',', ' r', '%immediate'))
b2r_imm_Instr.setCode(opCode, 'execution')
b2r_imm_Instr.addBehavior(NoIncrementPC,'execution')	#Check if more behaviors need to be added
isa.addInstruction(b2r_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
bool br = ( ((int)rs<=0 && op4 == 0) || ((int)rs>0 && op4 == 0x1) );
	if (op2 == 0){
		PC = SimpleBranch(br,(int)SignExtend(immediate<<2,18));
	}else{
		PC = LikelyBranch(br,(int)SignExtend(immediate<<2,18));
	}
""")
bz_imm_Instr = trap.Instruction('BRANCHZ', True)
bz_imm_Instr.setMachineCode(b_format1,{'op3': [0,1,1]},
('b', ('%op4', {int('1',2):'gtz', int('0',2):'lez'}), ('%op2', {int('1',2):'l'}),
 ' r', '%rs', ',', ' r', '%immediate'))
bz_imm_Instr.setCode(opCode, 'execution')
bz_imm_Instr.addBehavior(NoIncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(bz_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
bool br = ( ((int)rs<0 && (rt3 == 0x0 || rt3 == 0x2)) || ((int)rs>=0 && (rt3 == 0x1 || rt3== 0x3)) );
	if (rt == 0x1){
		GPR[31] = PC+8;
	}
	if (rt3 == 0x0 || rt3 == 0x1){
		PC = SimpleBranch(br,(int)SignExtend(immediate<<2,18));
	}else{
		PC = LikelyBranch(br,(int)SignExtend(immediate<<2,18));
	}
""")
breg_imm_Instr = trap.Instruction('BRANCHREGIMM', True)
breg_imm_Instr.setMachineCode(b_format2,{},
('b', ('%rt3', {int('00',2):'ltz', int('01',2):'gez', int('10',2):'ltz', int('11',2):'gez'}),
 ('%rt', {int('1',2):'al'}),
 ('%rt3', {int('10', 2):'l', int('11', 2):'l'}),
 ' r', '%rs', ',', ' r', '%immediate'))
breg_imm_Instr.setCode(opCode, 'execution')
breg_imm_Instr.addBehavior(NoIncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(breg_imm_Instr)



#
#BREAK
#

opCode = cxx_writer.writer_code.Code("""
	RaiseException(BP);
""")
break_reg_Instr = trap.Instruction('BREAK', True)
break_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 0, 1, 1, 0, 1]},
('break'))
break_reg_Instr.setCode(opCode, 'execution')
break_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(break_reg_Instr)



#
#CACHE
#



#
#COP0
#

opCode = cxx_writer.writer_code.Code("""

sel = 0; //Check how sel value is determined (0 or 1)
if (rd == 16){
	if (sel == 1){
		CONFIG1 = rt;
	}
	else {
		CONFIG0= rt;
	}
}else if (rd == 28){
	if (sel == 1){
		TAGLO = rt;
	}
	else {
		DATALO = rt;
	}
} else if (rd == 0 || rd == 1 || rd == 2 || rd == 3 || rd == 4 || rd == 5 || rd == 6 || rd == 7 || rd == 10 || rd == 20 || rd == 21 || rd == 22 || rd == 25 || rd == 27 || rd == 29 ){
	RaiseException(RI);
}

else {
	switch (rd){
		case 8:{
			BadVAddr = rt;
		break;}
		case 9:{
			COUNT = rt;
		break;}
		case 11:{
			COMPARE = rt;
		break;}
		case 12:{
			STATUS = rt;
		break;}
		case 13:{
			CAUSE = rt;
		break;}
		case 14:{
			EPC = rt;
		break;}
		case 15:{
			PRID = rt;
		break;}
		case 17:{
			LLADDR = rt;
		break;}
		case 18:{
			WATCHLO = rt;
		break;}
		case 19:{
			WATCHHI = rt;
		break;}
		case 23:{
			DEBUG = rt;
		break;}
		case 24:{
			DEPC = rt;
		break;}
		case 26:{
			ERRCTL = rt;
		break;}
		case 30:{
			ERROREPC = rt;
		break;}
		case 31:{
			DESAVE = rt;
		break;}
		default:{
		break;}
	}
}

""")
mtc0_Instr = trap.Instruction ('MTC0',True)
mtc0_Instr.setMachineCode(cop_format,{'opcode':[0,1,0,0,0,0],'rs1':[0,0],'rs2':[1,0,0]},('mtc0',' r','%rt', ',',' r','%rd'))
mtc0_Instr.setCode(opCode, 'execution')
mtc0_Instr.addBehavior(IncrementPC, 'execution') 
isa.addInstruction(mtc0_Instr)



#
#CLO
#

opCode = cxx_writer.writer_code.Code("""
rd = 0;
unsigned int temp = rs;
for (int i = 0; i < 32; i++) {
	rd += temp % 2;
	temp = temp>>1;
}
""")
clo_reg_Instr = trap.Instruction('CLO', True)
clo_reg_Instr.setMachineCode(register_format,{'opcode': [0,1,1,1,0,0],'function':[1,0,0,0,0,1]},('clo r','%rd',' r','%rs'))
clo_reg_Instr.setCode(opCode, 'execution')
clo_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(clo_reg_Instr)



#
#CLZ
#

opCode = cxx_writer.writer_code.Code("""
rd = 0;
unsigned int temp = rs;
for (int i = 0; i < 32; i++) {
	rd += temp % 2;
	temp = temp>>1;
}
rd = 32-rd;
""")
clz_reg_Instr = trap.Instruction('CLZ', True)
clz_reg_Instr.setMachineCode(register_format,{'opcode': [0,1,1,1,0,0],'function':[1,0,0,0,0,0]},('clz r','%rd', ',',' r','%rs'))
clz_reg_Instr.setCode(opCode, 'execution')
clz_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(clz_reg_Instr)



#
#DERET
#



#
#DIV instruction family
#

opCode = cxx_writer.writer_code.Code("""
if (rt == 0){
	LO =0;
	HI =rs;
}else{
	LO = (int)rs / (int)rt;
	HI = (int)rs % (int)rt;
}
""")
div_reg_Instr = trap.Instruction('DIV', True)
div_reg_Instr.setMachineCode(register_format,{'opcode': [0,0,0,0,0,0],'function':[0,1,1,0,1,0]},('div r','%rs', ',',' r','%rt'))
div_reg_Instr.setCode(opCode, 'execution')
div_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(div_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
if (rt == 0){
	LO =0;
	HI =rs;
}else{
	LO = (unsigned int)rs / (unsigned int)rt;
	HI = (unsigned int)rs % (unsigned int)rt;
}
""")
divu_reg_Instr = trap.Instruction('DIVU', True)
divu_reg_Instr.setMachineCode(register_format,{'opcode': [0,0,0,0,0,0],'function':[0,1,1,0,1,1]},('divu r','%rs', ',',' r','%rt'))
divu_reg_Instr.setCode(opCode, 'execution')
divu_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(divu_reg_Instr)



#
#ERET
#



#
#JUMP Instruction Family
#

#Revisar estas funciones de la familia jump -- hay que configurar los aliases, entonces la forma de acceder al registro AC puede ser que cambie

opCode = cxx_writer.writer_code.Code("""
if (op2 == 1){
	GPR[31] = PC+8;
}
PC = (PC&0xF0000000) + (target<<2);
""")
j_jump_Instr = trap.Instruction('JUMP', True)
j_jump_Instr.setMachineCode(jump_format,{},('j', ('%op2',{int('1',2):'al'}), ' r', '%target'))
j_jump_Instr.setCode(opCode, 'execution')
j_jump_Instr.addBehavior(NoIncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(j_jump_Instr)


opCode = cxx_writer.writer_code.Code("""
if (CONFIG1[key_CA] == 0){
	PC = rs;
} else {
	PC = rs<<1;
}
""")
jr_jump_Instr = trap.Instruction('JUMPR', True)
jr_jump_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function': [0, 0, 1, 0, 0, 0]},('jr', ' r', '%rs'))
jr_jump_Instr.setCode(opCode, 'execution')
jr_jump_Instr.addBehavior(NoIncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(jr_jump_Instr)


opCode = cxx_writer.writer_code.Code("""
rd = PC+8;
if (CONFIG1[key_CA] == 0){
	PC = rs;
} else {
	PC = rs<<1;
}
""")
jlr_jump_Instr = trap.Instruction('JUMPLR', True)
jlr_jump_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function': [0, 0, 1, 0, 0, 1]},('jalr', ' r', '%rs', ',', ' r', '%rd'))
jlr_jump_Instr.setCode(opCode, 'execution')
jlr_jump_Instr.addBehavior(NoIncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(jlr_jump_Instr)


#
#LOAD Instruction Family
#

opCode = cxx_writer.writer_code.Code("""
long result;
long address = SignExtend(immediate,16)+rs;
if (address >= 2048000000 || address < 0)
	RaiseException(ADEL_FETCH);
if ( ((address%2) != 0 ) && op3 == 0x01)
	RaiseException(ADEL);
if ( ((address%4) != 0 ) && op3 == 0x03)
	RaiseException(ADEL);
if (op3 == 0){
	result = dataMem.read_byte(address);
	result = SignExtend(result,8);
}
if (op3 == 0b01){
	result = dataMem.read_half(address);
	result = SignExtend(result,16);
}
if (op3 == 0b11){
	result = dataMem.read_word(address);
}
if (op3 == 0b10){
	short bytes = address & 0x00000003;
	address = address & 0xFFFFFFFC;
	long aux1;
	long aux2 = rt;
		aux1 = dataMem.read_word(address)<<(bytes*8);
		switch(bytes){
			case 0x0:{
				aux2 = aux2 & 0x00000000;
			break;}
			case 0x1:{
				aux2 = aux2 & 0x00000FF;
			break;}
			case 0x2:{
				aux2 = aux2 & 0x0000FFFF;
			break;}
			case 0x3:{
				aux2 = aux2 & 0x00FFFFFF;
			break;}
			default:{
			break;}
		}
	result = aux1 | aux2;
}
rt = result;
""")
load_imm_Instr = trap.Instruction('LOAD', True)
load_imm_Instr.setMachineCode(s_format,{'op': [1, 0, 0], 'op2': [0]},
('l', ('%op3', {int('00',2):'b', int('01',2):'h', int('10',2):'wl', int('11',2):'w'}),
 ' r', '%rt', ',', ' r', '%immediate', '(', 'r', '%rs', ')'))
load_imm_Instr.setCode(opCode, 'execution')
load_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Throw exceptions (for LH also bus error.)
isa.addInstruction(load_imm_Instr)


opCode = cxx_writer.writer_code.Code("""	//ASK HOW DOES DATAMEM READS, ACCORDING TO ENDIANESS
long result;
long address = SignExtend(immediate,16)+rs;
if (address >= 2048000000 || address < 0)
	RaiseException(ADEL_FETCH);
if ( ((address%2) != 0 ) && op3 == 0x01)
	RaiseException(ADEL);
if (op3 == 0)
	result = dataMem.read_byte(address);
if (op3 == 0b01)
	result = dataMem.read_half(address);
if (op3 == 0b11)
	result = dataMem.read_word(address);
if (op3 == 0b10){
	short bytes = address & 0x0003;
	address = address & 0xFFFFFFFC;
	long aux1;
	long aux2 = rt;
		aux1 = dataMem.read_word(address)>>((3-bytes)*8);
		switch(bytes){
			case 0x0:{
				aux2 = aux2 & 0xFFFFFF00;
			break;}
			case 0x1:{
				aux2 = aux2 & 0xFFFF0000;
			break;}
			case 0x2:{
				aux2 = aux2 & 0xFF000000;
			break;}
			case 0x3:{
				aux2 = aux2 & 0x00000000;
			break;}
			default:{
			break;}
		}
	result = aux1 | aux2;
}
rt = result;
""")
load2_imm_Instr = trap.Instruction('LOAD_U_R', True)
load2_imm_Instr.setMachineCode(s_format,{'op': [1, 0, 0], 'op2': [1]},
('l', ('%op3', {int('00',2):'bu', int('01',2):'hu', int('10',2):'wr'}),
 ' r', '%rt', ',', ' r', '%immediate', '(', 'r', '%rs', ')'))
load2_imm_Instr.setCode(opCode, 'execution')
load2_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Throw exceptions (Address error.)
isa.addInstruction(load2_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
long address = SignExtend(immediate,16)+rs;
if (address >= 2048000000 || address < 0)
	RaiseException(ADEL_FETCH);
if ((address%4) != 0)
	RaiseException(ADEL);
rt = dataMem.read_word(address);
LLbit = 0b1;
""")
loadl_imm_Instr = trap.Instruction('LL', True)
loadl_imm_Instr.setMachineCode(immediate_format,{'opcode': [1, 1, 0, 0, 0, 0]},
('ll', ' r', '%rt', ',', ' r', '%immediate', '(', 'r', '%rs', ')'))
loadl_imm_Instr.setCode(opCode, 'execution')
loadl_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Throw exceptions (Address error, Reserved Instruction.)
isa.addInstruction(loadl_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
rt = immediate << 16;
""")
lui_imm_Instr = trap.Instruction('LUI', True)
lui_imm_Instr.setMachineCode(immediate_format,{'opcode': [0, 0, 1, 1, 1, 1]},
('lui', ' r', '%rt', ',', ' r', '%immediate'))
lui_imm_Instr.setCode(opCode, 'execution')
lui_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Throw exceptions (Address error, Reserved Instruction.)
isa.addInstruction(lui_imm_Instr)



#
#MULTIPLY Instruction Family
#

opCodeCommon1 = cxx_writer.writer_code.Code("""
long long op1 = rs;
long long op2 = rt;
if((rs & (1 << 31)) != 0)
    op1 = ((unsigned long long)0xFFFFFFFF00000000) | rs;
if((rt & (1 << 31)) != 0)
    op2 = ((unsigned long long)0xFFFFFFFF00000000) | rt;
result = (long long)(op1*op2);
""")
opCodeCommon2 = cxx_writer.writer_code.Code("""
long long op1 = rs;
long long op2 = rt;
result = (unsigned long long)(op1*op2);
""")
opCode = cxx_writer.writer_code.Code("""
long long hiAux = HI;
long long operand = ((hiAux<<32))|(LO);
long long temp = operand + result;
LO = temp & 0x0FFFFFFFF;
HI = temp>>32;
""")
madd_reg_Instr = trap.Instruction('MADD', True)
madd_reg_Instr.setMachineCode(register_format,{'opcode': [0, 1, 1, 1, 0, 0], 'function':[0, 0, 0, 0, 0, 0]},
('madd', ' r', '%rs', ',', ' r', ' %rt'))
madd_reg_Instr.setCode(opCodeCommon1, 'execution1')
madd_reg_Instr.setCode(opCode, 'execution')
madd_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
madd_reg_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(madd_reg_Instr)


maddu_reg_Instr = trap.Instruction('MADDU', True)
maddu_reg_Instr.setMachineCode(register_format,{'opcode': [0, 1, 1, 1, 0, 0], 'function':[0, 0, 0, 0, 0, 1]},
('maddu', ' r', '%rs', ',', ' r', ' %rt'))
maddu_reg_Instr.setCode(opCodeCommon2, 'execution1')
maddu_reg_Instr.setCode(opCode, 'execution')
maddu_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
maddu_reg_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(maddu_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
long long hiAux = HI;
long long operand = (((long long)(hiAux))<<32)|(LO);
long long temp = operand - result;
LO = temp & 0x0FFFFFFFF;
HI = temp>>32;
""")
msub_reg_Instr = trap.Instruction('MSUB', True)
msub_reg_Instr.setMachineCode(register_format,{'opcode': [0, 1, 1, 1, 0, 0], 'function':[0, 0, 0, 1, 0, 0]},
('msub', ' r', '%rs', ',', ' r', ' %rt'))
msub_reg_Instr.setCode(opCodeCommon1, 'execution1')
msub_reg_Instr.setCode(opCode, 'execution')
msub_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
msub_reg_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(msub_reg_Instr)


msubu_reg_Instr = trap.Instruction('MSUBU', True)
msubu_reg_Instr.setMachineCode(register_format,{'opcode': [0, 1, 1, 1, 0, 0], 'function':[0, 0, 0, 1, 0, 1]},
('msubu', ' r', '%rs', ',', ' r', ' %rt'))
msubu_reg_Instr.setCode(opCodeCommon2, 'execution1')
msubu_reg_Instr.setCode(opCode, 'execution')
msubu_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
msubu_reg_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(msubu_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
rd = result;
""")
mul_reg_Instr = trap.Instruction('MUL', True)
mul_reg_Instr.setMachineCode(register_format,{'opcode': [0, 1, 1, 1, 0, 0], 'function':[0, 0, 0, 0, 1, 0]},
('mul', ' r', '%rd', ',', ' r', '%rs', ',', ' r', ' %rt'))
mul_reg_Instr.setCode(opCodeCommon1, 'execution1')
mul_reg_Instr.setCode(opCode, 'execution')
mul_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
mul_reg_Instr.addVariable(('result', 'BIT<64>'))
opCode = cxx_writer.writer_code.Code("""
LO = result;
HI = result>>32;
""")
mult_reg_Instr = trap.Instruction('MULT', True)
mult_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 1, 1, 0, 0, 0]},
('mult', ' r', '%rs', ',', ' r', ' %rt'))
mult_reg_Instr.setCode(opCodeCommon1, 'execution1')
mult_reg_Instr.setCode(opCode, 'execution')
mult_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
mult_reg_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(mult_reg_Instr)
isa.addInstruction(mul_reg_Instr)



multu_reg_Instr = trap.Instruction('MULTU', True)
multu_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 1, 1, 0, 0, 1]},
('multu', ' r', '%rs', ',', ' r', ' %rt'))
multu_reg_Instr.setCode(opCodeCommon2, 'execution1')
multu_reg_Instr.setCode(opCode, 'execution')
multu_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
multu_reg_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(multu_reg_Instr)



#
#MOVE Instruction Family
#

opCode = cxx_writer.writer_code.Code("""
rd = HI;
""")
mfhi_reg_Instr = trap.Instruction('MFHI', True)
mfhi_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 1, 0, 0, 0, 0]},
('mfhi', ' r', '%rd'))
mfhi_reg_Instr.setCode(opCode, 'execution')
mfhi_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(mfhi_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
rd = LO;
""")
mflo_reg_Instr = trap.Instruction('MFLO', True)
mflo_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 1, 0, 0, 1, 0]},
('mflo', ' r', '%rd'))
mflo_reg_Instr.setCode(opCode, 'execution')
mflo_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(mflo_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
HI = rs;
""")
mthi_reg_Instr = trap.Instruction('MTHI', True)
mthi_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 1, 0, 0, 0, 1]},
('mthi', ' r', '%rs'))
mthi_reg_Instr.setCode(opCode, 'execution')
mthi_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Restriction: A computed result written to the HI/LO pair by DIV, DIVU, MULT, or MULTU must be 	read by MFHI or MFLO before a new result can be written into either HI or LO.

isa.addInstruction(mthi_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
LO = rs;
""")
mtlo_reg_Instr = trap.Instruction('MTLO', True)
mtlo_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 1, 0, 0, 1, 1]},
('mflo', ' r', '%rs'))
mtlo_reg_Instr.setCode(opCode, 'execution')
mtlo_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Restriction: A computed result written to the HI/LO pair by DIV, DIVU, MULT, or MULTU must be 	read by MFHI or MFLO
isa.addInstruction(mtlo_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
if (rt != 0)
	rd = rs;
""")
movn_reg_Instr = trap.Instruction('MOVN', True)
movn_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 0, 1, 0, 1, 1]},
('movn', ' r', '%rd', ',', ' r', '%rs', ',', ' r', '%rt'))
movn_reg_Instr.setCode(opCode, 'execution')
movn_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Programming Notes: The non-zero value tested here is the condition true result from the SLT, SLTI, SLTU, and SLTIU comparison instructions.

isa.addInstruction(movn_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
if (rt == 0)
	rd = rs;
""")
movz_reg_Instr = trap.Instruction('MOVZ', True)
movz_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 0, 1, 0, 1, 0]},
('movz', ' r', '%rd', ',', ' r', '%rs', ',', ' r', '%rt'))
movz_reg_Instr.setCode(opCode, 'execution')
movz_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Programming Notes: The non-zero value tested here is the condition true result from the SLT, SLTI, SLTU, and SLTIU comparison instructions.

isa.addInstruction(movz_reg_Instr)


# Pending move from coprocessor and move to corpocessor




#
#OR Instruction Family
#

opCode = cxx_writer.writer_code.Code("""
	rd = ~(rs | rt);
""")
nor_reg_Instr = trap.Instruction('NOR', True)
nor_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[1, 0, 0, 1, 1, 1]},
('nor', ' r', '%rd', ',', ' r', '%rs', ',', ' r', '%rt'))
nor_reg_Instr.setCode(opCode, 'execution')
nor_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(nor_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
	rd = rs | rt;
""")
or_reg_Instr = trap.Instruction('OR', True)
or_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[1, 0, 0, 1, 0, 1]},
('or', ' r', '%rd', ',', ' r', '%rs', ',', ' r', '%rt'))
or_reg_Instr.setCode(opCode, 'execution')
or_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(or_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
	rt = immediate | rs;
""")
or_imm_Instr = trap.Instruction('ORI', True)
or_imm_Instr.setMachineCode(immediate_format,{'opcode': [0, 0, 1, 1, 0, 1]},
('ori', ' r', '%rt', ',', ' r', '%rs', ',', ' r', '%immediate'))
or_imm_Instr.setCode(opCode, 'execution')
or_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(or_imm_Instr)



#
#PREFETCH
#




#
#STORE Instruction Family
#

opCode = cxx_writer.writer_code.Code("""
long address = SignExtend(immediate,16) + rs;
if (address >= 2048000000 || address < 0)
	RaiseException(ADES);
dataMem.write_byte(address, rt);
""")
sb_imm_Instr = trap.Instruction('SB', True)
sb_imm_Instr.setMachineCode(immediate_format,{'opcode': [1, 0, 1, 0, 0, 0]},
('sb', ' r', '%rt', ',', ' r', '%immediate', '(', 'r', '%rs', ')'))
sb_imm_Instr.setCode(opCode, 'execution')
sb_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Throw exceptions (Bus error, Address error.)
isa.addInstruction(sb_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
long address = SignExtend(immediate,16) + rs;
if (address >= 2048000000 || address < 0)
	RaiseException(ADES);
if ( (address%4) != 0 )
	RaiseException(ADES);
if (LLbit)
	dataMem.write_word(address, rt);
rt = 0x0 | LLbit;
LLbit= 0;
""")
sc_imm_Instr = trap.Instruction('SC', True)
sc_imm_Instr.setMachineCode(immediate_format,{'opcode': [1, 1, 1, 0, 0, 0]},
('sc', ' r', '%rt', ',', ' r', '%immediate', '(', 'r', '%rs', ')'))
sc_imm_Instr.setCode(opCode, 'execution')
sc_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Throw exceptions (Reserved Instruction.)
							#Check restrictions on page 283
isa.addInstruction(sc_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
long address = SignExtend(immediate,16) + rs;
if (address >= 2048000000 || address < 0)
	RaiseException(ADES);
if ( (address%2) != 0 )
	RaiseException(ADES);
dataMem.write_half(address, rt);
""")
sh_imm_Instr = trap.Instruction('SH', True)
sh_imm_Instr.setMachineCode(immediate_format,{'opcode': [1, 0, 1, 0, 0, 1]},
('sh', ' r', '%rt', ',', ' r', '%immediate', '(', 'r', '%rs', ')'))
sh_imm_Instr.setCode(opCode, 'execution')
sh_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(sh_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
long address = SignExtend(immediate,16) + rs;
if (address >= 2048000000 || address < 0)
	RaiseException(ADES);
if ( (address%4) != 0 )
	RaiseException(ADES);
dataMem.write_word(address, rt);
""")
sw_imm_Instr = trap.Instruction('SW', True)
sw_imm_Instr.setMachineCode(immediate_format,{'opcode': [1, 0, 1, 0, 1, 1]},
('sw', ' r', '%rt', ',', ' r', '%immediate', '(', 'r', '%rs', ')'))
sw_imm_Instr.setCode(opCode, 'execution')
sw_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(sw_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
long address = SignExtend(immediate,16) + rs;
if (address >= 2048000000 || address < 0)
	RaiseException(ADES);
short bytes = address & 0x3;
address = address & 0xFFFFFFFC;
long aux1 = dataMem.read_word(address);
long result;
	rt = rt>>(bytes*8);
	switch(bytes){
		case 0x0:{
			aux1 = 0x0;
		break;}
		case 0x1:{
			aux1 = aux1 & 0xFF000000;
		break;}
		case 0x2:{
			aux1 = aux1 & 0xFFFF0000;
		break;}
		case 0x3:{
			aux1 = aux1 & 0xFFFFFF00;
		break;}
		default:{
		break;}
	}

	result = rt | aux1;	
dataMem.write_word(address, result);
""")
swl_imm_Instr = trap.Instruction('SWL', True)
swl_imm_Instr.setMachineCode(immediate_format,{'opcode': [1, 0, 1, 0, 1, 0]},
('swl', ' r', '%rt', ',', ' r', '%immediate', '(', 'r', '%rs', ')'))
swl_imm_Instr.setCode(opCode, 'execution')
swl_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Throw exceptions (Bus Error, Address Error.)
isa.addInstruction(swl_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
long address = SignExtend(immediate,16) + rs;
if (address >= 2048000000 || address < 0)
	RaiseException(ADES);
short bytes = address & 0x0003;
address = address & 0xFFFC;
long aux1 = dataMem.read_word(address);
long result;
	rt = rt<<((3-bytes)*8);

	switch(bytes){
		case 0x0:{
			aux1 = aux1 & 0x00FFFFFF;
		break;}
		case 0x1:{
			aux1 = aux1 & 0x0000FFFF;
		break;}
		case 0x2:{
			aux1 = aux1 & 0x000000FF;
		break;}
		case 0x3:{
			aux1 = 0x00000000;
		break;}
		default:{
		break;}
	}

	result = rt | aux1;
	
dataMem.write_word(address, result);
""")
swr_imm_Instr = trap.Instruction('SWR', True)
swr_imm_Instr.setMachineCode(immediate_format,{'opcode': [1, 0, 1, 1, 1, 0]},
('swr', ' r', '%rt', ',', ' r', '%immediate', '(', 'r', '%rs', ')'))
swr_imm_Instr.setCode(opCode, 'execution')
swr_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Throw exceptions (Bus Error, Address Error.)
isa.addInstruction(swr_imm_Instr)



#
#Software Debug Breakpoint
#



#Implement this again

opCode = cxx_writer.writer_code.Code("""
//if ( DM == 0 ) {
	//RaiseException(SIGNAL_DEBUG_BREAKPOINT);
//} else {
	//RaiseException(SIGNAL_DEBUG_MODE_BREAKPOINT);
//}
""")
sdbbp_reg_Instr = trap.Instruction('SDBBP', True)
sdbbp_reg_Instr.setMachineCode(code_format,{'opcode': [0, 1, 1, 1, 0, 0], 'function':[1, 1, 1, 1, 1, 1]},
('sdbbp', ' r', '%code'))
sdbbp_reg_Instr.setCode(opCode, 'execution')
sdbbp_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(sdbbp_reg_Instr)



#
#SHIFT Instruction Family
#

opCode = cxx_writer.writer_code.Code("""
	rd = rt << sa;
""")
sll_reg_Instr = trap.Instruction('SLL', True)
sll_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 0, 0, 0, 0, 0]},
('sll', ' r', '%rd', ',', ' r', '%rt', ',', ' r', '%sa'))
sll_reg_Instr.setCode(opCode, 'execution')
sll_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(sll_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
short shift = rs & 0x001F;
	rd = rt << shift;
""")
sllv_reg_Instr = trap.Instruction('SLLV', True)
sllv_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 0, 0, 1, 0, 0]},
('sllv', ' r', '%rd', ',', ' r', '%rt', ',', ' r', '%rs'))
sllv_reg_Instr.setCode(opCode, 'execution')
sllv_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(sllv_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
long temp = 0x0;
long sign = (0x80000000 & rt);
for (int x=0; x<sa; x++ ){
	temp = temp | sign;
	sign = sign>>1;
}
	rd = (rt >> sa) | temp;
""")
sra_reg_Instr = trap.Instruction('SRA', True)
sra_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 0, 0, 0, 1, 1]},
('sra', ' r', '%rd', ',', ' r', '%rt', ',', ' r', '%sa'))
sra_reg_Instr.setCode(opCode, 'execution')
sra_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(sra_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
short shift = rs & 0x001F;
long temp = 0x0000;
long sign = (0x80000000 & rt);
for (int x=0; x<shift; x++ ){
	temp = temp | sign;
	sign = sign>>1;
}
	rd = (rt >> shift) | temp;
""")
srav_reg_Instr = trap.Instruction('SRAV', True)
srav_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 0, 0, 1, 1, 1]},
('srav', ' r', '%rd', ',', ' r', '%rt', ',', ' r', '%rs'))
srav_reg_Instr.setCode(opCode, 'execution')
srav_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(srav_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
	rd = rt >> sa;
""")
srl_reg_Instr = trap.Instruction('SRL', True)
srl_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 0, 0, 0, 1, 0]},
('srl', ' r', '%rd', ',', ' r', '%rt', ',', ' r', '%sa'))
srl_reg_Instr.setCode(opCode, 'execution')
srl_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(srl_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
short shift = rs & 0x001F;
	rd = rt >> shift;
""")
srlv_reg_Instr = trap.Instruction('SRLV', True)
srlv_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 0, 0, 1, 1, 0]},
('srlv', ' r', '%rd', ',', ' r', '%rt', ',', ' r', '%rs'))
srlv_reg_Instr.setCode(opCode, 'execution')
srlv_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(srlv_reg_Instr)




#
#SET Instruction Family
#

opCode = cxx_writer.writer_code.Code("""
if ((int)rs < (int)rt ){
	rd = 0x0001;
}else{
	rd = 0x0000;
}
""")
slt_reg_Instr = trap.Instruction('SLT', True)
slt_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[1, 0, 1, 0, 1, 0]},
('slt', ' r', '%rd', ',', ' r', '%rs', ',', ' r', '%rt'))
slt_reg_Instr.setCode(opCode, 'execution')
slt_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(slt_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
if ((int)rs < (int)(SignExtend(immediate,16)) ){
	rt = 0x0001;
}else{
	rt = 0x0000;
}
""")
slti_imm_Instr = trap.Instruction('SLTI', True)
slti_imm_Instr.setMachineCode(immediate_format,{'opcode': [0, 0, 1, 0, 1, 0]},
('slti', ' r', '%rt', ',', ' r', '%rs', ',', ' r', '%immediate'))
slti_imm_Instr.setCode(opCode, 'execution')
slti_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(slti_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
if ((unsigned) ((int)rs) < (unsigned int)(SignExtend(immediate,16)) ){
	rt = 0x0001;
}else{
	rt = 0x0000;
}
""")
sltiu_imm_Instr = trap.Instruction('SLTIU', True)
sltiu_imm_Instr.setMachineCode(immediate_format,{'opcode': [0, 0, 1, 0, 1, 1]},
('sltiu', ' r', '%rt', ',', ' r', '%rs', ',', ' r', '%immediate'))
sltiu_imm_Instr.setCode(opCode, 'execution')
sltiu_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(sltiu_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
if ((unsigned int)rs < (unsigned int)rt ){
	rd = 0x0001;
}else{
	rd = 0x0000;
}
""")
sltu_reg_Instr = trap.Instruction('SLTU', True)
sltu_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[1, 0, 1, 0, 1, 1]},
('sltu', ' r', '%rd', ',', ' r', '%rs', ',', ' r', '%rt'))
sltu_reg_Instr.setCode(opCode, 'execution')
sltu_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(sltu_reg_Instr)



#
#SUB Instruction Family
#

opCode = cxx_writer.writer_code.Code("""
long long opr1 = (rs & 0x80000000);
opr1 = opr1<<1 |rs;
long long opr2 = (rt & 0x80000000);
opr2 = opr2<<1 |rt;
long long temp32 = opr1-opr2;
long long temp31 = rs - rt;

if (((temp32 & 0x100000000)>>32) != ((temp31 & 0x80000000)>>31)){
	RaiseException(OV);
}else{
	rd = temp31;
}
""")
sub_reg_Instr = trap.Instruction('SUB', True)
sub_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[1, 0, 0, 0, 1, 0]},
('sub', ' r', '%rd', ',', ' r', '%rs', ',', ' r', '%rt'))
sub_reg_Instr.setCode(opCode, 'execution')
sub_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(sub_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
rd = rs-rt;
""")
subu_reg_Instr = trap.Instruction('SUBU', True)
subu_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[1, 0, 0, 0, 1, 1]},
('subu', ' r', '%rd', ',', ' r', '%rs', ',', ' r', '%rt'))
subu_reg_Instr.setCode(opCode, 'execution')
subu_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(subu_reg_Instr)



#
#Synchronize Shared Memory
#



#
#System Call
#


opCode = cxx_writer.writer_code.Code("""
RaiseException(SYS);
""")
syscall_reg_Instr = trap.Instruction('SYSCALL', True)
syscall_reg_Instr.setMachineCode(code_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[0, 0, 1, 1, 0, 0]},
('syscall'))
syscall_reg_Instr.setCode(opCode, 'execution')
syscall_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(syscall_reg_Instr)



#
#TRAP Instruction Family
#

opCodeOperands = cxx_writer.writer_code.Code("""
opr1 = rs;
opr2 = rt;
""")
opCodeOperandsI = cxx_writer.writer_code.Code("""
opr1 = rs;
opr2 = SignExtend(immediate,16);
""")
opCodeCondition = cxx_writer.writer_code.Code("""
cond = ((signed int)opr1==(signed int)opr2);
""")
opCodeCompare = cxx_writer.writer_code.Code("""
if (cond)
	RaiseException(TR);
""")
teq_reg_Instr = trap.Instruction('TEQ', True)
teq_reg_Instr.setMachineCode(trap_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[1, 1, 0, 1, 0, 0]},
('teq', ' r', '%rs', ',', ' r', '%rt'))
teq_reg_Instr.setCode(opCodeOperands, 'execution1')
teq_reg_Instr.setCode(opCodeCondition, 'execution2')
teq_reg_Instr.setCode(opCodeCompare, 'execution')
teq_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
teq_reg_Instr.addVariable(('opr1', 'BIT<32>'))
teq_reg_Instr.addVariable(('opr2', 'BIT<32>'))
teq_reg_Instr.addVariable(('cond', 'BIT<1>'))
isa.addInstruction(teq_reg_Instr)

teqi_reg_Instr = trap.Instruction('TEQI', True)
teqi_reg_Instr.setMachineCode(immediate_trap_format,{'opcode': [0, 0, 0, 0, 0, 1], 'rt': [0, 1, 1, 0, 0]},
('teqi', ' r', '%rs', ',', ' r', '%immediate'))
teqi_reg_Instr.setCode(opCodeOperandsI, 'execution1')
teqi_reg_Instr.setCode(opCodeCondition, 'execution2')
teqi_reg_Instr.setCode(opCodeCompare, 'execution')
teqi_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
teqi_reg_Instr.addVariable(('opr1', 'BIT<32>'))
teqi_reg_Instr.addVariable(('opr2', 'BIT<32>'))
teqi_reg_Instr.addVariable(('cond', 'BIT<1>'))
isa.addInstruction(teqi_reg_Instr)


opCodeCondition = cxx_writer.writer_code.Code("""
cond = ((signed int)opr1 >= (signed int)opr2);
""")
tge_reg_Instr = trap.Instruction('TGE', True)
tge_reg_Instr.setMachineCode(trap_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[1, 1, 0, 0, 0, 0]},
('tge', ' r', '%rs', ',', ' r', '%rt'))
tge_reg_Instr.setCode(opCodeOperands, 'execution1')
tge_reg_Instr.setCode(opCodeCondition, 'execution2')
tge_reg_Instr.setCode(opCodeCompare, 'execution')
tge_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
tge_reg_Instr.addVariable(('opr1', 'BIT<32>'))
tge_reg_Instr.addVariable(('opr2', 'BIT<32>'))
tge_reg_Instr.addVariable(('cond', 'BIT<1>'))
isa.addInstruction(tge_reg_Instr)

tgei_reg_Instr = trap.Instruction('TGEI', True)
tgei_reg_Instr.setMachineCode(immediate_trap_format,{'opcode': [0, 0, 0, 0, 0, 1], 'rt': [0, 1, 0, 0, 0]},
('tgei', ' r', '%rs', ',', ' r', '%immediate'))
tgei_reg_Instr.setCode(opCodeOperandsI, 'execution1')
tgei_reg_Instr.setCode(opCodeCondition, 'execution2')
tgei_reg_Instr.setCode(opCodeCompare, 'execution')
tgei_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
tgei_reg_Instr.addVariable(('opr1', 'BIT<32>'))
tgei_reg_Instr.addVariable(('opr2', 'BIT<32>'))
tgei_reg_Instr.addVariable(('cond', 'BIT<1>'))
isa.addInstruction(tgei_reg_Instr)

opCodeCondition = cxx_writer.writer_code.Code("""
cond = ((unsigned int)opr1 >= (unsigned int)opr2);
""")
tgeiu_reg_Instr = trap.Instruction('TGEIU', True)
tgeiu_reg_Instr.setMachineCode(immediate_trap_format,{'opcode': [0, 0, 0, 0, 0, 1], 'rt': [0, 1, 0, 0, 1]},
('tgeiu', ' r', '%rs', ',', ' r', '%immediate'))
tgeiu_reg_Instr.setCode(opCodeOperandsI, 'execution1')
tgeiu_reg_Instr.setCode(opCodeCondition, 'execution2')
tgeiu_reg_Instr.setCode(opCodeCompare, 'execution')
tgeiu_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
tgeiu_reg_Instr.addVariable(('opr1', 'BIT<32>'))
tgeiu_reg_Instr.addVariable(('opr2', 'BIT<32>'))
tgeiu_reg_Instr.addVariable(('cond', 'BIT<1>'))
isa.addInstruction(tgeiu_reg_Instr)

tgeu_reg_Instr = trap.Instruction('TGEU', True)
tgeu_reg_Instr.setMachineCode(trap_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[1, 1, 0, 0, 0, 1]},
('tgeu', ' r', '%rs', ',', ' r', '%rt'))
tgeu_reg_Instr.setCode(opCodeOperands, 'execution1')
tgeu_reg_Instr.setCode(opCodeCondition, 'execution2')
tgeu_reg_Instr.setCode(opCodeCompare, 'execution')
tgeu_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
tgeu_reg_Instr.addVariable(('opr1', 'BIT<32>'))
tgeu_reg_Instr.addVariable(('opr2', 'BIT<32>'))
tgeu_reg_Instr.addVariable(('cond', 'BIT<1>'))
isa.addInstruction(tgeu_reg_Instr)

opCodeCondition = cxx_writer.writer_code.Code("""
cond = ((signed int)opr1<(signed int)opr2);
""")
tlt_reg_Instr = trap.Instruction('TLT', True)
tlt_reg_Instr.setMachineCode(trap_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[1, 1, 0, 0, 1, 0]},
('tlt', ' r', '%rs', ',', ' r', '%rt'))
tlt_reg_Instr.setCode(opCodeOperands, 'execution1')
tlt_reg_Instr.setCode(opCodeCondition, 'execution2')
tlt_reg_Instr.setCode(opCodeCompare, 'execution')
tlt_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
tlt_reg_Instr.addVariable(('opr1', 'BIT<32>'))
tlt_reg_Instr.addVariable(('opr2', 'BIT<32>'))
tlt_reg_Instr.addVariable(('cond', 'BIT<1>'))
isa.addInstruction(tlt_reg_Instr)

tlti_reg_Instr = trap.Instruction('TLTI', True)
tlti_reg_Instr.setMachineCode(immediate_trap_format,{'opcode': [0, 0, 0, 0, 0, 1], 'rt': [0, 1, 0, 1, 0]},
('tlti', ' r', '%rs', ',', ' r', '%immediate'))
tlti_reg_Instr.setCode(opCodeOperandsI, 'execution1')
tlti_reg_Instr.setCode(opCodeCondition, 'execution2')
tlti_reg_Instr.setCode(opCodeCompare, 'execution')
tlti_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
tlti_reg_Instr.addVariable(('opr1', 'BIT<32>'))
tlti_reg_Instr.addVariable(('opr2', 'BIT<32>'))
tlti_reg_Instr.addVariable(('cond', 'BIT<1>'))
isa.addInstruction(tlti_reg_Instr)

opCodeCondition = cxx_writer.writer_code.Code("""
cond = ((unsigned int)opr1<(unsigned int)opr2);
""")
tltiu_reg_Instr = trap.Instruction('TLTIU', True)
tltiu_reg_Instr.setMachineCode(immediate_trap_format,{'opcode': [0, 0, 0, 0, 0, 1], 'rt': [0, 1, 0, 1, 1]},
('tltiu', ' r', '%rs', ',', ' r', '%immediate'))
tltiu_reg_Instr.setCode(opCodeOperandsI, 'execution1')
tltiu_reg_Instr.setCode(opCodeCondition, 'execution2')
tltiu_reg_Instr.setCode(opCodeCompare, 'execution')
tltiu_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
tltiu_reg_Instr.addVariable(('opr1', 'BIT<32>'))
tltiu_reg_Instr.addVariable(('opr2', 'BIT<32>'))
tltiu_reg_Instr.addVariable(('cond', 'BIT<1>'))
isa.addInstruction(tltiu_reg_Instr)

tltu_reg_Instr = trap.Instruction('TLTU', True)
tltu_reg_Instr.setMachineCode(trap_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[1, 1, 0, 0, 1, 1]},
('tltu', ' r', '%rs', ',', ' r', '%rt'))
tltu_reg_Instr.setCode(opCodeOperands, 'execution1')
tltu_reg_Instr.setCode(opCodeCondition, 'execution2')
tltu_reg_Instr.setCode(opCodeCompare, 'execution')
tltu_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
tltu_reg_Instr.addVariable(('opr1', 'BIT<32>'))
tltu_reg_Instr.addVariable(('opr2', 'BIT<32>'))
tltu_reg_Instr.addVariable(('cond', 'BIT<1>'))
isa.addInstruction(tltu_reg_Instr)

opCodeCondition = cxx_writer.writer_code.Code("""
cond = (opr1!=opr2);
""")
tne_reg_Instr = trap.Instruction('TNE', True)
tne_reg_Instr.setMachineCode(trap_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[1, 1, 0, 1, 1, 0]},
('tne', ' r', '%rs', ',', ' r', '%rt'))
tne_reg_Instr.setCode(opCodeOperands, 'execution1')
tne_reg_Instr.setCode(opCodeCondition, 'execution2')
tne_reg_Instr.setCode(opCodeCompare, 'execution')
tne_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
tne_reg_Instr.addVariable(('opr1', 'BIT<32>'))
tne_reg_Instr.addVariable(('opr2', 'BIT<32>'))
tne_reg_Instr.addVariable(('cond', 'BIT<1>'))
isa.addInstruction(tne_reg_Instr)

tnei_reg_Instr = trap.Instruction('TNEI', True)
tnei_reg_Instr.setMachineCode(immediate_trap_format,{'opcode': [0, 0, 0, 0, 0, 1], 'rt': [0, 1, 1, 1, 0]},
('tnei', ' r', '%rs', ',', ' r', '%immediate'))
tnei_reg_Instr.setCode(opCodeOperandsI, 'execution1')
tnei_reg_Instr.setCode(opCodeCondition, 'execution2')
tnei_reg_Instr.setCode(opCodeCompare, 'execution')
tnei_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
tnei_reg_Instr.addVariable(('opr1', 'BIT<32>'))
tnei_reg_Instr.addVariable(('opr2', 'BIT<32>'))
tnei_reg_Instr.addVariable(('cond', 'BIT<1>'))
isa.addInstruction(tnei_reg_Instr)



#
#XOR Instruction Family
#

opCode = cxx_writer.writer_code.Code("""
	rd = rs ^ rt;
""")
xor_reg_Instr = trap.Instruction('XOR', True)
xor_reg_Instr.setMachineCode(register_format,{'opcode': [0, 0, 0, 0, 0, 0], 'function':[1, 0, 0, 1, 1, 0]},
('xor', ' r', '%rd', ',', ' r', '%rs', ',', ' r', '%rt'))
xor_reg_Instr.setCode(opCode, 'execution')
xor_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(xor_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
	rs = immediate ^ rt;
""")
xor_imm_Instr = trap.Instruction('XORI', True)
xor_imm_Instr.setMachineCode(immediate_format,{'opcode': [0, 0, 1, 1, 1, 0]},
('xori', ' r', '%rt', ',', ' r', '%rs', ',', ' r', '%immediate'))
xor_imm_Instr.setCode(opCode, 'execution')
xor_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
isa.addInstruction(xor_imm_Instr)


#
#WAIT Instruction 
#

opCode = cxx_writer.writer_code.Code("""
ExtraRegister=0x80000000;	
""")
wait_Instr = trap.Instruction('WAITINST', True)
wait_Instr.setMachineCode(wait_format,{'opcode': [0, 1, 0, 0, 0, 0],  'inst':[1, 0, 0, 0, 0, 0]},
('WAIT'))
wait_Instr.setCode(opCode, 'execution')
wait_Instr.addBehavior(IncrementPC, 'execution')
isa.addInstruction(wait_Instr)
