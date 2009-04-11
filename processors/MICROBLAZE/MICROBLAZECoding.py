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
oper_imm.setVarField('imm', ('GPR', 0), 'in')

#BRANCH COND with REG
branch_cond_reg = trap.MachineCode([('opcode0', 6), ('opcode1', 5), ('ra', 5), ('rb',5), ('opcode2',11)])
branch_cond_reg.setVarField('ra', ('GPR', 0), 'in')
branch_cond_reg.setVarField('rb', ('GPR', 0), 'in')

#BRANCH COND with IMM
branch_cond_imm = trap.MachineCode([('opcode0', 6), ('opcode1', 5), ('ra', 5), ('imm',16)])
branch_cond_imm.setVarField('ra', ('GPR', 0), 'in'))
branch_cond_imm.setVarField('imm', ('GPR', 0), 'in'))

#BRANCH UNCOND with REG
branch_uncond_reg = trap.MachineCode([('opcode0', 6), ('rd', 5), ('opcode1', 5), ('rb',5), ('opcode2',11)])
branch_uncond_reg.setVarField('rd', ('GPR', 0), 'out')
branch_uncond_reg.setVarField('rb', ('GPR', 0), 'in')

#BRANCH UNCOND with IMM
branch_uncond_imm = trap.MachineCode([('opcode0', 6), ('rd', 5), ('opcode1', 5), ('imm',16)])
branch_uncond_reg.setVarField('rd', ('GPR', 0), 'out')
branch_uncond_reg.setVarField('imm', ('GPR', 0), 'in')

#BARREL with REG
barrel_reg = trap.MachineCode([('opcode0', 6), ('rd', 5), ('ra', 5), ('rb',5), ('opcode1',11)])
barrel_reg.setVarField('rd', ('GPR', 0), 'out')
barrel_reg.setVarField('ra', ('GPR', 0), 'in')
barrel_reg.setVarField('rb', ('GPR', 0), 'in')

#BARREL with IMM
barrel_imm = trap.MachineCode([('opcode0', 6), ('rd', 5), ('ra', 5),('opcode1',5), ('opcode2', 6), ('imm', 5)])
barrel_imm.setVarField('rd', ('GPR', 0), 'out')
barrel_imm.setVarField('ra', ('GPR', 0), 'in')
barrel_imm.setVarField('imm', ('GPR', 0), 'in')


