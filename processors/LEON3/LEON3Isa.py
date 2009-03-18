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
from LEON3Coding import *
from LEON3Methods import *

# ISA declaration: it is the container for all the single instructions
isa = trap.ISA()

# Now I add to the ISA all the helper methods and operations which will be
# called from the instructions
isa.addMethod(IncrementRegWindow_method)
isa.addMethod(DecrementRegWindow_method)
isa.addMethod(SignExtend_method)
isa.addMethod(RaiseException_method)

# Now I add some useful definitions to be used inside the instructions; they will be
# inserted as defines in the hpp and file of the instructions
isa.addDefines("""
#define RESET 0
#define DATA_STORE_ERROR 1
#define INSTR_ACCESS_MMU_MISS 2
#define INSTR_ACCESS_ERROR 3
#define R_REGISTER_ACCESS_ERROR 4
#define INSTR_ACCESS_EXC 5
#define PRIVILEDGE_INSTR 6
#define ILLEGAL_INSTR 7
#define FP_DISABLED 8
#define CP_DISABLED 9
#define UNIMPL_FLUSH 10
#define WATCHPOINT_DETECTED 11
#define WINDOW_OVERFLOW 12
#define WINDOW_UNDERFLOW 13
#define MEM_ADDR_NOT_ALIGNED 14
#define FP_EXCEPTION 15
#define CP_EXCEPTION 16
#define DATA_ACCESS_ERROR 17
#define DATA_ACCESS_MMU_MISS 18
#define DATA_ACCESS_EXC 19
#define TAG_OVERFLOW 20
#define DIV_ZERO 21
#define TRAP_INSTRUCTION 22
#define IRQ_LEV_15 23
#define IRQ_LEV_14 24
#define IRQ_LEV_13 25
#define IRQ_LEV_12 26
#define IRQ_LEV_11 27
#define IRQ_LEV_10 28
#define IRQ_LEV_9 29
#define IRQ_LEV_8 30
#define IRQ_LEV_7 31
#define IRQ_LEV_6 32
#define IRQ_LEV_5 33
#define IRQ_LEV_4 34
#define IRQ_LEV_3 35
#define IRQ_LEV_2 36
#define IRQ_LEV_1 37
#define IMPL_DEP_EXC 38
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

opCode = cxx_writer.writer_code.Code("""
""")
# Load Integer Instruction Family
ldsb_imm_Instr = trap.Instruction('LDSB_imm', True, frequency = 5)
ldsb_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 0, 1, 0, 0, 1]}, 'TODO')
ldsb_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
ldsb_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldsb_imm_Instr)
ldsb_reg_Instr = trap.Instruction('LDSB_reg', True, frequency = 5)
ldsb_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 0, 1, 0, 0, 1]}, 'TODO')
ldsb_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
ldsb_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldsb_reg_Instr)
ldsh_imm_Instr = trap.Instruction('LDSH_imm', True, frequency = 5)
ldsh_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 0, 1, 0, 1, 0]}, 'TODO')
ldsh_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
ldsh_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldsh_imm_Instr)
ldsh_reg_Instr = trap.Instruction('LDSH_reg', True, frequency = 5)
ldsh_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 0, 1, 0, 1, 0]}, 'TODO')
ldsh_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
ldsh_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldsh_reg_Instr)
ldub_imm_Instr = trap.Instruction('LDUB_imm', True, frequency = 5)
ldub_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 0, 0, 0, 0, 1]}, 'TODO')
ldub_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
ldub_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldub_imm_Instr)
ldub_reg_Instr = trap.Instruction('LDUB_reg', True, frequency = 5)
ldub_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 0, 0, 0, 0, 1]}, 'TODO')
ldub_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
ldub_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldub_reg_Instr)
lduh_imm_Instr = trap.Instruction('LDUH_imm', True, frequency = 5)
lduh_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 0, 0, 0, 1, 0]}, 'TODO')
lduh_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
lduh_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(lduh_imm_Instr)
lduh_reg_Instr = trap.Instruction('LDUH_reg', True, frequency = 5)
lduh_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 0, 0, 0, 1, 0]}, 'TODO')
lduh_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
lduh_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(lduh_reg_Instr)
ld_imm_Instr = trap.Instruction('LD_imm', True, frequency = 5)
ld_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 0, 0, 0, 0, 0]}, 'TODO')
ld_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
ld_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(ld_imm_Instr)
ld_reg_Instr = trap.Instruction('LD_reg', True, frequency = 5)
ld_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 0, 0, 0, 0, 0]}, 'TODO')
ld_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
ld_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(ld_reg_Instr)
ldd_imm_Instr = trap.Instruction('LDD_imm', True, frequency = 5)
ldd_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 0, 0, 0, 1, 1]}, 'TODO')
ldd_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
ldd_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldd_imm_Instr)
ldd_reg_Instr = trap.Instruction('LDD_reg', True, frequency = 5)
ldd_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 0, 0, 0, 1, 1]}, 'TODO')
ldd_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
ldd_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldd_reg_Instr)
ldsba_imm_Instr = trap.Instruction('LDSBA_imm', True, frequency = 5)
ldsba_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 1, 1, 0, 0, 1]}, 'TODO')
ldsba_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
ldsba_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldsba_imm_Instr)
ldsba_reg_Instr = trap.Instruction('LDSBA_reg', True, frequency = 5)
ldsba_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 1, 1, 0, 0, 1]}, 'TODO')
ldsba_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
ldsba_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldsba_reg_Instr)
ldsha_imm_Instr = trap.Instruction('LDSHA_imm', True, frequency = 5)
ldsha_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 1, 1, 0, 1, 0]}, 'TODO')
ldsha_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
ldsha_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldsha_imm_Instr)
ldsha_reg_Instr = trap.Instruction('LDSHA_reg', True, frequency = 5)
ldsha_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 1, 1, 0, 1, 0]}, 'TODO')
ldsha_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
ldsha_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldsha_reg_Instr)
lduba_imm_Instr = trap.Instruction('LDUBA_imm', True, frequency = 5)
lduba_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 1, 0, 0, 0, 1]}, 'TODO')
lduba_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
lduba_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(lduba_imm_Instr)
lduba_reg_Instr = trap.Instruction('LDUBA_reg', True, frequency = 5)
lduba_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 1, 0, 0, 0, 1]}, 'TODO')
lduba_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
lduba_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(lduba_reg_Instr)
lduha_imm_Instr = trap.Instruction('LDUHA_imm', True, frequency = 5)
lduha_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 1, 0, 0, 1, 0]}, 'TODO')
lduha_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
lduha_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(lduha_imm_Instr)
lduha_reg_Instr = trap.Instruction('LDUHA_reg', True, frequency = 5)
lduha_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 1, 0, 0, 1, 0]}, 'TODO')
lduha_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
lduha_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(lduha_reg_Instr)
lda_imm_Instr = trap.Instruction('LDA_imm', True, frequency = 5)
lda_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 1, 0, 0, 0, 0]}, 'TODO')
lda_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
lda_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(lda_imm_Instr)
lda_reg_Instr = trap.Instruction('LDA_reg', True, frequency = 5)
lda_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 1, 0, 0, 0, 0]}, 'TODO')
lda_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
lda_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(lda_reg_Instr)
ldda_imm_Instr = trap.Instruction('LDDA_imm', True, frequency = 5)
ldda_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 1, 0, 0, 1, 1]}, 'TODO')
ldda_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
ldda_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldda_imm_Instr)
ldda_reg_Instr = trap.Instruction('LDDA_reg', True, frequency = 5)
ldda_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 1, 0, 0, 1, 1]}, 'TODO')
ldda_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
ldda_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldda_reg_Instr)

# Store integer instructions
stb_imm_Instr = trap.Instruction('STB_imm', True, frequency = 5)
stb_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 0, 0, 1, 0, 1]}, 'TODO')
stb_imm_Instr.setVarField('rd', ('REGS', 0), 'in')
stb_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(stb_imm_Instr)
stb_reg_Instr = trap.Instruction('STB_reg', True, frequency = 5)
stb_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 0, 0, 1, 0, 1]}, 'TODO')
stb_reg_Instr.setVarField('rd', ('REGS', 0), 'in')
stb_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(stb_reg_Instr)
sth_imm_Instr = trap.Instruction('STH_imm', True, frequency = 5)
sth_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 0, 0, 1, 1, 0]}, 'TODO')
sth_imm_Instr.setVarField('rd', ('REGS', 0), 'in')
sth_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(sth_imm_Instr)
sth_reg_Instr = trap.Instruction('STH_reg', True, frequency = 5)
sth_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 0, 0, 1, 1, 0]}, 'TODO')
sth_reg_Instr.setVarField('rd', ('REGS', 0), 'in')
sth_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(sth_reg_Instr)
st_imm_Instr = trap.Instruction('ST_imm', True, frequency = 5)
st_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 0, 0, 1, 0, 0]}, 'TODO')
st_imm_Instr.setVarField('rd', ('REGS', 0), 'in')
st_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(st_imm_Instr)
st_reg_Instr = trap.Instruction('ST_reg', True, frequency = 5)
st_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 0, 0, 1, 0, 0]}, 'TODO')
st_reg_Instr.setVarField('rd', ('REGS', 0), 'in')
st_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(st_reg_Instr)
std_imm_Instr = trap.Instruction('STD_imm', True, frequency = 5)
std_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 0, 0, 1, 1, 1]}, 'TODO')
std_imm_Instr.setVarField('rd', ('REGS', 0), 'in')
std_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(std_imm_Instr)
std_reg_Instr = trap.Instruction('STD_reg', True, frequency = 5)
std_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 0, 0, 1, 1, 1]}, 'TODO')
std_reg_Instr.setVarField('rd', ('REGS', 0), 'in')
std_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(std_reg_Instr)
stba_imm_Instr = trap.Instruction('STBA_imm', True, frequency = 5)
stba_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 1, 0, 1, 0, 1]}, 'TODO')
stba_imm_Instr.setVarField('rd', ('REGS', 0), 'in')
stba_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(stba_imm_Instr)
stba_reg_Instr = trap.Instruction('STBA_reg', True, frequency = 5)
stba_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 1, 0, 1, 0, 1]}, 'TODO')
stba_reg_Instr.setVarField('rd', ('REGS', 0), 'in')
stba_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(stba_reg_Instr)
stha_imm_Instr = trap.Instruction('STHA_imm', True, frequency = 5)
stha_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 1, 0, 1, 1, 0]}, 'TODO')
stha_imm_Instr.setVarField('rd', ('REGS', 0), 'in')
stha_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(stha_imm_Instr)
stha_reg_Instr = trap.Instruction('STHA_reg', True, frequency = 5)
stha_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 1, 0, 1, 1, 0]}, 'TODO')
stha_reg_Instr.setVarField('rd', ('REGS', 0), 'in')
stha_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(stha_reg_Instr)
sta_imm_Instr = trap.Instruction('STA_imm', True, frequency = 5)
sta_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 1, 0, 1, 0, 0]}, 'TODO')
sta_imm_Instr.setVarField('rd', ('REGS', 0), 'in')
sta_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(sta_imm_Instr)
sta_reg_Instr = trap.Instruction('STA_reg', True, frequency = 5)
sta_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 1, 0, 1, 0, 0]}, 'TODO')
sta_reg_Instr.setVarField('rd', ('REGS', 0), 'in')
sta_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(sta_reg_Instr)
stda_imm_Instr = trap.Instruction('STDA_imm', True, frequency = 5)
stda_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 1, 0, 1, 1, 1]}, 'TODO')
stda_imm_Instr.setVarField('rd', ('REGS', 0), 'in')
stda_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(stda_imm_Instr)
stda_reg_Instr = trap.Instruction('STDA_reg', True, frequency = 5)
stda_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 1, 0, 1, 1, 1]}, 'TODO')
stda_reg_Instr.setVarField('rd', ('REGS', 0), 'in')
stda_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(stda_reg_Instr)

# Atomic Load/Store
ldstub_imm_Instr = trap.Instruction('LDSTUB_imm', True, frequency = 5)
ldstub_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 0, 1, 1, 0, 1]}, 'TODO')
ldstub_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
ldstub_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldstub_imm_Instr)
ldstub_reg_Instr = trap.Instruction('LDSTUB_reg', True, frequency = 5)
ldstub_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 0, 1, 1, 0, 1]}, 'TODO')
ldstub_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
ldstub_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldstub_reg_Instr)
ldstuba_imm_Instr = trap.Instruction('LDSTUBA_imm', True, frequency = 5)
ldstuba_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 1, 1, 1, 0, 1]}, 'TODO')
ldstuba_imm_Instr.setVarField('rd', ('REGS', 0), 'out')
ldstuba_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldstuba_imm_Instr)
ldstuba_reg_Instr = trap.Instruction('LDSTUBA_reg', True, frequency = 5)
ldstuba_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 1, 1, 1, 0, 1]}, 'TODO')
ldstuba_reg_Instr.setVarField('rd', ('REGS', 0), 'out')
ldstuba_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(ldstuba_reg_Instr)

# Swap
swap_imm_Instr = trap.Instruction('SWAP_imm', True, frequency = 5)
swap_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 0, 1, 1, 1, 1]}, 'TODO')
swap_imm_Instr.setVarField('rd', ('REGS', 0), 'inout')
swap_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(swap_imm_Instr)
swap_reg_Instr = trap.Instruction('SWAP_reg', True, frequency = 5)
swap_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 0, 1, 1, 1, 1]}, 'TODO')
swap_reg_Instr.setVarField('rd', ('REGS', 0), 'inout')
swap_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(swap_reg_Instr)
swapa_imm_Instr = trap.Instruction('SWAPA_imm', True, frequency = 5)
swapa_imm_Instr.setMachineCode(mem_format2, {'op3': [0, 1, 1, 1, 1, 1]}, 'TODO')
swapa_imm_Instr.setVarField('rd', ('REGS', 0), 'inout')
swapa_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(swapa_imm_Instr)
swapa_reg_Instr = trap.Instruction('SWAPA_reg', True, frequency = 5)
swapa_reg_Instr.setMachineCode(mem_format1, {'op3': [0, 1, 1, 1, 1, 1]}, 'TODO')
swapa_reg_Instr.setVarField('rd', ('REGS', 0), 'inout')
swapa_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(swapa_reg_Instr)

# sethi
opCodeExec = cxx_writer.writer_code.Code("""
result = 0xfffffc00 & (imm22 << 10);
""")
sethi_Instr = trap.Instruction('SETHI', True, frequency = 5)
sethi_Instr.setMachineCode(b_sethi_format1, {'op2': [1, 0, 0]}, ('sethi ', '%imm22', 'r ', '%rd'))
sethi_Instr.setCode(opCodeExec, 'execute')
sethi_Instr.addBehavior(WB_plain, 'wb')
sethi_Instr.addBehavior(IncrementPC, 'fetch')
sethi_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(sethi_Instr)

# Logical Instructions
opCodeReadRegs1 = cxx_writer.writer_code.Code("""
rs1_op = rs1;
""")
opCodeReadRegs2 = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = rs2;
""")
opCodeExecImm = cxx_writer.writer_code.Code("""
result = rs1_op & SignExtend(simm13, 13);
""")
and_imm_Instr = trap.Instruction('AND_imm', True, frequency = 5)
and_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 0, 0, 1]}, ('and r', '%rs1', ' ', '%simm13', ' r', '%rd'))
and_imm_Instr.setCode(opCodeExecImm, 'execute')
and_imm_Instr.setCode(opCodeReadRegs1, 'regs')
and_imm_Instr.addBehavior(WB_plain, 'wb')
and_imm_Instr.addBehavior(IncrementPC, 'fetch')
and_imm_Instr.addVariable(('result', 'BIT<32>'))
and_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
isa.addInstruction(and_imm_Instr)
opCodeExecReg = cxx_writer.writer_code.Code("""
result = rs1_op & rs2_op;
""")
and_reg_Instr = trap.Instruction('AND_reg', True, frequency = 5)
and_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 0, 0, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('and r', '%rs1', ' r', '%rs2', ' r', '%rd'))
and_reg_Instr.setCode(opCodeExecReg, 'execute')
and_reg_Instr.setCode(opCodeReadRegs2, 'regs')
and_reg_Instr.addBehavior(WB_plain, 'wb')
and_reg_Instr.addBehavior(IncrementPC, 'fetch')
and_reg_Instr.addVariable(('result', 'BIT<32>'))
and_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
and_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(and_reg_Instr)
andcc_imm_Instr = trap.Instruction('ANDcc_imm', True, frequency = 5)
andcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 0, 0, 1]}, ('andcc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
andcc_imm_Instr.setCode(opCodeExecImm, 'execute')
andcc_imm_Instr.setCode(opCodeReadRegs1, 'regs')
andcc_imm_Instr.addBehavior(WB_icc, 'wb')
andcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
andcc_imm_Instr.addBehavior(ICC_writeLogic, 'execute', False)
andcc_imm_Instr.addVariable(('result', 'BIT<32>'))
andcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
andcc_imm_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(andcc_imm_Instr)
andcc_reg_Instr = trap.Instruction('ANDcc_reg', True, frequency = 5)
andcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 0, 0, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('andcc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
andcc_reg_Instr.setCode(opCodeExecReg, 'execute')
andcc_reg_Instr.setCode(opCodeReadRegs2, 'regs')
andcc_reg_Instr.addBehavior(WB_icc, 'wb')
andcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
andcc_reg_Instr.addBehavior(ICC_writeLogic, 'execute', False)
andcc_reg_Instr.addVariable(('result', 'BIT<32>'))
andcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
andcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
andcc_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(andcc_reg_Instr)
opCodeExecImm = cxx_writer.writer_code.Code("""
result = rs1_op & ~(SignExtend(simm13, 13));
""")
andn_imm_Instr = trap.Instruction('ANDN_imm', True, frequency = 5)
andn_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 1, 0, 1]}, ('andn r', '%rs1', ' ', '%simm13', ' r', '%rd'))
andn_imm_Instr.setCode(opCodeExecImm, 'execute')
andn_imm_Instr.setCode(opCodeReadRegs1, 'regs')
andn_imm_Instr.addBehavior(WB_plain, 'wb')
andn_imm_Instr.addBehavior(IncrementPC, 'fetch')
andn_imm_Instr.addVariable(('result', 'BIT<32>'))
andn_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
isa.addInstruction(andn_imm_Instr)
opCodeExecReg = cxx_writer.writer_code.Code("""
result = rs1_op & ~rs2_op;
""")
andn_reg_Instr = trap.Instruction('ANDN_reg', True, frequency = 5)
andn_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 1, 0, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('andn r', '%rs1', ' r', '%rs2', ' r', '%rd'))
andn_reg_Instr.setCode(opCodeExecReg, 'execute')
andn_reg_Instr.setCode(opCodeReadRegs2, 'regs')
andn_reg_Instr.addBehavior(WB_plain, 'wb')
andn_reg_Instr.addBehavior(IncrementPC, 'fetch')
andn_reg_Instr.addVariable(('result', 'BIT<32>'))
andn_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
andn_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(andn_reg_Instr)
andncc_imm_Instr = trap.Instruction('ANDNcc_imm', True, frequency = 5)
andncc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 1, 0, 1]}, ('andncc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
andncc_imm_Instr.setCode(opCodeExecImm, 'execute')
andncc_imm_Instr.setCode(opCodeReadRegs1, 'regs')
andncc_imm_Instr.addBehavior(WB_icc, 'wb')
andncc_imm_Instr.addBehavior(ICC_writeLogic, 'execute', False)
andncc_imm_Instr.addBehavior(IncrementPC, 'fetch')
andncc_imm_Instr.addVariable(('result', 'BIT<32>'))
andncc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
andncc_imm_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(andncc_imm_Instr)
andncc_reg_Instr = trap.Instruction('ANDNcc_reg', True, frequency = 5)
andncc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 1, 0, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('andncc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
andncc_reg_Instr.setCode(opCodeExecReg, 'execute')
andncc_reg_Instr.setCode(opCodeReadRegs2, 'regs')
andncc_reg_Instr.addBehavior(WB_icc, 'wb')
andncc_reg_Instr.addBehavior(IncrementPC, 'fetch')
andncc_reg_Instr.addBehavior(ICC_writeLogic, 'execute', False)
andncc_reg_Instr.addVariable(('result', 'BIT<32>'))
andncc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
andncc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
andncc_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(andncc_reg_Instr)
opCodeExecImm = cxx_writer.writer_code.Code("""
result = rs1_op | SignExtend(simm13, 13);
""")
or_imm_Instr = trap.Instruction('OR_imm', True, frequency = 5)
or_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 0, 1, 0]}, ('or r', '%rs1', ' ', '%simm13', ' r', '%rd'))
or_imm_Instr.setCode(opCodeExecImm, 'execute')
or_imm_Instr.setCode(opCodeReadRegs1, 'regs')
or_imm_Instr.addBehavior(WB_plain, 'wb')
or_imm_Instr.addBehavior(IncrementPC, 'fetch')
or_imm_Instr.addVariable(('result', 'BIT<32>'))
or_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
isa.addInstruction(or_imm_Instr)
opCodeExecReg = cxx_writer.writer_code.Code("""
result = rs1_op | rs2_op;
""")
or_reg_Instr = trap.Instruction('OR_reg', True, frequency = 5)
or_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 0, 1, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('or r', '%rs1', ' r', '%rs2', ' r', '%rd'))
or_reg_Instr.setCode(opCodeExecReg, 'execute')
or_reg_Instr.setCode(opCodeReadRegs2, 'regs')
or_reg_Instr.addBehavior(WB_plain, 'wb')
or_reg_Instr.addBehavior(IncrementPC, 'fetch')
or_reg_Instr.addVariable(('result', 'BIT<32>'))
or_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
or_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(or_reg_Instr)
orcc_imm_Instr = trap.Instruction('ORcc_imm', True, frequency = 5)
orcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 0, 1, 0]}, ('orcc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
orcc_imm_Instr.setCode(opCodeExecImm, 'execute')
orcc_imm_Instr.setCode(opCodeReadRegs1, 'regs')
orcc_imm_Instr.addBehavior(WB_icc, 'wb')
orcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
orcc_imm_Instr.addBehavior(ICC_writeLogic, 'execute', False)
orcc_imm_Instr.addVariable(('result', 'BIT<32>'))
orcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
orcc_imm_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(orcc_imm_Instr)
orcc_reg_Instr = trap.Instruction('ORcc_reg', True, frequency = 5)
orcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 0, 1, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('orcc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
orcc_reg_Instr.setCode(opCodeExecReg, 'execute')
orcc_reg_Instr.setCode(opCodeReadRegs2, 'regs')
orcc_reg_Instr.addBehavior(WB_icc, 'wb')
orcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
orcc_reg_Instr.addBehavior(ICC_writeLogic, 'execute', False)
orcc_reg_Instr.addVariable(('result', 'BIT<32>'))
orcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
orcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
orcc_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(orcc_reg_Instr)
opCodeExecImm = cxx_writer.writer_code.Code("""
result = rs1_op | ~(SignExtend(simm13, 13));
""")
orn_imm_Instr = trap.Instruction('ORN_imm', True, frequency = 5)
orn_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 1, 1, 0]}, ('orn r', '%rs1', ' ', '%simm13', ' r', '%rd'))
orn_imm_Instr.setCode(opCodeExecImm, 'execute')
orn_imm_Instr.setCode(opCodeReadRegs1, 'regs')
orn_imm_Instr.addBehavior(WB_plain, 'wb')
orn_imm_Instr.addBehavior(IncrementPC, 'fetch')
orn_imm_Instr.addVariable(('result', 'BIT<32>'))
orn_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
isa.addInstruction(orn_imm_Instr)
opCodeExecReg = cxx_writer.writer_code.Code("""
result = rs1_op | ~rs2_op;
""")
orn_reg_Instr = trap.Instruction('ORN_reg', True, frequency = 5)
orn_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 1, 1, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('orn r', '%rs1', ' r', '%rs2', ' r', '%rd'))
orn_reg_Instr.setCode(opCodeExecReg, 'execute')
orn_reg_Instr.setCode(opCodeReadRegs2, 'regs')
orn_reg_Instr.addBehavior(WB_plain, 'wb')
orn_reg_Instr.addBehavior(IncrementPC, 'fetch')
orn_reg_Instr.addVariable(('result', 'BIT<32>'))
orn_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
orn_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(orn_reg_Instr)
orncc_imm_Instr = trap.Instruction('ORNcc_imm', True, frequency = 5)
orncc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 1, 1, 0]}, ('orncc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
orncc_imm_Instr.setCode(opCodeExecImm, 'execute')
orncc_imm_Instr.setCode(opCodeReadRegs1, 'regs')
orncc_imm_Instr.addBehavior(WB_icc, 'wb')
orncc_imm_Instr.addBehavior(IncrementPC, 'fetch')
orncc_imm_Instr.addBehavior(ICC_writeLogic, 'execute', False)
orncc_imm_Instr.addVariable(('result', 'BIT<32>'))
orncc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
isa.addInstruction(orncc_imm_Instr)
orncc_reg_Instr = trap.Instruction('ORNcc_reg', True, frequency = 5)
orncc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 1, 1, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('orncc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
orncc_reg_Instr.setCode(opCodeExecReg, 'execute')
orncc_reg_Instr.setCode(opCodeReadRegs2, 'regs')
orncc_reg_Instr.addBehavior(WB_icc, 'wb')
orncc_reg_Instr.addBehavior(IncrementPC, 'fetch')
orncc_reg_Instr.addBehavior(ICC_writeLogic, 'execute', False)
orncc_reg_Instr.addVariable(('result', 'BIT<32>'))
orncc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
orncc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
orncc_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(orncc_reg_Instr)
opCodeExecImm = cxx_writer.writer_code.Code("""
result = rs1_op ^ SignExtend(simm13, 13);
""")
xor_imm_Instr = trap.Instruction('XOR_imm', True, frequency = 5)
xor_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 0, 1, 1]}, ('xor r', '%rs1', ' ', '%simm13', ' r', '%rd'))
xor_imm_Instr.setCode(opCodeExecImm, 'execute')
xor_imm_Instr.setCode(opCodeReadRegs1, 'regs')
xor_imm_Instr.addBehavior(WB_plain, 'wb')
xor_imm_Instr.addBehavior(IncrementPC, 'fetch')
xor_imm_Instr.addVariable(('result', 'BIT<32>'))
xor_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
isa.addInstruction(xor_imm_Instr)
opCodeExecReg = cxx_writer.writer_code.Code("""
result = rs1_op ^ rs2_op;
""")
xor_reg_Instr = trap.Instruction('XOR_reg', True, frequency = 5)
xor_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 0, 1, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('xor r', '%rs1', ' r', '%rs2', ' r', '%rd'))
xor_reg_Instr.setCode(opCodeExecReg, 'execute')
xor_reg_Instr.setCode(opCodeReadRegs2, 'regs')
xor_reg_Instr.addBehavior(WB_plain, 'wb')
xor_reg_Instr.addBehavior(IncrementPC, 'fetch')
xor_reg_Instr.addVariable(('result', 'BIT<32>'))
xor_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
xor_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(xor_reg_Instr)
xorcc_imm_Instr = trap.Instruction('XORcc_imm', True, frequency = 5)
xorcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 0, 1, 1]}, ('xorcc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
xorcc_imm_Instr.setCode(opCodeExecImm, 'execute')
xorcc_imm_Instr.setCode(opCodeReadRegs1, 'regs')
xorcc_imm_Instr.addBehavior(WB_icc, 'wb')
xorcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
xorcc_imm_Instr.addBehavior(ICC_writeLogic, 'execute', False)
xorcc_imm_Instr.addVariable(('result', 'BIT<32>'))
xorcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
xorcc_imm_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(xorcc_imm_Instr)
xorcc_reg_Instr = trap.Instruction('XORcc_reg', True, frequency = 5)
xorcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 0, 1, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('xorcc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
xorcc_reg_Instr.setCode(opCodeExecReg, 'execute')
xorcc_reg_Instr.setCode(opCodeReadRegs2, 'regs')
xorcc_reg_Instr.addBehavior(WB_icc, 'wb')
xorcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
xorcc_reg_Instr.addBehavior(ICC_writeLogic, 'execute', False)
xorcc_reg_Instr.addVariable(('result', 'BIT<32>'))
xorcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
xorcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
xorcc_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(xorcc_reg_Instr)
opCodeExecImm = cxx_writer.writer_code.Code("""
result = rs1_op ^ ~(SignExtend(simm13, 13));
""")
xnor_imm_Instr = trap.Instruction('XNOR_imm', True, frequency = 5)
xnor_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 1, 1, 1]}, ('xnor r', '%rs1', ' ', '%simm13', ' r', '%rd'))
xnor_imm_Instr.setCode(opCodeExecImm, 'execute')
xnor_imm_Instr.setCode(opCodeReadRegs1, 'regs')
xnor_imm_Instr.addBehavior(WB_plain, 'wb')
xnor_imm_Instr.addBehavior(IncrementPC, 'fetch')
xnor_imm_Instr.addVariable(('result', 'BIT<32>'))
xnor_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
isa.addInstruction(xnor_imm_Instr)
opCodeExecReg = cxx_writer.writer_code.Code("""
result = rs1_op ^ ~rs2_op;
""")
xnor_reg_Instr = trap.Instruction('XNOR_reg', True, frequency = 5)
xnor_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 1, 1, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('xnor r', '%rs1', ' r', '%rs2', ' r', '%rd'))
xnor_reg_Instr.setCode(opCodeExecReg, 'execute')
xnor_reg_Instr.setCode(opCodeReadRegs2, 'regs')
xnor_reg_Instr.addBehavior(WB_plain, 'wb')
xnor_reg_Instr.addBehavior(IncrementPC, 'fetch')
xnor_reg_Instr.addVariable(('result', 'BIT<32>'))
xnor_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
xnor_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(xnor_reg_Instr)
xnorcc_imm_Instr = trap.Instruction('XNORcc_imm', True, frequency = 5)
xnorcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 1, 1, 1]}, ('xnorcc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
xnorcc_imm_Instr.setCode(opCodeExecImm, 'execute')
xnorcc_imm_Instr.setCode(opCodeReadRegs1, 'regs')
xnorcc_imm_Instr.addBehavior(WB_icc, 'wb')
xnorcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
xnorcc_imm_Instr.addBehavior(ICC_writeLogic, 'execute', False)
xnorcc_imm_Instr.addVariable(('result', 'BIT<32>'))
xnorcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
xnorcc_imm_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(xnorcc_imm_Instr)
xnorcc_reg_Instr = trap.Instruction('XNORcc_reg', True, frequency = 5)
xnorcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 1, 1, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('xnorcc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
xnorcc_reg_Instr.setCode(opCodeExecReg, 'execute')
xnorcc_reg_Instr.setCode(opCodeReadRegs2, 'regs')
xnorcc_reg_Instr.addBehavior(WB_icc, 'wb')
xnorcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
xnorcc_reg_Instr.addBehavior(ICC_writeLogic, 'execute', False)
xnorcc_reg_Instr.addVariable(('result', 'BIT<32>'))
xnorcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
xnorcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
xnorcc_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(xnorcc_reg_Instr)

# Shift
opCodeRegsImm = cxx_writer.writer_code.Code("""
rs1_op = rs1;
""")
opCodeRegsRegs = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = rs2;
""")
opCodeExec = cxx_writer.writer_code.Code("""
result = rs1_op << simm13;
""")
sll_imm_Instr = trap.Instruction('SLL_imm', True, frequency = 5)
sll_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 0, 0, 1, 0, 1]}, ('sll r', '%rs1', ' ', '%simm13', ' r', '%rd'))
sll_imm_Instr.setCode(opCodeExec, 'execute')
sll_imm_Instr.setCode(opCodeRegsImm, 'regs')
sll_imm_Instr.addBehavior(WB_plain, 'wb')
sll_imm_Instr.addVariable(('result', 'BIT<32>'))
sll_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
isa.addInstruction(sll_imm_Instr)
opCodeExec = cxx_writer.writer_code.Code("""
result = rs1_op << (rs2_op & 0x0000001f);
""")
sll_reg_Instr = trap.Instruction('SLL_reg', True, frequency = 5)
sll_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 0, 0, 1, 0, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('sll r', '%rs1', ' r', '%rs2', ' r', '%rd'))
sll_reg_Instr.setCode(opCodeExec, 'execute')
sll_reg_Instr.setCode(opCodeRegsRegs, 'regs')
sll_reg_Instr.addBehavior(WB_plain, 'wb')
sll_reg_Instr.addVariable(('result', 'BIT<32>'))
sll_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
sll_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(sll_reg_Instr)
opCodeExec = cxx_writer.writer_code.Code("""
result = ((unsigned int)rs1_op) >> simm13;
""")
srl_imm_Instr = trap.Instruction('SRL_imm', True, frequency = 5)
srl_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 0, 0, 1, 1, 0]}, ('srl r', '%rs1', ' ', '%simm13', ' r', '%rd'))
srl_imm_Instr.setCode(opCodeExec, 'execute')
srl_imm_Instr.setCode(opCodeRegsImm, 'regs')
srl_imm_Instr.addBehavior(WB_plain, 'wb')
srl_imm_Instr.addVariable(('result', 'BIT<32>'))
srl_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
isa.addInstruction(srl_imm_Instr)
opCodeExec = cxx_writer.writer_code.Code("""
result = ((unsigned int)rs1_op) >> (rs2_op & 0x0000001f);
""")
srl_reg_Instr = trap.Instruction('SRL_reg', True, frequency = 5)
srl_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 0, 0, 1, 1, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('srl r', '%rs1', ' r', '%rs2', ' r', '%rd'))
srl_reg_Instr.setCode(opCodeExec, 'execute')
srl_reg_Instr.setCode(opCodeRegsRegs, 'regs')
srl_reg_Instr.addBehavior(WB_plain, 'wb')
srl_reg_Instr.addVariable(('result', 'BIT<32>'))
srl_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
srl_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(srl_reg_Instr)
opCodeExec = cxx_writer.writer_code.Code("""
result = ((int)rs1_op) >> simm13;
""")
sra_imm_Instr = trap.Instruction('SRA_imm', True, frequency = 5)
sra_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 0, 0, 1, 1, 1]}, ('sra r', '%rs1', ' ', '%simm13', ' r', '%rd'))
sra_imm_Instr.setCode(opCodeExec, 'execute')
sra_imm_Instr.setCode(opCodeRegsImm, 'regs')
sra_imm_Instr.addBehavior(WB_plain, 'wb')
sra_imm_Instr.addVariable(('result', 'BIT<32>'))
sra_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
isa.addInstruction(sra_imm_Instr)
opCodeExec = cxx_writer.writer_code.Code("""
result = ((int)rs1_op) >> (rs2_op & 0x0000001f);
""")
sra_reg_Instr = trap.Instruction('SRA_reg', True, frequency = 5)
sra_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 0, 0, 1, 1, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('sra r', '%rs1', ' r', '%rs2', ' r', '%rd'))
sra_reg_Instr.setCode(opCodeExec, 'execute')
sra_reg_Instr.setCode(opCodeRegsRegs, 'regs')
sra_reg_Instr.addBehavior(WB_plain, 'wb')
sra_reg_Instr.addVariable(('result', 'BIT<32>'))
sra_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
sra_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(sra_reg_Instr)

# Add instruction
opCodeRegsImm = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = SignExtend(simm13, 13);
""")
opCodeRegsRegs = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = rs2;
""")
opCodeExec = cxx_writer.writer_code.Code("""
result = rs1_op + rs2_op;
""")
add_imm_Instr = trap.Instruction('ADD_imm', True, frequency = 5)
add_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 0, 0, 0]}, ('add r', '%rs1', ' ', '%simm13', ' r', '%rd'))
add_imm_Instr.setCode(opCodeRegsImm, 'regs')
add_imm_Instr.setCode(opCodeExec, 'execute')
add_imm_Instr.addBehavior(WB_plain, 'wb')
add_imm_Instr.addBehavior(IncrementPC, 'fetch')
add_imm_Instr.addVariable(('result', 'BIT<32>'))
add_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
add_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(add_imm_Instr)
add_reg_Instr = trap.Instruction('ADD_reg', True, frequency = 5)
add_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 0, 0, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('add r', '%rs1', ' r', '%rs2', ' r', '%rd'))
add_reg_Instr.setCode(opCodeRegsRegs, 'regs')
add_reg_Instr.setCode(opCodeExec, 'execute')
add_reg_Instr.addBehavior(WB_plain, 'wb')
add_reg_Instr.addBehavior(IncrementPC, 'fetch')
add_reg_Instr.addVariable(('result', 'BIT<32>'))
add_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
add_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(add_reg_Instr)
addcc_imm_Instr = trap.Instruction('ADDcc_imm', True, frequency = 5)
addcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 0, 0, 0]}, ('addcc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
addcc_imm_Instr.setCode(opCodeRegsImm, 'regs')
addcc_imm_Instr.setCode(opCodeExec, 'execute')
addcc_imm_Instr.addBehavior(WB_icc, 'wb')
addcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
addcc_imm_Instr.addBehavior(ICC_writeAdd, 'execute', False)
addcc_imm_Instr.addVariable(('result', 'BIT<32>'))
addcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
addcc_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
addcc_imm_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(addcc_imm_Instr)
addcc_reg_Instr = trap.Instruction('ADDcc_reg', True, frequency = 5)
addcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 0, 0, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('addcc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
addcc_reg_Instr.setCode(opCodeRegsRegs, 'regs')
addcc_reg_Instr.setCode(opCodeExec, 'execute')
addcc_reg_Instr.addBehavior(WB_icc, 'wb')
addcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
addcc_reg_Instr.addBehavior(ICC_writeAdd, 'execute', False)
addcc_reg_Instr.addVariable(('result', 'BIT<32>'))
addcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
addcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
addcc_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(addcc_reg_Instr)
opCodeExec = cxx_writer.writer_code.Code("""
result = rs1_op + rs2_op + PSRbp[key_ICC_c];
""")
addx_imm_Instr = trap.Instruction('ADDX_imm', True, frequency = 5)
addx_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 1, 0, 0, 0]}, ('addx r', '%rs1', ' ', '%simm13', ' r', '%rd'))
addx_imm_Instr.setCode(opCodeRegsImm, 'regs')
addx_imm_Instr.setCode(opCodeExec, 'execute')
addx_imm_Instr.addBehavior(WB_plain, 'wb')
addx_imm_Instr.addBehavior(IncrementPC, 'fetch')
addx_imm_Instr.addVariable(('result', 'BIT<32>'))
addx_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
addx_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
addx_imm_Instr.addSpecialRegister('PSRbp', 'in')
isa.addInstruction(addx_imm_Instr)
addx_reg_Instr = trap.Instruction('ADDX_reg', True, frequency = 5)
addx_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 1, 0, 0, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('addx r', '%rs1', ' r', '%rs2', ' r', '%rd'))
addx_reg_Instr.setCode(opCodeRegsRegs, 'regs')
addx_reg_Instr.setCode(opCodeExec, 'execute')
addx_reg_Instr.addBehavior(WB_plain, 'wb')
addx_reg_Instr.addBehavior(IncrementPC, 'fetch')
addx_reg_Instr.addVariable(('result', 'BIT<32>'))
addx_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
addx_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
addx_reg_Instr.addSpecialRegister('PSRbp', 'in')
isa.addInstruction(addx_reg_Instr)
addxcc_imm_Instr = trap.Instruction('ADDXcc_imm', True, frequency = 5)
addxcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 1, 0, 0, 0]}, ('addxcc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
addxcc_imm_Instr.setCode(opCodeRegsImm, 'regs')
addxcc_imm_Instr.setCode(opCodeExec, 'execute')
addxcc_imm_Instr.addBehavior(WB_icc, 'wb')
addxcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
addxcc_imm_Instr.addBehavior(ICC_writeAdd, 'execute', False)
addxcc_imm_Instr.addVariable(('result', 'BIT<32>'))
addxcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
addxcc_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
addxcc_imm_Instr.addSpecialRegister('PSRbp', 'inout')
isa.addInstruction(addxcc_imm_Instr)
addxcc_reg_Instr = trap.Instruction('ADDXcc_reg', True, frequency = 5)
addxcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 1, 0, 0, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('addxcc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
addxcc_reg_Instr.setCode(opCodeRegsRegs, 'regs')
addxcc_reg_Instr.setCode(opCodeExec, 'execute')
addxcc_reg_Instr.addBehavior(WB_icc, 'wb')
addxcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
addxcc_reg_Instr.addBehavior(ICC_writeAdd, 'execute', False)
addxcc_reg_Instr.addVariable(('result', 'BIT<32>'))
addxcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
addxcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
addxcc_reg_Instr.addSpecialRegister('PSRbp', 'inout')
isa.addInstruction(addxcc_reg_Instr)
opCodeExec = cxx_writer.writer_code.Code("""
result = rs1_op + rs2_op;
temp_V = ((unsigned int)((rs1_op & rs2_op & (~result)) | ((~rs1_op) & (~rs2_op) & result))) >> 31;
if(!temp_V && (((rs1_op | rs2_op) & 0x00000003) != 0)){
    temp_V = 1;
}
""")
taddcc_imm_Instr = trap.Instruction('TADDcc_imm', True, frequency = 5)
taddcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 0, 0, 0, 0, 0]}, ('taddcc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
taddcc_imm_Instr.setCode(opCodeRegsImm, 'regs')
taddcc_imm_Instr.setCode(opCodeExec, 'execute')
taddcc_imm_Instr.addBehavior(WB_icc, 'wb')
taddcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
taddcc_imm_Instr.addBehavior(ICC_writeTAdd, 'execute', False)
taddcc_imm_Instr.addVariable(('result', 'BIT<32>'))
taddcc_imm_Instr.addVariable(('temp_V', 'BIT<1>'))
taddcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
taddcc_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
taddcc_imm_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(taddcc_imm_Instr)
taddcc_reg_Instr = trap.Instruction('TADDcc_reg', True, frequency = 5)
taddcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 0, 0, 0, 0, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('taddcc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
taddcc_reg_Instr.setCode(opCodeRegsRegs, 'regs')
taddcc_reg_Instr.setCode(opCodeExec, 'execute')
taddcc_reg_Instr.addBehavior(WB_icc, 'wb')
taddcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
taddcc_reg_Instr.addBehavior(ICC_writeTAdd, 'execute', False)
taddcc_reg_Instr.addVariable(('result', 'BIT<32>'))
taddcc_reg_Instr.addVariable(('temp_V', 'BIT<1>'))
taddcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
taddcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
taddcc_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(taddcc_reg_Instr)
opCodeTrap = cxx_writer.writer_code.Code("""
if(temp_V){
    RaiseException(TAG_OVERFLOW);
}
""")
taddcctv_imm_Instr = trap.Instruction('TADDccTV_imm', True, frequency = 5)
taddcctv_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 0, 0, 0, 1, 0]}, ('taddcctv r', '%rs1', ' ', '%simm13', ' r', '%rd'))
taddcctv_imm_Instr.setCode(opCodeRegsImm, 'regs')
taddcctv_imm_Instr.setCode(opCodeExec, 'execute')
taddcctv_imm_Instr.setCode(opCodeTrap, 'exception')
taddcctv_imm_Instr.addBehavior(WB_icctv, 'wb')
taddcctv_imm_Instr.addBehavior(IncrementPC, 'fetch')
taddcctv_imm_Instr.addBehavior(ICC_writeTVAdd, 'execute', False)
taddcctv_imm_Instr.addVariable(('result', 'BIT<32>'))
taddcctv_imm_Instr.addVariable(('temp_V', 'BIT<1>'))
taddcctv_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
taddcctv_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
taddcctv_imm_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(taddcctv_imm_Instr)
taddcctv_reg_Instr = trap.Instruction('TADDccTV_reg', True, frequency = 5)
taddcctv_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 0, 0, 0, 1, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('taddcctv r', '%rs1', ' r', '%rs2', ' r', '%rd'))
taddcctv_reg_Instr.setCode(opCodeRegsRegs, 'regs')
taddcctv_reg_Instr.setCode(opCodeExec, 'execute')
taddcctv_reg_Instr.setCode(opCodeTrap, 'exception')
taddcctv_reg_Instr.addBehavior(WB_icctv, 'wb')
taddcctv_reg_Instr.addBehavior(IncrementPC, 'fetch')
taddcctv_reg_Instr.addBehavior(ICC_writeTVAdd, 'execute', False)
taddcctv_reg_Instr.addVariable(('result', 'BIT<32>'))
taddcctv_reg_Instr.addVariable(('temp_V', 'BIT<1>'))
taddcctv_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
taddcctv_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
taddcctv_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(taddcctv_reg_Instr)

# Subtract
opCodeRegsImm = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = SignExtend(simm13, 13);
""")
opCodeRegsRegs = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = rs2;
""")
opCodeExec = cxx_writer.writer_code.Code("""
result = rs1_op - rs2_op;
""")
sub_imm_Instr = trap.Instruction('SUB_imm', True, frequency = 5)
sub_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 1, 0, 0]}, ('sub r', '%rs1', ' ', '%simm13', ' r', '%rd'))
sub_imm_Instr.setCode(opCodeRegsImm, 'regs')
sub_imm_Instr.setCode(opCodeExec, 'execute')
sub_imm_Instr.addBehavior(WB_plain, 'wb')
sub_imm_Instr.addBehavior(IncrementPC, 'fetch')
sub_imm_Instr.addVariable(('result', 'BIT<32>'))
sub_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
sub_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(sub_imm_Instr)
sub_reg_Instr = trap.Instruction('SUB_reg', True, frequency = 5)
sub_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 1, 0, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('sub r', '%rs1', ' r', '%rs2', ' r', '%rd'))
sub_reg_Instr.setCode(opCodeRegsRegs, 'regs')
sub_reg_Instr.setCode(opCodeExec, 'execute')
sub_reg_Instr.addBehavior(WB_plain, 'wb')
sub_reg_Instr.addBehavior(IncrementPC, 'fetch')
sub_reg_Instr.addVariable(('result', 'BIT<32>'))
sub_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
sub_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(sub_reg_Instr)
subcc_imm_Instr = trap.Instruction('SUBcc_imm', True, frequency = 5)
subcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 1, 0, 0]}, ('subcc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
subcc_imm_Instr.setCode(opCodeRegsImm, 'regs')
subcc_imm_Instr.setCode(opCodeExec, 'execute')
subcc_imm_Instr.addBehavior(WB_icc, 'wb')
subcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
subcc_imm_Instr.addBehavior(ICC_writeSub, 'execute', False)
subcc_imm_Instr.addVariable(('result', 'BIT<32>'))
subcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
subcc_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
subcc_imm_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(subcc_imm_Instr)
subcc_reg_Instr = trap.Instruction('SUBcc_reg', True, frequency = 5)
subcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 1, 0, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('subcc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
subcc_reg_Instr.setCode(opCodeRegsRegs, 'regs')
subcc_reg_Instr.setCode(opCodeExec, 'execute')
subcc_reg_Instr.addBehavior(WB_icc, 'wb')
subcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
subcc_reg_Instr.addBehavior(ICC_writeSub, 'execute', False)
subcc_reg_Instr.addVariable(('result', 'BIT<32>'))
subcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
subcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
subcc_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(subcc_reg_Instr)
opCodeExec = cxx_writer.writer_code.Code("""
result = rs1_op - rs2_op - PSRbp[key_ICC_c];
""")
subx_imm_Instr = trap.Instruction('SUBX_imm', True, frequency = 5)
subx_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 1, 1, 0, 0]}, ('subx r', '%rs1', ' ', '%simm13', ' r', '%rd'))
subx_imm_Instr.setCode(opCodeRegsImm, 'regs')
subx_imm_Instr.setCode(opCodeExec, 'execute')
subx_imm_Instr.addBehavior(WB_plain, 'wb')
subx_imm_Instr.addBehavior(IncrementPC, 'fetch')
subx_imm_Instr.addVariable(('result', 'BIT<32>'))
subx_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
subx_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
subx_imm_Instr.addSpecialRegister('PSRbp', 'in')
isa.addInstruction(subx_imm_Instr)
subx_reg_Instr = trap.Instruction('SUBX_reg', True, frequency = 5)
subx_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 1, 1, 0, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('subx r', '%rs1', ' r', '%rs2', ' r', '%rd'))
subx_reg_Instr.setCode(opCodeRegsRegs, 'regs')
subx_reg_Instr.setCode(opCodeExec, 'execute')
subx_reg_Instr.addBehavior(WB_plain, 'wb')
subx_reg_Instr.addBehavior(IncrementPC, 'fetch')
subx_reg_Instr.addVariable(('result', 'BIT<32>'))
subx_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
subx_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
subx_reg_Instr.addSpecialRegister('PSRbp', 'in')
isa.addInstruction(subx_reg_Instr)
subxcc_imm_Instr = trap.Instruction('SUBXcc_imm', True, frequency = 5)
subxcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 1, 1, 0, 0]}, ('subxcc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
subxcc_imm_Instr.setCode(opCodeRegsImm, 'regs')
subxcc_imm_Instr.setCode(opCodeExec, 'execute')
subxcc_imm_Instr.addBehavior(WB_icc, 'wb')
subxcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
subxcc_imm_Instr.addBehavior(ICC_writeSub, 'execute', False)
subxcc_imm_Instr.addVariable(('result', 'BIT<32>'))
subxcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
subxcc_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
subxcc_imm_Instr.addSpecialRegister('PSRbp', 'inout')
isa.addInstruction(subxcc_imm_Instr)
subxcc_reg_Instr = trap.Instruction('SUBXcc_reg', True, frequency = 5)
subxcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 1, 1, 0, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('subxcc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
subxcc_reg_Instr.setCode(opCodeRegsRegs, 'regs')
subxcc_reg_Instr.setCode(opCodeExec, 'execute')
subxcc_reg_Instr.addBehavior(WB_icc, 'wb')
subxcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
subxcc_reg_Instr.addBehavior(ICC_writeSub, 'execute', False)
subxcc_reg_Instr.addVariable(('result', 'BIT<32>'))
subxcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
subxcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
subxcc_reg_Instr.addSpecialRegister('PSRbp', 'inout')
isa.addInstruction(subxcc_reg_Instr)
opCodeExec = cxx_writer.writer_code.Code("""
result = rs1_op - rs2_op;
temp_V = ((unsigned int)((rs1_op & (~rs2_op) & (~result)) | ((~rs1_op) & rs2_op & result))) >> 31;
if(!temp_V && (((rs1_op | rs2_op) & 0x00000003) != 0)){
    temp_V = 1;
}
""")
tsubcc_imm_Instr = trap.Instruction('TSUBcc_imm', True, frequency = 5)
tsubcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 0, 0, 0, 0, 1]}, ('tsubcc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
tsubcc_imm_Instr.setCode(opCodeRegsImm, 'regs')
tsubcc_imm_Instr.setCode(opCodeExec, 'execute')
tsubcc_imm_Instr.addBehavior(WB_icc, 'wb')
tsubcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
tsubcc_imm_Instr.addBehavior(ICC_writeTSub, 'execute', False)
tsubcc_imm_Instr.addVariable(('result', 'BIT<32>'))
tsubcc_imm_Instr.addVariable(('temp_V', 'BIT<1>'))
tsubcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
tsubcc_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
tsubcc_imm_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(tsubcc_imm_Instr)
tsubcc_reg_Instr = trap.Instruction('TSUBcc_reg', True, frequency = 5)
tsubcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 0, 0, 0, 0, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('tsubcc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
tsubcc_reg_Instr.setCode(opCodeRegsRegs, 'regs')
tsubcc_reg_Instr.setCode(opCodeExec, 'execute')
tsubcc_reg_Instr.addBehavior(WB_icc, 'wb')
tsubcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
tsubcc_reg_Instr.addBehavior(ICC_writeTSub, 'execute', False)
tsubcc_reg_Instr.addVariable(('result', 'BIT<32>'))
tsubcc_reg_Instr.addVariable(('temp_V', 'BIT<1>'))
tsubcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
tsubcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
tsubcc_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(tsubcc_reg_Instr)
opCodeTrap = cxx_writer.writer_code.Code("""
if(temp_V){
    RaiseException(TAG_OVERFLOW);
}
""")
tsubcctv_imm_Instr = trap.Instruction('TSUBccTV_imm', True, frequency = 5)
tsubcctv_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 0, 0, 0, 1, 1]}, ('tsubcctv r', '%rs1', ' ', '%simm13', ' r', '%rd'))
tsubcctv_imm_Instr.setCode(opCodeRegsImm, 'regs')
tsubcctv_imm_Instr.setCode(opCodeExec, 'execute')
tsubcctv_imm_Instr.setCode(opCodeTrap, 'exception')
tsubcctv_imm_Instr.addBehavior(WB_icctv, 'wb')
tsubcctv_imm_Instr.addBehavior(IncrementPC, 'fetch')
tsubcctv_imm_Instr.addBehavior(ICC_writeTVSub, 'execute', False)
tsubcctv_imm_Instr.addVariable(('result', 'BIT<32>'))
tsubcctv_imm_Instr.addVariable(('temp_V', 'BIT<1>'))
tsubcctv_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
tsubcctv_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
tsubcctv_imm_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(tsubcctv_imm_Instr)
tsubcctv_reg_Instr = trap.Instruction('TSUBccTV_reg', True, frequency = 5)
tsubcctv_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 0, 0, 0, 1, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('tsubcctv r', '%rs1', ' r', '%rs2', ' r', '%rd'))
tsubcctv_reg_Instr.setCode(opCodeRegsRegs, 'regs')
tsubcctv_reg_Instr.setCode(opCodeExec, 'execute')
tsubcctv_reg_Instr.setCode(opCodeTrap, 'exception')
tsubcctv_reg_Instr.addBehavior(WB_icctv, 'wb')
tsubcctv_reg_Instr.addBehavior(IncrementPC, 'fetch')
tsubcctv_reg_Instr.addBehavior(ICC_writeTVSub, 'execute', False)
tsubcctv_reg_Instr.addVariable(('result', 'BIT<32>'))
tsubcctv_reg_Instr.addVariable(('temp_V', 'BIT<1>'))
tsubcctv_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
tsubcctv_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
tsubcctv_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(tsubcctv_reg_Instr)

# Multiply Step
opCodeRegsImm = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = SignExtend(simm13, 13);
""")
opCodeRegsRegs = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = rs2;
""")
opCodeExec = cxx_writer.writer_code.Code("""
unsigned int yNew = (((unsigned int)Ybp) >> 1) | (rs1_op << 31);
rs1_op = ((PSRbp[key_ICC_n] ^ PSRbp[key_ICC_v]) << 31) | (((unsigned int)rs1_op) >> 1);
result = rs1_op;
if((Ybp & 0x00000001) != 0){
    result += rs2_op;
}
else{
    rs2_op = 0;
}
Ybp = yNew;
""")
mulscc_imm_Instr = trap.Instruction('MULScc_imm', True, frequency = 5)
mulscc_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 0, 0, 1, 0, 0]}, ('mulscc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
mulscc_imm_Instr.setCode(opCodeRegsImm, 'regs')
mulscc_imm_Instr.setCode(opCodeExec, 'execute')
mulscc_imm_Instr.addBehavior(WB_yicc, 'wb')
mulscc_imm_Instr.addBehavior(IncrementPC, 'fetch')
mulscc_imm_Instr.addBehavior(ICC_writeAdd, 'execute', False)
mulscc_imm_Instr.addVariable(('result', 'BIT<32>'))
mulscc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
mulscc_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
mulscc_imm_Instr.addSpecialRegister('PSRbp', 'in')
mulscc_imm_Instr.addSpecialRegister('Ybp', 'inout')
isa.addInstruction(mulscc_imm_Instr)
mulscc_reg_Instr = trap.Instruction('MULScc_reg', True, frequency = 5)
mulscc_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 0, 0, 1, 0, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('mulscc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
mulscc_reg_Instr.setCode(opCodeRegsRegs, 'regs')
mulscc_reg_Instr.setCode(opCodeExec, 'execute')
mulscc_reg_Instr.addBehavior(WB_yicc, 'wb')
mulscc_reg_Instr.addBehavior(IncrementPC, 'fetch')
mulscc_reg_Instr.addBehavior(ICC_writeAdd, 'execute', False)
mulscc_reg_Instr.addVariable(('result', 'BIT<32>'))
mulscc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
mulscc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
mulscc_reg_Instr.addSpecialRegister('PSRbp', 'in')
mulscc_reg_Instr.addSpecialRegister('Ybp', 'inout')
isa.addInstruction(mulscc_reg_Instr)

# Multiply
opCodeRegsImm = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = SignExtend(simm13, 13);
""")
opCodeRegsRegs = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = rs2;
""")
opCodeExecS = cxx_writer.writer_code.Code("""
long long resultTemp = (long long)(((long long)((int)rs1_op))*((long long)((int)rs2_op)));
Ybp = ((unsigned long long)resultTemp) >> 32;
result = resultTemp & 0x00000000FFFFFFFF;
""")
opCodeExecU = cxx_writer.writer_code.Code("""
unsigned long long resultTemp = (unsigned long long)(((unsigned long long)((unsigned int)rs1_op))*((unsigned long long)((unsigned int)rs2_op)));
Ybp = resultTemp >> 32;
result = resultTemp & 0x00000000FFFFFFFF;
""")
umul_imm_Instr = trap.Instruction('UMUL_imm', True, frequency = 5)
umul_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 1, 0, 1, 0]}, ('umul r', '%rs1', ' ', '%simm13', ' r', '%rd'))
umul_imm_Instr.setCode(opCodeRegsImm, 'regs')
umul_imm_Instr.setCode(opCodeExecU, 'execute')
umul_imm_Instr.addBehavior(WB_y, 'wb')
umul_imm_Instr.addBehavior(IncrementPC, 'fetch')
umul_imm_Instr.addVariable(('result', 'BIT<32>'))
umul_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
umul_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
umul_imm_Instr.addSpecialRegister('Ybp', 'out')
isa.addInstruction(umul_imm_Instr)
umul_reg_Instr = trap.Instruction('UMUL_reg', True, frequency = 5)
umul_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 1, 0, 1, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('umul r', '%rs1', ' r', '%rs2', ' r', '%rd'))
umul_reg_Instr.setCode(opCodeRegsRegs, 'regs')
umul_reg_Instr.setCode(opCodeExecU, 'execute')
umul_reg_Instr.addBehavior(WB_y, 'wb')
umul_reg_Instr.addBehavior(IncrementPC, 'fetch')
umul_reg_Instr.addVariable(('result', 'BIT<32>'))
umul_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
umul_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
umul_reg_Instr.addSpecialRegister('Ybp', 'out')
isa.addInstruction(umul_reg_Instr)
smul_imm_Instr = trap.Instruction('SMUL_imm', True, frequency = 5)
smul_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 1, 0, 1, 1]}, ('smul r', '%rs1', ' ', '%simm13', ' r', '%rd'))
smul_imm_Instr.setCode(opCodeRegsImm, 'regs')
smul_imm_Instr.setCode(opCodeExecS, 'execute')
smul_imm_Instr.addBehavior(WB_y, 'wb')
smul_imm_Instr.addBehavior(IncrementPC, 'fetch')
smul_imm_Instr.addVariable(('result', 'BIT<32>'))
smul_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
smul_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
smul_imm_Instr.addSpecialRegister('Ybp', 'out')
isa.addInstruction(smul_imm_Instr)
smul_reg_Instr = trap.Instruction('SMUL_reg', True, frequency = 5)
smul_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 1, 0, 1, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('smul r', '%rs1', ' r', '%rs2', ' r', '%rd'))
smul_reg_Instr.setCode(opCodeRegsRegs, 'regs')
smul_reg_Instr.setCode(opCodeExecS, 'execute')
smul_reg_Instr.addBehavior(WB_y, 'wb')
smul_reg_Instr.addBehavior(IncrementPC, 'fetch')
smul_reg_Instr.addVariable(('result', 'BIT<32>'))
smul_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
smul_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
smul_reg_Instr.addSpecialRegister('Ybp', 'out')
isa.addInstruction(smul_reg_Instr)
umulcc_imm_Instr = trap.Instruction('UMULcc_imm', True, frequency = 5)
umulcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 1, 0, 1, 0]}, ('umulcc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
umulcc_imm_Instr.setCode(opCodeRegsImm, 'regs')
umulcc_imm_Instr.setCode(opCodeExecU, 'execute')
umulcc_imm_Instr.addBehavior(WB_yicc, 'wb')
umulcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
umulcc_imm_Instr.addBehavior(ICC_writeLogic, 'execute', False)
umulcc_imm_Instr.addVariable(('result', 'BIT<32>'))
umulcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
umulcc_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
umulcc_imm_Instr.addSpecialRegister('Ybp', 'out')
umulcc_imm_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(umulcc_imm_Instr)
umulcc_reg_Instr = trap.Instruction('UMULcc_reg', True, frequency = 5)
umulcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 1, 0, 1, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('umulcc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
umulcc_reg_Instr.setCode(opCodeRegsRegs, 'regs')
umulcc_reg_Instr.setCode(opCodeExecU, 'execute')
umulcc_reg_Instr.addBehavior(WB_yicc, 'wb')
umulcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
umulcc_reg_Instr.addBehavior(ICC_writeLogic, 'execute', False)
umulcc_reg_Instr.addVariable(('result', 'BIT<32>'))
umulcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
umulcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
umulcc_reg_Instr.addSpecialRegister('Ybp', 'out')
umulcc_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(umulcc_reg_Instr)
smulcc_imm_Instr = trap.Instruction('SMULcc_imm', True, frequency = 5)
smulcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 1, 0, 1, 1]}, ('smulcc r', '%rs1', ' ', '%simm13', ' r', '%rd'))
smulcc_imm_Instr.setCode(opCodeRegsImm, 'regs')
smulcc_imm_Instr.setCode(opCodeExecS, 'execute')
smulcc_imm_Instr.addBehavior(WB_yicc, 'wb')
smulcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
smulcc_imm_Instr.addBehavior(ICC_writeLogic, 'execute', False)
smulcc_imm_Instr.addVariable(('result', 'BIT<32>'))
smulcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
smulcc_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
smulcc_imm_Instr.addSpecialRegister('Ybp', 'out')
smulcc_imm_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(smulcc_imm_Instr)
smulcc_reg_Instr = trap.Instruction('SMULcc_reg', True, frequency = 5)
smulcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 1, 0, 1, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('smulcc r', '%rs1', ' r', '%rs2', ' r', '%rd'))
smulcc_reg_Instr.setCode(opCodeRegsRegs, 'regs')
smulcc_reg_Instr.setCode(opCodeExecS, 'execute')
smulcc_reg_Instr.addBehavior(WB_yicc, 'wb')
smulcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
smulcc_reg_Instr.addBehavior(ICC_writeLogic, 'execute', False)
smulcc_reg_Instr.addVariable(('result', 'BIT<32>'))
smulcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
smulcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
smulcc_reg_Instr.addSpecialRegister('Ybp', 'out')
smulcc_reg_Instr.addSpecialRegister('PSRbp', 'out')
isa.addInstruction(smulcc_reg_Instr)

# Multiply Accumulate Instructions
opCodeRegsImm = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = SignExtend(simm13, 13);
""")
opCodeRegsRegs = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = rs2;
""")
opCodeExecS = cxx_writer.writer_code.Code("""
int resultTemp = ((int)SignExtend(rs1_op & 0x0000ffff, 16))*((int)SignExtend(rs2_op & 0x0000ffff, 16));
long long resultAcc = ((((long long)(Ybp & 0x000000ff)) << 32) | (int)ASR18bp) + resultTemp;
Ybp = (resultAcc & 0x000000ff00000000LL) >> 32;
ASR18bp = resultAcc & 0x00000000FFFFFFFFLL;
result = resultAcc & 0x00000000FFFFFFFFLL;
""")
opCodeExecU = cxx_writer.writer_code.Code("""
unsigned int resultTemp = ((unsigned int)rs1_op & 0x0000ffff)*((unsigned int)rs2_op & 0x0000ffff);
unsigned long long resultAcc = ((((unsigned long long)(Ybp & 0x000000ff)) << 32) | (unsigned int)ASR18bp) + resultTemp;
Ybp = (resultAcc & 0x000000ff00000000LL) >> 32;
ASR18bp = resultAcc & 0x00000000FFFFFFFFLL;
result = resultAcc & 0x00000000FFFFFFFFLL;
""")
umac_imm_Instr = trap.Instruction('UMAC_imm', True, frequency = 5)
umac_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 1, 1, 1, 1, 0]}, ('umac r', '%rs1', ' ', '%simm13', ' r', '%rd'))
umac_imm_Instr.setCode(opCodeRegsImm, 'regs')
umac_imm_Instr.setCode(opCodeExecU, 'execute')
umac_imm_Instr.addBehavior(WB_yasr, 'wb')
umac_imm_Instr.addBehavior(IncrementPC, 'fetch')
umac_imm_Instr.addVariable(('result', 'BIT<32>'))
umac_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
umac_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
umac_imm_Instr.addSpecialRegister('Ybp', 'inout')
umac_imm_Instr.addSpecialRegister('ASR18bp', 'inout')
isa.addInstruction(umac_imm_Instr)
umac_reg_Instr = trap.Instruction('UMAC_reg', True, frequency = 5)
umac_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 1, 1, 1, 1, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('umac r', '%rs1', ' r', '%rs2', ' r', '%rd'))
umac_reg_Instr.setCode(opCodeRegsRegs, 'regs')
umac_reg_Instr.setCode(opCodeExecU, 'execute')
umac_reg_Instr.addBehavior(WB_yasr, 'wb')
umac_reg_Instr.addBehavior(IncrementPC, 'fetch')
umac_reg_Instr.addVariable(('result', 'BIT<32>'))
umac_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
umac_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
umac_reg_Instr.addSpecialRegister('Ybp', 'inout')
umac_reg_Instr.addSpecialRegister('ASR18bp', 'inout')
isa.addInstruction(umac_reg_Instr)
smac_imm_Instr = trap.Instruction('SMAC_imm', True, frequency = 5)
smac_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 1, 1, 1, 1, 1]}, ('smac r', '%rs1', ' ', '%simm13', ' r', '%rd'))
smac_imm_Instr.setCode(opCodeRegsImm, 'regs')
smac_imm_Instr.setCode(opCodeExecS, 'execute')
smac_imm_Instr.addBehavior(WB_yasr, 'wb')
smac_imm_Instr.addBehavior(IncrementPC, 'fetch')
smac_imm_Instr.addVariable(('result', 'BIT<32>'))
smac_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
smac_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
smac_imm_Instr.addSpecialRegister('Ybp', 'inout')
smac_imm_Instr.addSpecialRegister('ASR18bp', 'inout')
isa.addInstruction(smac_imm_Instr)
smac_reg_Instr = trap.Instruction('SMAC_reg', True, frequency = 5)
smac_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 1, 1, 1, 1, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('smac r', '%rs1', ' r', '%rs2', ' r', '%rd'))
smac_reg_Instr.setCode(opCodeRegsRegs, 'regs')
smac_reg_Instr.setCode(opCodeExecS, 'execute')
smac_reg_Instr.addBehavior(WB_yasr, 'wb')
smac_reg_Instr.addBehavior(IncrementPC, 'fetch')
smac_reg_Instr.addVariable(('result', 'BIT<32>'))
smac_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
smac_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
smac_reg_Instr.addSpecialRegister('Ybp', 'inout')
smac_reg_Instr.addSpecialRegister('ASR18bp', 'inout')
isa.addInstruction(smac_reg_Instr)

# Divide
opCodeRegsImm = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = SignExtend(simm13, 13);
""")
opCodeRegsRegs = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = rs2;
""")
opCodeExecU = cxx_writer.writer_code.Code("""
exception = rs2_op == 0;
if(!exception){
    unsigned long long res64 = ((unsigned long long)((((unsigned long long)Ybp) << 32) | (unsigned long long)rs1_op))/(unsigned long long)rs2_op;
    temp_V = (res64 & 0xFFFFFFFF00000000LL) != 0;
    if(temp_V){
        result = 0xFFFFFFFF;
    }
    else{
        result = (unsigned int)(res64 & 0x00000000FFFFFFFFLL);
    }
}
""")
opCodeExecS = cxx_writer.writer_code.Code("""
exception = rs2_op == 0;
if(!exception){
    long long res64 = ((long long)((((long long)((int)Ybp)) << 32) | (long long)((int)rs1_op)))/((long long)((int)rs2_op));
    temp_V = (res64 & 0xFFFFFFFF80000000LL) != 0 && (res64 & 0xFFFFFFFF80000000LL) != 0x1FFFFFFFF0000000LL;
    if(temp_V){
        if(res64 > 0){
            result = 0x7FFFFFFF;
        }
        else{
            result = 0x80000000;
        }
    }
    else{
        result = (unsigned int)(res64 & 0x00000000FFFFFFFFLL);
    }
}
""")
opCodeTrap = cxx_writer.writer_code.Code("""
if(exception){
    RaiseException(DIV_ZERO);
}
""")
udiv_imm_Instr = trap.Instruction('UDIV_imm', True, frequency = 5)
udiv_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 1, 1, 1, 0]}, ('udiv', ' r', '%rs1', ' ', '%simm13', '%rd'))
udiv_imm_Instr.setCode(opCodeRegsImm, 'regs')
udiv_imm_Instr.setCode(opCodeExecU, 'execute')
udiv_imm_Instr.setCode(opCodeTrap, 'exception')
udiv_imm_Instr.addBehavior(IncrementPC, 'fetch')
udiv_imm_Instr.addBehavior(WB_plain, 'wb')
udiv_imm_Instr.addVariable(('exception', 'BIT<1>'))
udiv_imm_Instr.addVariable(('temp_V', 'BIT<1>'))
udiv_imm_Instr.addVariable(('result', 'BIT<32>'))
udiv_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
udiv_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
udiv_imm_Instr.addSpecialRegister('Ybp', 'in')
isa.addInstruction(udiv_imm_Instr)
udiv_reg_Instr = trap.Instruction('UDIV_reg', True, frequency = 5)
udiv_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 1, 1, 1, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('udiv', ' r', '%rs1', ' r', '%rs2', '%rd'))
udiv_reg_Instr.setCode(opCodeRegsRegs, 'regs')
udiv_reg_Instr.setCode(opCodeExecU, 'execute')
udiv_reg_Instr.setCode(opCodeTrap, 'exception')
udiv_reg_Instr.addBehavior(IncrementPC, 'fetch')
udiv_reg_Instr.addBehavior(WB_plain, 'wb')
udiv_reg_Instr.addVariable(('exception', 'BIT<1>'))
udiv_reg_Instr.addVariable(('temp_V', 'BIT<1>'))
udiv_reg_Instr.addVariable(('result', 'BIT<32>'))
udiv_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
udiv_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
udiv_reg_Instr.addSpecialRegister('Ybp', 'in')
isa.addInstruction(udiv_reg_Instr)
sdiv_imm_Instr = trap.Instruction('SDIV_imm', True, frequency = 5)
sdiv_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 1, 1, 1, 1]}, ('sdiv', ' r', '%rs1', ' ', '%simm13', '%rd'))
sdiv_imm_Instr.setCode(opCodeRegsImm, 'regs')
sdiv_imm_Instr.setCode(opCodeExecS, 'execute')
sdiv_imm_Instr.setCode(opCodeTrap, 'exception')
sdiv_imm_Instr.addBehavior(IncrementPC, 'fetch')
sdiv_imm_Instr.addBehavior(WB_plain, 'wb')
sdiv_imm_Instr.addVariable(('exception', 'BIT<1>'))
sdiv_imm_Instr.addVariable(('temp_V', 'BIT<1>'))
sdiv_imm_Instr.addVariable(('result', 'BIT<32>'))
sdiv_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
sdiv_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
sdiv_imm_Instr.addSpecialRegister('Ybp', 'in')
isa.addInstruction(sdiv_imm_Instr)
sdiv_reg_Instr = trap.Instruction('SDIV_reg', True, frequency = 5)
sdiv_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 1, 1, 1, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('sdiv', ' r', '%rs1', ' r', '%rs2', '%rd'))
sdiv_reg_Instr.setCode(opCodeRegsRegs, 'regs')
sdiv_reg_Instr.setCode(opCodeExecS, 'execute')
sdiv_reg_Instr.setCode(opCodeTrap, 'exception')
sdiv_reg_Instr.addBehavior(IncrementPC, 'fetch')
sdiv_reg_Instr.addBehavior(WB_plain, 'wb')
sdiv_reg_Instr.addVariable(('exception', 'BIT<1>'))
sdiv_reg_Instr.addVariable(('temp_V', 'BIT<1>'))
sdiv_reg_Instr.addVariable(('result', 'BIT<32>'))
sdiv_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
sdiv_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
sdiv_reg_Instr.addSpecialRegister('Ybp', 'in')
isa.addInstruction(sdiv_reg_Instr)
udivcc_imm_Instr = trap.Instruction('UDIVcc_imm', True, frequency = 5)
udivcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 1, 1, 1, 0]}, ('udivcc', ' r', '%rs1', ' ', '%simm13', '%rd'))
udivcc_imm_Instr.setCode(opCodeRegsImm, 'regs')
udivcc_imm_Instr.setCode(opCodeExecU, 'execute')
udivcc_imm_Instr.setCode(opCodeTrap, 'exception')
udivcc_imm_Instr.addBehavior(ICC_writeDiv, 'execute')
udivcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
udivcc_imm_Instr.addBehavior(WB_icc, 'wb')
udivcc_imm_Instr.addVariable(('exception', 'BIT<1>'))
udivcc_imm_Instr.addVariable(('temp_V', 'BIT<1>'))
udivcc_imm_Instr.addVariable(('result', 'BIT<32>'))
udivcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
udivcc_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
udivcc_imm_Instr.addSpecialRegister('Ybp', 'in')
udivcc_imm_Instr.addSpecialRegister('PSRbp', 'inout')
isa.addInstruction(udivcc_imm_Instr)
udivcc_reg_Instr = trap.Instruction('UDIVcc_reg', True, frequency = 5)
udivcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 1, 1, 1, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('udivcc', ' r', '%rs1', ' r', '%rs2', '%rd'))
udivcc_reg_Instr.setCode(opCodeRegsRegs, 'regs')
udivcc_reg_Instr.setCode(opCodeExecU, 'execute')
udivcc_reg_Instr.setCode(opCodeTrap, 'exception')
udivcc_reg_Instr.addBehavior(ICC_writeDiv, 'execute')
udivcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
udivcc_reg_Instr.addBehavior(WB_icc, 'wb')
udivcc_reg_Instr.addVariable(('exception', 'BIT<1>'))
udivcc_reg_Instr.addVariable(('temp_V', 'BIT<1>'))
udivcc_reg_Instr.addVariable(('result', 'BIT<32>'))
udivcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
udivcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
udivcc_reg_Instr.addSpecialRegister('Ybp', 'in')
udivcc_reg_Instr.addSpecialRegister('PSRbp', 'inout')
isa.addInstruction(udivcc_reg_Instr)
sdivcc_imm_Instr = trap.Instruction('SDIVcc_imm', True, frequency = 5)
sdivcc_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 1, 1, 1, 1]}, ('sdivcc', ' r', '%rs1', ' ', '%simm13', '%rd'))
sdivcc_imm_Instr.setCode(opCodeRegsImm, 'regs')
sdivcc_imm_Instr.setCode(opCodeExecS, 'execute')
sdivcc_imm_Instr.setCode(opCodeTrap, 'exception')
sdivcc_imm_Instr.addBehavior(ICC_writeDiv, 'execute')
sdivcc_imm_Instr.addBehavior(IncrementPC, 'fetch')
sdivcc_imm_Instr.addBehavior(WB_icc, 'wb')
sdivcc_imm_Instr.addVariable(('exception', 'BIT<1>'))
sdivcc_imm_Instr.addVariable(('temp_V', 'BIT<1>'))
sdivcc_imm_Instr.addVariable(('result', 'BIT<32>'))
sdivcc_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
sdivcc_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
sdivcc_imm_Instr.addSpecialRegister('Ybp', 'in')
sdivcc_imm_Instr.addSpecialRegister('PSRbp', 'inout')
isa.addInstruction(sdivcc_imm_Instr)
sdivcc_reg_Instr = trap.Instruction('SDIVcc_reg', True, frequency = 5)
sdivcc_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 1, 1, 1, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('sdivcc', ' r', '%rs1', ' r', '%rs2', '%rd'))
sdivcc_reg_Instr.setCode(opCodeRegsRegs, 'regs')
sdivcc_reg_Instr.setCode(opCodeExecS, 'execute')
sdivcc_reg_Instr.setCode(opCodeTrap, 'exception')
sdivcc_reg_Instr.addBehavior(ICC_writeDiv, 'execute')
sdivcc_reg_Instr.addBehavior(IncrementPC, 'fetch')
sdivcc_reg_Instr.addBehavior(WB_icc, 'wb')
sdivcc_reg_Instr.addVariable(('exception', 'BIT<1>'))
sdivcc_reg_Instr.addVariable(('temp_V', 'BIT<1>'))
sdivcc_reg_Instr.addVariable(('result', 'BIT<32>'))
sdivcc_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
sdivcc_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
sdivcc_reg_Instr.addSpecialRegister('Ybp', 'in')
sdivcc_reg_Instr.addSpecialRegister('PSRbp', 'inout')
isa.addInstruction(sdivcc_reg_Instr)

# Save and Restore
opCodeRegsImm = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = SignExtend(simm13, 13);
""")
opCodeRegsRegs = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = rs2;
""")
opCodeExec = cxx_writer.writer_code.Code("""
result = rs1_op + rs2_op;
okNewWin = IncrementRegWindow();
""")
opCodeTrap = cxx_writer.writer_code.Code("""
if(!okNewWin){
    RaiseException(WINDOW_OVERFLOW);
}
""")
opCodeWb = cxx_writer.writer_code.Code("""
if(okNewWin){
    rd = result;
}
""")
save_imm_Instr = trap.Instruction('SAVE_imm', True, frequency = 5)
save_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 1, 1, 1, 0, 0]}, ('save', ' r', '%rs1', ' ', '%simm13', ' r', '%rd'))
save_imm_Instr.setCode(opCodeRegsImm, 'regs')
save_imm_Instr.setCode(opCodeExec, 'execute')
save_imm_Instr.setCode(opCodeTrap, 'exception')
save_imm_Instr.setCode(opCodeWb, 'wb')
save_imm_Instr.addBehavior(IncrementPC, 'fetch')
save_imm_Instr.addVariable(('okNewWin', 'BIT<1>'))
save_imm_Instr.addVariable(('result', 'BIT<32>'))
save_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
save_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(save_imm_Instr)
save_reg_Instr = trap.Instruction('SAVE_reg', True, frequency = 5)
save_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 1, 1, 1, 0, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('save', ' r', '%rs1', ' r', '%rs2', ' r', '%rd'))
save_reg_Instr.setCode(opCodeRegsRegs, 'regs')
save_reg_Instr.setCode(opCodeExec, 'execute')
save_reg_Instr.setCode(opCodeTrap, 'exception')
save_reg_Instr.setCode(opCodeWb, 'wb')
save_reg_Instr.addBehavior(IncrementPC, 'fetch')
save_reg_Instr.addVariable(('okNewWin', 'BIT<1>'))
save_reg_Instr.addVariable(('result', 'BIT<32>'))
save_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
save_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(save_reg_Instr)
opCodeTrap = cxx_writer.writer_code.Code("""
if(!okNewWin){
    RaiseException(WINDOW_UNDERFLOW);
}
""")
restore_imm_Instr = trap.Instruction('RESTORE_imm', True, frequency = 5)
restore_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 1, 1, 1, 0, 1]}, ('restore', ' r', '%rs1', ' ', '%simm13', ' r', '%rd'))
restore_imm_Instr.setCode(opCodeRegsImm, 'regs')
restore_imm_Instr.setCode(opCodeExec, 'execute')
restore_imm_Instr.setCode(opCodeTrap, 'exception')
restore_imm_Instr.setCode(opCodeWb, 'wb')
restore_imm_Instr.addBehavior(IncrementPC, 'fetch')
restore_imm_Instr.addVariable(('okNewWin', 'BIT<1>'))
restore_imm_Instr.addVariable(('result', 'BIT<32>'))
restore_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
restore_imm_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(restore_imm_Instr)
restore_reg_Instr = trap.Instruction('RESTORE_reg', True, frequency = 5)
restore_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 1, 1, 1, 0, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('restore', ' r', '%rs1', ' r', '%rs2', ' r', '%rd'))
restore_reg_Instr.setCode(opCodeRegsRegs, 'regs')
restore_reg_Instr.setCode(opCodeExec, 'execute')
restore_reg_Instr.setCode(opCodeTrap, 'exception')
restore_reg_Instr.setCode(opCodeWb, 'wb')
restore_reg_Instr.addBehavior(IncrementPC, 'fetch')
restore_reg_Instr.addVariable(('okNewWin', 'BIT<1>'))
restore_reg_Instr.addVariable(('result', 'BIT<32>'))
restore_reg_Instr.addVariable(('rs1_op', 'BIT<32>'))
restore_reg_Instr.addVariable(('rs2_op', 'BIT<32>'))
isa.addInstruction(restore_reg_Instr)

# Branch on Integer Condition Codes
opCode = cxx_writer.writer_code.Code("""
switch(cond){
    case 0x8:{
        // Branch Always
        unsigned int targetPc = PC + 4*(SignExtend(disp22, 22));
        #ifdef ACC_MODEL
        PC = targetPc;
        NPC = targetPc + 4;
        if(a == 1){
            flush();
        }
        #else
        if(a == 1){
            PC = targetPc - 4;
            NPC = targetPc;
        }
        else{
            PC = NPC;
            NPC = targetPc - 4;
        }
        #endif
    break;}
    case 0:{
        // Branch Never
        #ifdef ACC_MODEL
        if(a == 1){
            flush();
        }
        #else
        if(a == 1){
            PC = NPC + 4;
            NPC += 8;
        }
        else{
            PC = NPC;
            NPC += 4;
        }
        #endif
    break;}
    default:{
        // All the other non-special situations
        bool exec = ((cond == 0x9) && PSRbp[key_ICC_z] == 0) ||
                    ((cond == 0x1) && PSRbp[key_ICC_z] != 0) ||
                    ((cond == 0xa) && (PSRbp[key_ICC_z] == 0) && (PSRbp[key_ICC_n] == PSRbp[key_ICC_v])) ||
                    ((cond == 0x2) && ((PSRbp[key_ICC_z] != 0) || (PSRbp[key_ICC_n] != PSRbp[key_ICC_v]))) ||
                    ((cond == 0xb) && PSRbp[key_ICC_n] == PSRbp[key_ICC_v]) ||
                    ((cond == 0x3) && PSR[key_ICC_n] != PSRbp[key_ICC_v]) ||
                    ((cond == 0xc) && (PSRbp[key_ICC_c] + PSRbp[key_ICC_z]) == 0) ||
                    ((cond == 0x4) && (PSRbp[key_ICC_c] + PSRbp[key_ICC_z]) > 0) ||
                    ((cond == 0xd) && PSRbp[key_ICC_c] == 0) ||
                    ((cond == 0x5) && PSRbp[key_ICC_c] != 0) ||
                    ((cond == 0xe) && PSRbp[key_ICC_n] == 0) ||
                    ((cond == 0x6) && PSRbp[key_ICC_n] != 0) ||
                    ((cond == 0xf) && PSRbp[key_ICC_v] == 0) ||
                    ((cond == 0x7) && PSRbp[key_ICC_v] != 0);
        if(exec){
            unsigned int targetPc = PC + 4*(SignExtend(disp22, 22));
            #ifdef ACC_MODEL
            PC = targetPc;
            NPC = targetPc + 4;
            #else
            PC = NPC;
            NPC = targetPc - 4;
            #endif
        }
        else{
            if(a == 1){
                #ifdef ACC_MODEL
                flush();
                #else
                PC = NPC + 4;
                NPC += 8;
                #endif
            }
            #ifndef ACC_MODEL
            else{
                PC = NPC;
                NPC += 4;
            }
            #endif
        }
    break;}
}
""")
branch_Instr = trap.Instruction('BRANCH', True, frequency = 5)
branch_Instr.setMachineCode(b_sethi_format2, {'op2' : [0, 1, 0]},
('b', ('%cond', {int('1000', 2) : 'a',
int('0000', 2) : 'n', int('1001', 2) : 'ne', int('0001', 2) : 'e', int('1010', 2) : 'g', int('0010', 2) : 'le',
int('1011', 2) : 'ge', int('0011', 2) : 'l', int('1100', 2) : 'gu', int('0100', 2) : 'leu', int('1101', 2) : 'cc',
int('01010', 2) : 'cs', int('1110', 2) : 'pos', int('0110', 2) : 'neg', int('1111', 2) : 'vc', int('0111', 2) : 'vs',}),
('%a', {1: ',a'}), ' ', '%disp22'))
branch_Instr.setCode(opCode, 'decode')
branch_Instr.addBehavior(IncrementPC, 'fetch', functionalModel = False)
branch_Instr.addSpecialRegister('PSRbp', 'in')
isa.addInstruction(branch_Instr)

# Call and Link
opCodeWb = cxx_writer.writer_code.Code("""
REGS[15] = oldPC;
""")
opCode = cxx_writer.writer_code.Code("""
unsigned int curPC = PC;
unsigned int target = curPC + (disp30 << 2);
oldPC = curPC - 4;
#ifdef ACC_MODEL
PC = target;
NPC = target + 4;
#else
PC = NPC;
NPC = target;
#endif
""")
call_Instr = trap.Instruction('CALL', True, frequency = 5)
call_Instr.setMachineCode(call_format, {}, ('call ', '%disp30'))
call_Instr.setCode(opCode, 'decode')
call_Instr.setCode(opCodeWb, 'wb')
call_Instr.addBehavior(IncrementPC, 'fetch', functionalModel = False)
call_Instr.addSpecialRegister('REGS[15]', 'out')
call_Instr.addVariable(('oldPC', 'BIT<32>'))
isa.addInstruction(call_Instr)

# Jump and Link
opCodeWb = cxx_writer.writer_code.Code("""
if(!trapNotAligned){
    rd = oldPC;
}
""")
opCodeRegsImm = cxx_writer.writer_code.Code("""
unsigned int jumpAddr = rs1 + SignExtend(simm13, 13);
if((jumpAddr & 0x00000003) != 0){
    trapNotAligned = true;
}
else{
    oldPC = PC - 4;
    #ifdef ACC_MODEL
    PC = jumpAddr;
    NPC = jumpAddr + 4;
    #else
    PC = NPC;
    NPC = jumpAddr;
    #endif
}
""")
opCodeRegsRegs = cxx_writer.writer_code.Code("""
unsigned int jumpAddr = rs1 + rs2;
if((jumpAddr & 0x00000003) != 0){
    trapNotAligned = true;
}
else{
    oldPC = PC - 4;
    #ifdef ACC_MODEL
    PC = jumpAddr;
    NPC = jumpAddr + 4;
    #else
    PC = NPC;
    NPC = jumpAddr;
    #endif
}
""")
opCodeTrap = cxx_writer.writer_code.Code("""
if(trapNotAligned){
    RaiseException(MEM_ADDR_NOT_ALIGNED);
}
""")
jump_imm_Instr = trap.Instruction('JUMP_imm', True, frequency = 5)
jump_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 1, 1, 0, 0, 0]}, ('jmpl', ' r', '%rs1', '+', '%simm13', ' r', '%rd'))
jump_imm_Instr.setCode(opCodeRegsImm, 'decode')
jump_imm_Instr.setCode(opCodeWb, 'wb')
jump_imm_Instr.addBehavior(IncrementPC, 'fetch', functionalModel = False)
jump_imm_Instr.addVariable(cxx_writer.writer_code.Variable('trapNotAligned', cxx_writer.writer_code.boolType))
jump_imm_Instr.addVariable(('oldPC', 'BIT<32>'))
isa.addInstruction(jump_imm_Instr)
jump_reg_Instr = trap.Instruction('JUMP_reg', True, frequency = 5)
jump_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 1, 1, 0, 0, 0], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, ('jmpl', ' r', '%rs1', '+r', '%rs2', ' r', '%rd'))
jump_reg_Instr.setCode(opCodeRegsRegs, 'decode')
jump_reg_Instr.setCode(opCodeWb, 'wb')
jump_reg_Instr.addBehavior(IncrementPC, 'fetch', functionalModel = False)
jump_reg_Instr.addVariable(cxx_writer.writer_code.Variable('trapNotAligned', cxx_writer.writer_code.boolType))
jump_reg_Instr.addVariable(('oldPC', 'BIT<32>'))
isa.addInstruction(jump_reg_Instr)

# Return from Trap
# N.B. In the reg read stage it writes the values of the SU and ET PSR
# fields???????
opCodeRegsImm = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = SignExtend(simm13, 13);
""")
opCodeRegsRegs = cxx_writer.writer_code.Code("""
rs1_op = rs1;
rs2_op = rs2;
""")
rett_imm_Instr = trap.Instruction('RETT_imm', True, frequency = 5)
rett_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 1, 1, 0, 0, 1]}, 'TODO')
isa.addInstruction(rett_imm_Instr)
rett_reg_Instr = trap.Instruction('RETT_reg', True, frequency = 5)
rett_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 1, 1, 0, 0, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, 'TODO')
isa.addInstruction(rett_reg_Instr)

