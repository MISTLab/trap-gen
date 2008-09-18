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
from ARMCoding import *
from ARMMethods import *

# ISA declaration: it is the container for all the single instructions
isa = trap.ISA()

# Now I add to the ISA all the helper methods and operations which will be
# called from the instructions
isa.addMethod(triggerIRQ)
isa.addMethod(triggerFIQ)
isa.addMethod(restoreSPSR_method)
isa.addMethod(updateAlias_method)
isa.addMethod(AShiftRight_method)
isa.addMethod(RotateRight_method)

#-------------------------------------------------------------------------------------
# Let's now procede to set the behavior of the instructions
#-------------------------------------------------------------------------------------
#
# Note the special operations:
#
# -- flush(): flushes the current instruction out of the pipeline; if we are
# in the middle of the execution of some code, it also terminates the
# execution of that part of code (it is like an exception)
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

# ADC instruction family
opCode = cxx_writer.Code("""
result = (long long) ((long long)rn + (long long)operand);
if (CPSR["C"]){
    result += 1;
}
rd = result;
""")
adc_shift_imm_Instr = trap.Instruction('ADC_si', True)
adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
adc_shift_imm_Instr.setCode(opCode, 'execute')
adc_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
adc_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
adc_shift_imm_Instr.addBehavior(UpdatePSRSum, 'execute', False)
adc_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
adc_shift_imm_Instr.addVariable(('result', 'BIT<64>'))
adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
isa.addInstruction(adc_shift_imm_Instr)
adc_shift_reg_Instr = trap.Instruction('ADC_sr', True)
adc_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
adc_shift_reg_Instr.setCode(opCode, 'execute')
adc_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
adc_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
adc_shift_reg_Instr.addBehavior(UpdatePSRSum, 'execute', False)
adc_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
adc_shift_reg_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(adc_shift_reg_Instr)
adc_imm_Instr = trap.Instruction('ADC_i', True)
adc_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [0, 1, 0, 1]}, 'TODO')
adc_imm_Instr.setCode(opCode, 'execute')
adc_imm_Instr.addBehavior(condCheckOp, 'execute')
adc_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
adc_imm_Instr.addBehavior(UpdatePSRSum, 'execute', False)
adc_imm_Instr.addBehavior(UpdatePC, 'execute', False)
adc_imm_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(adc_imm_Instr)

# ADD instruction family
opCode = cxx_writer.Code("""
result = (long long) ((long long)rn + (long long)operand);
rd = result;
""")
add_shift_imm_Instr = trap.Instruction('ADD_si', True)
add_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 0]}, 'TODO')
add_shift_imm_Instr.setCode(opCode, 'execute')
add_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
add_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
add_shift_imm_Instr.addBehavior(UpdatePSRSum, 'execute', False)
add_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
add_shift_imm_Instr.addVariable(('result', 'BIT<64>'))
add_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
isa.addInstruction(add_shift_imm_Instr)
add_shift_reg_Instr = trap.Instruction('ADD_sr', True)
add_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 1, 0, 0]}, 'TODO')
add_shift_reg_Instr.setCode(opCode, 'execute')
add_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
add_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
add_shift_reg_Instr.addBehavior(UpdatePSRSum, 'execute', False)
add_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
add_shift_reg_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(add_shift_reg_Instr)
add_imm_Instr = trap.Instruction('ADD_i', True)
add_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [0, 1, 0, 0]}, 'TODO')
add_imm_Instr.setCode(opCode, 'execute')
add_imm_Instr.addBehavior(condCheckOp, 'execute')
add_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
add_imm_Instr.addBehavior(UpdatePSRSum, 'execute', False)
add_imm_Instr.addBehavior(UpdatePC, 'execute', False)
add_imm_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(add_imm_Instr)

# AND instruction family
opCode = cxx_writer.Code("""
rd = rn & operand;
""")
and_shift_imm_Instr = trap.Instruction('AND_si', True)
and_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 0, 0, 0]}, 'TODO')
and_shift_imm_Instr.setCode(opCode, 'execute')
and_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
and_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
and_shift_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
and_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
and_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
isa.addInstruction(and_shift_imm_Instr)
and_shift_reg_Instr = trap.Instruction('AND_sr', True)
and_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 0, 0, 0]}, 'TODO')
and_shift_reg_Instr.setCode(opCode, 'execute')
and_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
and_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
and_shift_reg_Instr.addBehavior(UpdatePSRBit, 'execute', False)
and_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(and_shift_reg_Instr)
and_imm_Instr = trap.Instruction('AND_i', True)
and_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [0, 0, 0, 0]}, 'TODO')
and_imm_Instr.setCode(opCode, 'execute')
and_imm_Instr.addBehavior(condCheckOp, 'execute')
and_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
and_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
and_imm_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(and_imm_Instr)

