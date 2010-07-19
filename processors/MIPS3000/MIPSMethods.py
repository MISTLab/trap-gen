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
    
if (exceptionId == RESET){
	STATUS[key_RP] = 0;
	STATUS[key_BEV] = 1;
	STATUS[key_TS] = 0;
	STATUS[key_SR] = 0; 
	STATUS[key_NMI] = 0;
	STATUS[key_ERL] = 1; 
	WATCHLO[key_I] = 0;
	WATCHLO[key_R] = 0; 
	WATCHLO[key_W] = 0;
	// Since we are not working with pipelines we don't consider the branch delay slot case, otherwise we'd need a conditional to evaluate the value of ErrorEPC.
	ERROREPC = PC; 
	//PC = 0xBFC00000;  
}

else if (exceptionId == SOFT_RESET){
	STATUS[key_BEV] = 1;
	STATUS[key_TS] = 0;
	STATUS[key_SR] = 1;
	STATUS[key_NMI] = 0;
	STATUS[key_ERL] = 1; 
	ERROREPC = PC; 
	//PC = 0xBFC00000;
}

else if (exceptionId == NMI){

	STATUS[key_BEV] = 1;
	STATUS[key_TS] = 0;
	STATUS[key_SR] = 0;
	STATUS[key_NMI] = 1;
	STATUS[key_ERL] = 1; 
	ERROREPC = PC; 
	//PC = 0xBFC00000;
}

// Debug Exception Processing 

else if(exceptionId == DSS || exceptionId == DINT || exceptionId == DIB  || exceptionId == DBP  || exceptionId == DDBLad  || exceptionId == DDBS  || exceptionId == DDBL ){

	DEPC = PC; // Assuming no branch delay slot
	DEBUG[key_DBD] = 0; 

	switch (exceptionId){
		case DSS:				
			DEBUG[key_DSS] = 1;
		break;

		case DINT:
			DEBUG[key_DINT] = 1;
		break; 

		case DIB:
			DEBUG[key_DIB] = 1;
		break; 

		case DBP:
			DEBUG[key_DBp] = 1;
		break; 

		case DDBLad:
			DEBUG[key_DDBL] = 1;
		break; 

		case DDBS:
			DEBUG[key_DDBS] = 1;
		break; 

		case DDBL:
			DEBUG[key_DDBL] = 1;
		break; 

		default:
		break;
	}

	DEBUG[key_Halt] == 1; //  we assumed the clock is never stopped since we are not modelling the bus

	if (STATUS[key_RP] == 1 || ExtraRegister[key_waitbit] == 1){ 			
		DEBUG[key_Doze] = 1;  	
	} else {
		DEBUG[key_Doze] = 0;
	}
 
	DEBUG[key_DM] = 1; 
	if (ECR[key_ProbTrap]==1){
		PC = 0xFF200200;
	}else {
		PC = 0xBFC00480;
	}

} else { 

	
//General Exception Processing 

	if(STATUS[key_EXL] == 0){
		EPC = PC; 
		CAUSE[key_BD]= 0; // Assuming no branch delay slot 
		if((exceptionId == INT) && (CAUSE[key_IV]==1)){
			vectorOffset = 0x200;
		}else{
			vectorOffset = 0x180;
		}

	}else{
		vectorOffset = 0x180;
	}

	CAUSE[key_CE]= 0;

	switch (exceptionId){
		case INT:
			CAUSE[key_EXCCODE]= 0x00;
		break;
	
		case ADEL_FETCH:
			CAUSE[key_EXCCODE]= 0x04;
		break;

		case ADEL:
			CAUSE[key_EXCCODE]= 0x04;
		break;

		case ADES:
			CAUSE[key_EXCCODE]= 0x05;
		break;
		
		case IBE:
			CAUSE[key_EXCCODE]= 0x06;
		break;

		case DBE:
			CAUSE[key_EXCCODE]= 0x07;
		break;

		case SYS:
			CAUSE[key_EXCCODE]= 0x08;
		break;

		case BP:
			CAUSE[key_EXCCODE]= 0x09;
		break;

		case RI:
			CAUSE[key_EXCCODE]= 0x0A;
		break;

		case CPU:
			CAUSE[key_EXCCODE]= 0x0B;
		break;

		case OV:
			CAUSE[key_EXCCODE]= 0x0C;
		break;

		case TR:
			CAUSE[key_EXCCODE]= 0x0D;
		break;

		case DEFERRED_WATCH:
			CAUSE[key_EXCCODE]= 0x17;
		break;

		case WATCH_FETCH:
			CAUSE[key_EXCCODE]= 0x17;
		break;

		case WATCH_DATA:
			CAUSE[key_EXCCODE]= 0x17;
		break;

		case MACHINE_CHECK:
			CAUSE[key_EXCCODE]= 0x18;
		break;
		
		default:
		break;
	}

	STATUS[key_EXL] = 1; 

	if (STATUS[key_BEV]=1){
		//PC = 0xBFC00200 + vectorOffset;
	} else {
		//PC = 0x80000000 + vectorOffset; 
	}

}			

	
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
	FPC = 0;
} else if (cond3 == 1){
	PC = (PC&0xF0000000) + FPC + 4; //I need to add 4 because I am fetching the PC-4. In the case of a branch this is not necessary because I anyway added +4 when waiting for the next instruction to add the FPC to the PC.
	ExtraRegister[key_jump1] = 0;
	FPC = 0;
} else if (cond4 == 1){
	PC = FPC + 4; //I need to add 4 because I am fetching the PC-4. In the case of a branch this is not necessary because I anyway added +4 when waiting for the next instruction to add the FPC to the PC.
	ExtraRegister[key_jump2] = 0;
	FPC = 0;
}else {
	PC += 4;
}
""")
IncrementPC = trap.HelperOperation('IncrementPC', opCode, exception = False)

#No Increment PC
opCode = cxx_writer.writer_code.Code("""
""")
NoIncrementPC = trap.HelperOperation('NoIncrementPC', opCode, exception = False)




