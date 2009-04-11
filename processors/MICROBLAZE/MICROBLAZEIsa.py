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
from MICROBLAZECoding import *
from MICROBLAZEMethods import *

# ISA declaration: it is the container for all the single instructions
isa = trap.ISA()

# Now I add to the ISA all the helper methods and operations which will be
# called from the instructions
isa.addMethod(restoreSPSR_method)
isa.addMethod(updateAlias_method)
isa.addMethod(AShiftRight_method)
isa.addMethod(RotateRight_method)
isa.addMethod(LSRegShift_method)
isa.addMethod(SignExtend_method)
isa.addMethod(UpdatePSRBitM_method)
isa.addMethod(UpdatePSRAdd_method)
isa.addMethod(UpdatePSRSub_method)

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

#this is just a trial

#ADD instruction family
# ADD, first version
#~ opCode = cxx_writer.writer_code.Code("""
#~ unsigned long long result = (int)rb + (int)ra;
#~ MSR[C] = ((unsigned long long)result) >> 32;  #get the CarryOut
#~ rd = (unsigned int)result;
#~ """)
#~ add_Instr = trap.Instruction('ADD', True)
#~ add_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
#~ add_Instr.setCode(opCode,'execute')
#~ add_Instr.addBehavior(IncrementPC, 'execute')
#~ isa.addInstruction(add_Instr)

# ADD, second version
opCode = cxx_writer.writer_code.Code("""
result = (int)rb + (int)ra;
MSR[key_C] = result >> 32;  #get the CarryOut
rd = (unsigned int)result;
""")
add_Instr = trap.Instruction('ADD', True) #?? what does 'true' mean?
add_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
add_Instr.setCode(opCode,'execute')
add_Instr.addBehavior(IncrementPC, 'execute')
add_Instr.addVariable(('result', 'BIT<64>'))
add_Instr.addTest({'rd': 5, 'ra': 3, 'rb': 2}, {'GPR[3]': 4, 'GPR[2]': 6, 'GPR[5]': 0xfffff, 'PC':0x0}, {'GPR[5]': 10, 'PC':0x8})
isa.addInstruction(add_Instr)

# ADDC
opCode = cxx_writer.writer_code.Code("""
result = (int)rb + (int)ra + (unsigned int)MSR[key_C];
MSR[key_C] = result >> 32; #get the CarryOut
rd = (unsigned int)result;
""")
addc_Instr = trap.Instruction('ADDC', True)
addc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
addc_Instr.setCode(opCode,'execute')
addc_Instr.addBehavior(IncrementPC, 'execute')
addc_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(addc_Instr)

# ADDK
opCode = cxx_writer.writer_code.Code("""
rd = (int)rb + (int)ra;
""")
addk_Instr = trap.Instruction('ADDK', True)
addk_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
addk_Instr.setCode(opCode,'execute')
addk_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(addk_Instr)

# ADDKC
opCode = cxx_writer.writer_code.Code("""
rd = (int)rb + (int)ra +(unsigned int)MSR[key_C];
""")
addkc_Instr = trap.Instruction('ADDKC', True)
addkc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
addkc_Instr.setCode(opCode,'execute')
addkc_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(addkc_Instr)

#ADDI instruction family
#ADDI
opCode = cxx_writer.writer_code.Code("""
result = (int)ra + ((int)SignExtend(imm, 16));
MSR[key_C] = result >> 32;
rd = (unsigned int)result;
""")
addi_Instr = trap.Instruction('ADDI', True)
addi_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,0,0]}, 'TODO')
addi_Instr.setCode(opCode,'execute')
addi_Instr.addBehavior(IncrementPC, 'execute')
addi_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(addi_Instr)

#ADDIC
opCode = cxx_writer.writer_code.Code("""
result = (int)ra + ((int)SignExtend(imm,16)) + (unsigned int)MSR[key_C];
MSR[key_C] = result >> 32;
rd = (unsigned int)result;
""")
addic_Instr = trap.Instruction('ADDIC', True)
addic_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,1,0]}, 'TODO')
addic_Instr.setCode(opCode,'execute')
addic_Instr.addBehavior(IncrementPC, 'execute')
addic_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(addic_Instr)

#ADDIK
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra + ((int)SignExtend(imm, 16));
""")
addik_Instr = trap.Instruction('ADDIK', True)
addik_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,0,0]}, 'TODO')
addik_Instr.setCode(opCode,'execute')
addik_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(addik_Instr)

#ADDIKC
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra + ((int)SignExtend(imm, 16)) +(int)MSR[key_C];
""")
addikc_Instr = trap.Instruction('ADDIKC', True)
addikc_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,1,0]}, 'TODO')
addikc_Instr.setCode(opCode,'execute')
addikc_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(addikc_Instr)

