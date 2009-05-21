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

def updateAliasCode():
    code = """for(int i = 8; i < 32; i++){
        REGS[i].updateAlias(WINREGS[(newCwp*16 + i - 8) % (16*NUM_REG_WIN)]);
    }
    """
    #code = ''
    #for i in range(8, 32):
        #code += 'REGS[' + str(i) + '].updateAlias(WINREGS[(newCwp*16 + ' + str(i - 8) + ') % (16*NUM_REG_WIN)]);\n'
    return code

# Method used to move to the next register window; this simply consists in
# the check that there is an empty valid window and in the update of
# the window aliases
IncrementRegWindow_code = """
newCwp = ((unsigned int)(PSR[key_CWP] + 1)) % NUM_REG_WIN;
if(((0x01 << (newCwp)) & WIM) != 0){
    return false;
}
PSRbp = (PSR & 0xFFFFFFE0) | newCwp;
PSR.immediateWrite(PSRbp);
"""
IncrementRegWindow_code += updateAliasCode()
IncrementRegWindow_code += 'return true;'
opCode = cxx_writer.writer_code.Code(IncrementRegWindow_code)
IncrementRegWindow_method = trap.HelperMethod('IncrementRegWindow', opCode, 'execute')
IncrementRegWindow_method.setSignature(cxx_writer.writer_code.boolType)
IncrementRegWindow_method.addVariable(('newCwp', 'BIT<32>'))
# Method used to move to the previous register window; this simply consists in
# the check that there is an empty valid window and in the update of
# the window aliases
DecrementRegWindow_code = """
newCwp = ((unsigned int)(PSR[key_CWP] - 1)) % NUM_REG_WIN;
if(((0x01 << (newCwp)) & WIM) != 0){
    return false;
}
PSRbp = (PSR & 0xFFFFFFE0) | newCwp;
PSR.immediateWrite(PSRbp);
"""
DecrementRegWindow_code += updateAliasCode()
DecrementRegWindow_code += 'return true;'
opCode = cxx_writer.writer_code.Code(DecrementRegWindow_code)
DecrementRegWindow_method = trap.HelperMethod('DecrementRegWindow', opCode, 'execute')
DecrementRegWindow_method.setSignature(cxx_writer.writer_code.boolType)
DecrementRegWindow_method.addVariable(('newCwp', 'BIT<32>'))

# Sign extends the input bitstring
opCode = cxx_writer.writer_code.Code("""
if((bitSeq & (1 << (bitSeq_length - 1))) != 0)
    bitSeq |= (((unsigned int)0xFFFFFFFF) << bitSeq_length);
return bitSeq;
""")
SignExtend_method = trap.HelperMethod('SignExtend', opCode, 'execute')
SignExtend_method.setSignature(cxx_writer.writer_code.intType, [('bitSeq', 'BIT<32>'), cxx_writer.writer_code.Parameter('bitSeq_length', cxx_writer.writer_code.uintType)])

