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

isa.addMethod(SignExtend_method)


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

#ADD instruction family
# ADD
opCode = cxx_writer.writer_code.Code("""
long long result = (long long)((int)rb) + (long long)((int)ra);
MSR[key_C] = ((ra^rb^(int)(result >> 1)) & 0x80000000) != 0;
rd = (int)result; 
""")
add_Instr = trap.Instruction('ADD', True)
add_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
add_Instr.setCode(opCode,'execute')
add_Instr.addBehavior(IncrementPC, 'execute')
add_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
add_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
add_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
add_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x3, 'PC':0x4, 'MSR':0x20000000})
add_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x7f000000, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(add_Instr)

# ADDC
opCode = cxx_writer.writer_code.Code("""
long long result = (long long)((int)ra) + (long long)((int)rb) + (long long)MSR[key_C];
MSR[key_C] = ((ra^rb^(int)(result >> 1)) & 0x80000000) != 0;
rd = (int)result;
""")
addc_Instr = trap.Instruction('ADDC', True)
addc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
addc_Instr.setCode(opCode,'execute')
addc_Instr.addBehavior(IncrementPC, 'execute')
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 11, 'PC':0x4, 'MSR':0x00000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x3, 'PC':0x4, 'MSR':0x20000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x7f000000, 'PC':0x4, 'MSR':0x20000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x80000002, 'PC':0x4, 'MSR':0x00000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x4, 'PC':0x4, 'MSR':0x20000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x7f000001, 'PC':0x4, 'MSR':0x20000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfffffffe, 'GPR[2]': 0x00000001, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x00000000, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(addc_Instr)

# ADDK
opCode = cxx_writer.writer_code.Code("""
rd = (int)rb + (int)ra;
""")
addk_Instr = trap.Instruction('ADDK', True)
addk_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
addk_Instr.setCode(opCode,'execute')
addk_Instr.addBehavior(IncrementPC, 'execute')
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x20000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x3, 'PC':0x4, 'MSR':0x00000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x7f000000, 'PC':0x4, 'MSR':0x00000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x20000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x3, 'PC':0x4, 'MSR':0x20000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x7f000000, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(addk_Instr)

# ADDKC
opCode = cxx_writer.writer_code.Code("""
rd = (int)rb + (int)ra +(int)MSR[key_C];
""")
addkc_Instr = trap.Instruction('ADDKC', True)
addkc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
addkc_Instr.setCode(opCode,'execute')
addkc_Instr.addBehavior(IncrementPC, 'execute')
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 11, 'PC':0x4, 'MSR':0x20000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x3, 'PC':0x4, 'MSR':0x00000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x7f000000, 'PC':0x4, 'MSR':0x00000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x80000002, 'PC':0x4, 'MSR':0x20000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x4, 'PC':0x4, 'MSR':0x20000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x7f000001, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(addkc_Instr)

#ADDI instruction family
#ADDI
opCode = cxx_writer.writer_code.Code("""
int imm_value = (int)SignExtend(imm, 16);
long long result = (long long)((int)ra) + ((long long)imm_value);
MSR[key_C] = ((ra^imm_value^(int)(result >> 1)) & 0x80000000) != 0;
rd = (int)result;
""")
addi_Instr = trap.Instruction('ADDI', True)
addi_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,0,0]}, 'TODO')
addi_Instr.setCode(opCode,'execute')
addi_Instr.addBehavior(IncrementPC, 'execute')
addi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0002}, {'GPR[1]': 0x7fffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x00fe8000, 'PC':0x4, 'MSR':0x20000000})
addi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x00fe8000, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(addi_Instr)

#ADDIC
opCode = cxx_writer.writer_code.Code("""
int imm_value = (int)SignExtend(imm, 16);
long long result = (long long)((int)ra) + ((long long)imm_value) + (long long)MSR[key_C];
MSR[key_C] = ((ra^imm_value^(int)(result >> 1)) & 0x80000000) != 0;
rd = (int)result;
""")
addic_Instr = trap.Instruction('ADDIC', True)
addic_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,1,0]}, 'TODO')
addic_Instr.setCode(opCode,'execute')
addic_Instr.addBehavior(IncrementPC, 'execute')
addic_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addic_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 11, 'PC':0x4, 'MSR':0x00000000})
addic_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0002}, {'GPR[1]': 0x7fffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addic_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x00fe8000, 'PC':0x4, 'MSR':0x20000000})
addic_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x00fe8001, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(addic_Instr)

#ADDIK
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra + ((int)SignExtend(imm, 16));
""")
addik_Instr = trap.Instruction('ADDIK', True)
addik_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,0,0]}, 'TODO')
addik_Instr.setCode(opCode,'execute')
addik_Instr.addBehavior(IncrementPC, 'execute')
addik_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addik_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x20000000})
addik_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0002}, {'GPR[1]': 0x7fffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addik_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x00fe8000, 'PC':0x4, 'MSR':0x00000000})
addik_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x00fe8000, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(addik_Instr)

#ADDIKC
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra + (int)SignExtend(imm, 16) + (int)MSR[key_C];
""")
addikc_Instr = trap.Instruction('ADDIKC', True)
addikc_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,1,0]}, 'TODO')
addikc_Instr.setCode(opCode,'execute')
addikc_Instr.addBehavior(IncrementPC, 'execute')
addikc_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addikc_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 11, 'PC':0x4, 'MSR':0x20000000})
addikc_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0002}, {'GPR[1]': 0x7fffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addikc_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000}, {'GPR[3]': 0x00fe8000, 'PC':0x4, 'MSR':0x00000000})
addikc_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000}, {'GPR[3]': 0x00fe8001, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(addikc_Instr)

#AND instruction family
#AND
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra & (int)rb;
""")
and_Instr = trap.Instruction('AND', True)
and_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
and_Instr.setCode(opCode,'execute')
and_Instr.addBehavior(IncrementPC, 'execute')
and_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x66440044, 'PC':0x4})
isa.addInstruction(and_Instr)

#ANDI
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra & (int)SignExtend(imm, 16);
""")
andi_Instr = trap.Instruction('ANDI', True)
andi_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,0,1]}, 'TODO')
andi_Instr.setCode(opCode,'execute')
andi_Instr.addBehavior(IncrementPC, 'execute')
andi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x6666}, {'GPR[1]': 0xffcc8844, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x00000044, 'PC':0x4})
isa.addInstruction(andi_Instr)

