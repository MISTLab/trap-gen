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

# In MICROBLAZE there are two types of instructions: typeA and typeB.
# Obviously, there are many variants for each type.

#OPER with REG
oper_reg = trap.MachineCode([('opcode0', 6), ('rd', 5), ('ra', 5), ('rb',5), ('opcode1',11)])
oper_reg.setVarField('rd', ('GPR', 0), 'out')
oper_reg.setVarField('ra', ('GPR', 0), 'in')
oper_reg.setVarField('rb', ('GPR', 0), 'in')

#OPER with IMM
oper_imm = trap.MachineCode([('opcode', 6), ('rd', 5), ('ra', 5),('imm',16)])
oper_imm.setVarField('rd', ('GPR', 0), 'out')
oper_imm.setVarField('ra', ('GPR', 0), 'in')

#BRANCH COND with REG
branch_cond_reg = trap.MachineCode([('opcode0', 6), ('opcode1', 5), ('ra', 5), ('rb',5), ('opcode2',11)])
branch_cond_reg.setVarField('ra', ('GPR', 0), 'in')
branch_cond_reg.setVarField('rb', ('GPR', 0), 'in')

#BRANCH COND with IMM
branch_cond_imm = trap.MachineCode([('opcode0', 6), ('opcode1', 5), ('ra', 5), ('imm',16)])
branch_cond_imm.setVarField('ra', ('GPR', 0), 'in')

#BRANCH UNCOND with REG
branch_uncond_reg = trap.MachineCode([('opcode0', 6), ('rd', 5), ('opcode1', 5), ('rb',5), ('opcode2',11)])
branch_uncond_reg.setVarField('rd', ('GPR', 0), 'out')
branch_uncond_reg.setVarField('rb', ('GPR', 0), 'in')

#BRANCH UNCOND with IMM
branch_uncond_imm = trap.MachineCode([('opcode0', 6), ('rd', 5), ('opcode1', 5), ('imm',16)])
branch_uncond_imm.setVarField('rd', ('GPR', 0), 'out')

#BARREL with REG
barrel_reg = trap.MachineCode([('opcode0', 6), ('rd', 5), ('ra', 5), ('rb',5), ('opcode1',11)])
barrel_reg.setVarField('rd', ('GPR', 0), 'out')
barrel_reg.setVarField('ra', ('GPR', 0), 'in')
barrel_reg.setVarField('rb', ('GPR', 0), 'in')

#BARREL with IMM
barrel_imm = trap.MachineCode([('opcode0', 6), ('rd', 5), ('ra', 5),('zero',5), ('opcode1', 6), ('imm', 5)])
barrel_imm.setVarField('rd', ('GPR', 0), 'out')
barrel_imm.setVarField('ra', ('GPR', 0), 'in')

#FLOAT compare
float_cmp = trap.MachineCode([('opcode0', 6), ('rd', 5), ('ra', 5),('rb',5), ('opcode1', 4), ('opsel', 3), ('opcode2', 4)])
float_cmp.setVarField('rd', ('GPR', 0), 'out')
float_cmp.setVarField('ra', ('GPR', 0), 'in')
float_cmp.setVarField('rb', ('GPR', 0), 'in')

#FLOAT unary oper
float_unary = trap.MachineCode([('opcode0', 6), ('rd', 5), ('ra', 5), ('zero', 5),('opcode1', 11)])
float_unary.setVarField('rd', ('GPR', 0), 'out')
float_unary.setVarField('ra', ('GPR', 0), 'in')

#IMM code
imm_code = trap.MachineCode([('opcode', 6), ('zero', 5), ('zero', 5),('imm', 16)])

#MFS code
mfs_code = trap.MachineCode([('opcode', 6), ('rd', 5), ('zero', 5), ('sel', 2), ('rs', 14)])
mfs_code.setVarField('rd', ('GPR', 0), 'out')
mfs_code.setBitfield('sel', [1,0])

#MTS code
mts_code = trap.MachineCode([('opcode', 6), ('zero', 5), ('ra', 5), ('sel', 2), ('rs', 14)])
mts_code.setVarField('ra', ('GPR', 0), 'in')
mts_code.setBitfield('sel', [1,1])

#MSR oper
msr_oper = trap.MachineCode([('opcode0', 6), ('rd', 5), ('opcode1', 6), ('imm15', 15)])
msr_oper.setVarField('rd', ('GPR', 0), 'out')

#UNARY oper (SIGN EXTEND - SRA,SRC,SRL)
unary_oper = trap.MachineCode([('opcode0', 6), ('rd', 5), ('ra', 5), ('opcode1', 16)])
unary_oper.setVarField('rd', ('GPR', 0), 'out')
unary_oper.setVarField('ra', ('GPR', 0), 'in')

#CACHE oper
cache_oper = trap.MachineCode([('opcode0', 6), ('zero', 5), ('ra', 5), ('rb', 5), ('opcode1', 11)])
cache_oper.setVarField('ra', ('GPR', 0), 'in')
cache_oper.setVarField('rb', ('GPR', 0), 'in')
