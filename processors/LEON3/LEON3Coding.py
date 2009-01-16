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
## Lets now start with defining the instructions, i.e. their bitstring and
## mnemonic and their behavior (look at page 68 of the ARM Architecture
## Reference Manual). Note the zero* field: it is a special identifier and it
## means that all those bits have value 0; the same applies for one*
#dataProc_imm_shift = trap.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
## All of the register specifiers are indexes in the registry bank REGS,
## with no offset (so we access them directly, REGS[rn])
#dataProc_imm_shift.setVarField('rn', ('REGS', 0))
#dataProc_imm_shift.setVarField('rd', ('REGS', 0))
#dataProc_imm_shift.setVarField('rm', ('REGS', 0))
