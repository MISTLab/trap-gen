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



from LEON3Isa import *


#ldsb_imm_Instr.addTest({}, {}, {})

#ldsb_reg_Instr.addTest({}, {}, {})

#ldsh_imm_Instr.addTest({}, {}, {})

#ldsh_reg_Instr.addTest({}, {}, {})

#ldub_imm_Instr.addTest({}, {}, {})

#ldub_reg_Instr.addTest({}, {}, {})

#lduh_imm_Instr.addTest({}, {}, {})

#lduh_reg_Instr.addTest({}, {}, {})

#ld_imm_Instr.addTest({}, {}, {})

#ld_reg_Instr.addTest({}, {}, {})

#ldd_imm_Instr.addTest({}, {}, {})

#ldd_reg_Instr.addTest({}, {}, {})

#ldsba_reg_Instr.addTest({}, {}, {})

#ldsha_reg_Instr.addTest({}, {}, {})

#lduba_reg_Instr.addTest({}, {}, {})

#lduha_reg_Instr.addTest({}, {}, {})

#lda_reg_Instr.addTest({}, {}, {})

#ldda_reg_Instr.addTest({}, {}, {})

# Store integer instructions
#stb_imm_Instr.addTest({}, {}, {})

#stb_reg_Instr.addTest({}, {}, {})

#sth_imm_Instr.addTest({}, {}, {})

#sth_reg_Instr.addTest({}, {}, {})

#st_imm_Instr.addTest({}, {}, {})

#st_reg_Instr.addTest({}, {}, {})

#std_imm_Instr.addTest({}, {}, {})

#std_reg_Instr.addTest({}, {}, {})

#stba_reg_Instr.addTest({}, {}, {})

#stha_reg_Instr.addTest({}, {}, {})

#sta_reg_Instr.addTest({}, {}, {})

#stda_reg_Instr.addTest({}, {}, {})

# Atomic Load/Store
#ldstub_imm_Instr.addTest({}, {}, {})

#ldstub_reg_Instr.addTest({}, {}, {})

#ldstuba_reg_Instr.addTest({}, {}, {})

# Swap
#swap_imm_Instr.addTest({}, {}, {})

#swap_reg_Instr.addTest({}, {}, {})

#swapa_reg_Instr.addTest({}, {}, {})

# sethi
sethi_Instr.addTest({'rd': 0, 'imm22': 0xfff}, {'PC' : 0x0, 'NPC' : 0x4}, {'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8})
sethi_Instr.addTest({'rd': 1, 'imm22': 0xfff}, {'REGS[1]' : 0xaaaaaaaa, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[1]' : 0x003ffc00, 'PC' : 0x8, 'NPC' : 0x8})
sethi_Instr.addTest({'rd': 20, 'imm22': 0x3fffff}, {'REGS[20]' : 0xaaaaaaaa, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[20]' : 0xfffffc00, 'PC' : 0x8, 'NPC' : 0x8})

# Logical Instructions
and_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[10]' : 0xffffffff, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8})
and_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[1]' : 0x0fff, 'PC' : 0x8, 'NPC' : 0x8})
and_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8})
and_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[10]' : 0x0888, 'PC' : 0x8, 'NPC' : 0x8})

and_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[10]' : 0xffffffff, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8})
and_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[1]' : 0x0fff, 'PC' : 0x8, 'NPC' : 0x8})
and_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xffffffff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8})
and_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[10]' : 0x0888, 'PC' : 0x8, 'NPC' : 0x8})

andcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0xffffffff, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
andcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0fff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
andcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
andcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0888, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
andcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 0x0}, {'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00400000})

andcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0xffffffff, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
andcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0xffffffff}, {'REGS[1]' : 0x0fff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0xff0fffff})
andcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xffffffff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
andcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0888, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
andcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0x0, 'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00400000})

andn_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[10]' : 0xffffffff, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8})
andn_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8})
andn_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[1]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8})
andn_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[10]' : 0x88888000, 'PC' : 0x8, 'NPC' : 0x8})

andn_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[10]' : 0xffffffff, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8})
andn_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8})
andn_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xffffffff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[1]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8})
andn_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[10]' : 0x88888000, 'PC' : 0x8, 'NPC' : 0x8})

andncc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0, 'PSRbp' : 0x0}, {'REGS[10]' : 0xffffffff, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
andncc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0, 'PSRbp' : 0x0}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
andncc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0, 'PSRbp' : 0x0}, {'REGS[1]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00400000})
andncc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0, 'PSRbp' : 0x0}, {'REGS[10]' : 0x88888000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})

andncc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0, 'PSRbp' : 0x0}, {'REGS[10]' : 0xffffffff, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
andncc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
andncc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xffffffff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[1]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00400000})
andncc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[10]' : 0x88888000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})

or_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
or_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
or_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
or_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
or_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 0xf0f}, {'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x88888f8f, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})

or_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
or_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
or_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
or_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xffffffff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
or_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xf0f, 'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x88888f8f, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})

orcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
orcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
orcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
orcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
orcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 0xf0f}, {'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x88888f8f, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})

orcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
orcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
orcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
orcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xffffffff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
orcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xf0f, 'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x88888f8f, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})

orn_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
orn_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
orn_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
orn_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
orn_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 0xf0f}, {'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0xfffff8f8, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})

orn_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
orn_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
orn_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
orn_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xffffffff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
orn_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xf0f, 'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0xfffff8f8, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})

orncc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
orncc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
orncc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
orncc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00400000})
orncc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 0xf0f}, {'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0xfffff8f8, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})

orncc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
orncc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
orncc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
orncc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xffffffff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00400000})
orncc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xf0f, 'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0xfffff8f8, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})

xor_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xor_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0fff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xor_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xor_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xor_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 0xf0f}, {'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x88888787, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})

xor_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xor_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0fff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xor_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xor_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xffffffff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xor_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xf0f, 'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x88888787, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})

xorcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
xorcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0fff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
xorcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
xorcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
xorcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 0xf0f}, {'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x88888787, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})

xorcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
xorcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0fff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
xorcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
xorcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xffffffff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xffffffff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
xorcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xf0f, 'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x88888787, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})

xnor_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xnor_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xnor_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0fff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xnor_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xnor_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 0xf0f}, {'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x77777878, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})

xnor_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xnor_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xnor_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0fff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xnor_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xffffffff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})
xnor_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xf0f, 'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x77777878, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x0})

xnorcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
xnorcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
xnorcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0fff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
xnorcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00400000})
xnorcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 0xf0f}, {'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x77777878, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})

xnorcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x0, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
xnorcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0xfffff000, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00800000})
xnorcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xfff, 'REGS[10]' : 0xffffffff, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0fff, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})
xnorcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xffffffff, 'REGS[10]' : 0x0, 'REGS[1]' : 0x0, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[1]' : 0x0, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00400000})
xnorcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0xf0f, 'REGS[10]' : 0x88888888, 'PC' : 0x0, 'NPC' : 0x4, 'PSR' : 0x0}, {'REGS[10]' : 0x77777878, 'PC' : 0x8, 'NPC' : 0x8, 'PSR' : 0x00000000})

# Shift
sll_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x00001234}, {'REGS[1]' : 0x00012340})
sll_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0xffffffff}, {'REGS[1]' : 0xfffffff0})

sll_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2':2}, {'REGS[2]' : 4, 'REGS[10]' : 0x00001234}, {'REGS[1]' : 0x00012340})
sll_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2':2}, {'REGS[2]' : 4, 'REGS[10]' : 0xffffffff}, {'REGS[1]' : 0xfffffff0})

srl_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x00001234}, {'REGS[1]' : 0x00000123})
srl_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0xffffffff}, {'REGS[1]' : 0x0fffffff})

srl_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2':2}, {'REGS[2]' : 4, 'REGS[10]' : 0x00001234}, {'REGS[1]' : 0x00000123})
srl_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2':2}, {'REGS[2]' : 4, 'REGS[10]' : 0xffffffff}, {'REGS[1]' : 0x0fffffff})

sra_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x00001234}, {'REGS[1]' : 0x00000123})
sra_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0xffffff11}, {'REGS[1]' : 0xfffffff1})

sra_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2':2}, {'REGS[2]' : 4, 'REGS[10]' : 0x00001234}, {'REGS[1]' : 0x00000123})
sra_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2':2}, {'REGS[2]' : 4, 'REGS[10]' : 0xffffff11}, {'REGS[1]' : 0xfffffff1})

# Add instruction
add_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04}, {'REGS[0]' : 0x0})
add_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04}, {'REGS[1]' : 0x08})
add_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04}, {'REGS[10]' : 0x08})
add_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4}, {'REGS[1]' : 0x0})
add_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5}, {'REGS[1]' : -1})
add_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4}, {'REGS[1]' : -1})