#ANDN
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra & ~((int)rb);
""")
andn_Instr = trap.Instruction('ANDN', True)
andn_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,1,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
andn_Instr.setCode(opCode,'execute')
andn_Instr.addBehavior(IncrementPC, 'execute')
andn_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(andn_Instr)

#ANDNI
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra & ~((int)SignExtend(imm, 16));
""")
andni_Instr = trap.Instruction('ANDNI', True)
andni_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,1,1]}, 'TODO')
andni_Instr.setCode(opCode,'execute')
andni_Instr.addBehavior(IncrementPC, 'execute')
andni_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x6666}, {'GPR[1]': 0xffcc8844, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0xffcc8800, 'PC':0x4})
isa.addInstruction(andni_Instr)

#from here to the end, it is specified for each instruction, only
#the bytecode and the name.
#After, it will be specified also the behavior.

#BRANCH instruction family
#BEQ
opCode = cxx_writer.writer_code.Code("""
if ((int)ra==0) {
	PC = PC + (int)rb;
} else {
	PC = PC + 4;
}
""")
beq_Instr = trap.Instruction('BEQ','True')
beq_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
beq_Instr.setCode(opCode,'execute')
beq_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
beq_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0xfffffff0, 'PC':0x500000}, {'PC':0x4ffff0})
beq_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 1, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500004})
isa.addInstruction(beq_Instr)

#BEQD
opCode = cxx_writer.writer_code.Code("""

""")
beqd_Instr = trap.Instruction('BEQD','True')
beqd_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
beqd_Instr.setCode(opCode,'execute')
isa.addInstruction(beqd_Instr)

#BEQI
opCode = cxx_writer.writer_code.Code("""
if ((int)ra==0) {
	PC = PC + SignExtend(imm,16);
} else {
	PC = PC + 4;
}
""")
beqi_Instr = trap.Instruction('BEQI','True')
beqi_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,0,0]}, 'TODO')
beqi_Instr.setCode(opCode,'execute')
beqi_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x500010})
beqi_Instr.addTest({'ra': 1, 'imm': 0xfff0}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x4ffff0})
beqi_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 1, 'PC':0x500000}, {'PC':0x500004})
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
if ((int)ra>=0) {
	PC = PC + (int)rb;
} else {
	PC = PC + 4;
}
""")
bge_Instr = trap.Instruction('BGE','True')
bge_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,1,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bge_Instr.setCode(opCode,'execute')
bge_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
bge_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0xfffffff0, 'PC':0x500000}, {'PC':0x4ffff0})
bge_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': -5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500004})
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
if ((int)ra>=0) {
	PC = PC + SignExtend(imm,16);
} else {
	PC = PC + 4;
}
""")
bgei_Instr = trap.Instruction('BGEI','True')
bgei_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,1,0,1]}, 'TODO')
bgei_Instr.setCode(opCode,'execute')
bgei_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 5, 'PC':0x500000}, {'PC':0x500010})
bgei_Instr.addTest({'ra': 1, 'imm': 0xfff0}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x4ffff0})
bgei_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': -5, 'PC':0x500000}, {'PC':0x500004})
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
if ((int)ra>0) {
	PC = PC + (int)rb;
} else {
	PC = PC + 4;
}
""")
bgt_Instr = trap.Instruction('BGT','True')
bgt_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bgt_Instr.setCode(opCode,'execute')
bgt_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
bgt_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0xfffffff0, 'PC':0x500000}, {'PC':0x500004})
bgt_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': -5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500004})
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
if ((int)ra>0) {
	PC = PC + SignExtend(imm,16);
} else {
	PC = PC + 4;
}
""")
bgti_Instr = trap.Instruction('BGTI','True')
bgti_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,1,0,0]}, 'TODO')
bgti_Instr.setCode(opCode,'execute')
bgti_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 5, 'PC':0x500000}, {'PC':0x500010})
bgti_Instr.addTest({'ra': 1, 'imm': 0xfff0}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x500004})
bgti_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': -5, 'PC':0x500000}, {'PC':0x500004})
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
if ((int)ra<=0) {
	PC = PC + (int)rb;
} else {
	PC = PC + 4;
}
""")
ble_Instr = trap.Instruction('BLE','True')
ble_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,1,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
ble_Instr.setCode(opCode,'execute')
ble_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500004})
ble_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0xfffffff0, 'PC':0x500000}, {'PC':0x4ffff0})
ble_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': -5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
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
if ((int)ra<=0) {
	PC = PC + SignExtend(imm,16);
} else {
	PC = PC + 4;
}
""")
blei_Instr = trap.Instruction('BLEI','True')
blei_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,1,1]}, 'TODO')
blei_Instr.setCode(opCode,'execute')
blei_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 5, 'PC':0x500000}, {'PC':0x500004})
blei_Instr.addTest({'ra': 1, 'imm': 0xfff0}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x4ffff0})
blei_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': -5, 'PC':0x500000}, {'PC':0x500010})
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
if ((int)ra<0) {
	PC = PC + (int)rb;
} else {
	PC = PC + 4;
}
""")
blt_Instr = trap.Instruction('BLT','True')
blt_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,1,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
blt_Instr.setCode(opCode,'execute')
blt_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500004})
blt_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0xfffffff0, 'PC':0x500000}, {'PC':0x500004})
blt_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': -5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
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
if ((int)ra<0) {
	PC = PC + SignExtend(imm,16);
} else {
	PC = PC + 4;
}
""")
blti_Instr = trap.Instruction('BLTI','True')
blti_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,1,0]}, 'TODO')
blti_Instr.setCode(opCode,'execute')
blti_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 5, 'PC':0x500000}, {'PC':0x500004})
blti_Instr.addTest({'ra': 1, 'imm': 0xfff0}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x500004})
blti_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': -5, 'PC':0x500000}, {'PC':0x500010})
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
if ((int)ra!=0) {
	PC = PC + (int)rb;
} else {
	PC = PC + 4;
}
""")
bne_Instr = trap.Instruction('BNE','True')
bne_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bne_Instr.setCode(opCode,'execute')
bne_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
bne_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0xfffffff0, 'PC':0x500000}, {'PC':0x500004})
bne_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': -5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
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
if ((int)ra!=0) {
	PC = PC + SignExtend(imm,16);
} else {
	PC = PC + 4;
}
""")
bnei_Instr = trap.Instruction('BNEI','True')
bnei_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,0,1]}, 'TODO')
bnei_Instr.setCode(opCode,'execute')
bnei_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 5, 'PC':0x500000}, {'PC':0x500010})
bnei_Instr.addTest({'ra': 1, 'imm': 0xfff0}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x500004})
bnei_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': -5, 'PC':0x500000}, {'PC':0x500010})
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
rd = (unsigned int)ra >> ((int)rb & 0x1f); /* I consider only the five less significant bits */
""")
bsrl_Instr = trap.Instruction('BSRL', True)
bsrl_Instr.setMachineCode(barrel_reg, {'opcode0': [0,1,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bsrl_Instr.setCode(opCode,'execute')
bsrl_Instr.addBehavior(IncrementPC, 'execute')
bsrl_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x151fbb18, 'GPR[2]': 0x7, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x2a3f76, 'PC':0x4})
bsrl_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x151fbb18, 'GPR[2]': 0xf5489fe7, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x2a3f76, 'PC':0x4})
bsrl_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff1fbb18, 'GPR[2]': 0x7, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x1fe3f76, 'PC':0x4})
isa.addInstruction(bsrl_Instr)

#BSRA (S=0, T=1)
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra >> ((int)rb & 0x1f); /* the C shift is Arithmetical! */
""")
bsra_Instr = trap.Instruction('BSRA', True)
bsra_Instr.setMachineCode(barrel_reg, {'opcode0': [0,1,0,0,0,1], 'opcode1': [0,1,0,0,0,0,0,0,0,0,0]}, 'TODO')
bsra_Instr.setCode(opCode,'execute')
bsra_Instr.addBehavior(IncrementPC, 'execute')
bsra_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x151fbb18, 'GPR[2]': 0x7, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x2a3f76, 'PC':0x4})
bsra_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x151fbb18, 'GPR[2]': 0xf5489fe7, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x2a3f76, 'PC':0x4})
bsra_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff1fbb18, 'GPR[2]': 0x7, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0xfffe3f76, 'PC':0x4})
isa.addInstruction(bsra_Instr)

