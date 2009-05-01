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
isa.addMethod(handleMemoryException_method)
isa.addMethod(handleUserPermissionException_method)


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
add_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('add r', '%rd', ' r', '%ra', ' r', '%rb'))
add_Instr.setCode(opCode,'execute')
add_Instr.addBehavior(IMM_reset, 'execute')
add_Instr.addBehavior(IncrementPC, 'execute')
add_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
add_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
add_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
add_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x3, 'PC':0x4, 'MSR':0x20000000})
add_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x7f000000, 'PC':0x4, 'MSR':0x20000000})
add_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0x50}, {'GPR[3]': 10, 'PC':0x50, 'MSR':0x00000000, 'TARGET':0xffffffff})
add_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0x50, 'IMMREG': 0x8000abcd}, {'GPR[3]': 10, 'PC':0x50, 'MSR':0x00000000, 'TARGET':0xffffffff, 'IMMREG': 0x0000abcd})
isa.addInstruction(add_Instr)

# ADDC
opCode = cxx_writer.writer_code.Code("""
long long result = (long long)((int)ra) + (long long)((int)rb) + (long long)MSR[key_C];
MSR[key_C] = ((ra^rb^(int)(result >> 1)) & 0x80000000) != 0;
rd = (int)result;
""")
addc_Instr = trap.Instruction('ADDC', True)
addc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('addc r', '%rd', ' r', '%ra', ' r', '%rb'))
addc_Instr.setCode(opCode,'execute')
addc_Instr.addBehavior(IMM_reset, 'execute')
addc_Instr.addBehavior(IncrementPC, 'execute')
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 11, 'PC':0x4, 'MSR':0x00000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x3, 'PC':0x4, 'MSR':0x20000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x7f000000, 'PC':0x4, 'MSR':0x20000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x80000002, 'PC':0x4, 'MSR':0x00000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x4, 'PC':0x4, 'MSR':0x20000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x7f000001, 'PC':0x4, 'MSR':0x20000000})
addc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfffffffe, 'GPR[2]': 0x00000001, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x00000000, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(addc_Instr)

# ADDK
opCode = cxx_writer.writer_code.Code("""
rd = (int)rb + (int)ra;
""")
addk_Instr = trap.Instruction('ADDK', True)
addk_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('addk r', '%rd', ' r', '%ra', ' r', '%rb'))
addk_Instr.setCode(opCode,'execute')
addk_Instr.addBehavior(IMM_reset, 'execute')
addk_Instr.addBehavior(IncrementPC, 'execute')
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x20000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x3, 'PC':0x4, 'MSR':0x00000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x7f000000, 'PC':0x4, 'MSR':0x00000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x20000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x3, 'PC':0x4, 'MSR':0x20000000})
addk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x7f000000, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(addk_Instr)

# ADDKC
opCode = cxx_writer.writer_code.Code("""
rd = (int)rb + (int)ra +(int)MSR[key_C];
""")
addkc_Instr = trap.Instruction('ADDKC', True)
addkc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('addkc r', '%rd', ' r', '%ra', ' r', '%rb'))
addkc_Instr.setCode(opCode,'execute')
addkc_Instr.addBehavior(IMM_reset, 'execute')
addkc_Instr.addBehavior(IncrementPC, 'execute')
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 11, 'PC':0x4, 'MSR':0x20000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x3, 'PC':0x4, 'MSR':0x00000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x7f000000, 'PC':0x4, 'MSR':0x00000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x7fffffff, 'GPR[2]': 0x2, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x80000002, 'PC':0x4, 'MSR':0x20000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffffffff, 'GPR[2]': 0x4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x4, 'PC':0x4, 'MSR':0x20000000})
addkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff000000, 'GPR[2]': 0x80000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x7f000001, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(addkc_Instr)

#ADDI instruction family
#ADDI
opCode = cxx_writer.writer_code.Code("""
long long result = (long long)((int)ra) + ((long long)(int)imm_value);
MSR[key_C] = ((ra^imm_value^(int)(result >> 1)) & 0x80000000) != 0;
rd = (int)result;
""")
addi_Instr = trap.Instruction('ADDI', True)
addi_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,0,0]}, ('addi r', '%rd', ' r', '%ra', ' ', '%imm'))
addi_Instr.setCode(opCode,'execute')
addi_Instr.addBehavior(IMM_handler, 'execute')
addi_Instr.addBehavior(IncrementPC, 'execute')
addi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff, 'IMMREG':0x0}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff, 'IMMREG':0x0}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0002}, {'GPR[1]': 0x7fffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff, 'IMMREG':0x0}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff, 'IMMREG':0x0}, {'GPR[3]': 0x00fe8000, 'PC':0x4, 'MSR':0x20000000})
addi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff, 'IMMREG':0x0}, {'GPR[3]': 0x00fe8000, 'PC':0x4, 'MSR':0x20000000})
addi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 0, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff, 'IMMREG':0x80001234}, {'GPR[3]': 0x12340006, 'PC':0x4, 'MSR':0x00000000})
isa.addInstruction(addi_Instr)

#ADDIC
opCode = cxx_writer.writer_code.Code("""
long long result = (long long)((int)ra) + ((long long)(int)imm_value) + (long long)MSR[key_C];
MSR[key_C] = ((ra^imm_value^(int)(result >> 1)) & 0x80000000) != 0;
rd = (int)result;
""")
addic_Instr = trap.Instruction('ADDIC', True)
addic_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,1,0]}, ('addic r', '%rd', ' r', '%ra', ' ', '%imm'))
addic_Instr.setCode(opCode,'execute')
addic_Instr.addBehavior(IMM_handler, 'execute')
addic_Instr.addBehavior(IncrementPC, 'execute')
addic_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addic_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 11, 'PC':0x4, 'MSR':0x00000000})
addic_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0002}, {'GPR[1]': 0x7fffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addic_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x00fe8000, 'PC':0x4, 'MSR':0x20000000})
addic_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x00fe8001, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(addic_Instr)

#ADDIK
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra + (int)imm_value;
""")
addik_Instr = trap.Instruction('ADDIK', True)
addik_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,0,0]}, ('addik r', '%rd', ' r', '%ra', ' ', '%imm'))
addik_Instr.setCode(opCode,'execute')
addik_Instr.addBehavior(IMM_handler, 'execute')
addik_Instr.addBehavior(IncrementPC, 'execute')
addik_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addik_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x20000000})
addik_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0002}, {'GPR[1]': 0x7fffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addik_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x00fe8000, 'PC':0x4, 'MSR':0x00000000})
addik_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x00fe8000, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(addik_Instr)

#ADDIKC
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra + (int)imm_value + (int)MSR[key_C];
""")
addikc_Instr = trap.Instruction('ADDIKC', True)
addikc_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,1,0]}, ('addikc r', '%rd', ' r', '%ra', ' ', '%imm'))
addikc_Instr.setCode(opCode,'execute')
addikc_Instr.addBehavior(IMM_handler, 'execute')
addikc_Instr.addBehavior(IncrementPC, 'execute')
addikc_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'MSR':0x00000000})
addikc_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0006}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 11, 'PC':0x4, 'MSR':0x20000000})
addikc_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x0002}, {'GPR[1]': 0x7fffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x80000001, 'PC':0x4, 'MSR':0x00000000})
addikc_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x00000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x00fe8000, 'PC':0x4, 'MSR':0x00000000})
addikc_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x8000}, {'GPR[1]': 0x00ff0000, 'GPR[3]': 0xfffff, 'PC':0x0, 'MSR':0x20000000, 'TARGET':0xffffffff}, {'GPR[3]': 0x00fe8001, 'PC':0x4, 'MSR':0x20000000})
isa.addInstruction(addikc_Instr)

#AND instruction family
#AND
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra & (int)rb;
""")
and_Instr = trap.Instruction('AND', True)
and_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('and r', '%rd', ' r', '%ra', ' r', '%rb'))
and_Instr.setCode(opCode,'execute')
and_Instr.addBehavior(IMM_reset, 'execute')
and_Instr.addBehavior(IncrementPC, 'execute')
and_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x66440044, 'PC':0x4})
isa.addInstruction(and_Instr)

#ANDI
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra & (int)imm_value;
""")
andi_Instr = trap.Instruction('ANDI', True)
andi_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,0,1]}, ('andi r', '%rd', ' r', '%ra', ' ', '%imm'))
andi_Instr.setCode(opCode,'execute')
andi_Instr.addBehavior(IMM_handler, 'execute')
andi_Instr.addBehavior(IncrementPC, 'execute')
andi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x6666}, {'GPR[1]': 0xffcc8844, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x00000044, 'PC':0x4})
andi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x6666}, {'GPR[1]': 0xffcc8844, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff, 'IMMREG': 0x8000f0ff}, {'GPR[3]': 0xf0cc0044, 'PC':0x4})
isa.addInstruction(andi_Instr)

#ANDN
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra & ~((int)rb);
""")
andn_Instr = trap.Instruction('ANDN', True)
andn_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,1,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('addn r', '%rd', ' r', '%ra', ' r', '%rb'))
andn_Instr.setCode(opCode,'execute')
andn_Instr.addBehavior(IMM_reset, 'execute')
andn_Instr.addBehavior(IncrementPC, 'execute')
andn_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(andn_Instr)

#ANDNI
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra & ~((int)imm_value);
""")
andni_Instr = trap.Instruction('ANDNI', True)
andni_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,1,1]}, ('andi r', '%rd', ' r', '%ra', ' ', '%imm'))
andni_Instr.setCode(opCode,'execute')
andni_Instr.addBehavior(IMM_handler, 'execute')
andni_Instr.addBehavior(IncrementPC, 'execute')
andni_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x6666}, {'GPR[1]': 0xffcc8844, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffcc8800, 'PC':0x4})
isa.addInstruction(andni_Instr)

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
beq_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('beq r', '%ra', ' r', '%rb'))
beq_Instr.setCode(opCode,'execute')
beq_Instr.addBehavior(IMM_reset, 'execute')
beq_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
beq_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0xfffffff0, 'PC':0x500000}, {'PC':0x4ffff0})
beq_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 1, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500004})
isa.addInstruction(beq_Instr)

#BEQD
opCode = cxx_writer.writer_code.Code("""
if ((int)ra == 0 ) {
	TARGET = PC + (int)rb;
} else {
	TARGET = PC + 8; /* we have to jump to the instruction AFTER the delay slot. */
}
PC = PC + 4;
""")
beqd_Instr = trap.Instruction('BEQD','True')
beqd_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('beqd r', '%ra', ' r', '%rb'))
beqd_Instr.setCode(opCode,'execute')
beqd_Instr.addBehavior(IMM_reset, 'execute')
beqd_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0x10, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500010})
beqd_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 1, 'GPR[2]': 0x10, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500008})
isa.addInstruction(beqd_Instr)

#BEQI
opCode = cxx_writer.writer_code.Code("""
if ((int)ra==0) {
	PC = PC + (int)imm_value;
} else {
	PC = PC + 4;
}
""")
beqi_Instr = trap.Instruction('BEQI','True')
beqi_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,0,0]}, ('beqi r', '%ra', ' ', '%imm'))
beqi_Instr.setCode(opCode,'execute')
beqi_Instr.addBehavior(IMM_handler, 'execute')
beqi_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x500010})
beqi_Instr.addTest({'ra': 1, 'imm': 0xfff0}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x4ffff0})
beqi_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 1, 'PC':0x500000}, {'PC':0x500004})
isa.addInstruction(beqi_Instr)

#BEQID
opCode = cxx_writer.writer_code.Code("""
if ((int)ra == 0 ) {
	TARGET = PC + (int)imm_value;
} else {
	TARGET = PC + 8; /* we have to jump to the instruction AFTER the delay slot. */
}
PC = PC + 4;
""")
beqid_Instr = trap.Instruction('BEQID','True')
beqid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,0,0,0]}, ('beqid r', '%ra', ' ', '%imm'))
beqid_Instr.setCode(opCode,'execute')
beqid_Instr.addBehavior(IMM_handler, 'execute')
beqid_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 0, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500010})
beqid_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 1, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500008})
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
bge_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,1,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('bge r', '%ra', ' r', '%rb'))
bge_Instr.setCode(opCode,'execute')
bge_Instr.addBehavior(IMM_reset, 'execute')
bge_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
bge_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0xfffffff0, 'PC':0x500000}, {'PC':0x4ffff0})
bge_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': -5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500004})
isa.addInstruction(bge_Instr)

#BGED
opCode = cxx_writer.writer_code.Code("""
if ((int)ra >= 0 ) {
	TARGET = PC + (int)rb;
} else {
	TARGET = PC + 8; /* we have to jump to the instruction AFTER the delay slot. */
}
PC = PC + 4;
""")
bged_Instr = trap.Instruction('BGED','True')
bged_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,1,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('bged r', '%ra', ' r', '%rb'))
bged_Instr.setCode(opCode,'execute')
bged_Instr.addBehavior(IMM_reset, 'execute')
bged_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 1, 'GPR[2]': 0x10, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500010})
bged_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': -1, 'GPR[2]': 0x10, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500008})
isa.addInstruction(bged_Instr)

#BGEI
opCode = cxx_writer.writer_code.Code("""
if ((int)ra>=0) {
	PC = PC + (int)imm_value;
} else {
	PC = PC + 4;
}
""")
bgei_Instr = trap.Instruction('BGEI','True')
bgei_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,1,0,1]}, ('bgei r', '%ra', ' ', '%imm'))
bgei_Instr.setCode(opCode,'execute')
bgei_Instr.addBehavior(IMM_handler, 'execute')
bgei_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 5, 'PC':0x500000}, {'PC':0x500010})
bgei_Instr.addTest({'ra': 1, 'imm': 0xfff0}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x4ffff0})
bgei_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': -5, 'PC':0x500000}, {'PC':0x500004})
isa.addInstruction(bgei_Instr)