# BRANCH instruction family
opCode = cxx_writer.Code("""
if(l == 1) {
    LR = PC - 4;
}
PC += ((SignExtend(offset, 24) << 2);
stall(2);
""")
branch_Instr = trap.Instruction('BRANCH', True)
branch_Instr.setMachineCode(branch, {}, 'TODO')
branch_Instr.setCode(opCode, 'execute')
branch_Instr.addBehavior(condCheckOp, 'execute')
isa.addInstruction(branch_Instr)
opCode = cxx_writer.Code("""
// Note how the T bit is not considered since we do not bother with
// thumb mode
PC = rm & 0xFFFFFFFC;
stall(2);
""")
branch_thumb_Instr = trap.Instruction('BRANCHX', True)
branch_thumb_Instr.setMachineCode(branch_thumb, {}, 'TODO')
branch_thumb_Instr.setCode(opCode, 'execute')
branch_thumb_Instr.addBehavior(condCheckOp, 'execute')
isa.addInstruction(branch_thumb_Instr)

# BIC instruction family
opCode = cxx_writer.Code("""
rd = rn & ~operand;
""")
bic_shift_imm_Instr = trap.Instruction('BIC_si', True)
bic_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 1, 1, 0]}, 'TODO')
bic_shift_imm_Instr.setCode(opCode, 'execute')
bic_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
bic_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
bic_shift_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
bic_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
bic_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
isa.addInstruction(bic_shift_imm_Instr)
bic_shift_reg_Instr = trap.Instruction('BIC_sr', True)
bic_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 1, 1, 0]}, 'TODO')
bic_shift_reg_Instr.setCode(opCode, 'execute')
bic_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
bic_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
bic_shift_reg_Instr.addBehavior(UpdatePSRBit, 'execute', False)
bic_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(bic_shift_reg_Instr)
bic_imm_Instr = trap.Instruction('BIC_i', True)
bic_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 1, 1, 0]}, 'TODO')
bic_imm_Instr.setCode(opCode, 'execute')
bic_imm_Instr.addBehavior(condCheckOp, 'execute')
bic_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
bic_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
bic_imm_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(bic_imm_Instr)

# CMN instruction family
opCode = cxx_writer.Code("""
result = (long long) ((long long)rn + (long long)operand);
""")
cmn_shift_imm_Instr = trap.Instruction('CMN_si', True)
cmn_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 0, 1, 1], 's': [1]}, 'TODO')
cmn_shift_imm_Instr.setCode(opCode, 'execute')
cmn_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
cmn_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
cmn_shift_imm_Instr.addBehavior(UpdatePSRSum, 'execute', False)
cmn_shift_imm_Instr.addVariable(('result', 'BIT<64>'))
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
isa.addInstruction(cmn_shift_imm_Instr)
cmn_shift_reg_Instr = trap.Instruction('CMN_sr', True)
cmn_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 0, 1, 1], 's': [1]}, 'TODO')
cmn_shift_reg_Instr.setCode(opCode, 'execute')
cmn_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
cmn_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
cmn_shift_reg_Instr.addBehavior(UpdatePSRSum, 'execute', False)
cmn_shift_reg_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(cmn_shift_reg_Instr)
cmn_imm_Instr = trap.Instruction('CMN_i', True)
cmn_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 0, 1, 1], 's': [1]}, 'TODO')
cmn_imm_Instr.setCode(opCode, 'execute')
cmn_imm_Instr.addBehavior(condCheckOp, 'execute')
cmn_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
cmn_imm_Instr.addBehavior(UpdatePSRSum, 'execute', False)
cmn_imm_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(cmn_imm_Instr)

