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
#   (a) Luca Fossati, fossati@elet.polimi.it
#   (b) Redwanur Rahman, md.rahman@mail.polimi.it
#   (c) Ashanka das, Ak.das@mail.polimi.it
####################################################################################


# Lets first of all import the necessary files for the
# creation of the processor
import trap
import cxx_writer
from PPC405Coding import *
from PPC405Methods import *

# ISA declaration: it is the container for all the single instructions
isa = trap.ISA()
#ADD
opCode = cxx_writer.writer_code.Code("""
rt = (int)rb + (int)ra;
""")
add_Instr = trap.Instruction('ADD', True)
add_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,0,0,0,0,1,0,1,0]}, ('add r', '%rt', ' r', '%ra', ' r', '%rb'))
add_Instr.setCode(opCode,'execute')
add_Instr.addBehavior(IncrementPC, 'execute')
add_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(add_Instr)

#ADDC
opCode = cxx_writer.writer_code.Code("""
rt = (int)rb + (int)ra;
if ((int)rb + (int)ra>exp(2,32)-1) {
	XER[CA] = 1;
}
else {
	XER[CA] = 0;
}
""")
#addc_Instr = trap.Instruction('ADDC', True)
#addc_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,0,1,0,1,0]}, ('add r', '%rt', ' r', '%ra', ' r', '%rb'))
#addc_Instr.setCode(opCode,'execute')
#addc_Instr.addBehavior(IncrementPC, 'execute')
#addc_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
#isa.addInstruction(addc_Instr)
#ADDE
#opCode = cxx_writer.writer_code.Code("""
#rt = (int)rb + (int)ra + XER[CA];
#if ((int)rb + (int)ra + XER[CA] > exp(2,32)-1) {
#	XER[CA] = 1;
#}
#else {
#	XER[CA] = 0;
#}
#""")
#adde_Instr = trap.Instruction('ADDE', True)
#adde_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,0,0,0,1,0,1,0]}, ('add r', '%rt', ' r', '%ra', ' r', '%rb'))
#adde_Instr.setCode(opCode,'execute')
#adde_Instr.addBehavior(IncrementPC, 'execute')
#adde_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
#isa.addInstruction(adde_Instr)
#ADDI
opCode = cxx_writer.writer_code.Code("""
if(ra == 0){
	rt = 0 + exts(IM);
}
else{
	(rt) = (int)(ra) + exts(IM);
}
""")
#addi_Instr = trap.Instruction('ADDI', True)
#addi_Instr.setMachineCode(oper_Dform_2 , {'primary_opcode': [0,1,1,1,1,1] }, ('add r', '%rt', ' r', '%ra'))
#addi_Instr.setCode(opCode,'execute')
#addi_Instr.addBehavior(IncrementPC, 'execute')
#addi_Instr.addTest({'rt': 3, 'ra': 1}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
#isa.addInstruction(addi_Instr)
#ADDIC 
#ADDIS
#ADDME
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra + XER[CA]+(-1);
if ((int)ra + XER[CA]+0xFFFFFFFF > exp(2,32)-1) {
	XER[CA] = 1;
}
else {
	XER[CA] = 0;
}
""")
#addme_Instr = trap.Instruction('ADDME', True)
#addme_Instr.setMachineCode(oper_X0form_3, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,1,1,0,1,0,1,0]}, ('Add r', '%rt', ' r', '%ra'))
#addme_Instr.setCode(opCode,'execute')
#addme_Instr.addBehavior(IncrementPC, 'execute')
#addme_Instr.addTest({'rt': 1, 'ra': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
#isa.addInstruction(addme_Instr)
#ADDZE
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra + XER[CA];
if ((int)ra + XER[CA]> exp(2,32)-1) {
	XER[CA] = 1;
}
else {
	XER[CA] = 0;
}
""")
#addze_Instr = trap.Instruction('ADDZE', True)
#addze_Instr.setMachineCode(oper_X0form_3, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,1,1,1,0,0]}, ('Add r', '%rt', ' r', '%ra'))
#addze_Instr.setCode(opCode,'execute')
#addze_Instr.addBehavior(IncrementPC, 'execute')
#addze_Instr.addTest({'rt': 1, 'ra': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
#isa.addInstruction(addze_Instr)
#AND
#opCode = cxx_writer.writer_code.Code("""
#ra = (int)rs & (int)rb;
#""")
#and_Instr = trap.Instruction('AND', True)
#and_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,1,1,0,0,1,0,1,0]}, ('and r', '%ra', ' r', '%rs', ' r', '%rb'))
#and_Instr.setCode(opCode,'execute')
#and_Instr.addBehavior(IncrementPC, 'execute')
#and_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x66440044, 'PC':0x4})
#and_Instr.addTest({'ra': 1, 'rs': 1, 'rb': 1}, {'GPR[1]': 0xab88cd77, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[1]': 0xab88cd77, 'PC':0x4})
#isa.addInstruction(and_Instr)
#ANDC
#opCode = cxx_writer.writer_code.Code("""
#ra = (int)rs & ~((int)rb);
#""")
#andc_Instr = trap.Instruction('ANDC', True)
#andc_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,1,1,1,1,0,0]}, ('and r', '%ra', ' r', '%rs', ' r', '%rb'))
#andc_Instr.setCode(opCode,'execute')
#andc_Instr.addBehavior(IncrementPC, 'execute')
#andc_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
#isa.addInstruction(andc_Instr)
#ANDI 
#ANDIS
#B
#BC
#BCCTR
#BCLR
#CMP
opCode = cxx_writer.writer_code.Code("""
int c0,c1,c2,c3;
if (int)ra < (int)rb c0=1;
if (int)ra > (int)rb c1=1;
if (int)ra = (int)rb c2=1;
c3=XER[S0];
int n=bf;
CR[n]=c0; 
//CR[1]=c1; CR[2]=c2; CR[3]=c3;
""")
#cmp_Instr = trap.Instruction('CMP', True)
#cmp_Instr.setMachineCode(oper_Xform_16, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,0,0,0,0,0,0]}, ('cmp r', '%bf', ' r', '%ra', ' r', '%rb'))
#cmp_Instr.setCode(opCode,'execute')
#cmp_Instr.addBehavior(IncrementPC, 'execute')
#cmp_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
#isa.addInstruction(cmp_Instr)
#CMPI
opCode = cxx_writer.writer_code.Code("""
int c0=0,c1=0,c2=0,c3=0;
if (int)ra < exts(im_si) c0=1;
if (int)ra > exts(im_si) c1=1;
if (int)ra = exts(im_si) c2=1;
c3=XER[S0];
int n=bf;
CR[n]=c0; 
//CR[1]=c1; CR[2]=c2; CR[3]=c3;
""")
#cmpi_Instr = trap.Instruction('CMPI', True)
#cmpi_Instr.setMachineCode(oper_Dform_5, {'primary_opcode': [0,0,1,1,0,1]}, ('cmpi r', '%bf', ' r', '%ra', ' r', '%rb'))
#cmpi_Instr.setCode(opCode,'execute')
#cmpi_Instr.addBehavior(IncrementPC, 'execute')
#cmpi_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
#isa.addInstruction(cmpi_Instr)
#CMPL
opCode = cxx_writer.writer_code.Code("""
int c0,c1,c2,c3;
if (int)ra < (int)rb c0=1;
if (int)ra > (int)rb c1=1;
if (int)ra = (int)rb c2=1;
c3=XER[S0];
int n=bf;
CR[n]=c0; 
//CR[1]=c1; CR[2]=c2; CR[3]=c3;
""")
#cmpl_Instr = trap.Instruction('CMPL', True)
#cmpl_Instr.setMachineCode(oper_Xform_16, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,1,0,0,0,0,0]}, ('cmpi r', '%bf', ' r', '%ra', ' r', '%rb'))
#cmpl_Instr.setCode(opCode,'execute')
#cmpl_Instr.addBehavior(IncrementPC, 'execute')
#cmpi_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
#isa.addInstruction(cmpl_Instr)
#CMPLI
#CNTLZW
#CRAND
#CRANDC
#CREQV
#CRNAND
#CRNOR
#CROR
#CRORC
#CRXOR
#DCBA
#DCBF
#DCBI