#BGEID
opCode = cxx_writer.writer_code.Code("""
if ((int)ra >= 0 ) {
	TARGET = PC + (int)imm_value;
} else {
	TARGET = PC + 8; /* we have to jump to the instruction AFTER the delay slot. */
}
PC = PC + 4;
""")
bgeid_Instr = trap.Instruction('BGEID','True')
bgeid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,1,0,1]}, ('bgeid r', '%ra', ' ', '%imm'))
bgeid_Instr.setCode(opCode,'execute')
bgeid_Instr.addBehavior(IMM_handler, 'execute')
bgeid_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 0, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500010})
bgeid_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': -1, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500008})
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
bgt_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('bgt r', '%ra', ' r', '%rb'))
bgt_Instr.setCode(opCode,'execute')
bgt_Instr.addBehavior(IMM_reset, 'execute')
bgt_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
bgt_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0xfffffff0, 'PC':0x500000}, {'PC':0x500004})
bgt_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': -5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500004})
isa.addInstruction(bgt_Instr)

#BGTD
opCode = cxx_writer.writer_code.Code("""
if ((int)ra > 0 ) {
	TARGET = PC + (int)rb;
} else {
	TARGET = PC + 8; /* we have to jump to the instruction AFTER the delay slot. */
}
PC = PC + 4;
""")
bgtd_Instr = trap.Instruction('BGTD','True')
bgtd_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('bgtd r', '%ra', ' r', '%rb'))
bgtd_Instr.setCode(opCode,'execute')
bgtd_Instr.addBehavior(IMM_reset, 'execute')
bgtd_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 1, 'GPR[2]': 0x10, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500010})
bgtd_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0x10, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500008})
isa.addInstruction(bgtd_Instr)

#BGTI
opCode = cxx_writer.writer_code.Code("""
if ((int)ra>0) {
	PC = PC + (int)imm_value;
} else {
	PC = PC + 4;
}
""")
bgti_Instr = trap.Instruction('BGTI','True')
bgti_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,1,0,0]}, ('bgti r', '%ra', ' ', '%imm'))
bgti_Instr.setCode(opCode,'execute')
bgti_Instr.addBehavior(IMM_handler, 'execute')
bgti_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 5, 'PC':0x500000}, {'PC':0x500010})
bgti_Instr.addTest({'ra': 1, 'imm': 0xfff0}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x500004})
bgti_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': -5, 'PC':0x500000}, {'PC':0x500004})
isa.addInstruction(bgti_Instr)

#BGTID
opCode = cxx_writer.writer_code.Code("""
if ((int)ra > 0 ) {
	TARGET = PC + (int)imm_value;
} else {
	TARGET = PC + 8; /* we have to jump to the instruction AFTER the delay slot. */
}
PC = PC + 4;
""")
bgtid_Instr = trap.Instruction('BGTID','True')
bgtid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,1,0,0]}, ('bgtid r', '%ra', ' ', '%imm'))
bgtid_Instr.setCode(opCode,'execute')
bgtid_Instr.addBehavior(IMM_handler, 'execute')
bgtid_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 1, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500010})
bgtid_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 0, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500008})
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
ble_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,1,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('ble r', '%ra', ' r', '%rb'))
ble_Instr.setCode(opCode,'execute')
ble_Instr.addBehavior(IMM_reset, 'execute')
ble_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500004})
ble_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0xfffffff0, 'PC':0x500000}, {'PC':0x4ffff0})
ble_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': -5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
isa.addInstruction(ble_Instr)

#BLED
opCode = cxx_writer.writer_code.Code("""
if ((int)ra <= 0 ) {
	TARGET = PC + (int)rb;
} else {
	TARGET = PC + 8; /* we have to jump to the instruction AFTER the delay slot. */
}
PC = PC + 4;
""")
bled_Instr = trap.Instruction('BLED','True')
bled_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,0,1,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('bled r', '%ra', ' r', '%rb'))
bled_Instr.setCode(opCode,'execute')
bled_Instr.addBehavior(IMM_reset, 'execute')
bled_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': -1, 'GPR[2]': 0x10, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500010})
bled_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 1, 'GPR[2]': 0x10, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500008})
isa.addInstruction(bled_Instr)

#BLEI
opCode = cxx_writer.writer_code.Code("""
if ((int)ra<=0) {
	PC = PC + (int)imm_value;
} else {
	PC = PC + 4;
}
""")
blei_Instr = trap.Instruction('BLEI','True')
blei_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,1,1]}, ('blei r', '%ra', ' ', '%imm'))
blei_Instr.setCode(opCode,'execute')
blei_Instr.addBehavior(IMM_handler, 'execute')
blei_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 5, 'PC':0x500000}, {'PC':0x500004})
blei_Instr.addTest({'ra': 1, 'imm': 0xfff0}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x4ffff0})
blei_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': -5, 'PC':0x500000}, {'PC':0x500010})
isa.addInstruction(blei_Instr)

#BLEID
opCode = cxx_writer.writer_code.Code("""
if ((int)ra <= 0 ) {
	TARGET = PC + (int)imm_value;
} else {
	TARGET = PC + 8; /* we have to jump to the instruction AFTER the delay slot. */
}
PC = PC + 4;
""")
bleid_Instr = trap.Instruction('BLEID','True')
bleid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,0,1,1]}, ('bleid r', '%ra', ' ', '%imm'))
bleid_Instr.setCode(opCode,'execute')
bleid_Instr.addBehavior(IMM_handler, 'execute')
bleid_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 0, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500010})
bleid_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 1, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500008})
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
blt_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,1,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('blt r', '%ra', ' r', '%rb'))
blt_Instr.setCode(opCode,'execute')
blt_Instr.addBehavior(IMM_reset, 'execute')
blt_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500004})
blt_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0xfffffff0, 'PC':0x500000}, {'PC':0x500004})
blt_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': -5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
isa.addInstruction(blt_Instr)

#BLTD
opCode = cxx_writer.writer_code.Code("""
if ((int)ra < 0 ) {
	TARGET = PC + (int)rb;
} else {
	TARGET = PC + 8; /* we have to jump to the instruction AFTER the delay slot. */
}
PC = PC + 4;
""")
bltd_Instr = trap.Instruction('BLTD','True')
bltd_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,0,1,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('bltd r', '%ra', ' r', '%rb'))
bltd_Instr.setCode(opCode,'execute')
bltd_Instr.addBehavior(IMM_reset, 'execute')
bltd_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': -1, 'GPR[2]': 0x10, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500010})
bltd_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0x10, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500008})
isa.addInstruction(bltd_Instr)

#BLTI
opCode = cxx_writer.writer_code.Code("""
if ((int)ra<0) {
	PC = PC + (int)imm_value;
} else {
	PC = PC + 4;
}
""")
blti_Instr = trap.Instruction('BLTI','True')
blti_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,1,0]}, ('blti r', '%ra', ' ', '%imm'))
blti_Instr.setCode(opCode,'execute')
blti_Instr.addBehavior(IMM_handler, 'execute')
blti_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 5, 'PC':0x500000}, {'PC':0x500004})
blti_Instr.addTest({'ra': 1, 'imm': 0xfff0}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x500004})
blti_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': -5, 'PC':0x500000}, {'PC':0x500010})
isa.addInstruction(blti_Instr)

#BLTID
opCode = cxx_writer.writer_code.Code("""
if ((int)ra < 0 ) {
	TARGET = PC + (int)imm_value;
} else {
	TARGET = PC + 8; /* we have to jump to the instruction AFTER the delay slot. */
}
PC = PC + 4;
""")
bltid_Instr = trap.Instruction('BLTID','True')
bltid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,0,1,0]}, ('bltid r', '%ra', ' ', '%imm'))
bltid_Instr.setCode(opCode,'execute')
bltid_Instr.addBehavior(IMM_handler, 'execute')
bltid_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': -1, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500010})
bltid_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 0, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500008})
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
bne_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [0,0,0,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('bne r', '%ra', ' r', '%rb'))
bne_Instr.setCode(opCode,'execute')
bne_Instr.addBehavior(IMM_reset, 'execute')
bne_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
bne_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0xfffffff0, 'PC':0x500000}, {'PC':0x500004})
bne_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': -5, 'GPR[2]': 0x10, 'PC':0x500000}, {'PC':0x500010})
isa.addInstruction(bne_Instr)

#BNED
opCode = cxx_writer.writer_code.Code("""
if ((int)ra != 0 ) {
	TARGET = PC + (int)rb;
} else {
	TARGET = PC + 8; /* we have to jump to the instruction AFTER the delay slot. */
}
PC = PC + 4;
""")
bned_Instr = trap.Instruction('BNED','True')
bned_Instr.setMachineCode(branch_cond_reg, {'opcode0': [1,0,0,1,1,1], 'opcode1': [1,0,0,0,1], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('bned r', '%ra', ' r', '%rb'))
bned_Instr.setCode(opCode,'execute')
bned_Instr.addBehavior(IMM_reset, 'execute')
bned_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 1, 'GPR[2]': 0x10, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500010})
bned_Instr.addTest({'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0x10, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500008})
isa.addInstruction(bned_Instr)

#BNEI
opCode = cxx_writer.writer_code.Code("""
if ((int)ra!=0) {
	PC = PC + (int)imm_value;
} else {
	PC = PC + 4;
}
""")
bnei_Instr = trap.Instruction('BNEI','True')
bnei_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [0,0,0,0,1]}, ('bnei r', '%ra', ' ', '%imm'))
bnei_Instr.setCode(opCode,'execute')
bnei_Instr.addBehavior(IMM_handler, 'execute')
bnei_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 5, 'PC':0x500000}, {'PC':0x500010})
bnei_Instr.addTest({'ra': 1, 'imm': 0xfff0}, {'GPR[1]': 0, 'PC':0x500000}, {'PC':0x500004})
bnei_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': -5, 'PC':0x500000}, {'PC':0x500010})
isa.addInstruction(bnei_Instr)

#BNEID
opCode = cxx_writer.writer_code.Code("""
if ((int)ra != 0 ) {
	TARGET = PC + (int)imm_value;
} else {
	TARGET = PC + 8; /* we have to jump to the instruction AFTER the delay slot. */
}
PC = PC + 4;
""")
bneid_Instr = trap.Instruction('BNEID','True')
bneid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,1,1], 'opcode1': [1,0,0,0,1]}, ('bneid r', '%ra', ' ', '%imm'))
bneid_Instr.setCode(opCode,'execute')
bneid_Instr.addBehavior(IMM_handler, 'execute')
bneid_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 1, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500010})
bneid_Instr.addTest({'ra': 1, 'imm': 0x10}, {'GPR[1]': 0, 'PC':0x500000, 'TARGET':0xffffffff}, {'PC':0x500004, 'TARGET':0x500008})
isa.addInstruction(bneid_Instr)

#BR
opCode = cxx_writer.writer_code.Code("""
PC = PC + (int)rb;
""")
br_Instr = trap.Instruction('BR','True')
br_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [0,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('br r', '%rd', ' r', '%rb'))
br_Instr.setCode(opCode,'execute')
br_Instr.addBehavior(IMM_reset, 'execute')
br_Instr.addTest({'rb': 1}, {'GPR[1]': 0x50, 'PC':0x500000}, {'PC':0x500050})
isa.addInstruction(br_Instr)

#BRA
opCode = cxx_writer.writer_code.Code("""
PC = (int)rb;
""")
bra_Instr = trap.Instruction('BRA','True')
bra_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [0,1,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('bra r', '%rd', ' r', '%rb'))
bra_Instr.setCode(opCode,'execute')
bra_Instr.addBehavior(IMM_reset, 'execute')
bra_Instr.addTest({'rb': 1}, {'GPR[1]': 0x50, 'PC':0x500000}, {'PC':0x50})
isa.addInstruction(bra_Instr)

#BRD
opCode = cxx_writer.writer_code.Code("""
TARGET = PC + (int)rb;
PC = PC + 4;
""")
brd_Instr = trap.Instruction('BRD','True')
brd_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [1,0,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('brd r', '%rd', ' r', '%rb'))
brd_Instr.setCode(opCode,'execute')
brd_Instr.addBehavior(IMM_reset, 'execute')
brd_Instr.addTest({'rb': 1}, {'GPR[1]': 0x50, 'PC':0x500000}, {'PC':0x500004, 'TARGET':0x500050})
isa.addInstruction(brd_Instr)

#BRAD
opCode = cxx_writer.writer_code.Code("""
TARGET = (int)rb;
PC = PC + 4;
""")
brad_Instr = trap.Instruction('BRAD','True')
brad_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [1,1,0,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('brad r', '%rd', ' r', '%rb'))
brad_Instr.setCode(opCode,'execute')
brad_Instr.addBehavior(IMM_reset, 'execute')
brad_Instr.addTest({'rb': 1}, {'GPR[1]': 0x50, 'PC':0x500000}, {'PC':0x500004, 'TARGET':0x50})
isa.addInstruction(brad_Instr)

#BRLD
opCode = cxx_writer.writer_code.Code("""
rd = PC;
TARGET = PC + (int)rb;
PC = PC + 4;
""")
brld_Instr = trap.Instruction('BRLD','True')
brld_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [1,0,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('brld r', '%rd', ' r', '%rb'))
brld_Instr.setCode(opCode,'execute')
brld_Instr.addBehavior(IMM_reset, 'execute')
brld_Instr.addTest({'rb': 1, 'rd': 2}, {'GPR[1]': 0x50, 'GPR[2]':0xffff, 'PC':0x500000}, {'GPR[2]': 0x500000, 'PC':0x500004, 'TARGET':0x500050})
isa.addInstruction(brld_Instr)

