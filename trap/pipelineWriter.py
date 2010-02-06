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

from procWriter import getInstrIssueCodePipe, getInterruptCode, computeFetchCode, computeCurrentPC, fetchWithCacheCode, standardInstrFetch

from procWriter import hash_map_include

hasCheckHazard = False
wbStage = None
chStage = None

def getGetPipelineStages(self, trace, combinedTrace, model, namespace):
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
    constructorCode += 'this->chStalled = false;\n'
    constructorCode += 'this->stalled = false;\n'
    constructorCode += 'this->stageEnded = false;\n'
    stageBeginningFlag = cxx_writer.writer_code.Attribute('stageBeginning', cxx_writer.writer_code.boolType, 'pu')
    pipelineElements.append(stageBeginningFlag)
    constructorCode += 'this->stageBeginning = false;\n'
    hasToFlush = cxx_writer.writer_code.Attribute('hasToFlush', cxx_writer.writer_code.boolType, 'pu')
    pipelineElements.append(hasToFlush)
    constructorCode += 'this->hasToFlush = false;\n'
    stageEndedEvent = cxx_writer.writer_code.Attribute('stageEndedEv', cxx_writer.writer_code.sc_eventType, 'pu')
    pipelineElements.append(stageEndedEvent)
    stageBeginningEvent = cxx_writer.writer_code.Attribute('stageBeginningEv', cxx_writer.writer_code.sc_eventType, 'pu')
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

    for pipe in self.pipes:
        otherStageAttr = cxx_writer.writer_code.Attribute('stage_' + pipe.name, pipeType.makePointer(), 'pro')
        pipelineElements.append(otherStageAttr)
        otherStageParam = cxx_writer.writer_code.Parameter('stage_' + pipe.name, pipeType.makePointer())
        constructorParamsBase.append(otherStageParam)
        constructorInit.append('stage_' + pipe.name + '(stage_' + pipe.name + ')')
        baseConstructorInit += 'stage_' + pipe.name + ', '

    chStalledAttr = cxx_writer.writer_code.Attribute('chStalled', cxx_writer.writer_code.boolType, 'pu')
    pipelineElements.append(chStalledAttr)
    stalledAttr = cxx_writer.writer_code.Attribute('stalled', cxx_writer.writer_code.boolType, 'pu')
    pipelineElements.append(stalledAttr)
    stageAttr = cxx_writer.writer_code.Attribute('prevStage', pipeType.makePointer(), 'pu')
    pipelineElements.append(stageAttr)
    stageAttr = cxx_writer.writer_code.Attribute('succStage', pipeType.makePointer(), 'pu')
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

    # Now lets determine the stages which need a call to check hazard
    #checkHazadsStagesDecl = []
    #if hasCheckHazard:
        #for instr in self.isa.instructions.values():
            #for stageName in instr.specialInRegs.keys():
                #if not stageName in checkHazadsStagesDecl:
                    #checkHazadsStagesDecl.append(stageName)
    # Remember that all the stages preceding the the last one where we check for
    # hazards have to check if the following stages are stalled.

    # Now I have to actually declare the different pipeline stages, all of them being equal a part from
    # the fecth stage which have to fetch instructions and check interrupts before calling
    # the appropriate behavior method
    checkHazardsMet = False
    wbStage = self.pipes[-1]
    chStage = self.pipes[0]
    seenStages = 0
    for pipeStage in self.pipes:
        seenStages += 1
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
            codeString += 'unsigned int numNOPS = 0;\n'
            codeString += 'bool startMet = false;\n'
            if self.instructionCache:
                codeString += 'template_map< ' + str(self.bitSizes[1]) + ', CacheElem >::iterator instrCacheEnd = this->instrCache.end();\n\n'
            codeString += 'while(true){\n'

            # Here is the code to notify start of the instruction execution
            codeString += 'this->instrExecuting = true;\n'

            codeString += 'unsigned int numCycles = 0;\n'
            if hasCheckHazard:
                codeString += 'if(!this->chStalled){\n'

            codeString += '\n// HERE WAIT FOR BEGIN OF ALL STAGES\nthis->waitPipeBegin();\n'

            # Here is the code to deal with interrupts; note one problem: if an interrupt is raised, we need to
            # deal with it in the correct stage, i.e. we need to create a special instruction reaching the correct
            # stage and dealing with it properly.
            codeString += getInterruptCode(self, trace, pipeStage)
            # computes the correct memory and/or memory port from which fetching the instruction stream
            fetchCode = computeFetchCode(self)
            # computes the address from which the next instruction shall be fetched
            fetchAddress = computeCurrentPC(self, model)
            codeString += str(self.bitSizes[1]) + ' curPC = ' + fetchAddress + ';\n'

            # Here is the code for updating cycle counts
            codeString += """if(!startMet && curPC == this->profStartAddr){
                this->profTimeStart = sc_time_stamp();
            }
            if(startMet && curPC == this->profEndAddr){
                this->profTimeEnd = sc_time_stamp();
            }
            """

            # Now lets start with the code necessary to check the tools, to see if they need
            # the pipeline to be empty before being able to procede with execution
            codeString += """
                #ifndef DISABLE_TOOLS
                // code necessary to check the tools, to see if they need
                // the pipeline to be empty before being able to procede with execution
                if(this->toolManager.emptyPipeline(curPC)){
                    numNOPS++;
                }
                else{
                    numNOPS = 0;
                }
                if(numNOPS > 0 && numNOPS < """ + str(len(self.pipes)) + """){
                    this->curInstruction = this->NOPInstrInstance;
                """
            if trace and not combinedTrace:
                codeString += 'std::cerr << \"PC: \" << std::hex << std::showbase << curPC << " propagating NOP because tools need it" << std::endl;\n'
            codeString += """}
                else{
                    numNOPS = 0;
                #endif
                    //Ok, either the pipeline is empty or there is not tool which needs the pipeline
                    //to be empty: I can procede with the execution
            """

            # Lets start with the code for the instruction queue
            codeString += """#ifdef ENABLE_HISTORY
            HistoryInstrType instrQueueElem;
            if(this->historyEnabled){
                instrQueueElem.cycle = (unsigned int)(sc_time_stamp()/this->latency);
                instrQueueElem.address = curPC;
            }
            #endif
            """

            # We need to fetch the instruction ... only if the cache is not used or if
            # the index of the cache is the current instruction
            if not (self.instructionCache and self.fastFetch):
                codeString += fetchCode
            if trace and not combinedTrace:
                codeString += 'std::cerr << \"Fetching PC: \" << std::hex << std::showbase << curPC << std::endl;\n'

            # Now lets starts the real instruction fetch: two paths are possible: the instruction buffer
            # and the normal instruction stream.
            if self.instructionCache:
                codeString += fetchWithCacheCode(self, fetchCode, trace, combinedTrace, getInstrIssueCodePipe, hasCheckHazard, pipeStage)
            else:
                codeString += standardInstrFetch(self, trace, combinedTrace, getInstrIssueCodePipe, hasCheckHazard, pipeStage)

            # Lets finish with the code for the instruction queue: I just still have to
            # check if it is time to save to file the instruction queue
            codeString += """#ifdef ENABLE_HISTORY
            if(this->historyEnabled){
                // First I add the new element to the queue
                this->instHistoryQueue.push_back(instrQueueElem);
                //Now, in case the queue dump file has been specified, I have to check if I need to save it
                if(this->histFile){
                    this->undumpedHistElems++;
                    if(undumpedHistElems == this->instHistoryQueue.capacity()){
                        boost::circular_buffer<HistoryInstrType>::const_iterator beg, end;
                        for(beg = this->instHistoryQueue.begin(), end = this->instHistoryQueue.end(); beg != end; beg++){
                            this->histFile << beg->toStr() << std::endl;
                        }
                        this->undumpedHistElems = 0;
                    }
                }
            }
            #endif
            """

            # Finally we have completed waiting for the other cycles in order to be able to go on
            # with this cycle.
            codeString += """this->numInstructions++;
                #ifndef DISABLE_TOOLS
                }
                #endif
            """
            if self.irqs:
                codeString += '}\n'
            codeString += """wait((numCycles + 1)*this->latency);
            // HERE WAIT FOR END OF ALL STAGES
            this->waitPipeEnd();

            """

            codeString += """
            // Now I have to propagate the instruction to the next cycle if
            // the next stage has completed elaboration
            if(this->hasToFlush){
                if(this->curInstruction->toDestroy){
                    delete this->curInstruction;
                }
                else{
                    this->curInstruction->inPipeline = false;
                }
                this->curInstruction = this->NOPInstrInstance;
                this->nextInstruction = this->NOPInstrInstance;
                this->hasToFlush = false;
            }
            """
            codeString += 'this->succStage->nextInstruction = this->curInstruction;\n'
            if hasCheckHazard:
                codeString += """}
                else{
                    //The current stage is not doing anything since one of the following stages
                    //is blocked to a data hazard.
                    this->waitPipeBegin();
                    //Note that I need to return controll to the scheduler, otherwise
                    //I will be impossible to procede, this thread will always execute
                    wait(this->latency);
                    this->waitPipeEnd();
                    if(this->hasToFlush){
                        if(this->curInstruction->toDestroy){
                            delete this->curInstruction;
                        }
                        else{
                            this->curInstruction->inPipeline = false;
                        }
                        this->curInstruction = this->NOPInstrInstance;
                        this->nextInstruction = this->NOPInstrInstance;
                        this->hasToFlush = false;
                    }
                }
            """
            # Here is the code to notify start of the instruction execution
            codeString += """this->refreshRegisters();
                this->instrExecuting = false;
                this->instrEndEvent.notify();
            """
            # Now I have to insert the code for checking the presence of hazards;
            # in particular I have to see if the instruction to be executed next in
            # the checkHazardsStage will lock
            if hasCheckHazard:
                codeString += 'Instruction * succToCheck = this->'
                for pipeStageTemp in self.pipes:
                    if pipeStageTemp.checkHazard:
                        break
                    else:
                        codeString += 'succStage->'
                codeString += 'nextInstruction;\n'
                codeString += 'if(!succToCheck->checkHazard_' + pipeStageTemp.name + '()){\n'
                codeTemp = 'this->'
                for pipeStageTemp in self.pipes:
                    codeString += codeTemp + 'chStalled = true;\n'
                    codeTemp += 'succStage->'
                    if pipeStageTemp.checkHazard:
                        break
                codeString += '}\nelse{\n'
                codeTemp = 'this->'
                for pipeStageTemp in self.pipes:
                    codeString += codeTemp + 'chStalled = false;\n'
                    codeTemp += 'succStage->'
                    if pipeStageTemp.checkHazard:
                        break
                codeString += '}\n'
            if trace and not combinedTrace:
                codeString += 'std::cerr << \"---------------------------------------------------------------\" << std::endl << std::endl;\n'
            codeString += '}\n'
        else:
            # This is a normal pipeline stage

            # First of all I have to wait for the completion of the other pipeline stages before being able
            # to go on.
            if hasCheckHazard and not checkHazardsMet:
                codeString += 'Instruction * nextStageInstruction;\n'
            codeString += """while(true){
            unsigned int numCycles = 0;
            bool flushAnnulled = false;

            // HERE WAIT FOR BEGIN OF ALL STAGES
            this->waitPipeBegin();

            this->curInstruction = this->nextInstruction;
            """

            if hasCheckHazard and not checkHazardsMet:
                codeString += 'if(!this->chStalled){\n'

            if trace and not combinedTrace:
                codeString += 'std::cerr << \"Stage ' + pipeStage.name + ' instruction at PC = \" << std::hex << std::showbase << this->curInstruction->fetchPC << std::endl;\n'

            #if hasCheckHazard and pipeStage.name in checkHazadsStagesDecl:
            if hasCheckHazard and pipeStage.checkHazard:
                codeString += 'this->curInstruction->lockRegs_' + pipeStage.name + '();\n'

            if trace and combinedTrace and pipeStage == self.pipes[-1]:
                codeString += 'if(this->curInstruction != this->NOPInstrInstance){\n'
                codeString += 'std::cerr << \"Current PC: \" << std::hex << std::showbase << this->curInstruction->fetchPC << std::endl;\n'
                codeString += '}\n'
            # Now we issue the instruction, i.e. we execute its behavior related to this pipeline stage
            codeString += getInstrIssueCodePipe(self, trace, combinedTrace, 'this->curInstruction', hasCheckHazard, pipeStage)
            # Finally I finalize the pipeline stage by synchrnonizing with the others
            codeString += 'wait((numCycles + 1)*this->latency);\n'
            codeString += """// flushing current stage
            if(this->curInstruction->flushPipeline || flushAnnulled){
                this->curInstruction->flushPipeline = false;
                //Now I have to flush the preceding pipeline stages
                this->prevStage->flush();
            }
            """

            if not hasCheckHazard or checkHazardsMet:
                codeString += """// HERE WAIT FOR END OF ALL STAGES
                this->waitPipeEnd();

                """

            if pipeStage != self.pipes[-1]:
                codeString += """if(this->hasToFlush){
                        if(this->curInstruction->toDestroy){
                            delete this->curInstruction;
                        }
                        else{
                            this->curInstruction->inPipeline = false;
                        }
                        // First of all I have to free any used resource in case there are any
                        this->curInstruction = this->NOPInstrInstance;
                        this->nextInstruction = this->NOPInstrInstance;
                        this->hasToFlush = false;
                    }
                """
                if hasCheckHazard and not checkHazardsMet:
                    codeString += 'nextStageInstruction = this->curInstruction;\n'

            if pipeStage == self.pipes[-1]:
                # Here I have to check if it is the case of destroying the instruction
                codeString += 'if(this->curInstruction->toDestroy){\n'
                codeString += 'delete this->curInstruction;\n'
                codeString += '}\n'
                codeString += 'else{\n'
                codeString += 'this->curInstruction->inPipeline = false;\n'
                codeString += '}\n'
            if hasCheckHazard and not checkHazardsMet:
                codeString += """}
                else{
                    //The current stage is not doing anything since one of the following stages
                    //is blocked to a data hazard.
                    //Note that I need to return controll to the scheduler, otherwise
                    //I will be impossible to procede, this thread will always execute
                    wait(this->latency);
                """
                if trace and hasCheckHazard and pipeStage.checkHazard and not combinedTrace:
                    codeString += """std::cerr << "Stage: """ + pipeStage.name + """ - Instruction " << this->curInstruction->getInstructionName() << " Mnemonic = " << this->curInstruction->getMnemonic() << " at PC = " << std::hex << std::showbase << this->curInstruction->fetchPC << " stalled on a data hazard" << std::endl;
                    std::cerr << "Stalled registers: " << this->curInstruction->printBusyRegs() << std::endl << std::endl;
                    """
                codeString += """if(this->hasToFlush){
                        if(this->curInstruction->toDestroy){
                            delete this->curInstruction;
                        }
                        else{
                            this->curInstruction->inPipeline = false;
                        }
                        // First of all I have to free any used resource in case there are any
                        this->curInstruction = this->NOPInstrInstance;
                        this->nextInstruction = this->NOPInstrInstance;
                        this->hasToFlush = false;
                    }
                    nextStageInstruction = this->NOPInstrInstance;
                }
                """
            if hasCheckHazard and not checkHazardsMet:
                codeString += """// HERE WAIT FOR END OF ALL STAGES
                this->waitPipeEnd();

                """
            if pipeStage != self.pipes[-1]:
                if checkHazardsMet:
                    codeString += 'this->succStage->nextInstruction = this->curInstruction;\n'
                else:
                    codeString += 'this->succStage->nextInstruction = nextStageInstruction;\n'
            codeString += '}\n'
        if pipeStage.checkHazard:
            checkHazardsMet = True

        behaviorMethodBody = cxx_writer.writer_code.Code(codeString)
        behaviorMethodDecl = cxx_writer.writer_code.Method('behavior', behaviorMethodBody, cxx_writer.writer_code.voidType, 'pu')
        curPipeElements.append(behaviorMethodDecl)
        constructorCode += 'SC_THREAD(behavior);\n'

        waitPipeBeginCode = """this->stageBeginning = true;
        this->stageBeginningEv.notify();
        """
        for pipeStageInner in self.pipes:
            if pipeStageInner != pipeStage:
                waitPipeBeginCode += """if(!this->stage_""" + pipeStageInner.name + """->stageBeginning){
                    wait(this->stage_""" + pipeStageInner.name + """->stageBeginningEv);
                }
                """
        waitPipeBeginCode += 'this->stageEnded = false;'
        waitPipeBeginBody = cxx_writer.writer_code.Code(waitPipeBeginCode)
        waitPipeBeginDecl = cxx_writer.writer_code.Method('waitPipeBegin', waitPipeBeginBody, cxx_writer.writer_code.voidType, 'pri', noException = True)
        curPipeElements.append(waitPipeBeginDecl)

        waitPipeEndCode = """this->stageBeginning = false;
        this->stageEnded = true;
        this->stageEndedEv.notify();
        """
        for pipeStageInner in self.pipes:
            if pipeStageInner != pipeStage:
                waitPipeEndCode += """if(!this->stage_""" + pipeStageInner.name + """->stageEnded){
                    wait(this->stage_""" + pipeStageInner.name + """->stageEndedEv);
                }
                """
        waitPipeEndBody = cxx_writer.writer_code.Code(waitPipeEndCode)
        waitPipeEndDecl = cxx_writer.writer_code.Method('waitPipeEnd', waitPipeEndBody, cxx_writer.writer_code.voidType, 'pri', noException = True)
        curPipeElements.append(waitPipeEndDecl)

        IntructionType = cxx_writer.writer_code.Type('Instruction', 'instructions.hpp')
        IntructionTypePtr = IntructionType.makePointer()

        pipelineStageMap = {}
        notCheckStages = []
        checkHazardsStageMet = False
        for curPipeMap in self.pipes:
            pipelineStageMap[curPipeMap.name] = curPipeMap
            if checkHazardsStageMet:
                notCheckStages.append(curPipeMap.name)
            if curPipeMap.checkHazard:
                checkHazardsStageMet = True

        if pipeStage == self.pipes[0]:
            # I create the refreshRegisters method; note that in order to update the registers
            # i simply have to call the "propagate" method; I also have to deal with the update of the alias
            # by manually moving the pointer to the pipeline register from one stage alias to
            # the other to update the alias
            codeString = '// Now we update the registers to propagate the values in the pipeline\n'
            for reg in self.regs:
                codeString += 'if(this->' + reg.name + '.hasToPropagate){\n'
                ########
                if trace and not combinedTrace:
                    codeString += 'std::cerr << "Propagating register ' + reg.name + '" << std::endl;\n'
                ########
                codeString += 'this->' + reg.name + '.propagate();\n'
                codeString += '}\n'
            for regB in self.regBanks:
                codeString += 'for(int i = 0; i < ' + str(regB.numRegs) + '; i++){\n'
                codeString += 'if(this->' + regB.name + '[i].hasToPropagate){\n'
                ########
                if trace and not combinedTrace:
                    codeString += 'std::cerr << "Propagating register ' + regB.name + '[" << std::dec << i << "]" << std::endl;\n'
                ########
                codeString += 'this->' + regB.name + '[i].propagate();\n'
                codeString += '}\n}\n'
            # Now lets procede to the update of the alias: for each stage alias I have to copy the reference
            # of the general pipeline register from one stage to the other
            codeString += '\n//Here we update the aliases, so that what they point to is updated in the pipeline\n'
            for i in reversed(range(0, len(self.pipes) -1)):
                for alias in self.aliasRegs:
                    if not alias.isFixed:
                        codeString += 'if(this->' + alias.name + '_' + self.pipes[i + 1].name + '.getPipeReg() != this->' + alias.name + '_' + self.pipes[i].name + '.getPipeReg()){\n'
                        if trace and not combinedTrace:
                            codeString += 'std::cerr << "Updating alias ' + alias.name + '_' + self.pipes[i + 1].name + '" << std::endl;\n'
                        codeString += 'this->' + alias.name + '_' + self.pipes[i + 1].name + '.propagateAlias(*(this->' + alias.name + '_' + self.pipes[i].name + '.getPipeReg()));\n'
                        codeString += '}\n'
                for aliasB in self.aliasRegBanks:
                    checkContiguous = True
                    for j in range(0, len(aliasB.fixedIndices) - 1):
                        if aliasB.fixedIndices[j] + 1 != aliasB.fixedIndices[j + 1]:
                            checkContiguous = False
                            break
                    if checkContiguous:
                        if aliasB.fixedIndices[0] > 0:
                            if aliasB.checkGroup:
                                codeString += 'if(this->' + aliasB.name + '_' + self.pipes[i + 1].name + '[0].getPipeReg() != this->' + aliasB.name + '_' + self.pipes[i].name + '[0].getPipeReg()){\n'
                            codeString += 'for(int i = 0; i < ' + str(aliasB.fixedIndices[-1]) + '; i++){\n'
                            if not aliasB.checkGroup:
                                codeString += 'if(this->' + aliasB.name + '_' + self.pipes[i + 1].name + '[i].getPipeReg() != this->' + aliasB.name + '_' + self.pipes[i].name + '[i].getPipeReg()){\n'
                            if trace and not combinedTrace:
                                codeString += 'std::cerr << "Updating alias ' + aliasB.name + '_' + self.pipes[i + 1].name + '[" << i << "]" << std::endl;\n'
                            codeString += 'this->' + aliasB.name + '_' + self.pipes[i + 1].name + '[i].propagateAlias(*(this->' + aliasB.name + '_' + self.pipes[i].name + '[i].getPipeReg()));\n'
                            codeString += '}\n'
                            codeString += '}\n'
                        if aliasB.fixedIndices[-1] + 1 < aliasB.numRegs:
                            if aliasB.checkGroup:
                                codeString += 'if(this->' + aliasB.name + '_' + self.pipes[i + 1].name + '[' + str(aliasB.fixedIndices[-1] + 1) + '].getPipeReg() != this->' + aliasB.name + '_' + self.pipes[i].name + '[' + str(aliasB.fixedIndices[-1] + 1) + '].getPipeReg()){\n'
                            codeString += 'for(int i = ' + str(aliasB.fixedIndices[-1] + 1) + '; i < ' + str(aliasB.numRegs) + '; i++){\n'
                            if not aliasB.checkGroup:
                                codeString += 'if(this->' + aliasB.name + '_' + self.pipes[i + 1].name + '[i].getPipeReg() != this->' + aliasB.name + '_' + self.pipes[i].name + '[i].getPipeReg()){\n'
                            if trace and not combinedTrace:
                                codeString += 'std::cerr << "Updating alias ' + aliasB.name + '_' + self.pipes[i + 1].name + '[" << i << "]" << std::endl;\n'
                            codeString += 'this->' + aliasB.name + '_' + self.pipes[i + 1].name + '[i].propagateAlias(*(this->' + aliasB.name + '_' + self.pipes[i].name + '[i].getPipeReg()));\n'
                            codeString += '}\n'
                            codeString += '}\n'
                    else:
                        for j in range(0, aliasB.numRegs):
                            if not j in aliasB.fixedIndices:
                                codeString += 'if(this->' + aliasB.name + '_' + self.pipes[i + 1].name + '[' + str(j) + '].getPipeReg() != this->' + aliasB.name + '_' + self.pipes[i].name + '[' + str(j) + '].getPipeReg()){\n'
                                if trace and not combinedTrace:
                                    codeString += 'std::cerr << "Updating alias ' + aliasB.name + '_' + self.pipes[i + 1].name + '[" << ' + str(i) + ' << "]" << std::endl;\n'
                                codeString += 'this->' + aliasB.name + '_' + self.pipes[i + 1].name + '[' + str(j) + '].propagateAlias(*(this->' + aliasB.name + '_' + self.pipes[i].name + '[' + str(j) + '].getPipeReg()));\n'
                                codeString += '}\n'
            # Now I have to produce the code for unlocking the registers in the unlockQueue
            codeString += """
            // Finally registers are unlocked, so that stalls due to data hazards can be resolved
            std::map<unsigned int, std::vector<Register *> >::iterator unlockQueueIter, unlockQueueEnd;
            for(unlockQueueIter = BasePipeStage::unlockQueue.begin(), unlockQueueEnd = BasePipeStage::unlockQueue.end(); unlockQueueIter != unlockQueueEnd; unlockQueueIter++){
                std::vector<Register *>::iterator regToUnlockIter, regToUnlockEnd;
                if(unlockQueueIter->first == 0){
                    for(regToUnlockIter = unlockQueueIter->second.begin(), regToUnlockEnd = unlockQueueIter->second.end(); regToUnlockIter != regToUnlockEnd; regToUnlockIter++){
                        (*regToUnlockIter)->unlock();
                    }
                }
                else{
                    for(regToUnlockIter = unlockQueueIter->second.begin(), regToUnlockEnd = unlockQueueIter->second.end(); regToUnlockIter != regToUnlockEnd; regToUnlockIter++){
                        (*regToUnlockIter)->unlock(unlockQueueIter->first);
                    }
                }
                unlockQueueIter->second.clear();
            }
            """
            refreshRegistersBody = cxx_writer.writer_code.Code(codeString)
            refreshRegistersDecl = cxx_writer.writer_code.Method('refreshRegisters', refreshRegistersBody, cxx_writer.writer_code.voidType, 'pri', noException = True)
            curPipeElements.append(refreshRegistersDecl)
            # Here I declare the references to the pipeline registers and to the alias
            pipeRegisterType = cxx_writer.writer_code.Type('PipelineRegister', 'registers.hpp')
            for reg in self.regs:
                if self.fetchReg[0] != reg.name:
                    attribute = cxx_writer.writer_code.Attribute(reg.name, pipeRegisterType.makeRef(), 'pri')
                    constructorParams = [cxx_writer.writer_code.Parameter(reg.name, pipeRegisterType.makeRef())] + constructorParams
                    constructorInit.append(reg.name + '(' + reg.name + ')')
                    curPipeElements.append(attribute)
            for regB in self.regBanks:
                attribute = cxx_writer.writer_code.Attribute(regB.name, pipeRegisterType.makePointer(), 'pri')
                constructorParams = [cxx_writer.writer_code.Parameter(regB.name, pipeRegisterType.makePointer())] + constructorParams
                constructorInit.append(regB.name + '(' + regB.name + ')')
                curPipeElements.append(attribute)
            aliasType = cxx_writer.writer_code.Type('Alias', 'alias.hpp')
            for pipeStageInner in self.pipes:
                for alias in self.aliasRegs:
                    attribute = cxx_writer.writer_code.Attribute(alias.name + '_' + pipeStageInner.name, aliasType.makeRef(), 'pri')
                    constructorParams = [cxx_writer.writer_code.Parameter(alias.name + '_' + pipeStageInner.name, aliasType.makeRef())] + constructorParams
                    constructorInit.append(alias.name + '_' + pipeStageInner.name + '(' + alias.name + '_' + pipeStageInner.name + ')')
                    curPipeElements.append(attribute)
                for aliasB in self.aliasRegBanks:
                    attribute = cxx_writer.writer_code.Attribute(aliasB.name + '_' + pipeStageInner.name, aliasType.makePointer(), 'pri')
                    constructorParams = [cxx_writer.writer_code.Parameter(aliasB.name + '_' + pipeStageInner.name, aliasType.makePointer())] + constructorParams
                    constructorInit.append(aliasB.name + '_' + pipeStageInner.name + '(' + aliasB.name + '_' + pipeStageInner.name + ')')
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
            # fetch register;
            regsNames = [i.name for i in self.regBanks + self.regs]
            fetchRegType = resourceType[self.fetchReg[0]]
            if self.fetchReg[0] in regsNames:
                fetchRegType = pipeRegisterType
            fetchAttr = cxx_writer.writer_code.Attribute(self.fetchReg[0], fetchRegType.makeRef(), 'pri')
            constructorParams = [cxx_writer.writer_code.Parameter(self.fetchReg[0], fetchRegType.makeRef())] + constructorParams
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
                IRQAttribute = cxx_writer.writer_code.Attribute(irq.name, irqWidthType.makeRef(), 'pri')
                constructorParams = [cxx_writer.writer_code.Parameter(irq.name, irqWidthType.makeRef())] + constructorParams
                constructorInit.append(irq.name + '(' + irq.name + ')')
                curPipeElements.append(IRQAttribute)
            if self.instructionCache:
                CacheElemType = cxx_writer.writer_code.Type('CacheElem')
                template_mapType = cxx_writer.writer_code.TemplateType('template_map', [self.bitSizes[1], CacheElemType], hash_map_include)
                cacheAttribute = cxx_writer.writer_code.Attribute('instrCache', template_mapType, 'pri')
                curPipeElements.append(cacheAttribute)

            # The fetch stage also contains the tools manager
            ToolsManagerType = cxx_writer.writer_code.TemplateType('ToolsManager', [self.bitSizes[1]], 'ToolsIf.hpp')
            toolManagerAttribute = cxx_writer.writer_code.Attribute('toolManager', ToolsManagerType.makeRef(), 'pri')
            curPipeElements.append(toolManagerAttribute)
            constructorParams = [cxx_writer.writer_code.Parameter('toolManager', ToolsManagerType.makeRef())] + constructorParams
            constructorInit.append('toolManager(toolManager)')
            # Lets finally declare the attributes and constructor parameters for counting the cycles in a specified time
            # frame
            profilingTimeStartAttribute = cxx_writer.writer_code.Attribute('profTimeStart', cxx_writer.writer_code.sc_timeRefType, 'pu')
            curPipeElements.append(profilingTimeStartAttribute)
            constructorParams = [cxx_writer.writer_code.Parameter('profTimeStart', cxx_writer.writer_code.sc_timeRefType)] + constructorParams
            constructorInit.append('profTimeStart(profTimeStart)')
            profilingTimeEndAttribute = cxx_writer.writer_code.Attribute('profTimeEnd', cxx_writer.writer_code.sc_timeRefType, 'pu')
            curPipeElements.append(profilingTimeEndAttribute)
            constructorParams = [cxx_writer.writer_code.Parameter('profTimeEnd', cxx_writer.writer_code.sc_timeRefType)] + constructorParams
            constructorInit.append('profTimeEnd(profTimeEnd)')
            profilingAddrStartAttribute = cxx_writer.writer_code.Attribute('profStartAddr', self.bitSizes[1], 'pu')
            curPipeElements.append(profilingAddrStartAttribute)
            constructorCode += 'this->profStartAddr = (' + str(self.bitSizes[1]) + ')-1;\n'
            profilingAddrEndAttribute = cxx_writer.writer_code.Attribute('profEndAddr', self.bitSizes[1], 'pu')
            constructorCode += 'this->profEndAddr = (' + str(self.bitSizes[1]) + ')-1;\n'
            curPipeElements.append(profilingAddrEndAttribute)
            # Here are the attributes for the instruction history queue
            instrQueueFileAttribute = cxx_writer.writer_code.Attribute('histFile', cxx_writer.writer_code.ofstreamType, 'pu')
            curPipeElements.append(instrQueueFileAttribute)
            historyEnabledAttribute = cxx_writer.writer_code.Attribute('historyEnabled', cxx_writer.writer_code.boolType, 'pu')
            curPipeElements.append(historyEnabledAttribute)
            constructorCode += 'this->historyEnabled = false;\n'
            instrHistType = cxx_writer.writer_code.Type('HistoryInstrType', 'instructionBase.hpp')
            histQueueType = cxx_writer.writer_code.TemplateType('boost::circular_buffer', [instrHistType], 'boost/circular_buffer.hpp')
            instHistoryQueueAttribute = cxx_writer.writer_code.Attribute('instHistoryQueue', histQueueType, 'pu')
            curPipeElements.append(instHistoryQueueAttribute)
            constructorCode += 'this->instHistoryQueue.set_capacity(1000);\n'
            undumpedHistElemsAttribute = cxx_writer.writer_code.Attribute('undumpedHistElems', cxx_writer.writer_code.uintType, 'pu')
            curPipeElements.append(undumpedHistElemsAttribute)
            constructorCode += 'this->undumpedHistElems = 0;\n'
            # Now, before the processor elements is destructed I have to make sure that the history dump file is correctly closed
            destrCode = """#ifdef ENABLE_HISTORY
            if(this->historyEnabled){
                //Now, in case the queue dump file has been specified, I have to check if I need to save it
                if(this->histFile){
                    if(this->undumpedHistElems > 0){
                        boost::circular_buffer<HistoryInstrType>::const_iterator beg, end;
                        for(beg = this->instHistoryQueue.begin(), end = this->instHistoryQueue.end(); beg != end; beg++){
                            this->histFile << beg->toStr() << std::endl;
                        }
                    }
                    this->histFile.flush();
                    this->histFile.close();
                }
            }
            #endif
            """
            destructorBody = cxx_writer.writer_code.Code(destrCode)
            publicDestr = cxx_writer.writer_code.Destructor(destructorBody, 'pu')

        constructorInit = ['sc_module(pipeName)', 'BasePipeStage(' + baseConstructorInit[:-2] + ')'] + constructorInit
        curPipeDecl = cxx_writer.writer_code.SCModule(pipeStage.name.upper() + '_PipeStage', curPipeElements, [pipeType], namespaces = [namespace])
        constructorBody = cxx_writer.writer_code.Code(constructorCode + 'end_module();')
        publicCurPipeConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, constructorInit)
        if pipeStage == self.pipes[0]:
            curPipeDecl.addDestructor(publicDestr)
        curPipeDecl.addConstructor(publicCurPipeConstr)
        pipeCodeElements.append(curPipeDecl)

    return pipeCodeElements