#BSLL (S=1, T=0)
opCode = cxx_writer.writer_code.Code("""
rd = (unsigned int)ra << ((int)rb & 0x1f);
""")
bsll_Instr = trap.Instruction('BSLL', True)
bsll_Instr.setMachineCode(barrel_reg, {'opcode0': [0,1,0,0,0,1], 'opcode1': [1,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
bsll_Instr.setCode(opCode,'execute')
bsll_Instr.addBehavior(IncrementPC, 'execute')
bsll_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x151fbb18, 'GPR[2]': 0x7, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x8fdd8c00, 'PC':0x4})
bsll_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x151fbb18, 'GPR[2]': 0xf5489fe7, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x8fdd8c00, 'PC':0x4})
bsll_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff1fbb18, 'GPR[2]': 0x7, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x8fdd8c00, 'PC':0x4})
isa.addInstruction(bsll_Instr)

#BSRLI (S=0, T=0)
opCode = cxx_writer.writer_code.Code("""
rd = (unsigned int)ra >> (unsigned int)imm;
""")
bsrli_Instr = trap.Instruction('BSRLI', True)
bsrli_Instr.setMachineCode(barrel_imm, {'opcode0': [0,1,1,0,0,1], 'opcode1': [0,0,0,0,0,0]}, 'TODO')
bsrli_Instr.setCode(opCode,'execute')
bsrli_Instr.addBehavior(IncrementPC, 'execute')
bsrli_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 7}, {'GPR[1]': 0x151fbb18, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x2a3f76, 'PC':0x4})
bsrli_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 7}, {'GPR[1]': 0xff1fbb18, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x1fe3f76, 'PC':0x4})
isa.addInstruction(bsrli_Instr)

