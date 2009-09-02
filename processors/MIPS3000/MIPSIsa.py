#Starting to define the instructions by family. Alphabetical order (according to the instructions) is being used.
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
isa.addMethod(SimpleBranch)
isa.addMethod(LikelyBranch)

# Now I add some useful definitions to be used inside the instructions; they will be
# inserted as defines in the hpp and file of the instructions
isa.addDefines("""
#define 
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

# ADD instruction family


opCode = cxx_writer.writer_code.Code("""
rd = (int)rs + (int)rt;
""")	#Add exception
add_reg_Instr = trap.Instruction('ADD', True, frequency = ?)
add_reg_Instr.setMachineCode(register_format,{'opcode': [0,0,0,0,0,0],'function':[1,0,0,0,0,0]},('add r','%rd',' r','%rs',' r','%rt'))
add_reg_Instr.setCode(opCode, 'execution')
add_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Overflow exception should be thrown
add_reg_Instr.addTest('TODO')
isa.addInstruction(add_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
rt = (int)rs + SignExtend(immediate);
""")
addi_imm_Instr = trap.Instruction('ADDI', True, frequency = ?)
addi_imm_Instr.setMachineCode(imm_format,{'opcode': [0,0,1,0,0,0]},('addi r','%rt',' r','%rs',' r','%immediate'))
addi_imm_Instr.setCode(opCode, 'execution')
addi_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#Overflow exception should be thrown
addi_imm_Instr.addTest('TODO')
isa.addInstruction(addi_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
rt = (int)rs + (int)immediate;
""")
addiu_imm_Instr = trap.Instruction('ADDIU', True, frequency = ?)
addiu_imm_Instr.setMachineCode(imm_format,{'opcode': [0,0,1,0,0,1]},('addiu r','%rt',' r','%rs',' r','%immediate'))
addiu_imm_Instr.setCode(opCode, 'execution')
addiu_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
addiu_imm_Instr.addTest('TODO')
isa.addInstruction(addiu_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
rd = (int)rs + (int)rt;
""")
addu_reg_Instr = trap.Instruction('ADDU', True, frequency = ?)
addu_reg_Instr.setMachineCode(register_format,{'opcode': [0,0,0,0,0,0],'function':[1,0,0,0,0,1]},('addu r','%rd',' r','%rs',' r','%rt'))
addu_reg_Instr.setCode(opCode, 'execution')
addu_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
addu_reg_Instr.addTest('TODO')
isa.addInstruction(addu_reg_Instr)



#AND instruction family

opCode = cxx_writer.writer_code.Code("""
rd = rs & rt;
""")
and_reg_Instr = trap.Instruction('AND', True, frequency = ?)
and_reg_Instr.setMachineCode(register_format,{'opcode': [0,0,0,0,0,0],'function':[1,0,0,1,0,0]},('and r','%rd',' r','%rs',' r','%rt'))
and_reg_Instr.setCode(opCode, 'execution')
and_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
and_reg_Instr.addTest('TODO')
isa.addInstruction(and_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
rt = rs & (0x00 || immediate);
""")
andi_imm_Instr = trap.Instruction('ANDI', True, frequency = ?)
andi_imm_Instr.setMachineCode(imm_format,{'opcode': [0,0,1,1,0,0]},('andi r','%rt',' r','%rs',' r','%immediate'))
andi_imm_Instr.setCode(opCode, 'execution')
andi_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
andi_imm_Instr.addTest('TODO')
isa.addInstruction(andi_imm_Instr)



#BRANCH instruction family
#See what happens with the instructions B and BAL

opCode = cxx_writer.writer_code.Code("""
bool br = ( (rs == rt && op4 == 0) || (rs != rt && op4 == 0x1) );
	if (op2 == 0){
		SimpleBranch(br,(int)SignExtend(immediate));
	}else{
		LikelyBranch(br,(int)SignExtend(immediate));
	}
""")	#Specify correctly the jump instruction
b2r_imm_Instr = trap.Instruction('BRANCH2REGISTERS', True, frequency = ?)
b2r_imm_Instr.setMachineCode(b_format1,{'op3': [010]},
('b', ('%op4', {int('1',2):'ne', int('0',2):'eq'}), ('%op2', {int('1',2):'l'})
 ' r', '%rs', ' r', '%rt', ' r', '%immediate'))
b2r_imm_Instr.setCode(opCode, 'execution')
b2r_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
b2r_imm_Instr.addTest('TODO')
isa.addInstruction(b2r_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
bool br = ( ((int)rs<=0 && op4 == 0) || ((int)rs>0 && op4 == 0x1) );
	if (op2 == 0){
		SimpleBranch(br,(int)SignExtend(immediate));
	}else{
		LikelyBranch(br,(int)SignExtend(immediate));
	}
""")
bz_imm_Instr = trap.Instruction('BRANCHZ', True, frequency = ?)
bz_imm_Instr.setMachineCode(bz_format1,{'op3': [011]},
('b', ('%op4', {int('1',2):'gtz', int('0',2):'lez'}), ('%op2', {int('1',2):'l'}),
 ' r', '%rs', ' r', '%immediate'))