#from here to the end, it is specified for each instruction, only
#the bytecode and the name.
#After, it will be specified also the behavior.

#AND
opCode = cxx_writer.writer_code.Code("""

""")
and_Instr = trap.Instruction('AND', True)
and_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
and_Instr.setCode(opCode,'execute')
isa.addInstruction(and_Instr)

#AND instruction family
#ANDI
opCode = cxx_writer.writer_code.Code("""

""")
andi_Instr = trap.Instruction('AND', True)
andi_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,0,1]}, 'TODO')
andi_Instr.setCode(opCode,'execute')
isa.addInstruction(andi_Instr)

#ANDN
opCode = cxx_writer.writer_code.Code("""

""")
andn_Instr = trap.Instruction('ANDN', True)
andn_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,1,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
andn_Instr.setCode(opCode,'execute')
isa.addInstruction(andn_Instr)

#ANDNI
opCode = cxx_writer.writer_code.Code("""

""")
andni_Instr = trap.Instruction('ANDNI', True)
andni_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,1,1]}, 'TODO')
andni_Instr.setCode(opCode,'execute')
isa.addInstruction(andni_Instr)

#BRANCH instruction family
#BEQ
#TODO: check if BEQ opcode is correct
opCode = cxx_writer.writer_code.Code("""
if (ra==0) {
	PC = PC + ((int)SignExtend(rb, 8));
} else {
	PC = PC + 4;
}
""")
beq_Instr = trap.Instruction('BEQ','True')
beq_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
beq_Instr.setCode(opCode,'execute')
# we increment PC in the code. We don't have to use IncrementPCBehavior.
# beq_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(beq_Instr)

#BEQD
#TODO: check if BEQ is correct
opCode = cxx_writer.writer_code.Code("""

""")
beqd_Instr = trap.Instruction('BEQD','True')
beqd_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
beqd_Instr.setCode(opCode,'execute')
# we increment PC in the code. We don't have to use IncrementPCBehavior.
# beq_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(beqd_Instr)

#BEQI
opCode = cxx_writer.writer_code.Code("""

""")
beqi_Instr = trap.Instruction('BEQI','True')
beqi_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,0,0]}, 'TODO')
beqi_Instr.setCode(opCode,'execute')
isa.addInstruction(beqi_Instr)

#BEQID
opCode = cxx_writer.writer_code.Code("""

""")
beqid_Instr = trap.Instruction('BEQID','True')
beqid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,0,0,0]}, 'TODO')
beqid_Instr.setCode(opCode,'execute')
isa.addInstruction(beqid_Instr)

#BGE
opCode = cxx_writer.writer_code.Code("""

""")
bge_Instr = trap.Instruction('BGE','True')
bge_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,1,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bge_Instr.setCode(opCode,'execute')
isa.addInstruction(bge_Instr)

#BGED
opCode = cxx_writer.writer_code.Code("""

""")
bged_Instr = trap.Instruction('BGED','True')
bged_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,1,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bged_Instr.setCode(opCode,'execute')
isa.addInstruction(bged_Instr)

#BGEI
opCode = cxx_writer.writer_code.Code("""

""")
bgei_Instr = trap.Instruction('BGEI','True')
bgei_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,1,0,1]}, 'TODO')
bgei_Instr.setCode(opCode,'execute')
isa.addInstruction(bgei_Instr)

#BGEID
opCode = cxx_writer.writer_code.Code("""

""")
bgeid_Instr = trap.Instruction('BGEID','True')
bgeid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,1,0,1]}, 'TODO')
bgeid_Instr.setCode(opCode,'execute')
isa.addInstruction(bgeid_Instr)

#BGT
opCode = cxx_writer.writer_code.Code("""

""")
bgt_Instr = trap.Instruction('BGT','True')
bgt_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bgt_Instr.setCode(opCode,'execute')
isa.addInstruction(bgt_Instr)

#BGTD
opCode = cxx_writer.writer_code.Code("""

""")
bgtd_Instr = trap.Instruction('BGTD','True')
bgtd_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bgtd_Instr.setCode(opCode,'execute')
isa.addInstruction(bgtd_Instr)

#BGTI
opCode = cxx_writer.writer_code.Code("""

""")
bgti_Instr = trap.Instruction('BGTI','True')
bgti_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,1,0,0]}, 'TODO')
bgti_Instr.setCode(opCode,'execute')
isa.addInstruction(bgti_Instr)

#BGTID
opCode = cxx_writer.writer_code.Code("""

""")
bgtid_Instr = trap.Instruction('BGTID','True')
bgtid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,1,0,0]}, 'TODO')
bgtid_Instr.setCode(opCode,'execute')
isa.addInstruction(bgtid_Instr)