#BRALD
opCode = cxx_writer.writer_code.Code("""
rd = PC;
TARGET = (int)rb;
PC = PC + 4;
""")
brald_Instr = trap.Instruction('BRALD','True')
brald_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [1,1,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('brald r', '%rd', ' r', '%rb'))
brald_Instr.setCode(opCode,'execute')
brald_Instr.addBehavior(IMM_reset, 'execute')
brald_Instr.addTest({'rb': 1, 'rd': 2}, {'GPR[1]': 0x50, 'GPR[2]':0xffff, 'PC':0x500000}, {'GPR[2]': 0x500000, 'PC':0x500004, 'TARGET':0x50})
isa.addInstruction(brald_Instr)

#BRI
opCode = cxx_writer.writer_code.Code("""
PC = PC + (int)imm_value;
""")
bri_Instr = trap.Instruction('BRI','True')
bri_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [0,0,0,0,0]}, ('bri r', '%rd', ' ', '%imm'))
bri_Instr.addBehavior(IMM_handler, 'execute')
bri_Instr.setCode(opCode,'execute')
bri_Instr.addTest({'imm': 0x50}, {'PC':0x500000}, {'PC':0x500050})
isa.addInstruction(bri_Instr)

#BRAI
opCode = cxx_writer.writer_code.Code("""
PC = (int)imm_value;
""")
brai_Instr = trap.Instruction('BRAI','True')
brai_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [0,1,0,0,0]}, ('brai r', '%rd', ' ', '%imm'))
brai_Instr.setCode(opCode,'execute')
brai_Instr.addBehavior(IMM_handler, 'execute')
brai_Instr.addTest({'imm': 0x50}, {'PC':0x500000}, {'PC':0x50})
isa.addInstruction(brai_Instr)

#BRID
opCode = cxx_writer.writer_code.Code("""
TARGET = PC + (int)imm_value;
PC = PC + 4;
""")
brid_Instr = trap.Instruction('BRID','True')
brid_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [1,0,0,0,0]}, ('brid r', '%rd', ' ', '%imm'))
brid_Instr.setCode(opCode,'execute')
brid_Instr.addBehavior(IMM_handler, 'execute')
brid_Instr.addTest({'imm': 0x50}, {'PC':0x500000}, {'PC':0x500004, 'TARGET':0x500050})
isa.addInstruction(brid_Instr)

#BRAID
opCode = cxx_writer.writer_code.Code("""
TARGET = (int)imm_value;
PC = PC + 4;
""")
brai_Instr = trap.Instruction('BRAID','True')
brai_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [1,1,0,0,0]}, ('braid r', '%rd', ' ', '%imm'))
brai_Instr.setCode(opCode,'execute')
brai_Instr.addBehavior(IMM_handler, 'execute')
brai_Instr.addTest({'imm': 0x50}, {'PC':0x500000}, {'PC':0x500004, 'TARGET':0x50})
isa.addInstruction(brai_Instr)

#BRLID
opCode = cxx_writer.writer_code.Code("""
rd = PC;
TARGET = PC + (int)imm_value;
PC = PC + 4;
""")
brlid_Instr = trap.Instruction('BRLID','True')
brlid_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [1,0,1,0,0]}, ('brlid r', '%rd', ' ', '%imm'))
brlid_Instr.setCode(opCode,'execute')
brlid_Instr.addBehavior(IMM_handler, 'execute')
brlid_Instr.addTest({'rd': 1, 'imm': 0x50}, {'GPR[1]': 0xffff, 'PC':0x500000}, {'GPR[1]': 0x500000, 'PC':0x500004, 'TARGET':0x500050})
isa.addInstruction(brlid_Instr)

#BRALID
opCode = cxx_writer.writer_code.Code("""
rd = PC;
TARGET = (int)imm_value;
PC = PC + 4;
""")
bralid_Instr = trap.Instruction('BRALID','True')
bralid_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [1,1,1,0,0]}, ('bralid r', '%rd', ' ', '%imm'))
bralid_Instr.setCode(opCode,'execute')
bralid_Instr.addBehavior(IMM_handler, 'execute')
bralid_Instr.addTest({'rd': 1, 'imm': 0x50}, {'GPR[1]': 0xffff, 'PC':0x500000}, {'GPR[1]': 0x500000, 'PC':0x500004, 'TARGET':0x50})
isa.addInstruction(bralid_Instr)

#BRK
opCode = cxx_writer.writer_code.Code("""
if ( MSR[key_UM] == 0x1 ) {
	ESR[key_EC] = 0x1c;
} else {
	rd = PC;
	PC = (int)rb;
	MSR[key_BIP] = 0x1;
}
""")
brk_Instr = trap.Instruction('BRK','True')
brk_Instr.setMachineCode(branch_uncond_reg, {'opcode0': [1,0,0,1,1,0], 'opcode1': [0,1,1,0,0], 'opcode2': [0,0,0,0,0,0,0,0,0,0,0]}, ('brk r', '%rd', ' r', '%rb'))
brk_Instr.setCode(opCode,'execute')
brk_Instr.addBehavior(IMM_reset, 'execute')
brk_Instr.addTest({'rd': 1, 'rb': 2}, {'GPR[1]': 0xffff, 'GPR[2]': 0x50, 'PC':0x500000, 'MSR': 0x0}, {'GPR[1]': 0x500000, 'PC':0x50, 'MSR': 0x10000000})
brk_Instr.addTest({'rd': 1, 'rb': 2}, {'GPR[1]': 0xffff, 'GPR[2]': 0x50, 'PC':0x500000, 'MSR': 0x00100000}, {'GPR[1]': 0xffff, 'PC':0x500000, 'MSR': 0x00100000, 'ESR': 0xe0000000})
isa.addInstruction(brk_Instr)

#BRKI
opCode = cxx_writer.writer_code.Code("""
if ((MSR[key_UM] == 1) && ((int)imm_value != 0x8) && ((int)imm_value != 0x18)) {
	ESR[key_EC] = 0x1c;
} else {
	rd = PC;
	PC = (int)imm_value;
	MSR[key_BIP] = 0x1;
	if ( ((int)imm_value == 0x8) || ((int)imm_value == 0x18) ) {
		MSR[key_UMS] = MSR[key_UM];
		MSR[key_VMS] = MSR[key_VM];
		MSR[key_UM] = 0x0;
		MSR[key_VM] = 0x0;
	}
}
""")
brki_Instr = trap.Instruction('BRKI','True')
brki_Instr.setMachineCode(branch_uncond_imm, {'opcode0': [1,0,1,1,1,0], 'opcode1': [0,1,1,0,0]}, ('brki r', '%rd', ' ', '%imm'))
brki_Instr.setCode(opCode,'execute')
brki_Instr.addBehavior(IMM_handler, 'execute')
brki_Instr.addTest({'rd': 1, 'imm': 0x8bcd}, {'GPR[1]': 0xffff, 'PC':0x500000, 'MSR': 0x0}, {'GPR[1]': 0x500000, 'PC':0xffff8bcd, 'MSR': 0x10000000})
brki_Instr.addTest({'rd': 1, 'imm': 0x8}, {'GPR[1]': 0xffff, 'PC':0x500000, 'MSR': 0x0}, {'GPR[1]': 0x500000, 'PC':0x00000008, 'MSR': 0x10000000})
brki_Instr.addTest({'rd': 1, 'imm': 0x8}, {'GPR[1]': 0xffff, 'PC':0x500000, 'MSR': 0x00040000}, {'GPR[1]': 0x500000, 'PC':0x00000008, 'MSR': 0x10020000})
brki_Instr.addTest({'rd': 1, 'imm': 0x8}, {'GPR[1]': 0xffff, 'PC':0x500000, 'MSR': 0x00100000}, {'GPR[1]': 0x500000, 'PC':0x00000008, 'MSR': 0x10080000})
brki_Instr.addTest({'rd': 1, 'imm': 0x40}, {'GPR[1]': 0xffff, 'PC':0x500000, 'MSR': 0x00100000}, {'GPR[1]': 0xffff, 'PC':0x500000, 'ESR': 0xe0000000})
isa.addInstruction(brki_Instr)

#BARREL SHIFT family
#BSRL (S=0, T=0)
opCode = cxx_writer.writer_code.Code("""
rd = (unsigned int)ra >> ((int)rb & 0x1f); /* I consider only the five less significant bits */
""")
bsrl_Instr = trap.Instruction('BSRL', True)
bsrl_Instr.setMachineCode(barrel_reg, {'opcode0': [0,1,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('bsrl r', '%rd', ' r', '%ra', ' r', '%rb'))
bsrl_Instr.setCode(opCode,'execute')
bsrl_Instr.addBehavior(IMM_reset, 'execute')
bsrl_Instr.addBehavior(IncrementPC, 'execute')
bsrl_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x151fbb18, 'GPR[2]': 0x7, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x2a3f76, 'PC':0x4})
bsrl_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x151fbb18, 'GPR[2]': 0xf5489fe7, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x2a3f76, 'PC':0x4})
bsrl_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff1fbb18, 'GPR[2]': 0x7, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x1fe3f76, 'PC':0x4})
isa.addInstruction(bsrl_Instr)

#BSRA (S=0, T=1)
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra >> ((int)rb & 0x1f); /* the C shift is Arithmetical! */
""")
bsra_Instr = trap.Instruction('BSRA', True)
bsra_Instr.setMachineCode(barrel_reg, {'opcode0': [0,1,0,0,0,1], 'opcode1': [0,1,0,0,0,0,0,0,0,0,0]}, ('bsra r', '%rd', ' r', '%ra', ' r', '%rb'))
bsra_Instr.setCode(opCode,'execute')
bsra_Instr.addBehavior(IMM_reset, 'execute')
bsra_Instr.addBehavior(IncrementPC, 'execute')
bsra_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x151fbb18, 'GPR[2]': 0x7, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x2a3f76, 'PC':0x4})
bsra_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x151fbb18, 'GPR[2]': 0xf5489fe7, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x2a3f76, 'PC':0x4})
bsra_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff1fbb18, 'GPR[2]': 0x7, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xfffe3f76, 'PC':0x4})
isa.addInstruction(bsra_Instr)

#BSLL (S=1, T=0)
opCode = cxx_writer.writer_code.Code("""
rd = (unsigned int)ra << ((int)rb & 0x1f);
""")
bsll_Instr = trap.Instruction('BSLL', True)
bsll_Instr.setMachineCode(barrel_reg, {'opcode0': [0,1,0,0,0,1], 'opcode1': [1,0,0,0,0,0,0,0,0,0,0]}, ('bsll r', '%rd', ' r', '%ra', ' r', '%rb'))
bsll_Instr.setCode(opCode,'execute')
bsll_Instr.addBehavior(IMM_reset, 'execute')
bsll_Instr.addBehavior(IncrementPC, 'execute')
bsll_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x151fbb18, 'GPR[2]': 0x7, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x8fdd8c00, 'PC':0x4})
bsll_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x151fbb18, 'GPR[2]': 0xf5489fe7, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x8fdd8c00, 'PC':0x4})
bsll_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xff1fbb18, 'GPR[2]': 0x7, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x8fdd8c00, 'PC':0x4})
isa.addInstruction(bsll_Instr)

#BSRLI (S=0, T=0)
opCode = cxx_writer.writer_code.Code("""
rd = (unsigned int)ra >> (int)imm_value;
""")
bsrli_Instr = trap.Instruction('BSRLI', True)
bsrli_Instr.setMachineCode(barrel_imm, {'opcode0': [0,1,1,0,0,1], 'opcode1': [0,0,0,0,0,0]}, ('bsrli r', '%rd', ' r', '%ra', ' ', '%imm'))
bsrli_Instr.setCode(opCode,'execute')
bsrli_Instr.addBehavior(IMM_handler, 'execute')
bsrli_Instr.addBehavior(IncrementPC, 'execute')
bsrli_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 7}, {'GPR[1]': 0x151fbb18, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x2a3f76, 'PC':0x4})
bsrli_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 7}, {'GPR[1]': 0xff1fbb18, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x1fe3f76, 'PC':0x4})
isa.addInstruction(bsrli_Instr)

#BSRAI (S=0, T=1)
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra >> (int)imm_value;
""")
bsrai_Instr = trap.Instruction('BSRAI', True)
bsrai_Instr.setMachineCode(barrel_imm, {'opcode0': [0,1,1,0,0,1], 'opcode1': [0,1,0,0,0,0]}, ('bsrai r', '%rd', ' r', '%ra', ' ', '%imm'))
bsrai_Instr.setCode(opCode,'execute')
bsrai_Instr.addBehavior(IMM_handler, 'execute')
bsrai_Instr.addBehavior(IncrementPC, 'execute')
bsrai_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 7}, {'GPR[1]': 0x151fbb18, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x2a3f76, 'PC':0x4})
bsrai_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 7}, {'GPR[1]': 0xff1fbb18, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xfffe3f76, 'PC':0x4})
isa.addInstruction(bsrai_Instr)

