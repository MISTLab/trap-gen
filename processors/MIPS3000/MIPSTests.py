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



from MIPSIsa import *

#
# ADD instruction family
#

add_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x44444444,   'GPR[11]' : 0x44444444, 'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0x44444444,   'GPR[11]' : 0x44444444, 'PC' : 0x4})
add_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x44444441,   'GPR[11]' : 0x44444444, 'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0x44444441,   'GPR[11]' : 0x44444444, 'PC' : 0x4})
add_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x88888888,   'GPR[11]' : 0x99999999, 'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0x88888888,   'GPR[11]' : 0x99999999, 'PC' : 0x4})
add_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : -5,   'GPR[11]' : 4, 'PC' : 0}, {'GPR[0]' : -1, 'GPR[10]' : -5,   'GPR[11]' : 4, 'PC' : 4})
add_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 4,   'GPR[11]' : -5, 'PC' : 0}, {'GPR[0]' : -1, 'GPR[10]' : 4,   'GPR[11]' : -5, 'PC' : 4})
add_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : -4,   'GPR[11]' : 4, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : -4,   'GPR[11]' : 4, 'PC' : 4})


addi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 7}, {'GPR[0]' : 0, 'GPR[10]' : 4,   'PC' : 0}, {'GPR[0]' : 11, 'GPR[10]' : 4,   'PC' : 4})
addi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': -7}, {'GPR[0]' : 0, 'GPR[10]' : 4,   'PC' : 0}, {'GPR[0]' : -3, 'GPR[10]' : 4,   'PC' : 4})
addi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': -5}, {'GPR[0]' : 8, 'GPR[10]' : 5,   'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 5,   'PC' : 4})
addi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 2}, {'GPR[0]' : 0, 'GPR[10]' : 4294967295,   'PC' : 0}, {'GPR[0]' : 0x1, 'GPR[10]' : 4294967295,   'PC' : 4})
addi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0x0FFF}, {'GPR[0]' : 0, 'GPR[10]' : -4095,   'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : -4095,   'PC' : 4})
addi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0x8FFF}, {'GPR[0]' : 0, 'GPR[10]' : 4095,   'PC' : 0}, {'GPR[0]' : 0xFFFF9FFE, 'GPR[10]' : 4095,   'PC' : 4})
addi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0xAAAA}, {'GPR[0]' : 0, 'GPR[10]' : 0x12341234,   'PC' : 0}, {'GPR[0]' : 0x1233BCDE, 'GPR[10]' : 0x12341234,   'PC' : 4})


addiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 7}, {'GPR[0]' : 0, 'GPR[10]' : 4,   'PC' : 0}, {'GPR[0]' : 11, 'GPR[10]' : 4,   'PC' : 4})
addiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': -7}, {'GPR[0]' : 0, 'GPR[10]' : 4,   'PC' : 0}, {'GPR[0]' : -3, 'GPR[10]' : 4,   'PC' : 4})
addiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': -5}, {'GPR[0]' : 0, 'GPR[10]' : 5,   'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 5,   'PC' : 4})
addiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 2}, {'GPR[0]' : 0, 'GPR[10]' : 4294967295,   'PC' : 0}, {'GPR[0]' : 0x1, 'GPR[10]' : 4294967295,   'PC' : 4})
addiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0x0FFF}, {'GPR[0]' : 0, 'GPR[10]' : -4095,   'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : -4095,   'PC' : 4})
addiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0x8FFF}, {'GPR[0]' : 0, 'GPR[10]' : 4095,   'PC' : 0}, {'GPR[0]' : 0xFFFF9FFE, 'GPR[10]' : 4095,   'PC' : 4})
addiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0xAAAA}, {'GPR[0]' : 0, 'GPR[10]' : 0x12341234,   'PC' : 0}, {'GPR[0]' : 0x1233BCDE, 'GPR[10]' : 0x12341234,   'PC' : 4})


addu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x44444444,   'GPR[11]' : 0x44444444, 'PC' : 0}, {'GPR[0]' : 0x88888888, 'GPR[10]' : 0x44444444,   'GPR[11]' : 0x44444444, 'PC' : 0x4})
addu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x44444441,   'GPR[11]' : 0x44444444, 'PC' : 0}, {'GPR[0]' : 0x88888885, 'GPR[10]' : 0x44444441,   'GPR[11]' : 0x44444444, 'PC' : 0x4})
addu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x88888888,   'GPR[11]' : 0x99999999, 'PC' : 0}, {'GPR[0]' : 0x22222221, 'GPR[10]' : 0x88888888,   'GPR[11]' : 0x99999999, 'PC' : 0x4})
addu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : -5,   'GPR[11]' : 4, 'PC' : 0}, {'GPR[0]' : -1, 'GPR[10]' : -5,   'GPR[11]' : 4, 'PC' : 4})
addu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 4,   'GPR[11]' : -5, 'PC' : 0}, {'GPR[0]' : -1, 'GPR[10]' : 4,   'GPR[11]' : -5, 'PC' : 4})
addu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : -4,   'GPR[11]' : 4, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : -4,   'GPR[11]' : 4, 'PC' : 4})



#
#AND instruction family
#


and_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 0}, {'GPR[0]' : 0xFFFFFFFF, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 4})
and_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x00000000, 'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x00000000, 'PC' : 4})
and_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x55555555, 'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x55555555, 'PC' : 4})
and_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 0}, {'GPR[0]' : 0xAAAAAAAA, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 4})
and_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x22222222, 'PC' : 0}, {'GPR[0]' : 0x22222222, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x22222222, 'PC' : 4})
and_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x12341234,   'GPR[11]' : 0x23412341, 'PC' : 0}, {'GPR[0]' : 0x2000200, 'GPR[10]' : 0x12341234,   'GPR[11]' : 0x23412341, 'PC' : 4})


andi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0xFFFF}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFFFF,  'PC' : 0}, {'GPR[0]' : 0x0FFFF, 'GPR[10]' : 0xFFFFFFFF,   'PC' : 4})
andi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0x0}, {'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0x00000000,   'PC' : 4})
andi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0x5555}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0xAAAAAAAA,   'PC' : 4})
andi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0xFFFF}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'PC' : 0}, {'GPR[0]' : 0x0AAAA, 'GPR[10]' : 0xAAAAAAAA,   'PC' : 4})
andi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0x2222}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'PC' : 0}, {'GPR[0]' : 0x02222, 'GPR[10]' : 0xAAAAAAAA,   'PC' : 4})
andi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0x2341}, {'GPR[0]' : 0, 'GPR[10]' : 0x12341234,   'PC' : 0}, {'GPR[0]' : 0x0200, 'GPR[10]' : 0x12341234,   'PC' : 4})



#
#BRANCH instruction family
#

b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0xFFF,  'op4' : 0, 'op2' : 0},{'GPR[0]' : 0, 'GPR[10]': 0, 'PC' :0},{'PC' : 0x3FFC})
b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0x1A8,  'op4' : 0, 'op2' : 0},{'GPR[0]' : 0xA6BB88C6, 'GPR[10]': 0xA6BB88C6, 'PC' :0x456},{'PC' : 0xAF6})
b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0x1A8,  'op4' : 0, 'op2' : 0},{'GPR[0]' : 0xA6BB88C6, 'GPR[10]': 0xA6BB88C5, 'PC' :0x456},{'PC' : 0x45A})
b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0xAAA,  'op4' : 0, 'op2' : 0},{'GPR[0]' : 0x80000001, 'GPR[10]': 0x1, 'PC' :0x456},{'PC' : 0x45A})

b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0xFFF,  'op4' : 1, 'op2' : 0},{'GPR[0]' : 0, 'GPR[10]': 0, 'PC' :0},{'PC' : 4})
b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0x1A8,  'op4' : 1, 'op2' : 0},{'GPR[0]' : 0xA6BB88C6, 'GPR[10]': 0xA6BB88C6, 'PC' :0x456},{'PC' : 0x45A})
b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0x1A8,  'op4' : 1, 'op2' : 0},{'GPR[0]' : 0xA6BB88C6, 'GPR[10]': 0xA6BB88C5, 'PC' :0x456},{'PC' : 0xAF6})
b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0xAAA,  'op4' : 1, 'op2' : 0},{'GPR[0]' : 0x80000001, 'GPR[10]': 0x1, 'PC' :0x456},{'PC' : 0x2EFE})

b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0xFFF,  'op4' : 0, 'op2' : 1},{'GPR[0]' : 0, 'GPR[10]': 0, 'PC' :0},{'PC' : 0x3FFC})
b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0x1A8,  'op4' : 0, 'op2' : 1},{'GPR[0]' : 0xA6BB88C6, 'GPR[10]': 0xA6BB88C6, 'PC' :0x456},{'PC' : 0xAF6})
b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0x1A8,  'op4' : 0, 'op2' : 1},{'GPR[0]' : 0xA6BB88C6, 'GPR[10]': 0xA6BB88C5, 'PC' :0x456},{'PC' : 0x45A})
b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0xAAA,  'op4' : 0, 'op2' : 1},{'GPR[0]' : 0x80000001, 'GPR[10]': 0x1, 'PC' :0x456},{'PC' : 0x45A})

b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0xFFF,  'op4' : 1, 'op2' : 1},{'GPR[0]' : 0, 'GPR[10]': 0, 'PC' :0},{'PC' : 4})
b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0x1A8,  'op4' : 1, 'op2' : 1},{'GPR[0]' : 0xA6BB88C6, 'GPR[10]': 0xA6BB88C6, 'PC' :0x456},{'PC' : 0x45A})
b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0x1A8,  'op4' : 1, 'op2' : 1},{'GPR[0]' : 0xA6BB88C6, 'GPR[10]': 0xA6BB88C5, 'PC' :0x456},{'PC' : 0xAF6})
b2r_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate' : 0xAAA,  'op4' : 1, 'op2' : 1},{'GPR[0]' : 0x80000001, 'GPR[10]': 0x1, 'PC' :0x456},{'PC' : 0x2EFE})


bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'op4' : 0, 'op2' : 0},{'GPR[0]' : 0x80000001, 'PC' :0x456},{'PC' : 0x2EFE})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'op4' : 0, 'op2' : 0},{'GPR[0]' : 0x00000000, 'PC' :0x400},{'PC' : 0xFFFEAEA8})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'op4' : 0, 'op2' : 0},{'GPR[0]' : 0xFFFFFFFF, 'PC' :0xB00},{'PC' : 0xAFC})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'op4' : 0, 'op2' : 0},{'GPR[0]' : 0xA9274956, 'PC' :0xD75},{'PC' : 0xD341})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'op4' : 0, 'op2' : 0},{'GPR[0]' : 0x00000001, 'PC' :0x456},{'PC' : 0x45A})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'op4' : 0, 'op2' : 0},{'GPR[0]' : 0x06, 'PC' :0x400},{'PC' : 0x404})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'op4' : 0, 'op2' : 0},{'GPR[0]' : 0x7FFFFFFF, 'PC' :0xB00},{'PC' : 0xB04})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'op4' : 0, 'op2' : 0},{'GPR[0]' : 0x29274956, 'PC' :0xD75},{'PC' : 0xD79})

bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'op4' : 0, 'op2' : 1},{'GPR[0]' : 0x80000001, 'PC' :0x456},{'PC' : 0x2EFE})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'op4' : 0, 'op2' : 1},{'GPR[0]' : 0x00000000, 'PC' :0x400},{'PC' : 0xFFFEAEA8})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'op4' : 0, 'op2' : 1},{'GPR[0]' : 0xFFFFFFFF, 'PC' :0xB00},{'PC' : 0xAFC})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'op4' : 0, 'op2' : 1},{'GPR[0]' : 0xA9274956, 'PC' :0xD75},{'PC' : 0xD341})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'op4' : 0, 'op2' : 1},{'GPR[0]' : 0x00000001, 'PC' :0x456},{'PC' : 0x45A})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'op4' : 0, 'op2' : 1},{'GPR[0]' : 0x06, 'PC' :0x400},{'PC' : 0x404})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'op4' : 0, 'op2' : 1},{'GPR[0]' : 0x7FFFFFFF, 'PC' :0xB00},{'PC' : 0xB04})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'op4' : 0, 'op2' : 1},{'GPR[0]' : 0x29274956, 'PC' :0xD75},{'PC' : 0xD79})

bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'op4' : 1, 'op2' : 0},{'GPR[0]' : 0x80000001, 'PC' :0x456},{'PC' : 0x45A})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'op4' : 1, 'op2' : 0},{'GPR[0]' : 0x00000000, 'PC' :0x400},{'PC' : 0x404})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'op4' : 1, 'op2' : 0},{'GPR[0]' : 0xFFFFFFFF, 'PC' :0xB00},{'PC' : 0xB04})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'op4' : 1, 'op2' : 0},{'GPR[0]' : 0xA9274956, 'PC' :0xD75},{'PC' : 0xD79})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'op4' : 1, 'op2' : 0},{'GPR[0]' : 0x00000001, 'PC' :0x456},{'PC' : 0x2EFE})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'op4' : 1, 'op2' : 0},{'GPR[0]' : 0x06, 'PC' :0x400},{'PC' : 0xFFFEAEA8})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'op4' : 1, 'op2' : 0},{'GPR[0]' : 0x7FFFFFFF, 'PC' :0xB00},{'PC' : 0xAFC})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'op4' : 1, 'op2' : 0},{'GPR[0]' : 0x29274956, 'PC' :0xD75},{'PC' : 0xD341})

bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'op4' : 1, 'op2' : 1},{'GPR[0]' : 0x80000001, 'PC' :0x456},{'PC' : 0x45A})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'op4' : 1, 'op2' : 1},{'GPR[0]' : 0x00000000, 'PC' :0x400},{'PC' : 0x404})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'op4' : 1, 'op2' : 1},{'GPR[0]' : 0xFFFFFFFF, 'PC' :0xB00},{'PC' : 0xB04})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'op4' : 1, 'op2' : 1},{'GPR[0]' : 0xA9274956, 'PC' :0xD75},{'PC' : 0xD79})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'op4' : 1, 'op2' : 1},{'GPR[0]' : 0x00000001, 'PC' :0x456},{'PC' : 0x2EFE})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'op4' : 1, 'op2' : 1},{'GPR[0]' : 0x06, 'PC' :0x400},{'PC' : 0xFFFEAEA8})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'op4' : 1, 'op2' : 1},{'GPR[0]' : 0x7FFFFFFF, 'PC' :0xB00},{'PC' : 0xAFC})
bz_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'op4' : 1, 'op2' : 1},{'GPR[0]' : 0x29274956, 'PC' :0xD75},{'PC' : 0xD341})


breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 0, 'rt3' : 0x0},{'GPR[0]' : 0x80000001, 'PC' :0x456},{'PC' : 0x2EFE})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 0, 'rt3' : 0x0},{'GPR[0]' : 0x00000000, 'PC' :0x400},{'PC' : 0x404})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 0, 'rt3' : 0x0},{'GPR[0]' : 0xFFFFFFFF, 'PC' :0xB00},{'PC' : 0xAFC})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 0, 'rt3' : 0x0},{'GPR[0]' : 0xA9274956, 'PC' :0xD75},{'PC' : 0xD341})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 0, 'rt3' : 0x0},{'GPR[0]' : 0x00000001, 'PC' :0x456},{'PC' : 0x45A})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 0, 'rt3' : 0x0},{'GPR[0]' : 0x06, 'PC' :0x400},{'PC' : 0x404})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 0, 'rt3' : 0x0},{'GPR[0]' : 0x7FFFFFFF, 'PC' :0xB00},{'PC' : 0xB04})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 0, 'rt3' : 0x0},{'GPR[0]' : 0x29274956, 'PC' :0xD75},{'PC' : 0xD79})

breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 0, 'rt3' : 0x1},{'GPR[0]' : 0x80000001, 'PC' :0x456},{'PC' : 0x45A})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 0, 'rt3' : 0x1},{'GPR[0]' : 0x00000000, 'PC' :0x400},{'PC' : 0xFFFEAEA8})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 0, 'rt3' : 0x1},{'GPR[0]' : 0xFFFFFFFF, 'PC' :0xB00},{'PC' : 0xB04})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 0, 'rt3' : 0x1},{'GPR[0]' : 0xA9274956, 'PC' :0xD75},{'PC' : 0xD79})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 0, 'rt3' : 0x1},{'GPR[0]' : 0x00000001, 'PC' :0x456},{'PC' : 0x2EFE})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 0, 'rt3' : 0x1},{'GPR[0]' : 0x06, 'PC' :0x400},{'PC' : 0xFFFEAEA8})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 0, 'rt3' : 0x1},{'GPR[0]' : 0x7FFFFFFF, 'PC' :0xB00},{'PC' : 0xAFC})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 0, 'rt3' : 0x1},{'GPR[0]' : 0x29274956, 'PC' :0xD75},{'PC' : 0xD341})

breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 0, 'rt3' : 0x2},{'GPR[0]' : 0x80000001, 'PC' :0x456},{'PC' : 0x2EFE})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 0, 'rt3' : 0x2},{'GPR[0]' : 0x00000000, 'PC' :0x400},{'PC' : 0x404})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 0, 'rt3' : 0x2},{'GPR[0]' : 0xFFFFFFFF, 'PC' :0xB00},{'PC' : 0xAFC})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 0, 'rt3' : 0x2},{'GPR[0]' : 0xA9274956, 'PC' :0xD75},{'PC' : 0xD341})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 0, 'rt3' : 0x2},{'GPR[0]' : 0x00000001, 'PC' :0x456},{'PC' : 0x45A})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 0, 'rt3' : 0x2},{'GPR[0]' : 0x06, 'PC' :0x400},{'PC' : 0x404})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 0, 'rt3' : 0x2},{'GPR[0]' : 0x7FFFFFFF, 'PC' :0xB00},{'PC' : 0xB04})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 0, 'rt3' : 0x2},{'GPR[0]' : 0x29274956, 'PC' :0xD75},{'PC' : 0xD79})

breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 0, 'rt3' : 0x3},{'GPR[0]' : 0x80000001, 'PC' :0x456},{'PC' : 0x45A})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 0, 'rt3' : 0x3},{'GPR[0]' : 0x00000000, 'PC' :0x400},{'PC' : 0xFFFEAEA8})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 0, 'rt3' : 0x3},{'GPR[0]' : 0xFFFFFFFF, 'PC' :0xB00},{'PC' : 0xB04})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 0, 'rt3' : 0x3},{'GPR[0]' : 0xA9274956, 'PC' :0xD75},{'PC' : 0xD79})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 0, 'rt3' : 0x3},{'GPR[0]' : 0x00000001, 'PC' :0x456},{'PC' : 0x2EFE})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 0, 'rt3' : 0x3},{'GPR[0]' : 0x06, 'PC' :0x400},{'PC' : 0xFFFEAEA8})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 0, 'rt3' : 0x3},{'GPR[0]' : 0x7FFFFFFF, 'PC' :0xB00},{'PC' : 0xAFC})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 0, 'rt3' : 0x3},{'GPR[0]' : 0x29274956, 'PC' :0xD75},{'PC' : 0xD341})

breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 1, 'rt3' : 0x0},{'GPR[0]' : 0x80000001, 'PC' : 0x456},{'PC' : 0x2EFE, 'GPR[31]' : 0x45E})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 1, 'rt3' : 0x0},{'GPR[0]' : 0x00000000, 'PC' : 0x400},{'PC' : 0x404, 'GPR[31]' : 0x408})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 1, 'rt3' : 0x0},{'GPR[0]' : 0xFFFFFFFF, 'PC' : 0xB00},{'PC' : 0xAFC, 'GPR[31]' : 0xB08})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 1, 'rt3' : 0x0},{'GPR[0]' : 0xA9274956, 'PC' : 0xD75},{'PC' : 0xD341, 'GPR[31]' : 0xD7D})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 1, 'rt3' : 0x0},{'GPR[0]' : 0x00000001, 'PC' : 0x456},{'PC' : 0x45A, 'GPR[31]' : 0x45E})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 1, 'rt3' : 0x0},{'GPR[0]' : 0x06, 'PC' : 0x400},{'PC' : 0x404, 'GPR[31]' : 0x408})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 1, 'rt3' : 0x0},{'GPR[0]' : 0x7FFFFFFF, 'PC' : 0xB00},{'PC' : 0xB04, 'GPR[31]' : 0xB08})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 1, 'rt3' : 0x0},{'GPR[0]' : 0x29274956, 'PC' : 0xD75},{'PC' : 0xD79, 'GPR[31]' : 0xD7D})

breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 1, 'rt3' : 0x1},{'GPR[0]' : 0x80000001, 'PC' : 0x456},{'PC' : 0x45A, 'GPR[31]' : 0x45E})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 1, 'rt3' : 0x1},{'GPR[0]' : 0x00000000, 'PC' : 0x400},{'PC' : 0xFFFEAEA8, 'GPR[31]' : 0x408})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 1, 'rt3' : 0x1},{'GPR[0]' : 0xFFFFFFFF, 'PC' : 0xB00},{'PC' : 0xB04, 'GPR[31]' : 0xB08})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 1, 'rt3' : 0x1},{'GPR[0]' : 0xA9274956, 'PC' : 0xD75},{'PC' : 0xD79, 'GPR[31]' : 0xD7D})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 1, 'rt3' : 0x1},{'GPR[0]' : 0x00000001, 'PC' : 0x456},{'PC' : 0x2EFE, 'GPR[31]' : 0x45E})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 1, 'rt3' : 0x1},{'GPR[0]' : 0x06, 'PC' : 0x400},{'PC' : 0xFFFEAEA8, 'GPR[31]' : 0x408})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 1, 'rt3' : 0x1},{'GPR[0]' : 0x7FFFFFFF, 'PC' : 0xB00},{'PC' : 0xAFC, 'GPR[31]' : 0xB08})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 1, 'rt3' : 0x1},{'GPR[0]' : 0x29274956, 'PC' : 0xD75},{'PC' : 0xD341, 'GPR[31]' : 0xD7D})

breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 1, 'rt3' : 0x2},{'GPR[0]' : 0x80000001, 'PC' : 0x456},{'PC' : 0x2EFE, 'GPR[31]' : 0x45E})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 1, 'rt3' : 0x2},{'GPR[0]' : 0x00000000, 'PC' : 0x400},{'PC' : 0x404, 'GPR[31]' : 0x408})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 1, 'rt3' : 0x2},{'GPR[0]' : 0xFFFFFFFF, 'PC' : 0xB00},{'PC' : 0xAFC, 'GPR[31]' : 0xB08})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 1, 'rt3' : 0x2},{'GPR[0]' : 0xA9274956, 'PC' : 0xD75},{'PC' : 0xD341, 'GPR[31]' : 0xD7D})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 1, 'rt3' : 0x2},{'GPR[0]' : 0x00000001, 'PC' : 0x456},{'PC' : 0x45A, 'GPR[31]' : 0x45E})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 1, 'rt3' : 0x2},{'GPR[0]' : 0x06, 'PC' : 0x400},{'PC' : 0x404, 'GPR[31]' : 0x408})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 1, 'rt3' : 0x2},{'GPR[0]' : 0x7FFFFFFF, 'PC' : 0xB00},{'PC' : 0xB04, 'GPR[31]' : 0xB08})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 1, 'rt3' : 0x2},{'GPR[0]' : 0x29274956, 'PC' : 0xD75},{'PC' : 0xD79, 'GPR[31]' : 0xD7D})

breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 1, 'rt3' : 0x3},{'GPR[0]' : 0x80000001, 'PC' : 0x456},{'PC' : 0x45A, 'GPR[31]' : 0x45E})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 1, 'rt3' : 0x3},{'GPR[0]' : 0x00000000, 'PC' : 0x400},{'PC' : 0xFFFEAEA8, 'GPR[31]' : 0x408})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 1, 'rt3' : 0x3},{'GPR[0]' : 0xFFFFFFFF, 'PC' : 0xB00},{'PC' : 0xB04, 'GPR[31]' : 0xB08})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 1, 'rt3' : 0x3},{'GPR[0]' : 0xA9274956, 'PC' : 0xD75},{'PC' : 0xD79, 'GPR[31]' : 0xD7D})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAA,  'rt' : 1, 'rt3' : 0x3},{'GPR[0]' : 0x00000001, 'PC' : 0x456},{'PC' : 0x2EFE, 'GPR[31]' : 0x45E})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xAAAA,  'rt' : 1, 'rt3' : 0x3},{'GPR[0]' : 0x06, 'PC' : 0x400},{'PC' : 0xFFFEAEA8, 'GPR[31]' : 0x408})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0xFFFF,  'rt' : 1, 'rt3' : 0x3},{'GPR[0]' : 0x7FFFFFFF, 'PC' : 0xB00},{'PC' : 0xAFC, 'GPR[31]' : 0xB08})
breg_imm_Instr.addTest({'rs': 0, 'immediate' : 0x3173,  'rt' : 1, 'rt3' : 0x3},{'GPR[0]' : 0x29274956, 'PC' : 0xD75},{'PC' : 0xD341, 'GPR[31]' : 0xD7D})



#
#BREAK
#

break_reg_Instr.addTest({},{},{})



#
#CLO
#


clo_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0X12341234,  'PC' : 0},{'GPR[0]': 10,   'GPR[10]': 0X12341234,  'PC' : 4})
clo_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0X11111111,  'PC' : 0},{'GPR[0]': 8,   'GPR[10]': 0X11111111,  'PC' : 4})
clo_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0XFFFFFFFF,  'PC' : 0},{'GPR[0]': 32,   'GPR[10]': 0XFFFFFFFF,  'PC' : 4})
clo_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0X00000000,  'PC' : 0},{'GPR[0]': 0,   'GPR[10]': 0X00000000,  'PC' : 4})
clo_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0X12345678,  'PC' : 0},{'GPR[0]': 13,   'GPR[10]': 0X12345678,  'PC' : 4})
clo_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0X87654321,  'PC' : 0},{'GPR[0]': 13,   'GPR[10]': 0X87654321,  'PC' : 4})
clo_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0XFFFF0000,  'PC' : 0},{'GPR[0]': 16,   'GPR[10]': 0XFFFF0000,  'PC' : 4})


#
#CLZ
#


clz_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0X12341234,  'PC' : 0},{'GPR[0]': 22,   'GPR[10]': 0X12341234,  'PC' : 4})
clz_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0X11111111,  'PC' : 0},{'GPR[0]': 24,   'GPR[10]': 0X11111111,  'PC' : 4})
clz_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0XFFFFFFFF,  'PC' : 0},{'GPR[0]': 0,   'GPR[10]': 0XFFFFFFFF,  'PC' : 4})
clz_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0X00000000,  'PC' : 0},{'GPR[0]': 32,   'GPR[10]': 0X00000000,  'PC' : 4})
clz_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0X12345678,  'PC' : 0},{'GPR[0]': 19,   'GPR[10]': 0X12345678,  'PC' : 4})
clz_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0X87654321,  'PC' : 0},{'GPR[0]': 19,   'GPR[10]': 0X87654321,  'PC' : 4})
clz_reg_Instr.addTest({'rd': 0, 'rs': 10},{'GPR[0]': 0,   'GPR[10]': 0XFFFF0000,  'PC' : 0},{'GPR[0]': 16,   'GPR[10]': 0XFFFF0000,  'PC' : 4})