#BSRAI (S=0, T=1)
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra >> (unsigned int)imm;
""")
bsrai_Instr = trap.Instruction('BSRAI', True)
bsrai_Instr.setMachineCode(barrel_imm, {'opcode0': [0,1,1,0,0,1], 'opcode1': [0,1,0,0,0,0]}, 'TODO')
bsrai_Instr.setCode(opCode,'execute')
bsrai_Instr.addBehavior(IncrementPC, 'execute')
bsrai_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 7}, {'GPR[1]': 0x151fbb18, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x2a3f76, 'PC':0x4})
bsrai_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 7}, {'GPR[1]': 0xff1fbb18, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0xfffe3f76, 'PC':0x4})
isa.addInstruction(bsrai_Instr)

#BSLLI (S=0, T=1)
opCode = cxx_writer.writer_code.Code("""
rd = (unsigned int)ra << (unsigned int)imm;
""")
bslli_Instr = trap.Instruction('BSLLI', True)
bslli_Instr.setMachineCode(barrel_imm, {'opcode0': [0,1,1,0,0,1], 'opcode1': [1,0,0,0,0,0]}, 'TODO')
bslli_Instr.setCode(opCode,'execute')
bslli_Instr.addBehavior(IncrementPC, 'execute')
bslli_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 7}, {'GPR[1]': 0x151fbb18, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x8fdd8c00, 'PC':0x4})
bslli_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 7}, {'GPR[1]': 0xff1fbb18, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x8fdd8c00, 'PC':0x4})
isa.addInstruction(bslli_Instr)

#COMPARE family
#CMP
opCode = cxx_writer.writer_code.Code("""
int result = (int)rb - (int)ra;
if ((int)ra > (int) rb) {
	result |= 0x80000000;
} else {
	result &= 0x7fffffff;
}
rd = result;
""")
cmp_Instr = trap.Instruction('CMP', True)
cmp_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,1]}, 'TODO')
cmp_Instr.setCode(opCode,'execute')
cmp_Instr.addBehavior(IncrementPC, 'execute')
cmp_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0xffffd999, 'PC':0x4})
cmp_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xfffea385, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0xfffda652, 'PC':0x4})
cmp_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x15c7b, 'GPR[2]': 0xffff02cd, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0xfffda652, 'PC':0x4})
isa.addInstruction(cmp_Instr)

#CMPU
opCode = cxx_writer.writer_code.Code("""
unsigned int result = (unsigned int)rb - (unsigned int)ra;
if ((unsigned int)ra > (unsigned int) rb) {
	result |= 0x80000000;
} else {
	result &= 0x7fffffff;
}
rd = result;
""")
cmpu_Instr = trap.Instruction('CMPU', True)
cmpu_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,1,1]}, 'TODO')
cmpu_Instr.setCode(opCode,'execute')
cmpu_Instr.addBehavior(IncrementPC, 'execute')
cmpu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0xffffd999, 'PC':0x4})
cmpu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xfffea385, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x7ffda652, 'PC':0x4})
cmpu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x15c7b, 'GPR[2]': 0xffff02cd, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x7ffda652, 'PC':0x4})
isa.addInstruction(cmpu_Instr)

#FLOAT family
#FADD
opCode = cxx_writer.writer_code.Code("""

""")
fadd_Instr = trap.Instruction('FADD', True)
fadd_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
fadd_Instr.setCode(opCode,'execute')
isa.addInstruction(fadd_Instr)

#FRSUB
opCode = cxx_writer.writer_code.Code("""

""")
frsub_Instr = trap.Instruction('FRSUB', True)
frsub_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,0,0,1,0,0,0,0,0,0,0]}, 'TODO')
frsub_Instr.setCode(opCode,'execute')
isa.addInstruction(frsub_Instr)

#FMUL
opCode = cxx_writer.writer_code.Code("""

""")
fmul_Instr = trap.Instruction('FMUL', True)
fmul_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,0,1,0,0,0,0,0,0,0,0]}, 'TODO')
fmul_Instr.setCode(opCode,'execute')
isa.addInstruction(fmul_Instr)

#FDIV
opCode = cxx_writer.writer_code.Code("""

""")
fdiv_Instr = trap.Instruction('FDIV', True)
fdiv_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,0,1,1,0,0,0,0,0,0,0]}, 'TODO')
fdiv_Instr.setCode(opCode,'execute')
isa.addInstruction(fdiv_Instr)

#FCMP
opCode = cxx_writer.writer_code.Code("""

""")
fcmp_Instr = trap.Instruction('FCMP', True)
fcmp_Instr.setMachineCode(float_cmp, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,1,0,0], 'opcode2': [0,0,0,0]}, 'TODO')
fcmp_Instr.setCode(opCode,'execute')
isa.addInstruction(fcmp_Instr)

#FLT
opCode = cxx_writer.writer_code.Code("""

""")
flt_Instr = trap.Instruction('FLT', True)
flt_Instr.setMachineCode(float_unary, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,1,0,1,0,0,0,0,0,0,0]}, 'TODO')
flt_Instr.setCode(opCode,'execute')
isa.addInstruction(flt_Instr)

#FINT
opCode = cxx_writer.writer_code.Code("""

""")
fint_Instr = trap.Instruction('FINT', True)
fint_Instr.setMachineCode(float_unary, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,1,1,0,0,0,0,0,0,0,0]}, 'TODO')
fint_Instr.setCode(opCode,'execute')
isa.addInstruction(fint_Instr)

#FSQRT
opCode = cxx_writer.writer_code.Code("""

""")
fsqrt_Instr = trap.Instruction('FSQRT', True)
fsqrt_Instr.setMachineCode(float_unary, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,1,1,1,0,0,0,0,0,0,0]}, 'TODO')
fsqrt_Instr.setCode(opCode,'execute')
isa.addInstruction(fsqrt_Instr)

#GET / GETD
#very strange instructions :)

#IDIV
opCode = cxx_writer.writer_code.Code("""

""")
idiv_Instr = trap.Instruction('IDIV', True)
idiv_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
idiv_Instr.setCode(opCode,'execute')
isa.addInstruction(idiv_Instr)

#IDIVU
opCode = cxx_writer.writer_code.Code("""

""")
idivu_Instr = trap.Instruction('IDIVU', True)
idivu_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,0]}, 'TODO')
idivu_Instr.setCode(opCode,'execute')
isa.addInstruction(idivu_Instr)

#IMM
opCode = cxx_writer.writer_code.Code("""

""")
imm_Instr = trap.Instruction('IMM', True)
imm_Instr.setMachineCode(imm_code, {'opcode': [1,0,1,1,0,0]}, 'TODO')
imm_Instr.setCode(opCode,'execute')
isa.addInstruction(imm_Instr)

#LOAD family
#LBU
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)rb;
rd = dataMem.read_byte(addr);
rd &= 0x000000ff;
""")
lbu_Instr = trap.Instruction('LBU', True)
lbu_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
lbu_Instr.setCode(opCode,'execute')
lbu_Instr.addBehavior(IncrementPC, 'execute')
lbu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0}, {'GPR[3]': 0xff, 'PC' : 0x4})
lbu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0}, {'GPR[3]': 0x44, 'PC' : 0x4})
lbu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456cd, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0}, {'GPR[3]': 0xff, 'PC' : 0x4})
isa.addInstruction(lbu_Instr)