add_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 11}, {'REGS[10]' : 0x04, 'REGS[11]' : 0x04}, {'REGS[0]' : 0x0})
add_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[10]' : 0x04, 'REGS[11]' : 0x04}, {'REGS[1]' : 0x08})
add_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 11}, {'REGS[10]' : 0x04, 'REGS[11]' : 0x04}, {'REGS[10]' : 0x08})
add_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[10]' : -4, 'REGS[11]' : 0x04}, {'REGS[1]' : 0x0})
add_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[10]' : -5, 'REGS[11]' : 0x04}, {'REGS[1]' : -1})
add_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[10]' : 4, 'REGS[11]' : -5}, {'REGS[1]' : -1})

addcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0}, {'REGS[0]' : 0x0, 'PSR': 0x0})
addcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0}, {'REGS[1]' : 0x08, 'PSR': 0x0})
addcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0}, {'REGS[10]' : 0x08, 'PSR': 0x0})
addcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0x0}, {'REGS[1]' : 0x0, 'PSR': 0x00500000})
addcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5, 'PSR': 0x0}, {'REGS[1]' : -1, 'PSR': 0x00800000})
addcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4, 'PSR': 0x0}, {'REGS[1]' : -1, 'PSR': 0x00800000})
addcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1000}, {'REGS[10]' : 0xfffff000, 'PSR': 0x0}, {'REGS[1]' : 0xffffe000, 'PSR': 0x00900000})
addcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1000}, {'REGS[10]' : 0x1001, 'PSR': 0x0}, {'REGS[1]' : 0x1, 'PSR': 0x00100000})

addcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0}, {'REGS[0]' : 0x0, 'PSR': 0x0})
addcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0}, {'REGS[1]' : 0x08, 'PSR': 0x0})
addcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0}, {'REGS[10]' : 0x08, 'PSR': 0x0})
addcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : -4, 'PSR': 0x0}, {'REGS[1]' : 0x0, 'PSR': 0x00500000})
addcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : -5, 'PSR': 0x0}, {'REGS[1]' : -1, 'PSR': 0x00800000})
addcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : -5, 'REGS[10]' : 4, 'PSR': 0x0}, {'REGS[1]' : -1, 'PSR': 0x00800000})
addcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x7fffffff, 'REGS[10]' : 0x7fffffff, 'PSR': 0x0}, {'REGS[1]' : 0xfffffffe, 'PSR': 0x00a00000})
addcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x80000000, 'REGS[10]' : 0x80000000, 'PSR': 0x0}, {'REGS[1]' : 0x0, 'PSR': 0x00700000})
addcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x80000001, 'REGS[10]' : 0x80000000, 'PSR': 0x0}, {'REGS[1]' : 0x01, 'PSR': 0x00300000})

addx_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[0]' : 0x0})
addx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : 0x08})
addx_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[10]' : 0x08})
addx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : 0x0})
addx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : -1})
addx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : -1})
addx_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[0]' : 0x0})
addx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x09})
addx_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[10]' : 0x09})
addx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x1})
addx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0})
addx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0})

addx_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[0]' : 0x0})
addx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : 0x08})
addx_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[10]' : 0x08})
addx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : -4, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : 0x0})
addx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : -5, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : -1})
addx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : -5, 'REGS[10]' : 4, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : -1})
addx_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[0]' : 0x0})
addx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x09})
addx_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[10]' : 0x09})
addx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : -4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x1})
addx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : -5, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0})
addx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : -5, 'REGS[10]' : 4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0})

addxcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[0]' : 0x0, 'PSR': 0x0})
addxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : 0x08, 'PSR': 0x0})
addxcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[10]' : 0x08, 'PSR': 0x0})
addxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : 0x0, 'PSR': 0x00500000})
addxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : -1, 'PSR': 0x00800000})
addxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : -1, 'PSR': 0x00800000})
addxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1000}, {'REGS[10]' : 0xfffff000, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : 0xffffe000, 'PSR': 0x00900000})
addxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1000}, {'REGS[10]' : 0x1001, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : 0x1, 'PSR': 0x00100000})
addxcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[0]' : 0x0, 'PSR': 0x0})
addxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x09, 'PSR': 0x0})
addxcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[10]' : 0x09, 'PSR': 0x0})
addxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x01, 'PSR': 0x00100000})
addxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0, 'PSR': 0x00500000})
addxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0, 'PSR': 0x00500000})
addxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1000}, {'REGS[10]' : 0xfffff000, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0xffffe001, 'PSR': 0x00900000})
addxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1000}, {'REGS[10]' : 0x1001, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x2, 'PSR': 0x00100000})

addxcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[0]' : 0x0, 'PSR': 0x0})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : 0x08, 'PSR': 0x0})
addxcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[10]' : 0x08, 'PSR': 0x0})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : -4, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : 0x0, 'PSR': 0x00500000})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : -5, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : -1, 'PSR': 0x00800000})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : -5, 'REGS[10]' : 4, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : -1, 'PSR': 0x00800000})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x7fffffff, 'REGS[10]' : 0x7fffffff, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : 0xfffffffe, 'PSR': 0x00a00000})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0xffffffff, 'REGS[10]' : 1, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : 0x0, 'PSR': 0x00500000})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x80000000, 'REGS[10]' : 0x80000001, 'PSR': 0x0, 'PSRbp': 0x0}, {'REGS[1]' : 0x1, 'PSR': 0x00300000})
addxcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[0]' : 0x0, 'PSR': 0x0})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x09, 'PSR': 0x0})
addxcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[10]' : 0x09, 'PSR': 0x0})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : -4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x01, 'PSR': 0x00100000})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : -5, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0, 'PSR': 0x00500000})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : -4, 'REGS[10]' : 3, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x0, 'PSR': 0x00500000})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x7fffffff, 'REGS[10]' : 0x7fffffff, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0xffffffff, 'PSR': 0x00a00000})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x80000000, 'REGS[10]' : 0x80000000, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x1, 'PSR': 0x00300000})
addxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x80000000, 'REGS[10]' : 0x80000001, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x2, 'PSR': 0x00300000})

taddcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0}, {'REGS[0]' : 0x0, 'PSR': 0x0})
taddcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0}, {'REGS[1]' : 0x08, 'PSR': 0x0})
taddcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0}, {'REGS[10]' : 0x08, 'PSR': 0x0})
taddcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0x0}, {'REGS[1]' : 0x0, 'PSR': 0x00500000})
taddcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5, 'PSR': 0x0}, {'REGS[1]' : -1, 'PSR': 0x00a00000})
taddcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4, 'PSR': 0x0}, {'REGS[1]' : -1, 'PSR': 0x00a00000})
taddcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1000}, {'REGS[10]' : 0xfffff000, 'PSR': 0x0}, {'REGS[1]' : 0xffffe000, 'PSR': 0x00900000})
taddcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1000}, {'REGS[10]' : 0x1001, 'PSR': 0x0}, {'REGS[1]' : 0x1, 'PSR': 0x00300000})

taddcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0}, {'REGS[0]' : 0x0, 'PSR': 0x0})
taddcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0}, {'REGS[1]' : 0x08, 'PSR': 0x0})
taddcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0}, {'REGS[10]' : 0x08, 'PSR': 0x0})
taddcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : -4, 'PSR': 0x0}, {'REGS[1]' : 0x0, 'PSR': 0x00500000})
taddcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x04, 'REGS[10]' : -5, 'PSR': 0x0}, {'REGS[1]' : -1, 'PSR': 0x00a00000})
taddcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : -5, 'REGS[10]' : 4, 'PSR': 0x0}, {'REGS[1]' : -1, 'PSR': 0x00a00000})
taddcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x7fffffff, 'REGS[10]' : 0x7fffffff, 'PSR': 0x0}, {'REGS[1]' : 0xfffffffe, 'PSR': 0x00a00000})
taddcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x80000000, 'REGS[10]' : 0x80000000, 'PSR': 0x0}, {'REGS[1]' : 0x0, 'PSR': 0x00700000})
taddcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]' : 0x80000001, 'REGS[10]' : 0x80000000, 'PSR': 0x0}, {'REGS[1]' : 0x01, 'PSR': 0x00300000})