# CMP instruction family
opCode = cxx_writer.Code("""
result = (long long) ((long long)rn - (long long)operand);
""")
cmp_shift_imm_Instr = trap.Instruction('CMP_si', True)
cmp_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 0, 1, 0], 's': [1]}, 'TODO')
cmp_shift_imm_Instr.setCode(opCode, 'execute')
cmp_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
cmp_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
cmp_shift_imm_Instr.addBehavior(UpdatePSRSub, 'execute', False)
cmp_shift_imm_Instr.addVariable(('result', 'BIT<64>'))
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
isa.addInstruction(cmp_shift_imm_Instr)
cmp_shift_reg_Instr = trap.Instruction('CMP_sr', True)
cmp_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 0, 1, 0], 's': [1]}, 'TODO')
cmp_shift_reg_Instr.setCode(opCode, 'execute')
cmp_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
cmp_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
cmp_shift_reg_Instr.addBehavior(UpdatePSRSub, 'execute', False)
cmp_shift_reg_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(cmp_shift_reg_Instr)
cmp_imm_Instr = trap.Instruction('CMP_i', True)
cmp_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 0, 1, 0], 's': [1]}, 'TODO')
cmp_imm_Instr.setCode(opCode, 'execute')
cmp_imm_Instr.addBehavior(condCheckOp, 'execute')
cmp_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
cmp_imm_Instr.addBehavior(UpdatePSRSub, 'execute', False)
cmp_imm_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(cmp_imm_Instr)

# EOR instruction family
opCode = cxx_writer.Code("""
rd = rn ^ operand;
""")
eor_shift_imm_Instr = trap.Instruction('EOR_si', True)
eor_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 0, 0, 1]}, 'TODO')
eor_shift_imm_Instr.setCode(opCode, 'execute')
eor_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
eor_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
eor_shift_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
eor_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
eor_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
isa.addInstruction(eor_shift_imm_Instr)
eor_shift_reg_Instr = trap.Instruction('EOR_sr', True)
eor_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 0, 0, 1]}, 'TODO')
eor_shift_reg_Instr.setCode(opCode, 'execute')
eor_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
eor_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
eor_shift_reg_Instr.addBehavior(UpdatePSRBit, 'execute', False)
eor_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(eor_shift_reg_Instr)
eor_imm_Instr = trap.Instruction('EOR_i', True)
eor_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [0, 0, 0, 1]}, 'TODO')
eor_imm_Instr.setCode(opCode, 'execute')
eor_imm_Instr.addBehavior(condCheckOp, 'execute')
eor_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
eor_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
eor_imm_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(eor_imm_Instr)

# LDM instruction family
opCode = cxx_writer.Code("""
unsigned int numRegsToLoad = 0;
//First of all I have to check that I'm not dealing with user mode registers:
if((s == 1) && ((reg_list & 0x00008000) == 0)){
    //I'm dealing with user-mode registers: LDM type two
    //Load the registers common to all modes
    for(int i = 0; i < 16; i++){
        if((reg_list & (0x00000001 << i)) != 0){
            RB[i] = dataMem.read_word(start_address);
            start_address += 4;
            numRegsToLoad++;
        }
    }
    loadLatency = numRegsToLoad + 1;
}
else{
    //I'm dealing just with the current registers: LDM type one or three
    // First of all if it is necessary I perform the writeback
    if(w != 0){
        rn = wb_address;
    }

    //First af all I read the memory in the register I in the register list.
    for(int i = 0; i < 15; i++){
        if((reg_list & (0x00000001 << i)) != 0){
            REGS[i] = dataMem.read_word(start_address);
            start_address += 4;
            numRegsToLoad++;
        }
    }
    loadLatency = numRegsToLoad + 1;

    //I tread in a special way the PC, since loading a value in the PC is like performing a branch.
    if((reg_list & 0x00008000) != 0){
        //I have to load also the PC: it is like a branch; since I don't bother with
        //Thumb mode, bits 0 and 1 of the PC are ignored
        PC = dataMem.read_word(start_address) & 0xFFFFFFFC;
        if(s == 1){
            //LDM type three: in this type of operation I also have to restore the PSR.
            restoreSPSR();
        }
        numRegsToLoad++;
        loadLatency += 2;
    }
}
if((reg_list & 0x00008000) == 0){
    PC += 4;
}
stall(loadLatency);
""")
ldm_Instr = trap.Instruction('LDM', True)
ldm_Instr.setMachineCode(ls_multiple, {}, 'TODO')
ldm_Instr.setCode(opCode, 'execute')
ldm_Instr.addBehavior(condCheckOp, 'execute')
ldm_Instr.addBehavior(LSM_reglist_Op, 'execute')
isa.addInstruction(ldm_Instr)