#BLE
opCode = cxx_writer.writer_code.Code("""

""")
ble_Instr = trap.Instruction('BLE','True')
ble_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,1,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
ble_Instr.setCode(opCode,'execute')
isa.addInstruction(ble_Instr)

#BLED
opCode = cxx_writer.writer_code.Code("""

""")
bled_Instr = trap.Instruction('BLED','True')
bled_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,0,1,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bled_Instr.setCode(opCode,'execute')
isa.addInstruction(bled_Instr)

#BLEI
opCode = cxx_writer.writer_code.Code("""

""")
blei_Instr = trap.Instruction('BLEI','True')
blei_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,1,1]}, 'TODO')
blei_Instr.setCode(opCode,'execute')
isa.addInstruction(blei_Instr)

#BLEID
opCode = cxx_writer.writer_code.Code("""

""")
bleid_Instr = trap.Instruction('BLEID','True')
bleid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,0,1,1]}, 'TODO')
bleid_Instr.setCode(opCode,'execute')
isa.addInstruction(bleid_Instr)

#BLT
opCode = cxx_writer.writer_code.Code("""

""")
blt_Instr = trap.Instruction('BLT','True')
blt_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,1,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
blt_Instr.setCode(opCode,'execute')
isa.addInstruction(blt_Instr)

#BLTD
opCode = cxx_writer.writer_code.Code("""

""")
bltd_Instr = trap.Instruction('BLTD','True')
bltd_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,0,1,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bltd_Instr.setCode(opCode,'execute')
isa.addInstruction(bltd_Instr)

#BLTI
opCode = cxx_writer.writer_code.Code("""

""")
blti_Instr = trap.Instruction('BLTI','True')
blti_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,1,0]}, 'TODO')
blti_Instr.setCode(opCode,'execute')
isa.addInstruction(blti_Instr)

#BLTID
opCode = cxx_writer.writer_code.Code("""

""")
bltid_Instr = trap.Instruction('BLTID','True')
bltid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,0,1,0]}, 'TODO')
bltid_Instr.setCode(opCode,'execute')
isa.addInstruction(bltid_Instr)

#BNE
opCode = cxx_writer.writer_code.Code("""

""")
bne_Instr = trap.Instruction('BNE','True')
bne_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bne_Instr.setCode(opCode,'execute')
isa.addInstruction(bne_Instr)

#BNED
opCode = cxx_writer.writer_code.Code("""

""")
bned_Instr = trap.Instruction('BNED','True')
bned_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,0,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bned_Instr.setCode(opCode,'execute')
isa.addInstruction(bned_Instr)

#BNEI
opCode = cxx_writer.writer_code.Code("""

""")
bnei_Instr = trap.Instruction('BNEI','True')
bnei_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,0,1]}, 'TODO')
bnei_Instr.setCode(opCode,'execute')
isa.addInstruction(bnei_Instr)

#BNEID
opCode = cxx_writer.writer_code.Code("""

""")
bneid_Instr = trap.Instruction('BNEID','True')
bneid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,0,0,1]}, 'TODO')
bneid_Instr.setCode(opCode,'execute')
isa.addInstruction(bneid_Instr)

#BR
opCode = cxx_writer.writer_code.Code("""

""")
br_Instr = trap.Instruction('BR','True')
br_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [0,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
br_Instr.setCode(opCode,'execute')
isa.addInstruction(br_Instr)

#BRA
opCode = cxx_writer.writer_code.Code("""

""")
bra_Instr = trap.Instruction('BRA','True')
bra_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [0,1,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bra_Instr.setCode(opCode,'execute')
isa.addInstruction(bra_Instr)

#BRD
opCode = cxx_writer.writer_code.Code("""

""")
brd_Instr = trap.Instruction('BRD','True')
brd_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [1,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
brd_Instr.setCode(opCode,'execute')
isa.addInstruction(brd_Instr)

#BRAD
opCode = cxx_writer.writer_code.Code("""

""")
brad_Instr = trap.Instruction('BRAD','True')
brad_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [1,1,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
brad_Instr.setCode(opCode,'execute')
isa.addInstruction(brad_Instr)

#BRLD
opCode = cxx_writer.writer_code.Code("""

""")
brld_Instr = trap.Instruction('BRLD','True')
brld_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [1,0,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
brld_Instr.setCode(opCode,'execute')
isa.addInstruction(brld_Instr)

#BRALD
opCode = cxx_writer.writer_code.Code("""

""")
brald_Instr = trap.Instruction('BRALD','True')
brald_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [1,1,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
brald_Instr.setCode(opCode,'execute')
isa.addInstruction(brald_Instr)

#BRI
opCode = cxx_writer.writer_code.Code("""

""")
bri_Instr = trap.Instruction('BRI','True')
bri_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [0,0,0,0,0]}, 'TODO')
bri_Instr.setCode(opCode,'execute')
isa.addInstruction(bri_Instr)

#BRAI
opCode = cxx_writer.writer_code.Code("""

""")
brai_Instr = trap.Instruction('BRAI','True')
brai_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [0,1,0,0,0]}, 'TODO')
brai_Instr.setCode(opCode,'execute')
isa.addInstruction(brai_Instr)

#BRID
opCode = cxx_writer.writer_code.Code("""

""")
brid_Instr = trap.Instruction('BRID','True')
brid_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [1,0,0,0,0]}, 'TODO')
brid_Instr.setCode(opCode,'execute')
isa.addInstruction(brid_Instr)