#~ dataProc_imm_shift = trap.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
#~ # All of the register specifiers are indexes in the registry bank REGS,
#~ # with no offset (so we access them directly, REGS[rn])
#~ dataProc_imm_shift.setVarField('rn', ('REGS', 0), 'in')
#~ dataProc_imm_shift.setVarField('rd', ('REGS', 0), 'out')
#~ dataProc_imm_shift.setVarField('rm', ('REGS', 0), 'in')
#~ dataProc_reg_shift = trap.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('rs', 4), ('zero', 1), ('shift_op', 2), ('one', 1), ('rm', 4)])
#~ dataProc_reg_shift.setVarField('rn', ('REGS', 0), 'in')
#~ dataProc_reg_shift.setVarField('rd', ('REGS', 0), 'out')
#~ dataProc_reg_shift.setVarField('rm', ('REGS', 0), 'in')
#~ dataProc_reg_shift.setVarField('rs', ('REGS', 0), 'in')
#~ dataProc_imm = trap.MachineCode([('cond', 4), ('id', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('rotate', 4), ('immediate', 8)])
#~ dataProc_imm.setVarField('rn', ('REGS', 0), 'in')
#~ dataProc_imm.setVarField('rd', ('REGS', 0), 'out')
#~ dataProc_imm.setBitfield('id', [0, 0, 1])
#~ 
#~ move_imm2psr = trap.MachineCode([('cond', 4), ('opcode0', 5), ('r', 1), ('opcode1', 2), ('mask', 4), ('rd', 4), ('rotate', 4), ('immediate', 8)])
#~ move_imm2psr_reg = trap.MachineCode([('cond', 4), ('opcode0', 5), ('r', 1), ('opcode1', 2), ('mask', 4), ('one', 4), ('zero', 8), ('rm', 4)])
#~ move_imm2psr_reg.setVarField('rm', ('REGS', 0), 'in')
#~ 
#~ ls_immOff = trap.MachineCode([('cond', 4), ('opcode', 3), ('p', 1), ('u', 1), ('b', 1), ('w', 1), ('l', 1), ('rn', 4), ('rd', 4), ('immediate', 12)])
#~ ls_immOff.setBitfield('opcode', [0, 1, 0])
#~ ls_immOff.setVarField('rn', ('REGS', 0), 'in')
#~ ls_immOff.setVarField('rd', ('REGS', 0), 'out')
#~ ls_regOff = trap.MachineCode([('cond', 4), ('opcode', 3), ('p', 1), ('u', 1), ('b', 1), ('w', 1), ('l', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
#~ ls_regOff.setBitfield('opcode', [0, 1, 1])
#~ ls_regOff.setVarField('rn', ('REGS', 0), 'in')
#~ ls_regOff.setVarField('rd', ('REGS', 0), 'out')
#~ ls_regOff.setVarField('rm', ('REGS', 0), 'in')
#~ lsshb_regOff = trap.MachineCode([('cond', 4), ('opcode0', 3), ('p', 1), ('u', 1), ('i', 1), ('w', 1), ('l', 1), ('rn', 4), ('rd', 4), ('addr_mode0', 4), ('opcode1', 4), ('addr_mode1', 4)])
#~ lsshb_regOff.setBitfield('opcode0', [0, 0, 0])
#~ lsshb_regOff.setVarField('rn', ('REGS', 0), 'in')
#~ lsshb_regOff.setVarField('rd', ('REGS', 0), 'out')
#~ ls_multiple = trap.MachineCode([('cond', 4), ('opcode', 3), ('p', 1), ('u', 1), ('s', 1), ('w', 1), ('l', 1), ('rn', 4), ('reg_list', 16)])
#~ ls_multiple.setBitfield('opcode', [1, 0, 0])
#~ ls_multiple.setVarField('rn', ('REGS', 0))
#~ 
#~ branch = trap.MachineCode([('cond', 4), ('opcode', 3), ('l', 1), ('offset', 24)])
#~ branch.setBitfield('opcode', [1, 0, 1])
#~ branch_thumb = trap.MachineCode([('cond', 4), ('opcode0', 8), ('zero', 12), ('opcode1', 4), ('rm', 4)])
#~ branch_thumb.setBitfield('opcode0', [0, 0, 0, 1, 0, 0, 1, 0])
#~ branch_thumb.setBitfield('opcode1', [0, 0, 0, 1])
#~ branch_thumb.setVarField('rm', ('REGS', 0), 'in')
#~ 
#~ multiply = trap.MachineCode([('cond', 4), ('opcode0', 7), ('s', 1), ('rd', 4), ('rn', 4), ('rs', 4), ('opcode1', 4), ('rm', 4)])
#~ multiply.setVarField('rd', ('REGS', 0), 'out')
#~ multiply.setVarField('rs', ('REGS', 0), 'in')
#~ multiply.setVarField('rm', ('REGS', 0), 'in')
#~ multiply.setBitfield('opcode1', [1, 0, 0, 1])
#~ 
#~ swi = trap.MachineCode([('cond', 4), ('one', 4), ('swi_number', 24)])
#~ swap = trap.MachineCode([('cond', 4), ('opcode0', 5), ('b', 1), ('zero', 2), ('rn', 4), ('rd', 4), ('zero', 4), ('opcode1', 4), ('rm', 4)])
#~ swap.setVarField('rd', ('REGS', 0), 'out')
#~ swap.setVarField('rn', ('REGS', 0), 'in')
#~ swap.setVarField('rm', ('REGS', 0), 'in')
#~ swap.setBitfield('opcode0', [0, 0, 0, 1, 0])
#~ swap.setBitfield('opcode1', [1, 0, 0, 1])
#~ 
#~ # Co-Processor Instructions
#~ cp_ls = trap.MachineCode([('cond', 4), ('opcode', 3), ('p', 1), ('u', 1), ('n', 1), ('w', 1), ('l', 1), ('rn', 4), ('crd', 4), ('cpnum', 4), ('offset', 8)])
#~ cp_ls.setBitfield('opcode', [1, 1, 0])
#~ cp_ls.setVarField('rn', ('REGS', 0))
#~ cp_dataProc = trap.MachineCode([('cond', 4), ('opcode0', 4), ('opcode1', 4), ('crn', 4), ('crd', 4), ('cpnum', 4), ('opcode2', 4), ('zero', 1), ('crm', 4)])
#~ cp_dataProc.setBitfield('opcode0', [1, 1, 1, 0])
#~ cp_regMove = trap.MachineCode([('cond', 4), ('opcode0', 4), ('opcode1', 3), ('l', 1), ('crn', 4), ('crd', 4), ('cpnum', 4), ('opcode2', 4), ('one', 1), ('crm', 4)])
#~ cp_regMove.setBitfield('opcode0', [1, 1, 1, 0])
#~ 