#
#DIV instruction family
#


div_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 286331153,   'GPR[10]': 45869,  'PC' : 0},{'HI': 16855,   'LO': 6242,   'GPR[0]': 286331153,   'GPR[10]': 45869,  'PC' : 4})
div_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 8,   'GPR[10]': 4,  'PC' : 0},{'HI': 0,   'LO': 2,   'GPR[0]': 8,   'GPR[10]': 4,  'PC' : 4})
div_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 2,  'PC' : 0},{'HI': -1,   'LO': 0,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 2,  'PC' : 4})
div_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': -1000000,   'GPR[10]': 3,  'PC' : 0},{'HI': -1,   'LO': -333333,   'GPR[0]': -1000000,   'GPR[10]': 3,  'PC' : 4})
div_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 0x7FFFFFFF,   'GPR[10]': 467,  'PC' : 0},{'HI': 25,   'LO': 4598466,   'GPR[0]': 0x7FFFFFFF,   'GPR[10]': 467,  'PC' : 4})
div_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 0x80000001,   'GPR[10]': 467,  'PC' : 0},{'HI': -25,   'LO': -4598466,   'GPR[0]': 0x80000001,   'GPR[10]': 467,  'PC' : 4})
div_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 0x0,   'GPR[10]': 467,  'PC' : 0},{'HI': 0,   'LO': 0,   'GPR[0]': 0,   'GPR[10]': 467,  'PC' : 4})
div_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 0},{'HI': 467,   'LO': 0,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 4})


divu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 286331153,   'GPR[10]': 45869,  'PC' : 0},{'HI': 16855,   'LO': 6242,   'GPR[0]': 286331153,   'GPR[10]': 45869,  'PC' : 4})
divu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 8,   'GPR[10]': 4,  'PC' : 0},{'HI': 0,   'LO': 2,   'GPR[0]': 8,   'GPR[10]': 4,  'PC' : 4})
divu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 2,  'PC' : 0},{'HI': 1,   'LO': 0x7FFFFFFF,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 2,  'PC' : 4})
divu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 1000000,   'GPR[10]': 3,  'PC' : 0},{'HI': 1,   'LO': 333333,   'GPR[0]': 1000000,   'GPR[10]': 3,  'PC' : 4})
divu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 0x7FFFFFFF,   'GPR[10]': 467,  'PC' : 0},{'HI': 25,   'LO': 4598466,   'GPR[0]': 0x7FFFFFFF,   'GPR[10]': 467,  'PC' : 4})
divu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 0x80000001,   'GPR[10]': 467,  'PC' : 0},{'HI': 27,   'LO': 4598466,   'GPR[0]': 0x80000001,   'GPR[10]': 467,  'PC' : 4})
divu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 0x0,   'GPR[10]': 467,  'PC' : 0},{'HI': 0,   'LO': 0,   'GPR[0]': 0,   'GPR[10]': 467,  'PC' : 4})
divu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 0},{'HI': 467,   'LO': 0,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 4})



#
#JUMP Instruction Family
#

j_jump_Instr.addTest({'op2': 0, 'target': 0x3FFFFFF},{'PC': 0x40000000},{'PC': 0x4FFFFFFC})
j_jump_Instr.addTest({'op2': 0, 'target': 0x3FFFFFF},{'PC': 0x44477BCB},{'PC': 0x4FFFFFFC})
j_jump_Instr.addTest({'op2': 0, 'target': 0x3FFFFFF},{'PC': 0xF000BCD0},{'PC': 0xFFFFFFFC})
j_jump_Instr.addTest({'op2': 0, 'target': 0x3FFFFFF},{'PC': 0x06200BBB},{'PC': 0x0FFFFFFC})
j_jump_Instr.addTest({'op2': 0, 'target': 0x3111111},{'PC': 0xB0000000},{'PC': 0xBC444444})
j_jump_Instr.addTest({'op2': 0, 'target': 0x1234},{'PC': 0xA0000000},{'PC': 0xA00048D0})
j_jump_Instr.addTest({'op2': 0, 'target': 0x3F},{'PC': 0},{'PC': 0xFC})

j_jump_Instr.addTest({'op2': 1, 'target': 0x3FFFFFF},{'PC': 0x40000000},{'PC': 0x4FFFFFFC, 'GPR[31]': 0x40000008})
j_jump_Instr.addTest({'op2': 1, 'target': 0x3FFFFFF},{'PC': 0x44477BCB},{'PC': 0x4FFFFFFC, 'GPR[31]': 0x44477BD3})
j_jump_Instr.addTest({'op2': 1, 'target': 0x3FFFFFF},{'PC': 0xF000BCD0},{'PC': 0xFFFFFFFC, 'GPR[31]': 0xF000BCD8})
j_jump_Instr.addTest({'op2': 1, 'target': 0x3FFFFFF},{'PC': 0x06200BBB},{'PC': 0x0FFFFFFC, 'GPR[31]': 0x06200BC3})
j_jump_Instr.addTest({'op2': 1, 'target': 0x3111111},{'PC': 0xB0000000},{'PC': 0xBC444444, 'GPR[31]': 0xB0000008})
j_jump_Instr.addTest({'op2': 1, 'target': 0x1234},{'PC': 0xA0000000},{'PC': 0xA00048D0, 'GPR[31]': 0xA0000008})
j_jump_Instr.addTest({'op2': 1, 'target': 0x3F},{'PC': 0},{'PC': 0xFC, 'GPR[31]': 0x8})


jr_jump_Instr.addTest({'rs': 0},{'PC': 0x40000000, 'GPR[0]': 0xFBBDD770},{'PC': 0xFBBDD770})
jr_jump_Instr.addTest({'rs': 0},{'PC': 0xFFFFFFFF, 'GPR[0]': 0xFBBDD770},{'PC': 0xFBBDD770})
jr_jump_Instr.addTest({'rs': 0},{'PC': 0x0, 'GPR[0]': 0x55387BD0},{'PC': 0x55387BD0})
jr_jump_Instr.addTest({'rs': 0},{'PC': 0x1234DDEE, 'GPR[0]': 0x6770},{'PC': 0x6770})


jlr_jump_Instr.addTest({'rs': 0, 'rd': 8},{'PC': 0x40000000, 'GPR[0]': 0xFBBDD770},{'PC': 0xFBBDD770, 'GPR[8]': 0x40000008})
jlr_jump_Instr.addTest({'rs': 0, 'rd': 8},{'PC': 0xFFFFFFFF, 'GPR[0]': 0xFBBDD770},{'PC': 0xFBBDD770, 'GPR[8]': 0x7})
jlr_jump_Instr.addTest({'rs': 0, 'rd': 8},{'PC': 0x0, 'GPR[0]': 0x55387BD0},{'PC': 0x55387BD0, 'GPR[8]': 0x8})
jlr_jump_Instr.addTest({'rs': 0, 'rd': 8},{'PC': 0x1234DDEE, 'GPR[0]': 0x6770},{'PC': 0x6770, 'GPR[8]': 0x1234DDF6})


#
#LOAD Instruction Family
#

load_imm_Instr.addTest({'op3': 0, 'rt': 0, 'rs': 2, 'immediate': 0},{'GPR[2]': 4, 'dataMem[0x4]': 0x11223355,   'PC' : 0},{'GPR[0]': 0x00000011,   'PC' : 4})
load_imm_Instr.addTest({'op3': 0, 'rt': 0, 'rs': 2, 'immediate': 0x0FFF},{'GPR[2]': 1, 'dataMem[0x1000]': 0x11223355,   'PC' : 0},{'GPR[0]': 0x00000011,   'PC' : 4})
load_imm_Instr.addTest({'op3': 0, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[2]': 0x6A120000, 'dataMem[0x6A1200A8]': 0xFFFFFFFF,   'PC' : 0},{'GPR[0]': 0xFFFFFFFF,   'PC' : 4})
load_imm_Instr.addTest({'op3': 0, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 4, 'GPR[2]': 0x7A120000,   'PC' : 0},{'GPR[0]': 4,   'PC' : 4})
load_imm_Instr.addTest({'op3': 0, 'rt': 0, 'rs': 2, 'immediate': 0xFFF0},{'GPR[2]': 32, 'dataMem[0x10]': 0x9972845F,   'PC' : 0},{'GPR[0]': 0xFFFFFF99,   'PC' : 4})

load_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0},{'GPR[2]': 4, 'dataMem[0x4]': 0x11223355,   'PC' : 0},{'GPR[0]': 0x00001122,   'PC' : 4})
load_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0x0FFF},{'GPR[2]': 1, 'dataMem[0x1000]': 0x11223355,   'PC' : 0},{'GPR[0]': 0x00001122,   'PC' : 4})
load_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[2]': 0x6A120000, 'dataMem[0x6A1200A8]': 0xFFFFFFFF,   'PC' : 0},{'GPR[0]': 0xFFFFFFFF,   'PC' : 4})
load_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0xA6},{'GPR[2]': 0x6A120000, 'dataMem[0x6A1200A6]': 0x1FFFFFFF,   'PC' : 0},{'GPR[0]': 0x00001FFF,   'PC' : 4})
load_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 4, 'GPR[2]': 0x7A120000,   'PC' : 0},{'GPR[0]': 4,   'PC' : 4})
load_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 4, 'GPR[2]': 3,   'PC' : 0},{'GPR[0]': 4,   'PC' : 4})
load_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0xFFF0},{'GPR[2]': 32, 'dataMem[0x10]': 0x9972845F,   'PC' : 0},{'GPR[0]': 0xFFFF9972,   'PC' : 4})

load_imm_Instr.addTest({'op3': 2, 'rt': 0, 'rs': 2, 'immediate': 0xFFF0},{'GPR[0]': 0xAABB8834, 'GPR[2]': 32, 'dataMem[0x10]': 0x9972845F,   'PC' : 0},{'GPR[0]': 0x9972845F,   'PC' : 4})
load_imm_Instr.addTest({'op3': 2, 'rt': 0, 'rs': 2, 'immediate': 0x0},{'GPR[0]': 0xAABB8834, 'GPR[2]': 1, 'dataMem[0x0]': 0x9972845F,   'PC' : 0},{'GPR[0]': 0x72845F34,   'PC' : 4})
load_imm_Instr.addTest({'op3': 2, 'rt': 0, 'rs': 2, 'immediate': 0x0},{'GPR[0]': 0xAABB8834, 'GPR[2]': 1, 'dataMem[0x1]': 0x9972845F,   'PC' : 0},{'GPR[0]': 0x99728434,   'PC' : 4})
load_imm_Instr.addTest({'op3': 2, 'rt': 0, 'rs': 2, 'immediate': 0x0FFF},{'GPR[0]': 0xAABB8834, 'GPR[2]': 0, 'dataMem[0xFFC]': 0xDDCC7265,   'PC' : 0},{'GPR[0]': 0x65BB8834,   'PC' : 4})
load_imm_Instr.addTest({'op3': 2, 'rt': 0, 'rs': 2, 'immediate': 0xFFF0},{'GPR[0]': 0xAABB8834, 'GPR[2]': 18, 'dataMem[0x0]': 0xDDCC7265,   'PC' : 0},{'GPR[0]': 0x72658834,   'PC' : 4})
load_imm_Instr.addTest({'op3': 2, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 0xAABB8834, 'GPR[2]': 0x7A120000, 'dataMem[0x0]': 0xDDCC7265,   'PC' : 0},{'GPR[0]': 0xAABB8834,   'PC' : 4})