#BRAID
opCode = cxx_writer.writer_code.Code("""

""")
brai_Instr = trap.Instruction('BRAID','True')
brai_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [1,1,0,0,0]}, 'TODO')
brai_Instr.setCode(opCode,'execute')
isa.addInstruction(brai_Instr)

#BRLID
opCode = cxx_writer.writer_code.Code("""

""")
brlid_Instr = trap.Instruction('BRLID','True')
brlid_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [1,0,1,0,0]}, 'TODO')
brlid_Instr.setCode(opCode,'execute')
isa.addInstruction(brlid_Instr)

#BRALID
opCode = cxx_writer.writer_code.Code("""

""")
bralid_Instr = trap.Instruction('BRALID','True')
bralid_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [1,1,1,0,0]}, 'TODO')
bralid_Instr.setCode(opCode,'execute')
isa.addInstruction(bralid_Instr)

#BRK
#BRK is equal to BRAL
opCode = cxx_writer.writer_code.Code("""

""")
brk_Instr = trap.Instruction('BRK','True')
brk_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [0,1,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
brk_Instr.setCode(opCode,'execute')
isa.addInstruction(brk_Instr)

#BRKI
#BRKI is equal to BRALI
opCode = cxx_writer.writer_code.Code("""

""")
brki_Instr = trap.Instruction('BRKI','True')
brki_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [0,1,1,0,0]}, 'TODO')
brki_Instr.setCode(opCode,'execute')
isa.addInstruction(brki_Instr)

#BARREL SHIFT family
#BSRL (S=0, T=0)
opCode = cxx_writer.writer_code.Code("""

""")­
bsrl_Instr = trap.Instruction('BSRL', True)
bsrl_Instr.setMachineCode(barrel_reg, {'opcode0': [0,1,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bsrl_Instr.setCode(opCode,'execute')
isa.addInstruction(bsrl_Instr)

#BSRA (S=0, T=1)
opCode = cxx_writer.writer_code.Code("""

""")­
bsra_Instr = trap.Instruction('BSRA', True)
bsra_Instr.setMachineCode(barrel_reg, {'opcode0': [0,1,0,0,0,1], 'opcode1': [0,1,0,0,0,0,0,0,0,0,0]}, 'TODO')
bsra_Instr.setCode(opCode,'execute')
isa.addInstruction(bsra_Instr)

#BSLL (S=1, T=0)
opCode = cxx_writer.writer_code.Code("""

""")­
bsll_Instr = trap.Instruction('BSLL', True)
bsll_Instr.setMachineCode(barrel_reg, {'opcode0': [0,1,0,0,0,1], 'opcode1': [1,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bsll_Instr.setCode(opCode,'execute')
isa.addInstruction(bsll_Instr)

#BSRLI (S=0, T=0)
opCode = cxx_writer.writer_code.Code("""

""")­
bsrli_Instr = trap.Instruction('BSRLI', True)
bsrli_Instr.setMachineCode(barrel_imm, {'opcode0': [0,1,1,0,0,1], 'opcode1': [0,0,0,0,0], 'opcode2': [0,0,0,0,0,0]}, 'TODO')
bsrli_Instr.setCode(opCode,'execute')
isa.addInstruction(bsrli_Instr)

#BSRAI (S=0, T=1)
opCode = cxx_writer.writer_code.Code("""

""")­
bsrai_Instr = trap.Instruction('BSRAI', True)
bsrai_Instr.setMachineCode(barrel_imm, {'opcode0': [0,1,1,0,0,1], 'opcode1': [0,0,0,0,0], 'opcode2': [0,1,0,0,0,0]}, 'TODO')
bsrai_Instr.setCode(opCode,'execute')
isa.addInstruction(bsrai_Instr)

#BSLLI (S=0, T=1)
opCode = cxx_writer.writer_code.Code("""

""")­
bslli_Instr = trap.Instruction('BSLLI', True)
bslli_Instr.setMachineCode(barrel_imm, {'opcode0': [0,1,1,0,0,1], 'opcode1': [0,0,0,0,0], 'opcode2': [1,0,0,0,0,0]}, 'TODO')
bslli_Instr.setCode(opCode,'execute')
isa.addInstruction(bslli_Instr)

#CMP ...