#BSLLI (S=0, T=1)
opCode = cxx_writer.writer_code.Code("""
rd = (unsigned int)ra << (int)imm_value;
""")
bslli_Instr = trap.Instruction('BSLLI', True)
bslli_Instr.setMachineCode(barrel_imm, {'opcode0': [0,1,1,0,0,1], 'opcode1': [1,0,0,0,0,0]}, ('bslli r', '%rd', ' r', '%ra', ' ', '%imm'))
bslli_Instr.setCode(opCode,'execute')
bslli_Instr.addBehavior(IMM_handler, 'execute')
bslli_Instr.addBehavior(IncrementPC, 'execute')
bslli_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 7}, {'GPR[1]': 0x151fbb18, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x8fdd8c00, 'PC':0x4})
bslli_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 7}, {'GPR[1]': 0xff1fbb18, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x8fdd8c00, 'PC':0x4})
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
cmp_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,1]}, ('cmp r', '%rd', ' r', '%ra', ' r', '%rb'))
cmp_Instr.setCode(opCode,'execute')
cmp_Instr.addBehavior(IMM_reset, 'execute')
cmp_Instr.addBehavior(IncrementPC, 'execute')
cmp_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
cmp_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xfffea385, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xfffda652, 'PC':0x4})
cmp_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x15c7b, 'GPR[2]': 0xffff02cd, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xfffda652, 'PC':0x4})
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
cmpu_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,1,1]}, ('cmpu r', '%rd', ' r', '%ra', ' r', '%rb'))
cmpu_Instr.setCode(opCode,'execute')
cmpu_Instr.addBehavior(IMM_reset, 'execute')
cmpu_Instr.addBehavior(IncrementPC, 'execute')
cmpu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
cmpu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xfffea385, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x7ffda652, 'PC':0x4})
cmpu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x15c7b, 'GPR[2]': 0xffff02cd, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x7ffda652, 'PC':0x4})
isa.addInstruction(cmpu_Instr)

#FLOAT family
#FADD
opCode = cxx_writer.writer_code.Code("""
unsigned int ira=(unsigned int)ra;
float fra=  *( (float*)( (void*)(&ira) ) );
unsigned int irb=(unsigned int)rb;
float frb= *( (float*)( (void*)(&irb) ) );
float fres=fra+frb;
unsigned int res= *( (int*)( (void*)(&fres) ) );
//if isDnz(ra) or isDnz(rb):
if ( (ira & 0x7f800000 == 0 && ira & 0x007fffff != 0) || ( irb & 0x7f800000 == 0 && irb & 0x007fffff != 0 )){ 
	rd=(unsigned int)0xffc00000;
	FSR[key_DO]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
//else if isSigNan(ra) or isSigNaN(rb) or (isPosInfinite(ra) and isNegInfinite(rb)) or (isNegInfinite(ra) and isPosInfinite(rb)):
else if (	(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff !=0 && ira & 0x00400000 == 0) ||
		(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff !=0 && irb & 0x00400000 == 0) ||
		(
			(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff == 0 & ira & 0x80000000 == 0x80000000) &&
			(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff == 0 & irb & 0x80000000 == 0)
		) ||
		(
			(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff == 0 & ira & 0x80000000 == 0) &&
			(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff == 0 & irb & 0x80000000 == 0x80000000)
		)
	){
	rd=(unsigned int)0xffc00000;
	FSR[key_IO]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
//else if isQuietNaN(ra) or isQuietNaN(rb):
else if (
		(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff !=0 && ira & 0x00400000 == 0x00400000) ||
		(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff !=0 && irb & 0x00400000 == 0x00400000)
	){
	rd=(unsigned int)0xffc00000;
}
//else if isDnz (ra+rb):
else if(res & 0x7f800000 == 0 && res & 0x007fffff != 0){
	rd=(unsigned int) res & 0x80000000 == 0x80000000;
	FSR[key_UF]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
//else if isNaN(ra+rb):
else if (res & 0x7f800000 == 0x7f800000 && res & 0x007fffff !=0){
	rd=(unsigned int) res & 0x80000000 == 0x80000000;
	FSR[key_OF]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
else {
	rd=(unsigned int)res;
}
""")
fadd_Instr = trap.Instruction('FADD', True)
fadd_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, 'TODO')
fadd_Instr.setCode(opCode,'execute')
fadd_Instr.addBehavior(IMM_reset, 'execute')
fadd_Instr.addBehavior(IncrementPC, 'execute')
fadd_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xc073c6a8, 'GPR[2]': 0xc0800000, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xc0f9e354, 'PC':0x4})
isa.addInstruction(fadd_Instr)

#FRSUB
opCode = cxx_writer.writer_code.Code("""
unsigned int ira=(unsigned int)ra;
float fra=  *( (float*)( (void*)(&ira) ) );
unsigned int irb=(unsigned int)rb;
float frb= *( (float*)( (void*)(&irb) ) );
float fres=frb-fra;
unsigned int res= *( (int*)( (void*)(&fres) ) );
//if isDnz(ra) or isDnz(rb):
if ( (ira & 0x7f800000 == 0 && ira & 0x007fffff != 0) || ( irb & 0x7f800000 == 0 && irb & 0x007fffff != 0 )){ 
	rd=(unsigned int)0xffc00000;
	FSR[key_DO]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
//else if isSigNan(ra) or isSigNaN(rb) or (isPosInfinite(ra) and isPosInfinite(rb)) or (isNegInfinite(ra) and isNegInfinite(rb)):
else if (	(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff !=0 && ira & 0x00400000 == 0) ||
		(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff !=0 && irb & 0x00400000 == 0) ||
		(
			(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff == 0 & ira & 0x80000000 == 0x80000000) &&
			(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff == 0 & irb & 0x80000000 == 0x80000000)
		) ||
		(
			(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff == 0 & ira & 0x80000000 == 0) &&
			(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff == 0 & irb & 0x80000000 == 0)
		)
	){
	rd=(unsigned int)0xffc00000;
	FSR[key_IO]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
//else if isQuietNaN(ra) or isQuietNaN(rb):
else if (
		(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff !=0 && ira & 0x00400000 == 0x00400000) ||
		(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff !=0 && irb & 0x00400000 == 0x00400000)
	){
	rd=(unsigned int)0xffc00000;
}
//else if isDnz (rb-ra):
else if(res & 0x7f800000 == 0 && res & 0x007fffff != 0){
	rd=(unsigned int) res & 0x80000000 == 0x80000000;
	FSR[key_UF]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
//else if isNaN(rb-ra):
else if (res & 0x7f800000 == 0x7f800000 && res & 0x007fffff !=0){
	rd=(unsigned int) res & 0x80000000 == 0x80000000;
	FSR[key_OF]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
else {
	rd=(unsigned int)res;
}
""")
frsub_Instr = trap.Instruction('FRSUB', True)
frsub_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,0,0,1,0,0,0,0,0,0,0]}, 'TODO')
frsub_Instr.setCode(opCode,'execute')
frsub_Instr.addBehavior(IMM_reset, 'execute')
frsub_Instr.addBehavior(IncrementPC, 'execute')
frsub_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xc073c6a8, 'GPR[2]': 0xc0f9e354, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xc0800000, 'PC':0x4})
isa.addInstruction(frsub_Instr)

#FMUL
opCode = cxx_writer.writer_code.Code("""
unsigned int ira=(unsigned int)ra;
float fra=  *( (float*)( (void*)(&ira) ) );
unsigned int irb=(unsigned int)rb;
float frb= *( (float*)( (void*)(&irb) ) );
float fres=frb * fra;
unsigned int res= *( (int*)( (void*)(&fres) ) );
//if isDnz(ra) or isDnz(rb):
if ( (ira & 0x7f800000 == 0 && ira & 0x007fffff != 0) || ( irb & 0x7f800000 == 0 && irb & 0x007fffff != 0 )){ 
	rd=(unsigned int)0xffc00000;
	FSR[key_DO]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
//else if isSigNan(ra) or isSigNaN(rb) or (isZero(ra) and isInfinite(rb)) or (isInfinite(ra) and isZero(rb)):
else if (	(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff !=0 && ira & 0x00400000 == 0) ||
		(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff !=0 && irb & 0x00400000 == 0) ||
		(
			(ira & 0x7f800000 == 0 && ira & 0x007fffff == 0) &&
			(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff == 0)
		) ||
		(
			(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff == 0) &&
			(irb & 0x7f800000 == 0 && irb & 0x007fffff == 0)
		)
	){
	rd=(unsigned int)0xffc00000;
	FSR[key_IO]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
//else if isQuietNaN(ra) or isQuietNaN(rb):
else if (
		(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff !=0 && ira & 0x00400000 == 0x00400000) ||
		(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff !=0 && irb & 0x00400000 == 0x00400000)
	){
	rd=(unsigned int)0xffc00000;
}
//else if isDnz (rb*ra):
else if(res & 0x7f800000 == 0 && res & 0x007fffff != 0){
	rd=(unsigned int) res & 0x80000000 == 0x80000000;
	FSR[key_UF]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
//else if isNaN(rb*ra):
else if (res & 0x7f800000 == 0x7f800000 && res & 0x007fffff !=0){
	rd=(unsigned int) res & 0x80000000 == 0x80000000;
	FSR[key_OF]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
else {
	rd=(unsigned int)res;
}
""")
fmul_Instr = trap.Instruction('FMUL', True)
fmul_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,0,1,0,0,0,0,0,0,0,0]}, 'TODO')
fmul_Instr.setCode(opCode,'execute')
fmul_Instr.addBehavior(IMM_reset, 'execute')
fmul_Instr.addBehavior(IncrementPC, 'execute')
fmul_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xc073c6a8, 'GPR[2]': 0xc0800000, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x4173c6a8, 'PC':0x4})
isa.addInstruction(fmul_Instr)

#FDIV
opCode = cxx_writer.writer_code.Code("""
unsigned int ira=(unsigned int)ra;
float fra=  *( (float*)( (void*)(&ira) ) );
unsigned int irb=(unsigned int)rb;
float frb= *( (float*)( (void*)(&irb) ) );
float fres=frb / fra;
unsigned int res= *( (int*)( (void*)(&fres) ) );
//if isDnz(ra) or isDnz(rb):
if ( (ira & 0x7f800000 == 0 && ira & 0x007fffff != 0) || ( irb & 0x7f800000 == 0 && irb & 0x007fffff != 0 )){ 
	rd=(unsigned int)0xffc00000;
	FSR[key_DO]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
//else if isSigNan(ra) or isSigNaN(rb) or (isZero(ra) and isZero(rb)) or (isInfinite(ra) and isInfinite(rb)):
else if (	(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff !=0 && ira & 0x00400000 == 0) ||
		(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff !=0 && irb & 0x00400000 == 0) ||
		(
			(ira & 0x7f800000 == 0 && ira & 0x007fffff == 0) &&
			(irb & 0x7f800000 == 0 && irb & 0x007fffff == 0)
			
		) ||
		(
			(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff == 0) &&
			(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff == 0)
		)
	){
	rd=(unsigned int)0xffc00000;
	FSR[key_IO]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
//else if isZero(ra) and not isInfinite(rb):
else if ( 
		(ira & 0x7f800000 == 0 && ira & 0x007fffff == 0) && 
		( ! ( irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff == 0 )) ){
	rd =(unsigned int) res & 0x80000000 == 0x80000000;
	FSR[key_DZ]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
//else if isQuietNaN(ra) or isQuietNaN(rb):
else if (
		(ira & 0x7f800000 == 0x7f800000 && ira & 0x007fffff !=0 && ira & 0x00400000 == 0x00400000) ||
		(irb & 0x7f800000 == 0x7f800000 && irb & 0x007fffff !=0 && irb & 0x00400000 == 0x00400000)
	){
	rd=(unsigned int)0xffc00000;
}
//else if isDnz (rb/ra):
else if(res & 0x7f800000 == 0 && res & 0x007fffff != 0){
	rd=(unsigned int) res & 0x80000000 == 0x80000000;
	FSR[key_UF]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
//else if isNaN(rb/ra):
else if (res & 0x7f800000 == 0x7f800000 && res & 0x007fffff !=0){
	rd=(unsigned int) res & 0x80000000 == 0x80000000;
	FSR[key_OF]=1;
	ESR[key_EC]=0x0c;
	//EXCEPTION
}
else {
	rd=(unsigned int)res;
}
""")
fdiv_Instr = trap.Instruction('FDIV', True)
fdiv_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,0,1,1,0,0,0,0,0,0,0]}, 'TODO')
fdiv_Instr.setCode(opCode,'execute')
fdiv_Instr.addBehavior(IMM_reset, 'execute')
fdiv_Instr.addBehavior(IncrementPC, 'execute')
fdiv_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xc07a1cac, 'GPR[2]': 0xc0000000, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x3f030368, 'PC':0x4})
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
int ira=(int)ra;
float frd=(float)ira;
rd=*((int*) ((void*)(&frd)));
""")
flt_Instr = trap.Instruction('FLT', True)
flt_Instr.setMachineCode(float_unary, {'opcode0': [0,1,0,1,1,0], 'opcode1': [0,1,0,1,0,0,0,0,0,0,0]}, 'TODO')
flt_Instr.setCode(opCode,'execute')
flt_Instr.addBehavior(IMM_reset, 'execute')
flt_Instr.addBehavior(IncrementPC, 'execute')
flt_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]': 0xfffffffd, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xc0400000, 'PC':0x4})
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
if (ra==0){
	rd=(int)0;
	MSR[key_DZ]=1;
	ESR[key_EC]=0x14; // 00101 ---> 10100
	//EXCEPTION
}
else{
	rd=(int) (((int)rb)/((int)ra));
}
""")
idiv_Instr = trap.Instruction('IDIV', True)
idiv_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('idiv r', '%rd', ' r', '%ra', ' r', '%rb'))
idiv_Instr.setCode(opCode,'execute')
idiv_Instr.addBehavior(IMM_reset, 'execute')
idiv_Instr.addBehavior(IncrementPC, 'execute')
idiv_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x123456ab, 'PC' : 0x0, 'TARGET':0xffffffff,'MSR':0,'ESR':0}, {'GPR[3]': 0x2, 'PC' : 0x4})
idiv_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x2, 'GPR[2]' : 0xfffffffe, 'GPR[3]' : 0x123456ab, 'PC' : 0x0, 'TARGET':0xffffffff,'MSR':0,'ESR':0}, {'GPR[3]': 0xffffffff, 'PC' : 0x4})
idiv_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0, 'GPR[2]' : 0x20, 'GPR[3]' : 0x123456ab, 'PC' : 0x0, 'TARGET':0xffffffff,'MSR':0,'ESR':0}, {'GPR[3]': 0, 'PC' : 0x4,'MSR':0x02000000,'ESR':0xa0000000})
isa.addInstruction(idiv_Instr)

