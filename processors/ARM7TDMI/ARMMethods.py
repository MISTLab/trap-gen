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
# This is the code which is called before fecthing each instruction
# to check if an interrupt has been raised and take the appropriate action
# TODO: I do not like this way: I would like to make it more automatic
IRQOperation = cxx_writer.Code("""
if(FIQ.read() && (CPSR["F"] == 0)){
    triggerFIQ();
    flush();
}
if(IRQ.read() && (CPSR["I"] == 0)){
    triggerIRQ();
    flush();
}
""")
# Now I also have to implement the triggerFIQ() and triggerIRQ()
# operations
opCode = cxx_writer.Code("""
//Save LR_irq
LR_IRQ = PC;
//Save the current PSR
SPSR[1] = CPSR;
//I switch the register bank (i.e. I update the
//alias)
REGS[13].updateAlias(RB[21]);
REGS[14].updateAlias(RB[22]);
//Create the new PSR
CPSR = (CPSR & 0xFFFFFFD0) | 0x00000092;
//Finally I update the PC
#ifdef CYCLE_ACCURATE
PC = 0x18;
#else
PC = 0x20;
#endif
""")
triggerIRQ = trap.HelperMethod('triggerIRQ', opCode)
opCode = cxx_writer.Code("""
//Save LR_irq
LR_FIQ = PC;
//Save the current PSR
SPSR[0] = CPSR;
//I switch the register bank (i.e. I update the
//alias)
REGS[8].updateAlias(RB[23]);
REGS[9].updateAlias(RB[24]);
REGS[10].updateAlias(RB[25]);
REGS[11].updateAlias(RB[26]);
REGS[12].updateAlias(RB[27]);
REGS[13].updateAlias(RB[28]);
REGS[14].updateAlias(RB[29]);
//Create the new PSR
CPSR = (CPSR & 0xFFFFFFD0) | 0x000000D1;
//Finally I update the PC
#ifdef CYCLE_ACCURATE
PC = 0x1C;
#else
PC = 0x24;
#endif
""")
triggerFIQ = trap.HelperMethod('triggerFIQ', opCode)
# *******
# Here we define some helper methods, which are not directly part of the
# instructions, but which can be called by the instruction body
# *******
opCode = cxx_writer.Code("""
shifted = toShift >> shift_amm;
//Controlling the sign extensions
if((toShift & 0x80000000) != 0){
    shifted |= (((unsigned int)0xFFFFFFFF) << (32 - shift_amm));
}
else{
    shifted &= (((unsigned int)0xFFFFFFFF) >> shift_amm);
}
return shifted;
""")
AShiftRight_method = trap.HelperMethod('ArithmeticShiftRight', opCode)
AShiftRight_method.setSignature(('BIT<32>'), [cxx_writer.Parameter('shift_amm', cxx_writer.uintType), ('toShift', 'BIT<32>')])
AShiftRight_method.addVariable(('shifted', 'BIT<32>'))

opCode = cxx_writer.Code("""
//value which must be glued to the left of the shifted quantity
toGlue = toRotate & (((unsigned int)0xFFFFFFFF) >> (32 - rotate_amm));
rotated = ((toRotate >> rotate_amm) & (((unsigned int)0xFFFFFFFF) >> rotate_amm));
toGlue <<= (32 - rotate_amm);
return (toGlue | rotated);
""")
RotateRight_method = trap.HelperMethod('RotateRight', opCode)
RotateRight_method.setSignature(('BIT<32>'), [cxx_writer.Parameter('rotate_amm', cxx_writer.uintType), ('toRotate', 'BIT<32>')])
RotateRight_method.addVariable(('rotated', 'BIT<32>'))
RotateRight_method.addVariable(('toGlue', 'BIT<32>'))