# Trap on Integer Condition Code; note this instruction also receives the forwarding
# of the PSR, the same as the branch instruction
opCode = cxx_writer.writer_code.Code("""
// All the other non-special situations
raiseException = (cond == 0x8) ||
            ((cond == 0x9) && PSRbp[key_ICC_z] == 0) ||
            ((cond == 0x1) && PSRbp[key_ICC_z] != 0) ||
            ((cond == 0xa) && (PSRbp[key_ICC_z] == 0) && (PSRbp[key_ICC_n] == PSRbp[key_ICC_v])) ||
            ((cond == 0x2) && ((PSRbp[key_ICC_z] != 0) || (PSRbp[key_ICC_n] != PSRbp[key_ICC_v]))) ||
            ((cond == 0xb) && PSRbp[key_ICC_n] == PSRbp[key_ICC_v]) ||
            ((cond == 0x3) && PSR[key_ICC_n] != PSRbp[key_ICC_v]) ||
            ((cond == 0xc) && (PSRbp[key_ICC_c] + PSRbp[key_ICC_z]) == 0) ||
            ((cond == 0x4) && (PSRbp[key_ICC_c] + PSRbp[key_ICC_z]) > 0) ||
            ((cond == 0xd) && PSRbp[key_ICC_c] == 0) ||
            ((cond == 0x5) && PSRbp[key_ICC_c] != 0) ||
            ((cond == 0xe) && PSRbp[key_ICC_n] == 0) ||
            ((cond == 0x6) && PSRbp[key_ICC_n] != 0) ||
            ((cond == 0xf) && PSRbp[key_ICC_v] == 0) ||
            ((cond == 0x7) && PSRbp[key_ICC_v] != 0);
""")
opCodeTrapImm = cxx_writer.writer_code.Code("""
if(raiseException){
    RaiseException(TRAP_INSTRUCTION, (rs1 + SignExtend(imm7, 7)) & 0x0000007F);
}
""")
opCodeTrapReg = cxx_writer.writer_code.Code("""
if(raiseException){
    RaiseException(TRAP_INSTRUCTION, (rs1 + rs2) & 0x0000007F);
}
""")
trap_imm_Instr = trap.Instruction('TRAP_imm', True, frequency = 5)
trap_imm_Instr.setMachineCode(ticc_format2, {'op3': [1, 1, 1, 0, 1, 0]},
('t', ('%cond', {int('1000', 2) : 'a',
int('0000', 2) : 'n', int('1001', 2) : 'ne', int('0001', 2) : 'e', int('1010', 2) : 'g', int('0010', 2) : 'le',
int('1011', 2) : 'ge', int('0011', 2) : 'l', int('1100', 2) : 'gu', int('0100', 2) : 'leu', int('1101', 2) : 'cc',
int('01010', 2) : 'cs', int('1110', 2) : 'pos', int('0110', 2) : 'neg', int('1111', 2) : 'vc', int('0111', 2) : 'vs',}),
' r', '%rs1', '+', '%imm7'))
trap_imm_Instr.setCode(opCode, 'decode')
trap_imm_Instr.setCode(opCodeTrapImm, 'exception')
trap_imm_Instr.addBehavior(IncrementPC, 'fetch')
trap_imm_Instr.addSpecialRegister('PSRbp', 'in')
trap_imm_Instr.addVariable(cxx_writer.writer_code.Variable('raiseException', cxx_writer.writer_code.boolType))
isa.addInstruction(trap_imm_Instr)
trap_reg_Instr = trap.Instruction('TRAP_reg', True, frequency = 5)
trap_reg_Instr.setMachineCode(ticc_format1, {'op3': [1, 1, 1, 0, 1, 0]},
('t', ('%cond', {int('1000', 2) : 'a',
int('0000', 2) : 'n', int('1001', 2) : 'ne', int('0001', 2) : 'e', int('1010', 2) : 'g', int('0010', 2) : 'le',
int('1011', 2) : 'ge', int('0011', 2) : 'l', int('1100', 2) : 'gu', int('0100', 2) : 'leu', int('1101', 2) : 'cc',
int('01010', 2) : 'cs', int('1110', 2) : 'pos', int('0110', 2) : 'neg', int('1111', 2) : 'vc', int('0111', 2) : 'vs',}),
' r', '%rs1', '+r', '%rs2'))
trap_reg_Instr.setCode(opCode, 'decode')
trap_reg_Instr.setCode(opCodeTrapReg, 'exception')
trap_reg_Instr.addBehavior(IncrementPC, 'fetch')
trap_reg_Instr.addSpecialRegister('PSRbp', 'in')
trap_reg_Instr.addVariable(cxx_writer.writer_code.Variable('raiseException', cxx_writer.writer_code.boolType))
isa.addInstruction(trap_reg_Instr)

