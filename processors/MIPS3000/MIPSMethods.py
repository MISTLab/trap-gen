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

VER COMO MANEJAR LAS INTERRUPCIONES
VERIFICAR QUE SE ESTEN GENERANDO LAS EXCEPCIONES CUANDO SE DEBAN GENERAR
COMO DIFERIR(que se ejecuten más tarde) EXCEPCIONES (PARA WATCH POR EJEMPLO)
VERIFICAR LO DE EXCEPCIONES MASK OR UNMASK

if (exceptionId < 3 || exceptionId == 5){
	
	if (exeptionId == RESET){
		CONFIG0 = 0xA5000002;
		CONFIG1 = 0x0000000A;
		RP = 0;
		I = 0;
		R = 0;
		W = 0;
	}

	BEV = 1;
	TS = 0;
	SR = 0;
	if (exceptionId == SOFT_RESET)
		SR = 1;
	NMI = 0;
	if (exceptionId == NMI)
		NMI = 1;
	ERL = 1;

	// Since we are not working with pipelines, there are no branch delays slots.
	ERROREPC = PC;
	PC = 0xBFC00000;

} else if ( (exceptionId == DSS) || (exceptionId == DINT) || (exceptionId == DIB) || (exceptionId == DBP)|| (exceptionId == DDBLS) || (exceptionId == DDBL) ){

		// Since we are not working with pipelines, there are no branch delays slots.
		DEPC = PC;
		DBD = 0;

		switch (exceptionId){
			case DSS:{
				DSS = 1;
			}break;
			case DINT:{
				DINT = 1;
			}break;
			case DIB:{
				DIB = 1;
			}break;
			case DBP:{
				DBp = 1;
			}break;
			case DDBLad:{
				DDBL = 1;
			}break;
			case DDBS:{
				DDBS = 1;
			}break;
			case DDBL:{
				DDBL = 1;
			}break;
		}

		Halt //Defining whether the internal system bus was stopped or not. (How to check it?)
		if (RP == 1){ //Defining whether the processor was in low power mode or not. (How to check it was in low power mode if entered by WAIT?)
			Doze = 1;
		} else {
			Doze = 0;
		}

		DM = 1;

		if (ProbTrap == 1){
	   		PC = 0xFF20_0200;
		}else{
		   	PC = 0xBFC0_0480;
		}


	} else{

			CE = 0; //Unit number of the coprocessor

		    switch(exceptionId){
			case INT:{
			EXCCODE = 0x00;
			}break;

			case WATCH_FETCH:{
				if (EXL == 1 || ERL == 1 || DM== 1){
					WP = 1;
					deferre exception;
				}
			EXCCODE = 0x17;
			}break;

			case ADEL_FETCH:{
			BadVAddr = PC;
			EXCCODE = 0x04;
			}break;

			case IBE:{
			EXCCODE = 0x06;
			}break;

			case SYS:{
			EXCCODE = 0x08;
			}break;

			case BP:{
			EXCCODE = 0x09;
			}break;

			case CPU:{
			EXCCODE = 0x0B;
			}break;

			case RI:{
			EXCCODE = 0x0A;
			}break;

			case OV:{
			EXCCODE = 0x0C;
			}break;

			case TR:{
			EXCCODE = 0x0D;
			}break;

			case WATCH_DATA:{
				if (EXL == 1 || ERL == 1 || DM== 1){
					WP = 1;
					deferre exception;
				}
			EXCCODE = 0x17;
			}break;

			case ADEL:{
			BadVAddr = PC;
			EXCCODE = 0x04;
			}break;

			case ADES:{
			BadVAddr = PC;
			EXCCODE = 0x05;
			}break;

			case DBE:{
			EXCCODE = 0x07;
			}break;

			default:{
			}break;
		    }


		if (EXL == 0){
		// Since we are not working with pipelines, there are no branch delays slots.
			EPC = PC;
			BD = 0;

			if ( (exceptionId == INT) && IV == 1){
				vectorOffset = 0x200;
			} else {
				vectorOffset = 0x180;
			}
		} else {
			vectorOffset = 0x180;
		}


		EXL = 1;

		if (BEV == 1){
			PC= 0xBFC00200 + vectorOffset;
		}else{
			PC= 0x80000000 + vectorOffset;
		}
	}
}


annull();

}
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