#IDIVU
opCode = cxx_writer.writer_code.Code("""
if (ra==0){
	rd=(unsigned int)0;
	MSR[key_DZ]=1;
	ESR[key_EC]=0x5;
	//EXCEPTION
}
else{
	rd=(unsigned int) (((unsigned int)rb)/((unsigned int)ra));
}
""")
idivu_Instr = trap.Instruction('IDIVU', True)
idivu_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,0]}, ('idivu r', '%rd', ' r', '%ra', ' r', '%rb'))
idivu_Instr.setCode(opCode,'execute')
idivu_Instr.addBehavior(IMM_reset, 'execute')
idivu_Instr.addBehavior(IncrementPC, 'execute')
idivu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x123456ab, 'PC' : 0x0, 'TARGET':0xffffffff,'MSR':0,'ESR':0}, {'GPR[3]': 0x2, 'PC' : 0x4})
idivu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x2, 'GPR[2]' : 0xfffffffe, 'GPR[3]' : 0x123456ab, 'PC' : 0x0, 'TARGET':0xffffffff,'MSR':0,'ESR':0}, {'GPR[3]': 0x7fffffff, 'PC' : 0x4})
idivu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0, 'GPR[2]' : 0x20, 'GPR[3]' : 0x123456ab, 'PC' : 0x0, 'TARGET':0xffffffff,'MSR':0,'ESR':0}, {'GPR[3]': 0, 'PC' : 0x4,'MSR':0x02000000,'ESR':0x28000000})
isa.addInstruction(idivu_Instr)

#IMM
opCode = cxx_writer.writer_code.Code("""
IMMREG = (int)imm & 0x0000ffff;
IMMREG |= 0x80000000;
/* We set the MSB bit: this indicate that the register's content is valid */
""")
imm_Instr = trap.Instruction('IMM', True)
imm_Instr.setMachineCode(imm_code, {'opcode': [1,0,1,1,0,0]}, ('imm', ' ', '%imm'))
imm_Instr.setCode(opCode,'execute')
imm_Instr.addBehavior(IMM_reset, 'execute')
imm_Instr.addBehavior(IncrementPC, 'execute')
imm_Instr.addTest({'imm': 0x8bcd}, {'IMMREG' : 0x00000000,'PC' : 0x0, 'TARGET':0xffffffff}, {'IMMREG' : 0x80008bcd, 'PC' : 0x4})
imm_Instr.addTest({'imm': 0x7bcd}, {'IMMREG' : 0x00000000,'PC' : 0x0, 'TARGET':0xffffffff}, {'IMMREG' : 0x80007bcd, 'PC' : 0x4})
isa.addInstruction(imm_Instr)

#LOAD family
#LBU
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)rb;
rd = dataMem.read_byte(addr);
rd &= 0x000000ff;
""")
lbu_Instr = trap.Instruction('LBU', True)
lbu_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('lbu r', '%rd', ' r', '%ra', ' r', '%rb'))
lbu_Instr.setCode(opCode,'execute')
lbu_Instr.addBehavior(IMM_reset, 'execute')
lbu_Instr.addBehavior(IncrementPC, 'execute')
lbu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xff, 'PC' : 0x4})
lbu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x44, 'PC' : 0x4})
lbu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456cd, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xff, 'PC' : 0x4})
isa.addInstruction(lbu_Instr)

#LBUI
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)imm_value;
rd = dataMem.read_byte(addr);
rd &= 0x000000ff;
""")
lbui_Instr = trap.Instruction('LBUI', True)
lbui_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,0,0,0]}, ('lbui r', '%rd', ' r', '%ra', ' ', '%imm'))
lbui_Instr.setCode(opCode,'execute')
lbui_Instr.addBehavior(IMM_handler, 'execute')
lbui_Instr.addBehavior(IncrementPC, 'execute')
lbui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x20}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xff, 'PC' : 0x4})
lbui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x44, 'PC' : 0x4})
lbui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456cd, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xff, 'PC' : 0x4})
isa.addInstruction(lbui_Instr)

#LHU
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)rb;
if ( (addr & 0x00000001) != 0 ) {
	handleMemoryException(0x0,0x0,rd_bit,addr);
} else {
	rd = dataMem.read_half(addr);
	rd &= 0x0000ffff;
}
""")
lhu_Instr = trap.Instruction('LHU', True)
lhu_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('lhu r', '%rd', ' r', '%ra', ' r', '%rb'))
lhu_Instr.setCode(opCode,'execute')
lhu_Instr.addBehavior(IMM_reset, 'execute')
lhu_Instr.addBehavior(IncrementPC, 'execute')
lhu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x1111, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0x0000ff44, 'PC' : 0x4, 'ESR': 0x0})
lhu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x1111, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0x1111, 'PC' : 0x20, 'ESR': 0x08c00000, 'EAR': 0x31})
lhu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x22, 'GPR[3]' : 0x1111, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0x0000ff44, 'PC' : 0x4, 'ESR': 0x0})
lhu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x13, 'GPR[2]' : 0x21, 'GPR[3]' : 0x1111, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0x0000ff44, 'PC' : 0x4, 'ESR': 0x0})
lhu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x1111, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0x500000}, {'GPR[3]' : 0x1111, 'PC' : 0x20, 'ESR': 0x08c80000, 'BTR':0x500000, 'EAR': 0x31})
isa.addInstruction(lhu_Instr)

#LHUI
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)imm_value;
if ( (addr & 0x00000001) != 0 ) {
	handleMemoryException(0x0,0x0,rd_bit,addr);
} else {
	rd = dataMem.read_half(addr);
	rd &= 0x0000ffff;
}
""")
lhui_Instr = trap.Instruction('LHUI', True)
lhui_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,0,0,1]}, ('lhui r', '%rd', ' r', '%ra', ' ', '%imm'))
lhui_Instr.setCode(opCode,'execute')
lhui_Instr.addBehavior(IMM_handler, 'execute')
lhui_Instr.addBehavior(IncrementPC, 'execute')
lhui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x20}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0x0000ff44, 'PC' : 0x4, 'ESR': 0x0})
lhui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0x1111, 'PC' : 0x20, 'ESR': 0x08c00000, 'EAR': 0x31})
lhui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x22}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0x0000ff44, 'PC' : 0x4, 'ESR': 0x0})
lhui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x13, 'GPR[3]' : 0x1111, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0x0000ff44, 'PC' : 0x4, 'ESR': 0x0})
lhui_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0x500000}, {'GPR[3]' : 0x1111, 'PC' : 0x20, 'ESR': 0x08c80000, 'BTR':0x500000, 'EAR': 0x31})
isa.addInstruction(lhui_Instr)

#WARNING: the SET/GPR[1] trick must be deleted!
#LW
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)rb;
if ( (addr & 0x00000003) != 0 ) {
	handleMemoryException(0x1,0x0,rd_bit,addr);
} else {
	rd = dataMem.read_word(addr);
}
""")
lw_Instr = trap.Instruction('LW', True)
lw_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('lw r', '%rd', ' r', '%ra', ' r', '%rb'))
lw_Instr.setCode(opCode,'execute')
lw_Instr.addBehavior(IMM_reset, 'execute')
lw_Instr.addBehavior(IncrementPC, 'execute')
lw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x1111, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0xff445566, 'PC' : 0x4, 'ESR': 0x0})
lw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x1111, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0x1111, 'PC' : 0x20, 'ESR': 0x08d00000, 'EAR': 0x31})
lw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x22, 'GPR[3]' : 0x1111, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0x1111, 'PC' : 0x20, 'ESR': 0x08d00000, 'EAR': 0x32})
lw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x13, 'GPR[2]' : 0x21, 'GPR[3]' : 0x1111, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0xff445566, 'PC' : 0x4, 'ESR': 0x0})
lw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x1111, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0x500000}, {'GPR[3]' : 0x1111, 'PC' : 0x20, 'ESR': 0x08d80000, 'BTR':0x500000, 'EAR': 0x31})
isa.addInstruction(lw_Instr)

#LWI
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)imm_value;
if ( (addr & 0x00000003) != 0 ) {
	handleMemoryException(0x1,0x0,rd_bit,addr);
} else {
	rd = dataMem.read_word(addr);
}
""")
lwi_Instr = trap.Instruction('LWI', True)
lwi_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,0,1,0]}, ('lwi r', '%rd', ' r', '%ra', ' ', '%imm'))
lwi_Instr.setCode(opCode,'execute')
lwi_Instr.addBehavior(IMM_handler, 'execute')
lwi_Instr.addBehavior(IncrementPC, 'execute')
lwi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x20}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0xff445566, 'PC' : 0x4, 'ESR': 0x0})
lwi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0x1111, 'PC' : 0x20, 'ESR': 0x08d00000, 'EAR': 0x31})
lwi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x22}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0x1111, 'PC' : 0x20, 'ESR': 0x08d00000, 'EAR': 0x32})
lwi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x13, 'GPR[3]' : 0x1111, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'GPR[3]' : 0xff445566, 'PC' : 0x4, 'ESR': 0x0})
lwi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x1111, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0x500000}, {'GPR[3]' : 0x1111, 'PC' : 0x20, 'ESR': 0x08d80000, 'BTR':0x500000, 'EAR': 0x31})
isa.addInstruction(lwi_Instr)

#MFS
opCode = cxx_writer.writer_code.Code("""
switch (rs){
	case 0x0000:
		rd=PC;
		break;
	case 0x0001:
		rd=MSR;
		break;
	case 0x0003:
		rd=EAR;
		break;
	case 0x0005:
		rd=ESR;
		break;
	case 0x0007:
		rd=FSR;
		break;
	case 0x000b:
		rd=BTR;
		break;
	case 0x000d:
		rd=EDR;
		break;
	case 0x1000:
		rd=PID;
		break;
	case 0x1001:
		rd=ZPR;
		break;
	case 0x1002:
		rd=TLBX;
		break;
	case 0x1003:
		rd=TLBLO;
		break;
	case 0x1004:
		rd=TLBHI;
		break;
};
if (rs>=0x2000 && rs <=0x200b){
	rd=PVR[rs-0x2000];
}
""")
mfs_Instr = trap.Instruction('MFS', True)
mfs_Instr.setMachineCode(mfs_code, {'opcode': [1,0,0,1,0,1]}, 'TODO')
mfs_Instr.setCode(opCode,'execute')
mfs_Instr.addBehavior(IMM_reset, 'execute')
mfs_Instr.addBehavior(IncrementPC, 'execute')
mfs_Instr.addTest({'rd': 1, 'rs': 0x0001}, {'GPR[1]' : 0x13, 'PC' : 0x0,'MSR': 0xabcd, 'TARGET':0xffffffff}, {'GPR[1]' : 0xabcd, 'PC' : 0x4})
mfs_Instr.addTest({'rd': 1, 'rs': 0x2001}, {'GPR[1]' : 0x13, 'PC' : 0x0,'PVR[1]': 0xabcd, 'TARGET':0xffffffff}, {'GPR[1]' : 0xabcd, 'PC' : 0x4})
isa.addInstruction(mfs_Instr)

#MSRCLR. The bit reversing problem is handled
opCode = cxx_writer.writer_code.Code("""
if (MSR[key_UM] == 1 && ((unsigned int)imm15) != 0x4 ){
	ESR[key_EC]=0x1c; // 00111 -----> 11100
	//EXCEPTION
}
else{
	rd=MSR;
	unsigned int imm=0;
	for (int i=0;i<15;i++){
		imm+=(((unsigned int)imm15)%2)==0;
		imm15>>=1;
		imm<<=1;
	}
	imm<<=16;
	imm |= 0x0001ffff;
	MSR &= imm ;
}
""")
msrclr_Instr = trap.Instruction('MSRCLR', True)
msrclr_Instr.setMachineCode(msr_oper, {'opcode0': [1,0,0,1,0,1], 'opcode1': [0,0,0,0,1,0]}, 'TODO')
msrclr_Instr.setCode(opCode,'execute')
msrclr_Instr.addBehavior(IMM_reset, 'execute')
msrclr_Instr.addBehavior(IncrementPC, 'execute')
msrclr_Instr.addTest({'rd': 1, 'imm15': 0x5}, {'GPR[1]' : 0x13, 'PC' : 0x0,'MSR': 0xffffffff,'ESR':0, 'TARGET':0xffffffff}, {'GPR[1]' : 0x13, 'PC' : 0x4, 'MSR': 0xffffffff,'ESR':0xe0000000})
msrclr_Instr.addTest({'rd': 1, 'imm15': 0x4}, {'GPR[1]' : 0x13, 'PC' : 0x0,'MSR': 0xffffffff,'ESR':0, 'TARGET':0xffffffff}, {'GPR[1]' : 0xffffffff, 'PC' : 0x4, 'MSR': 0xdfffffff,'ESR':0})
msrclr_Instr.addTest({'rd': 1, 'imm15': 0x0001}, {'GPR[1]' : 0x13, 'PC' : 0x0,'MSR': 0xf0000000,'ESR':0, 'TARGET':0xffffffff}, {'GPR[1]' : 0xf0000000, 'PC' : 0x4, 'MSR': 0x70000000,'ESR':0})
isa.addInstruction(msrclr_Instr)

