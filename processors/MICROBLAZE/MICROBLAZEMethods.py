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
import cxx_writer

#-------------------------------------------------------
# Miscellaneous operations which can be used and
# accessed by any instruction
#-------------------------------------------------------
# *******
# Here we define some helper methods, which are not directly part of the
# instructions, but which can be called by the instruction body
# *******

opCode = cxx_writer.writer_code.Code("""
if((bitSeq & (1 << (bitSeq_length - 1))) != 0)
    bitSeq |= (((unsigned int)0xFFFFFFFF) << bitSeq_length);
return bitSeq;
""")
SignExtend_method = trap.HelperMethod('SignExtend', opCode, 'execute')
SignExtend_method.setSignature(('BIT<32>'), [('bitSeq', 'BIT<32>'), cxx_writer.writer_code.Parameter('bitSeq_length', cxx_writer.writer_code.uintType)])

# PC increment
opCode = cxx_writer.writer_code.Code("""
if (TARGET == 0xffffffff) {
	PC = PC + 4;
} else {
	PC = TARGET;
	TARGET = 0xffffffff;
}
""")
IncrementPC = trap.HelperOperation('IncrementPC', opCode, inline = False)

opCode = cxx_writer.writer_code.Code("""
	if ( IMMREG & 0x80000000 ) {  /* IMM instruction */
		imm_value = ((int)imm & 0x0000ffff) + (int)(IMMREG << 16);
		IMMREG &= 0x7fffffff;
	} else {	/* No IMM instruction */
		imm_value = (int)SignExtend(imm,16);
	} 
	
	
""")
IMM_handler = trap.HelperOperation('IMM_handler', opCode)
IMM_handler.addInstuctionVar(('imm_value', 'BIT<32>'))
IMM_handler.addUserInstructionElement('imm')

opCode = cxx_writer.writer_code.Code("""
	IMMREG &= 0x7fffffff;
""")
IMM_reset = trap.HelperOperation('IMM_reset', opCode)