load_imm_Instr.addTest({'op3': 3, 'rt': 0, 'rs': 2, 'immediate': 0},{'GPR[2]': 4, 'dataMem[0x4]': 0x11223355,   'PC' : 0},{'GPR[0]': 0x11223355,   'PC' : 4})
load_imm_Instr.addTest({'op3': 3, 'rt': 0, 'rs': 2, 'immediate': 0x0FFF},{'GPR[2]': 1, 'dataMem[0x1000]': 0x11223355,   'PC' : 0},{'GPR[0]': 0x11223355,   'PC' : 4})
load_imm_Instr.addTest({'op3': 3, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[2]': 0x6A120000, 'dataMem[0x6A1200A8]': 0xFFFFFFFF,   'PC' : 0},{'GPR[0]': 0xFFFFFFFF,   'PC' : 4})
load_imm_Instr.addTest({'op3': 3, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 4, 'GPR[2]': 0x7A120000,   'PC' : 0},{'GPR[0]': 4,   'PC' : 4})
load_imm_Instr.addTest({'op3': 3, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 4, 'GPR[2]': 3,   'PC' : 0},{'GPR[0]': 4,   'PC' : 4})
load_imm_Instr.addTest({'op3': 3, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 4, 'GPR[2]': 2,   'PC' : 0},{'GPR[0]': 4,   'PC' : 4})
load_imm_Instr.addTest({'op3': 3, 'rt': 0, 'rs': 2, 'immediate': 0xFFF0},{'GPR[2]': 32, 'dataMem[0x10]': 0x9972845F,   'PC' : 0},{'GPR[0]': 0x9972845F,   'PC' : 4})


load2_imm_Instr.addTest({'op3': 0, 'rt': 0, 'rs': 2, 'immediate': 0},{'GPR[2]': 4, 'dataMem[0x4]': 0x11223355,   'PC' : 0},{'GPR[0]': 0x00000011,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 0, 'rt': 0, 'rs': 2, 'immediate': 0x0FFF},{'GPR[2]': 1, 'dataMem[0x1000]': 0x11223355,   'PC' : 0},{'GPR[0]': 0x00000011,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 0, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[2]': 0x6A120000, 'dataMem[0x6A1200A8]': 0xFFFFFFFF,   'PC' : 0},{'GPR[0]': 0x000000FF,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 0, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 4, 'GPR[2]': 0x7A120000,   'PC' : 0},{'GPR[0]': 4,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 0, 'rt': 0, 'rs': 2, 'immediate': 0xFFF0},{'GPR[2]': 32, 'dataMem[0x10]': 0x9972845F,   'PC' : 0},{'GPR[0]': 0x00000099,   'PC' : 4})

load2_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0},{'GPR[2]': 4, 'dataMem[0x4]': 0x11223355,   'PC' : 0},{'GPR[0]': 0x00001122,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0x0FFF},{'GPR[2]': 1, 'dataMem[0x1000]': 0x11223355,   'PC' : 0},{'GPR[0]': 0x00001122,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[2]': 0x6A120000, 'dataMem[0x6A1200A8]': 0xFFFFFFFF,   'PC' : 0},{'GPR[0]': 0x0000FFFF,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0xA6},{'GPR[2]': 0x6A120000, 'dataMem[0x6A1200A6]': 0x1FFFFFFF,   'PC' : 0},{'GPR[0]': 0x00001FFF,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 4, 'GPR[2]': 0x7A120000,   'PC' : 0},{'GPR[0]': 4,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 4, 'GPR[2]': 3,   'PC' : 0},{'GPR[0]': 4,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 1, 'rt': 0, 'rs': 2, 'immediate': 0xFFF0},{'GPR[2]': 32, 'dataMem[0x10]': 0x9972845F,   'PC' : 0},{'GPR[0]': 0x00009972,   'PC' : 4})

load2_imm_Instr.addTest({'op3': 2, 'rt': 0, 'rs': 2, 'immediate': 0xFFF0},{'GPR[0]': 0xAABB8834, 'GPR[2]': 32, 'dataMem[0x10]': 0x9972845F,   'PC' : 0,   'PC' : 4},{'GPR[0]': 0xAABB8899})
load2_imm_Instr.addTest({'op3': 2, 'rt': 0, 'rs': 2, 'immediate': 0x0},{'GPR[0]': 0xAABB8834, 'GPR[2]': 1, 'dataMem[0x0]': 0x9972845F,   'PC' : 0},{'GPR[0]': 0xAABB9972,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 2, 'rt': 0, 'rs': 2, 'immediate': 0x0},{'GPR[0]': 0xAABB8834, 'GPR[2]': 5, 'dataMem[0x2]': 0x9972845F,   'PC' : 0},{'GPR[0]': 0xAABB845F,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 2, 'rt': 0, 'rs': 2, 'immediate': 0x0FFF},{'GPR[0]': 0xAABB8834, 'GPR[2]': 0, 'dataMem[0xFFC]': 0xDDCC7265,   'PC' : 0},{'GPR[0]': 0xDDCC7265,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 2, 'rt': 0, 'rs': 2, 'immediate': 0xFFF0},{'GPR[0]': 0xAABB8834, 'GPR[2]': 18, 'dataMem[0x0]': 0xDDCC7265,   'PC' : 0},{'GPR[0]': 0xAADDCC72,   'PC' : 4})
load2_imm_Instr.addTest({'op3': 2, 'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 0xAABB8834, 'GPR[2]': 0x7A120000, 'dataMem[0x0]': 0xDDCC7265,   'PC' : 0},{'GPR[0]': 0xAABB8834,   'PC' : 4})


loadl_imm_Instr.addTest({'rt': 0, 'rs': 2, 'immediate': 0},{'GPR[2]': 4, 'dataMem[0x4]': 0x11223355,   'PC' : 0},{'GPR[0]': 0x11223355, 'LLbit': 1,   'PC' : 4})
loadl_imm_Instr.addTest({'rt': 0, 'rs': 2, 'immediate': 0x0FFF},{'GPR[2]': 1, 'dataMem[0x1000]': 0x11223355,   'PC' : 0},{'GPR[0]': 0x11223355, 'LLbit': 1,   'PC' : 4})
loadl_imm_Instr.addTest({'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[2]': 0x6A120000, 'dataMem[0x6A1200A8]': 0xFFFFFFFF,   'PC' : 0},{'GPR[0]': 0xFFFFFFFF, 'LLbit': 1,   'PC' : 4})
loadl_imm_Instr.addTest({'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 4, 'GPR[2]': 0x7A120000,   'PC' : 0},{'GPR[0]': 4, 'LLbit': 0,   'PC' : 4})
loadl_imm_Instr.addTest({'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 4, 'GPR[2]': 3,   'PC' : 0},{'GPR[0]': 4, 'LLbit': 0,   'PC' : 4})
loadl_imm_Instr.addTest({'rt': 0, 'rs': 2, 'immediate': 0xA8},{'GPR[0]': 4, 'GPR[2]': 2,   'PC' : 0},{'GPR[0]': 4, 'LLbit': 0,   'PC' : 4})
loadl_imm_Instr.addTest({'rt': 0, 'rs': 2, 'immediate': 0xFFF0},{'GPR[2]': 32, 'dataMem[0x10]': 0x9972845F,   'PC' : 0},{'GPR[0]': 0x9972845F, 'LLbit': 1,   'PC' : 4})


lui_imm_Instr.addTest({'rt': 20, 'immediate': 0xAABB},{'PC' : 0},{'GPR[20]': 0xAABB0000,   'PC' : 4})
lui_imm_Instr.addTest({'rt': 20, 'immediate': 0x1234},{'PC' : 0},{'GPR[20]': 0x12340000,   'PC' : 4})
lui_imm_Instr.addTest({'rt': 20, 'immediate': 0xF800},{'PC' : 0},{'GPR[20]': 0xF8000000,   'PC' : 4})
lui_imm_Instr.addTest({'rt': 20, 'immediate': 0xFA},{'PC' : 0},{'GPR[20]': 0xFA0000,   'PC' : 4})
lui_imm_Instr.addTest({'rt': 20, 'immediate': 0x0},{'PC' : 0},{'GPR[20]': 0x0,   'PC' : 4})
lui_imm_Instr.addTest({'rt': 20, 'immediate': 0xFFFF},{'PC' : 0},{'GPR[20]': 0xFFFF0000,   'PC' : 4})
lui_imm_Instr.addTest({'rt': 20, 'immediate': 0x386},{'PC' : 0},{'GPR[20]': 0x3860000,   'PC' : 4})



#
#MULTIPLY Instruction Family
#

madd_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 0},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 4})
madd_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 1,  'PC' : 0},{'HI': 1000,   'LO': 1467,   'GPR[0]': 467,   'GPR[10]': 1,  'PC' : 4})
madd_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 65535,   'GPR[0]': 65535,   'GPR[10]': 2,  'PC' : 0},{'HI': 1000,   'LO': 196605,   'GPR[0]': 65535,   'GPR[10]': 2,  'PC' : 4})
madd_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 65535,   'GPR[0]': 65535,   'GPR[10]': -2,  'PC' : 0},{'HI': 0x3E7,   'LO': 0xFFFF0001,   'GPR[0]': 65535,   'GPR[10]': -2,  'PC' : 4})
madd_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 0xFFF,   'LO': 0xFFFFFFFF,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 0},{'HI': 0x1000,  'LO': 0,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 4})
madd_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 0xEFFF,   'LO': 0xFFFFFFFF,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 0},{'HI': 0xF000,   'LO': 0,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 4})
madd_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 0,   'LO': 0,   'GPR[0]': 0x0FFFFFFF,   'GPR[10]': 0x0FFFFFFF,  'PC' : 0},{'HI': 0xFFFFFF,   'LO': 0xE0000001,   'GPR[0]': 0x0FFFFFFF,   'GPR[10]': 0x0FFFFFFF,  'PC' : 4})


maddu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 0},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 4})
maddu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 1,  'PC' : 0},{'HI': 1000,   'LO': 1467,   'GPR[0]': 467,   'GPR[10]': 1,  'PC' : 4})
maddu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 65535,   'GPR[0]': 65535,   'GPR[10]': 2,  'PC' : 0},{'HI': 1000,   'LO': 196605,   'GPR[0]': 65535,   'GPR[10]': 2,  'PC' : 4})
maddu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 0,   'LO': 0,   'GPR[0]': 0x10,   'GPR[10]': 0xFFFFFFFE,  'PC' : 0},{'HI': 0xF,   'LO': 0xFFFFFFE0,   'GPR[0]': 0x10,   'GPR[10]': -2,  'PC' : 4})
maddu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 0x1,   'LO': 0xFFFFFFFE,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 0},{'HI': 0xFFFFFFFF,   'LO': 0xFFFFFFFF,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 4})


msub_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 0},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 4})
msub_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 1000,   'GPR[0]': 0xFFFFF,   'GPR[10]': 0xFFFFF,  'PC' : 0},{'HI': 0x2E8,   'LO': 0x002003E7,   'GPR[0]': 0xFFFFF,   'GPR[10]': 0xFFFFF,  'PC' : 4})
msub_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 65535,   'GPR[0]': 65535,   'GPR[10]': 2,  'PC' : 0},{'HI': 0x3E7,   'LO': 0xFFFF0001,   'GPR[0]': 65535,   'GPR[10]': 2,  'PC' : 4})
msub_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 65535,   'GPR[0]': 65535,   'GPR[10]': -2,  'PC' : 0},{'HI': 1000,   'LO': 196605,   'GPR[0]': 65535,   'GPR[10]': -2,  'PC' : 4})
msub_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 0x1E8,   'LO': 0x80,   'GPR[0]': 1280000000,   'GPR[10]': 1280000000,  'PC' : 0},{'HI': 0xE9433DC9,   'LO': 0x70000080,   'GPR[0]': 1280000000,   'GPR[10]': 1280000000,  'PC' : 4})


msubu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 0},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 4})
msubu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 1000,   'GPR[0]': 0xFFFFF,   'GPR[10]': 0xFFFFF,  'PC' : 0},{'HI': 0x2E8,   'LO': 0x002003E7,   'GPR[0]': 0xFFFFF,   'GPR[10]': 0xFFFFF,  'PC' : 4})
msubu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 65535,   'GPR[0]': 65535,   'GPR[10]': 2,  'PC' : 0},{'HI': 0x3E7,   'LO': 0xFFFF0001,   'GPR[0]': 65535,   'GPR[10]': 2,  'PC' : 4})
msubu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 65535,   'GPR[0]': 65535,   'GPR[10]': -2,  'PC' : 0},{'HI': 0xFFFF03E9,   'LO': 0x0002FFFD,   'GPR[0]': 65535,   'GPR[10]': -2,  'PC' : 4})
msubu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 0x1E8,   'LO': 0x80,   'GPR[0]': 1280000000,   'GPR[10]': 1280000000,  'PC' : 0},{'HI': 0xE9433DC9,   'LO': 0x70000080,   'GPR[0]': 1280000000,   'GPR[10]': 1280000000,  'PC' : 4})
msubu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 0,   'LO': 0,   'GPR[0]': 0x10,   'GPR[10]': 0xFFFFFFFE,  'PC' : 0},{'HI': 0xFFFFFFF0,   'LO': 0x00000020,   'GPR[0]': 0x10,   'GPR[10]': -2,  'PC' : 4})
msubu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 0x1,   'LO': 0xFFFFFFFE,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 0},{'HI': 0x3,   'LO': 0xFFFFFFFD,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 4})


mul_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 0},{'GPR[0]' : 1, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 4})
mul_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11},{'GPR[0]' : 0, 'GPR[10]' : 32767,   'GPR[11]' : 32767, 'PC' : 0},{'GPR[0]' : 0x3FFF0001, 'GPR[10]' : 32767,   'GPR[11]' : 32767, 'PC' : 4})
mul_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11},{'GPR[0]' : 0, 'GPR[10]' : 32767,   'GPR[11]' : -32767, 'PC' : 0},{'GPR[0]' : 0xC000FFFF, 'GPR[10]' : 32767,   'GPR[11]' : -32767, 'PC' : 4})
mul_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11},{'GPR[0]' : 0, 'GPR[10]' : -32767,   'GPR[11]' : -32767, 'PC' : 0},{'GPR[0]' : 0x3FFF0001, 'GPR[10]' : -32767,   'GPR[11]' : -32767, 'PC' : 4})
mul_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11},{'GPR[0]' : 0, 'GPR[10]' : -2147483647,   'GPR[11]' : -2147483647, 'PC' : 0},{'GPR[0]' : 0x0000001, 'GPR[10]' : -2147483647,   'GPR[11]' : -2147483647, 'PC' : 4})
mul_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11},{'GPR[0]' : 0, 'GPR[10]' : 2147483647,   'GPR[11]' : -2147483647, 'PC' : 0},{'GPR[0]' : 0xFFFFFFFF, 'GPR[10]' : 2147483647,   'GPR[11]' : -2147483647, 'PC' : 4})
mul_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11},{'GPR[0]' : 0, 'GPR[10]' : 874139251,   'GPR[11]' : 54789399, 'PC' : 0},{'GPR[0]' : 0x61714B55, 'GPR[10]' : 874139251,   'GPR[11]' : 54789399, 'PC' : 4})