#MSRSET
opCode = cxx_writer.writer_code.Code("""
if (MSR[key_UM] == 1 && ((unsigned int)imm15) != 0x4 ){
	ESR[key_EC]=0x1c; // 00111 -----> 11100
	//EXCEPTION
}
else{
	rd=MSR;
	unsigned int imm=0;
	for (int i=0;i<15;i++){
		imm+=((unsigned int)imm15)%2;
		imm15>>=1;
		imm<<=1;
	}
	imm<<=16;
	imm &= 0xfffe0000;
	MSR |= imm ;
}
""")
msrset_Instr = trap.Instruction('MSRSET', True)
msrset_Instr.setMachineCode(msr_oper, {'opcode0': [1,0,0,1,0,1], 'opcode1': [0,0,0,0,0,0]}, 'TODO')
msrset_Instr.setCode(opCode,'execute')
msrset_Instr.addBehavior(IMM_reset, 'execute')
msrset_Instr.addBehavior(IncrementPC, 'execute')
msrset_Instr.addTest({'rd': 1, 'imm15': 0x5}, {'GPR[1]' : 0x13, 'PC' : 0x0,'MSR': 0xffffffff,'ESR':0, 'TARGET':0xffffffff}, {'GPR[1]' : 0x13, 'PC' : 0x4, 'MSR': 0xffffffff,'ESR':0xe0000000})
msrset_Instr.addTest({'rd': 1, 'imm15': 0x4}, {'GPR[1]' : 0x13, 'PC' : 0x0,'MSR': 0x00000000,'ESR':0, 'TARGET':0xffffffff}, {'GPR[1]' : 0x00000000, 'PC' : 0x4, 'MSR': 0x20000000,'ESR':0})
msrset_Instr.addTest({'rd': 1, 'imm15': 0x4001}, {'GPR[1]' : 0x13, 'PC' : 0x0,'MSR': 0xf0000000,'ESR':0, 'TARGET':0xffffffff}, {'GPR[1]' : 0xf0000000, 'PC' : 0x4, 'MSR': 0xf0020000,'ESR':0})
isa.addInstruction(msrset_Instr)

#MTS
opCode = cxx_writer.writer_code.Code("""
if (MSR[key_UM] == 1){
	ESR[key_EC]=0x1c;
	//EXCEPTION;
}
else{
	switch (rs){
		case 0x0001:
			MSR=(int)ra;
			break;
		case 0x0007:
			FSR=(int)ra;
			break;
		case 0x1000:
			PID=(int)ra;
			break;
		case 0x1001:
			ZPR=(int)ra;
			break;
		case 0x1002:
			TLBX=(int)ra;
			break;
		case 0x1003:
			TLBLO=(int)ra;
			break;
		case 0x1004:
			TLBHI=(int)ra;
			break;
		case 0x1005:
			TLBSX=(int)ra;
			break;
	};
}
""")
mts_Instr = trap.Instruction('MTS', True)
mts_Instr.setMachineCode(mts_code, {'opcode': [1,0,0,1,0,1]}, 'TODO')
mts_Instr.setCode(opCode,'execute')
mts_Instr.addBehavior(IMM_reset, 'execute')
mts_Instr.addBehavior(IncrementPC, 'execute')
mts_Instr.addTest({'ra': 1, 'rs': 0x0001}, {'GPR[1]' : 0x13, 'PC' : 0x0,'MSR': 0x0, 'TARGET':0xffffffff}, {'GPR[1]' : 0x13,'MSR':0x13, 'PC' : 0x4})
mts_Instr.addTest({'ra': 1, 'rs': 0x1001}, {'GPR[1]' : 0x13, 'PC' : 0x0,'MSR': 0xffffffff, 'TARGET':0xffffffff}, {'GPR[1]' : 0x13,'MSR':0xffffffff, 'PC' : 0x4})
isa.addInstruction(mts_Instr)

#MUL
opCode = cxx_writer.writer_code.Code("""
long long res = ( (long long)(int)rb * (long long)(int)ra );
rd = (unsigned int) res;
""")
mul_Instr = trap.Instruction('MUL', True)
mul_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('mul r', '%rd', ' r', '%ra', ' r', '%rb'))
mul_Instr.setCode(opCode,'execute')
mul_Instr.addBehavior(IMM_reset, 'execute')
mul_Instr.addBehavior(IncrementPC, 'execute')
mul_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 24, 'PC':0x4})
mul_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfffffffc, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffffe8, 'PC':0x4})
mul_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x10000001, 'GPR[2]': 0x10, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x10, 'PC':0x4})
mul_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xefffffff, 'GPR[2]': 0x100, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffff00, 'PC':0x4})
mul_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x10000001, 'GPR[2]': 0xffffff00, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffff00, 'PC':0x4})
mul_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xefffffff, 'GPR[2]': 0xffffff00, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x100, 'PC':0x4})
isa.addInstruction(mul_Instr)

#MULH
opCode = cxx_writer.writer_code.Code("""
long long res = (long long) ( ( (long long)(int)ra) * ( (long long)(int)rb )   );
res>>=32;
rd = (unsigned int) res;
""")
mulh_Instr = trap.Instruction('MULH', True)
mulh_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,1]}, ('mulh r', '%rd', ' r', '%ra', ' r', '%rb'))
mulh_Instr.setCode(opCode,'execute')
mulh_Instr.addBehavior(IMM_reset, 'execute')
mulh_Instr.addBehavior(IncrementPC, 'execute')
mulh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0, 'PC':0x4})
mulh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfffffffc, 'GPR[2]': 6, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffffff, 'PC':0x4})
mulh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x10000001, 'GPR[2]': 0x10, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x1, 'PC':0x4})
mulh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xefffffff, 'GPR[2]': 0x100, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffffef, 'PC':0x4})
mulh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xefffffff, 'GPR[2]': 0xffffff00, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x10, 'PC':0x4})
isa.addInstruction(mulh_Instr)

#MULHU
opCode = cxx_writer.writer_code.Code("""
unsigned long long res = (  (unsigned long long)ra *  (unsigned long long) rb );
res>>=32;
rd = (unsigned int) res;
""")
mulhu_Instr = trap.Instruction('MULHU', True)
mulhu_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,1]}, ('mulhu r', '%rd', ' r', '%ra', ' r', '%rb'))
mulhu_Instr.setCode(opCode,'execute')
mulhu_Instr.addBehavior(IMM_reset, 'execute')
mulhu_Instr.addBehavior(IncrementPC, 'execute')
mulhu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0, 'PC':0x4})
mulhu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfffffffc, 'GPR[2]': 6, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x5, 'PC':0x4})
mulhu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x10000001, 'GPR[2]': 0x10, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x1, 'PC':0x4})
mulhu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xefffffff, 'GPR[2]': 0x100, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xef, 'PC':0x4})
isa.addInstruction(mulhu_Instr)

#MULHSU
opCode = cxx_writer.writer_code.Code("""
long long res = (long long)(int)ra * (unsigned long long) rb;
res>>=32;
rd = (unsigned int) res;
""")
mulhsu_Instr = trap.Instruction('MULHSU', True)
mulhsu_Instr.setMachineCode(oper_reg, {'opcode0': [0,1,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,0]}, ('mulhsu r', '%rd', ' r', '%ra', ' r', '%rb'))
mulhsu_Instr.setCode(opCode,'execute')
mulhsu_Instr.addBehavior(IMM_reset, 'execute')
mulhsu_Instr.addBehavior(IncrementPC, 'execute')
mulhsu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0, 'PC':0x4})
mulhsu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfffffffc, 'GPR[2]': 6, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffffff, 'PC':0x4})
mulhsu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 0xfffffffa, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x3, 'PC':0x4})
mulhsu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x10000001, 'GPR[2]': 0x10, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x1, 'PC':0x4})
mulhsu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xefffffff, 'GPR[2]': 0x100, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffffef, 'PC':0x4})
mulhsu_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x10000001, 'GPR[2]': 0xffffff00, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffff0, 'PC':0x4})
isa.addInstruction(mulhsu_Instr)

#MULI
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra * (int)imm_value;
""")
muli_Instr = trap.Instruction('MULI', True)
muli_Instr.setMachineCode(oper_imm, {'opcode': [0,1,1,0,0,0]}, ('muli r', '%rd', ' r', '%ra', ' ', '%imm'))
muli_Instr.setCode(opCode,'execute')
muli_Instr.addBehavior(IMM_handler, 'execute')
muli_Instr.addBehavior(IncrementPC, 'execute')
muli_Instr.addTest({'rd': 3, 'ra': 1,'imm': 0}, {'GPR[1]': 4, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0, 'PC':0x4})
muli_Instr.addTest({'rd': 3, 'ra': 1,'imm': 1}, {'GPR[1]': 0xfffffffc, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xfffffffc, 'PC':0x4})
muli_Instr.addTest({'rd': 3, 'ra': 1,'imm': 0xffff}, {'GPR[1]': 4, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xfffffffc, 'PC':0x4})
muli_Instr.addTest({'rd': 3, 'ra': 1,'imm': 0xffff}, {'GPR[1]': 0xfffffffc, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x4, 'PC':0x4})
muli_Instr.addTest({'rd': 3, 'ra': 1,'imm': 5}, {'GPR[1]': 30000, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 150000, 'PC':0x4})
isa.addInstruction(muli_Instr)

#OR
opCode = cxx_writer.writer_code.Code("""
rd = (unsigned int) (((unsigned int)ra) | ((unsigned int)rb));
""")
or_Instr = trap.Instruction('OR', True)
or_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('or r', '%rd', ' r', '%ra', ' r', '%rb'))
or_Instr.setCode(opCode,'execute')
or_Instr.addBehavior(IMM_reset, 'execute')
or_Instr.addBehavior(IncrementPC, 'execute')
or_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0, 'GPR[2]': 0, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0, 'PC':4})
or_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 2, 'GPR[2]': 0, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 2, 'PC':4})
isa.addInstruction(or_Instr)

#ORI
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra | (int)imm_value;
""")
ori_Instr = trap.Instruction('ORI', True)
ori_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,0,0]}, ('ori r', '%rd', ' r', '%ra', ' ', '%imm'))
ori_Instr.setCode(opCode,'execute')
ori_Instr.addBehavior(IMM_handler, 'execute')
ori_Instr.addBehavior(IncrementPC, 'execute')
ori_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0}, {'GPR[1]': 0,  'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0, 'PC':4})
ori_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0}, {'GPR[1]': 2,  'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 2, 'PC':4})
ori_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0xf000}, {'GPR[1]': 0,  'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xfffff000, 'PC':4})
ori_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0xffff}, {'GPR[1]': 0,  'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffffff, 'PC':4})
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
pcmpbf_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,0,0], 'opcode1': [1,0,0,0,0,0,0,0,0,0,0]}, ('pcmpbf r', '%rd', ' r', '%ra', ' r', '%rb'))
pcmpbf_Instr.setCode(opCode,'execute')
pcmpbf_Instr.addBehavior(IMM_reset, 'execute')
pcmpbf_Instr.addBehavior(IncrementPC, 'execute')
pcmpbf_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xffffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x0, 'PC':0x4})
pcmpbf_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0x12ffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x1, 'PC':0x4})
pcmpbf_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xff34ffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x2, 'PC':0x4})
pcmpbf_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xfffffeff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x3, 'PC':0x4})
pcmpbf_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xffffffdc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x4, 'PC':0x4})
pcmpbf_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xff34ffdc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x2, 'PC':0x4})
isa.addInstruction(pcmpbf_Instr)

#PCMPEQ
opCode = cxx_writer.writer_code.Code("""
rd = ((int)rb == (int)ra);
""")
pcmpeq_Instr = trap.Instruction('PCMPEQ', True)
pcmpeq_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,1,0], 'opcode1': [1,0,0,0,0,0,0,0,0,0,0]}, ('pcmpeq r', '%rd', ' r', '%ra', ' r', '%rb'))
pcmpeq_Instr.setCode(opCode,'execute')
pcmpeq_Instr.addBehavior(IMM_reset, 'execute')
pcmpeq_Instr.addBehavior(IncrementPC, 'execute')
pcmpeq_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0x1234fedc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x1, 'PC':0x4})
pcmpeq_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xffffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x0, 'PC':0x4})
isa.addInstruction(pcmpeq_Instr)

#PCMPNE
opCode = cxx_writer.writer_code.Code("""
rd = ((int)rb != (int)ra);
""")
pcmpne_Instr = trap.Instruction('PCMPNE', True)
pcmpne_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,1,1], 'opcode1': [1,0,0,0,0,0,0,0,0,0,0]}, ('pcmpne r', '%rd', ' r', '%ra', ' r', '%rb'))
pcmpne_Instr.setCode(opCode,'execute')
pcmpne_Instr.addBehavior(IMM_reset, 'execute')
pcmpne_Instr.addBehavior(IncrementPC, 'execute')
pcmpne_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0x1234fedc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x0, 'PC':0x4})
pcmpne_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0x1234fedc, 'GPR[2]': 0xffffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x1, 'PC':0x4})
isa.addInstruction(pcmpne_Instr)

#PUT / PUTD
#very strange instructions :)

