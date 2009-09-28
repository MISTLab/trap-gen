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

from procWriter import getInstrIssueCodePipe, getInterruptCode, computeFetchCode, computeCurrentPC, fetchWithCacheCode

from procWriter import hash_map_include

hasCheckHazard = False
wbStage = None
chStage = None

def getGetPipelineStages(self, trace, model, namespace):
    global hasCheckHazard
    global wbStage
    global chStage
    from procWriter import resourceType
    # Returns the code implementing the class representing a pipeline stage
    pipeCodeElements = []
    pipelineElements = []
    constructorCode = ''
    constructorParamsBase = []
    constructorInit = []
    baseConstructorInit = ''
    pipeType = cxx_writer.writer_code.Type('BasePipeStage')
    IntructionType = cxx_writer.writer_code.Type('Instruction', includes = ['instructions.hpp'])
    registerType = cxx_writer.writer_code.Type('Register', includes = ['registers.hpp'])

    stageEndedFlag = cxx_writer.writer_code.Attribute('stageEnded', cxx_writer.writer_code.boolType, 'pu')
    pipelineElements.append(stageEndedFlag)
    constructorCode += 'this->stageEnded = false;\n'
    stageBeginningFlag = cxx_writer.writer_code.Attribute('stageBeginning', cxx_writer.writer_code.boolType, 'pu')
    pipelineElements.append(stageBeginningFlag)
    constructorCode += 'this->stageBeginning = false;\n'
    hasToFlush = cxx_writer.writer_code.Attribute('hasToFlush', cxx_writer.writer_code.boolType, 'pu')
    pipelineElements.append(hasToFlush)
    constructorCode += 'this->hasToFlush = false;\n'
    stageEndedEvent = cxx_writer.writer_code.Attribute('stageEndedEv', cxx_writer.writer_code.sc_eventType, 'pu')
    pipelineElements.append(stageEndedEvent)
    stageBeginningEvent = cxx_writer.writer_code.Attribute('stageBeginningEv', cxx_writer.writer_code.sc_eventType, 'pro')
    pipelineElements.append(stageBeginningEvent)

    NOPIntructionType = cxx_writer.writer_code.Type('NOPInstruction', 'instructions.hpp')
    NOPinstructionsAttribute = cxx_writer.writer_code.Attribute('NOPInstrInstance', NOPIntructionType.makePointer(), 'pu')
    pipelineElements.append(NOPinstructionsAttribute)
    constructorCode += 'this->NOPInstrInstance = NULL;\n'

    # Lets declare the interrupt instructions in case we have any and we also declare the signal attribute
    for irq in self.irqs:
        IRQIntructionType = cxx_writer.writer_code.Type('IRQ_' + irq.name + '_Instruction', 'instructions.hpp')
        IRQinstructionAttribute = cxx_writer.writer_code.Attribute(irq.name + '_irqInstr', IRQIntructionType.makePointer(), 'pu')
        pipelineElements.append(IRQinstructionAttribute)
        constructorCode += 'this->' + irq.name + '_irqInstr = NULL;\n'

    latencyAttribute = cxx_writer.writer_code.Attribute('latency', cxx_writer.writer_code.sc_timeType, 'pro')
    pipelineElements.append(latencyAttribute)
    latencyParam = cxx_writer.writer_code.Parameter('latency', cxx_writer.writer_code.sc_timeType.makeRef())
    constructorParamsBase.append(latencyParam)
    constructorInit.append('latency(latency)')
    baseConstructorInit += 'latency, '

    curInstrAttr = cxx_writer.writer_code.Attribute('curInstruction', IntructionType.makePointer(), 'pu')
    pipelineElements.append(curInstrAttr)
    constructorCode += 'this->curInstruction = NULL;\n'
    nextInstrAttr = cxx_writer.writer_code.Attribute('nextInstruction', IntructionType.makePointer(), 'pu')
    pipelineElements.append(nextInstrAttr)
    constructorCode += 'this->nextInstruction = NULL;\n'

    flushCode = """this->hasToFlush = true;
    if(this->prevStage != NULL){
        this->prevStage->flush();
    }
    """
    flushBody = cxx_writer.writer_code.Code(flushCode)
    flushDecl = cxx_writer.writer_code.Method('flush', flushBody, cxx_writer.writer_code.voidType, 'pu', noException = True)
    pipelineElements.append(flushDecl)

    waitPipeBeginCode = """this->stageBeginning = true;
    this->stageBeginningEv.notify();
    """
    for i in range(0, len(self.pipes) - 1):
        waitPipeBeginCode += """if(!this->stage_""" + str(i) + """->stageBeginning){
            wait(this->stage_""" + str(i) + """->stageBeginningEv);
        }
        """
    waitPipeBeginCode += 'this->stageEnded = false;'
    returnType = cxx_writer.writer_code.voidType
    waitPipeBeginBody = cxx_writer.writer_code.Code(waitPipeBeginCode)
    waitPipeBeginDecl = cxx_writer.writer_code.Method('waitPipeBegin', waitPipeBeginBody, returnType, 'pu', noException = True)
    pipelineElements.append(waitPipeBeginDecl)

    waitPipeEndCode = """this->stageBeginning = false;
    this->stageEnded = true;
    this->stageEndedEv.notify();
    """
    for i in range(0, len(self.pipes) - 1):
        waitPipeEndCode += """if(!this->stage_""" + str(i) + """->stageEnded){
            wait(this->stage_""" + str(i) + """->stageEndedEv);
        }
        """
    returnType = cxx_writer.writer_code.voidType
    waitPipeEndBody = cxx_writer.writer_code.Code(waitPipeEndCode)
    waitPipeEndDecl = cxx_writer.writer_code.Method('waitPipeEnd', waitPipeEndBody, cxx_writer.writer_code.voidType, 'pu', noException = True)
    pipelineElements.append(waitPipeEndDecl)

    for i in range(0, len(self.pipes) - 1):
        otherStageAttr = cxx_writer.writer_code.Attribute('stage_' + str(i), pipeType.makePointer(), 'pro')
        pipelineElements.append(otherStageAttr)
        otherStageParam = cxx_writer.writer_code.Parameter('stage_' + str(i), pipeType.makePointer())
        constructorParamsBase.append(otherStageParam)
        constructorInit.append('stage_' + str(i) + '(stage_' + str(i) + ')')
        baseConstructorInit += 'stage_' + str(i) + ', '

    stageAttr = cxx_writer.writer_code.Attribute('prevStage', pipeType.makePointer(), 'pro')
    pipelineElements.append(stageAttr)
    stageAttr = cxx_writer.writer_code.Attribute('succStage', pipeType.makePointer(), 'pro')
    pipelineElements.append(stageAttr)
    unlockQueueType = cxx_writer.writer_code.TemplateType('std::map', ['unsigned int', cxx_writer.writer_code.TemplateType('std::vector', [registerType.makePointer()], 'vector')], 'map')
    unlockQueueAttr = cxx_writer.writer_code.Attribute('unlockQueue', unlockQueueType, 'pro', static = True)
    pipelineElements.append(unlockQueueAttr)
    prevStageParam = cxx_writer.writer_code.Parameter('prevStage', pipeType.makePointer(), initValue = 'NULL')
    succStageParam = cxx_writer.writer_code.Parameter('succStage', pipeType.makePointer(), initValue = 'NULL')
    constructorParamsBase.append(prevStageParam)
    constructorParamsBase.append(succStageParam)
    constructorInit.append('prevStage(prevStage)')
    constructorInit.append('succStage(succStage)')
    baseConstructorInit += 'prevStage, '
    baseConstructorInit += 'succStage, '
    pipelineDecl = cxx_writer.writer_code.ClassDeclaration('BasePipeStage', pipelineElements, namespaces = [namespace])
    constructorBody = cxx_writer.writer_code.Code(constructorCode)
    publicPipelineConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParamsBase, constructorInit)
    pipelineDecl.addConstructor(publicPipelineConstr)
    pipeCodeElements.append(pipelineDecl)

    hasCheckHazard = False
    hasWb = False
    for pipeStage in self.pipes:
        if pipeStage.checkHazard:
            if self.pipes.index(pipeStage) + 1 < len(self.pipes):
                if not self.pipes[self.pipes.index(pipeStage) + 1].endHazard:
                    hasCheckHazard = True
        if pipeStage.endHazard:
            if self.pipes.index(pipeStage) - 1 >= 0:
                if not self.pipes[self.pipes.index(pipeStage) - 1].checkHazard:
                    hasWb = True

    # Now I have to actually declare the different pipeline stages, all of them being equal a part from
    # the fecth stage which have to fetch instructions and check interrupts before calling
    # the appropriate behavior method
    checkHazardsMet = False
    wbStage = self.pipes[-1]
    chStage = self.pipes[0]
    for pipeStage in self.pipes:
        if pipeStage.wb:
            wbStage = pipeStage
        if pipeStage.checkHazard:
            chStage = pipeStage

        pipeNameParam = cxx_writer.writer_code.Parameter('pipeName', cxx_writer.writer_code.sc_module_nameType)
        curPipeElements = []
        constructorCode = ''
        constructorInit = []
        constructorParams = [pipeNameParam] + constructorParamsBase

        codeString = """this->curInstruction = this->NOPInstrInstance;
        this->nextInstruction = this->NOPInstrInstance;
        """
        if pipeStage == self.pipes[0]:
            # This is the fetch pipeline stage, I have to fetch instructions
            if self.instructionCache:
                codeString += 'template_map< ' + str(self.bitSizes[1]) + ', CacheElem >::iterator instrCacheEnd = this->instrCache.end();\n'
            codeString += 'while(true){\n'

            # Here is the code to notify start of the instruction execution
            codeString += 'this->instrExecuting = true;\n'

            codeString += """// HERE WAIT FOR BEGIN OF ALL STAGES
            this->waitPipeBegin();

            """
            codeString += 'unsigned int numCycles = 0;\n'

            # Here is the code to deal with interrupts; note one problem: if an interrupt is raised, we need to
            # deal with it in the correct stage, i.e. we need to create a special instruction reaching the correct
            # stage and dealing with it properly.
            codeString += getInterruptCode(self, pipeStage)
            # computes the correct memory and/or memory port from which fetching the instruction stream
            fetchCode = computeFetchCode(self)
            # computes the address from which the next instruction shall be fetched
            fetchAddress = computeCurrentPC(self, model)
            codeString += str(self.bitSizes[1]) + ' curPC = ' + fetchAddress + ';\n'
            # We need to fetch the instruction ... only if the cache is not used or if
            # the index of the cache is the current instruction
            if not (self.instructionCache and self.fastFetch):
                codeString += fetchCode
            if trace:
                codeString += 'std::cerr << \"Current PC: \" << std::hex << std::showbase << curPC << std::endl;\n'

            # Now lets starts the real instruction fetch: two paths are possible: the instruction buffer
            # and the normal instruction stream.
            if self.instructionCache:
                codeString += fetchWithCacheCode(self, fetchCode, trace, getInstrIssueCodePipe, hasCheckHazard, pipeStage)
            else:
                codeString += standardInstrFetch(self, trace, getInstrIssueCodePipe, hasCheckHazard, pipeStage)

            # Finally we have completed waiting for the other cycles in order to be able to go on
            # with this cycle.
            if self.irqs:
                codeString += '}\n'
            codeString += """wait((numCycles + 1)*this->latency);
            // HERE WAIT FOR END OF ALL STAGES
            this->waitPipeEnd();

            """

            # Here is the code to notify start of the instruction execution
            codeString += 'this->instrExecuting = false;\n'
            if self.systemc:
                codeString += 'this->instrEndEvent.notify();\n'

            codeString += """
            // Now I have to propagate the instruction to the next cycle if
            // the next stage has completed elaboration
            if(this->hasToFlush){
                this->curInstruction = this->NOPInstrInstance;
                this->hasToFlush = false;
            }
            this->refreshRegisters();
            this->succStage->nextInstruction = this->curInstruction;
            this->numInstructions++;
            }
            """
        else:
            # This is a normal pipeline stage

            # First of all I have to wait for the completion of the other pipeline stages before being able
            # to go on.
            codeString += """while(true){
            unsigned int numCycles = 0;
            // HERE WAIT FOR BEGIN OF ALL STAGES
            this->waitPipeBegin();

            """
            if pipeStage.checkTools:
                fetchAddress = computeCurrentPC(self, model)
                codeString += str(self.bitSizes[1]) + ' curPC = ' + fetchAddress + ';\n'
            codeString += 'this->curInstruction = this->nextInstruction;\n'
            # Now we issue the instruction, i.e. we execute its behavior related to this pipeline stage
            codeString += getInstrIssueCodePipe(self, trace, 'this->curInstruction', hasCheckHazard, pipeStage)
            # Finally I finalize the pipeline stage by synchrnonizing with the others
            codeString += """wait((numCycles + 1)*this->latency);"""
            codeString += """// flushing current stage
            if(this->curInstruction->flushPipeline){
                this->curInstruction->flushPipeline = false;
                //Now I have to flush the preceding pipeline stages
                this->prevStage->flush();
            }
            """
            codeString += """// HERE WAIT FOR END OF ALL STAGES
            this->waitPipeEnd();

            """
            if pipeStage != self.pipes[-1]:
                codeString += """// Now I have to propagate the instruction to the next cycle if
                // the next stage has completed elaboration
                if(this->hasToFlush){
                    this->curInstruction = this->NOPInstrInstance;
                    this->hasToFlush = false;
                }
                this->succStage->nextInstruction = this->curInstruction;
                """
            codeString += '}'
        if pipeStage.checkHazard:
            checkHazardsMet = True

        behaviorMethodBody = cxx_writer.writer_code.Code(codeString)
        behaviorMethodDecl = cxx_writer.writer_code.Method('behavior', behaviorMethodBody, cxx_writer.writer_code.voidType, 'pu')
        curPipeElements.append(behaviorMethodDecl)
        constructorCode += 'SC_THREAD(behavior);\n'

        IntructionType = cxx_writer.writer_code.Type('Instruction', 'instructions.hpp')
        IntructionTypePtr = IntructionType.makePointer()
        if pipeStage == self.pipes[0]:
            # I create the refreshRegisters method; note that in order to update the registers
            # I just need to access any of the instructions, for instance I use the registers
            # if the NOP instruction. I have to see if the register values are different
            # from the registers in the wb stage: in case they are I update them with these
            # values, otherwise I go over the other stages and see if there is one different
            # and I update it. For each update I also update the other pipeline regs
            codeString = ''
            for reg in self.regs:
                if not reg.name in self.regOrder.keys():
                    codeString += 'if(this->' + reg.name + ' != this->NOPInstrInstance->' + reg.name + '_' + wbStage.name + '){\n'
                    codeString += 'this->' + reg.name + ' = this->NOPInstrInstance->' + reg.name + '_' + wbStage.name + ';\n'
                    for upPipe in self.pipes:
                        if upPipe != wbStage:
                            codeString += 'this->NOPInstrInstance->' + reg.name + '_' + upPipe.name + ' = this->' + reg.name + ';\n'
                    codeString += '}\n'
                    for checkPipe in self.pipes:
                        if checkPipe != wbStage:
                            codeString += 'else if(this->' + reg.name + ' != this->NOPInstrInstance->' + reg.name + '_' + checkPipe.name + '){\n'
                            codeString += 'this->' + reg.name + ' = this->NOPInstrInstance->' + reg.name + '_' + checkPipe.name + ';\n'
                            for upPipe in self.pipes:
                                if upPipe != checkPipe:
                                    codeString += 'this->NOPInstrInstance->' + reg.name + '_' + upPipe.name + ' = this->' + reg.name + ';\n'
                            codeString += '}\n'
                else:
                    for customWBStage in self.regOrder[reg.name]:
                        if customWBStage != self.regOrder[reg.name][0]:
                            codeString += 'else '
                        codeString += 'if(this->' + reg.name + ' != this->NOPInstrInstance->' + reg.name + '_' + customWBStage + '){\n'
                        codeString += 'this->' + reg.name + ' = this->NOPInstrInstance->' + reg.name + '_' + customWBStage + ';\n'
                        for upPipe in self.pipes:
                            if upPipe != wbStage:
                                codeString += 'this->NOPInstrInstance->' + reg.name + '_' + upPipe.name + ' = this->' + reg.name + ';\n'
                        codeString += '}\n'

            for regB in self.regBanks:
                codeString += 'for(int i = 0; i < ' + str(regB.numRegs) + '; i++){\n'
                if not regB.name in self.regOrder.keys():
                    codeString += 'if(this->' + regB.name + '[i] != this->NOPInstrInstance->' + regB.name + '_' + wbStage.name + '[i]){\n'
                    codeString += 'this->' + regB.name + '[i] = this->NOPInstrInstance->' + regB.name + '_' + wbStage.name + '[i];\n'
                    for upPipe in self.pipes:
                        if upPipe != wbStage:
                            codeString += 'this->NOPInstrInstance->' + regB.name + '_' + upPipe.name + '[i] = this->' + regB.name + '[i];\n'
                    codeString += '}\n'
                    for checkPipe in self.pipes:
                        if checkPipe != wbStage:
                            codeString += 'else if(this->' + regB.name + '[i] != this->NOPInstrInstance->' + regB.name + '_' + checkPipe.name + '[i]){\n'
                            codeString += 'this->' + regB.name + '[i] = this->NOPInstrInstance->' + regB.name + '_' + checkPipe.name + '[i];\n'
                            for upPipe in self.pipes:
                                if upPipe != checkPipe:
                                    codeString += 'this->NOPInstrInstance->' + regB.name + '_' + upPipe.name + '[i] = this->' + regB.name + '[i];\n'
                            codeString += '}\n'
                else:
                    for customWBStage in self.regOrder[regB.name]:
                        if customWBStage != self.regOrder[regB.name][0]:
                            codeString += 'else '
                        codeString += 'if(this->' + regB.name + '[i] != this->NOPInstrInstance->' + regB.name + '_' + customWBStage + '){\n'
                        codeString += 'this->' + regB.name + '[i] = this->NOPInstrInstance->' + regB.name + '_' + customWBStage + ';\n'
                        for upPipe in self.pipes:
                            if upPipe != wbStage:
                                codeString += 'this->NOPInstrInstance->' + regB.name + '_' + upPipe.name + '[i] = this->' + regB.name + '[i];\n'
                        codeString += '}\n'
                codeString += '}\n'
            # Now I have to produce the code for unlocking the registers in the unlockQueue
            codeString += """
            std::map<unsigned int, std::vector<Register *> >::iterator unlockQueueIter, unlockQueueEnd;
            for(unlockQueueIter = BasePipeStage::unlockQueue.begin(), unlockQueueEnd = BasePipeStage::unlockQueue.end(); unlockQueueIter != unlockQueueEnd; unlockQueueIter++){
                std::vector<Register *>::iterator regToUnlockIter, regToUnlockEnd;
                if(unlockQueueIter->first == 0){
                    for(regToUnlockIter = unlockQueueIter->second.begin(), regToUnlockEnd = unlockQueueIter->second.end(); regToUnlockIter != regToUnlockEnd; regToUnlockIter++){
                        (*regToUnlockIter)->unlock();
                    }
                }
                else{
                    sc_time regLat = unlockQueueIter->first*this->latency;
                    for(regToUnlockIter = unlockQueueIter->second.begin(), regToUnlockEnd = unlockQueueIter->second.end(); regToUnlockIter != regToUnlockEnd; regToUnlockIter++){
                        (*regToUnlockIter)->unlock(regLat);
                    }
                }
            }
            """
            refreshRegistersBody = cxx_writer.writer_code.Code(codeString)
            refreshRegistersDecl = cxx_writer.writer_code.Method('refreshRegisters', refreshRegistersBody, cxx_writer.writer_code.voidType, 'pu')
            curPipeElements.append(refreshRegistersDecl)
            # Here I declare the references to the real processor registers which I update at the
            # end of each cycle
            for reg in self.regs:
                if reg.name != self.fetchReg[0]:
                    attribute = cxx_writer.writer_code.Attribute(reg.name, resourceType[reg.name].makeRef(), 'pu')
                    constructorParams = [cxx_writer.writer_code.Parameter(reg.name, resourceType[reg.name].makeRef())] + constructorParams
                    constructorInit.append(reg.name + '(' + reg.name + ')')
                    curPipeElements.append(attribute)
            for regB in self.regBanks:
                attribute = cxx_writer.writer_code.Attribute(regB.name, resourceType[regB.name].makeRef(), 'pu')
                constructorParams = [cxx_writer.writer_code.Parameter(regB.name, resourceType[regB.name].makeRef())] + constructorParams
                constructorInit.append(regB.name + '(' + regB.name + ')')
                curPipeElements.append(attribute)
            # I have to also instantiate the reference to the memories, in order to be able to
            # fetch instructions
            if self.memory:
                # I perform the fetch from the local memory
                memName = self.memory[0]
                memType = cxx_writer.writer_code.Type('LocalMemory', 'memory.hpp').makeRef()
            else:
                for name, isFetch  in self.tlmPorts.items():
                    if isFetch:
                        memName = name
                        memType = cxx_writer.writer_code.Type('TLMMemory', 'externalPorts.hpp').makeRef()
            constructorParams = [cxx_writer.writer_code.Parameter(memName, memType)] + constructorParams
            constructorInit.append(memName + '(' + memName + ')')
            memRefAttr = cxx_writer.writer_code.Attribute(memName, memType, 'pri')
            curPipeElements.append(memRefAttr)
            decoderAttribute = cxx_writer.writer_code.Attribute('decoder', cxx_writer.writer_code.Type('Decoder', 'decoder.hpp'), 'pu')
            curPipeElements.append(decoderAttribute)
            # I also have to add the map containig the ISA instructions to this stage
            instructionsAttribute = cxx_writer.writer_code.Attribute('INSTRUCTIONS', IntructionTypePtr.makePointer().makeRef(), 'pri')
            curPipeElements.append(instructionsAttribute)
            constructorParams = [cxx_writer.writer_code.Parameter('INSTRUCTIONS', IntructionTypePtr.makePointer().makeRef())] + constructorParams
            constructorInit.append('INSTRUCTIONS(INSTRUCTIONS)')
            fetchAttr = cxx_writer.writer_code.Attribute(self.fetchReg[0], resourceType[self.fetchReg[0]].makeRef(), 'pu')
            constructorParams = [cxx_writer.writer_code.Parameter(self.fetchReg[0], resourceType[self.fetchReg[0]].makeRef())] + constructorParams
            constructorInit.append(self.fetchReg[0] + '(' + self.fetchReg[0] + ')')
            curPipeElements.append(fetchAttr)
            numInstructions = cxx_writer.writer_code.Attribute('numInstructions', cxx_writer.writer_code.uintType.makeRef(), 'pri')
            constructorParams = [cxx_writer.writer_code.Parameter('numInstructions', cxx_writer.writer_code.uintType.makeRef())] + constructorParams
            constructorInit.append('numInstructions(numInstructions)')
            curPipeElements.append(numInstructions)
            attribute = cxx_writer.writer_code.Attribute('instrExecuting', cxx_writer.writer_code.boolType.makeRef(), 'pri')
            constructorParams = [cxx_writer.writer_code.Parameter('instrExecuting', cxx_writer.writer_code.boolType.makeRef())] + constructorParams
            constructorInit.append('instrExecuting(instrExecuting)')
            curPipeElements.append(attribute)
            attribute = cxx_writer.writer_code.Attribute('instrEndEvent', cxx_writer.writer_code.sc_eventType.makeRef(), 'pri')
            constructorParams = [cxx_writer.writer_code.Parameter('instrEndEvent', cxx_writer.writer_code.sc_eventType.makeRef())] + constructorParams
            constructorInit.append('instrEndEvent(instrEndEvent)')
            curPipeElements.append(attribute)

            for irq in self.irqs:
                from isa import resolveBitType
                irqWidthType = resolveBitType('BIT<' + str(irq.portWidth) + '>')
                IRQAttribute = cxx_writer.writer_code.Attribute(irq.name, irqWidthType.makeRef(), 'pu')
                constructorParams = [cxx_writer.writer_code.Parameter(irq.name, irqWidthType.makeRef())] + constructorParams
                constructorInit.append(irq.name + '(' + irq.name + ')')
                curPipeElements.append(IRQAttribute)
            if self.instructionCache:
                CacheElemType = cxx_writer.writer_code.Type('CacheElem')
                template_mapType = cxx_writer.writer_code.TemplateType('template_map', [self.bitSizes[1], CacheElemType], hash_map_include)
                cacheAttribute = cxx_writer.writer_code.Attribute('instrCache', template_mapType, 'pri')
                curPipeElements.append(cacheAttribute)

        if pipeStage.checkTools:
            ToolsManagerType = cxx_writer.writer_code.TemplateType('ToolsManager', [self.bitSizes[1]], 'ToolsIf.hpp')
            toolManagerAttribute = cxx_writer.writer_code.Attribute('toolManager', ToolsManagerType.makeRef(), 'pri')
            curPipeElements.append(toolManagerAttribute)
            constructorParams = [cxx_writer.writer_code.Parameter('toolManager', ToolsManagerType.makeRef())] + constructorParams
            constructorInit.append('toolManager(toolManager)')
            fetchAttr = cxx_writer.writer_code.Attribute(self.fetchReg[0], resourceType[self.fetchReg[0]].makeRef(), 'pri')
            constructorParams = [cxx_writer.writer_code.Parameter(self.fetchReg[0], resourceType[self.fetchReg[0]].makeRef())] + constructorParams
            constructorInit.append(self.fetchReg[0] + '(' + self.fetchReg[0] + ')')
            curPipeElements.append(fetchAttr)
            instructionsAttribute = cxx_writer.writer_code.Attribute('INSTRUCTIONS', IntructionTypePtr.makePointer().makeRef(), 'pri')
            constructorInit.append('INSTRUCTIONS(INSTRUCTIONS)')
            curPipeElements.append(instructionsAttribute)

        constructorInit = ['sc_module(pipeName)', 'BasePipeStage(' + baseConstructorInit[:-2] + ')'] + constructorInit
        curPipeDecl = cxx_writer.writer_code.SCModule(pipeStage.name.upper() + '_PipeStage', curPipeElements, [pipeType], namespaces = [namespace])
        constructorBody = cxx_writer.writer_code.Code(constructorCode + 'end_module();')
        publicCurPipeConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, constructorInit)
        curPipeDecl.addConstructor(publicCurPipeConstr)
        pipeCodeElements.append(curPipeDecl)

    return pipeCodeElements
