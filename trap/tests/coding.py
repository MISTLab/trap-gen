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


import unittest
import processor
import isa
import cxx_writer
import os

class TestCoding(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testComputeCoding1(self):
        # Checks that everything is ok if no ambiguity exists in the instruction encoding
        isaVar = isa.ISA()
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        dataProc_reg_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('rs', 4), ('zero', 1), ('shift_op', 2), ('one', 1), ('rm', 4)])
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        adc_shift_reg_Instr = isa.Instruction('ADC_sr', True)
        adc_shift_reg_Instr.setMachineCode(dataProc_reg_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        isaVar.addInstruction(adc_shift_imm_Instr)
        isaVar.addInstruction(adc_shift_reg_Instr)

        # Now we can compute the checks
        isaVar.computeCoding()
        self.assertEqual([None for i in range(0, 4)] + [0, 0, 0, 0, 1, 0, 1] + [None for i in range(0, 16)] + [0] + [None for i in range(0, 4)], adc_shift_imm_Instr.bitstring)
        self.assertEqual([None for i in range(0, 4)] + [0, 0, 0, 0, 1, 0, 1] + [None for i in range(0, 13)] + [0] + [None,  None] + [1] + [None for i in range(0, 4)], adc_shift_reg_Instr.bitstring)

    def testComputeCoding2(self):
        # Checks that everything is ok if no ambiguity exists in the instruction encoding
        isaVar = isa.ISA()
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('one', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('one', 1), ('rm', 4)])
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        isaVar.addInstruction(adc_shift_imm_Instr)

        # Now we can compute the checks
        isaVar.computeCoding()
        self.assertEqual([None for i in range(0, 4)] + [1, 1, 1, 0, 1, 0, 1] + [None for i in range(0, 16)] + [1] + [None for i in range(0, 4)], adc_shift_imm_Instr.bitstring)

    def testOk(self):
        # Checks that everything is ok if no ambiguity exists in the instruction encoding
        isaVar = isa.ISA()
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        ls_immOff = isa.MachineCode([('cond', 4), ('opcode', 3), ('p', 1), ('u', 1), ('b', 1), ('w', 1), ('l', 1), ('rn', 4), ('rd', 4), ('immediate', 12)])
        ls_immOff.setBitfield('opcode', [0, 1, 0])
        ls_multiple = isa.MachineCode([('cond', 4), ('opcode', 3), ('p', 1), ('u', 1), ('s', 1), ('w', 1), ('l', 1), ('rn', 4), ('reg_list', 16)])
        ls_multiple.setBitfield('opcode', [1, 0, 0])
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        secondInstr = isa.Instruction('SECOND', False)
        secondInstr .setMachineCode(ls_immOff)
        thirdInstr = isa.Instruction('THIRD', False)
        thirdInstr .setMachineCode(ls_multiple)
        isaVar.addInstruction(adc_shift_imm_Instr)
        isaVar.addInstruction(secondInstr)
        isaVar.addInstruction(thirdInstr)

        # Now we can compute the checks
        isaVar.computeCoding()
        isaVar.checkCoding()

    def testAmbiguityTwo(self):
        # Checks that an error is raised if an ambiguity exists between two instructions
        isaVar = isa.ISA()
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        ls_immOff = isa.MachineCode([('cond', 4), ('opcode', 2), ('p', 2), ('u', 1), ('b', 1), ('w', 1), ('l', 1), ('rn', 4), ('rd', 4), ('immediate', 12)])
        ls_immOff.setBitfield('opcode', [1, 0])
        ls_multiple = isa.MachineCode([('cond', 4), ('opcode', 3), ('p', 1), ('u', 1), ('s', 1), ('w', 1), ('l', 1), ('rn', 4), ('reg_list', 16)])
        ls_multiple.setBitfield('opcode', [1, 0, 0])
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        secondInstr = isa.Instruction('SECOND', False)
        secondInstr .setMachineCode(ls_immOff)
        thirdInstr = isa.Instruction('THIRD', False)
        thirdInstr .setMachineCode(ls_multiple)
        isaVar.addInstruction(adc_shift_imm_Instr)
        isaVar.addInstruction(secondInstr)
        isaVar.addInstruction(thirdInstr)

        # Now we can compute the checks
        isaVar.computeCoding()
        error = False
        try:
            isaVar.checkCoding()
        except:
            error = True
        self.assert_(error)

    def testAmbiguitySet(self):
        # Checks that an error is raised if an ambiguity exists between a set of instructions
        isaVar = isa.ISA()
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('opc', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        dataProc_imm_shift.setBitfield('opc', [1, 0, None])
        ls_immOff = isa.MachineCode([('cond', 4), ('opcode', 2), ('p', 2), ('u', 1), ('b', 1), ('w', 1), ('l', 1), ('rn', 4), ('rd', 4), ('immediate', 12)])
        ls_immOff.setBitfield('opcode', [1, 0])
        ls_multiple = isa.MachineCode([('cond', 4), ('opcode', 3), ('p', 1), ('u', 1), ('s', 1), ('w', 1), ('l', 1), ('rn', 4), ('reg_list', 16)])
        ls_multiple.setBitfield('opcode', [1, 0, 0])
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [None, None, None, None]}, 'TODO')
        secondInstr = isa.Instruction('SECOND', False)
        secondInstr .setMachineCode(ls_immOff)
        thirdInstr = isa.Instruction('THIRD', False)
        thirdInstr .setMachineCode(ls_multiple)
        isaVar.addInstruction(adc_shift_imm_Instr)
        isaVar.addInstruction(secondInstr)
        isaVar.addInstruction(thirdInstr)

        # Now we can compute the checks
        isaVar.computeCoding()
        error = False
        try:
            isaVar.checkCoding()
        except:
            error = True
        self.assert_(error)