mult_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 0},{'HI': 0,   'LO': 1,   'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 4})
mult_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : 32767,   'GPR[11]' : 32767, 'PC' : 0},{'HI': 0,   'LO': 0x3FFF0001,   'GPR[10]' : 32767,   'GPR[11]' : 32767, 'PC' : 4})
mult_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : 32767,   'GPR[11]' : -32767, 'PC' : 0},{'HI': 0xFFFFFFFF,   'LO': 0xC000FFFF,   'GPR[10]' : 32767,   'GPR[11]' : -32767, 'PC' : 4})
mult_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : -32767,   'GPR[11]' : -32767, 'PC' : 0},{'HI': 0,   'LO': 0x3FFF0001,   'GPR[10]' : -32767,   'GPR[11]' : -32767, 'PC' : 4})
mult_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : -2147483647,   'GPR[11]' : -2147483647, 'PC' : 0},{'HI': 0x3FFFFFFF,   'LO': 0x00000001,   'GPR[10]' : -2147483647,   'GPR[11]' : -2147483647, 'PC' : 4})
mult_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : 2147483647,   'GPR[11]' : -2147483647, 'PC' : 0},{'HI': 0xC0000000,   'LO': 0xFFFFFFFF,   'GPR[10]' : 2147483647,   'GPR[11]' : -2147483647, 'PC' : 4})
mult_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : 874139251,   'GPR[11]' : 54789399, 'PC' : 0},{'HI': 0xAA26F1,   'LO': 0x61714B55,   'GPR[10]' : 874139251,   'GPR[11]' : 54789399, 'PC' : 4})


multu_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 0},{'HI': 0xFFFFFFFE,   'LO': 1,   'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 4})
multu_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : 32767,   'GPR[11]' : 32767, 'PC' : 0},{'HI': 0,   'LO': 0x3FFF0001,   'GPR[10]' : 32767,   'GPR[11]' : 32767, 'PC' : 4})
multu_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : 32767,   'GPR[11]' : -32767, 'PC' : 0},{'HI': 0x7FFE,   'LO': 0xC000FFFF,   'GPR[10]' : 32767,   'GPR[11]' : -32767, 'PC' : 4})
multu_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : -32767,   'GPR[11]' : -32767, 'PC' : 0},{'HI': 0xFFFF0002,   'LO': 0x3FFF0001,   'GPR[10]' : -32767,   'GPR[11]' : -32767, 'PC' : 4})
multu_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : -2147483647,   'GPR[11]' : -2147483647, 'PC' : 0},{'HI': 0x40000001,   'LO': 0x00000001,   'GPR[10]' : -2147483647,   'GPR[11]' : -2147483647, 'PC' : 4})
multu_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : 2147483647,   'GPR[11]' : -2147483647, 'PC' : 0},{'HI': 0x3FFFFFFF,   'LO': 0xFFFFFFFF,   'GPR[10]' : 2147483647,   'GPR[11]' : -2147483647, 'PC' : 4})
multu_reg_Instr.addTest({'rs': 10, 'rt': 11},{'GPR[10]' : 874139251,   'GPR[11]' : 54789399, 'PC' : 0},{'HI': 0xAA26F1,   'LO': 0x61714B55,   'GPR[10]' : 874139251,   'GPR[11]' : 54789399, 'PC' : 4})



#
#MOVE Instruction Family
#

mfhi_reg_Instr.addTest({'rd':0},{'HI' : 0xFFFF8194,  'PC': 0},{'GPR[0]' : 0xFFFF8194,   'HI': 0xFFFF8194,  'PC': 4})
mfhi_reg_Instr.addTest({'rd':0},{'HI' : 0x7ABCDEF3,  'PC': 0},{'GPR[0]' : 0x7ABCDEF3,   'HI': 0x7ABCDEF3,  'PC': 4})
mfhi_reg_Instr.addTest({'rd':0},{'HI' : -162738495,  'PC': 0},{'GPR[0]' : -162738495,   'HI': -162738495,  'PC': 4})
mfhi_reg_Instr.addTest({'rd':0},{'HI' : 10293847,  'PC': 0},{'GPR[0]' : 10293847,   'HI': 10293847,  'PC': 4})
mfhi_reg_Instr.addTest({'rd':0},{'HI' : 0,  'PC': 0},{'GPR[0]' : 0,   'HI': 0,  'PC': 4})


mflo_reg_Instr.addTest({'rd':0},{'LO' : 0xFFFF8194,  'PC': 0},{'GPR[0]' : 0xFFFF8194,   'LO': 0xFFFF8194,  'PC': 4})
mflo_reg_Instr.addTest({'rd':0},{'LO' : 0x7ABCDEF3,  'PC': 0},{'GPR[0]' : 0x7ABCDEF3,   'LO': 0x7ABCDEF3,  'PC': 4})
mflo_reg_Instr.addTest({'rd':0},{'LO' : -162738495,  'PC': 0},{'GPR[0]' : -162738495,   'LO': -162738495,  'PC': 4})
mflo_reg_Instr.addTest({'rd':0},{'LO' : 10293847,  'PC': 0},{'GPR[0]' : 10293847,   'LO': 10293847,  'PC': 4})
mflo_reg_Instr.addTest({'rd':0},{'LO' : 0,  'PC': 0},{'GPR[0]' : 0,   'LO': 0,  'PC': 4})


mthi_reg_Instr.addTest({'rs':0},{'GPR[0]' : 0xFFFF8194,  'PC': 0},{'GPR[0]' : 0xFFFF8194,   'HI': 0xFFFF8194,  'PC': 4})
mthi_reg_Instr.addTest({'rs':0},{'GPR[0]' : 0x7ABCDEF3,  'PC': 0},{'GPR[0]' : 0x7ABCDEF3,   'HI': 0x7ABCDEF3,  'PC': 4})
mthi_reg_Instr.addTest({'rs':0},{'GPR[0]' : -162738495,  'PC': 0},{'GPR[0]' : -162738495,   'HI': -162738495,  'PC': 4})
mthi_reg_Instr.addTest({'rs':0},{'GPR[0]' : 10293847,  'PC': 0},{'GPR[0]' : 10293847,   'HI': 10293847,  'PC': 4})
mthi_reg_Instr.addTest({'rs':0},{'GPR[0]' : 0,  'PC': 0},{'GPR[0]' : 0,   'HI': 0,  'PC': 4})


mtlo_reg_Instr.addTest({'rs':0},{'GPR[0]' : 0xFFFF8194,  'PC': 0},{'GPR[0]' : 0xFFFF8194,   'LO': 0xFFFF8194,  'PC': 4})
mtlo_reg_Instr.addTest({'rs':0},{'GPR[0]' : 0x7ABCDEF3,  'PC': 0},{'GPR[0]' : 0x7ABCDEF3,   'LO': 0x7ABCDEF3,  'PC': 4})
mtlo_reg_Instr.addTest({'rs':0},{'GPR[0]' : -162738495,  'PC': 0},{'GPR[0]' : -162738495,   'LO': -162738495,  'PC': 4})
mtlo_reg_Instr.addTest({'rs':0},{'GPR[0]' : 10293847,  'PC': 0},{'GPR[0]' : 10293847,   'LO': 10293847,  'PC': 4})
mtlo_reg_Instr.addTest({'rs':0},{'GPR[0]' : 0,  'PC': 0},{'GPR[0]' : 0,   'LO': 0,  'PC': 4})



#
#OR Instruction Family
#

nor_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 4})
nor_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x00000000, 'PC' : 0}, {'GPR[0]' : 0xFFFFFFFF, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x00000000, 'PC' : 4})
nor_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x55555555, 'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x55555555, 'PC' : 4})
nor_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 4})
nor_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x22222222, 'PC' : 0}, {'GPR[0]' : 0x55555555, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x22222222, 'PC' : 4})
nor_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x12341234,   'GPR[11]' : 0x23412341, 'PC' : 0}, {'GPR[0]' : 0xCC8ACC8A, 'GPR[10]' : 0x12341234,   'GPR[11]' : 0x23412341, 'PC' : 4})


or_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 0}, {'GPR[0]' : 0xFFFFFFFF, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 4})
or_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x00000000, 'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x00000000, 'PC' : 4})
or_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x55555555, 'PC' : 0}, {'GPR[0]' : 0xFFFFFFFF, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x55555555, 'PC' : 4})
or_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 0}, {'GPR[0]' : 0xFFFFFFFF, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 4})
or_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x22222222, 'PC' : 0}, {'GPR[0]' : 0xAAAAAAAA, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x22222222, 'PC' : 4})
or_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x12341234,   'GPR[11]' : 0x23412341, 'PC' : 0}, {'GPR[0]' : 0x33753375, 'GPR[10]' : 0x12341234,   'GPR[11]' : 0x23412341, 'PC' : 4})


or_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0xFFFF}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFFFF,  'PC' : 0}, {'GPR[0]' : 0xFFFFFFFF, 'GPR[10]' : 0xFFFFFFFF,   'PC' : 4})
or_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0x0000}, {'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0x00000000,   'PC' : 4})
or_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0x5555}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'PC' : 0}, {'GPR[0]' : 0xAAAAFFFF, 'GPR[10]' : 0xAAAAAAAA,   'PC' : 4})
or_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0xFFFF}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'PC' : 0}, {'GPR[0]' : 0xAAAAFFFF, 'GPR[10]' : 0xAAAAAAAA,   'PC' : 4})
or_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0x2222}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'PC' : 0}, {'GPR[0]' : 0xAAAAAAAA, 'GPR[10]' : 0xAAAAAAAA,   'PC' : 4})
or_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0x2341}, {'GPR[0]' : 0, 'GPR[10]' : 0x12341234,   'PC' : 0}, {'GPR[0]' : 0x12343375, 'GPR[10]' : 0x12341234,   'PC' : 4})



#
#STORE Instruction Family
#

sb_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0x2341},{'GPR[0]': 0, 'GPR[10]': 0x12345678, 'PC' : 0},{'dataMem[0x2341]': 0x78000000,   'PC' : 4})
sb_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xAAAA},{'GPR[0]': 0x5556, 'GPR[10]': 0xAFAFBCDE, 'PC' : 0},{'dataMem[0x0]': 0xDE000000,   'PC' : 4})
sb_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0x1111},{'GPR[0]': 0, 'GPR[10]': 0x80BBDA, 'PC' : 0},{'dataMem[0x1111]': 0xDA000000,   'PC' : 4})
sb_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFFF},{'GPR[0]': 33, 'GPR[10]': 0x45678, 'PC' : 0},{'dataMem[0x20]': 0x78000000,   'PC' : 4})
sb_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0x41},{'GPR[0]': 0, 'GPR[10]': 0xDECB0333, 'PC' : 0},{'dataMem[0x41]': 0x33000000,   'PC' : 4})
sb_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xA341},{'GPR[0]': 0XFAD8067, 'GPR[10]': 0xFDA888, 'PC' : 0},{'dataMem[0xFAD23A8]': 0x88000000,   'PC' : 4})
sb_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xA341},{'GPR[0]': 0XFAD8067, 'GPR[10]': 0x1, 'PC' : 0},{'dataMem[0xFAD23A8]': 0x01000000,   'PC' : 4})
sb_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0x3341},{'GPR[0]': 0X7A120000, 'GPR[10]': 0x7A120098, 'PC' : 0},{'dataMem[0xFAD23A8]': 0x00000000,   'PC' : 4})


sc_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xA341},{'LLbit': 1, 'GPR[0]': 0XFAD8067, 'GPR[10]': 0x7A120098, 'PC' : 0},{'LLbit': 0, 'GPR[10]': 1,'dataMem[0xFAD23A8]': 0x7A120098,   'PC' : 4})
sc_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xA341},{'LLbit': 1, 'GPR[0]': 0XB97F, 'GPR[10]': 0xFFFFFFFF, 'PC' : 0},{'LLbit': 0, 'GPR[10]': 1,'dataMem[0x5CC0]': 0xFFFFFFFF,   'PC' : 4})
sc_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xA341},{'LLbit': 1, 'GPR[0]': 0X5CBF, 'GPR[10]': 0xFFFFFFFF, 'PC' : 0},{'LLbit': 0, 'GPR[10]': 1,'dataMem[0x0]': 0xFFFFFFFF,   'PC' : 4})
sc_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0x7341},{'LLbit': 1, 'GPR[0]': 0X13, 'GPR[10]': 0xDD68, 'PC' : 4400000},{'LLbit': 0, 'GPR[10]': 1,'dataMem[0x7354]': 0xDD68,   'PC' : 4400004})
sc_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xA341},{'LLbit': 1, 'GPR[0]': 0XB97E, 'GPR[10]': 0xFFFFFFFF, 'PC' : 0},{'LLbit': 0, 'GPR[10]': 0xFFFFFFFF,'dataMem[0x5CBF]': 0,   'PC' : 4})
sc_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xA341},{'LLbit': 1, 'GPR[0]': 0X5CC0, 'GPR[10]': 0xFFFFFFFF, 'PC' : 0},{'LLbit': 0, 'GPR[10]': 0xFFFFFFFF,'dataMem[0x1]': 0,   'PC' : 4})
sc_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0x7341},{'LLbit': 1, 'GPR[0]': 0X0, 'GPR[10]': 0xDD68, 'PC' : 4400000},{'LLbit': 0, 'GPR[10]': 0xDD68,'dataMem[0x7341]': 0,   'PC' : 4400004})
sc_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xA341},{'LLbit': 0, 'GPR[0]': 0XFAD8067, 'GPR[10]': 0x7A120098, 'PC' : 0},{'LLbit': 0, 'GPR[10]': 0,'dataMem[0xFAD23A8]': 0,   'PC' : 4})
sc_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xA341},{'LLbit': 0, 'GPR[0]': 0XB97F, 'GPR[10]': 0xFFFFFFFF, 'PC' : 0},{'LLbit': 0, 'GPR[10]': 0,'dataMem[0x5CC0]': 0,   'PC' : 4})
sc_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0x7341},{'LLbit': 0, 'GPR[0]': 0XB97F, 'GPR[10]': 0x07, 'PC' : 4400000},{'LLbit': 0, 'GPR[10]': 0,'dataMem[0x12CC0]': 0,   'PC' : 4400004})
sc_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xA341},{'LLbit': 0, 'GPR[0]': 0X0, 'GPR[10]': 0xFFFFFFFF, 'PC' : 0},{'LLbit': 0, 'GPR[10]': 0xFFFFFFFF,'dataMem[0x341]': 0,   'PC' : 4})
sc_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0x7341},{'LLbit': 0, 'GPR[0]': 0X0, 'GPR[10]': 0x07, 'PC' : 4400000},{'LLbit': 0, 'GPR[10]': 0x07,'dataMem[0x7341]': 0,   'PC' : 4400004})