# LDR instruction family
# Normal load instruction
opCode = cxx_writer.Code("""
memLastBits = address & 0x00000003;
// if the memory address is not word aligned I have to rotate the loaded value
if(memLastBits == 0)
    value = dateMem.read_word(address);
else{
    value = RotateRight(8*memLastBits, dateMem.read_word(address));
}

//Perform the writeback; as usual I have to behave differently
//if a load a value to the PC
if(rd_bit == 15){
    //I don't consider the 2 less significant bits since I don't bother with
    //thumb mode.
    PC = value & 0xFFFFFFFC;
    stall(4);
}
else{
    rd = value;
    PC += 4;
    stall(2);
}
""")
ldr_imm_Instr = trap.Instruction('LDR_imm', True)
ldr_imm_Instr.setMachineCode(ls_immOff, {'b': [0], 'l': [1]}, 'TODO')
ldr_imm_Instr.setCode(opCode, 'execute')
ldr_imm_Instr.addBehavior(condCheckOp, 'execute')
ldr_imm_Instr.addBehavior(ls_imm_Op, 'execute')
ldr_imm_Instr.addVariable(('memLastBits', 'BIT<32>'))
ldr_imm_Instr.addVariable(('value', 'BIT<32>'))
isa.addInstruction(ldr_imm_Instr)
ldr_off_Instr = trap.Instruction('LDR_off', True)
ldr_off_Instr.setMachineCode(ls_regOff, {'b': [0], 'l': [1]}, 'TODO')
ldr_off_Instr.setCode(opCode, 'execute')
ldr_off_Instr.addBehavior(condCheckOp, 'execute')
ldr_off_Instr.addBehavior(ls_reg_Op, 'execute')
ldr_off_Instr.addVariable(('memLastBits', 'BIT<32>'))
ldr_off_Instr.addVariable(('value', 'BIT<32>'))
isa.addInstruction(ldr_off_Instr)
# LDRB instruction family
# Normal load instruction
opCode = cxx_writer.Code("""
rd = dateMem.read_word(address);
stall(2);
""")
ldrb_imm_Instr = trap.Instruction('LDRB_imm', True)
ldrb_imm_Instr.setMachineCode(ls_immOff, {'b': [1], 'l': [1]}, 'TODO')
ldrb_imm_Instr.setCode(opCode, 'execute')
ldrb_imm_Instr.addBehavior(condCheckOp, 'execute')
ldrb_imm_Instr.addBehavior(ls_imm_Op, 'execute')
ldrb_imm_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(ldrb_imm_Instr)
ldrb_off_Instr = trap.Instruction('LDRB_off', True)
ldrb_off_Instr.setMachineCode(ls_regOff, {'b': [1], 'l': [1]}, 'TODO')
ldrb_off_Instr.setCode(opCode, 'execute')
ldrb_off_Instr.addBehavior(condCheckOp, 'execute')
ldrb_off_Instr.addBehavior(ls_reg_Op, 'execute')
ldrb_off_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(ldrb_off_Instr)
# LDRH instruction family
opCode = cxx_writer.Code("""
rd = dateMem.read_half(address);
stall(2);
""")
ldrh_off_Instr = trap.Instruction('LDRH_off', True)
ldrh_off_Instr.setMachineCode(lsshb_regOff, {'opcode1': [1, 0, 1, 1]}, 'TODO')
ldrh_off_Instr.setCode(opCode, 'execute')
ldrh_off_Instr.addBehavior(condCheckOp, 'execute')
ldrh_off_Instr.addBehavior(ls_sh_Op, 'execute')
ldrh_off_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(ldrh_off_Instr)
# LDRS H/B instruction family
opCode = cxx_writer.Code("""
rd = dateMem.read_half(address);
stall(2);
""")
ldrsh_off_Instr = trap.Instruction('LDRSH_off', True)
ldrsh_off_Instr.setMachineCode(lsshb_regOff, {'opcode1': [1, 1, 1, 1]}, 'TODO')
ldrsh_off_Instr.setCode(opCode, 'execute')
ldrsh_off_Instr.addBehavior(condCheckOp, 'execute')
ldrsh_off_Instr.addBehavior(ls_sh_Op, 'execute')
ldrsh_off_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(ldrsh_off_Instr)
opCode = cxx_writer.Code("""
rd = dateMem.read_byte(address);
stall(2);
""")
ldrsb_off_Instr = trap.Instruction('LDRSB_off', True)
ldrsb_off_Instr.setMachineCode(lsshb_regOff, {'opcode1': [1, 1, 0, 1]}, 'TODO')
ldrsb_off_Instr.setCode(opCode, 'execute')
ldrsb_off_Instr.addBehavior(condCheckOp, 'execute')
ldrsb_off_Instr.addBehavior(ls_sh_Op, 'execute')
ldrsb_off_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(ldrsb_off_Instr)

