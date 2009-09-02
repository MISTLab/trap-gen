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


import trap

#---------------------------------------------------------
# Instruction Encoding
#---------------------------------------------------------
# Lets now start with defining the instructions, i.e. their bitstring and
# mnemonic and their behavior. Note the zero* field: it is a special identifier and it
# means that all those bits have value 0; the same applies for one*
# As stated in page 175 of "MIPS32 4KTM Processor Core Family Software User’s Manual" 
# (Document Number: MD00016), there are mainly 3 different format types.
# To make the description of some group of instructions easier, another types of 
# instructions will be added.


#General Immediate type format (I-Type)
imm_format = trap.MachineCode([('opcode', 6), ('rs', 5), ('rt', 5), ('immediate', 16)])
imm_format.setVarField('rs', ('GPR', 0), 'in')
imm_format.setVarField('rt', ('GPR', 0), 'inout')

#Jump type format (J-Type)
jump_format = trap.MachineCode([('opcode', 5), ('op2',1), ('target', 26)])
jump_format.setBitfield('opcode',[0, 0, 0, 0, 1])

#General Register type format (R-Type)
register_format = trap.MachineCode([('opcode', 6),('rs', 5),('rt', 5),('rd', 5),('sa', 5),('function', 6)])
register_format.setVarField('rs', ('GPR', 0), 'in')
register_format.setVarField('rt', ('GPR', 0), 'inout')
register_format.setVarField('rd', ('GPR', 0), 'out')

#Branch Instruction format (B-Type)
b_format1 = trap.MachineCode([('op', 1), ('op2', 1), ('op3', 3), ('op4', 1), ('rs', 5), ('rt', 5), ('immediate', 16)])
b_format1.setBitfield('op', [0])
b_format1.setVarField('rs', ('GPR', 0), 'in')
b_format1.setVarField('rt', ('GPR', 0), 'inout')

b_format2 = trap.MachineCode([('opcode', 6), ('rs', 5), ('rt', 1), ('rt2', 2), ('rt3', 2), ('immediate', 16)])
b_format2.setBitfield('opcode', [0, 0, 0, 0, 0, 1])
b_format2.setBitfield('rt2', [0,0])
b_format2.setVarField('rs', ('GPR', 0), 'in')

#Load, Store and Special symbols Instruction format (S-Type)
s_format = trap.MachineCode([('op',3),('op2',1),('op3',2),('rs',5),('rt',5)])
s_format.setVarField('rs', ('GPR', 0), 'in')
s_format.setVarField('rt', ('GPR', 0), 'inout')