#LBUI
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + SignExtend(imm,16);
rd = dataMem.read_byte(addr);
rd &= 0x000000ff;
""")
lbui_Instr = trap.Instruction('LBUI', True)
lbui_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,0,0,0]}, 'TODO')
lbui_Instr.setCode(opCode,'execute')
lbui_Instr.addBehavior(IncrementPC, 'execute')
lbui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x20}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0}, {'GPR[3]': 0xff, 'PC' : 0x4})
lbui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0}, {'GPR[3]': 0x44, 'PC' : 0x4})
lbui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456cd, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0}, {'GPR[3]': 0xff, 'PC' : 0x4})
isa.addInstruction(lbui_Instr)

#LHU
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)rb;
if ( (addr & 0x00000001) != 0 ) {
	ESR[key_EC] = 0x1;
	ESR[key_W] = 0x0;
	ESR[key_S] = 0x0;
	ESR[key_Rx] = rd_bit; /* the value that identifies rd */
} else {
	rd = dataMem.read_half(addr);
	rd &= 0x0000ffff;
}
""")
lhu_Instr = trap.Instruction('LHU', True)
lhu_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
lhu_Instr.setCode(opCode,'execute')
lhu_Instr.addBehavior(IncrementPC, 'execute')
lhu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x1111, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0x0000ff44, 'PC' : 0x4, 'ESR': 0x0})
lhu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x1111, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0x1111, 'PC' : 0x4, 'ESR': 0x80D00000})
lhu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x22, 'GPR[3]' : 0x1111, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0x0000ff44, 'PC' : 0x4, 'ESR': 0x0})
lhu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x13, 'GPR[2]' : 0x21, 'GPR[3]' : 0x1111, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0x0000ff44, 'PC' : 0x4, 'ESR': 0x0})
isa.addInstruction(lhu_Instr)

#LHUI
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + SignExtend(imm,16);
if ( (addr & 0x00000001) != 0 ) {
	ESR[key_EC] = 0x1;
	ESR[key_W] = 0x0;
	ESR[key_S] = 0x0;
	ESR[key_Rx] = rd_bit; /* the value that identifies rd */
} else {
	rd = dataMem.read_half(addr);
	rd &= 0x0000ffff;
}
""")
lhui_Instr = trap.Instruction('LHUI', True)
lhui_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,0,0,1]}, 'TODO')
lhui_Instr.setCode(opCode,'execute')
lhui_Instr.addBehavior(IncrementPC, 'execute')
lhui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x20}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0x0000ff44, 'PC' : 0x4, 'ESR': 0x0})
lhui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0x1111, 'PC' : 0x4, 'ESR': 0x80D00000})
lhui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x22}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0x0000ff44, 'PC' : 0x4, 'ESR': 0x0})
lhui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x13, 'GPR[3]' : 0x1111, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0x0000ff44, 'PC' : 0x4, 'ESR': 0x0})
isa.addInstruction(lhui_Instr)

#LW
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)rb;
if ( (addr & 0x00000003) != 0 ) {
	ESR[key_EC] = 0x1;
	ESR[key_W] = 0x1;
	ESR[key_S] = 0x0;
	ESR[key_Rx] = rd_bit; /* the value that identifies rd */
} else {
	rd = dataMem.read_word(addr);
}
""")
lw_Instr = trap.Instruction('LW', True)
lw_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
lw_Instr.setCode(opCode,'execute')
lw_Instr.addBehavior(IncrementPC, 'execute')
lw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x1111, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0xff445566, 'PC' : 0x4, 'ESR': 0x0})
lw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x1111, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0x1111, 'PC' : 0x4, 'ESR': 0x80D00000})
lw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x22, 'GPR[3]' : 0x1111, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0x1111, 'PC' : 0x4, 'ESR': 0x80D00000})
lw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x13, 'GPR[2]' : 0x21, 'GPR[3]' : 0x1111, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0xff445566, 'PC' : 0x4, 'ESR': 0x0})
isa.addInstruction(lw_Instr)

#LWI
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + SignExtend(imm,16);
if ( (addr & 0x00000003) != 0 ) {
	ESR[key_EC] = 0x1;
	ESR[key_W] = 0x1;
	ESR[key_S] = 0x0;
	ESR[key_Rx] = rd_bit; /* the value that identifies rd */
} else {
	rd = dataMem.read_word(addr);
}
""")
lwi_Instr = trap.Instruction('LWI', True)
lwi_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,0,1,0]}, 'TODO')
lwi_Instr.setCode(opCode,'execute')
lwi_Instr.addBehavior(IncrementPC, 'execute')
lwi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x20}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0xff445566, 'PC' : 0x4, 'ESR': 0x0})
lwi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0x1111, 'PC' : 0x4, 'ESR': 0x80D00000})
lwi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x22}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0x1111, 'PC' : 0x4, 'ESR': 0x80D00000})
lwi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x13, 'GPR[3]' : 0x1111, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'GPR[3]' : 0xff445566, 'PC' : 0x4, 'ESR': 0x0})
isa.addInstruction(lwi_Instr)

#MFS
opCode = cxx_writer.writer_code.Code("""

""")
mfs_Instr = trap.Instruction('MFS', True)
mfs_Instr.setMachineCode(mfs_code, {'opcode': [1,0,0,1,0,1]}, 'TODO')
mfs_Instr.setCode(opCode,'execute')
isa.addInstruction(mfs_Instr)

#MSRCLR
opCode = cxx_writer.writer_code.Code("""

""")
msrclr_Instr = trap.Instruction('MSRCLR', True)
msrclr_Instr.setMachineCode(msr_oper, {'opcode0': [1,0,0,1,0,1], 'opcode1': [0,0,0,0,1,0]}, 'TODO')
msrclr_Instr.setCode(opCode,'execute')
isa.addInstruction(msrclr_Instr)

#MSRSET
opCode = cxx_writer.writer_code.Code("""

""")
msrset_Instr = trap.Instruction('MSRSET', True)
msrset_Instr.setMachineCode(msr_oper, {'opcode0': [1,0,0,1,0,1], 'opcode1': [0,0,0,0,0,0]}, 'TODO')
msrset_Instr.setCode(opCode,'execute')
isa.addInstruction(msrset_Instr)

#MTS
opCode = cxx_writer.writer_code.Code("""