# Normal PC increment, used when not in a branch instruction; in a branch instruction
# I will directly modify both PC and nPC in case we are in a the cycle accurate model,
# while just nPC in case we are in the functional one; if the branch has the annulling bit
# set, then also in the functional model both the PC and nPC will be modified
raiseExcCode = """
if(PSR[key_ET] == 0){
    if(exceptionId < IRQ_LEV_15){
        // I print a core dump and then I signal an error: an exception happened while
        // exceptions were disabled in the processor core
        THROW_EXCEPTION("Exception " << exceptionId << " happened while the PSR[ET] = 0; PC = " << std::hex << std::showbase << PC << std::endl << "Instruction " << getMnemonic());
    }
}
else{
    unsigned int curPSR = PSR;
    curPSR = (curPSR & 0xffffffbf) | (PSR[key_S] << 6);
    curPSR = (curPSR & 0xffffff7f) | 0x00000080;
    curPSR &= 0xffffffdf;
    unsigned int newCwp = ((unsigned int)(PSR[key_CWP] - 1)) % NUM_REG_WIN;
"""
raiseExcCode += updateAliasCode()
raiseExcCode +=  """
    curPSR = (curPSR & 0xffffffe0) + newCwp;
    PSR = curPSR;
    PSRbp = curPSR;
    #ifdef ACC_MODEL
    REGS[17] = PC;
    REGS[18] = NPC;
    #else
    REGS[17] = PC - 12;
    REGS[18] = NPC - 4;
    #endif
    switch(exceptionId){
        case RESET:{
        }break;
        case DATA_STORE_ERROR:{
            TBR[key_TT] = 0x2b;
        }break;
        case INSTR_ACCESS_MMU_MISS:{
            TBR[key_TT] = 0x3c;
        }break;
        case INSTR_ACCESS_ERROR:{
            TBR[key_TT] = 0x21;
        }break;
        case R_REGISTER_ACCESS_ERROR:{
            TBR[key_TT] = 0x20;
        }break;
        case INSTR_ACCESS_EXC:{
            TBR[key_TT] = 0x01;
        }break;
        case PRIVILEDGE_INSTR:{
            TBR[key_TT] = 0x03;
        }break;
        case ILLEGAL_INSTR:{
            TBR[key_TT] = 0x02;
        }break;
        case FP_DISABLED:{
            TBR[key_TT] = 0x04;
        }break;
        case CP_DISABLED:{
            TBR[key_TT] = 0x24;
        }break;
        case UNIMPL_FLUSH:{
            TBR[key_TT] = 0x25;
        }break;
        case WATCHPOINT_DETECTED:{
            TBR[key_TT] = 0x0b;
        }break;
        case WINDOW_OVERFLOW:{
            TBR[key_TT] = 0x05;
        }break;
        case WINDOW_UNDERFLOW:{
            TBR[key_TT] = 0x06;
        }break;
        case MEM_ADDR_NOT_ALIGNED:{
            TBR[key_TT] = 0x07;
        }break;
        case FP_EXCEPTION:{
            TBR[key_TT] = 0x08;
        }break;
        case CP_EXCEPTION:{
            TBR[key_TT] = 0x28;
        }break;
        case DATA_ACCESS_ERROR:{
            TBR[key_TT] = 0x29;
        }break;
        case DATA_ACCESS_MMU_MISS:{
            TBR[key_TT] = 0x2c;
        }break;
        case DATA_ACCESS_EXC:{
            TBR[key_TT] = 0x09;
        }break;
        case TAG_OVERFLOW:{
            TBR[key_TT] = 0x0a;
        }break;
        case DIV_ZERO:{
            TBR[key_TT] = 0x2a;
        }break;
        case TRAP_INSTRUCTION:{
            TBR[key_TT] = 0x80 + customTrapOffset;
        }break;
        case IRQ_LEV_15:{
            TBR[key_TT] = 0x1f;
        }break;
        case IRQ_LEV_14:{
            TBR[key_TT] = 0x1e;
        }break;
        case IRQ_LEV_13:{
            TBR[key_TT] = 0x1d;
        }break;
        case IRQ_LEV_12:{
            TBR[key_TT] = 0x1c;
        }break;
        case IRQ_LEV_11:{
            TBR[key_TT] = 0x1b;
        }break;
        case IRQ_LEV_10:{
            TBR[key_TT] = 0x1a;
        }break;
        case IRQ_LEV_9:{
            TBR[key_TT] = 0x19;
        }break;
        case IRQ_LEV_8:{
            TBR[key_TT] = 0x18;
        }break;
        case IRQ_LEV_7:{
            TBR[key_TT] = 0x17;
        }break;
        case IRQ_LEV_6:{
            TBR[key_TT] = 0x16;
        }break;
        case IRQ_LEV_5:{
            TBR[key_TT] = 0x15;
        }break;
        case IRQ_LEV_4:{
            TBR[key_TT] = 0x14;
        }break;
        case IRQ_LEV_3:{
            TBR[key_TT] = 0x13;
        }break;
        case IRQ_LEV_2:{
            TBR[key_TT] = 0x12;
        }break;
        case IRQ_LEV_1:{
            TBR[key_TT] = 0x11;
        }break;
        case IMPL_DEP_EXC:{
            TBR[key_TT] = 0x60 + customTrapOffset;
        }break;
        default:{
        }break;
    }
    if(exceptionId == RESET){
        // I have to jump to address 0 and restart execution
        PC = 0;
        NPC = 4;
    }
    else{
        // I have to jump to the address contained in the TBR register
        PC = TBR;
        NPC = TBR + 4;
    }
    flush();
    annull();
}
"""
RaiseException_method = trap.HelperMethod('RaiseException', cxx_writer.writer_code.Code(raiseExcCode), 'exception')
RaiseException_methodParams = [cxx_writer.writer_code.Parameter('exceptionId', cxx_writer.writer_code.uintType)]
RaiseException_methodParams.append(cxx_writer.writer_code.Parameter('customTrapOffset', cxx_writer.writer_code.uintType, initValue = '0'))
RaiseException_method.setSignature(cxx_writer.writer_code.voidType, RaiseException_methodParams)