# Read State Register
opCodeRegs = cxx_writer.writer_code.Code("""
y_temp = Y;
""")
opCodeWb = cxx_writer.writer_code.Code("""
rd = y_temp;
""")
readY_Instr = trap.Instruction('READy', True, frequency = 5)
readY_Instr.setMachineCode(read_special_format, {'op3': [1, 0, 1, 0, 0, 0], 'asr': [0, 0, 0, 0, 0]},
('rd ', 'y', ' r', '%rd'), subInstr = True)
readY_Instr.setCode(opCodeRegs, 'regs')
readY_Instr.setCode(opCodeWb, 'wb')
readY_Instr.addBehavior(IncrementPC, 'fetch')
readY_Instr.addVariable(('y_temp', 'BIT<32>'))
isa.addInstruction(readY_Instr)
opCodeRegs = cxx_writer.writer_code.Code("""
asr_temp = ASR[asr];
""")
opCodeWb = cxx_writer.writer_code.Code("""
rd = asr_temp;
""")
readASR_Instr = trap.Instruction('READasr', True, frequency = 5)
readASR_Instr.setMachineCode(read_special_format, {'op3': [1, 0, 1, 0, 0, 0]}, ('rd asr ', 'asr', ' r', '%rd'))
readASR_Instr.setCode(opCodeRegs, 'regs')
readASR_Instr.setCode(opCodeWb, 'wb')
readASR_Instr.addBehavior(IncrementPC, 'fetch')
readASR_Instr.addVariable(('asr_temp', 'BIT<32>'))
isa.addInstruction(readASR_Instr)
opCodeRegs = cxx_writer.writer_code.Code("""
psr_temp = PSR;
supervisor = PSR[key_S];
""")
opCodeTrap = cxx_writer.writer_code.Code("""
if(!supervisor){
    RaiseException(PRIVILEDGE_INSTR);
}
""")
opCodeWb = cxx_writer.writer_code.Code("""
rd = psr_temp;
""")
readPsr_Instr = trap.Instruction('READpsr', True, frequency = 5)
readPsr_Instr.setMachineCode(read_special_format, {'op3': [1, 0, 1, 0, 0, 1]}, ('rd ', 'psr r', '%rd'))
readPsr_Instr.setCode(opCodeRegs, 'regs')
readPsr_Instr.setCode(opCodeTrap, 'exception')
readPsr_Instr.setCode(opCodeWb, 'wb')
readPsr_Instr.addBehavior(IncrementPC, 'fetch')
readPsr_Instr.addVariable(cxx_writer.writer_code.Variable('supervisor', cxx_writer.writer_code.boolType))
readPsr_Instr.addVariable(('psr_temp', 'BIT<32>'))
isa.addInstruction(readPsr_Instr)
opCodeRegs = cxx_writer.writer_code.Code("""
wim_temp = WIM;
supervisor = PSR[key_S];
""")
opCodeTrap = cxx_writer.writer_code.Code("""
if(!supervisor){
    RaiseException(PRIVILEDGE_INSTR);
}
""")
opCodeWb = cxx_writer.writer_code.Code("""
rd = wim_temp;
""")
readWim_Instr = trap.Instruction('READwim', True, frequency = 5)
readWim_Instr.setMachineCode(read_special_format, {'op3': [1, 0, 1, 0, 1, 0]}, ('rd ', 'wim r', '%rd'))
readWim_Instr.setCode(opCodeRegs, 'regs')
readWim_Instr.setCode(opCodeTrap, 'exception')
readWim_Instr.setCode(opCodeWb, 'wb')
readWim_Instr.addBehavior(IncrementPC, 'fetch')
readWim_Instr.addVariable(cxx_writer.writer_code.Variable('supervisor', cxx_writer.writer_code.boolType))
readWim_Instr.addVariable(('wim_temp', 'BIT<32>'))
isa.addInstruction(readWim_Instr)
opCodeRegs = cxx_writer.writer_code.Code("""
tbr_temp = TBR;
supervisor = PSR[key_S];
""")
opCodeTrap = cxx_writer.writer_code.Code("""
if(!supervisor){
    RaiseException(PRIVILEDGE_INSTR);
}
""")
opCodeWb = cxx_writer.writer_code.Code("""
rd = tbr_temp;
""")
readTbr_Instr = trap.Instruction('READtbr', True, frequency = 5)
readTbr_Instr.setMachineCode(read_special_format, {'op3': [1, 0, 1, 0, 1, 1]}, ('rd ', 'tbr r', '%rd'))
readTbr_Instr.setCode(opCodeRegs, 'regs')
readTbr_Instr.setCode(opCodeTrap, 'exception')
readTbr_Instr.setCode(opCodeWb, 'wb')
readTbr_Instr.addBehavior(IncrementPC, 'fetch')
readTbr_Instr.addVariable(cxx_writer.writer_code.Variable('supervisor', cxx_writer.writer_code.boolType))
readTbr_Instr.addVariable(('tbr_temp', 'BIT<32>'))
isa.addInstruction(readTbr_Instr)