taddcctv_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0, 'TBR' : 0x0}, {'REGS[0]' : 0x0, 'PSR': 0x0})
taddcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0, 'TBR' : 0x0}, {'REGS[1]' : 0x08, 'PSR': 0x0})
taddcctv_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x0, 'TBR' : 0x0}, {'REGS[10]' : 0x08, 'PSR': 0x0})
taddcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0x0}, {'REGS[1]' : 0x0, 'PSR': 0x00500000})
taddcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[1]' : 0xabc, 'REGS[10]' : -5, 'PSR': 0x20, 'TBR' : 0x0}, {'REGS[1]' : 0xabc, 'PSR': 0x087, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
taddcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[1]' : 0xabc, 'REGS[10]' : 4, 'PSR': 0x20, 'TBR' : 0x0}, {'REGS[1]' : 0xabc, 'PSR': 0x087, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
taddcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1000}, {'REGS[10]' : 0xfffff000, 'PSR': 0x0, 'TBR' : 0x0}, {'REGS[1]' : 0xffffe000, 'PSR': 0x00900000})
taddcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1000}, {'REGS[1]' : 0xabc, 'REGS[10]' : 0x1001, 'PSR': 0x20, 'TBR' : 0x0}, {'REGS[1]' : 0xabc, 'PSR': 0x087, 'TBR' : 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
taddcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[1]' : 0xabc, 'REGS[10]' : 4, 'PSR': 0xa0, 'TBR' : 0x0}, {'REGS[1]' : 0xabc, 'PSR': 0x0c7, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
taddcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[1]' : 0xabc, 'REGS[10]' : 4, 'PSR': 0x20, 'TBR' : 0x0, 'PC': 0xaa, 'NPC': 0xbb}, {'REGS[17]' : 0xbf, 'REGS[18]' : 0xbf, 'REGS[1]' : 0xabc, 'PSR': 0x087, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
taddcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[1]' : 0xabc, 'REGS[10]' : 4, 'PSR': 0x22, 'TBR' : 0x0}, {'REGS[1]' : 0xabc, 'PSR': 0x081, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
taddcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[1]' : 0xabc, 'WINREGS[42]' : 0xd, 'REGS[10]' : 4, 'PSR': 0x23, 'TBR' : 0x0, 'PC': 0xaa, 'NPC': 0xcc}, {'REGS[17]' : 0xd0, 'REGS[18]' : 0xd0, 'REGS[1]' : 0xabc, 'PSR': 0x082, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4, 'WINREGS[2]' : 4, 'REGS[10]' : 0xd})
taddcctv_imm_Instr.addTest({'rd': 1, 'rs1': 15, 'simm13':-5}, {'REGS[1]' : 0xabc, 'WINREGS[122]' : 0xd, 'REGS[15]' : 4, 'PSR': 0x20, 'TBR' : 0x0, 'PC': 0xaa, 'NPC': 0xcc}, {'REGS[17]' : 0xd0, 'REGS[18]' : 0xd0, 'REGS[1]' : 0xabc, 'PSR': 0x087, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4, 'WINREGS[7]' : 4, 'REGS[10]' : 0xd})

taddcctv_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 11}, {'REGS[11]': 0x04, 'REGS[1]' : 0xabc, 'REGS[10]' : 0x04, 'PSR': 0x0, 'TBR' : 0x0}, {'REGS[0]' : 0x0, 'PSR': 0x0})
taddcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]': 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0, 'TBR' : 0x0}, {'REGS[1]' : 0x08, 'PSR': 0x0})
taddcctv_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 11}, {'REGS[11]': 0x04, 'REGS[10]' : 0x04, 'PSR': 0x0, 'TBR' : 0x0}, {'REGS[10]' : 0x08, 'PSR': 0x0})
taddcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]': 0x04, 'REGS[10]' : -4, 'PSR': 0x0}, {'REGS[1]' : 0x0, 'PSR': 0x00500000})
taddcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]': 0x04, 'REGS[1]' : 0xabc, 'REGS[10]' : -5, 'PSR': 0x20, 'TBR' : 0x0}, {'REGS[1]' : 0xabc, 'PSR': 0x087, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
taddcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]': -5, 'REGS[1]' : 0xabc, 'REGS[10]' : 4, 'PSR': 0x20, 'TBR' : 0x0}, {'REGS[1]' : 0xabc, 'PSR': 0x087, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
taddcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]': 0xfffff000, 'REGS[10]' : 0xfffff000, 'PSR': 0x0, 'TBR' : 0x0}, {'REGS[1]' : 0xffffe000, 'PSR': 0x00900000})
taddcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]': 0xfffff000, 'REGS[1]' : 0xabc, 'REGS[10]' : 0x1001, 'PSR': 0x20, 'TBR' : 0x0}, {'REGS[1]' : 0xabc, 'PSR': 0x087, 'TBR' : 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
taddcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]': -5, 'REGS[1]' : 0xabc, 'REGS[10]' : 4, 'PSR': 0xa0, 'TBR' : 0x0}, {'REGS[1]' : 0xabc, 'PSR': 0x0c7, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
taddcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]': -5, 'REGS[1]' : 0xabc, 'REGS[10]' : 4, 'PSR': 0x20, 'TBR' : 0x0, 'PC': 0xaa, 'NPC': 0xbb}, {'REGS[17]' : 0xbf, 'REGS[18]' : 0xbf, 'REGS[1]' : 0xabc, 'PSR': 0x087, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
taddcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]': -5, 'REGS[1]' : 0xabc, 'REGS[10]' : 4, 'PSR': 0x22, 'TBR' : 0x0}, {'REGS[1]' : 0xabc, 'PSR': 0x081, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
taddcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 11}, {'REGS[11]': -5, 'REGS[1]' : 0xabc, 'WINREGS[42]' : 0xd, 'REGS[10]' : 4, 'PSR': 0x23, 'TBR' : 0x0, 'PC': 0xaa, 'NPC': 0xcc}, {'REGS[17]' : 0xd0, 'REGS[18]' : 0xd0, 'REGS[1]' : 0xabc, 'PSR': 0x082, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4, 'WINREGS[2]' : 4, 'REGS[10]' : 0xd})
taddcctv_reg_Instr.addTest({'rd': 1, 'rs1': 15, 'rs2': 11}, {'REGS[11]': -5, 'REGS[1]' : 0xabc, 'WINREGS[122]' : 0xd, 'REGS[15]' : 4, 'PSR': 0x20, 'TBR' : 0x0, 'PC': 0xaa, 'NPC': 0xcc}, {'REGS[17]' : 0xd0, 'REGS[18]' : 0xd0, 'REGS[1]' : 0xabc, 'PSR': 0x087, 'TBR': 0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4, 'WINREGS[7]' : 4, 'REGS[10]' : 0xd})

# Subtract
sub_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04}, {'REGS[0]' : 0x0})
sub_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04}, {'REGS[1]' : 0x4})
sub_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04}, {'REGS[1]' : 0x0})
sub_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04}, {'REGS[10]' : 0x0})
sub_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':3}, {'REGS[10]' : 0x04}, {'REGS[10]' : 0x01})
sub_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4}, {'REGS[1]' : -8})
sub_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5}, {'REGS[1]' : -9})
sub_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4}, {'REGS[1]' : 9})

sub_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0, 'REGS[10]' : 0x04}, {'REGS[0]' : 0x0})
sub_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0, 'REGS[10]' : 0x04}, {'REGS[1]' : 0x4})
sub_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 4, 'REGS[10]' : 0x04}, {'REGS[1]' : 0x0})
sub_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 4, 'REGS[10]' : 0x04}, {'REGS[10]' : 0x0})
sub_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 3, 'REGS[10]' : 0x04}, {'REGS[10]' : 0x01})
sub_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 4, 'REGS[10]' : -4}, {'REGS[1]' : -8})
sub_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 4, 'REGS[10]' : -5}, {'REGS[1]' : -9})
sub_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : -5, 'REGS[10]' : 4}, {'REGS[1]' : 9})

subcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0}, {'REGS[0]' : 0x0, 'PSR': 0})
subcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0}, {'REGS[1]' : 0x4, 'PSR': 0})
subcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0}, {'REGS[1]' : 0x0, 'PSR': 0x00400000})
subcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0}, {'REGS[10]' : 0x0, 'PSR': 0x00400000})
subcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':3}, {'REGS[10]' : 0x04, 'PSR': 0}, {'REGS[10]' : 0x01, 'PSR': 0})
subcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0}, {'REGS[1]' : -8, 'PSR': 0x00800000})
subcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5, 'PSR': 0}, {'REGS[1]' : -9, 'PSR': 0x00800000})
subcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4, 'PSR': 0}, {'REGS[1]' : 9, 'PSR': 0x00100000})
subcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0x0fff}, {'REGS[10]' : 0x80000000, 'PSR': 0}, {'REGS[1]' : 0x7FFFF001, 'PSR': 0x00200000})
subcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0x1000}, {'REGS[10]' : 0x7fffffff, 'PSR': 0}, {'REGS[1]' : 0x80000fff, 'PSR': 0x00b00000})

subcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0, 'REGS[10]': 0x04, 'PSR': 0}, {'REGS[0]' : 0x0, 'PSR': 0})
subcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0, 'REGS[10]': 0x04, 'PSR': 0}, {'REGS[1]' : 0x4, 'PSR': 0})
subcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': 0x04, 'PSR': 0}, {'REGS[1]' : 0x0, 'PSR': 0x00400000})
subcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': 0x04, 'PSR': 0}, {'REGS[10]' : 0x0, 'PSR': 0x00400000})
subcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 3, 'REGS[10]': 0x04, 'PSR': 0}, {'REGS[10]' : 0x01, 'PSR': 0})
subcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': -4, 'PSR': 0}, {'REGS[1]' : -8, 'PSR': 0x00800000})
subcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': -5, 'PSR': 0}, {'REGS[1]' : -9, 'PSR': 0x00800000})
subcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': -5, 'REGS[10]': 4, 'PSR': 0}, {'REGS[1]' : 9, 'PSR': 0x00100000})
subcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x0fff, 'REGS[10]': 0x80000000, 'PSR': 0}, {'REGS[1]' : 0x7FFFF001, 'PSR': 0x00200000})
subcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xfffff000, 'REGS[10]': 0x7fffffff, 'PSR': 0}, {'REGS[1]': 0x80000fff, 'PSR': 0x00b00000})