# Code used to jump to the trap handler address. This code modifies the PC and the NPC
# so that the next instruction fetched is the one of the trap handler;
# it also performs a flush of the pipeline
opCode = cxx_writer.writer_code.Code("""unsigned int npc = NPC;
PC = npc;
npc += 4;
NPC = npc;
""")
IncrementPC = trap.HelperOperation('IncrementPC', opCode, exception = False)

# Write back of the result of most operations, expecially ALUs;
# such operations do not modify the PSR
opCode = cxx_writer.writer_code.Code("""
rd = result;
""")
WB_plain = trap.HelperOperation('WB_plain', opCode)
WB_plain.addInstuctionVar(('result', 'BIT<32>'))
WB_plain.addUserInstructionElement('rd')

# Write back of the result of most operations, expecially ALUs;
# such operations also modify the PSR
opCode = cxx_writer.writer_code.Code("""
rd = result;
PSR = (PSR & 0xff0fffff) | (PSRbp & 0x00f00000);
""")
WB_icc = trap.HelperOperation('WB_icc', opCode)
WB_icc.addInstuctionVar(('result', 'BIT<32>'))
WB_icc.addUserInstructionElement('rd')

# Write back of the result of most operations, expecially ALUs;
# such operations also modify the PSR
opCode = cxx_writer.writer_code.Code("""
if(!temp_V){
    rd = result;
    PSR = (PSR & 0xff0fffff) | (PSRbp & 0x00f00000);
}
""")
WB_icctv = trap.HelperOperation('WB_icctv', opCode)
WB_icctv.addInstuctionVar(('result', 'BIT<32>'))
WB_icctv.addInstuctionVar(('temp_V', 'BIT<1>'))
WB_icctv.addUserInstructionElement('rd')

# Write back of the result of mutiplication operations
# which modify the ICC conditions codes and the Y register
opCode = cxx_writer.writer_code.Code("""
rd = result;
PSR = (PSR & 0xff0fffff) | (PSRbp & 0x00f00000);
Y = Ybp;
""")
WB_yicc = trap.HelperOperation('WB_yicc', opCode)
WB_yicc.addInstuctionVar(('result', 'BIT<32>'))
WB_yicc.addUserInstructionElement('rd')

# Write back of the result of MAC operations
# which modify the ICC conditions codes, the Y register, and ASR[18]
opCode = cxx_writer.writer_code.Code("""
rd = result;
PSR = (PSR & 0xff0fffff) | (PSRbp & 0x00f00000);
Y = Ybp;
ASR[18] = ASR18bp;
""")
WB_yiccasr = trap.HelperOperation('WB_yiccasr', opCode)
WB_yiccasr.addInstuctionVar(('result', 'BIT<32>'))
WB_yiccasr.addUserInstructionElement('rd')