# Mutiply instruction family
opCode = cxx_writer.Code("""
rd = (int)((rm * rs) + REGS[rn]);

if((rs & 0xFFFFFF00) == 0x0 || (rs & 0xFFFFFF00) == 0xFFFFFF00){
    stall(2);
}
else if((rs & 0xFFFF0000) == 0x0 || (rs & 0xFFFF0000) == 0xFFFF0000){
    stall(3);
}
else if((rs & 0xFF000000) == 0x0 || (rs & 0xFF000000) == 0xFF000000)7
    stall(4);
}
else{
    stall(5);
}
""")
mla_Instr = trap.Instruction('mla_Instr', True)
mla_Instr.setMachineCode(multiply, {'opcode0': [0, 0, 0, 0, 0, 0, 1]}, 'TODO')
mla_Instr.setCode(opCode, 'execute')
mla_Instr.addBehavior(condCheckOp, 'execute')
mla_Instr.addBehavior(UpdatePSRmul, 'execute', False)
mla_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(mla_Instr)

opCode = cxx_writer.Code("""
rd = (int)(rm * rs);

if((rs & 0xFFFFFF00) == 0x0 || (rs & 0xFFFFFF00) == 0xFFFFFF00){
    stall(1);
}
else if((rs & 0xFFFF0000) == 0x0 || (rs & 0xFFFF0000) == 0xFFFF0000){
    stall(2);
}
else if((rs & 0xFF000000) == 0x0 || (rs & 0xFF000000) == 0xFF000000)7
    stall(3);
}
else{
    stall(4);
}
""")
mul_Instr = trap.Instruction('mul_Instr', True)
mul_Instr.setMachineCode(multiply, {'opcode0': [0, 0, 0, 0, 0, 0, 0]}, 'TODO')
mul_Instr.setCode(opCode, 'execute')
mul_Instr.addBehavior(condCheckOp, 'execute')
mul_Instr.addBehavior(UpdatePSRmul, 'execute', False)
mul_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(mul_Instr)

opCode = cxx_writer.Code("""
//Perform the operation
long long result = (long long)(((long long)rm * (long long)rs) + (((long long)rd) << 32) + (long long)REGS[rn]);
//Check if I have to update the processor flags
rd = (unsigned int)(result >> 32);
REGS[rn] = result & 0xFFFFFFFF;

if((rs & 0xFFFFFF00) == 0x0 || (rs & 0xFFFFFF00) == 0xFFFFFF00){
    stall(3);
}
else if((rs & 0xFFFF0000) == 0x0 || (rs & 0xFFFF0000) == 0xFFFF0000){
    stall(4);
}
else if((rs & 0xFF000000) == 0x0 || (rs & 0xFF000000) == 0xFF000000){
    stall(5);
}
else{
    stall(6);
}
""")
smlal_Instr = trap.Instruction('smlal_Instr', True)
smlal_Instr.setMachineCode(multiply, {'opcode0': [0, 0, 0, 0, 1, 1, 1]}, 'TODO')
smlal_Instr.setCode(opCode, 'execute')
smlal_Instr.addBehavior(condCheckOp, 'execute')
smlal_Instr.addBehavior(UpdatePSRmul, 'execute', False)
smlal_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(smlal_Instr)

opCode = cxx_writer.Code("""
//Perform the operation
long long result = (long long)((long long)rm * (long long)rs);
//Check if I have to update the processor flags
rd = (unsigned int)(result >> 32);
REGS[rn] = result & 0xFFFFFFFF;

if((rs & 0xFFFFFF00) == 0x0 || (rs & 0xFFFFFF00) == 0xFFFFFF00){
    stall(3);
}
else if((rs & 0xFFFF0000) == 0x0 || (rs & 0xFFFF0000) == 0xFFFF0000){
    stall(4);
}
else if((rs & 0xFF000000) == 0x0 || (rs & 0xFF000000) == 0xFF000000){
    stall(5);
}
else{
    stall(6);
}
""")
smull_Instr = trap.Instruction('smull_Instr', True)
smull_Instr.setMachineCode(multiply, {'opcode0': [0, 0, 0, 0, 1, 1, 0]}, 'TODO')
smull_Instr.setCode(opCode, 'execute')
smull_Instr.addBehavior(condCheckOp, 'execute')
smull_Instr.addBehavior(UpdatePSRmul, 'execute', False)
smull_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(smull_Instr)