""")
mts_Instr = trap.Instruction('MTS', True)
mts_Instr.setMachineCode(mts_code, {'opcode': [1,0,0,1,0,1]}, 'TODO')
mts_Instr.setCode(opCode,'execute')
isa.addInstruction(mts_Instr)

#MUL
opCode = cxx_writer.writer_code.Code("""

""")
mul_Instr = trap.Instruction('MUL', True)
mul_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
mul_Instr.setCode(opCode,'execute')
isa.addInstruction(mul_Instr)

#MULH
opCode = cxx_writer.writer_code.Code("""

""")
mulh_Instr = trap.Instruction('MULH', True)
mulh_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,1]}, 'TODO')
mulh_Instr.setCode(opCode,'execute')
isa.addInstruction(mulh_Instr)

#MULHU
opCode = cxx_writer.writer_code.Code("""

""")
mulhu_Instr = trap.Instruction('MULHU', True)
mulhu_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,1]}, 'TODO')
mulhu_Instr.setCode(opCode,'execute')
isa.addInstruction(mulhu_Instr)

#MULHSU
opCode = cxx_writer.writer_code.Code("""

""")
mulhsu_Instr = trap.Instruction('MULHSU', True)
mulhsu_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,0]}, 'TODO')
mulhsu_Instr.setCode(opCode,'execute')
isa.addInstruction(mulhsu_Instr)

#MULI
opCode = cxx_writer.writer_code.Code("""

""")
muli_Instr = trap.Instruction('MULI', True)
muli_Instr.setMachineCode(oper_imm, {'opcode': [0,1,1,0,0,0]}, 'TODO')
muli_Instr.setCode(opCode,'execute')
isa.addInstruction(muli_Instr)

#OR
opCode = cxx_writer.writer_code.Code("""

""")
or_Instr = trap.Instruction('OR', True)
or_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
or_Instr.setCode(opCode,'execute')
isa.addInstruction(or_Instr)

#ORI
opCode = cxx_writer.writer_code.Code("""

""")
ori_Instr = trap.Instruction('ORI', True)
ori_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,0,0]}, 'TODO')
ori_Instr.setCode(opCode,'execute')
isa.addInstruction(ori_Instr)

#PCMPBF
opCode = cxx_writer.writer_code.Code("""
if ( ((int)rb & 0xff000000) == ((int)ra & 0xff000000) )
	rd = 0x1;
else if ( ((int)rb & 0x00ff0000) == ((int)ra & 0x00ff0000) )
	rd = 0x2;
else if ( ((int)rb & 0x0000ff00) == ((int)ra & 0x0000ff00) )
	rd = 0x3;
else if ( ((int)rb & 0x000000ff) == ((int)ra & 0x000000ff) )
	rd = 0x4;
else
	rd = 0x0;
""")
pcmpbf_Instr = trap.Instruction('PCMPBF', True)
pcmpbf_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,0,0], 'opcode1': [1,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
pcmpbf_Instr.setCode(opCode,'execute')
pcmpbf_Instr.addBehavior(IncrementPC, 'execute')
pcmpbf_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xffffffff, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x0, 'PC':0x4})
pcmpbf_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0x12ffffff, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x1, 'PC':0x4})
pcmpbf_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xff34ffff, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x2, 'PC':0x4})
pcmpbf_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xfffffeff, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x3, 'PC':0x4})
pcmpbf_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xffffffdc, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x4, 'PC':0x4})
pcmpbf_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xff34ffdc, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x2, 'PC':0x4})
isa.addInstruction(pcmpbf_Instr)

#PCMPEQ
opCode = cxx_writer.writer_code.Code("""
rd = ((int)rb == (int)ra);
""")
pcmpeq_Instr = trap.Instruction('PCMPEQ', True)
pcmpeq_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,1,0], 'opcode1': [1,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
pcmpeq_Instr.setCode(opCode,'execute')
pcmpeq_Instr.addBehavior(IncrementPC, 'execute')
pcmpeq_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0x1234fedc, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x1, 'PC':0x4})
pcmpeq_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xffffffff, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x0, 'PC':0x4})
isa.addInstruction(pcmpeq_Instr)

#PCMPNE
opCode = cxx_writer.writer_code.Code("""
rd = ((int)rb != (int)ra);
""")
pcmpne_Instr = trap.Instruction('PCMPNE', True)
pcmpne_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,1,1], 'opcode1': [1,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
pcmpne_Instr.setCode(opCode,'execute')
pcmpne_Instr.addBehavior(IncrementPC, 'execute')
pcmpne_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0x1234fedc, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x0, 'PC':0x4})
pcmpne_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xffffffff, 'GPR[3]': 0xfffff, 'PC':0x0}, {'GPR[3]': 0x1, 'PC':0x4})
isa.addInstruction(pcmpne_Instr)

#PUT / PUTD
#very strange instructions :)

#RSUB instruction family
#RSUB
opCode = cxx_writer.writer_code.Code("""

""")
rsub_Instr = trap.Instruction('RSUB', True)
rsub_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
rsub_Instr.setCode(opCode,'execute')
isa.addInstruction(rsub_Instr)

# RSUBC
opCode = cxx_writer.writer_code.Code("""

""")
rsubc_Instr = trap.Instruction('RSUBC', True)
rsubc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,1,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
rsubc_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubc_Instr)

# RSUBK
opCode = cxx_writer.writer_code.Code("""

""")
rsubk_Instr = trap.Instruction('RSUBK', True)
rsubk_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
rsubk_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubk_Instr)

# RSUBKC
opCode = cxx_writer.writer_code.Code("""

""")
rsubkc_Instr = trap.Instruction('RSUBKC', True)
rsubkc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,1,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
rsubkc_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubkc_Instr)

#RSUBI instruction family
#RSUBI
opCode = cxx_writer.writer_code.Code("""

""")
rsubi_Instr = trap.Instruction('RSUBI', True)
rsubi_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,0,1]}, 'TODO')
rsubi_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubi_Instr)

#RSUBIC
opCode = cxx_writer.writer_code.Code("""