# Write back of the result of MAC operations
# which modify the Y register, and ASR[18]
opCode = cxx_writer.writer_code.Code("""
rd = result;
Y = Ybp;
ASR[18] = ASR18bp;
""")
WB_yasr = trap.HelperOperation('WB_yasr', opCode)
WB_yasr.addInstuctionVar(('result', 'BIT<32>'))
WB_yasr.addUserInstructionElement('rd')

# Write back of the normal of mutiplication operations
# which modify the Y register
opCode = cxx_writer.writer_code.Code("""
rd = result;
Y = Ybp;
""")
WB_y = trap.HelperOperation('WB_y', opCode)
WB_y.addInstuctionVar(('result', 'BIT<32>'))
WB_y.addUserInstructionElement('rd')

# Modification of the Integer Condition Codes of the Processor Status Register
# after an logical operation or after the multiply operation
opCode = cxx_writer.writer_code.Code("""
PSRbp[key_ICC_n] = ((result & 0x80000000) >> 31);
PSRbp[key_ICC_z] = (result == 0);
PSRbp[key_ICC_v] = 0;
PSRbp[key_ICC_c] = 0;
""")
ICC_writeLogic = trap.HelperOperation('ICC_writeLogic', opCode)
ICC_writeLogic.addInstuctionVar(('result', 'BIT<32>'))

# Modification of the Integer Condition Codes of the Processor Status Register
# after an addition operation
opCode = cxx_writer.writer_code.Code("""
PSRbp[key_ICC_n] = ((result & 0x80000000) >> 31);
PSRbp[key_ICC_z] = (result == 0);
PSRbp[key_ICC_v] = ((unsigned int)((rs1_op & rs2_op & (~result)) | ((~rs1_op) & (~rs2_op) & result))) >> 31;
PSRbp[key_ICC_c] = ((unsigned int)((rs1_op & rs2_op) | ((rs1_op | rs2_op) & (~result)))) >> 31;
""")
ICC_writeAdd = trap.HelperOperation('ICC_writeAdd', opCode)
ICC_writeAdd.addInstuctionVar(('result', 'BIT<32>'))
ICC_writeAdd.addInstuctionVar(('rs1_op', 'BIT<32>'))
ICC_writeAdd.addInstuctionVar(('rs2_op', 'BIT<32>'))

# Modification of the Integer Condition Codes of the Processor Status Register
# after a tagged addition operation
opCode = cxx_writer.writer_code.Code("""
PSRbp[key_ICC_n] = ((result & 0x80000000) >> 31);
PSRbp[key_ICC_z] = (result == 0);
PSRbp[key_ICC_v] = temp_V;
PSRbp[key_ICC_c] = ((unsigned int)((rs1_op & rs2_op) | ((rs1_op | rs2_op) & (~result)))) >> 31;
""")
ICC_writeTAdd = trap.HelperOperation('ICC_writeTAdd', opCode)
ICC_writeTAdd.addInstuctionVar(('result', 'BIT<32>'))
ICC_writeTAdd.addInstuctionVar(('temp_V', 'BIT<1>'))
ICC_writeTAdd.addInstuctionVar(('rs1_op', 'BIT<32>'))
ICC_writeTAdd.addInstuctionVar(('rs2_op', 'BIT<32>'))

# Modification of the Integer Condition Codes of the Processor Status Register
# after a division operation
opCode = cxx_writer.writer_code.Code("""
PSRbp[key_ICC_n] = ((result & 0x80000000) >> 31);
PSRbp[key_ICC_z] = (result == 0);
PSRbp[key_ICC_v] = temp_V;
PSRbp[key_ICC_c] = 0;
""")
ICC_writeDiv = trap.HelperOperation('ICC_writeDiv', opCode)
ICC_writeDiv.addInstuctionVar(('result', 'BIT<32>'))
ICC_writeDiv.addInstuctionVar(('temp_V', 'BIT<1>'))
ICC_writeDiv.addInstuctionVar(('rs1_op', 'BIT<32>'))
ICC_writeDiv.addInstuctionVar(('rs2_op', 'BIT<32>'))

