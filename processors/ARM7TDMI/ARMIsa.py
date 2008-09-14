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
cmn_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 0, 1, 1]}, 'TODO')
cmn_shift_imm_Instr.setCode(opCode, 'execute')
cmn_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
cmn_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
cmn_shift_imm_Instr.addBehavior(UpdatePSRSum, 'execute', False)
cmn_shift_imm_Instr.addVariable(('result', 'BIT<64>'))
cmn_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
isa.addInstruction(cmn_shift_imm_Instr)
cmn_shift_reg_Instr = trap.Instruction('CMN_sr', True)
cmn_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 0, 1, 1]}, 'TODO')
cmn_shift_reg_Instr.setCode(opCode, 'execute')
cmn_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
cmn_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
cmn_shift_reg_Instr.addBehavior(UpdatePSRSum, 'execute', False)
cmn_shift_reg_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(cmn_shift_reg_Instr)
cmn_imm_Instr = trap.Instruction('CMN_i', True)
cmn_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 0, 1, 1]}, 'TODO')
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
cmp_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [1, 0, 1, 0]}, 'TODO')
cmp_shift_imm_Instr.setCode(opCode, 'execute')
cmp_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
cmp_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
cmp_shift_imm_Instr.addBehavior(UpdatePSRSub, 'execute', False)
cmp_shift_imm_Instr.addVariable(('result', 'BIT<64>'))
cmp_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
isa.addInstruction(cmp_shift_imm_Instr)
cmp_shift_reg_Instr = trap.Instruction('CMP_sr', True)
cmp_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [1, 0, 1, 0]}, 'TODO')
cmp_shift_reg_Instr.setCode(opCode, 'execute')
cmp_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
cmp_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
cmp_shift_reg_Instr.addBehavior(UpdatePSRSub, 'execute', False)
cmp_shift_reg_Instr.addVariable(('result', 'BIT<64>'))
isa.addInstruction(cmp_shift_reg_Instr)
cmp_imm_Instr = trap.Instruction('CMP_i', True)
cmp_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [1, 0, 1, 0]}, 'TODO')
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
int i = 0;
int modeBits = 0;
int numRegsToLoad = 0;

ls_address = lsm_startaddress;

//First of all I have to check that I'm not dealing with user mode registers:
if((s == 1) && ((rlist & 0x00008000) == 0)){
    //I'm dealing with user-mode registers: LDM type two
    modeBits = PSR.read(0) & 0x0000000F;

    //Load the registers common to all modes
    for(i = 0; i < 8; i++){
        if((rlist & (0x00000001 << i)) != 0) {
            RB.write(i, DATA_MEM.read(ls_address.entire));
            ls_address.entire += 4;
            numRegsToLoad++;
        }
    }

    //Read the User Mode registers.
    for(i = 0; i < 7; i++){
        if((rlist & (0x00000001 << (8 + i))) != 0) {
            BANKED_REGS.write(i, DATA_MEM.read(ls_address.entire));
            ls_address.entire += 4;
            numRegsToLoad++;
        }
    }
}
else{
    //I'm dealing just with the current registers: LDM type one or three
    // First of all if it is necessary I perform the writeback
    if(w != 0){
        RB.write(rn, lsm_wbAddress.entire);
    }

    //First af all I read the memory in the register I in the register list.
    for(i = 0; i < 15; i++){
        if((rlist & (0x00000001 << i)) != 0) {
            RB.write(i, DATA_MEM.read(ls_address.entire));
            ls_address.entire += 4;
            numRegsToLoad++;
        }
    }

    //I tread in a special way the PC, since loading a value in the PC is like performing a branch.
    if((rlist & 0x00008000) != 0){
        //I have to load also the PC: it is like a branch; since I don't bother with
        //Thumb mode, bits 0 and 1 of the PC are ignored
        ac_pc = DATA_MEM.read(ls_address.entire) & 0xFFFFFFFC;
        RB.write(PC, (ac_pc + 4));
        if(s == 1) //LDM type three: in this type of operation I also have to restore the PSR.
            copySPSR();
        numRegsToLoad++;
        setInstrLatency(2);
    }
}
setInstrLatency(numRegsToLoad + 1);
""")
ldm_Instr = trap.Instruction('LDM', True)
ldm_Instr.setMachineCode(ls_multiple, {}, 'TODO')
ldm_Instr.setCode(opCode, 'execute')
ldm_Instr.addBehavior(condCheckOp, 'execute')
ldm_Instr.addBehavior(LSM_reglist_Op, 'execute')
ldm_Instr.addBehavior(IncrementPC, 'execute', False)
isa.addInstruction(ldm_Instr)