opCode = cxx_writer.Code("""
unsigned int curMode = CPSR["mode"];
switch(curMode){
    case 0x1:{
        //I'm in FIQ mode
        CPSR = SPSR[0];
        break;}
    case 0x2:{
        //I'm in IRQ mode
        CPSR = SPSR[1];
        break;}
    case 0x3:{
        //I'm in SVC mode
        CPSR = SPSR[2];
        break;}
    case 0x7:{
        //I'm in ABT mode
        CPSR = SPSR[3];
        break;}
    case 0xB:{
        //I'm in UND mode
        CPSR = SPSR[4];
        break;}
    default:{
        THROW_EXCEPTION("Unable to restore the PSR when starting from user or supervisor mode");
        break;}
}
updateAlias(curMode, CPSR["mode"]);
""")
restoreSPSR_method = trap.HelperMethod('restoreSPSR', opCode)
opCode = cxx_writer.Code("""
switch(toMode){
    case 0x0:
    case 0xF:{
        //User or System mode
        REGS[13].updateAlias(RB[13]);
        REGS[14].updateAlias(RB[14]);
    break;}
    case 0x2:{
        //IRQ mode
        REGS[13].updateAlias(RB[21]);
        REGS[14].updateAlias(RB[22]);
    break;}
    case 0x1:{
        //FIQ mode
        REGS[8].updateAlias(RB[23]);
        REGS[9].updateAlias(RB[24]);
        REGS[10].updateAlias(RB[25]);
        REGS[11].updateAlias(RB[26]);
        REGS[12].updateAlias(RB[27]);
        REGS[13].updateAlias(RB[28]);
        REGS[14].updateAlias(RB[29]);
    break;}
    case 0x3:{
        //SVC mode
        REGS[13].updateAlias(RB[15]);
        REGS[14].updateAlias(RB[16]);
    break;}
    case 0x7:{
        //ABT mode
        REGS[13].updateAlias(RB[17]);
        REGS[14].updateAlias(RB[18]);
    break;}
    case 0xB:{
        //UND mode
        REGS[13].updateAlias(RB[19]);
        REGS[14].updateAlias(RB[20]);
    break;}
    default:{
        THROW_EXCEPTION("Not valid toMode " << toMode << " when changing the registers")
    break;}
}

if(fromMode == 0x1 && toMode != 0x1){
    REGS[8].updateAlias(RB[8]);
    REGS[9].updateAlias(RB[9]);
    REGS[10].updateAlias(RB[10]);
    REGS[11].updateAlias(RB[11]);
    REGS[12].updateAlias(RB[12]);
}
""")
updateAlias_method = trap.HelperMethod('updateAlias', opCode)
updateAlias_method.setSignature(parameters = [cxx_writer.Parameter('fromMode', cxx_writer.uintType), cxx_writer.Parameter('toMode', cxx_writer.uintType)])