""")
rsubic_Instr = trap.Instruction('RSUBIC', True)
rsubic_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,1,1]}, 'TODO')
rsubic_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubic_Instr)

#RSUBIK
opCode = cxx_writer.writer_code.Code("""

""")
rsubik_Instr = trap.Instruction('RSUBIK', True)
rsubik_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,0,1]}, 'TODO')
rsubik_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubik_Instr)

#RSUBIKC
opCode = cxx_writer.writer_code.Code("""

""")
rsubikc_Instr = trap.Instruction('RSUBIKC', True)
rsubikc_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,1,1]}, 'TODO')
rsubikc_Instr.setCode(opCode,'execute')
isa.addInstruction(rsubikc_Instr)

#RETURN instruction family
#RTBD
opCode = cxx_writer.writer_code.Code("""

""")
rtbd_Instr = trap.Instruction('RTBD','True')
rtbd_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,0,1], 'opcode1': [1,0,0,1,0]}, 'TODO')
rtbd_Instr.setCode(opCode,'execute')
isa.addInstruction(rtbd_Instr)

#RTID
opCode = cxx_writer.writer_code.Code("""

""")
rtid_Instr = trap.Instruction('RTID','True')
rtid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,0,1], 'opcode1': [1,0,0,0,1]}, 'TODO')
rtid_Instr.setCode(opCode,'execute')
isa.addInstruction(rtid_Instr)

#RTED
opCode = cxx_writer.writer_code.Code("""

""")
rted_Instr = trap.Instruction('RTED','True')
rted_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,0,1], 'opcode1': [1,0,1,0,0]}, 'TODO')
rted_Instr.setCode(opCode,'execute')
isa.addInstruction(rted_Instr)

#RTSD
opCode = cxx_writer.writer_code.Code("""

""")
rtsd_Instr = trap.Instruction('RTSD','True')
rtsd_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,0,1], 'opcode1': [1,0,0,0,0]}, 'TODO')
rtsd_Instr.setCode(opCode,'execute')
isa.addInstruction(rtsd_Instr)

#STORE instruction family
#SB
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)rb;
dataMem.write_byte(addr, (unsigned char)(rd & 0x000000ff));
""")
sb_Instr = trap.Instruction('SB', True)
sb_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
sb_Instr.setCode(opCode,'execute')
sb_Instr.addBehavior(IncrementPC, 'execute')
sb_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0}, {'dataMem[0x30]': 0xab445566, 'PC' : 0x4})
sb_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0}, {'dataMem[0x30]': 0xffab5566, 'PC' : 0x4})
sb_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0}, {'dataMem[0x31]': 0xab445566, 'PC' : 0x4})
isa.addInstruction(sb_Instr)

#SBI
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + SignExtend(imm,16);
dataMem.write_byte(addr, (unsigned char)(rd & 0x000000ff));
""")
sbi_Instr = trap.Instruction('SBI', True)
sbi_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,1,0,0]}, 'TODO')
sbi_Instr.setCode(opCode,'execute')
sbi_Instr.addBehavior(IncrementPC, 'execute')
sbi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x20}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0}, {'dataMem[0x30]': 0xab445566, 'PC' : 0x4})
sbi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0}, {'dataMem[0x30]': 0xffab5566, 'PC' : 0x4})
sbi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0}, {'dataMem[0x31]': 0xab445566, 'PC' : 0x4})
isa.addInstruction(sbi_Instr)

#SH
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)rb;
if ( ( addr & 0x00000001 ) != 0 ) {
	ESR[key_EC] = 0x1;
	ESR[key_W] = 0x0;
	ESR[key_S] = 0x1;
	ESR[key_Rx] = rd_bit; /* the value that identifies rd */
} else {
	dataMem.write_half(addr, (unsigned int)(rd & 0x0000ffff));
}
""")
sh_Instr = trap.Instruction('SH', True)
sh_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,1,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
sh_Instr.setCode(opCode,'execute')
sh_Instr.addBehavior(IncrementPC, 'execute')
sh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x30]': 0x56ab5566, 'PC' : 0x4, 'ESR': 0x0})
sh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x31]': 0xff445566, 'PC' : 0x4, 'ESR': 0x80D00000})
sh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x22, 'GPR[3]' : 0x123456ab, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x32]': 0x56ab5566, 'PC' : 0x4, 'ESR': 0x0})
sh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x13, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x34]': 0x56ab5566, 'PC' : 0x4, 'ESR': 0x0})
isa.addInstruction(sh_Instr)

#SHI
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + SignExtend(imm,16);
if ( ( addr & 0x00000001 ) != 0 ) {
	ESR[key_EC] = 0x1;
	ESR[key_W] = 0x0;
	ESR[key_S] = 0x1;
	ESR[key_Rx] = rd_bit; /* the value that identifies rd */
} else {
	dataMem.write_half(addr, (unsigned int)(rd & 0x0000ffff));
}
""")
shi_Instr = trap.Instruction('SHI', True)
shi_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,1,0,1]}, 'TODO')
shi_Instr.setCode(opCode,'execute')
shi_Instr.addBehavior(IncrementPC, 'execute')
shi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x20}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x30]': 0x56ab5566, 'PC' : 0x4, 'ESR': 0x0})
shi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x31]': 0xff445566, 'PC' : 0x4, 'ESR': 0x80D00000})
shi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x22}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x32]': 0x56ab5566, 'PC' : 0x4, 'ESR': 0x0})
shi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x13, 'GPR[3]' : 0x123456ab, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x34]': 0x56ab5566, 'PC' : 0x4, 'ESR': 0x0})
isa.addInstruction(shi_Instr)

#SW
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)rb;
if ( ( addr & 0x00000003 ) != 0 ) {
	ESR[key_EC] = 0x1;
	ESR[key_W] = 0x1;
	ESR[key_S] = 0x1;
	ESR[key_Rx] = rd_bit; /* the value that identifies rd */
} else {
	dataMem.write_word(addr, (unsigned int)(rd));
}
""")
sw_Instr = trap.Instruction('SW', True)
sw_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,1,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
sw_Instr.setCode(opCode,'execute')
sw_Instr.addBehavior(IncrementPC, 'execute')
sw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x30]': 0x123456ab, 'PC' : 0x4, 'ESR': 0x0})
sw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x31]': 0xff445566, 'PC' : 0x4, 'ESR': 0x80D00000})
sw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x22, 'GPR[3]' : 0x123456ab, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x32]': 0xff445566, 'PC' : 0x4, 'ESR': 0x80D00000})
sw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x13, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x34]': 0x123456ab, 'PC' : 0x4, 'ESR': 0x0})
isa.addInstruction(sw_Instr)