bz_imm_Instr.setCode(opCode, 'execution')
bz_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
bz_imm_Instr.addTest('TODO')
isa.addInstruction(bz_imm_Instr)


opCode = cxx_writer.writer_code.Code("""
bool br = ( ((int)rs<0 && (rt3 == 0x0 || rt3 == 0x2)) || ((int)rs>=0 && (rt3 == 0x1 || rt3== 0x3)) );
	if (rt == 0x1){
		GPR[31] = PC+8;
	}
	if (rt3 == 0x0 || rt3 == 0x1){
		SimpleBranch(br,(int)SignExtend(immediate));
	}else{
		LikelyBranch(br,(int)SignExtend(immediate));
	}
""")
breg_imm_Instr = trap.Instruction('BRANCHREGIMM', True, frequency = ?)
breg_imm_Instr.setMachineCode(b_format2,{},
('b', ('%rt3', {int('00',2):'ltz', int('01',2):'gez', int('10',2):'ltz', int('11',2):'gez'}),
 ('%rt', {int('1',2):'al'}),
 ('%rt3', {int('10', 2):'l', int('11', 2):'l'}),
 ' r', '%rs', ' r', '%immediate'))
breg_imm_Instr.setCode(opCode, 'execution')
breg_imm_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
breg_imm_Instr.addTest('TODO')
isa.addInstruction(breg_imm_Instr)



#BREAK



#CACHE



#COP0



#CLO

opCode = cxx_writer.writer_code.Code("""
rd = 0;
for (int i = 0; i < 32; i++) {
	/*
	 *aux = rs;
	 *rd += ((aux<<i)>>31);
	*/
	rd += rs % 2;
}
""")
clo_reg_Instr = trap.Instruction('CLO', True, frequency = ?)
clo_reg_Instr.setMachineCode(register_format,{'opcode': [0,1,1,1,0,0],'function':[1,0,0,0,0,1]},('clo r','%rd',' r','%rs'))
clo_reg_Instr.setCode(opCode, 'execution')
clo_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
clo_reg_Instr.addTest('TODO')
isa.addInstruction(clo_reg_Instr)



#CLZ

opCode = cxx_writer.writer_code.Code("""
rd = 0;
for (int i = 0; i < 32; i++) {
	/*
	 *aux = rs;
	 *rd += (int)((aux<<i)>>31);
	 */
	rd += rs % 2;
}
rd = 32-rd;
""")
clz_reg_Instr = trap.Instruction('CLZ', True, frequency = ?)
clz_reg_Instr.setMachineCode(register_format,{'opcode': [0,1,1,1,0,0],'function':[1,0,0,0,0,1]},('clz r','%rd',' r','%rs'))
clz_reg_Instr.setCode(opCode, 'execution')
clz_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
clz_reg_Instr.addTest('TODO')
isa.addInstruction(clz_reg_Instr)



#DERET



#DIV instruction family

opCode = cxx_writer.writer_code.Code("""
LO = (int)SignExtend(rs) / (int)SignExtend(rt);
HI = (int)SignExtend(rs) % (int)SignExtend(rt);
""")	#Add exception
div_reg_Instr = trap.Instruction('DIV', True, frequency = ?)
div_reg_Instr.setMachineCode(register_format,{'opcode': [0,0,0,0,0,0],'function':[0,1,1,0,1,0]},('div r','%rd',' r','%rs'))
div_reg_Instr.setCode(opCode, 'execution')
div_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#DZ -division by zero- exception should be thrown
div_reg_Instr.addTest('TODO')
isa.addInstruction(div_reg_Instr)


opCode = cxx_writer.writer_code.Code("""
LO = (unsigned int)SignExtend(rs) / (unsigned int)SignExtend(rt);
HI = (unsigned int)SignExtend(rs) % (unsigned int)SignExtend(rt);
""")	#Add exception
divu_reg_Instr = trap.Instruction('DIVU', True, frequency = ?)
divu_reg_Instr.setMachineCode(register_format,{'opcode': [0,0,0,0,0,0],'function':[0,1,1,0,1,1]},('divu r','%rd',' r','%rs'))
divu_reg_Instr.setCode(opCode, 'execution')
divu_reg_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
							#DZ -division by zero- exception should be thrown
divu_reg_Instr.addTest('TODO')
isa.addInstruction(divu_reg_Instr)



#ERET



#JUMP Instruction Family

opCode = cxx_writer.writer_code.Code("""
if (op2 == 0b1){
GPR[31] = PC+8;
}
NPC = PC[31:28] || target<<2;
""")
jump_Instr = trap.Instruction('CLZ', True, frequency = ?)
jump_Instr.setMachineCode(jump_format,{},('j', ('%op2',{int('1',2):'al'}), ' r', '%target'))
jump_Instr.setCode(opCode, 'execution')
jump_Instr.addBehavior(IncrementPC, 'execution')	#Check if more behaviors need to be added
jump_Instr.addTest('TODO')
isa.addInstruction(jump_Instr)



#LOAD Instruction Family