sh_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0x7340},{'GPR[0]': 0X0, 'GPR[10]': 0x07, 'PC' : 4},{'dataMem[0x7340]': 0x00070000,   'PC' : 8})
sh_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0x40},{'GPR[0]': 0XFAD778, 'GPR[10]': 0x8BD7, 'PC' : 4},{'dataMem[0XFAD7B8]': 0x8BD70000,   'PC' : 8})
sh_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xA341},{'GPR[0]': 0XB97F, 'GPR[10]': 0x77AA8371, 'PC' : 4},{'dataMem[0x5CC0]': 0x83710000,   'PC' : 8})
sh_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 16, 'GPR[10]': 0xFFFF0000, 'PC' : 4},{'dataMem[0x0]': 0x0,   'PC' : 8})
sh_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 0x10, 'GPR[10]': 0xFFFF1000, 'PC' : 4},{'dataMem[0x0]': 0x10000000,   'PC' : 8})
sh_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 18, 'GPR[10]': 0xFFFF0080, 'PC' : 4},{'dataMem[0x0]': 0x80,   'PC' : 8})
sh_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 19, 'GPR[10]': 0xFFFF0080, 'PC' : 4},{'dataMem[0x0]': 0x0,   'PC' : 8})
sh_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 0x11, 'GPR[10]': 0xFFFF1000, 'PC' : 4},{'dataMem[0x0]': 0x0,   'PC' : 8})
sh_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 0, 'GPR[10]': 0xFFFF1070, 'PC' : 4},{'dataMem[0x0]': 0x0,   'PC' : 8})
sh_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFFF},{'GPR[0]': 0, 'GPR[10]': 0xFFFF1005, 'PC' : 4},{'dataMem[0x0]': 0x0,   'PC' : 8})


sw_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0x7340},{'GPR[0]': 0X0, 'GPR[10]': 0x07, 'PC' : 4},{'dataMem[0x7340]': 0x7,   'PC' : 8})
sw_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0x40},{'GPR[0]': 0XFAD778, 'GPR[10]': 0x8BD7, 'PC' : 4},{'dataMem[0XFAD7B8]': 0x8BD7,   'PC' : 8})
sw_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xA341},{'GPR[0]': 0XB97F, 'GPR[10]': 0x77AA8371, 'PC' : 4},{'dataMem[0x5CC0]': 0x77AA8371,   'PC' : 8})
sw_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 16, 'GPR[10]': 0xFFFF0000, 'PC' : 4},{'dataMem[0x0]': 0xFFFF0000,   'PC' : 8})
sw_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 0x10, 'GPR[10]': 0xFFFF1000, 'PC' : 4},{'dataMem[0x0]': 0xFFFF1000,   'PC' : 8})
sw_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 18, 'GPR[10]': 0xFFFF0080, 'PC' : 4},{'dataMem[0x0]': 0x0,   'PC' : 8})
sw_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 19, 'GPR[10]': 0xFFFF0080, 'PC' : 4},{'dataMem[0x0]': 0x0,   'PC' : 8})
sw_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 0x11, 'GPR[10]': 0xFFFF1000, 'PC' : 4},{'dataMem[0x0]': 0x0,   'PC' : 8})
sw_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 0, 'GPR[10]': 0xFFFF1070, 'PC' : 4},{'dataMem[0x0]': 0x0,   'PC' : 8})
sw_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFFF},{'GPR[0]': 0, 'GPR[10]': 0xFFFF1005, 'PC' : 4},{'dataMem[0x0]': 0x0,   'PC' : 8})


swl_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 16, 'GPR[10]': 0x44440000,'dataMem[0x0]': 0xFFFFFFFF,  'PC' : 4},{'dataMem[0x0]': 0x44440000,   'PC' : 8})
swl_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 17, 'GPR[10]': 0x44440000,'dataMem[0x0]': 0xFFFFFFFF,  'PC' : 4},{'dataMem[0x0]': 0xFF444400,   'PC' : 8})
swl_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 18, 'GPR[10]': 0x44440000,'dataMem[0x0]': 0xFFFFFFFF,  'PC' : 4},{'dataMem[0x0]': 0xFFFF4444,   'PC' : 8})
swl_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 19, 'GPR[10]': 0x44440000,'dataMem[0x0]': 0xFFFFFFFF,  'PC' : 4},{'dataMem[0x0]': 0xFFFFFF44,   'PC' : 8})
swl_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 10, 'GPR[10]': 0x44440000,'dataMem[0x0]': 0xFFFFFFFF,  'PC' : 4},{'dataMem[0x0]': 0xFFFFFFFF,   'PC' : 8})


swr_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 16, 'GPR[10]': 0x789ABCDE,'dataMem[0x0]': 0xFFFFFFFF,  'PC' : 4},{'dataMem[0x0]': 0xDEFFFFFF,   'PC' : 8})
swr_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 17, 'GPR[10]': 0x789ABCDE,'dataMem[0x0]': 0xFFFFFFFF,  'PC' : 4},{'dataMem[0x0]': 0xBCDEFFFF,   'PC' : 8})
swr_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 18, 'GPR[10]': 0x789ABCDE,'dataMem[0x0]': 0xFFFFFFFF,  'PC' : 4},{'dataMem[0x0]': 0x9ABCDEFF,   'PC' : 8})
swr_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 19, 'GPR[10]': 0x789ABCDE,'dataMem[0x0]': 0xFFFFFFFF,  'PC' : 4},{'dataMem[0x0]': 0x789ABCDE,   'PC' : 8})
swr_imm_Instr.addTest({'rs': 0, 'rt': 10, 'immediate': 0xFFF0},{'GPR[0]': 10, 'GPR[10]': 0x789ABCDE,'dataMem[0x0]': 0xFFFFFFFF,  'PC' : 4},{'dataMem[0x0]': 0xFFFFFFFF,   'PC' : 8})



#
#SHIFT Instruction Family
#

sll_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0x1F, 'PC' : 0},{'GPR[0]' : 0x80000000, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0x1F, 'PC' : 4})
sll_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x0, 'PC' : 0},{'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x0, 'PC' : 4})
sll_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x12345678,   'GPR[11]' : 0x15, 'PC' : 0},{'GPR[0]' : 0xCF000000, 'GPR[10]' : 0x12345678,   'GPR[11]' : 0x15, 'PC' : 4})
sll_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x12345678,   'GPR[11]' : 4, 'PC' : 0},{'GPR[0]' : 0x23456780, 'GPR[10]' : 0x12345678,   'GPR[11]' : 4, 'PC' : 4})
sll_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 8, 'PC' : 0},{'GPR[0]' : 0xDCBA9800, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 8, 'PC' : 4})
sll_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 16, 'PC' : 0},{'GPR[0]' : 0xBA980000, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 16, 'PC' : 4})
sll_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 1, 'PC' : 0},{'GPR[0]' : 0xE9EBEDEE, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 1, 'PC' : 4})
sll_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 3, 'PC' : 0},{'GPR[0]' : 0xA7AFB7B8, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 3, 'PC' : 4})
sll_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 7, 'PC' : 0},{'GPR[0]' : 0x7AFB7B80, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 7, 'PC' : 4})
sll_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 13, 'PC' : 0},{'GPR[0]' : 0xBEDEE000, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 13, 'PC' : 4})
sll_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 27, 'PC' : 0},{'GPR[0]' : 0xB8000000, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 27, 'PC' : 4})
sll_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 31, 'PC' : 0},{'GPR[0]' : 0x80000000, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 31, 'PC' : 4})
sll_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F8,   'GPR[11]' : 31, 'PC' : 0},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F8,   'GPR[11]' : 31, 'PC' : 4})


sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 0},{'GPR[0]' : 0x80000000, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 4})
sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x00000000, 'PC' : 0},{'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x00000000, 'PC' : 4})
sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x12345678,   'GPR[11]' : 0x55555555, 'PC' : 0},{'GPR[0]' : 0xCF000000, 'GPR[10]' : 0x12345678,   'GPR[11]' : 0x55555555, 'PC' : 4})
sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x12345678,   'GPR[11]' : 4, 'PC' : 0},{'GPR[0]' : 0x23456780, 'GPR[10]' : 0x12345678,   'GPR[11]' : 4, 'PC' : 4})
sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 8, 'PC' : 0},{'GPR[0]' : 0xDCBA9800, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 8, 'PC' : 4})
sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 16, 'PC' : 0},{'GPR[0]' : 0xBA980000, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 16, 'PC' : 4})
sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 1, 'PC' : 0},{'GPR[0]' : 0xE9EBEDEE, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 1, 'PC' : 4})
sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 3, 'PC' : 0},{'GPR[0]' : 0xA7AFB7B8, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 3, 'PC' : 4})
sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 7, 'PC' : 0},{'GPR[0]' : 0x7AFB7B80, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 7, 'PC' : 4})
sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 13, 'PC' : 0},{'GPR[0]' : 0xBEDEE000, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 13, 'PC' : 4})
sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 27, 'PC' : 0},{'GPR[0]' : 0xB8000000, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 27, 'PC' : 4})
sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 31, 'PC' : 0},{'GPR[0]' : 0x80000000, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 31, 'PC' : 4})
sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F8,   'GPR[11]' : 31, 'PC' : 0},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F8,   'GPR[11]' : 31, 'PC' : 4})
sllv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 32, 'PC' : 0},{'GPR[0]' : 0xF4F5F6F7, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 32, 'PC' : 4})


sra_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 25, 'PC' : 0},{'GPR[0]' : 0xFFFFFFFA, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 25, 'PC' : 4})
sra_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 14, 'PC' : 0},{'GPR[0]' : 0xFFFFD3D7, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 14, 'PC' : 4})
sra_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 4, 'PC' : 0},{'GPR[0]' : 0xFF4F5F6F, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 4, 'PC' : 4})
sra_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 0, 'PC' : 0},{'GPR[0]' : 0xF4F5F6F7, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 0, 'PC' : 4})
sra_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 25, 'PC' : 0},{'GPR[0]' : 0x3A, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 25, 'PC' : 4})
sra_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 14, 'PC' : 0},{'GPR[0]' : 0x1D3D7, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 14, 'PC' : 4})
sra_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 4, 'PC' : 0},{'GPR[0]' : 0x74F5F6F, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 4, 'PC' : 4})
sra_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 0, 'PC' : 0},{'GPR[0]' : 0x74F5F6F7, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 0, 'PC' : 4})
sra_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : -1697587,   'GPR[11]' : 17, 'PC' : 0},{'GPR[0]' : 0xFFFFFFF3, 'GPR[10]' : -1697587,   'GPR[11]' : 17, 'PC' : 4})


srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 25, 'PC' : 0},{'GPR[0]' : 0xFFFFFFFA, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 25, 'PC' : 4})
srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 14, 'PC' : 0},{'GPR[0]' : 0xFFFFD3D7, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 14, 'PC' : 4})
srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 4, 'PC' : 0},{'GPR[0]' : 0xFF4F5F6F, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 4, 'PC' : 4})
srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 0, 'PC' : 0},{'GPR[0]' : 0xF4F5F6F7, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 0, 'PC' : 4})
srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 25, 'PC' : 0},{'GPR[0]' : 0x3A, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 25, 'PC' : 4})
srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 14, 'PC' : 0},{'GPR[0]' : 0x1D3D7, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 14, 'PC' : 4})
srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 4, 'PC' : 0},{'GPR[0]' : 0x74F5F6F, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 4, 'PC' : 4})
srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 0, 'PC' : 0},{'GPR[0]' : 0x74F5F6F7, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 0, 'PC' : 4})
srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : -1697587,   'GPR[11]' : 17, 'PC' : 0},{'GPR[0]' : 0xFFFFFFF3, 'GPR[10]' : -1697587,   'GPR[11]' : 17, 'PC' : 4})
srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 0xFFFFFFEE, 'PC' : 0},{'GPR[0]' : 0xFFFFD3D7, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 0xFFFFFFEE, 'PC' : 4})
srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 0x61357304, 'PC' : 0},{'GPR[0]' : 0xFF4F5F6F, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 0x61357304, 'PC' : 4})
srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 0x925FEDF9, 'PC' : 0},{'GPR[0]' : 0x3A, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 0x925FEDF9, 'PC' : 4})
srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 0x183746E0, 'PC' : 0},{'GPR[0]' : 0x74F5F6F7, 'GPR[10]' : 0x74F5F6F7,   'GPR[11]' : 0x183746E0, 'PC' : 4})
srav_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : -1697587,   'GPR[11]' : 0x82FDABF1, 'PC' : 0},{'GPR[0]' : 0xFFFFFFF3, 'GPR[10]' : -1697587,   'GPR[11]' : 0x82FDABF1, 'PC' : 4})