# Behavior that checks for the condition code and consiquently flushes
# the current instruction or procedes with its execution
opCode = cxx_writer.Code("""
if(cond != 0xE){
    // Of course the previous if is redundand, the case would be enough, but
    // since cond == 0xE is the most common situation, treating it in a particular way
    // makes the code a bit faster
    switch(cond){
        case 0x0:{
            // EQ
            if (CPSR["Z"] == 0x0){
                flush();
            }
            break;
        }
        case 0x1:{
            // NE
            if (CPSR["Z"] != 0x0){
                flush();
            }
            break;
        }
        case 0x2:{
            // CS/HS
            if (CPSR["C"] == 0x0){
                flush();
            }
            break;
        }
        case 0x3:{
            // CC/LO
            if (CPSR["C"] != 0x0){
                flush();
            }
            break;
        }
        case 0x4:{
            // MI
            if (CPSR["N"] == 0x0){
                flush();
            }
            break;
        }
        case 0x5:{
            // PL
            if (CPSR["N"] != 0x0){
                flush();
            }
            break;
        }
        case 0x6:{
            // VS
            if (CPSR["V"] == 0x0){
                flush();
            }
            break;
        }
        case 0x7:{
            // VC
            if (CPSR["V"] != 0x0){
                flush();
            }
            break;
        }
        case 0x8:{
            // HI
            if ((CPSR & 0x60000000) != 0x20000000){
                flush();
            }
            break;
        }
        case 0x9:{
            // LS
            if ((CPSR & 0x60000000) == 0x20000000){
                flush();
            }
            break;
        }
        case 0xA:{
            // GE
            if (CPSR["V"] != CPSR.N){
                flush();
            }
            break;
        }
        case 0xB:{
            // LT
            if (CPSR["V"] == CPSR["N"]){
                flush();
            }
            break;
        }
        case 0xC:{
            // GT
            if ((CPSR["Z"] != 0x0) || (CPSR["V"] != CPSR["N"])){
                flush();
            }
            break;
        }
        case 0xD:{
            // LE
            if ((CPSR["Z"] == 0x0) && (CPSR["V"] == CPSR["N"])){
                flush();
            }
            break;
        }
        case 0xE:{
            // AL
            break;
        }
        default:{
            // Not recognized condition code
            THROW_EXCEPTION("Unpredictable condition code: " << cond);
            break;
        }
    }
}
""")
condCheckOp = trap.HelperOperation('condition_check', opCode)
condCheckOp.addUserInstructionElement('cond')
# Now I define the behavior for the shift immediate operation: all data processing instructions with
# an immediate value and a shift use it
opCode = cxx_writer.Code("""
if(shift_op == 0 && shift_amm == 0){
    operand = rm;
    carry = (CPSR["C"] != 0);
}
else{
#ifndef NDEBUG
    if ((shift_amm < 0) || (shift_amm > 31)){
        THROW_EXCEPTION("Shift ammunt " << shift_amm << " not valid");
    }
#endif
    switch(shift_op) {
        case 0x0:{
            // Logical shift left
            #ifndef NDEBUG
            if (shift_amm == 0){
                THROW_EXCEPTION("Shift ammunt " << shift_amm << " and logical shift left not valid: this situation should have already been cheched");
            }
            else{
            #endif
                operand = rm << shift_amm;
                carry = ((rm & (0x01 << (32 - shift_amm))) != 0);
            #ifndef NDEBUG
            }
            #endif
            break;}
        case 0x1:{
            // Logical shift right
            if (shift_amm == 0){
                //Which means shift of 32 bits, the whole number.
                operand = 0;
                carry = ((rm & 0x80000000) != 0);
            }
            else {
                operand = rm >> shift_amm;
                carry = ((rm & (0x01 << (shift_amm - 1))) != 0);
            }
            break;}
        case 0x2:{
            // Arithmetic shift right
            if (shift_amm == 0){
                //Which means shift of 32 bits
                if ((rm & 0x80000000) == 0x0){
                    operand = 0;
                    carry = false;
                }
                else{
                    operand = 0xFFFFFFFF;
                    carry = true;
                }
            }
            else {
                operand = ArithmeticShiftRight(shift_amm, rm);
                carry = ((rm & (0x01 << (shift_amm - 1))) != 0);
            }
            break;}
        case 0x3:{
            // Rotate right
            if (shift_amm == 0){
                //Rotate rigth with extend
                operand = (rm >> 1) | ((CPSR["C"]) << 31);
                carry = ((rm & 0x00000001) != 0);
            }
            else {
                operand = RotateRight(shift_amm, rm);
                carry = ((rm & (0x01 << (shift_amm - 1))) != 0);
            }
            break;}
        default:{
            THROW_EXCEPTION("Shift operation " << shift_op << " not valid");
            break;}
    }
}
""")
DPI_shift_imm_Op = trap.HelperOperation('DPI_shift_imm', opCode)
DPI_shift_imm_Op.addInstuctionVar(('operand', 'BIT<32>'))
DPI_shift_imm_Op.addInstuctionVar(('carry', 'BIT<1>'))
DPI_shift_imm_Op.addUserInstructionElement('shift_amm')
DPI_shift_imm_Op.addUserInstructionElement('rm')
DPI_shift_imm_Op.addUserInstructionElement('shift_op')
# Now I define the behavior for the shift register operation: all data processing instructions with
# an register value and a shift use it
opCode = cxx_writer.Code("""
unsigned int shift_amm = rs & 0x000000FF;
switch(shift_op) {
    case 0x0:{
        // Logical shift left
        if(shift_amm == 0){
            operand = rm;
            carry = (CPSR["C"] != 0);
        }
        else if (shift_amm < 32){
            operand = rm << shift_amm;
            carry = ((rm & (0x01 << (32 - shift_amm))) != 0);
        }
        else if (shift_amm == 32){
            operand = 0;
            carry = ((rm & 0x00000001) != 0);
        }
        else if (shift_amm > 32){
            operand = 0;
            carry = false;
        }
        break;}
    case 0x1:{
        // Logical shift right
        if(shift_amm == 0){
            operand = rm;
            carry = (CPSR["C"] != 0);
        }
        else if (shift_amm < 32){
            operand = rm >> shift_amm;
            carry = ((rm & (0x01 << shift_amm - 1)) != 0);
        }
        else if (shift_amm == 32){
            operand = 0;
            carry = ((rm & 0x80000000) != 0);
        }
        else if (shift_amm > 32){
            operand = 0;
            carry = 0;
        }
        break;}
    case 0x2:{
        // Arithmetic shift right
        if(shift_amm == 0){
            operand = rm;
            carry = (CPSR["C"] != 0);
        }
        else if (shift_amm < 32){
            operand = ArithmeticShiftRight(shift_amm, rm);
            carry = ((rm & (0x01 << (shift_amm - 1)))!= 0);
        }
        else{
            // shiftamount >= 32
            carry = ((rm & 0x80000000) != 0);
            if (!carry){
                operand = 0x0;
            }
            else{
                operand = 0xFFFFFFFF;
            }
        }
        break;}
    case 0x3:{
        // Rotate right
        if(shift_amm == 0){
            operand = rm;
            carry = (CPSR["C"] != 0);
        }
        else if((shift_amm & 0x0000001F) == 0){
            operand = rm;
            carry = ((rm & 0x80000000) != 0);
        }
        else{
            operand = RotateRight(shift_amm & 0x0000001F, rm);
            carry = (rm & (0x01 << ((shift_amm & 0x0000001F) -1)) != 0);
        }
        break;}
    default:{
        THROW_EXCEPTION("Shift operation " << shift_op << " not valid");
        break;}
}
//Ok, this operation is such that it stall the pipeline for 1 stage;
//note how the stall is not performed at this exact moment, but when
//all the operations of the stage have ended
stall(1);
""")
DPI_reg_shift_Op = trap.HelperOperation('DPI_reg_shift', opCode)
DPI_reg_shift_Op.addInstuctionVar(('operand', 'BIT<32>'))
DPI_reg_shift_Op.addInstuctionVar(('carry', 'BIT<1>'))
DPI_reg_shift_Op.addUserInstructionElement('shift_amm')
DPI_reg_shift_Op.addUserInstructionElement('rm')
DPI_reg_shift_Op.addUserInstructionElement('shift_op')
DPI_reg_shift_Op.addUserInstructionElement('rs')
# Now I define the behavior for the rotate immediate operation: all data processing instructions with
# an immediate value and a rotation use it
opCode = cxx_writer.Code("""
if (rotate == 0){
    operand = 0;
    carry = (CPSR["C"] != 0);
}
else{
    operand = RotateRight(rotate*2, immediate);
    carry = (operand & 0x80000000) != 0 ;
}
""")
DPI_imm_Op = trap.HelperOperation('DPI_imm', opCode)
DPI_imm_Op.addInstuctionVar(('operand', 'BIT<32>'))
DPI_imm_Op.addInstuctionVar(('carry', 'BIT<1>'))
DPI_imm_Op.addUserInstructionElement('rotate')
DPI_imm_Op.addUserInstructionElement('immediate')
# Now I define the behavior used by most of the data processing operations
# for the update of the program status register
# TODO: check carry and overflow operations; in particular, are they valid for
# each operation or there is a version for the addition and one for the
# subraction ops?
opCode = cxx_writer.Code("""
if (s == 0x1){
    if(rd_bit == 15){
        // In case the destination register is the program counter,
        // I have to switch to the saved program status register
        restoreSPSR();
    }
    else{
        //Here I have to normally update the flags
        // N flag if the results is negative
        CPSR["N"] = ((result & 0x0000000080000000LL) != 0);
        //Update flag Z if the result is 0
        CPSR["Z"] = (result == 0);
        //Update the C flag if a carry occurred in the operation
        CPSR["C"] = (((((rn >> 31) & 0x01) ^ ((operand >> 31) & 0x01)) ^ (result & 0x0000000100000000LL)) != 0);
        //Update the V flag if an overflow occurred in the operation
        CPSR["V"] = ((rn & operand & ~result & 0x0000000080000000LL) != 0 ||
                     (~rn & ~operand & result & 0x0000000080000000LL) != 0);
    }
}
""")
UpdatePSR = trap.HelperOperation('UpdatePSR', opCode)
UpdatePSR.addInstuctionVar(('result', 'BIT<64>'))
DPI_imm_Op.addUserInstructionElement('s')
DPI_imm_Op.addUserInstructionElement('rn')
DPI_imm_Op.addInstuctionVar(('operand', 'BIT<32>'))
# In case the program counter is the updated register I have
# to increment the latency of the operation
opCode = cxx_writer.Code("""
if(rd_bit == 15){
    #ifndef CYCLE_ACCURATE
    //In case I'm executing the functional model I have to increment the
    //program counter to take into account the fact the I do not
    //have the pipeline
    PC += 8;
    #endif
    //In case the destination register is the program counter I have to
    //specify that I have a latency of two clock cycles
    stall(2);
}
""")
UpdatePC = trap.HelperOperation('UpdatePC', opCode, False)
UpdatePC.addUserInstructionElement('rd')
