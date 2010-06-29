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
if((bitSeq & (1 << (bitSeq_length - 1))) != 0)
    bitSeq |= (((unsigned int)0xFFFFFFFF) << bitSeq_length);
return bitSeq;
""")
SignExtend_method = trap.HelperMethod('SignExtend', opCode, 'execution')
SignExtend_method.setSignature(('BIT<32>'), [('bitSeq', 'BIT<32>'), cxx_writer.writer_code.Parameter('bitSeq_length', cxx_writer.writer_code.uintType)])

#Simple Branch
opCode = cxx_writer.writer_code.Code("""
if (br == 1){
	FPC = offset;
}else{
	FPC = 0;
}
return FPC;
""")
SimpleBranch_method = trap.HelperMethod('SimpleBranch', opCode, 'execution')
SimpleBranch_method.setSignature(('BIT<32>'), [('br', 'BIT<1>'),('offset', 'BIT<32>')])

#Likely Branch
opCode = cxx_writer.writer_code.Code("""
if (br == 1){	//This should be done while the next instruction is being fetch, but we are not working with pipeline.
	FPC = offset;
}else{
	FPC = 0;
	//annull(); //Not to execute the branch slot. As we are not working with pipeline, this makes no difference.
}
return FPC;
""")
LikelyBranch_method = trap.HelperMethod('LikelyBranch', opCode, 'execution')
LikelyBranch_method.setSignature(('BIT<32>'), [('br', 'BIT<1>'),('offset', 'BIT<32>')])

# Exceptions
raiseExcCode =  """
long vectorOffset = 0;
    //std::cout << "Exception Entered " << exceptionId << std::endl;

LLbit = 0;

annull();

"""
#RaiseException_method = trap.HelperMethod('RaiseException', cxx_writer.writer_code.Code(raiseExcCode), 'exception')
RaiseException_method = trap.HelperMethod('RaiseException', cxx_writer.writer_code.Code(raiseExcCode), 'execution')
RaiseException_methodParams = [cxx_writer.writer_code.Parameter('exceptionId', cxx_writer.writer_code.uintType)]
RaiseException_methodParams.append(cxx_writer.writer_code.Parameter('customTrapOffset', cxx_writer.writer_code.uintType, initValue = '0'))
RaiseException_method.setSignature(cxx_writer.writer_code.voidType, RaiseException_methodParams)

#Increment PC
opCode = cxx_writer.writer_code.Code("""

bool cond1 = ExtraRegister[key_branch];
bool cond2 = ExtraRegister[key_lbranch];
bool cond3 = ExtraRegister[key_jump1];
bool cond4 = ExtraRegister[key_jump2];

if (cond1 == 1){
	PC += FPC;
	if (cond2 == 1){
		annull();
	}
	ExtraRegister[key_branch] = 0;
	ExtraRegister[key_lbranch] = 0;
} else if (cond3 == 1){
	PC = (PC&0xF0000000) + FPC + 4; //I need to add 4 because I am fetching the PC-4. In the case of a branch this is not necessary because I anyway added +4 when waiting for the next instruction to add the FPC to the PC.
	ExtraRegister[key_jump1] = 0;
} else if (cond4 == 1){
	PC = FPC + 4; //I need to add 4 because I am fetching the PC-4. In the case of a branch this is not necessary because I anyway added +4 when waiting for the next instruction to add the FPC to the PC.
	ExtraRegister[key_jump2] = 0;
}else {
	PC += 4;
}
""")
IncrementPC = trap.HelperOperation('IncrementPC', opCode, exception = False)

#No Increment PC
opCode = cxx_writer.writer_code.Code("""
""")
NoIncrementPC = trap.HelperOperation('NoIncrementPC', opCode, exception = False)