opCode = cxx_writer.Code("""
//Perform the operation
unsigned long long result = (unsigned long long)(((unsigned long long)rm * (unsigned long long)rs) + (((unsigned long long)rd) << 32) + (unsigned long long)REGS[rn]);
//Check if I have to update the processor flags
rd = (unsigned int)(result >> 32);
REGS[rn] = result & 0xFFFFFFFF;

if((rs & 0xFFFFFF00) == 0x0 || (rs & 0xFFFFFF00) == 0xFFFFFF00){
    stall(3);
}
else if((rs & 0xFFFF0000) == 0x0 || (rs & 0xFFFF0000) == 0xFFFF0000){
    stall(4);
}
else if((rs & 0xFF000000) == 0x0 || (rs & 0xFF000000) == 0xFF000000){
    stall(5);
}
else{
    stall(6);
}
""")
umlal_Instr = trap.Instruction('umlal_Instr', True)
umlal_Instr.setMachineCode(multiply, {'opcode0': [0, 0, 0, 0, 1, 0, 1]}, 'TODO')
umlal_Instr.setCode(opCode, 'execute')
umlal_Instr.addBehavior(condCheckOp, 'execute')
umlal_Instr.addBehavior(UpdatePSRmul, 'execute', False)
umlal_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(umlal_Instr)

opCode = cxx_writer.Code("""
//Perform the operation
unsigned long long result = (unsigned long long)((unsigned long long)rm * (unsigned long long)rs);
//Check if I have to update the processor flags
rd = (unsigned int)(result >> 32);
REGS[rn] = result & 0xFFFFFFFF;

if((rs & 0xFFFFFF00) == 0x0 || (rs & 0xFFFFFF00) == 0xFFFFFF00){
    stall(3);
}
else if((rs & 0xFFFF0000) == 0x0 || (rs & 0xFFFF0000) == 0xFFFF0000){
    stall(4);
}
else if((rs & 0xFF000000) == 0x0 || (rs & 0xFF000000) == 0xFF000000){
    stall(5);
}
else{
    stall(6);
}
""")
umull_Instr = trap.Instruction('umull_Instr', True)
umull_Instr.setMachineCode(multiply, {'opcode0': [0, 0, 0, 0, 1, 0, 0]}, 'TODO')
umull_Instr.setCode(opCode, 'execute')
umull_Instr.addBehavior(condCheckOp, 'execute')
umull_Instr.addBehavior(UpdatePSRmul, 'execute', False)
umull_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(umull_Instr)

# MOV instruction family
opCode = cxx_writer.Code("""
rd = operand;
""")
mov_shift_imm_Instr = trap.Instruction('MOV_si', True)
mov_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 1, 0, 1]}, 'TODO')
mov_shift_imm_Instr.setCode(opCode, 'execute')
mov_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
mov_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
mov_shift_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
mov_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
mov_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
isa.addInstruction(mov_shift_imm_Instr)
mov_shift_reg_Instr = trap.Instruction('MOV_sr', True)
mov_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 1, 0, 1]}, 'TODO')
mov_shift_reg_Instr.setCode(opCode, 'execute')
mov_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
mov_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
mov_shift_reg_Instr.addBehavior(UpdatePSRBit, 'execute', False)
mov_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(mov_shift_reg_Instr)
mov_imm_Instr = trap.Instruction('MOV_i', True)
mov_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 1, 0, 1]}, 'TODO')
mov_imm_Instr.setCode(opCode, 'execute')
mov_imm_Instr.addBehavior(condCheckOp, 'execute')
mov_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
mov_imm_Instr.addBehavior(UpdatePSRBit, 'execute', False)
mov_imm_Instr.addBehavior(UpdatePC, 'execute', False)
isa.addInstruction(mov_imm_Instr)

# MRS instruction
opCode = cxx_writer.Code("""
if(r == 1){ // I have to save the SPSR
    switch(CPSR["mode"]){
        case 0x1:{
            //I'm in FIQ mode
            rd = SPSR[0];
            break;}
        case 0x2:{
            //I'm in IRQ mode
            rd = SPSR[1];
            break;}
        case 0x3:{
            //I'm in SVC mode
            rd = SPSR[2];
            break;}
        case 0x7:{
            //I'm in ABT mode
            rd = SPSR[3];
            break;}
        case 0xB:{
            //I'm in UND mode
            rd = SPSR[4];
            break;}
        default:
            break;
    }
}
else{
    // I have to save the CPSR
    rd = CPSR;
}
""")
mrs_Instr = trap.Instruction('mrs_Instr', True)
mrs_Instr.setMachineCode(move_imm2psr, {'opcode0': [0, 0, 0, 1, 0], 'opcode1': [0, 0], 'mask': [1, 1, 1, 1], 'rotate': [0, 0, 0, 0], 'immediate': [0, 0, 0, 0, 0, 0, 0, 0]}, 'TODO')
mrs_Instr.setCode(opCode, 'execute')
mrs_Instr.addBehavior(condCheckOp, 'execute')
mrs_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(mrs_Instr)

