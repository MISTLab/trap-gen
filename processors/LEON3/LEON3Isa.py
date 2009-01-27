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

# Load Integer Instruction Family
opCode = cxx_writer.Code("""
""")
ldsb_imm_Instr = trap.Instruction('LDSB_imm', True, frequency = 5)
ldsb_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 1, 0, 0, 1]}, 'TODO')
ldsb_imm_Instr.setCode(opCode, 'execute')
ldsb_imm_Instr.addTest({}, {}, {})
isa.addInstruction(ldsb_imm_Instr)
ldsb_reg_Instr = trap.Instruction('LDSB_reg', True, frequency = 5)
ldsb_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 1, 0, 0, 1]}, 'TODO')
ldsb_reg_Instr.setCode(opCode, 'execute')
ldsb_reg_Instr.addTest({}, {}, {})
isa.addInstruction(ldsb_reg_Instr)
ldsh_imm_Instr = trap.Instruction('LDSH_imm', True, frequency = 5)
ldsh_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 1, 0, 1, 0]}, 'TODO')
ldsh_imm_Instr.setCode(opCode, 'execute')
ldsh_imm_Instr.addTest({}, {}, {})
isa.addInstruction(ldsh_imm_Instr)
ldsh_reg_Instr = trap.Instruction('LDSH_reg', True, frequency = 5)
ldsh_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 1, 0, 1, 0]}, 'TODO')
ldsh_reg_Instr.setCode(opCode, 'execute')
ldsh_reg_Instr.addTest({}, {}, {})
isa.addInstruction(ldsh_reg_Instr)
ldub_imm_Instr = trap.Instruction('LDUB_imm', True, frequency = 5)
ldub_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 0, 0, 1]}, 'TODO')
ldub_imm_Instr.setCode(opCode, 'execute')
ldub_imm_Instr.addTest({}, {}, {})
isa.addInstruction(ldub_imm_Instr)
ldub_reg_Instr = trap.Instruction('LDUB_reg', True, frequency = 5)
ldub_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 0, 0, 1]}, 'TODO')
ldub_reg_Instr.setCode(opCode, 'execute')
ldub_reg_Instr.addTest({}, {}, {})
isa.addInstruction(ldub_reg_Instr)
lduh_imm_Instr = trap.Instruction('LDUH_imm', True, frequency = 5)
lduh_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 1, 0, 0, 1]}, 'TODO')
lduh_imm_Instr.setCode(opCode, 'execute')
lduh_imm_Instr.addTest({}, {}, {})
isa.addInstruction(lduh_imm_Instr)
lduh_reg_Instr = trap.Instruction('LDUH_reg', True, frequency = 5)
lduh_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 1, 0, 0, 1]}, 'TODO')
lduh_reg_Instr.setCode(opCode, 'execute')
lduh_reg_Instr.addTest({}, {}, {})
isa.addInstruction(lduh_reg_Instr)
ld_imm_Instr = trap.Instruction('LD_imm', True, frequency = 5)
ld_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 0, 0, 0]}, 'TODO')
ld_imm_Instr.setCode(opCode, 'execute')
ld_imm_Instr.addTest({}, {}, {})
isa.addInstruction(ld_imm_Instr)
ld_reg_Instr = trap.Instruction('LD_reg', True, frequency = 5)
ld_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 0, 0, 0]}, 'TODO')
ld_reg_Instr.setCode(opCode, 'execute')
ld_reg_Instr.addTest({}, {}, {})
isa.addInstruction(ld_reg_Instr)
ldd_imm_Instr = trap.Instruction('LDD_imm', True, frequency = 5)
ldd_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 0, 1, 1]}, 'TODO')
ldd_imm_Instr.setCode(opCode, 'execute')
ldd_imm_Instr.addTest({}, {}, {})
isa.addInstruction(ldd_imm_Instr)
ldd_reg_Instr = trap.Instruction('LDD_reg', True, frequency = 5)
ldd_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 0, 1, 1]}, 'TODO')
ldd_reg_Instr.setCode(opCode, 'execute')
ldd_reg_Instr.addTest({}, {}, {})
isa.addInstruction(ldd_reg_Instr)
ldsba_imm_Instr = trap.Instruction('LDSBA_imm', True, frequency = 5)
ldsba_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 1, 0, 0, 1]}, 'TODO')
ldsba_imm_Instr.setCode(opCode, 'execute')
ldsba_imm_Instr.addTest({}, {}, {})
isa.addInstruction(ldsba_imm_Instr)
ldsba_reg_Instr = trap.Instruction('LDSBA_reg', True, frequency = 5)
ldsba_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 1, 0, 0, 1]}, 'TODO')
ldsba_reg_Instr.setCode(opCode, 'execute')
ldsba_reg_Instr.addTest({}, {}, {})
isa.addInstruction(ldsba_reg_Instr)
ldsha_imm_Instr = trap.Instruction('LDSHA_imm', True, frequency = 5)
ldsha_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 1, 0, 1, 0]}, 'TODO')
ldsha_imm_Instr.setCode(opCode, 'execute')
ldsha_imm_Instr.addTest({}, {}, {})
isa.addInstruction(ldsha_imm_Instr)
ldsha_reg_Instr = trap.Instruction('LDSHA_reg', True, frequency = 5)
ldsha_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 1, 0, 1, 0]}, 'TODO')
ldsha_reg_Instr.setCode(opCode, 'execute')
ldsha_reg_Instr.addTest({}, {}, {})
isa.addInstruction(ldsha_reg_Instr)
lduba_imm_Instr = trap.Instruction('LDUBA_imm', True, frequency = 5)
lduba_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 0, 0, 1]}, 'TODO')
lduba_imm_Instr.setCode(opCode, 'execute')
lduba_imm_Instr.addTest({}, {}, {})
isa.addInstruction(lduba_imm_Instr)
lduba_reg_Instr = trap.Instruction('LDUBA_reg', True, frequency = 5)
lduba_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 0, 0, 1]}, 'TODO')
lduba_reg_Instr.setCode(opCode, 'execute')
lduba_reg_Instr.addTest({}, {}, {})
isa.addInstruction(lduba_reg_Instr)
lduha_imm_Instr = trap.Instruction('LDUHA_imm', True, frequency = 5)
lduha_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 1, 0, 0, 1]}, 'TODO')
lduha_imm_Instr.setCode(opCode, 'execute')
lduha_imm_Instr.addTest({}, {}, {})
isa.addInstruction(lduha_imm_Instr)
lduha_reg_Instr = trap.Instruction('LDUHA_reg', True, frequency = 5)
lduha_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 1, 0, 0, 1]}, 'TODO')
lduha_reg_Instr.setCode(opCode, 'execute')
lduha_reg_Instr.addTest({}, {}, {})
isa.addInstruction(lduha_reg_Instr)
lda_imm_Instr = trap.Instruction('LDA_imm', True, frequency = 5)
lda_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 0, 0, 0]}, 'TODO')
lda_imm_Instr.setCode(opCode, 'execute')
lda_imm_Instr.addTest({}, {}, {})
isa.addInstruction(lda_imm_Instr)
lda_reg_Instr = trap.Instruction('LDA_reg', True, frequency = 5)
lda_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 0, 0, 0]}, 'TODO')
lda_reg_Instr.setCode(opCode, 'execute')
lda_reg_Instr.addTest({}, {}, {})
isa.addInstruction(lda_reg_Instr)
ldda_imm_Instr = trap.Instruction('LDDA_imm', True, frequency = 5)
ldda_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 0, 1, 1]}, 'TODO')
ldda_imm_Instr.setCode(opCode, 'execute')
ldda_imm_Instr.addTest({}, {}, {})
isa.addInstruction(ldda_imm_Instr)
ldda_reg_Instr = trap.Instruction('LDDA_reg', True, frequency = 5)
ldda_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 0, 1, 1]}, 'TODO')
ldda_reg_Instr.setCode(opCode, 'execute')
ldda_reg_Instr.addTest({}, {}, {})
isa.addInstruction(ldda_reg_Instr)