subx_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[0]' : 0x0})
subx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : 0x4})
subx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : 0x0})
subx_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[10]' : 0x0})
subx_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':3}, {'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[10]' : 0x01})
subx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : -8})
subx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : -9})
subx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : 9})
subx_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[0]' : 0x0})
subx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x3})
subx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : -1})
subx_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[10]' : -1})
subx_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':3}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[10]' : 0x0})
subx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : -9})
subx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : -10})
subx_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 8})

subx_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0, 'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[0]' : 0x0})
subx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0, 'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : 0x4})
subx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 4, 'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : 0x0})
subx_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 4, 'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[10]' : 0x0})
subx_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 3, 'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[10]' : 0x01})
subx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 4, 'REGS[10]' : -4, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : -8})
subx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 4, 'REGS[10]' : -5, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : -9})
subx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : -5, 'REGS[10]' : 4, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : 9})
subx_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0, 'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[0]' : 0x0})
subx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 0, 'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x3})
subx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 4, 'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : -1})
subx_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 4, 'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[10]' : -1})
subx_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 3, 'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[10]' : 0x0})
subx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 4, 'REGS[10]' : -4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : -9})
subx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : 4, 'REGS[10]' : -5, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : -10})
subx_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]' : -5, 'REGS[10]' : 4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 8})

subxcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[0]': 0x0, 'PSR': 0})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x4, 'PSR': 0})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x0, 'PSR': 0x00400000})
subxcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[10]': 0x0, 'PSR': 0x00400000})
subxcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':3}, {'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[10]': 0x01, 'PSR': 0})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': -8, 'PSR': 0x00800000})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': -9, 'PSR': 0x00800000})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 9, 'PSR': 0x00100000})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0x0fff}, {'REGS[10]' : 0x80000000, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x7FFFF001, 'PSR': 0x00200000})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0x1000}, {'REGS[10]' : 0x7fffffff, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x80000fff, 'PSR': 0x00b00000})
subxcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[0]': 0x0, 'PSR': 0})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]': 0x3, 'PSR': 0})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]': -1, 'PSR': 0x00900000})
subxcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[10]': -1, 'PSR': 0x00900000})
subxcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':3}, {'REGS[10]' : 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[10]': 0x0, 'PSR': 0x00400000})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]': -9, 'PSR': 0x00800000})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]': -10, 'PSR': 0x00800000})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]': 8, 'PSR': 0x00100000})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0x0fff}, {'REGS[10]' : 0x80000000, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]': 0x7FFFF000, 'PSR': 0x00200000})
subxcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0x1000}, {'REGS[10]' : 0x7fffffff, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]': 0x80000ffe, 'PSR': 0x00b00000})

subxcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0, 'REGS[10]': 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[0]' : 0x0, 'PSR': 0})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0, 'REGS[10]': 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : 0x4, 'PSR': 0})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : 0x0, 'PSR': 0x00400000})
subxcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[10]' : 0x0, 'PSR': 0x00400000})
subxcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 3, 'REGS[10]': 0x04, 'PSR': 0, 'PSRbp': 0}, {'REGS[10]' : 0x01, 'PSR': 0})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': -4, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : -8, 'PSR': 0x00800000})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': -5, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : -9, 'PSR': 0x00800000})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': -5, 'REGS[10]': 4, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : 9, 'PSR': 0x00100000})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x0fff, 'REGS[10]': 0x80000000, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]' : 0x7FFFF001, 'PSR': 0x00200000})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xfffff000, 'REGS[10]': 0x7fffffff, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x80000fff, 'PSR': 0x00b00000})
subxcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0, 'REGS[10]': 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[0]': 0x0, 'PSR': 0})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0, 'REGS[10]': 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]': 0x3, 'PSR': 0})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]': -1, 'PSR': 0x00900000})
subxcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[10]': -1, 'PSR': 0x00900000})
subxcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 3, 'REGS[10]': 0x04, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[10]': 0x0, 'PSR': 0x00400000})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': -4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : -9, 'PSR': 0x00800000})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': -5, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : -10, 'PSR': 0x00800000})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': -5, 'REGS[10]': 4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 8, 'PSR': 0x00100000})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x0fff, 'REGS[10]': 0x80000000, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]' : 0x7FFFF000, 'PSR': 0x00200000})
subxcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xfffff000, 'REGS[10]': 0x7fffffff, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'REGS[1]': 0x80000ffe, 'PSR': 0x00b00000})

tsubcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0}, {'REGS[0]' : 0x0, 'PSR': 0})
tsubcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0}, {'REGS[1]' : 0x4, 'PSR': 0})
tsubcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0}, {'REGS[1]' : 0x0, 'PSR': 0x00400000})
tsubcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0}, {'REGS[10]' : 0x0, 'PSR': 0x00400000})
tsubcc_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':3}, {'REGS[10]' : 0x04, 'PSR': 0}, {'REGS[10]' : 0x01, 'PSR': 0x00200000})
tsubcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0}, {'REGS[1]' : -8, 'PSR': 0x00800000})
tsubcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5, 'PSR': 0}, {'REGS[1]' : -9, 'PSR': 0x00a00000})
tsubcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4, 'PSR': 0}, {'REGS[1]' : 9, 'PSR': 0x00300000})
tsubcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0x0fff}, {'REGS[10]' : 0x80000000, 'PSR': 0}, {'REGS[1]' : 0x7FFFF001, 'PSR': 0x00200000})
tsubcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0x1000}, {'REGS[10]' : 0x7fffffff, 'PSR': 0}, {'REGS[1]' : 0x80000fff, 'PSR': 0x00b00000})

tsubcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0, 'REGS[10]': 0x04, 'PSR': 0}, {'REGS[0]' : 0x0, 'PSR': 0})
tsubcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0, 'REGS[10]': 0x04, 'PSR': 0}, {'REGS[1]' : 0x4, 'PSR': 0})
tsubcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': 0x04, 'PSR': 0}, {'REGS[1]' : 0x0, 'PSR': 0x00400000})
tsubcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': 0x04, 'PSR': 0}, {'REGS[10]' : 0x0, 'PSR': 0x00400000})
tsubcc_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 3, 'REGS[10]': 0x04, 'PSR': 0}, {'REGS[10]' : 0x01, 'PSR': 0x00200000})
tsubcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': -4, 'PSR': 0}, {'REGS[1]' : -8, 'PSR': 0x00800000})
tsubcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': -5, 'PSR': 0}, {'REGS[1]' : -9, 'PSR': 0x00a00000})
tsubcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': -5, 'REGS[10]': 4, 'PSR': 0}, {'REGS[1]' : 9, 'PSR': 0x00300000})
tsubcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x0fff, 'REGS[10]': 0x80000000, 'PSR': 0}, {'REGS[1]' : 0x7FFFF001, 'PSR': 0x00200000})
tsubcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xfffff000, 'REGS[10]': 0x7fffffff, 'PSR': 0}, {'REGS[1]': 0x80000fff, 'PSR': 0x00b00000})

tsubcctv_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0, 'TBR': 0x0}, {'REGS[0]' : 0x0, 'PSR': 0})
tsubcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0}, {'REGS[10]' : 0x04, 'PSR': 0, 'TBR': 0x0}, {'REGS[1]' : 0x4, 'PSR': 0})
tsubcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0, 'TBR': 0x0}, {'REGS[1]' : 0x0, 'PSR': 0x00400000})
tsubcctv_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':4}, {'REGS[10]' : 0x04, 'PSR': 0, 'TBR': 0x0}, {'REGS[10]' : 0x0, 'PSR': 0x00400000})
tsubcctv_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13':3}, {'REGS[10]' : 0x04, 'PSR': 0x20, 'TBR': 0x0}, {'WINREGS[2]' : 0x04, 'PSR': 0x87, 'TBR':0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
tsubcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0, 'TBR': 0x0}, {'REGS[1]' : -8, 'PSR': 0x00800000})
tsubcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -4, 'PSR': 0x20, 'TBR': 0x0}, {'REGS[1]' : -8, 'PSR': 0x00800020})
tsubcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':4}, {'REGS[10]' : -5, 'PSR': 0x20, 'TBR': 0x0, 'REGS[1]' : 0xabc}, {'REGS[1]' : 0xabc, 'PSR': 0x087, 'TBR':0x0a0})
tsubcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':-5}, {'REGS[10]' : 4, 'PSR': 0x20, 'TBR': 0x0, 'REGS[1]' : 0xabc}, {'TBR': 0x0a0, 'REGS[1]' : 0xabc, 'PSR': 0x087})
tsubcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0x0fff}, {'REGS[10]' : 0x80000000, 'TBR': 0x44000, 'PSR': 0x22, 'REGS[1]' : 0xabc}, {'REGS[1]' : 0xabc, 'PSR': 0x081, 'WINREGS[2]' : 0x80000000, 'PC': 0x440a4, 'NPC': 0x440a4})
tsubcctv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13':0x1000}, {'REGS[10]' : 0x7fffffff, 'TBR': 0x44000, 'PSR': 0xa2, 'REGS[1]' : 0xabc}, {'REGS[1]' : 0xabc, 'PSR': 0x0c1, 'WINREGS[2]' : 0x7fffffff, 'PC': 0x440a4, 'NPC': 0x440a4})