# Write State Register
opCodeXorR = cxx_writer.writer_code.Code("""
result = rs1 ^ rs2;
""")
opCodeXorI = cxx_writer.writer_code.Code("""
result = rs1 ^ SignExtend(simm13, 13);
""")
opCodeWb = cxx_writer.writer_code.Code("""
Y = result;
""")
opCodeExec = cxx_writer.writer_code.Code("""
Ybp = result;
""")
writeY_reg_Instr = trap.Instruction('WRITEY_reg', True, frequency = 5)
writeY_reg_Instr.setMachineCode(write_special_format1, {'op3': [1, 1, 0, 0, 0, 0], 'rd': [0, 0, 0, 0, 0]}, ('wr r', '%rs1', ' r', '%rs2', ' y'), subInstr = True)
writeY_reg_Instr.setCode(opCodeXorR, 'regs')
writeY_reg_Instr.setCode(opCodeExec, 'execute')
writeY_reg_Instr.setCode(opCodeWb, 'wb')
writeY_reg_Instr.addBehavior(IncrementPC, 'fetch')
writeY_reg_Instr.addSpecialRegister('Ybp', 'out')
writeY_reg_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(writeY_reg_Instr)
writeY_imm_Instr = trap.Instruction('WRITEY_imm', True, frequency = 5)
writeY_imm_Instr.setMachineCode(write_special_format2, {'op3': [1, 1, 0, 0, 0, 0], 'rd': [0, 0, 0, 0, 0]}, ('wr r', '%rs1', ' ', '%simm13', ' y'), subInstr = True)
writeY_imm_Instr.setCode(opCodeXorI, 'regs')
writeY_imm_Instr.setCode(opCodeExec, 'execute')
writeY_imm_Instr.setCode(opCodeWb, 'wb')
writeY_imm_Instr.addBehavior(IncrementPC, 'fetch')
writeY_imm_Instr.addSpecialRegister('Ybp', 'out')
writeY_imm_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(writeY_imm_Instr)
opCodeWb = cxx_writer.writer_code.Code("""
ASR[rd] = result;
""")
opCodeExec = cxx_writer.writer_code.Code("""
if(rd == 18){
    ASR18bp = result;
}
""")
writeASR_reg_Instr = trap.Instruction('WRITEasr_reg', True, frequency = 5)
writeASR_reg_Instr.setMachineCode(write_special_format1, {'op3': [1, 1, 0, 0, 0, 0]}, ('wr r', '%rs1', ' r', '%rs2', ' asr', '%rd'))
writeASR_reg_Instr.setCode(opCodeXorR, 'regs')
writeASR_reg_Instr.setCode(opCodeExec, 'execute')
writeASR_reg_Instr.setCode(opCodeWb, 'wb')
writeASR_reg_Instr.addBehavior(IncrementPC, 'fetch')
writeASR_reg_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(writeASR_reg_Instr)
writeASR_imm_Instr = trap.Instruction('WRITEasr_imm', True, frequency = 5)
writeASR_imm_Instr.setMachineCode(write_special_format2, {'op3': [1, 1, 0, 0, 0, 0]}, ('wr r', '%rs1', ' ', '%simm13', ' asr', '%rd'))
writeASR_imm_Instr.setCode(opCodeXorI, 'regs')
writeASR_imm_Instr.setCode(opCodeExec, 'execute')
writeASR_imm_Instr.setCode(opCodeWb, 'wb')
writeASR_imm_Instr.addBehavior(IncrementPC, 'fetch')
writeASR_imm_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(writeASR_imm_Instr)
# ############################TODO: With respect to exceptions, the program counter appears to be written immediately:
# this means that exceptions has to see the new value of the program counter ####################################
opCodeXorR = cxx_writer.writer_code.Code("""
result = rs1 ^ rs2;
raiseException = (PSR[key_S] == 0) || (((0x01 << (result & 0x0000001f)) & WIM) != 0);
""")
opCodeXorI = cxx_writer.writer_code.Code("""
result = rs1 ^ SignExtend(simm13, 13);
raiseException = (PSR[key_S] == 0) || (((0x01 << (result & 0x0000001f)) & WIM) != 0);
""")
opCodeWb = cxx_writer.writer_code.Code("""
if(!raiseException){
    PSR = result;
}
""")
opCodeExec = cxx_writer.writer_code.Code("""
if(!raiseException){
    PSRbp = result;
}
""")
opCodeTrap = cxx_writer.writer_code.Code("""
if(raiseException){
    RaiseException(PRIVILEDGE_INSTR);
}
""")
writePsr_reg_Instr = trap.Instruction('WRITEpsr_reg', True, frequency = 5)
writePsr_reg_Instr.setMachineCode(write_special_format1, {'op3': [1, 1, 0, 0, 0, 1]}, ('wr r', '%rs1', ' r', '%rs2', ' psr'))
writePsr_reg_Instr.setCode(opCodeXorR, 'regs')
writePsr_reg_Instr.setCode(opCodeExec, 'execute')
writePsr_reg_Instr.setCode(opCodeTrap, 'exception')
writePsr_reg_Instr.setCode(opCodeWb, 'wb')
writePsr_reg_Instr.addBehavior(IncrementPC, 'fetch')
writePsr_reg_Instr.addSpecialRegister('PSRbp', 'out')
writePsr_reg_Instr.addVariable(cxx_writer.writer_code.Variable('raiseException', cxx_writer.writer_code.boolType))
writePsr_reg_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(writePsr_reg_Instr)
writePsr_imm_Instr = trap.Instruction('WRITEpsr_imm', True, frequency = 5)
writePsr_imm_Instr.setMachineCode(write_special_format2, {'op3': [1, 1, 0, 0, 0, 1]}, ('wr r', '%rs1', ' ', '%simm13', ' psr'))
writePsr_imm_Instr.setCode(opCodeXorI, 'regs')
writePsr_imm_Instr.setCode(opCodeExec, 'execute')
writePsr_imm_Instr.setCode(opCodeTrap, 'exception')
writePsr_imm_Instr.setCode(opCodeWb, 'wb')
writePsr_imm_Instr.addBehavior(IncrementPC, 'fetch')
writePsr_imm_Instr.addSpecialRegister('PSRbp', 'out')
writePsr_imm_Instr.addVariable(cxx_writer.writer_code.Variable('raiseException', cxx_writer.writer_code.boolType))
writePsr_imm_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(writePsr_imm_Instr)
opCodeXorR = cxx_writer.writer_code.Code("""
result = rs1 ^ rs2;
raiseException = (PSR[key_S] == 0);
""")
opCodeXorI = cxx_writer.writer_code.Code("""
result = rs1 ^ SignExtend(simm13, 13);
raiseException = (PSR[key_S] == 0);
""")
opCodeWb = cxx_writer.writer_code.Code("""
if(!raiseException){
    WIM = result;
}
""")
opCodeTrap = cxx_writer.writer_code.Code("""
if(raiseException){
    RaiseException(PRIVILEDGE_INSTR);
}
""")
writeWim_reg_Instr = trap.Instruction('WRITEwim_reg', True, frequency = 5)
writeWim_reg_Instr.setMachineCode(write_special_format1, {'op3': [1, 1, 0, 0, 1, 0]}, ('wr r', '%rs1', ' r', '%rs2', ' wim'))
writeWim_reg_Instr.setCode(opCodeXorR, 'regs')
writeWim_reg_Instr.setCode(opCodeTrap, 'exception')
writeWim_reg_Instr.setCode(opCodeWb, 'wb')
writeWim_reg_Instr.addBehavior(IncrementPC, 'fetch')
writeWim_reg_Instr.addVariable(cxx_writer.writer_code.Variable('raiseException', cxx_writer.writer_code.boolType))
writeWim_reg_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(writeWim_reg_Instr)
writeWim_imm_Instr = trap.Instruction('WRITEwim_imm', True, frequency = 5)
writeWim_imm_Instr.setMachineCode(write_special_format2, {'op3': [1, 1, 0, 0, 1, 0]}, ('wr r', '%rs1', ' ', '%simm13', ' wim'))
writeWim_imm_Instr.setCode(opCodeXorI, 'regs')
writeWim_imm_Instr.setCode(opCodeTrap, 'exception')
writeWim_imm_Instr.setCode(opCodeWb, 'wb')
writeWim_imm_Instr.addBehavior(IncrementPC, 'fetch')
writeWim_imm_Instr.addVariable(cxx_writer.writer_code.Variable('raiseException', cxx_writer.writer_code.boolType))
writeWim_imm_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(writeWim_imm_Instr)
opCodeWb = cxx_writer.writer_code.Code("""
if(!raiseException){
    TBR[key_TBA] = ((result & 0xFFFFF000) >> 11);
}
""")
writeTbr_reg_Instr = trap.Instruction('WRITEtbr_reg', True, frequency = 5)
writeTbr_reg_Instr.setMachineCode(write_special_format1, {'op3': [1, 1, 0, 0, 1, 1]}, ('wr r', '%rs1', ' r', '%rs2', ' tbr'))
writeTbr_reg_Instr.setCode(opCodeXorR, 'regs')
writeTbr_reg_Instr.setCode(opCodeTrap, 'exception')
writeTbr_reg_Instr.setCode(opCodeWb, 'wb')
writeTbr_reg_Instr.addBehavior(IncrementPC, 'fetch')
writeTbr_reg_Instr.addVariable(cxx_writer.writer_code.Variable('raiseException', cxx_writer.writer_code.boolType))
writeTbr_reg_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(writeTbr_reg_Instr)
writeTbr_imm_Instr = trap.Instruction('WRITEtbr_imm', True, frequency = 5)
writeTbr_imm_Instr.setMachineCode(write_special_format2, {'op3': [1, 1, 0, 0, 1, 1]}, ('wr r', '%rs1', ' ', '%simm13', ' tbr'))
writeTbr_imm_Instr.setCode(opCodeXorI, 'regs')
writeTbr_imm_Instr.setCode(opCodeTrap, 'exception')
writeTbr_imm_Instr.setCode(opCodeWb, 'wb')
writeTbr_imm_Instr.addBehavior(IncrementPC, 'fetch')
writeTbr_imm_Instr.addVariable(cxx_writer.writer_code.Variable('raiseException', cxx_writer.writer_code.boolType))
writeTbr_imm_Instr.addVariable(('result', 'BIT<32>'))
isa.addInstruction(writeTbr_imm_Instr)