# Store integer instructions
stb_imm_Instr = trap.Instruction('STB_imm', True, frequency = 5)
stb_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 1, 0, 1]}, 'TODO')
stb_imm_Instr.setCode(opCode, 'execute')
stb_imm_Instr.addTest({}, {}, {})
isa.addInstruction(stb_imm_Instr)
stb_reg_Instr = trap.Instruction('STB_reg', True, frequency = 5)
stb_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 1, 0, 1]}, 'TODO')
stb_reg_Instr.setCode(opCode, 'execute')
stb_reg_Instr.addTest({}, {}, {})
isa.addInstruction(stb_reg_Instr)
sth_imm_Instr = trap.Instruction('STH_imm', True, frequency = 5)
sth_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 1, 1, 0]}, 'TODO')
sth_imm_Instr.setCode(opCode, 'execute')
sth_imm_Instr.addTest({}, {}, {})
isa.addInstruction(sth_imm_Instr)
sth_reg_Instr = trap.Instruction('STH_reg', True, frequency = 5)
sth_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 1, 1, 0]}, 'TODO')
sth_reg_Instr.setCode(opCode, 'execute')
sth_reg_Instr.addTest({}, {}, {})
isa.addInstruction(sth_reg_Instr)
st_imm_Instr = trap.Instruction('ST_imm', True, frequency = 5)
st_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 1, 0, 0]}, 'TODO')
st_imm_Instr.setCode(opCode, 'execute')
st_imm_Instr.addTest({}, {}, {})
isa.addInstruction(st_imm_Instr)
st_reg_Instr = trap.Instruction('ST_reg', True, frequency = 5)
st_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 1, 0, 0]}, 'TODO')
st_reg_Instr.setCode(opCode, 'execute')
st_reg_Instr.addTest({}, {}, {})
isa.addInstruction(st_reg_Instr)
std_imm_Instr = trap.Instruction('STD_imm', True, frequency = 5)
std_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 1, 1, 1]}, 'TODO')
std_imm_Instr.setCode(opCode, 'execute')
std_imm_Instr.addTest({}, {}, {})
isa.addInstruction(std_imm_Instr)
std_reg_Instr = trap.Instruction('STD_reg', True, frequency = 5)
std_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 0, 0, 1, 1, 1]}, 'TODO')
std_reg_Instr.setCode(opCode, 'execute')
std_reg_Instr.addTest({}, {}, {})
isa.addInstruction(std_reg_Instr)
stba_imm_Instr = trap.Instruction('STBA_imm', True, frequency = 5)
stba_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 1, 0, 1]}, 'TODO')
stba_imm_Instr.setCode(opCode, 'execute')
stba_imm_Instr.addTest({}, {}, {})
isa.addInstruction(stba_imm_Instr)
stba_reg_Instr = trap.Instruction('STBA_reg', True, frequency = 5)
stba_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 1, 0, 1]}, 'TODO')
stba_reg_Instr.setCode(opCode, 'execute')
stba_reg_Instr.addTest({}, {}, {})
isa.addInstruction(stba_reg_Instr)
stha_imm_Instr = trap.Instruction('STHA_imm', True, frequency = 5)
stha_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 1, 1, 0]}, 'TODO')
stha_imm_Instr.setCode(opCode, 'execute')
stha_imm_Instr.addTest({}, {}, {})
isa.addInstruction(stha_imm_Instr)
stha_reg_Instr = trap.Instruction('STHA_reg', True, frequency = 5)
stha_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 1, 1, 0]}, 'TODO')
stha_reg_Instr.setCode(opCode, 'execute')
stha_reg_Instr.addTest({}, {}, {})
isa.addInstruction(stha_reg_Instr)
sta_imm_Instr = trap.Instruction('STA_imm', True, frequency = 5)
sta_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 1, 0, 0]}, 'TODO')
sta_imm_Instr.setCode(opCode, 'execute')
sta_imm_Instr.addTest({}, {}, {})
isa.addInstruction(sta_imm_Instr)
sta_reg_Instr = trap.Instruction('STA_reg', True, frequency = 5)
sta_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 1, 0, 0]}, 'TODO')
sta_reg_Instr.setCode(opCode, 'execute')
sta_reg_Instr.addTest({}, {}, {})
isa.addInstruction(sta_reg_Instr)
stda_imm_Instr = trap.Instruction('STDA_imm', True, frequency = 5)
stda_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 1, 0, 1, 1, 1]}, 'TODO')
stda_imm_Instr.setCode(opCode, 'execute')
stda_imm_Instr.addTest({}, {}, {})
isa.addInstruction(stda_imm_Instr)
stda_reg_Instr = trap.Instruction('STDA_reg', True, frequency = 5)
stda_reg_Instr.setMachineCode(dpi_format1, {'op3': [0, 1, 0, 1, 1, 1]}, 'TODO')
stda_reg_Instr.setCode(opCode, 'execute')
stda_reg_Instr.addTest({}, {}, {})
isa.addInstruction(stda_reg_Instr)

# Atomic Load/Store