# MSR instruction family
opCode = cxx_writer.Code("""
value = RotateRight(rotate*2, immediate);
//Checking for unvalid bits
if((value & 0x00000010) == 0){
    THROW_EXCEPTION("MSR called with unvalid mode " << std::hex << std::showbase << value << ": we are trying to switch to 26 bit PC");
}
unsigned int currentMode = CPSR["mode"];
//Firs of all I check whether I have to modify the CPSR or the SPSR
if(r == 0){
    //CPSR
    //Now I modify the fields; note that in user mode I can just update the flags.
    if((mask & 0x1) != 0 && currentMode != 0){
        CPSR &= 0xFFFFFF00;
        CPSR |= value & 0x000000FF;
        //Now if I change mode I also have to update the registry bank
        if(currentMode != (CPSR & 0x0000000F)){
            restoreSPSR();
        }
    }
    if((mask & 0x2) != 0 && currentMode != 0){
        CPSR &= 0xFFFF00FF;
        CPSR |= value & 0x0000FF00;
    }
    if((mask & 0x4) != 0 && currentMode != 0){
        CPSR &= 0xFF00FFFF;
        CPSR |= value & 0x00FF0000;
    }
    if((mask & 0x8) != 0){
        CPSR &= 0x00FFFFFF;
        CPSR |= value & 0xFF000000;
    }
}
else{
    //SPSR
    switch(currentMode){
        case 0x1:{
            //I'm in FIQ mode
            if((mask & 0x1) != 0){
                SPSR[0] &= 0xFFFFFF00;
                SPSR[0] |= value & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[0] &= 0xFFFF00FF;
                SPSR[0] |= value & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[0] &= 0xFF00FFFF;
                SPSR[0] |= value & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[0] &= 0x00FFFFFF;
                SPSR[0] |= value & 0xFF000000;
            }
            break;}
        case 0x2:{
            //I'm in IRQ mode
            if((mask & 0x1) != 0){
                SPSR[1] &= 0xFFFFFF00;
                SPSR[1] |= value & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[1] &= 0xFFFF00FF;
                SPSR[1] |= value & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[1] &= 0xFF00FFFF;
                SPSR[1] |= value & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[1] &= 0x00FFFFFF;
                SPSR[1] |= value & 0xFF000000;
            }
            break;}
        case 0x3:{
            //I'm in SVC mode
            if((mask & 0x1) != 0){
                SPSR[2] &= 0xFFFFFF00;
                SPSR[2] |= value & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[2] &= 0xFFFF00FF;
                SPSR[2] |= value & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[2] &= 0xFF00FFFF;
                SPSR[2] |= value & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[2] &= 0x00FFFFFF;
                SPSR[2] |= value & 0xFF000000;
            }
            break;}
        case 0x7:{
            //I'm in ABT mode
            if((mask & 0x1) != 0){
                SPSR[3] &= 0xFFFFFF00;
                SPSR[3] |= value & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[3] &= 0xFFFF00FF;
                SPSR[3] |= value & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[3] &= 0xFF00FFFF;
                SPSR[3] |= value & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[3] &= 0x00FFFFFF;
                SPSR[3] |= value & 0xFF000000;
            }
            break;}
        case 0xB:{
            //I'm in UND mode
            if((mask & 0x1) != 0){
                SPSR[4] &= 0xFFFFFF00;
                SPSR[4] |= value & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[4] &= 0xFFFF00FF;
                SPSR[4] |= value & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[4] &= 0xFF00FFFF;
                SPSR[4] |= value & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[4] &= 0x00FFFFFF;
                SPSR[4] |= value & 0xFF000000;
            }
            break;}
        default:
            break;
    }
}
""")
msr_imm_Instr = trap.Instruction('msr_imm_Instr', True)
msr_imm_Instr.setMachineCode(move_imm2psr, {'opcode0': [0, 0, 1, 1, 0], 'opcode1': [1, 0], 'rd': [1, 1, 1, 1]}, 'TODO')
msr_imm_Instr.setCode(opCode, 'execute')
msr_imm_Instr.addBehavior(condCheckOp, 'execute')
msr_imm_Instr.addBehavior(IncrementPC, 'execute', False)
msr_imm_Instr.addVariable(('value', 'BIT<32>'))
isa.addInstruction(msr_imm_Instr)