# Modification of the Integer Condition Codes of the Processor Status Register
# after a tagged addition operation
opCode = cxx_writer.writer_code.Code("""
if(!temp_V){
    PSRbp[key_ICC_n] = ((result & 0x80000000) >> 31);
    PSRbp[key_ICC_z] = (result == 0);
    PSRbp[key_ICC_v] = 0;
    PSRbp[key_ICC_c] = ((unsigned int)((rs1_op & rs2_op) | ((rs1_op | rs2_op) & (~result)))) >> 31;
}
""")
ICC_writeTVAdd = trap.HelperOperation('ICC_writeTVAdd', opCode)
ICC_writeTVAdd.addInstuctionVar(('result', 'BIT<32>'))
ICC_writeTVAdd.addInstuctionVar(('temp_V', 'BIT<1>'))
ICC_writeTVAdd.addInstuctionVar(('rs1_op', 'BIT<32>'))
ICC_writeTVAdd.addInstuctionVar(('rs2_op', 'BIT<32>'))

# Modification of the Integer Condition Codes of the Processor Status Register
# after a subtraction operation
opCode = cxx_writer.writer_code.Code("""
PSRbp[key_ICC_n] = ((result & 0x80000000) >> 31);
PSRbp[key_ICC_z] = (result == 0);
PSRbp[key_ICC_v] = ((unsigned int)((rs1_op & (~rs2_op) & (~result)) | ((~rs1_op) & rs2_op & result))) >> 31;
PSRbp[key_ICC_c] = ((unsigned int)(((~rs1_op) & rs2_op) | (((~rs1_op) | rs2_op) & result))) >> 31;
""")
ICC_writeSub = trap.HelperOperation('ICC_writeSub', opCode)
ICC_writeSub.addInstuctionVar(('result', 'BIT<32>'))
ICC_writeSub.addInstuctionVar(('rs1_op', 'BIT<32>'))
ICC_writeSub.addInstuctionVar(('rs2_op', 'BIT<32>'))

# Modification of the Integer Condition Codes of the Processor Status Register
# after a tagged subtraction operation
opCode = cxx_writer.writer_code.Code("""
PSRbp[key_ICC_n] = ((result & 0x80000000) >> 31);
PSRbp[key_ICC_z] = (result == 0);
PSRbp[key_ICC_v] = temp_V;
PSRbp[key_ICC_c] = ((unsigned int)(((~rs1_op) & rs2_op) | (((~rs1_op) | rs2_op) & result))) >> 31;
""")
ICC_writeTSub = trap.HelperOperation('ICC_writeTSub', opCode)
ICC_writeTSub.addInstuctionVar(('result', 'BIT<32>'))
ICC_writeTSub.addInstuctionVar(('temp_V', 'BIT<1>'))
ICC_writeTSub.addInstuctionVar(('rs1_op', 'BIT<32>'))
ICC_writeTSub.addInstuctionVar(('rs2_op', 'BIT<32>'))

# Modification of the Integer Condition Codes of the Processor Status Register
# after a tagged subtraction operation
opCode = cxx_writer.writer_code.Code("""
if(!temp_V){
    PSRbp[key_ICC_n] = ((result & 0x80000000) >> 31);
    PSRbp[key_ICC_z] = (result == 0);
    PSRbp[key_ICC_v] = temp_V;
    PSRbp[key_ICC_c] = ((unsigned int)(((~rs1_op) & rs2_op) | (((~rs1_op) | rs2_op) & result))) >> 31;
}
""")
ICC_writeTVSub = trap.HelperOperation('ICC_writeTVSub', opCode)
ICC_writeTVSub.addInstuctionVar(('result', 'BIT<32>'))
ICC_writeTVSub.addInstuctionVar(('temp_V', 'BIT<1>'))
ICC_writeTVSub.addInstuctionVar(('rs1_op', 'BIT<32>'))
ICC_writeTVSub.addInstuctionVar(('rs2_op', 'BIT<32>'))