srl_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0x1F, 'PC' : 0},{'GPR[0]' : 0x1, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0x1F, 'PC' : 4})
srl_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x0, 'PC' : 0},{'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x0, 'PC' : 4})
srl_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x12345678,   'GPR[11]' : 0x15, 'PC' : 0},{'GPR[0]' : 0x91, 'GPR[10]' : 0x12345678,   'GPR[11]' : 0x15, 'PC' : 4})
srl_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x12345678,   'GPR[11]' : 4, 'PC' : 0},{'GPR[0]' : 0x1234567, 'GPR[10]' : 0x12345678,   'GPR[11]' : 4, 'PC' : 4})
srl_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 8, 'PC' : 0},{'GPR[0]' : 0xFEDCBA, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 8, 'PC' : 4})
srl_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 16, 'PC' : 0},{'GPR[0]' : 0xFEDC, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 16, 'PC' : 4})
srl_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 1, 'PC' : 0},{'GPR[0]' : 0x7A7AFB7B, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 1, 'PC' : 4})
srl_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 3, 'PC' : 0},{'GPR[0]' : 0x1E9EBEDE, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 3, 'PC' : 4})
srl_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 7, 'PC' : 0},{'GPR[0]' : 0x1E9EBED, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 7, 'PC' : 4})
srl_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 13, 'PC' : 0},{'GPR[0]' : 0x7A7AF, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 13, 'PC' : 4})
srl_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 27, 'PC' : 0},{'GPR[0]' : 0x1E, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 27, 'PC' : 4})
srl_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 31, 'PC' : 0},{'GPR[0]' : 0x1, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 31, 'PC' : 4})
srl_reg_Instr.addTest({'rd': 0, 'rt': 10, 'sa': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x74F5F6F8,   'GPR[11]' : 31, 'PC' : 0},{'GPR[0]' : 0, 'GPR[10]' : 0x74F5F6F8,   'GPR[11]' : 31, 'PC' : 4})


srlv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 0},{'GPR[0]' : 0x1, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 4})
srlv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x00000000, 'PC' : 0},{'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x00000000, 'PC' : 4})
srlv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x12345678,   'GPR[11]' : 0x55555555, 'PC' : 0},{'GPR[0]' : 0x91, 'GPR[10]' : 0x12345678,   'GPR[11]' : 0x55555555, 'PC' : 4})
srlv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0x12345678,   'GPR[11]' : 0x262425E4, 'PC' : 0},{'GPR[0]' : 0x1234567, 'GPR[10]' : 0x12345678,   'GPR[11]' : 0x262425E4, 'PC' : 4})
srlv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 8, 'PC' : 0},{'GPR[0]' : 0xFEDCBA, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 8, 'PC' : 4})
srlv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 0xFFFFFFF0, 'PC' : 0},{'GPR[0]' : 0xFEDC, 'GPR[10]' : 0xFEDCBA98,   'GPR[11]' : 0xFFFFFFF0, 'PC' : 4})
srlv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 0x840D, 'PC' : 0},{'GPR[0]' : 0x7A7AF, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 0x840D, 'PC' : 4})
srlv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 0xD9, 'PC' : 0},{'GPR[0]' : 0x7A, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 0xD9, 'PC' : 4})
srlv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F8,   'GPR[11]' : 0x327FF, 'PC' : 0},{'GPR[0]' : 0x1, 'GPR[10]' : 0xF4F5F6F8,   'GPR[11]' : 0x327FF, 'PC' : 4})
srlv_reg_Instr.addTest({'rd': 0, 'rt': 10, 'rs': 11},{'GPR[0]' : 0, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 32, 'PC' : 0},{'GPR[0]' : 0xF4F5F6F7, 'GPR[10]' : 0xF4F5F6F7,   'GPR[11]' : 32, 'PC' : 4})



#
#SET Instruction Family
#

slt_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : -4567,   'GPR[11]' : 41, 'PC' : 0}, {'GPR[0]' : 1, 'GPR[10]' : -4567,   'GPR[11]' : 41, 'PC' : 4})
slt_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : -2147483647,   'GPR[11]' : 2147483647, 'PC' : 0}, {'GPR[0]' : 1, 'GPR[10]' : -2147483647,   'GPR[11]' : 2147483647, 'PC' : 4})
slt_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 1234567,   'GPR[11]' : 1234568, 'PC' : 0}, {'GPR[0]' : 1, 'GPR[10]' : 1234567,   'GPR[11]' : 1234568, 'PC' : 4})
slt_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : -2147483647,   'GPR[11]' : -2147483646, 'PC' : 0}, {'GPR[0]' : 1, 'GPR[10]' : -2147483647,   'GPR[11]' : -2147483646, 'PC' : 4})
slt_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 2147483647,   'GPR[11]' : -2147483646, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 2147483647,   'GPR[11]' : -2147483646, 'PC' : 4})
slt_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xFEC4823,   'GPR[11]' : 173426, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 0xFEC4823,   'GPR[11]' : 173426, 'PC' : 4})
slt_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0,   'GPR[11]' : 0, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 0,   'GPR[11]' : 0, 'PC' : 4})
slt_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 98624251,   'GPR[11]' : 8145173, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 98624251,   'GPR[11]' : 8145173, 'PC' : 4})


slti_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 41}, {'GPR[0]' : 0, 'GPR[10]' : -4567, 'PC' : 0}, {'GPR[0]' : 1, 'GPR[10]' : -4567, 'PC' : 4})
slti_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0xD688}, {'GPR[0]' : 0, 'GPR[10]' : 1234567, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 1234567, 'PC' : 4})
slti_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': -32767}, {'GPR[0]' : 0, 'GPR[10]' : -32766, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : -32766, 'PC' : 4})
slti_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': -32767}, {'GPR[0]' : 0, 'GPR[10]' : 2147483647, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 2147483647, 'PC' : 4})
slti_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 13426}, {'GPR[0]' : 0, 'GPR[10]' : 0xFEC4823, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 0xFEC4823, 'PC' : 4})
slti_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0}, {'GPR[0]' : 0, 'GPR[10]' : 0, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 0, 'PC' : 4})
slti_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 32767}, {'GPR[0]' : 0, 'GPR[10]' : -98624251, 'PC' : 0}, {'GPR[0]' : 1, 'GPR[10]' : -98624251, 'PC' : 4})


sltiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0}, {'GPR[0]' : 0, 'GPR[10]' : 0, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 0, 'PC' : 4})
sltiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': -15}, {'GPR[0]' : 0, 'GPR[10]' : -14, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : -14, 'PC' : 4})
sltiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 65535}, {'GPR[0]' : 0, 'GPR[10]' : 5987, 'PC' : 0}, {'GPR[0]' : 1, 'GPR[10]' : 5987, 'PC' : 4})
sltiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0xFFFF}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFFE, 'PC' : 0}, {'GPR[0]' : 1, 'GPR[10]' : 0xFFFE, 'PC' : 4})
sltiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0xFFFF}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFFFE, 'PC' : 0}, {'GPR[0]' : 1, 'GPR[10]' : 0xFFFFE, 'PC' : 4})
sltiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0x135}, {'GPR[0]' : 0, 'GPR[10]' : 0xF01579, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 0xF01579, 'PC' : 4})
sltiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0xF007}, {'GPR[0]' : 0, 'GPR[10]' : 0xEEE, 'PC' : 0}, {'GPR[0]' : 1, 'GPR[10]' : 0xEEE, 'PC' : 4})
sltiu_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 0xF007}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFEEE, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFEEE, 'PC' : 4})


sltu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0,   'GPR[11]' : 0, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 0,   'GPR[11]' : 0, 'PC' : 4})
sltu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : -123456,   'GPR[11]' : -123457, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : -123456,   'GPR[11]' : -123457, 'PC' : 4})
sltu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFFF8,   'GPR[11]' : 0xFFFFFFF9, 'PC' : 0}, {'GPR[0]' : 1, 'GPR[10]' : 0xFFFFFFF8,   'GPR[11]' : 0xFFFFFFF9, 'PC' : 4})
sltu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFFF8,   'GPR[11]' : 0xFFF9, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFFF8,   'GPR[11]' : 0xFFF9, 'PC' : 4})
sltu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFBADFF8,   'GPR[11]' : 0xFFCAD1F9, 'PC' : 0}, {'GPR[0]' : 1, 'GPR[10]' : 0xFFBADFF8,   'GPR[11]' : 0xFFCAD1F9, 'PC' : 4})



#
#SUB Instruction Family
#

sub_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : 0x44444444,   'GPR[11]' : 0x14444444, 'PC' : 0}, {'GPR[0]' : 0x30000000, 'GPR[10]' : 0x44444444,   'GPR[11]' : 0x14444444, 'PC' : 0x4})
sub_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : 49283751,   'GPR[11]' : 49283751, 'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 49283751,   'GPR[11]' : 49283751, 'PC' : 0x4})
sub_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : 49283751,   'GPR[11]' : -49283751, 'PC' : 0}, {'GPR[0]' : 0x5E0054E, 'GPR[10]' : 49283751,   'GPR[11]' : -49283751, 'PC' : 0x4})
sub_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : 49283751,   'GPR[11]' : -492837, 'PC' : 0}, {'GPR[0]' : 0x2F787CC, 'GPR[10]' : 49283751,   'GPR[11]' : -492837, 'PC' : 0x4})
sub_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : -49283751,   'GPR[11]' : -492837, 'PC' : 0}, {'GPR[0]' : 0xFD17827E, 'GPR[10]' : -49283751,   'GPR[11]' : -492837, 'PC' : 0x4})
sub_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : -1000000,   'GPR[11]' : -4000, 'PC' : 0}, {'GPR[0]' : -996000, 'GPR[10]' : -1000000,   'GPR[11]' : -4000, 'PC' : 0x4})
sub_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : -1000000,   'GPR[11]' : 4000, 'PC' : 0}, {'GPR[0]' : -1004000, 'GPR[10]' : -1000000,   'GPR[11]' : 4000, 'PC' : 0x4})
sub_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : 2147483647,   'GPR[11]' : -2147483647, 'PC' : 0}, {'GPR[0]' : 0xF, 'GPR[10]' : 2147483647,   'GPR[11]' : -2147483647, 'PC' : 0x4})
sub_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : 2147483647,   'GPR[11]' : 2147483647, 'PC' : 0}, {'GPR[0]' : 0x0, 'GPR[10]' : 2147483647,   'GPR[11]' : 2147483647, 'PC' : 0x4})
sub_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : -2147483647,   'GPR[11]' : -2147483647, 'PC' : 0}, {'GPR[0]' : 0x0, 'GPR[10]' : -2147483647,   'GPR[11]' : -2147483647, 'PC' : 0x4})
sub_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : -2147483647,   'GPR[11]' : 2147483647, 'PC' : 0}, {'GPR[0]' : 0xF, 'GPR[10]' : -2147483647,   'GPR[11]' : 2147483647, 'PC' : 0x4})


subu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : 0x44444444,   'GPR[11]' : 0x14444444, 'PC' : 0}, {'GPR[0]' : 0x30000000, 'GPR[10]' : 0x44444444,   'GPR[11]' : 0x14444444, 'PC' : 0x4})
subu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : 49283751,   'GPR[11]' : 49283751, 'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 49283751,   'GPR[11]' : 49283751, 'PC' : 0x4})
subu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : 49283751,   'GPR[11]' : -49283751, 'PC' : 0}, {'GPR[0]' : 0x5E0054E, 'GPR[10]' : 49283751,   'GPR[11]' : -49283751, 'PC' : 0x4})
subu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : 49283751,   'GPR[11]' : -492837, 'PC' : 0}, {'GPR[0]' : 0x2F787CC, 'GPR[10]' : 49283751,   'GPR[11]' : -492837, 'PC' : 0x4})
subu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : -49283751,   'GPR[11]' : -492837, 'PC' : 0}, {'GPR[0]' : 0xFD17827E, 'GPR[10]' : -49283751,   'GPR[11]' : -492837, 'PC' : 0x4})
subu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : -1000000,   'GPR[11]' : -4000, 'PC' : 0}, {'GPR[0]' : -996000, 'GPR[10]' : -1000000,   'GPR[11]' : -4000, 'PC' : 0x4})
subu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : -1000000,   'GPR[11]' : 4000, 'PC' : 0}, {'GPR[0]' : -1004000, 'GPR[10]' : -1000000,   'GPR[11]' : 4000, 'PC' : 0x4})
subu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : 2147483647,   'GPR[11]' : -2147483647, 'PC' : 0}, {'GPR[0]' : 0xFFFFFFFE, 'GPR[10]' : 2147483647,   'GPR[11]' : -2147483647, 'PC' : 0x4})
subu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : 2147483647,   'GPR[11]' : 2147483647, 'PC' : 0}, {'GPR[0]' : 0x0, 'GPR[10]' : 2147483647,   'GPR[11]' : 2147483647, 'PC' : 0x4})
subu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : -2147483647,   'GPR[11]' : -2147483647, 'PC' : 0}, {'GPR[0]' : 0x0, 'GPR[10]' : -2147483647,   'GPR[11]' : -2147483647, 'PC' : 0x4})
subu_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0xF, 'GPR[10]' : -2147483647,   'GPR[11]' : 2147483647, 'PC' : 0}, {'GPR[0]' : 0x2, 'GPR[10]' : -2147483647,   'GPR[11]' : 2147483647, 'PC' : 0x4})