opCode = cxx_writer.Code("""
//Checking for unvalid bits
if((rm & 0x00000010) == 0){
    THROW_EXCEPTION("MSR called with unvalid mode " << std::hex << std::showbase << value << ": we are trying to switch to 26 bit PC");
}
unsigned int currentMode = CPSR["mode"];
//Firs of all I check whether I have to modify the CPSR or the SPSR
if(r == 0){
    //CPSR
    //Now I modify the fields; note that in user mode I can just update the flags.
    if((mask & 0x1) != 0 && currentMode != 0){
        CPSR &= 0xFFFFFF00;
        CPSR |= rm & 0x000000FF;
        //Now if I change mode I also have to update the registry bank
        if(currentMode != (CPSR & 0x0000000F)){
            restoreSPSR();
        }
    }
    if((mask & 0x2) != 0 && currentMode != 0){
        CPSR &= 0xFFFF00FF;
        CPSR |= rm & 0x0000FF00;
    }
    if((mask & 0x4) != 0 && currentMode != 0){
        CPSR &= 0xFF00FFFF;
        CPSR |= rm & 0x00FF0000;
    }
    if((mask & 0x8) != 0){
        CPSR &= 0x00FFFFFF;
        CPSR |= rm & 0xFF000000;
    }
}
else{
    //SPSR
    switch(currentMode){
        case 0x1:{
            //I'm in FIQ mode
            if((mask & 0x1) != 0){
                SPSR[0] &= 0xFFFFFF00;
                SPSR[0] |= rm & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[0] &= 0xFFFF00FF;
                SPSR[0] |= rm & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[0] &= 0xFF00FFFF;
                SPSR[0] |= rm & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[0] &= 0x00FFFFFF;
                SPSR[0] |= rm & 0xFF000000;
            }
            break;}
        case 0x2:{
            //I'm in IRQ mode
            if((mask & 0x1) != 0){
                SPSR[1] &= 0xFFFFFF00;
                SPSR[1] |= rm & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[1] &= 0xFFFF00FF;
                SPSR[1] |= rm & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[1] &= 0xFF00FFFF;
                SPSR[1] |= rm & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[1] &= 0x00FFFFFF;
                SPSR[1] |= rm & 0xFF000000;
            }
            break;}
        case 0x3:{
            //I'm in SVC mode
            if((mask & 0x1) != 0){
                SPSR[2] &= 0xFFFFFF00;
                SPSR[2] |= rm & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[2] &= 0xFFFF00FF;
                SPSR[2] |= rm & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[2] &= 0xFF00FFFF;
                SPSR[2] |= rm & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[2] &= 0x00FFFFFF;
                SPSR[2] |= rm & 0xFF000000;
            }
            break;}
        case 0x7:{
            //I'm in ABT mode
            if((mask & 0x1) != 0){
                SPSR[3] &= 0xFFFFFF00;
                SPSR[3] |= rm & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[3] &= 0xFFFF00FF;
                SPSR[3] |= rm & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[3] &= 0xFF00FFFF;
                SPSR[3] |= rm & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[3] &= 0x00FFFFFF;
                SPSR[3] |= rm & 0xFF000000;
            }
            break;}
        case 0xB:{
            //I'm in UND mode
            if((mask & 0x1) != 0){
                SPSR[4] &= 0xFFFFFF00;
                SPSR[4] |= rm & 0x000000FF;
            }
            if((mask & 0x2) != 0){
                SPSR[4] &= 0xFFFF00FF;
                SPSR[4] |= rm & 0x0000FF00;
            }
            if((mask & 0x4) != 0){
                SPSR[4] &= 0xFF00FFFF;
                SPSR[4] |= rm & 0x00FF0000;
            }
            if((mask & 0x8) != 0){
                SPSR[4] &= 0x00FFFFFF;
                SPSR[4] |= rm & 0xFF000000;
            }
            break;}
        default:
            break;
    }
}
""")
msr_reg_Instr = trap.Instruction('msr_reg_Instr', True)
msr_reg_Instr.setMachineCode(move_imm2psr_reg, {'opcode0': [0, 0, 0, 1, 0], 'opcode1': [1, 0]}, 'TODO')
msr_reg_Instr.setCode(opCode, 'execute')
msr_reg_Instr.addBehavior(condCheckOp, 'execute')
msr_reg_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(msr_reg_Instr)