tsubcctv_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0, 'REGS[10]': 0x04, 'PSR': 0, 'TBR': 0x0}, {'REGS[0]' : 0x0, 'PSR': 0})
tsubcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0, 'REGS[10]': 0x04, 'PSR': 0, 'TBR': 0x0}, {'REGS[1]' : 0x4, 'PSR': 0})
tsubcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': 0x04, 'PSR': 0, 'TBR': 0x0}, {'REGS[1]' : 0x0, 'PSR': 0x00400000})
tsubcctv_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': 0x04, 'PSR': 0, 'TBR': 0x0}, {'REGS[10]' : 0x0, 'PSR': 0x00400000})
tsubcctv_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 3, 'REGS[10]': 0x04, 'PSR': 0x20, 'TBR': 0x0}, {'REGS[2]': 3, 'WINREGS[2]' : 0x04, 'GLOBAL[2]' : 3, 'PSR': 0x87, 'TBR':0x0a0, 'PC': 0x0a4, 'NPC': 0x0a4})
tsubcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': -4, 'PSR': 0, 'TBR': 0x0}, {'REGS[1]' : -8, 'PSR': 0x00800000})
tsubcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': -4, 'PSR': 0x20, 'TBR': 0x0}, {'REGS[1]' : -8, 'PSR': 0x00800020})
tsubcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 4, 'REGS[10]': -5, 'PSR': 0x20, 'TBR': 0x0, 'REGS[1]' : 0xabc}, {'REGS[1]' : 0xabc, 'PSR': 0x087, 'TBR':0x0a0})
tsubcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': -5, 'REGS[10]': 4, 'PSR': 0x20, 'TBR': 0x0, 'REGS[1]' : 0xabc}, {'TBR': 0x0a0, 'REGS[1]' : 0xabc, 'PSR': 0x087})
tsubcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x0fff, 'REGS[10]': 0x80000000, 'TBR': 0x44000, 'PSR': 0x22, 'REGS[1]' : 0xabc}, {'REGS[1]' : 0xabc, 'PSR': 0x081, 'WINREGS[2]' : 0x80000000, 'PC': 0x440a4, 'NPC': 0x440a4})
tsubcctv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xfffff000, 'REGS[10]': 0x7fffffff, 'TBR': 0x44000, 'PSR': 0xa2, 'REGS[1]' : 0xabc}, {'REGS[1]' : 0xabc, 'PSR': 0x0c1, 'WINREGS[2]' : 0x7fffffff, 'PC': 0x440a4, 'NPC': 0x440a4})

# Multiply Step
mulscc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0}, {'Ybp': 0, 'Y': 0, 'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'Y': 0, 'REGS[0]': 0x0, 'PSR': 0})
mulscc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0}, {'Ybp': 0, 'Y': 0, 'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0x0}, {'Y': 0, 'REGS[1]': 0x2, 'PSR': 0x0})
mulscc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0}, {'Ybp': 0, 'Y': 0, 'REGS[10]' : 0x04, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'Y': 0, 'REGS[1]': 0x80000002, 'PSR': 0x00800000})
mulscc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 1}, {'Ybp': 0x3, 'Y': 0x3, 'REGS[10]' : 0x04, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'Y': 0x1, 'REGS[1]': 0x80000003, 'PSR': 0x00800000})
mulscc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 1}, {'Ybp': 0x3, 'Y': 0x3, 'REGS[10]' : 0x05, 'PSR': 0x0, 'PSRbp': 0x0}, {'Y': 0x80000001, 'REGS[1]': 0x3, 'PSR': 0x0})
mulscc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1000}, {'Ybp': 0x3, 'Y': 0x3, 'REGS[10]' : 0x05, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'Y': 0x80000001, 'REGS[1]': 0x7FFFF002, 'PSR': 0x00300000})
mulscc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1000}, {'Ybp': 0x3, 'Y': 0x3, 'REGS[10]' : 0x05, 'PSR': 0x00a00000, 'PSRbp': 0x00a00000}, {'Y': 0x80000001, 'REGS[1]': 0xFFFFF002, 'PSR': 0x00800000})

mulscc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0, 'Ybp': 0, 'Y': 0, 'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'Y': 0, 'REGS[0]': 0x0, 'PSR': 0})
mulscc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0, 'Ybp': 0, 'Y': 0, 'REGS[10]' : 0x04, 'PSR': 0x0, 'PSRbp': 0}, {'Y': 0, 'REGS[1]': 0x2, 'PSR': 0x0})
mulscc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0, 'Ybp': 0, 'Y': 0, 'REGS[10]' : 0x04, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'Y': 0, 'REGS[1]': 0x80000002, 'PSR': 0x00800000})
mulscc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 1, 'Ybp': 0x3, 'Y': 0x3, 'REGS[10]' : 0x04, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'Y': 0x1, 'REGS[1]': 0x80000003, 'PSR': 0x00800000})
mulscc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 1, 'Ybp': 0x3, 'Y': 0x3, 'REGS[10]' : 0x05, 'PSR': 0x0, 'PSRbp': 0x0}, {'Y': 0x80000001, 'REGS[1]': 0x3, 'PSR': 0x0})
mulscc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xfffff000, 'Ybp': 0x3, 'Y': 0x3, 'REGS[10]' : 0x05, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'Y': 0x80000001, 'REGS[1]': 0x7FFFF002, 'PSR': 0x00300000})
mulscc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xfffff000, 'Ybp': 0x3, 'Y': 0x3, 'REGS[10]' : 0x05, 'PSR': 0x00a00000, 'PSRbp': 0x00a00000}, {'Y': 0x80000001, 'REGS[1]': 0xFFFFF002, 'PSR': 0x00800000})

# Multiply
umul_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0x04}, {'Y': 0, 'REGS[0]': 0x0})
umul_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0xffffffff}, {'Y': 0x1, 'REGS[0]': 0x0})
umul_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0x04}, {'Y': 0, 'REGS[1]': 0x08})
umul_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0xffffffff}, {'Y': 0x1, 'REGS[1]': 0xfffffffe})
umul_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0x2}, {'Y': 0x1, 'REGS[1]': 0xfffffffe})
umul_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0xffffffff}, {'Y': 0xFFFFFFFE, 'REGS[1]': 0x00000001})
umul_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff}, {'Y': 0xFFE, 'REGS[1]': 0xFFFFF001})

umul_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]': 0x04}, {'Y': 0, 'REGS[0]': 0x0})
umul_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]': 0xffffffff}, {'Y': 0x1, 'REGS[0]': 0x0})
umul_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]': 0x04}, {'Y': 0, 'REGS[1]': 0x08})
umul_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]': 0xffffffff}, {'Y': 0x1, 'REGS[1]': 0xfffffffe})
umul_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xffffffff, 'REGS[10]': 0x2}, {'Y': 0x1, 'REGS[1]': 0xfffffffe})
umul_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xffffffff, 'REGS[10]': 0xffffffff}, {'Y': 0xFFFFFFFE, 'REGS[1]': 0x00000001})
umul_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xfff, 'REGS[10]': 0xffffffff}, {'Y': 0xFFE, 'REGS[1]': 0xFFFFF001})

smul_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0x04}, {'Y': 0, 'REGS[0]': 0x0})
smul_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0xffffffff}, {'Y': 0xffffffff, 'REGS[0]': 0x0})
smul_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0x04}, {'Y': 0, 'REGS[1]': 0x08})
smul_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0xffffffff}, {'Y': 0xffffffff, 'REGS[1]': 0xfffffffe})
smul_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0x2}, {'Y': 0xffffffff, 'REGS[1]': 0xfffffffe})
smul_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0xffffffff}, {'Y': 0x0, 'REGS[1]': 0x1})
smul_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff}, {'Y': 0xffffffff, 'REGS[1]': 0xFFFFF001})

smul_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]' : 0x04}, {'Y': 0, 'REGS[0]': 0x0})
smul_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]' : 0xffffffff}, {'Y': 0xffffffff, 'REGS[0]': 0x0})
smul_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]' : 0x04}, {'Y': 0, 'REGS[1]': 0x08})
smul_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]' : 0xffffffff}, {'Y': 0xffffffff, 'REGS[1]': 0xfffffffe})
smul_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xffffffff, 'REGS[10]' : 0x2}, {'Y': 0xffffffff, 'REGS[1]': 0xfffffffe})
smul_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xffffffff, 'REGS[10]' : 0xffffffff}, {'Y': 0x0, 'REGS[1]': 0x1})
smul_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x0fff, 'REGS[10]' : 0xffffffff}, {'Y': 0xffffffff, 'REGS[1]': 0xFFFFF001})

umulcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'Y': 0, 'REGS[0]': 0x0, 'PSR': 0x0})
umulcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0xffffffff, 'PSR': 0, 'PSRbp': 0}, {'Y': 0x1, 'REGS[0]': 0x0, 'PSR': 0x00800000})
umulcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0x04, 'PSR': 0, 'PSRbp': 0}, {'Y': 0, 'REGS[1]': 0x08, 'PSR': 0x0})
umulcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0xffffffff, 'PSR': 0, 'PSRbp': 0}, {'Y': 0x1, 'REGS[1]': 0xfffffffe, 'PSR': 0x00800000})
umulcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0x2, 'PSR': 0, 'PSRbp': 0}, {'Y': 0x1, 'REGS[1]': 0xfffffffe, 'PSR': 0x00800000})
umulcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0xffffffff, 'PSR': 0, 'PSRbp': 0}, {'Y': 0xFFFFFFFE, 'REGS[1]': 0x00000001, 'PSR': 0x0})
umulcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'PSR': 0, 'PSRbp': 0}, {'Y': 0xFFE, 'REGS[1]': 0xFFFFF001, 'PSR': 0x00800000})
umulcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x0}, {'REGS[10]' : 0xffffffff, 'PSR': 0, 'PSRbp': 0}, {'Y': 0x0, 'REGS[1]': 0x0, 'PSR': 0x00400000})

umulcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]' : 0x04, 'PSR': 0}, {'Y': 0, 'REGS[0]': 0x0, 'PSR': 0x0})
umulcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0x1, 'REGS[0]': 0x0, 'PSR': 0x00800000})
umulcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]' : 0x04, 'PSR': 0}, {'Y': 0, 'REGS[1]': 0x08, 'PSR': 0x0})
umulcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0x1, 'REGS[1]': 0xfffffffe, 'PSR': 0x00800000})
umulcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xffffffff, 'REGS[10]' : 0x2, 'PSR': 0}, {'Y': 0x1, 'REGS[1]': 0xfffffffe, 'PSR': 0x00800000})
umulcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xffffffff, 'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0xFFFFFFFE, 'REGS[1]': 0x00000001, 'PSR': 0x0})
umulcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x0fff, 'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0xFFE, 'REGS[1]': 0xFFFFF001, 'PSR': 0x00800000})
umulcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x0, 'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0x0, 'REGS[1]': 0x0, 'PSR': 0x00400000})

smulcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0x04, 'PSR': 0}, {'Y': 0, 'REGS[0]': 0x0, 'PSR': 0})
smulcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0xffffffff, 'REGS[0]': 0x0, 'PSR': 0x00800000})
smulcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0x04, 'PSR': 0}, {'Y': 0, 'REGS[1]': 0x08, 'PSR': 0})
smulcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0xffffffff, 'REGS[1]': 0xfffffffe, 'PSR': 0x00800000})
smulcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0x2, 'PSR': 0}, {'Y': 0xffffffff, 'REGS[1]': 0xfffffffe, 'PSR': 0x00800000})
smulcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0x0, 'REGS[1]': 0x1, 'PSR': 0})
smulcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0xffffffff, 'REGS[1]': 0xFFFFF001, 'PSR': 0x00800000})
smulcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x0}, {'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0x0, 'REGS[1]': 0x0, 'PSR': 0x00400000})

smulcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]' : 0x04, 'PSR': 0}, {'Y': 0, 'REGS[0]': 0x0, 'PSR': 0})
smulcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0xffffffff, 'REGS[0]': 0x0, 'PSR': 0x00800000})
smulcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]' : 0x04, 'PSR': 0}, {'Y': 0, 'REGS[1]': 0x08, 'PSR': 0})
smulcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0xffffffff, 'REGS[1]': 0xfffffffe, 'PSR': 0x00800000})
smulcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xffffffff, 'REGS[10]' : 0x2, 'PSR': 0}, {'Y': 0xffffffff, 'REGS[1]': 0xfffffffe, 'PSR': 0x00800000})
smulcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xffffffff, 'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0x0, 'REGS[1]': 0x1, 'PSR': 0})
smulcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x0fff, 'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0xffffffff, 'REGS[1]': 0xFFFFF001, 'PSR': 0x00800000})
smulcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x0, 'REGS[10]' : 0xffffffff, 'PSR': 0}, {'Y': 0x0, 'REGS[1]': 0x0, 'PSR': 0x00400000})

# Multiply Accumulate Instructions
umac_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]' : 0x04}, {'ASR[18]': 0x0c, 'Y': 0x08, 'REGS[0]': 0x0})
umac_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'ASR18bp': 0xfffffffe, 'ASR[18]': 0xfffffffe, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]' : 0x7fffffff}, {'ASR[18]': 0x1fffc, 'Y': 0x09, 'REGS[0]': 0x0})
umac_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 2}, {'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]' : 0x04}, {'ASR[18]': 0x0c, 'Y': 0x08, 'REGS[10]': 0x0c})
umac_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 2}, {'ASR18bp': 0xfffffffe, 'ASR[18]': 0xfffffffe, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]' : 0x7fffffff}, {'ASR[18]': 0x1fffc, 'Y': 0x09, 'REGS[10]': 0x1fffc})
umac_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0xff, 'Y': 0xff, 'REGS[10]' : 0x2}, {'ASR[18]': 0x20002, 'Y': 0xff, 'REGS[1]': 0x20002})
umac_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x0f, 'Y': 0x0f, 'REGS[10]' : 0xffffffff}, {'ASR[18]': 0xFFFE0005, 'Y': 0x0f, 'REGS[1]': 0xFFFE0005})
umac_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x0f, 'Y': 0x0f, 'REGS[10]' : 0xffffffff}, {'ASR[18]': 0xFFEF005, 'Y': 0x0f, 'REGS[1]': 0xFFEF005})

umac_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]': 0x04}, {'ASR[18]': 0x0c, 'Y': 0x08, 'REGS[0]': 0x0})
umac_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'ASR18bp': 0xfffffffe, 'ASR[18]': 0xfffffffe, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]' : 0x7fffffff}, {'ASR[18]': 0x1fffc, 'Y': 0x09, 'REGS[0]': 0x0})
umac_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]' : 0x04}, {'ASR[18]': 0x0c, 'Y': 0x08, 'REGS[10]': 0x0c})
umac_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'ASR18bp': 0xfffffffe, 'ASR[18]': 0xfffffffe, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]' : 0x7fffffff}, {'ASR[18]': 0x1fffc, 'Y': 0x09, 'REGS[10]': 0x1fffc})
umac_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xffffffff, 'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0xff, 'Y': 0xff, 'REGS[10]' : 0x2}, {'ASR[18]': 0x20002, 'Y': 0xff, 'REGS[1]': 0x20002})
umac_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xffffffff, 'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x0f, 'Y': 0x0f, 'REGS[10]' : 0xffffffff}, {'ASR[18]': 0xFFFE0005, 'Y': 0x0f, 'REGS[1]': 0xFFFE0005})
umac_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x00000fff, 'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x0f, 'Y': 0x0f, 'REGS[10]' : 0xffffffff}, {'ASR[18]': 0xFFEF005, 'Y': 0x0f, 'REGS[1]': 0xFFEF005})

smac_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]': 0x04}, {'ASR[18]': 0x0c, 'Y': 0x08, 'REGS[0]': 0x0})
smac_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'ASR18bp': 0xfffffffe, 'ASR[18]': 0xfffffffe, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]': 0x7fffffff}, {'ASR[18]': 0xfffffffc, 'Y': 0xff, 'REGS[0]': 0x0})
smac_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 2}, {'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]': 0x04}, {'ASR[18]': 0x0c, 'Y': 0x08, 'REGS[10]': 0x0c})
smac_imm_Instr.addTest({'rd': 10, 'rs1': 10, 'simm13': 2}, {'ASR18bp': 0xfffffffe, 'ASR[18]': 0xfffffffe, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]': 0x7fffffff}, {'ASR[18]': 0xfffffffc, 'Y': 0xff, 'REGS[10]': 0xfffffffc})
smac_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0xff, 'Y': 0xff, 'REGS[10]': 0x2}, {'ASR[18]': 0x02, 'Y': 0xff, 'REGS[1]': 0x02})
smac_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x1fff}, {'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x0f, 'Y': 0x0f, 'REGS[10]': 0xffffffff}, {'ASR[18]': 0x5, 'Y': 0x0f, 'REGS[1]': 0x5})
smac_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0xfff}, {'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x0f, 'Y': 0x0f, 'REGS[10]': 0xffffffff}, {'ASR[18]': 0xFFFFF005, 'Y': 0x0e, 'REGS[1]': 0xFFFFF005})

smac_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]': 0x04}, {'ASR[18]': 0x0c, 'Y': 0x08, 'REGS[0]': 0x0})
smac_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'ASR18bp': 0xfffffffe, 'ASR[18]': 0xfffffffe, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]': 0x7fffffff}, {'ASR[18]': 0xfffffffc, 'Y': 0xff, 'REGS[0]': 0x0})
smac_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]': 0x04}, {'ASR[18]': 0x0c, 'Y': 0x08, 'REGS[10]': 0x0c})
smac_reg_Instr.addTest({'rd': 10, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x02, 'ASR18bp': 0xfffffffe, 'ASR[18]': 0xfffffffe, 'Ybp': 0x08, 'Y': 0x08, 'REGS[10]': 0x7fffffff}, {'ASR[18]': 0xfffffffc, 'Y': 0xff, 'REGS[10]': 0xfffffffc})
smac_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xffffffff, 'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0xff, 'Y': 0xff, 'REGS[10]': 0x2}, {'ASR[18]': 0x02, 'Y': 0xff, 'REGS[1]': 0x02})
smac_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0xffffffff, 'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x0f, 'Y': 0x0f, 'REGS[10]': 0xffffffff}, {'ASR[18]': 0x5, 'Y': 0x0f, 'REGS[1]': 0x5})
smac_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 2}, {'REGS[2]': 0x00000fff, 'ASR18bp': 0x04, 'ASR[18]': 0x04, 'Ybp': 0x0f, 'Y': 0x0f, 'REGS[10]': 0xffffffff}, {'ASR[18]': 0xFFFFF005, 'Y': 0x0e, 'REGS[1]': 0xFFFFF005})