#RSUB instruction family
#RSUB
opCode = cxx_writer.writer_code.Code("""
long long result=(long long)(((long long)rb) + ((long long)(~ra))+1);
MSR[key_C]=((ra^rb^(int)(result >> 1)) & 0x80000000) == 0;
rd=(int)result;
""")
rsub_Instr = trap.Instruction('RSUB', True)
rsub_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('rsub r', '%rd', ' r', '%ra', ' r', '%rb'))
rsub_Instr.setCode(opCode,'execute')
rsub_Instr.addBehavior(IMM_reset, 'execute')
rsub_Instr.addBehavior(IncrementPC, 'execute')
rsub_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'MSR':0, 'GPR[1]': 0xffffffff, 'GPR[2]': 0xffffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x0, 'PC':0x4,'MSR': 0})
isa.addInstruction(rsub_Instr)

# RSUBC
opCode = cxx_writer.writer_code.Code("""
long long result=(long long)(((long long)rb) + ((long long)(~ra))+MSR[key_C]);
MSR[key_C]=((ra^rb^(int)(result >> 1)) & 0x80000000) == 0;
rd=(int)result;
""")
rsubc_Instr = trap.Instruction('RSUBC', True)
rsubc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,0,1,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('rsubc r', '%rd', ' r', '%ra', ' r', '%rb'))
rsubc_Instr.setCode(opCode,'execute')
rsubc_Instr.addBehavior(IMM_reset, 'execute')
rsubc_Instr.addBehavior(IncrementPC, 'execute')
rsubc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'MSR':0, 'GPR[1]': 0xffffffff, 'GPR[2]': 0xffffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffffff, 'PC':0x4,'MSR': 0x20000000})
isa.addInstruction(rsubc_Instr)

# RSUBK
opCode = cxx_writer.writer_code.Code("""
rd=(int)(((int)rb) + ((int)(~ra))+1);
""")
rsubk_Instr = trap.Instruction('RSUBK', True)
rsubk_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('rsubk r', '%rd', ' r', '%ra', ' r', '%rb'))
rsubk_Instr.setCode(opCode,'execute')
rsubk_Instr.addBehavior(IMM_reset, 'execute')
rsubk_Instr.addBehavior(IncrementPC, 'execute')
rsubk_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'MSR':0, 'GPR[1]': 0xffffffff, 'GPR[2]': 0xffffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x0, 'PC':0x4,'MSR': 0})
isa.addInstruction(rsubk_Instr)

# RSUBKC
opCode = cxx_writer.writer_code.Code("""
rd=(int)(((int)rb) + ((int)(~ra))+MSR[key_C]);
""")
rsubkc_Instr = trap.Instruction('RSUBKC', True)
rsubkc_Instr.setMachineCode(oper_reg, {'opcode0': [0,0,0,1,1,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('rsubkc r', '%rd', ' r', '%ra', ' r', '%rb'))
rsubkc_Instr.setCode(opCode,'execute')
rsubkc_Instr.addBehavior(IMM_reset, 'execute')
rsubkc_Instr.addBehavior(IncrementPC, 'execute')
rsubkc_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'MSR':0, 'GPR[1]': 0xffffffff, 'GPR[2]': 0xffffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffffff, 'PC':0x4,'MSR': 0})
isa.addInstruction(rsubkc_Instr)

#RSUBI instruction family
#RSUBI
opCode = cxx_writer.writer_code.Code("""
long long result=(long long)(((long long)imm_value) + ((long long)(~ra))+1);
MSR[key_C]=((ra^imm_value^(int)(result >> 1)) & 0x80000000) == 0;
rd=(int)result;
""")
rsubi_Instr = trap.Instruction('RSUBI', True)
rsubi_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,0,1]}, 'TODO')
rsubi_Instr.setCode(opCode,'execute')
rsubi_Instr.addBehavior(IMM_handler, 'execute')
rsubi_Instr.addBehavior(IncrementPC, 'execute')
rsubi_Instr.addTest({'rd': 3, 'ra': 1, 'imm':0xffff}, {'IMMREG': 0x8000ffff, 'MSR':0, 'GPR[1]': 0xffffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0, 'PC':0x4,'MSR': 0})
isa.addInstruction(rsubi_Instr)

#RSUBIC
opCode = cxx_writer.writer_code.Code("""
long long result=(long long)(((long long)imm_value) + ((long long)(~ra))+MSR[key_C]);
MSR[key_C]=((ra^imm_value^(int)(result >> 1)) & 0x80000000) == 0;
rd=(int)result;
""")
rsubic_Instr = trap.Instruction('RSUBIC', True)
rsubic_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,0,1,1]}, 'TODO')
rsubic_Instr.setCode(opCode,'execute')
rsubic_Instr.addBehavior(IMM_handler, 'execute')
rsubic_Instr.addBehavior(IncrementPC, 'execute')
rsubic_Instr.addTest({'rd': 3, 'ra': 1, 'imm':0xffff}, {'MSR':0, 'GPR[1]': 0xffffffff,'IMMREG':0x8000ffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffffff, 'PC':0x4,'MSR': 0x20000000})
isa.addInstruction(rsubic_Instr)

#RSUBIK
opCode = cxx_writer.writer_code.Code("""
rd=(int)(((int)imm_value) + ((int)(~ra))+1);
""")
rsubik_Instr = trap.Instruction('RSUBIK', True)
rsubik_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,0,1]}, 'TODO')
rsubik_Instr.setCode(opCode,'execute')
rsubik_Instr.addBehavior(IMM_handler, 'execute')
rsubik_Instr.addBehavior(IncrementPC, 'execute')
rsubik_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0xffff}, {'IMMREG': 0x8000ffff, 'MSR':0, 'GPR[1]': 0xffffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x0, 'PC':0x4,'MSR': 0})
isa.addInstruction(rsubik_Instr)

#RSUBIKC
opCode = cxx_writer.writer_code.Code("""
rd=(int)(((int)imm_value) + ((int)(~ra))+MSR[key_C]);
""")
rsubikc_Instr = trap.Instruction('RSUBIKC', True)
rsubikc_Instr.setMachineCode(oper_imm, {'opcode': [0,0,1,1,1,1]}, 'TODO')
rsubikc_Instr.setCode(opCode,'execute')
rsubikc_Instr.addBehavior(IMM_handler, 'execute')
rsubikc_Instr.addBehavior(IncrementPC, 'execute')
rsubikc_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0xffff}, {'IMMREG': 0X8000ffff, 'MSR':0, 'GPR[1]': 0xffffffff, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffffff, 'PC':0x4,'MSR': 0})
isa.addInstruction(rsubikc_Instr)

#RETURN instruction family
#RTBD
opCode = cxx_writer.writer_code.Code("""
if ( MSR[key_UM] == 1 ) {
	handleUserPermissionException();
} else {
	TARGET = (int)ra + (int)imm_value;
	MSR[key_BIP] = 0x0;
	MSR[key_UM] = MSR[key_UMS];
	MSR[key_VM] = MSR[key_VMS];
	PC = PC + 4;	
}
""")
rtbd_Instr = trap.Instruction('RTBD','True')
rtbd_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,0,1], 'opcode1': [1,0,0,1,0]}, ('rtbd r', '%ra', ' ', '%imm'));
rtbd_Instr.setCode(opCode,'execute')
rtbd_Instr.addBehavior(IMM_handler, 'execute')
rtbd_Instr.addTest({'ra': 1, 'imm':0x20}, {'GPR[1]': 0x50, 'PC':0x500000, 'MSR' : 0x0}, {'PC':0x500004, 'TARGET':0x70, 'MSR': 0x0})
rtbd_Instr.addTest({'ra': 1, 'imm':0x20}, {'GPR[1]': 0x50, 'PC':0x500000, 'MSR' : 0x00020000}, {'PC':0x500004, 'MSR' : 0x00060000})
rtbd_Instr.addTest({'ra': 1, 'imm':0x20}, {'GPR[1]': 0x50, 'PC':0x500000, 'MSR' : 0x00100000, 'ESR': 0x0}, {'PC':0x20, 'MSR' : 0x00480000, 'ESR': 0xe0000000})
isa.addInstruction(rtbd_Instr)

#RTID
opCode = cxx_writer.writer_code.Code("""
if ( MSR[key_UM] == 1 ) {
	handleUserPermissionException();
} else {
	TARGET = (int)ra + (int)imm_value;
	MSR[key_IE] = 0x1;
	MSR[key_UM] = MSR[key_UMS];
	MSR[key_VM] = MSR[key_VMS];
	PC = PC + 4;	
}
""")
rtid_Instr = trap.Instruction('RTID','True')
rtid_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,0,1], 'opcode1': [1,0,0,0,1]}, ('rtid r', '%ra', ' ', '%imm'))
rtid_Instr.setCode(opCode,'execute')
rtid_Instr.addBehavior(IMM_handler, 'execute')
rtid_Instr.addTest({'ra': 1, 'imm':0x20}, {'GPR[1]': 0x50, 'PC':0x500000, 'MSR' : 0x0}, {'PC':0x500004, 'TARGET':0x70, 'MSR': 0x40000000})
rtid_Instr.addTest({'ra': 1, 'imm':0x20}, {'GPR[1]': 0x50, 'PC':0x500000, 'MSR' : 0x00020000}, {'PC':0x500004, 'MSR' : 0x40060000})
rtid_Instr.addTest({'ra': 1, 'imm':0x20}, {'GPR[1]': 0x50, 'PC':0x500000, 'MSR' : 0x00100000, 'ESR': 0x0}, {'PC':0x20, 'MSR' : 0x00480000, 'ESR': 0xe0000000})
isa.addInstruction(rtid_Instr)

#RTED
#TODO: handle correctly exceptions: see page 59 of the reference
opCode = cxx_writer.writer_code.Code("""
if ( MSR[key_UM] == 1 ) {
	handleUserPermissionException();
} else {
	if (ESR[key_DS] ) {
		TARGET = BTR;	
	} else {
		TARGET = (int)ra + (int)imm_value;
	}
	MSR[key_EE] = 0x1;
	MSR[key_EIP] = 0x0;
	MSR[key_UM] = MSR[key_UMS];
	MSR[key_VM] = MSR[key_VMS];
	ESR = 0x0;
	PC = PC + 4;	
}
""")
rted_Instr = trap.Instruction('RTED','True')
rted_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,0,1], 'opcode1': [1,0,1,0,0]}, ('rted r', '%ra', ' ', '%imm'))
rted_Instr.setCode(opCode,'execute')
rted_Instr.addBehavior(IMM_handler, 'execute')
rted_Instr.addTest({'ra': 1, 'imm':0x20}, {'GPR[1]': 0x50, 'PC':0x500000, 'MSR' : 0x0}, {'PC':0x500004, 'TARGET':0x70, 'MSR': 0x00800000, 'TARGET':0x70})
rted_Instr.addTest({'ra': 1, 'imm':0x20}, {'GPR[1]': 0x50, 'PC':0x500000, 'MSR' : 0x00020000}, {'PC':0x500004, 'MSR' : 0x00860000, 'TARGET':0x70})
rted_Instr.addTest({'ra': 1, 'imm':0x20}, {'GPR[1]': 0x50, 'PC':0x500000, 'MSR' : 0x0, 'ESR': 0x00080000, 'BTR': 0x7777}, {'PC':0x500004, 'MSR' : 0x00800000, 'TARGET': 0x7777})
rted_Instr.addTest({'ra': 1, 'imm':0x20}, {'GPR[1]': 0x50, 'PC':0x500000, 'MSR' : 0x00100000, 'ESR': 0x0}, {'PC':0x20, 'MSR' : 0x00480000, 'ESR': 0xe0000000})
isa.addInstruction(rted_Instr)

#RTSD
opCode = cxx_writer.writer_code.Code("""
TARGET = (int)ra + (int)imm_value;
PC = PC + 4;
""")
rtsd_Instr = trap.Instruction('RTSD','True')
rtsd_Instr.setMachineCode(branch_cond_imm, {'opcode0': [1,0,1,1,0,1], 'opcode1': [1,0,0,0,0]}, ('rtsd r', '%ra', ' ', '%imm'))
rtsd_Instr.setCode(opCode,'execute')
rtsd_Instr.addBehavior(IMM_handler, 'execute')
rtid_Instr.addTest({'ra': 1, 'imm':0x20}, {'GPR[1]': 0x50, 'PC':0x500000, 'MSR' : 0x0, 'TARGET': 0xffffffff}, {'PC':0x500004, 'TARGET':0x70, 'MSR': 0x40000000})
rtid_Instr.addTest({'ra': 1, 'imm':0x20}, {'GPR[1]': 0x50, 'PC':0x500000, 'MSR' : 0x00020000, 'TARGET': 0xffffffff}, {'PC':0x500004, 'TARGET':0x70, 'MSR' : 0x40060000})
isa.addInstruction(rtsd_Instr)

#STORE instruction family
#SB
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)rb;
dataMem.write_byte(addr, (unsigned char)(rd & 0x000000ff));
""")
sb_Instr = trap.Instruction('SB', True)
sb_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('sb r', '%rd', ' r', '%ra', ' r', '%rb'))
sb_Instr.setCode(opCode,'execute')
sb_Instr.addBehavior(IMM_reset, 'execute')
sb_Instr.addBehavior(IncrementPC, 'execute')
sb_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'TARGET':0xffffffff}, {'dataMem[0x30]': 0xab445566, 'PC' : 0x4})
sb_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'TARGET':0xffffffff}, {'dataMem[0x30]': 0xffab5566, 'PC' : 0x4})
sb_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'TARGET':0xffffffff}, {'dataMem[0x31]': 0xab445566, 'PC' : 0x4})
isa.addInstruction(sb_Instr)

#SBI
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)imm_value;
dataMem.write_byte(addr, (unsigned char)(rd & 0x000000ff));
""")
sbi_Instr = trap.Instruction('SBI', True)
sbi_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,1,0,0]}, ('sbi r', '%rd', ' r', '%ra', ' ', '%imm'))
sbi_Instr.setCode(opCode,'execute')
sbi_Instr.addBehavior(IMM_handler, 'execute')
sbi_Instr.addBehavior(IncrementPC, 'execute')
sbi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x20}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'TARGET':0xffffffff}, {'dataMem[0x30]': 0xab445566, 'PC' : 0x4})
sbi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'TARGET':0xffffffff}, {'dataMem[0x30]': 0xffab5566, 'PC' : 0x4})
sbi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'TARGET':0xffffffff}, {'dataMem[0x31]': 0xab445566, 'PC' : 0x4})
isa.addInstruction(sbi_Instr)

