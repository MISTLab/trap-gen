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

import cxx_writer

def getGetIRQInstr(self, model, trace, namespace):
    from pipelineWriter import hasCheckHazard
    instructionType = cxx_writer.writer_code.Type('Instruction', 'instructions.hpp')
    emptyBody = cxx_writer.writer_code.Code('')

    IRQInstrClasses = []

    for irq in self.irqs:
        IRQInstrElements = []

        # now I have to go over the behavior of this interrupt and create, like for the instructions,
        # the behavior for the different pipeline stages
        if not model.startswith('acc'):
            behaviorCode = 'this->totalInstrCycles = 0;\n'
        userDefineBehavior = ''
        for pipeStage in self.pipes:
            if model.startswith('acc'):
                behaviorCode = 'this->stageCycles = 0;\n'
                userDefineBehavior = ''
            if irq.operation.has_key(pipeStage.name):
                userDefineBehavior += str(irq.operation[pipeStage.name])
                if model.startswith('acc'):
                    # now I have to take all the resources and create a define which
                    # renames such resources so that their usage can be transparent
                    # to the developer
                    for reg in self.regs + self.regBanks + self.aliasRegs + self.aliasRegBanks:
                        behaviorCode += '#define ' + reg.name + ' ' + reg.name + '_' + pipeStage.name + '\n'
                    behaviorCode += '\n'

                behaviorCode += userDefineBehavior

                if model.startswith('acc'):
                    for reg in self.regs + self.regBanks + self.aliasRegs + self.aliasRegBanks:
                        behaviorCode += '#undef ' + reg.name + '\n'
            if model.startswith('acc'):
                behaviorCode += 'return this->stageCycles;\n\n'
                registerType = cxx_writer.writer_code.Type('Register')
                unlockQueueType = cxx_writer.writer_code.TemplateType('std::map', ['unsigned int', cxx_writer.writer_code.TemplateType('std::vector', [registerType.makePointer()], 'vector')], 'map')
                unlockQueueParam = cxx_writer.writer_code.Parameter('unlockQueue', unlockQueueType.makeRef())
                behaviorBody = cxx_writer.writer_code.Code(behaviorCode)
                behaviorDecl = cxx_writer.writer_code.Method('behavior_' + pipeStage.name, behaviorBody, cxx_writer.writer_code.uintType, 'pu', [unlockQueueParam])
                IRQInstrElements.append(behaviorDecl)
        if not model.startswith('acc'):
            behaviorCode += 'return this->totalInstrCycles;'
            behaviorBody = cxx_writer.writer_code.Code(behaviorCode)
            behaviorDecl = cxx_writer.writer_code.Method('behavior', behaviorBody, cxx_writer.writer_code.uintType, 'pu')
            IRQInstrElements.append(behaviorDecl)

        # Standard Instruction methods, there is not much to do since the IRQ instruction does nothing special
        from procWriter import baseInstrInitElement
        replicateBody = cxx_writer.writer_code.Code('return new IRQ_' + irq.name + '_Instruction(' + baseInstrInitElement + ', this->' + irq.name + ');')
        replicateDecl = cxx_writer.writer_code.Method('replicate', replicateBody, instructionType.makePointer(), 'pu', noException = True, const = True)
        IRQInstrElements.append(replicateDecl)
        setparamsParam = cxx_writer.writer_code.Parameter('bitString', self.bitSizes[1].makeRef().makeConst())
        setparamsDecl = cxx_writer.writer_code.Method('setParams', emptyBody, cxx_writer.writer_code.voidType, 'pu', [setparamsParam], noException = True)
        IRQInstrElements.append(setparamsDecl)
        getIstructionNameBody = cxx_writer.writer_code.Code('return \"IRQ' + irq.name + 'Instruction\";')
        getIstructionNameDecl = cxx_writer.writer_code.Method('getInstructionName', getIstructionNameBody, cxx_writer.writer_code.stringType, 'pu', noException = True, const = True)
        IRQInstrElements.append(getIstructionNameDecl)
        getMnemonicBody = cxx_writer.writer_code.Code('return \"irq_' + irq.name + '\";')
        getMnemonicDecl = cxx_writer.writer_code.Method('getMnemonic', getMnemonicBody, cxx_writer.writer_code.stringType, 'pu', noException = True, const = True)
        IRQInstrElements.append(getMnemonicDecl)
        getIdBody = cxx_writer.writer_code.Code('return (unsigned int)-1;')
        getIdDecl = cxx_writer.writer_code.Method('getId', getIdBody, cxx_writer.writer_code.uintType, 'pu', noException = True, const = True)
        IRQInstrElements.append(getIdDecl)

        # Now we have all the methods related to data hazards detection and management:
        # TODO: is an implementation needed for the IRQ instruction?
        if model.startswith('acc'):
            if hasCheckHazard:
                for pipeStage in self.pipes:
                    checkHazardDecl = cxx_writer.writer_code.Method('checkHazard_' + pipeStage.name, emptyBody, cxx_writer.writer_code.boolType, 'pu')
                    IRQInstrElements.append(checkHazardDecl)
                    lockDecl = cxx_writer.writer_code.Method('lockRegs_' + pipeStage.name, emptyBody, cxx_writer.writer_code.voidType, 'pu')
                    IRQInstrElements.append(lockDecl)
                unlockHazard = False
                for pipeStage in self.pipes:
                    if pipeStage.checkHazard:
                        unlockHazard = True
                    if unlockHazard:
                        getUnlockDecl = cxx_writer.writer_code.Method('getUnlock_' + pipeStage.name, emptyBody, cxx_writer.writer_code.voidType, 'pu', [unlockQueueParam])
                        IRQInstrElements.append(getUnlockDecl)

            printBusyRegsDecl = cxx_writer.writer_code.Method('printBusyRegs', cxx_writer.writer_code.Code('return "";'), cxx_writer.writer_code.stringType, 'pu')
            IRQInstrElements.append(printBusyRegsDecl)


        # Here I add a method to specify the value of the received interrupt and the related attribute
        from isa import resolveBitType
        irqWidthType = resolveBitType('BIT<' + str(irq.portWidth) + '>')
        IRQAttribute = cxx_writer.writer_code.Attribute(irq.name, irqWidthType.makeRef(), 'pu')
        IRQInstrElements.append(IRQAttribute)
        irqParams = [cxx_writer.writer_code.Parameter(irq.name, irqWidthType.makeRef())]
        irqInit = [irq.name + '(' + irq.name + ')']
        InterruptValueParam = cxx_writer.writer_code.Parameter('interruptValue', irqWidthType.makeRef().makeConst())
        setInterruptValueBody = cxx_writer.writer_code.Code('this->' + irq.name + ' = interruptValue;')
        setInterruptValueDecl = cxx_writer.writer_code.Method('setInterruptValue', setInterruptValueBody, cxx_writer.writer_code.voidType, 'pu', [InterruptValueParam], noException = True, inline = True)
        IRQInstrElements.append(setInterruptValueDecl)

        # Finally I can declare the IRQ class for this specific IRQ
        from procWriter import baseInstrInitElement
        from isaWriter import baseInstrConstrParams
        publicConstr = cxx_writer.writer_code.Constructor(emptyBody, 'pu', baseInstrConstrParams + irqParams, ['Instruction(' + baseInstrInitElement + ')'] + irqInit)
        IRQInstrClass = cxx_writer.writer_code.ClassDeclaration('IRQ_' + irq.name + '_Instruction', IRQInstrElements, [instructionType], namespaces = [namespace])
        IRQInstrClass.addConstructor(publicConstr)
        publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
        IRQInstrClass.addDestructor(publicDestr)
        IRQInstrClasses.append(IRQInstrClass)

    return IRQInstrClasses
