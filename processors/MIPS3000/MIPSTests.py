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

add_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x44444444,   'GPR[11]' : 0x44444444, 'PC' : 0}, {'GPR[0]' : 0x88888888, 'GPR[10]' : 0x44444444,   'GPR[11]' : 0x44444444, 'PC' : 0x4})
add_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x44444441,   'GPR[11]' : 0x44444444, 'PC' : 0}, {'GPR[0]' : 0x88888885, 'GPR[10]' : 0x44444441,   'GPR[11]' : 0x44444444, 'PC' : 0x4})
add_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 0x88888888,   'GPR[11]' : 0x99999999, 'PC' : 0}, {'GPR[0]' : 0x33333333, 'GPR[10]' : 0x88888888,   'GPR[11]' : 0x99999999, 'PC' : 0x4})
add_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : -5,   'GPR[11]' : 4, 'PC' : 0}, {'GPR[0]' : -1, 'GPR[10]' : -5,   'GPR[11]' : 4, 'PC' : 4})
add_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : 4,   'GPR[11]' : -5, 'PC' : 0}, {'GPR[0]' : -1, 'GPR[10]' : 4,   'GPR[11]' : -5, 'PC' : 4})
add_reg_Instr.addTest({'rd': 0, 'rs': 10, 'rt': 11}, {'GPR[0]' : 0, 'GPR[10]' : -4,   'GPR[11]' : 4, 'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : -4,   'GPR[11]' : 4, 'PC' : 4})


addi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': 7}, {'GPR[0]' : 0, 'GPR[10]' : 4,   'PC' : 0}, {'GPR[0]' : 11, 'GPR[10]' : 4,   'PC' : 4})
addi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': -7}, {'GPR[0]' : 0, 'GPR[10]' : 4,   'PC' : 0}, {'GPR[0]' : -3, 'GPR[10]' : 4,   'PC' : 4})
addi_imm_Instr.addTest({'rt': 0, 'rs': 10, 'immediate': -5}, {'GPR[0]' : 0, 'GPR[10]' : 5,   'PC' : 0}, {'GPR[0]' : 0, 'GPR[10]' : 5,   'PC' : 4})
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
#MULTIPLY Instruction Family
#

madd_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 0},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 4})
madd_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 1,  'PC' : 0},{'HI': 1000,   'LO': 1467,   'GPR[0]': 467,   'GPR[10]': 1,  'PC' : 4})
madd_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 65535,   'GPR[0]': 65535,   'GPR[10]': 2,  'PC' : 0},{'HI': 1000,   'LO': 196605,   'GPR[0]': 65535,   'GPR[10]': 2,  'PC' : 4})
madd_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 65535,   'GPR[0]': 65535,   'GPR[10]': -2,  'PC' : 0},{'HI': 0x3E7,   'LO': 0xFFFF0001,   'GPR[0]': 65535,   'GPR[10]': -2,  'PC' : 4})
madd_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 0xFFF,   'LO': 0xFFFFFFFF,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 0},{'HI': 0x1000,  'LO': 0,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 4})
madd_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 0xEFFF,   'LO': 0xFFFFFFFF,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 0},{'HI': 0xF000,   'LO': 0,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 4})


maddu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 0},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 0,  'PC' : 4})
maddu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 1000,   'GPR[0]': 467,   'GPR[10]': 1,  'PC' : 0},{'HI': 1000,   'LO': 1467,   'GPR[0]': 467,   'GPR[10]': 1,  'PC' : 4})
maddu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 65535,   'GPR[0]': 65535,   'GPR[10]': 2,  'PC' : 0},{'HI': 1000,   'LO': 196605,   'GPR[0]': 65535,   'GPR[10]': 2,  'PC' : 4})
maddu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 1000,   'LO': 65535,   'GPR[0]': 65535,   'GPR[10]': -2,  'PC' : 0},{'HI': 0x103E6,   'LO':0xFFFE0002,   'GPR[0]': 65535,   'GPR[10]': -2,  'PC' : 4})
maddu_reg_Instr.addTest({'rs': 0, 'rt': 10},{'HI': 0x1,   'LO': 0xFFFFFFFE,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 0},{'HI': 0xFFFFFFFF,   'LO': 0xFFFFFFFF,   'GPR[0]': 0xFFFFFFFF,   'GPR[10]': 0xFFFFFFFF,  'PC' : 4})