#SH
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)rb;
if ( ( addr & 0x00000001 ) != 0 ) {
	handleMemoryException(0x0,0x1,rd_bit,addr);
} else {
	dataMem.write_half(addr, (unsigned int)(rd & 0x0000ffff));
}
""")
sh_Instr = trap.Instruction('SH', True)
sh_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,1,0,1], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('sh r', '%rd', ' r', '%ra', ' r', '%rb'))
sh_Instr.setCode(opCode,'execute')
sh_Instr.addBehavior(IMM_reset, 'execute')
sh_Instr.addBehavior(IncrementPC, 'execute')
sh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x30]': 0x56ab5566, 'PC' : 0x4, 'ESR': 0x0})
sh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x31]': 0xff445566, 'PC' : 0x20, 'ESR': 0x08e00000, 'EAR': 0x31})
sh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x22, 'GPR[3]' : 0x123456ab, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x32]': 0x56ab5566, 'PC' : 0x4, 'ESR': 0x0})
sh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x13, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x34]': 0x56ab5566, 'PC' : 0x4, 'ESR': 0x0})
sh_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0x500000}, {'dataMem[0x31]': 0xff445566, 'PC' : 0x20, 'ESR': 0x08e80000, 'BTR':0x500000, 'EAR': 0x31})
isa.addInstruction(sh_Instr)

#SHI
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)imm_value;
if ( ( addr & 0x00000001 ) != 0 ) {
	handleMemoryException(0x0,0x1,rd_bit,addr);
} else {
	dataMem.write_half(addr, (unsigned int)(rd & 0x0000ffff));
}
""")
shi_Instr = trap.Instruction('SHI', True)
shi_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,1,0,1]}, ('shi r', '%rd', ' r', '%ra', ' ', '%imm'))
shi_Instr.setCode(opCode,'execute')
shi_Instr.addBehavior(IMM_handler, 'execute')
shi_Instr.addBehavior(IncrementPC, 'execute')
shi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x20}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x30]': 0x56ab5566, 'PC' : 0x4, 'ESR': 0x0})
shi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x31]': 0xff445566, 'PC' : 0x20, 'ESR': 0x08e00000, 'EAR': 0x31})
shi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x22}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x32]': 0x56ab5566, 'PC' : 0x4, 'ESR': 0x0})
shi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x13, 'GPR[3]' : 0x123456ab, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x34]': 0x56ab5566, 'PC' : 0x4, 'ESR': 0x0})
shi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0x500000}, {'dataMem[0x31]': 0xff445566, 'PC' : 0x20, 'ESR': 0x08e80000, 'BTR':0x500000, 'EAR': 0x31})
isa.addInstruction(shi_Instr)

#SW
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)rb;
if ( ( addr & 0x00000003 ) != 0 ) {
	handleMemoryException(0x1,0x1,rd_bit,addr);
} else {
	dataMem.write_word(addr, (unsigned int)(rd));
}
""")
sw_Instr = trap.Instruction('SW', True)
sw_Instr.setMachineCode(oper_reg, {'opcode0': [1,1,0,1,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('sw r', '%rd', ' r', '%ra', ' r', '%rb'))
sw_Instr.setCode(opCode,'execute')
sw_Instr.addBehavior(IMM_reset, 'execute')
sw_Instr.addBehavior(IncrementPC, 'execute')
sw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x20, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x30]': 0x123456ab, 'PC' : 0x4, 'ESR': 0x0})
sw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x31]': 0xff445566, 'PC' : 0x20, 'ESR': 0x08f00000, 'EAR': 0x31})
sw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x22, 'GPR[3]' : 0x123456ab, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x32]': 0xff445566, 'PC' : 0x20, 'ESR': 0x08f00000, 'EAR': 0x32})
sw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x13, 'GPR[2]' : 0x21, 'GPR[3]' : 0x123456ab, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x34]': 0x123456ab, 'PC' : 0x4, 'ESR': 0x0})
sw_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]' : 0x10, 'GPR[2]' : 0x22, 'GPR[3]' : 0x123456ab, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0x500000}, {'dataMem[0x32]': 0xff445566, 'PC' : 0x20, 'ESR': 0x08f80000, 'BTR':0x500000, 'EAR': 0x32})
isa.addInstruction(sw_Instr)

#SWI
opCode = cxx_writer.writer_code.Code("""
int addr = (int)ra + (int)imm_value;
if ( ( addr & 0x00000003 ) != 0 ) {
	handleMemoryException(0x1,0x1,rd_bit,addr);
} else {
	dataMem.write_word(addr, (unsigned int)(rd));
}
""")
swi_Instr = trap.Instruction('SWI', True)
swi_Instr.setMachineCode(oper_imm, {'opcode': [1,1,1,1,1,0]}, ('swi r', '%rd', ' r', '%ra', ' ', '%imm'))
swi_Instr.setCode(opCode,'execute')
swi_Instr.addBehavior(IMM_handler, 'execute')
swi_Instr.addBehavior(IncrementPC, 'execute')
swi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x20}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x30]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x30]': 0x123456ab, 'PC' : 0x4, 'ESR': 0x0})
swi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x31]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x31]': 0xff445566, 'PC' : 0x20, 'ESR': 0x08f00000, 'EAR': 0x31})
swi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x22}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x32]': 0xff445566, 'PC' : 0x20, 'ESR': 0x08f00000, 'EAR': 0x32})
swi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x21}, {'GPR[1]' : 0x13, 'GPR[3]' : 0x123456ab, 'dataMem[0x34]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0xffffffff}, {'dataMem[0x34]': 0x123456ab, 'PC' : 0x4, 'ESR': 0x0})
swi_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0x22}, {'GPR[1]' : 0x10, 'GPR[3]' : 0x123456ab, 'dataMem[0x32]': 0xff445566, 'PC' : 0x0, 'ESR': 0x0, 'TARGET':0x500000}, {'dataMem[0x32]': 0xff445566, 'PC' : 0x20, 'ESR': 0x08f80000, 'BTR':0x500000, 'EAR': 0x32})
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
sext16_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1]}, ('sext16 r', '%rd', ' r', '%ra'))
sext16_Instr.setCode(opCode,'execute')
sext16_Instr.addBehavior(IMM_reset, 'execute')
sext16_Instr.addBehavior(IncrementPC, 'execute')
sext16_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0x6666, 'GPR[3]' : 0xffff, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x00006666, 'PC' : 0x4})
sext16_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0xabcd7777, 'GPR[3]' : 0xffff, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x00007777, 'PC' : 0x4})
sext16_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0xabcd8777, 'GPR[3]' : 0xffff, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffff8777, 'PC' : 0x4})
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
sext8_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0]}, ('sext8 r', '%rd', ' r', '%ra'))
sext8_Instr.setCode(opCode,'execute')
sext8_Instr.addBehavior(IMM_reset, 'execute')
sext8_Instr.addBehavior(IncrementPC, 'execute')
sext8_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0x6666, 'GPR[3]' : 0xffff, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x00000066, 'PC' : 0x4})
sext8_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0xabcd7777, 'GPR[3]' : 0xffff, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x00000077, 'PC' : 0x4})
sext8_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0xabcd7787, 'GPR[3]' : 0xffff, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffff87, 'PC' : 0x4})
isa.addInstruction(sext8_Instr)

#SRA
opCode = cxx_writer.writer_code.Code("""
rd=ra>>1;
rd |= (ra & 0x80000000);
MSR[key_C] = ra%2;
""")
sra_Instr = trap.Instruction('SRA', True)
sra_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]}, ('sra r', '%rd', ' r', '%ra'))
sra_Instr.setCode(opCode,'execute')
sra_Instr.addBehavior(IMM_reset, 'execute')
sra_Instr.addBehavior(IncrementPC, 'execute')
sra_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0x40000001,'MSR': 0, 'GPR[3]' : 0xffff, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x20000000, 'MSR': 0x20000000, 'PC' : 0x4})
sra_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0xc0000000,'MSR': 0, 'GPR[3]' : 0xffff, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xe0000000, 'MSR': 0, 'PC' : 0x4})
isa.addInstruction(sra_Instr)

#SRC
opCode = cxx_writer.writer_code.Code("""
rd=ra>>1;
rd |= (MSR[key_C]? 0x80000000 : 0);
MSR[key_C]=ra%2;
""")
src_Instr = trap.Instruction('SRC', True)
src_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1]}, ('src r', '%rd', ' r', '%ra'))
src_Instr.setCode(opCode,'execute')
src_Instr.addBehavior(IMM_reset, 'execute')
src_Instr.addBehavior(IncrementPC, 'execute')
src_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0x40000000,'MSR': 0x20000000, 'GPR[3]' : 0xffff, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xa0000000, 'MSR': 0x00000000, 'PC' : 0x4})
src_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0xc0000001,'MSR': 0x00000000, 'GPR[3]' : 0xffff, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x60000000, 'MSR': 0x20000000, 'PC' : 0x4})
isa.addInstruction(src_Instr)

#SRL
opCode = cxx_writer.writer_code.Code("""
rd=ra>>1;
rd &= 0x7fffffff;
MSR[key_C]=ra%2;
""")
srl_Instr = trap.Instruction('SRL', True)
srl_Instr.setMachineCode(unary_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1]}, ('srl r', '%rd', ' r', '%ra'))
srl_Instr.setCode(opCode,'execute')
srl_Instr.addBehavior(IMM_reset, 'execute')
srl_Instr.addBehavior(IncrementPC, 'execute')
srl_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0x40000000,'MSR': 0x20000000, 'GPR[3]' : 0xffff, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x20000000, 'MSR': 0x00000000, 'PC' : 0x4})
srl_Instr.addTest({'rd': 3, 'ra': 1}, {'GPR[1]' : 0xc0000001,'MSR': 0x20000000, 'GPR[3]' : 0xffff, 'PC' : 0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x60000000, 'MSR': 0x20000000, 'PC' : 0x4})
isa.addInstruction(srl_Instr)

#WDC
opCode = cxx_writer.writer_code.Code("""
/* This instruction is related to the Cache. Since we don't have
   Cache in our model, we simply ignore the implementation of 
   this instruction. */
""")
wdc_Instr = trap.Instruction('WDC', True)
wdc_Instr.setMachineCode(cache_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,1,1,0,0,1,0,0]}, ('wdc r', '%ra', ' r', '%rb'))
wdc_Instr.setCode(opCode,'execute')
wdc_Instr.addBehavior(IMM_reset, 'execute')
wdc_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(wdc_Instr)

#WIC
opCode = cxx_writer.writer_code.Code("""
/* This instruction is related to the Cache. Since we don't have
   Cache in our model, we simply ignore the implementation of 
   this instruction. */
""")
wic_Instr = trap.Instruction('WIC', True)
wic_Instr.setMachineCode(cache_oper, {'opcode0': [1,0,0,1,0,0], 'opcode1': [0,0,0,0,1,1,0,1,0,0,0]}, ('wic r', '%ra', ' r', '%rb'))
wic_Instr.setCode(opCode,'execute')
wic_Instr.addBehavior(IMM_reset, 'execute')
wic_Instr.addBehavior(IncrementPC, 'execute')
isa.addInstruction(wic_Instr)

#XOR
opCode = cxx_writer.writer_code.Code("""
//rd=(unsigned int)(((unsigned int)ra) ^ ((unsigned int)rb));
rd = (int)ra ^ (int)rb;
""")
xor_Instr = trap.Instruction('XOR', True)
xor_Instr.setMachineCode(oper_reg, {'opcode0': [1,0,0,0,1,0], 'opcode1': [0,0,0,0,0,0,0,0,0,0,0]}, ('xor r', '%rd', ' r', '%ra', ' r', '%rb'))
xor_Instr.setCode(opCode,'execute')
xor_Instr.addBehavior(IMM_reset, 'execute')
xor_Instr.addBehavior(IncrementPC, 'execute')
xor_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 3, 'GPR[2]': 0, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x3, 'PC':4})
xor_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 5, 'GPR[2]': 5, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0, 'PC':4})
xor_Instr.addTest({'rd': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xffff, 'GPR[2]': 0xffffffff, 'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffff0000, 'PC':4})
isa.addInstruction(xor_Instr)

#XORI
opCode = cxx_writer.writer_code.Code("""
rd = (int)ra ^ (int)imm_value;
""")
xori_Instr = trap.Instruction('XORI', True)
xori_Instr.setMachineCode(oper_imm, {'opcode': [1,0,1,0,1,0]}, ('xori r', '%rd', ' r', '%ra', ' ', '%imm'))
xori_Instr.setCode(opCode,'execute')
xori_Instr.addBehavior(IMM_handler, 'execute')
xori_Instr.addBehavior(IncrementPC, 'execute')
xori_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0}, {'GPR[1]': 3,  'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x3, 'PC':4})
xori_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 5}, {'GPR[1]': 5,  'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0, 'PC':4})
xori_Instr.addTest({'rd': 3, 'ra': 1, 'imm': 0xffff}, {'GPR[1]': 0xffff0000,  'GPR[3]': 0xffffffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x0000ffff, 'PC':4})
isa.addInstruction(xori_Instr)
