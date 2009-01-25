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
from LEON3Coding import *

# ISA declaration: it is the container for all the single instructions
isa = trap.ISA()

# Now I add to the ISA all the helper methods and operations which will be
# called from the instructions
#isa.addMethod(restoreSPSR_method)

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

## ADC instruction family
#opCode = cxx_writer.Code("""
#rd = (int)rn + (int)operand;
#if (CPSR[key_C]){
    #rd += 1;
#}
#""")
#adc_shift_imm_Instr = trap.Instruction('ADC_si', True, frequency = 5)
#adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
#adc_shift_imm_Instr.setCode(opCode, 'execute')
#adc_shift_imm_Instr.setWriteRegs([])
#adc_shift_imm_Instr.addBehavior(IncrementPC, 'fetch')
#adc_shift_imm_Instr.addBehavior(condCheckOp, 'execute')
#adc_shift_imm_Instr.addBehavior(DPI_shift_imm_Op, 'execute')
#adc_shift_imm_Instr.addBehavior(UpdatePSRSum, 'execute', False)
#adc_shift_imm_Instr.addBehavior(UpdatePC, 'execute', False)
#adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 7})
#adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 7, 'CPSR' : 0x00000000})
#adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
#adc_shift_imm_Instr.addTest({'cond': 0x0, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 0}, {'CPSR' : 0x0, 'REGS[10]': 123, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 123})
#adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 0}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 9})
#adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
#adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 1}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 4})
#adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
#adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 0x80000000}, {'REGS[10]': 2})
#adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 1, 'shift_op': 2}, {'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 4})
#adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 0, 'shift_op': 3}, {'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 0xffffffff}, {'REGS[10]': 3})
#adc_shift_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'shift_amm': 16, 'shift_op': 3}, {'REGS[9]': 3, 'REGS[8]': 0x00020020}, {'REGS[10]': 3 + 0x00200002})
#isa.addInstruction(adc_shift_imm_Instr)
#adc_shift_reg_Instr = trap.Instruction('ADC_sr', True, frequency = 5)
#adc_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
#adc_shift_reg_Instr.setCode(opCode, 'execute')
#adc_shift_reg_Instr.addBehavior(IncrementPC, 'fetch')
#adc_shift_reg_Instr.addBehavior(condCheckOp, 'execute')
#adc_shift_reg_Instr.addBehavior(DPI_reg_shift_Op, 'execute')
#adc_shift_reg_Instr.addBehavior(UpdatePSRSum, 'execute', False)
#adc_shift_reg_Instr.addBehavior(UpdatePC, 'execute', False)
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 1, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'CPSR' : 0x20000000, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 7, 'CPSR' : 0x00000000})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
#adc_shift_reg_Instr.addTest({'cond': 0x0, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 0, 'CPSR' : 0x0, 'REGS[10]': 123, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 123})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 0}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 9})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 4})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 1}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 0, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 1, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 4})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 32, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 3})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 2}, {'REGS[0]': 33, 'REGS[9]': 3, 'REGS[8]': 0x80000000}, {'REGS[10]': 2})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 0x20, 'REGS[9]': 3, 'REGS[8]': 3}, {'REGS[10]': 6})
#adc_shift_reg_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rm': 8, 'rs': 0, 'shift_op': 3}, {'REGS[0]': 16, 'REGS[9]': 3, 'REGS[8]': 0x00020020}, {'REGS[10]': 3 + 0x00200002})
#isa.addInstruction(adc_shift_reg_Instr)
#adc_imm_Instr = trap.Instruction('ADC_i', True, frequency = 5)
#adc_imm_Instr.setMachineCode(dataProc_imm, {'opcode': [0, 1, 0, 1]}, 'TODO')
#adc_imm_Instr.setCode(opCode, 'execute')
#adc_imm_Instr.addBehavior(IncrementPC, 'fetch')
#adc_imm_Instr.addBehavior(condCheckOp, 'execute')
#adc_imm_Instr.addBehavior(DPI_imm_Op, 'execute')
#adc_imm_Instr.addBehavior(UpdatePSRSum, 'execute', False)
#adc_imm_Instr.addBehavior(UpdatePC, 'execute', False)
#adc_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 0, 'immediate': 3}, {'REGS[9]': 3}, {'REGS[10]': 6})
#adc_imm_Instr.addTest({'cond': 0xe, 's': 0, 'rn': 9, 'rd': 10, 'rotate': 0xe, 'immediate': 0x3f}, {'REGS[9]': 3}, {'REGS[10]': 0x3f0 + 3})
#isa.addInstruction(adc_imm_Instr)