# Divide
udiv_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02}, {'REGS[0]': 0})
udiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02}, {'REGS[1]': 1})
udiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x0}, {'REGS[1]': 0})
udiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x2, 'Y': 0x2, 'REGS[10]': 0x0}, {'REGS[1]': 0xFFFFFFFF})
udiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0xFFFFFFFE}, {'REGS[1]': 0xFFFFFFFF})
udiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0}, {'REGS[1]': 0x80000000})
udiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0}, {'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0, 'REGS[1]': 0xabc, 'PSR': 0x20, 'TBR': 0x0}, {'REGS[1]': 0xabc, 'TBR': 0x2a0, 'PSR': 0x087, 'PC': 0x2a4, 'NPC': 0x2a4})
udiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0xFFFFFFFF})
udiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x01FFF}, {'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0xFFFFFFFF})
udiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x01FFF}, {'Ybp': 0x7FFFFFFF, 'Y': 0x7FFFFFFF, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x80000000})
udiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x01FFF}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x1})
udiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x00FFF}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x100100})

udiv_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02}, {'REGS[0]': 0})
udiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02}, {'REGS[1]': 1})
udiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x0}, {'REGS[1]': 0})
udiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x2, 'Y': 0x2, 'REGS[10]': 0x0}, {'REGS[1]': 0xFFFFFFFF})
udiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0xFFFFFFFE}, {'REGS[1]': 0xFFFFFFFF})
udiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0}, {'REGS[1]': 0x80000000})
udiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0, 'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0, 'REGS[1]': 0xabc, 'PSR': 0x20, 'TBR': 0x0}, {'REGS[1]': 0xabc, 'TBR': 0x2a0, 'PSR': 0x087, 'PC': 0x2a4, 'NPC': 0x2a4})
udiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0xFFFFFFFF})
udiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0xFFFFFFFF, 'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0xFFFFFFFF})
udiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0xFFFFFFFF, 'Ybp': 0x7FFFFFFF, 'Y': 0x7FFFFFFF, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x80000000})
udiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0xFFFFFFFF, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x1})
udiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0x0FFF, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x100100})

sdiv_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02}, {'REGS[0]': 0})
sdiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02}, {'REGS[1]': 1})
sdiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x0}, {'REGS[1]': 0})
sdiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x2, 'Y': 0x2, 'REGS[10]': 0x0}, {'REGS[1]': 0x7FFFFFFF})
sdiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0x6}, {'REGS[1]': 0x80000003})
sdiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0xFFFFFFFE}, {'REGS[1]': 0x7FFFFFFF})
sdiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0}, {'REGS[1]': 0x7FFFFFFF})
sdiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0}, {'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0, 'REGS[1]': 0xabc, 'PSR': 0x20, 'TBR': 0x0}, {'REGS[1]': 0xabc, 'TBR': 0x2a0, 'PSR': 0x087, 'PC': 0x2a4, 'NPC': 0x2a4})
sdiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x0})
sdiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFE}, {'REGS[1]': 0xFFFFFFFF})
sdiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x01FFF}, {'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x1})
sdiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x01FFF}, {'Ybp': 0x7FFFFFFF, 'Y': 0x7FFFFFFF, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x80000000})
sdiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x01FFF}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x80000000})
sdiv_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x00FFF}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x100100})

sdiv_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02}, {'REGS[0]': 0})
sdiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02}, {'REGS[1]': 1})
sdiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x0}, {'REGS[1]': 0})
sdiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x2, 'Y': 0x2, 'REGS[10]': 0x0}, {'REGS[1]': 0x7FFFFFFF})
sdiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0x6}, {'REGS[1]': 0x80000003})
sdiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0xFFFFFFFE}, {'REGS[1]': 0x7FFFFFFF})
sdiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0}, {'REGS[1]': 0x7FFFFFFF})
sdiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0, 'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0, 'REGS[1]': 0xabc, 'PSR': 0x20, 'TBR': 0x0}, {'REGS[1]': 0xabc, 'TBR': 0x2a0, 'PSR': 0x087, 'PC': 0x2a4, 'NPC': 0x2a4})
sdiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x0})
sdiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFE}, {'REGS[1]': 0xFFFFFFFF})
sdiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0xFFFFFFFF, 'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x1})
sdiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0xFFFFFFFF, 'Ybp': 0x7FFFFFFF, 'Y': 0x7FFFFFFF, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x80000000})
sdiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0xFFFFFFFF, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x80000000})
sdiv_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0x0FFF, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF}, {'REGS[1]': 0x100100})

udivcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02, 'PSR': 0, 'PSRbp': 0}, {'REGS[0]': 0, 'PSR': 0})
udivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 1, 'PSR': 0})
udivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x0, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0, 'PSR': 0x00400000})
udivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x2, 'Y': 0x2, 'REGS[10]': 0x0, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0xFFFFFFFF, 'PSR': 0x00a00000})
udivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0xFFFFFFFE, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0xFFFFFFFF, 'PSR': 0x00800000})
udivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x80000000, 'PSR': 0x00800000})
udivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0}, {'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0, 'REGS[1]': 0xabc, 'PSR': 0x20, 'TBR': 0x0}, {'REGS[1]': 0xabc, 'TBR': 0x2a0, 'PSR': 0x087, 'PC': 0x2a4, 'NPC': 0x2a4})
udivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0xFFFFFFFF, 'PSR': 0x00a00000})
udivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x01FFF}, {'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0xFFFFFFFF, 'PSR': 0x00a00000})
udivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x01FFF}, {'Ybp': 0x7FFFFFFF, 'Y': 0x7FFFFFFF, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x80000000, 'PSR': 0x00800000})
udivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x01FFF}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x1, 'PSR': 0})
udivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x00FFF}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x100100, 'PSR': 0})

udivcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02, 'PSR': 0, 'PSRbp': 0}, {'REGS[0]': 0, 'PSR': 0})
udivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 1, 'PSR': 0})
udivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x0, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0, 'PSR': 0})
udivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x2, 'Y': 0x2, 'REGS[10]': 0x0, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0xFFFFFFFF, 'PSR': 0})
udivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0xFFFFFFFE, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0xFFFFFFFF, 'PSR': 0})
udivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x80000000, 'PSR': 0})
udivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0, 'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0, 'REGS[1]': 0xabc, 'PSR': 0x20, 'TBR': 0x0}, {'REGS[1]': 0xabc, 'TBR': 0x2a0, 'PSR': 0x087, 'PC': 0x2a4, 'NPC': 0x2a4, 'PSR': 0})
udivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0xFFFFFFFF, 'PSR': 0})
udivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0xFFFFFFFF, 'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0xFFFFFFFF, 'PSR': 0})
udivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0xFFFFFFFF, 'Ybp': 0x7FFFFFFF, 'Y': 0x7FFFFFFF, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x80000000, 'PSR': 0})
udivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0xFFFFFFFF, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x1, 'PSR': 0})
udivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0x0FFF, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x100100, 'PSR': 0})