## Store Barrier
opCode = cxx_writer.writer_code.Code("""
""")
stbar_Instr = trap.Instruction('STBAR', True, frequency = 5)
stbar_Instr.setMachineCode(stbar_format, {}, 'TODO', subInstr = True)
stbar_Instr.setCode(opCode, 'execute')
isa.addInstruction(stbar_Instr)

# Unimplemented Instruction
opCode = cxx_writer.writer_code.Code("""
RaiseException(ILLEGAL_INSTR);
""")
unimpl_Instr = trap.Instruction('UNIMP', True, frequency = 5)
unimpl_Instr.setMachineCode(b_sethi_format1, {'op2' : [0, 0, 0]}, ('unimp', ' ', '%imm22'))
unimpl_Instr.setCode(opCode, 'exception')
unimpl_Instr.addBehavior(IncrementPC, 'fetch')
isa.addInstruction(unimpl_Instr)

# Flush Memory
opCode = cxx_writer.writer_code.Code("""
""")
flush_reg_Instr = trap.Instruction('FLUSH_reg', True, frequency = 5)
flush_reg_Instr.setMachineCode(dpi_format1, {'op3': [1, 1, 1, 0, 1, 1], 'asi' : [0, 0, 0, 0, 0, 0, 0, 0]}, 'TODO')
flush_reg_Instr.setCode(opCode, 'execute')
isa.addInstruction(flush_reg_Instr)
flush_imm_Instr = trap.Instruction('FLUSH_imm', True, frequency = 5)
flush_imm_Instr.setMachineCode(dpi_format2, {'op3': [1, 1, 1, 0, 1, 1]}, 'TODO')
flush_imm_Instr.setCode(opCode, 'execute')
isa.addInstruction(flush_imm_Instr)
