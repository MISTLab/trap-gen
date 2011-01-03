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
#   the Free Software Foundation; either version 3 of the License, or
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
#   (c) Luca Fossati, fossati@elet.polimi.it, fossati.l@gmail.com
#
####################################################################################


import unittest
import processor
import isa
import cxx_writer
import os

class TestRegs(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testOk(self):
        """Tests that no problems are signaled in case all the registers
        are valid and there are no references to unknown registers"""

        # First of all I build a fake processor description
        proc = processor.Processor('test', '0')
        regBank = processor.RegisterBank('RB', 30, 32)
        proc.addRegBank(regBank)
        cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 4)}
        cpsr = processor.Register('CPSR', 32, cpsrBitMask)
        cpsr.setDefaultValue(0x000000D3)
        proc.addRegister(cpsr)
        regs = processor.AliasRegBank('REGS', 16, 'RB[0-15]')
        proc.addAliasRegBank(regs)
        abi = processor.ABI('REGS[0]', 'REGS[0-3]', 'RB[15]')
        abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'CPSR': (25, 25)})
        proc.setABI(abi)
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        dataProc_imm_shift.setVarField('rn', ('REGS', 0))
        dataProc_imm_shift.setVarField('rd', ('RB', 0))
        dataProc_imm_shift.setVarField('rm', ('REGS', 0))
        isaVar = isa.ISA()
        proc.setISA(isaVar)
        opCode = cxx_writer.writer_code.Code('')
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        isaVar.addInstruction(adc_shift_imm_Instr)

        # The I call the check functions: they raise exceptions in case
        # there is a problem
        proc.checkAliases()
        proc.checkABI()
        proc.isa.checkRegisters(processor.extractRegInterval, proc.isRegExisting)

    def testAliasReg(self):
        """Tests that an exception is raised in case the alias refers to
        a non existing register
        First of all I build a fake processor description"""

        proc = processor.Processor('test', '0')
        regBank = processor.RegisterBank('RB', 30, 32)
        proc.addRegBank(regBank)
        cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 4)}
        cpsr = processor.Register('CPSR', 32, cpsrBitMask)
        cpsr.setDefaultValue(0x000000D3)
        proc.addRegister(cpsr)
        regs = processor.AliasRegBank('REGS', 16, 'RB[0-15]')
        proc.addAliasRegBank(regs)
        PC = processor.AliasRegister('PC', 'UNEXISTING')
        proc.addAliasReg(PC)
        abi = processor.ABI('REGS[0]', 'REGS[0-3]', 'RB[15]')
        abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'CPSR': (25, 25)})
        proc.setABI(abi)
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        dataProc_imm_shift.setVarField('rn', ('REGS', 0))
        dataProc_imm_shift.setVarField('rd', ('RB', 0))
        dataProc_imm_shift.setVarField('rm', ('REGS', 0))
        isaVar = isa.ISA()
        proc.setISA(isaVar)
        opCode = cxx_writer.writer_code.Code('')
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        isaVar.addInstruction(adc_shift_imm_Instr)

        # The I call the check functions: they raise exceptions in case
        # there is a problem
        foundError = False
        proc.checkABI()
        proc.isa.checkRegisters(processor.extractRegInterval, proc.isRegExisting)
        try:
            proc.checkAliases()
        except:
            foundError = True
        self.assert_(foundError)

    def testAliasRegBank(self):
        """Tests that an exception is raised in case the alias refers to
        a non existing register bank"""
        proc = processor.Processor('test', '0')
        regBank = processor.RegisterBank('RB', 30, 32)
        proc.addRegBank(regBank)
        cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 4)}
        cpsr = processor.Register('CPSR', 32, cpsrBitMask)
        cpsr.setDefaultValue(0x000000D3)
        proc.addRegister(cpsr)
        regs = processor.AliasRegBank('REGS', 16, 'RB[0-15]')
        proc.addAliasRegBank(regs)
        PC = processor.AliasRegister('PC', 'UNEXISTING[15]')
        proc.addAliasReg(PC)
        abi = processor.ABI('REGS[0]', 'REGS[0-3]', 'RB[15]')
        abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'CPSR': (25, 25)})
        proc.setABI(abi)
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        dataProc_imm_shift.setVarField('rn', ('REGS', 0))
        dataProc_imm_shift.setVarField('rd', ('RB', 0))
        dataProc_imm_shift.setVarField('rm', ('REGS', 0))
        isaVar = isa.ISA()
        proc.setISA(isaVar)
        opCode = cxx_writer.writer_code.Code('')
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        isaVar.addInstruction(adc_shift_imm_Instr)

        # The I call the check functions: they raise exceptions in case
        # there is a problem
        foundError = False
        proc.checkABI()
        proc.isa.checkRegisters(processor.extractRegInterval, proc.isRegExisting)
        try:
            proc.checkAliases()
        except:
            foundError = True
        self.assert_(foundError)

    def testAliasBankRegBank(self):
        """Tests that an exception is raised in case the alias bank refers to
        a non existing register bank"""
        proc = processor.Processor('test', '0')
        regBank = processor.RegisterBank('RB', 30, 32)
        proc.addRegBank(regBank)
        cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 4)}
        cpsr = processor.Register('CPSR', 32, cpsrBitMask)
        cpsr.setDefaultValue(0x000000D3)
        proc.addRegister(cpsr)
        regs = processor.AliasRegBank('REGS', 16, 'UNEXISTING[0-15]')
        proc.addAliasRegBank(regs)
        PC = processor.AliasRegister('PC', 'REGS[15]')
        proc.addAliasReg(PC)
        abi = processor.ABI('REGS[0]', 'REGS[0-3]', 'RB[15]')
        abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'CPSR': (25, 25)})
        proc.setABI(abi)
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        dataProc_imm_shift.setVarField('rn', ('REGS', 0))
        dataProc_imm_shift.setVarField('rd', ('RB', 0))
        dataProc_imm_shift.setVarField('rm', ('REGS', 0))
        isaVar = isa.ISA()
        proc.setISA(isaVar)
        opCode = cxx_writer.writer_code.Code('')
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        isaVar.addInstruction(adc_shift_imm_Instr)

        # The I call the check functions: they raise exceptions in case
        # there is a problem
        foundError = False
        proc.checkABI()
        proc.isa.checkRegisters(processor.extractRegInterval, proc.isRegExisting)
        try:
            proc.checkAliases()
        except:
            foundError = True
        self.assert_(foundError)

    def testAliasBankMixed(self):
        """Tests that an exception is raised in case the alias bank refers to
        a mixture of non existing registers and register banks"""
        proc = processor.Processor('test', '0')
        regBank = processor.RegisterBank('RB', 30, 32)
        proc.addRegBank(regBank)
        cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 4)}
        cpsr = processor.Register('CPSR', 32, cpsrBitMask)
        cpsr.setDefaultValue(0x000000D3)
        proc.addRegister(cpsr)
        regs = processor.AliasRegBank('REGS', 16, ('RB[0-14]', 'UNEXISTING'))
        proc.addAliasRegBank(regs)
        PC = processor.AliasRegister('PC', 'REGS[15]')
        proc.addAliasReg(PC)
        abi = processor.ABI('REGS[0]', 'REGS[0-3]', 'RB[15]')
        abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'CPSR': (25, 25)})
        proc.setABI(abi)
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        dataProc_imm_shift.setVarField('rn', ('REGS', 0))
        dataProc_imm_shift.setVarField('rd', ('RB', 0))
        dataProc_imm_shift.setVarField('rm', ('REGS', 0))
        isaVar = isa.ISA()
        proc.setISA(isaVar)
        opCode = cxx_writer.writer_code.Code('')
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        isaVar.addInstruction(adc_shift_imm_Instr)

        # The I call the check functions: they raise exceptions in case
        # there is a problem
        foundError = False
        proc.checkABI()
        proc.isa.checkRegisters(processor.extractRegInterval, proc.isRegExisting)
        try:
            proc.checkAliases()
        except:
            foundError = True
        self.assert_(foundError)

    def testABIReg(self):
        """Tests that an exception is raised in case the ABI refers to
        a non existing register"""
        proc = processor.Processor('test', '0')
        regBank = processor.RegisterBank('RB', 30, 32)
        proc.addRegBank(regBank)
        cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 4)}
        cpsr = processor.Register('CPSR', 32, cpsrBitMask)
        cpsr.setDefaultValue(0x000000D3)
        proc.addRegister(cpsr)
        regs = processor.AliasRegBank('REGS', 16, 'RB[0-15]')
        proc.addAliasRegBank(regs)
        PC = processor.AliasRegister('PC', 'REGS[15]')
        proc.addAliasReg(PC)
        abi = processor.ABI('REGS[0]', 'REGS[0-3]', 'RB[15]')
        abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'UNEXISTING': (25, 25)})
        proc.setABI(abi)
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        dataProc_imm_shift.setVarField('rn', ('REGS', 0))
        dataProc_imm_shift.setVarField('rd', ('RB', 0))
        dataProc_imm_shift.setVarField('rm', ('REGS', 0))
        isaVar = isa.ISA()
        proc.setISA(isaVar)
        opCode = cxx_writer.writer_code.Code('')
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        isaVar.addInstruction(adc_shift_imm_Instr)

        # The I call the check functions: they raise exceptions in case
        # there is a problem
        foundError = False
        proc.isa.checkRegisters(processor.extractRegInterval, proc.isRegExisting)
        proc.checkAliases()
        try:
            proc.checkABI()
        except:
            foundError = True
        self.assert_(foundError)

    def testABIArgsReg(self):
        """Tests that an exception is raised in case the ABI arguments refers to
        a non existing register"""
        proc = processor.Processor('test', '0')
        regBank = processor.RegisterBank('RB', 30, 32)
        proc.addRegBank(regBank)
        cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 4)}
        cpsr = processor.Register('CPSR', 32, cpsrBitMask)
        cpsr.setDefaultValue(0x000000D3)
        proc.addRegister(cpsr)
        regs = processor.AliasRegBank('REGS', 16, 'RB[0-15]')
        proc.addAliasRegBank(regs)
        PC = processor.AliasRegister('PC', 'REGS[15]')
        proc.addAliasReg(PC)
        abi = processor.ABI('REGS[0]', ('UNEXISTING', 'REGS[0-2]'), 'RB[15]')
        abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'CPSR': (25, 25)})
        proc.setABI(abi)
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        dataProc_imm_shift.setVarField('rn', ('REGS', 0))
        dataProc_imm_shift.setVarField('rd', ('RB', 0))
        dataProc_imm_shift.setVarField('rm', ('REGS', 0))
        isaVar = isa.ISA()
        proc.setISA(isaVar)
        opCode = cxx_writer.writer_code.Code('')
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        isaVar.addInstruction(adc_shift_imm_Instr)

        # The I call the check functions: they raise exceptions in case
        # there is a problem
        foundError = False
        proc.isa.checkRegisters(processor.extractRegInterval, proc.isRegExisting)
        proc.checkAliases()
        try:
            proc.checkABI()
        except:
            foundError = True
        self.assert_(foundError)

    def testABIArgsRegBank(self):
        """Tests that an exception is raised in case the ABI arguments refers to
        a non existing register bank"""
        proc = processor.Processor('test', '0')
        regBank = processor.RegisterBank('RB', 30, 32)
        proc.addRegBank(regBank)
        cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 4)}
        cpsr = processor.Register('CPSR', 32, cpsrBitMask)
        cpsr.setDefaultValue(0x000000D3)
        proc.addRegister(cpsr)
        regs = processor.AliasRegBank('REGS', 16, 'RB[0-15]')
        proc.addAliasRegBank(regs)
        PC = processor.AliasRegister('PC', 'REGS[15]')
        proc.addAliasReg(PC)
        abi = processor.ABI('REGS[0]', 'UNEXISTING[0-3]', 'RB[15]')
        abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'CPSR': (25, 25)})
        proc.setABI(abi)
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        dataProc_imm_shift.setVarField('rn', ('REGS', 0))
        dataProc_imm_shift.setVarField('rd', ('RB', 0))
        dataProc_imm_shift.setVarField('rm', ('REGS', 0))
        isaVar = isa.ISA()
        proc.setISA(isaVar)
        opCode = cxx_writer.writer_code.Code('')
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        isaVar.addInstruction(adc_shift_imm_Instr)

        # The I call the check functions: they raise exceptions in case
        # there is a problem
        foundError = False
        proc.isa.checkRegisters(processor.extractRegInterval, proc.isRegExisting)
        proc.checkAliases()
        try:
            proc.checkABI()
        except:
            foundError = True
        self.assert_(foundError)

    def testABIArgsMixed(self):
        """Tests that an exception is raised in case the ABI arguemnts refers to
        a mixture of non existing registers and register banks"""
        proc = processor.Processor('test', '0')
        regBank = processor.RegisterBank('RB', 30, 32)
        proc.addRegBank(regBank)
        cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 4)}
        cpsr = processor.Register('CPSR', 32, cpsrBitMask)
        cpsr.setDefaultValue(0x000000D3)
        proc.addRegister(cpsr)
        regs = processor.AliasRegBank('REGS', 16, 'RB[0-15]')
        proc.addAliasRegBank(regs)
        PC = processor.AliasRegister('PC', 'REGS[15]')
        proc.addAliasReg(PC)
        abi = processor.ABI('REGS[0]', 'REGS[40-50]', 'RB[15]')
        abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'CPSR': (25, 25)})
        proc.setABI(abi)
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        dataProc_imm_shift.setVarField('rn', ('REGS', 0))
        dataProc_imm_shift.setVarField('rd', ('RB', 0))
        dataProc_imm_shift.setVarField('rm', ('REGS', 0))
        isaVar = isa.ISA()
        proc.setISA(isaVar)
        opCode = cxx_writer.writer_code.Code('')
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        isaVar.addInstruction(adc_shift_imm_Instr)

        # The I call the check functions: they raise exceptions in case
        # there is a problem
        foundError = False
        proc.isa.checkRegisters(processor.extractRegInterval, proc.isRegExisting)
        proc.checkAliases()
        try:
            proc.checkABI()
        except:
            foundError = True
        self.assert_(foundError)

    def testRegsVariables(self):
        """Tests that an exception is raised in case the variables of
        the instructions have the same name of registers"""
        proc = processor.Processor('test', '0')
        regBank = processor.RegisterBank('RB', 30, 32)
        proc.addRegBank(regBank)
        cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 4)}
        cpsr = processor.Register('CPSR', 32, cpsrBitMask)
        cpsr.setDefaultValue(0x000000D3)
        proc.addRegister(cpsr)
        regs = processor.AliasRegBank('REGS', 16, 'RB[0-15]')
        proc.addAliasRegBank(regs)
        PC = processor.AliasRegister('PC', 'REGS[15]')
        proc.addAliasReg(PC)
        abi = processor.ABI('REGS[0]', 'REGS[0-3]', 'RB[15]')
        abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'CPSR': (25, 25)})
        proc.setABI(abi)
        dataProc_imm_shift = isa.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
        dataProc_imm_shift.setVarField('rn', ('REGS', 0))
        dataProc_imm_shift.setVarField('rd', ('RB', 0))
        dataProc_imm_shift.setVarField('rm', ('REGS', 0))
        isaVar = isa.ISA()
        proc.setISA(isaVar)
        opCode = cxx_writer.writer_code.Code('')
        adc_shift_imm_Instr = isa.Instruction('ADC_si', True)
        adc_shift_imm_Instr.setMachineCode(dataProc_imm_shift, {'opcode': [0, 1, 0, 1]}, 'TODO')
        adc_shift_imm_Instr.addVariable(('REGS', 'BIT<64>'))
        isaVar.addInstruction(adc_shift_imm_Instr)

        # The I call the check functions: they raise exceptions in case
        # there is a problem
        foundError = False
        proc.checkAliases()
        proc.checkABI()
        try:
            proc.isa.checkRegisters(processor.extractRegInterval, proc.isRegExisting)
        except:
            foundError = True
        self.assert_(foundError)