sdivcc_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02, 'PSR': 0, 'PSRbp': 0}, {'REGS[0]': 0, 'PSR': 0})
sdivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 1, 'PSR': 0})
sdivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x0, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0, 'PSR': 0})
sdivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x2, 'Y': 0x2, 'REGS[10]': 0x0, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x7FFFFFFF, 'PSR': 0})
sdivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0x6, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x80000003, 'PSR': 0})
sdivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0xFFFFFFFE, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x7FFFFFFF, 'PSR': 0})
sdivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x7FFFFFFF, 'PSR': 0})
sdivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0}, {'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0, 'REGS[1]': 0xabc, 'PSR': 0x20, 'TBR': 0x0}, {'REGS[1]': 0xabc, 'TBR': 0x2a0, 'PSR': 0x087, 'PC': 0x2a4, 'NPC': 0x2a4, 'PSR': 0})
sdivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x0, 'PSR': 0})
sdivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 2}, {'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFE, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0xFFFFFFFF, 'PSR': 0})
sdivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x01FFF}, {'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x1, 'PSR': 0})
sdivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x01FFF}, {'Ybp': 0x7FFFFFFF, 'Y': 0x7FFFFFFF, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x80000000, 'PSR': 0})
sdivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x01FFF}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x80000000, 'PSR': 0})
sdivcc_imm_Instr.addTest({'rd': 1, 'rs1': 10, 'simm13': 0x00FFF}, {'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x100100, 'PSR': 0})

sdivcc_reg_Instr.addTest({'rd': 0, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02, 'PSR': 0, 'PSRbp': 0}, {'REGS[0]': 0, 'PSR': 0})
sdivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x02, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 1, 'PSR': 0})
sdivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0x0, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0, 'PSR': 0})
sdivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x2, 'Y': 0x2, 'REGS[10]': 0x0, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x7FFFFFFF, 'PSR': 0})
sdivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0x6, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x80000003, 'PSR': 0})
sdivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0xFFFFFFFE, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x7FFFFFFF, 'PSR': 0})
sdivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x7FFFFFFF, 'PSR': 0})
sdivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0, 'Ybp': 0x1, 'Y': 0x1, 'REGS[10]': 0x0, 'REGS[1]': 0xabc, 'PSR': 0x20, 'TBR': 0x0}, {'REGS[1]': 0xabc, 'TBR': 0x2a0, 'PSR': 0x087, 'PC': 0x2a4, 'NPC': 0x2a4, 'PSR': 0})
sdivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x0, 'PSR': 0})
sdivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 2, 'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFE, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0xFFFFFFFF, 'PSR': 0})
sdivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0xFFFFFFFF, 'Ybp': 0xFFFFFFFF, 'Y': 0xFFFFFFFF, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x1, 'PSR': 0})
sdivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0xFFFFFFFF, 'Ybp': 0x7FFFFFFF, 'Y': 0x7FFFFFFF, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x80000000, 'PSR': 0})
sdivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0xFFFFFFFF, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x80000000, 'PSR': 0})
sdivcc_reg_Instr.addTest({'rd': 1, 'rs1': 10, 'rs2': 15}, {'REGS[15]': 0x0FFF, 'Ybp': 0x0, 'Y': 0x0, 'REGS[10]': 0xFFFFFFFF, 'PSR': 0, 'PSRbp': 0}, {'REGS[1]': 0x100100, 'PSR': 0})

# Save and Restore
#save_imm_Instr.addTest({}, {}, {})

#save_reg_Instr.addTest({}, {}, {})

#restore_imm_Instr.addTest({}, {}, {})

#restore_reg_Instr.addTest({}, {}, {})

# Branch on Integer Condition Codes
branch_Instr.addTest({'cond': int('1000', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1000', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x804, 'NPC' : 0x804})
branch_Instr.addTest({'cond': int('0000', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('0000', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1001', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1001', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1001', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00400000, 'PSRbp': 0x00400000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1001', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00400000, 'PSRbp': 0x00400000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('0001', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00400000, 'PSRbp': 0x00400000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0001', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00400000, 'PSRbp': 0x00400000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0001', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('0001', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('1010', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1010', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1010', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00a00000, 'PSRbp': 0x00a00000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1010', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00a00000, 'PSRbp': 0x00a00000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1010', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00400000, 'PSRbp': 0x00400000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1010', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00400000, 'PSRbp': 0x00400000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('1010', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1010', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('1010', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00200000, 'PSRbp': 0x00200000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1010', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00200000, 'PSRbp': 0x00200000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('1010', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00600000, 'PSRbp': 0x00600000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1010', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00600000, 'PSRbp': 0x00600000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('0010', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00400000, 'PSRbp': 0x00400000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0010', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00400000, 'PSRbp': 0x00400000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0010', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0010', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0010', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00200000, 'PSRbp': 0x00200000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0010', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00200000, 'PSRbp': 0x00200000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0010', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00600000, 'PSRbp': 0x00600000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0010', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00600000, 'PSRbp': 0x00600000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0010', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('0010', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('0010', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00a00000, 'PSRbp': 0x00a00000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('0010', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00a00000, 'PSRbp': 0x00a00000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('1011', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1011', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1011', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00a00000, 'PSRbp': 0x00a00000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1011', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00a00000, 'PSRbp': 0x00a00000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1011', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1011', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('1011', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00200000, 'PSRbp': 0x00200000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1011', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00200000, 'PSRbp': 0x00200000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('0011', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0011', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0011', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00200000, 'PSRbp': 0x00200000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0011', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00200000, 'PSRbp': 0x00200000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0011', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('0011', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('0011', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00a00000, 'PSRbp': 0x00a00000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('0011', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00a00000, 'PSRbp': 0x00a00000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('1100', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1100', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1100', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1100', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('1100', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00400000, 'PSRbp': 0x00400000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1100', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00400000, 'PSRbp': 0x00400000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('1100', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00500000, 'PSRbp': 0x00500000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1100', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00500000, 'PSRbp': 0x00500000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('0100', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0100', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0100', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00400000, 'PSRbp': 0x00400000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0100', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00400000, 'PSRbp': 0x00400000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0100', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00500000, 'PSRbp': 0x00500000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0100', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00500000, 'PSRbp': 0x00500000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0100', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('0100', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('1101', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1101', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1101', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1101', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('0101', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0101', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00100000, 'PSRbp': 0x00100000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0101', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('0101', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('1110', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1110', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1110', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1110', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('0110', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0110', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00800000, 'PSRbp': 0x00800000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0110', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('0110', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('1111', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1111', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('1111', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00200000, 'PSRbp': 0x00200000}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('1111', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00200000, 'PSRbp': 0x00200000}, {'PC' : 0x8, 'NPC' : 0x8})
branch_Instr.addTest({'cond': int('0111', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00200000, 'PSRbp': 0x00200000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0111', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x00200000, 'PSRbp': 0x00200000}, {'PC' : 0x8, 'NPC' : 0x800})
branch_Instr.addTest({'cond': int('0111', 2), 'a': 1, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0xc, 'NPC' : 0xc})
branch_Instr.addTest({'cond': int('0111', 2), 'a': 0, 'disp22': 0x200}, {'PC' : 0x0, 'NPC' : 0x4, 'PSR': 0x0, 'PSRbp': 0x0}, {'PC' : 0x8, 'NPC' : 0x8})

# Call and Link
call_Instr.addTest({'disp30': 0x0}, {'PC' : 0x0, 'NPC' : 0x4}, {'REGS[15]': 0, 'PC' : 0x8, 'NPC' : 0x4})
call_Instr.addTest({'disp30': 0xff}, {'PC' : 0x0, 'NPC' : 0x4}, {'REGS[15]': 0, 'PC' : 0x8, 'NPC' : 0x400})
call_Instr.addTest({'disp30': 0xff0}, {'PC' : 0x4, 'NPC' : 0x8}, {'REGS[15]': 4, 'PC' : 0xc, 'NPC' : 0x3fc8})

# Jump and Link
#jump_imm_Instr.addTest({}, {}, {})

#jump_reg_Instr.addTest({}, {}, {})

# Return from Trap
# N.B. In the reg read stage it writes the values of the SU and ET PSR
# fields???????
#rett_imm_Instr.addTest({}, {}, {})

#rett_reg_Instr.addTest({}, {}, {})

# Trap on Integer Condition Code; note this instruction also receives the forwarding
# of the PSR
#trap_imm_Instr.addTest({}, {}, {})

#trap_reg_Instr.addTest({}, {}, {})

# Read State Register
#readY_Instr.addTest({}, {}, {})

#readASR_Instr.addTest({}, {}, {})

#readPsr_Instr.addTest({}, {}, {})

#readWim_Instr.addTest({}, {}, {})

#readTbr_Instr.addTest({}, {}, {})

# Write State Register
#writeY_reg_Instr.addTest({}, {}, {})

#writeY_imm_Instr.addTest({}, {}, {})

#writeASR_reg_Instr.addTest({}, {}, {})

#writeASR_imm_Instr.addTest({}, {}, {})

#writePsr_reg_Instr.addTest({}, {}, {})

#writePsr_imm_Instr.addTest({}, {}, {})

#writeWim_reg_Instr.addTest({}, {}, {})

#writeWim_imm_Instr.addTest({}, {}, {})

#writeTbr_reg_Instr.addTest({}, {}, {})

#writeTbr_imm_Instr.addTest({}, {}, {})

## Store Barrier
#stbar_Instr.addTest({}, {}, {})

# Flush Memory
#flush_reg_Instr.addTest({}, {}, {})

#flush_imm_Instr.addTest({}, {}, {})