#SWI
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + SignExtend(imm,16);
if ( ( addr & 0x00000003 ) != 0 ) {
	ESR[key_EC] = 0x1;
	ESR[key_W] = 0x1;
	ESR[key_S] = 0x1;
	ESR[key_Rx] = rd_bit; /* the value that identifies rd */
} else {
	dataMem.write_word(addr, (unsigned int)(rd));
}
""")
swi_Instr = trap.Instruction('SWI', True)
swi_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,1,1,0]}, 'TODO')
swi_Instr.setCode(opCode,'execute')
swi_Instr.addBehavior(IncrementPC, 'execute')
swi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x20}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x30]': 0x123456ab, 'PC' : 0x4, 'ESR': 0x0})
swi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x31]': 0xff445566, 'PC' : 0x4, 'ESR': 0x80D00000})
swi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x22}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x32]': 0xff445566, 'PC' : 0x4, 'ESR': 0x80D00000})
swi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x13, 'GPR[3]' : 0x123456ab, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0}, {'dataMem[0x34]': 0x123456ab, 'PC' : 0x4, 'ESR': 0x0})
isa.addInstruction(swi_Instr)

#SEXT16
opCode = cxx_writer.writer_code.Code("""
if ( ( (int)ra & 0x00008000 ) != 0) {
	rd = (int)ra | 0xffff0000;
} else {
	rd = (int)ra & 0x0000ffff;
}
""")
sext16_Instr = trap.Instruction('SEXT16', True)
sext16_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1]}, 'TODO')
sext16_Instr.setCode(opCode,'execute')
sext16_Instr.addBehavior(IncrementPC, 'execute')
sext16_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0x6666, 'GPR[3]' : 0xffff, 'PC' : 0x0}, {'GPR[3]': 0x00006666, 'PC' : 0x4})
sext16_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0xabcd7777, 'GPR[3]' : 0xffff, 'PC' : 0x0}, {'GPR[3]': 0x00007777, 'PC' : 0x4})
sext16_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0xabcd8777, 'GPR[3]' : 0xffff, 'PC' : 0x0}, {'GPR[3]': 0xffff8777, 'PC' : 0x4})
isa.addInstruction(sext16_Instr)

#SEXT8
opCode = cxx_writer.writer_code.Code("""
if ( ( (int)ra & 0x00000080 ) != 0) {
	rd = (int)ra | 0xffffff00;
} else {
	rd = (int)ra & 0x000000ff;
}
""")
sext8_Instr = trap.Instruction('SEXT8', True)
sext8_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0]}, 'TODO')
sext8_Instr.setCode(opCode,'execute')
sext8_Instr.addBehavior(IncrementPC, 'execute')
sext8_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0x6666, 'GPR[3]' : 0xffff, 'PC' : 0x0}, {'GPR[3]': 0x00000066, 'PC' : 0x4})
sext8_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0xabcd7777, 'GPR[3]' : 0xffff, 'PC' : 0x0}, {'GPR[3]': 0x00000077, 'PC' : 0x4})
sext8_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0xabcd7787, 'GPR[3]' : 0xffff, 'PC' : 0x0}, {'GPR[3]': 0xffffff87, 'PC' : 0x4})
isa.addInstruction(sext8_Instr)

#SRA
opCode = cxx_writer.writer_code.Code("""

""")
sra_Instr = trap.Instruction('SRA', True)
sra_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]}, 'TODO')
sra_Instr.setCode(opCode,'execute')
isa.addInstruction(sra_Instr)

#SRC
opCode = cxx_writer.writer_code.Code("""

""")
src_Instr = trap.Instruction('SRC', True)
src_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1]}, 'TODO')
src_Instr.setCode(opCode,'execute')
isa.addInstruction(src_Instr)

#SRL
opCode = cxx_writer.writer_code.Code("""

""")
srl_Instr = trap.Instruction('SRL', True)
srl_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1]}, 'TODO')
srl_Instr.setCode(opCode,'execute')
isa.addInstruction(srl_Instr)

#WDC
opCode = cxx_writer.writer_code.Code("""
/* This instruction is related to the Cache. Since we don't have
   Cache in our model, we simply ignore the implementation of 
   this instruction. */
""")
wdc_Instr = trap.Instruction('WDC', True)
wdc_Instr.setMachineCode(cache_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,1,1,0,0,1,0,0]}, 'TODO')
wdc_Instr.setCode(opCode,'execute')
wdc_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(wdc_Instr)

#WIC
opCode = cxx_writer.writer_code.Code("""
/* This instruction is related to the Cache. Since we don't have
   Cache in our model, we simply ignore the implementation of 
   this instruction. */
""")
wic_Instr = trap.Instruction('WIC', True)
wic_Instr.setMachineCode(cache_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,1,1,0,1,0,0,0]}, 'TODO')
wic_Instr.setCode(opCode,'execute')
wic_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(wic_Instr)

#XOR
opCode = cxx_writer.writer_code.Code("""

""")
xor_Instr = trap.Instruction('XOR', True)
xor_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
xor_Instr.setCode(opCode,'execute')
isa.addInstruction(xor_Instr)

#XORI
opCode = cxx_writer.writer_code.Code("""

""")
xori_Instr = trap.Instruction('XORI', True)
xori_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,1,0]}, 'TODO')
xori_Instr.setCode(opCode,'execute')
isa.addInstruction(xori_Instr)