#
#System Call
#

syscall_reg_Instr.addTest({},{'PC' : 0},{'PC' : 4})



#
#TRAP Instruction Family
#

teq_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA, 'GPR[12]': 0xA, 'PC' : 0},{'PC' : 4})#
teq_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA98DDF12, 'GPR[12]': 0x298DDF12, 'PC' : 0},{'PC' : 4})
teq_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA98DDF12, 'GPR[12]': 0xA98DDF12, 'PC' : 0},{'PC' : 4})#
teq_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -1234, 'GPR[12]': -1234, 'PC' : 0},{'PC' : 4})#
teq_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -92835578, 'GPR[12]': -92835578, 'PC' : 0},{'PC' : 4})#
teq_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -92835578, 'GPR[12]': 92835578, 'PC' : 0},{'PC' : 4})
teq_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0, 'GPR[12]': 0, 'PC' : 0},{'PC' : 4})#


teqi_reg_Instr.addTest({'rs': 0, 'immediate': 0xA},{'GPR[0]': 0xA, 'PC' : 0},{'PC' : 4})#
teqi_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xDF12, 'PC' : 0},{'PC' : 4})#
teqi_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xA98DDF12, 'PC' : 0},{'PC' : 4})
teqi_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xFFFFDF12, 'PC' : 0},{'PC' : 4})
teqi_reg_Instr.addTest({'rs': 0, 'immediate': -1234},{'GPR[0]': -1234, 'PC' : 0},{'PC' : 4})#
teqi_reg_Instr.addTest({'rs': 0, 'immediate': -3834},{'GPR[0]': -3834, 'PC' : 0},{'PC' : 4})#
teqi_reg_Instr.addTest({'rs': 0, 'immediate': 32506},{'GPR[0]': 92831482, 'PC' : 0},{'PC' : 4})
teqi_reg_Instr.addTest({'rs': 0, 'immediate': 32506},{'GPR[0]': 32506, 'PC' : 0},{'PC' : 4})#


tge_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA, 'GPR[12]': 0xA, 'PC' : 0},{'PC' : 4})#
tge_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA98DDF12, 'GPR[12]': 0x298DDF12, 'PC' : 0},{'PC' : 4})
tge_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA98DDF12, 'GPR[12]': 0xA38DDF12, 'PC' : 0},{'PC' : 4})#
tge_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -1234, 'GPR[12]': -1234, 'PC' : 0},{'PC' : 4})#
tge_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -92835578, 'GPR[12]': -99835578, 'PC' : 0},{'PC' : 4})#
tge_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -92835578, 'GPR[12]': 92835578, 'PC' : 0},{'PC' : 4})
tge_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0x5, 'GPR[12]': 0xFFFFFFFF, 'PC' : 0},{'PC' : 4})#


tgei_reg_Instr.addTest({'rs': 0, 'immediate': 0xA},{'GPR[0]': 0xA, 'PC' : 0},{'PC' : 4})#
tgei_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF11},{'GPR[0]': 0xDF12, 'PC' : 0},{'PC' : 4})#
tgei_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xA98DDF12, 'PC' : 0},{'PC' : 4})
tgei_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xFFFFDF12, 'PC' : 0},{'PC' : 4})#
tgei_reg_Instr.addTest({'rs': 0, 'immediate': -14},{'GPR[0]': -1234, 'PC' : 0},{'PC' : 4})
tgei_reg_Instr.addTest({'rs': 0, 'immediate': -3834},{'GPR[0]': -903834, 'PC' : 0},{'PC' : 4})
tgei_reg_Instr.addTest({'rs': 0, 'immediate': 32506},{'GPR[0]': 92831482, 'PC' : 0},{'PC' : 4})#
tgei_reg_Instr.addTest({'rs': 0, 'immediate': 32506},{'GPR[0]': 506, 'PC' : 0},{'PC' : 4})


tgeiu_reg_Instr.addTest({'rs': 0, 'immediate': 0xA},{'GPR[0]': 0xA, 'PC' : 0},{'PC' : 4})#
tgeiu_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF11},{'GPR[0]': 0xDF12, 'PC' : 0},{'PC' : 4})
tgeiu_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xA98DDF12, 'PC' : 0},{'PC' : 4})
tgeiu_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xFFFFDF12, 'PC' : 0},{'PC' : 4})#
tgeiu_reg_Instr.addTest({'rs': 0, 'immediate': -14},{'GPR[0]': -1234, 'PC' : 0},{'PC' : 4})
tgeiu_reg_Instr.addTest({'rs': 0, 'immediate': -3834},{'GPR[0]': -903834, 'PC' : 0},{'PC' : 4})
tgeiu_reg_Instr.addTest({'rs': 0, 'immediate': 32506},{'GPR[0]': 92831482, 'PC' : 0},{'PC' : 4})#
tgeiu_reg_Instr.addTest({'rs': 0, 'immediate': 32506},{'GPR[0]': 506, 'PC' : 0},{'PC' : 4})
tgeiu_reg_Instr.addTest({'rs': 0, 'immediate': -12334},{'GPR[0]': -1234, 'PC' : 0},{'PC' : 4})#


tgeu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA, 'GPR[12]': 0xA, 'PC' : 0},{'PC' : 4})#
tgeu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA98DDF12, 'GPR[12]': 0x298DDF12, 'PC' : 0},{'PC' : 4})#
tgeu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA98DDF12, 'GPR[12]': 0xA38DDF12, 'PC' : 0},{'PC' : 4})#
tgeu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -1234, 'GPR[12]': -1234, 'PC' : 0},{'PC' : 4})#
tgeu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -92835578, 'GPR[12]': -99835578, 'PC' : 0},{'PC' : 4})#
tgeu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -92835578, 'GPR[12]': 92835578, 'PC' : 0},{'PC' : 4})#
tgeu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0x5, 'GPR[12]': 0xFFFFFFFF, 'PC' : 0},{'PC' : 4})
tgeu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -1234, 'GPR[12]': -14, 'PC' : 0},{'PC' : 4})


tlt_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA, 'GPR[12]': 0xA, 'PC' : 0},{'PC' : 4})
tlt_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA98DDF12, 'GPR[12]': 0x298DDF12, 'PC' : 0},{'PC' : 4})#
tlt_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA98DDF12, 'GPR[12]': 0xA38DDF12, 'PC' : 0},{'PC' : 4})
tlt_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -1234, 'GPR[12]': -1234, 'PC' : 0},{'PC' : 4})
tlt_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -92835578, 'GPR[12]': -99835578, 'PC' : 0},{'PC' : 4})
tlt_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -92835578, 'GPR[12]': 92835578, 'PC' : 0},{'PC' : 4})#
tlt_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0x5, 'GPR[12]': 0xFFFFFFFF, 'PC' : 0},{'PC' : 4})


tlti_reg_Instr.addTest({'rs': 0, 'immediate': 0xA},{'GPR[0]': 0xA, 'PC' : 0},{'PC' : 4})
tlti_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF11},{'GPR[0]': 0xDF12, 'PC' : 0},{'PC' : 4})
tlti_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xA98DDF12, 'PC' : 0},{'PC' : 4})#
tlti_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xFFFFDF12, 'PC' : 0},{'PC' : 4})
tlti_reg_Instr.addTest({'rs': 0, 'immediate': -14},{'GPR[0]': -1234, 'PC' : 0},{'PC' : 4})#
tlti_reg_Instr.addTest({'rs': 0, 'immediate': -3834},{'GPR[0]': -903834, 'PC' : 0},{'PC' : 4})#
tlti_reg_Instr.addTest({'rs': 0, 'immediate': 32506},{'GPR[0]': 92831482, 'PC' : 0},{'PC' : 4})
tlti_reg_Instr.addTest({'rs': 0, 'immediate': 32506},{'GPR[0]': 506, 'PC' : 0},{'PC' : 4})#


tltiu_reg_Instr.addTest({'rs': 0, 'immediate': 0xA},{'GPR[0]': 0xA, 'PC' : 0},{'PC' : 4})
tltiu_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF11},{'GPR[0]': 0xDF12, 'PC' : 0},{'PC' : 4})#
tltiu_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xA98DDF12, 'PC' : 0},{'PC' : 4})#
tltiu_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xFFFFDF12, 'PC' : 0},{'PC' : 4})
tltiu_reg_Instr.addTest({'rs': 0, 'immediate': -14},{'GPR[0]': -1234, 'PC' : 0},{'PC' : 4})#
tltiu_reg_Instr.addTest({'rs': 0, 'immediate': -3834},{'GPR[0]': -903834, 'PC' : 0},{'PC' : 4})#
tltiu_reg_Instr.addTest({'rs': 0, 'immediate': 32506},{'GPR[0]': 92831482, 'PC' : 0},{'PC' : 4})
tltiu_reg_Instr.addTest({'rs': 0, 'immediate': 32506},{'GPR[0]': 506, 'PC' : 0},{'PC' : 4})#
tltiu_reg_Instr.addTest({'rs': 0, 'immediate': -12334},{'GPR[0]': -1234, 'PC' : 0},{'PC' : 4})


tltu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA, 'GPR[12]': 0xA, 'PC' : 0},{'PC' : 4})
tltu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA98DDF12, 'GPR[12]': 0x298DDF12, 'PC' : 0},{'PC' : 4})
tltu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA98DDF12, 'GPR[12]': 0xA38DDF12, 'PC' : 0},{'PC' : 4})
tltu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -1234, 'GPR[12]': -1234, 'PC' : 0},{'PC' : 4})
tltu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -92835578, 'GPR[12]': -99835578, 'PC' : 0},{'PC' : 4})
tltu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -92835578, 'GPR[12]': 92835578, 'PC' : 0},{'PC' : 4})
tltu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0x5, 'GPR[12]': 0xFFFFFFFF, 'PC' : 0},{'PC' : 4})#
tltu_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -1234, 'GPR[12]': -14, 'PC' : 0},{'PC' : 4})#


tne_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA, 'GPR[12]': 0xA, 'PC' : 0},{'PC' : 4})
tne_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA98DDF12, 'GPR[12]': 0x298DDF12, 'PC' : 0},{'PC' : 4})#
tne_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0xA98DDF12, 'GPR[12]': 0xA98DDF12, 'PC' : 0},{'PC' : 4})
tne_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -1234, 'GPR[12]': -1234, 'PC' : 0},{'PC' : 4})
tne_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -92835578, 'GPR[12]': -92835578, 'PC' : 0},{'PC' : 4})
tne_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': -92835578, 'GPR[12]': 92835578, 'PC' : 0},{'PC' : 4})#
tne_reg_Instr.addTest({'rs': 0, 'rt': 12},{'GPR[0]': 0, 'GPR[12]': 0, 'PC' : 0},{'PC' : 4})


tnei_reg_Instr.addTest({'rs': 0, 'immediate': 0xA},{'GPR[0]': 0xA, 'PC' : 0},{'PC' : 4})
tnei_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xDF12, 'PC' : 0},{'PC' : 4})
tnei_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xA98DDF12, 'PC' : 0},{'PC' : 4})#
tnei_reg_Instr.addTest({'rs': 0, 'immediate': 0xDF12},{'GPR[0]': 0xFFFFDF12, 'PC' : 0},{'PC' : 4})#
tnei_reg_Instr.addTest({'rs': 0, 'immediate': -1234},{'GPR[0]': -1234, 'PC' : 0},{'PC' : 4})
tnei_reg_Instr.addTest({'rs': 0, 'immediate': -3834},{'GPR[0]': -3834, 'PC' : 0},{'PC' : 4})
tnei_reg_Instr.addTest({'rs': 0, 'immediate': 32506},{'GPR[0]': 92831482, 'PC' : 0},{'PC' : 4})#
tnei_reg_Instr.addTest({'rs': 0, 'immediate': 32506},{'GPR[0]': 32506, 'PC' : 0},{'PC' : 4})







#
#XOR Instruction Family
#

xor_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0xFFFFFFFF,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 4})
xor_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x00000000, 'PC' : 0}, {'GPR[0]' : 0x00000000, 'GPR[10]' : 0x00000000,   'GPR[11]' : 0x00000000, 'PC' : 4})
xor_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x55555555, 'PC' : 0}, {'GPR[0]' : 0xFFFFFFFF, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x55555555, 'PC' : 4})
xor_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 0}, {'GPR[0]' : 0x55555555, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0xFFFFFFFF, 'PC' : 4})
xor_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x22222222, 'PC' : 0}, {'GPR[0]' : 0x88888888, 'GPR[10]' : 0xAAAAAAAA,   'GPR[11]' : 0x22222222, 'PC' : 4})
xor_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x12341234,   'GPR[11]' : 0x23412341, 'PC' : 0}, {'GPR[0]' : 0x31753175, 'GPR[10]' : 0x12341234,   'GPR[11]' : 0x23412341, 'PC' : 4})



#Unsigned quiere decir que tomo lo que está en los registros y considero que ese es el número, por eso, cuando pongo números enteros negativos, se considera que lo que está en el registro es su complemento, pero no mostrando que es un valor negativo sino mostrando un numero natural.

#Si a lo que se referían con unsigned no era esto, cada vez que veo un operando que tenga el primer bit en uno (operando negativo), le debería sacar el complemento primero, antes de hacer cualquier operación, esto haría que tomase los operando unsigned como el número que yo pongo, sin el signo, tomando en cuenta esta consideración desde antes que se ponga en el registro ya complementado.








