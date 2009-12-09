#Implementing the methods.
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

#Sign Extension
opCode = cxx_writer.writer_code.Code("""
bitSeq |= (((unsigned int)0xFFFFFFFF) << 16);
return bitSeq;
""")
SignExtend_method = trap.HelperMethod('SignExtend', opCode, 'execution')
SignExtend_method.setSignature(('BIT<32>'), [('bitSeq', 'BIT<32>')])

#Simple Branch
opCode = cxx_writer.writer_code.Code("""
if (br == 1){
	PC += offset;
}else{
	PC += 4;
}
return PC;
""")
SimpleBranch_method = trap.HelperMethod('SimpleBranch', opCode, 'execution')
SimpleBranch_method.setSignature(('BIT<32>'), [('br', 'BIT<1>'),('offset', 'BIT<32>')])

#Likely Branch
opCode = cxx_writer.writer_code.Code("""
if (br == 1){	//This should be done while the next instruction is being fetch, but we are not working with pipeline.
	PC += offset;
}else{
	PC += 4;
	//anull(); //Not to execute the branch slot. As we are not working with pipeline, this makes no difference.
}
return PC;
""")
LikelyBranch_method = trap.HelperMethod('LikelyBranch', opCode, 'execution')
LikelyBranch_method.setSignature(('BIT<32>'), [('br', 'BIT<1>'),('offset', 'BIT<32>')])

# Exceptions
raiseExcCode =  """
long vectorOffset = 0;


annull();

"""
RaiseException_method = trap.HelperMethod('RaiseException', cxx_writer.writer_code.Code(raiseExcCode), 'exception')
RaiseException_methodParams = [cxx_writer.writer_code.Parameter('exceptionId', cxx_writer.writer_code.uintType)]
RaiseException_methodParams.append(cxx_writer.writer_code.Parameter('customTrapOffset', cxx_writer.writer_code.uintType, initValue = '0'))
RaiseException_method.setSignature(cxx_writer.writer_code.voidType, RaiseException_methodParams)

#Increment PC
opCode = cxx_writer.writer_code.Code("""
PC += 4;
""")
IncrementPC = trap.HelperOperation('IncrementPC', opCode, exception = False)




