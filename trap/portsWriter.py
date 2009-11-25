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

def getCPPExternalPorts(self, model, namespace):
    if len(self.tlmPorts) == 0:
        return None
    # creates the processor external TLM ports used for the
    # communication with the external world
    archDWordType = self.bitSizes[0]
    archWordType = self.bitSizes[1]
    archHWordType = self.bitSizes[2]
    archByteType = self.bitSizes[3]

    from procWriter import resourceType

    if self.isBigEndian:
        swapDEndianessCode = '#ifdef LITTLE_ENDIAN_BO\n'
    else:
        swapDEndianessCode = '#ifdef BIG_ENDIAN_BO\n'
    swapDEndianessCode += str(archWordType) + ' datum1 = (' + str(archWordType) + ')(datum);\nthis->swapEndianess(datum1);\n'
    swapDEndianessCode += str(archWordType) + ' datum2 = (' + str(archWordType) + ')(datum >> ' + str(self.wordSize*self.byteSize) + ');\nthis->swapEndianess(datum2);\n'
    swapDEndianessCode += 'datum = datum1 | (((' + str(archDWordType) + ')datum2) << ' + str(self.wordSize*self.byteSize) + ');\n#endif\n'

    swapEndianessCode = """//Now the code for endianess conversion: the processor is always modeled
            //with the host endianess; in case they are different, the endianess
            //is turned
            """
    if self.isBigEndian:
        swapEndianessCode += '#ifdef LITTLE_ENDIAN_BO\n'
    else:
        swapEndianessCode += '#ifdef BIG_ENDIAN_BO\n'
    swapEndianessCode += 'this->swapEndianess(datum);\n#endif\n'

    tlmPortElements = []

    MemoryToolsIfType = cxx_writer.writer_code.TemplateType('MemoryToolsIf', [str(archWordType)], 'ToolsIf.hpp')
    tlmPortElements.append(cxx_writer.writer_code.Attribute('debugger', MemoryToolsIfType.makePointer(), 'pri'))
    setDebuggerBody = cxx_writer.writer_code.Code('this->debugger = debugger;')
    tlmPortElements.append(cxx_writer.writer_code.Method('setDebugger', setDebuggerBody, cxx_writer.writer_code.voidType, 'pu', [cxx_writer.writer_code.Parameter('debugger', MemoryToolsIfType.makePointer())]))
    checkWatchPointCode = """if(this->debugger != NULL){
        this->debugger->notifyAddress(address, sizeof(datum));
    }
    """

    memIfType = cxx_writer.writer_code.Type('MemoryInterface', 'memory.hpp')
    tlm_dmiType = cxx_writer.writer_code.Type('tlm::tlm_dmi', 'tlm.h')
    TLMMemoryType = cxx_writer.writer_code.Type('TLMMemory')
    tlminitsocketType = cxx_writer.writer_code.TemplateType('tlm_utils::simple_initiator_socket', [TLMMemoryType, self.wordSize*self.byteSize], 'tlm_utils/simple_initiator_socket.h')
    payloadType = cxx_writer.writer_code.Type('tlm::tlm_generic_payload', 'tlm.h')
    phaseType = cxx_writer.writer_code.Type('tlm::tlm_phase', 'tlm.h')
    sync_enumType = cxx_writer.writer_code.Type('tlm::tlm_sync_enum', 'tlm.h')
    tlmPortInit = []
    constructorParams = []

    readMemAliasCode = ''
    writeMemAliasCode = ''
    aliasAttrs = []
    aliasParams = []
    aliasInit = []
    for alias in self.memAlias:
        aliasAttrs.append(cxx_writer.writer_code.Attribute(alias.alias, resourceType[alias.alias].makeRef(), 'pri'))
        aliasParams.append(cxx_writer.writer_code.Parameter(alias.alias, resourceType[alias.alias].makeRef()))
        aliasInit.append(alias.alias + '(' + alias.alias + ')')
        readMemAliasCode += 'if(address == ' + hex(long(alias.address)) + '){\nreturn this->' + alias.alias + ';\n}\n'
        writeMemAliasCode += 'if(address == ' + hex(long(alias.address)) + '){\n this->' + alias.alias + ' = datum;\nreturn;\n}\n'

    emptyBody = cxx_writer.writer_code.Code('')

    if model.endswith('AT'):
        # Some helper methods used only in the Approximate Timed coding style
        helperCode = """// TLM-2 backward non-blocking transport method
            // The timing annotation must be honored
            m_peq.notify(trans, phase, delay);
            return tlm::TLM_ACCEPTED;
            """
        helperBody = cxx_writer.writer_code.Code(helperCode)
        transParam = cxx_writer.writer_code.Parameter('trans', payloadType.makeRef())
        phaseParam = cxx_writer.writer_code.Parameter('phase', phaseType.makeRef())
        delayParam = cxx_writer.writer_code.Parameter('delay', cxx_writer.writer_code.sc_timeType.makeRef())
        helperDecl = cxx_writer.writer_code.Method('nb_transport_bw', helperBody, sync_enumType, 'pu', [transParam, phaseParam, delayParam], inline = True, noException = True)
        tlmPortElements.append(helperDecl)

        helperCode = """// Payload event queue callback to handle transactions from target
            // Transaction could have arrived through return path or backward path
            if (phase == tlm::END_REQ || (&trans == request_in_progress && phase == tlm::BEGIN_RESP)){
                // The end of the BEGIN_REQ phase
                request_in_progress = NULL;
                end_request_event.notify();
            }
            else if (phase == tlm::BEGIN_REQ || phase == tlm::END_RESP){
                SC_REPORT_FATAL("TLM-2", "Illegal transaction phase received by initiator");
            }

            if (phase == tlm::BEGIN_RESP){
                if (trans.is_response_error()){
                    SC_REPORT_ERROR("TLM-2", ("Transaction returned with error, response status = " + trans.get_response_string()).c_str());
                }

                // Send final phase transition to target
                tlm::tlm_phase fw_phase = tlm::END_RESP;
                sc_time delay = SC_ZERO_TIME;
                initSocket->nb_transport_fw(trans, fw_phase, delay);
                if (trans.is_response_error()){
                    SC_REPORT_ERROR("TLM-2", ("Transaction returned with error, response status = " + \
                        trans.get_response_string()).c_str());
                }
                this->end_response_event.notify(delay);
            }
            """
        helperBody = cxx_writer.writer_code.Code(helperCode)
        phaseParam = cxx_writer.writer_code.Parameter('phase', phaseType.makeRef().makeConst())
        helperDecl = cxx_writer.writer_code.Method('peq_cb', helperBody, cxx_writer.writer_code.voidType, 'pu', [transParam, phaseParam])
        tlmPortElements.append(helperDecl)

        tlmPortElements.append(cxx_writer.writer_code.Attribute('request_in_progress', payloadType.makePointer(), 'pri'))
        tlmPortElements.append(cxx_writer.writer_code.Attribute('end_request_event', cxx_writer.writer_code.sc_eventType, 'pri'))
        tlmPortElements.append(cxx_writer.writer_code.Attribute('end_response_event', cxx_writer.writer_code.sc_eventType, 'pri'))

    if model.endswith('LT'):
        readCode = """ datum = 0;
            if (this->dmi_ptr_valid){
                if(address + this->dmi_data.get_start_address() > this->dmi_data.get_end_address()){
                    SC_REPORT_ERROR("TLM-2", "Error in reading memory data through DMI: address out of bounds");
                }
                memcpy(&datum, this->dmi_data.get_dmi_ptr() - this->dmi_data.get_start_address() + address, sizeof(datum));
            """
        if not model.startswith('acc'):
            readCode += 'this->quantKeeper.inc(this->dmi_data.get_read_latency());'
        else:
            readCode += 'wait(this->dmi_data.get_read_latency());'
        readCode += """
            }
            else{
            """
        if not model.startswith('acc'):
            readCode += 'sc_time delay = this->quantKeeper.get_local_time();'
        else:
            readCode += 'sc_time delay = SC_ZERO_TIME;'
        readCode += """
                tlm::tlm_generic_payload trans;
                trans.set_address(address);
                trans.set_read();
                trans.set_data_ptr(reinterpret_cast<unsigned char*>(&datum));
                trans.set_data_length(sizeof(datum));
                trans.set_byte_enable_ptr(0);
                trans.set_dmi_allowed(false);
                trans.set_response_status( tlm::TLM_INCOMPLETE_RESPONSE );
                this->initSocket->b_transport(trans, delay);

                if(trans.is_response_error()){
                    std::string errorStr("Error from b_transport, response status = " + trans.get_response_string());
                    SC_REPORT_ERROR("TLM-2", errorStr.c_str());
                }
                if(trans.is_dmi_allowed()){
                    this->dmi_data.init();
                    this->dmi_ptr_valid = this->initSocket->get_direct_mem_ptr(trans, this->dmi_data);
                }
                //Now lets keep track of time
            """
        if not model.startswith('acc'):
            readCode += 'this->quantKeeper.set(delay);\n}\n'
        else:
            readCode += 'wait(delay);\n}\n'
    else:
        readCode = """ datum = 0;
        tlm::tlm_generic_payload trans;
        trans.set_address(address);
        trans.set_read();
        trans.set_data_ptr(reinterpret_cast<unsigned char*>(&datum));
        trans.set_data_length(sizeof(datum));
        trans.set_byte_enable_ptr(0);
        trans.set_dmi_allowed(false);
        trans.set_response_status(tlm::TLM_INCOMPLETE_RESPONSE);

        if(this->request_in_progress != NULL){
            wait(this->end_request_event);
        }
        request_in_progress = &trans;

        // Non-blocking transport call on the forward path
        sc_time delay = SC_ZERO_TIME;
        tlm::tlm_phase phase = tlm::BEGIN_REQ;
        tlm::tlm_sync_enum status;
        status = initSocket->nb_transport_fw(trans, phase, delay);

        if(trans.is_response_error()){
            std::string errorStr("Error from nb_transport_fw, response status = " + trans.get_response_string());
            SC_REPORT_ERROR("TLM-2", errorStr.c_str());
        }

        // Check value returned from nb_transport_fw
        if(status == tlm::TLM_UPDATED){
            // The timing annotation must be honored
            m_peq.notify(trans, phase, delay);
            wait(this->end_response_event);
        }
        else if(status == tlm::TLM_COMPLETED){
            // The completion of the transaction necessarily ends the BEGIN_REQ phase
            this->request_in_progress = NULL;
            // The target has terminated the transaction, I check the correctness
            if(trans.is_response_error()){
                SC_REPORT_ERROR("TLM-2", ("Transaction returned with error, response status = " + trans.get_response_string()).c_str());
            }
        }
        wait(this->end_response_event);
        """
    addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + str(archDWordType) + readCode + swapDEndianessCode + '\nreturn datum;')
    readBody.addInclude('trap_utils.hpp')
    readBody.addInclude('tlm.h')
    readDecl = cxx_writer.writer_code.Method('read_dword', readBody, archDWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + str(archWordType) + readCode + swapEndianessCode + '\nreturn datum;')
    readDecl = cxx_writer.writer_code.Method('read_word', readBody, archWordType, 'pu', [addressParam], inline = True, noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + str(archHWordType) + readCode + swapEndianessCode + '\nreturn datum;')
    readDecl = cxx_writer.writer_code.Method('read_half', readBody, archHWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + str(archByteType) + readCode + '\nreturn datum;')
    readDecl = cxx_writer.writer_code.Method('read_byte', readBody, archByteType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    writeCode = ''
    if model.endswith('LT'):
        writeCode += """if(this->dmi_ptr_valid){
                if(address + this->dmi_data.get_start_address() > this->dmi_data.get_end_address()){
                    SC_REPORT_ERROR("TLM-2", "Error in writing memory data through DMI: address out of bounds");
                }
                memcpy(this->dmi_data.get_dmi_ptr() - this->dmi_data.get_start_address() + address, &datum, sizeof(datum));
            """
        if not model.startswith('acc'):
            writeCode += 'this->quantKeeper.inc(this->dmi_data.get_write_latency());'
        else:
            writeCode += 'wait(this->dmi_data.get_write_latency());'
        writeCode += """
            }
            else{
            """
        if not model.startswith('acc'):
            writeCode += 'sc_time delay = this->quantKeeper.get_local_time();'
        else:
            writeCode += 'sc_time delay = SC_ZERO_TIME;'
        writeCode += """
                tlm::tlm_generic_payload trans;
                trans.set_address(address);
                trans.set_write();
                trans.set_data_ptr((unsigned char*)&datum);
                trans.set_data_length(sizeof(datum));
                trans.set_byte_enable_ptr(0);
                trans.set_dmi_allowed(false);
                trans.set_response_status(tlm::TLM_INCOMPLETE_RESPONSE);
                this->initSocket->b_transport(trans, delay);

                if(trans.is_response_error()){
                    std::string errorStr("Error from b_transport, response status = " + trans.get_response_string());
                    SC_REPORT_ERROR("TLM-2", errorStr.c_str());
                }
                if(trans.is_dmi_allowed()){
                    this->dmi_data.init();
                    this->dmi_ptr_valid = this->initSocket->get_direct_mem_ptr(trans, this->dmi_data);
                }
                //Now lets keep track of time
            """
        if not model.startswith('acc'):
            writeCode += 'this->quantKeeper.set(delay);\n}\n'
        else:
            writeCode += 'wait(delay);\n}\n'
    else:
        writeCode += """tlm::tlm_generic_payload trans;
        trans.set_address(address);
        trans.set_write();
        trans.set_data_ptr((unsigned char*)&datum);
        trans.set_data_length(sizeof(datum));
        trans.set_byte_enable_ptr(0);
        trans.set_dmi_allowed(false);
        trans.set_response_status(tlm::TLM_INCOMPLETE_RESPONSE);

        if(this->request_in_progress != NULL){
            wait(this->end_request_event);
        }
        request_in_progress = &trans;

        // Non-blocking transport call on the forward path
        sc_time delay = SC_ZERO_TIME;
        tlm::tlm_phase phase = tlm::BEGIN_REQ;
        tlm::tlm_sync_enum status;
        status = initSocket->nb_transport_fw(trans, phase, delay);

        if(trans.is_response_error()){
            std::string errorStr("Error from nb_transport_fw, response status = " + trans.get_response_string());
            SC_REPORT_ERROR("TLM-2", errorStr.c_str());
        }

        // Check value returned from nb_transport_fw
        if(status == tlm::TLM_UPDATED){
            // The timing annotation must be honored
            m_peq.notify(trans, phase, delay);
            wait(this->end_response_event);
        }
        else if(status == tlm::TLM_COMPLETED){
            // The completion of the transaction necessarily ends the BEGIN_REQ phase
            this->request_in_progress = NULL;
            // The target has terminated the transaction, I check the correctness
            if(trans.is_response_error()){
                SC_REPORT_ERROR("TLM-2", ("Transaction returned with error, response status = " + trans.get_response_string()).c_str());
            }
        }
        wait(this->end_response_event);
        """
    writeBody = cxx_writer.writer_code.Code(swapDEndianessCode + writeMemAliasCode + checkWatchPointCode + writeCode)
    datumParam = cxx_writer.writer_code.Parameter('datum', archDWordType)
    writeDecl = cxx_writer.writer_code.Method('write_dword', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    writeBody = cxx_writer.writer_code.Code(swapEndianessCode + writeMemAliasCode + checkWatchPointCode + writeCode)
    datumParam = cxx_writer.writer_code.Parameter('datum', archWordType)
    writeDecl = cxx_writer.writer_code.Method('write_word', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], inline = True, noException = True)
    tlmPortElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType)
    writeBody = cxx_writer.writer_code.Code(swapEndianessCode + writeMemAliasCode + checkWatchPointCode + writeCode)
    writeDecl = cxx_writer.writer_code.Method('write_half', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archByteType)
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkWatchPointCode + writeCode)
    writeDecl = cxx_writer.writer_code.Method('write_byte', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)

    readCode1 = """tlm::tlm_generic_payload trans;
        trans.set_address(address);
        trans.set_read();
        """
    readCode2 = """trans.set_data_ptr(reinterpret_cast<unsigned char *>(&datum));
        this->initSocket->transport_dbg(trans);
        """
    addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + readCode1 + 'trans.set_data_length(' + str(self.wordSize*2) + ');\n' + str(archDWordType) + ' datum = 0;\n' + readCode2 + swapDEndianessCode + 'return datum;')
    readBody.addInclude('trap_utils.hpp')
    readBody.addInclude('tlm.h')
    readDecl = cxx_writer.writer_code.Method('read_dword_dbg', readBody, archDWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + readCode1 + 'trans.set_data_length(' + str(self.wordSize) + ');\n' + str(archWordType) + ' datum = 0;\n' + readCode2 + swapEndianessCode + 'return datum;')
    readDecl = cxx_writer.writer_code.Method('read_word_dbg', readBody, archWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + readCode1 + 'trans.set_data_length(' + str(self.wordSize/2) + ');\n' + str(archHWordType) + ' datum = 0;\n' + readCode2 + swapEndianessCode + 'return datum;')
    readDecl = cxx_writer.writer_code.Method('read_half_dbg', readBody, archHWordType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    readBody = cxx_writer.writer_code.Code(readMemAliasCode + readCode1 + 'trans.set_data_length(1);\n' + str(archByteType) + ' datum = 0;\n' + readCode2 + 'return datum;')
    readDecl = cxx_writer.writer_code.Method('read_byte_dbg', readBody, archByteType, 'pu', [addressParam], noException = True)
    tlmPortElements.append(readDecl)
    writeCode1 = """tlm::tlm_generic_payload trans;
        trans.set_address(address);
        trans.set_write();
        """
    writeCode2 = """trans.set_data_ptr((unsigned char *)&datum);
        this->initSocket->transport_dbg(trans);
        """
    writeBody = cxx_writer.writer_code.Code(swapDEndianessCode + writeMemAliasCode + writeCode1 + 'trans.set_data_length(' + str(self.wordSize*2) + ');\n' + writeCode2)
    datumParam = cxx_writer.writer_code.Parameter('datum', archDWordType)
    writeDecl = cxx_writer.writer_code.Method('write_dword_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    writeBody = cxx_writer.writer_code.Code(swapEndianessCode + writeMemAliasCode + writeCode1 + 'trans.set_data_length(' + str(self.wordSize) + ');\n' + writeCode2)
    datumParam = cxx_writer.writer_code.Parameter('datum', archWordType)
    writeDecl = cxx_writer.writer_code.Method('write_word_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType)
    writeBody = cxx_writer.writer_code.Code(swapEndianessCode + writeMemAliasCode + writeCode1 + 'trans.set_data_length(' + str(self.wordSize/2) + ');\n' + writeCode2)
    writeDecl = cxx_writer.writer_code.Method('write_half_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archByteType)
    writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + writeCode1 + 'trans.set_data_length(1);\n' + writeCode2)
    writeDecl = cxx_writer.writer_code.Method('write_byte_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
    tlmPortElements.append(writeDecl)

    lockDecl = cxx_writer.writer_code.Method('lock', emptyBody, cxx_writer.writer_code.voidType, 'pu')
    tlmPortElements.append(lockDecl)
    unlockDecl = cxx_writer.writer_code.Method('unlock', emptyBody, cxx_writer.writer_code.voidType, 'pu')
    tlmPortElements.append(unlockDecl)

    constructorParams.append(cxx_writer.writer_code.Parameter('portName', cxx_writer.writer_code.sc_module_nameType))
    tlmPortInit.append('sc_module(portName)')
    initSockAttr = cxx_writer.writer_code.Attribute('initSocket', tlminitsocketType, 'pu')
    tlmPortElements.append(initSockAttr)
    constructorCode = 'this->debugger = NULL;\n'
    if model.endswith('LT'):
        if not model.startswith('acc'):
            quantumKeeperType = cxx_writer.writer_code.Type('tlm_utils::tlm_quantumkeeper', 'tlm_utils/tlm_quantumkeeper.h')
            quantumKeeperAttribute = cxx_writer.writer_code.Attribute('quantKeeper', quantumKeeperType.makeRef(), 'pri')
            tlmPortElements.append(quantumKeeperAttribute)
            tlmPortInit.append('quantKeeper(quantKeeper)')
            constructorParams.append(cxx_writer.writer_code.Parameter('quantKeeper', quantumKeeperType.makeRef()))
        dmi_ptr_validAttribute = cxx_writer.writer_code.Attribute('dmi_ptr_valid', cxx_writer.writer_code.boolType, 'pri')
        tlmPortElements.append(dmi_ptr_validAttribute)
        dmi_dataAttribute = cxx_writer.writer_code.Attribute('dmi_data', tlm_dmiType, 'pri')
        tlmPortElements.append(dmi_dataAttribute)
        constructorCode += 'this->dmi_ptr_valid = false;\n'
    else:
        peqType = cxx_writer.writer_code.TemplateType('tlm_utils::peq_with_cb_and_phase', [TLMMemoryType], 'tlm_utils/peq_with_cb_and_phase.h')
        tlmPortElements.append(cxx_writer.writer_code.Attribute('m_peq', peqType, 'pri'))
        tlmPortInit.append('m_peq(this, &TLMMemory::peq_cb)')
        tlmPortInit.append('request_in_progress(NULL)')
        constructorCode += """// Register callbacks for incoming interface method calls
            this->initSocket.register_nb_transport_bw(this, &TLMMemory::nb_transport_bw);
            """

    tlmPortElements += aliasAttrs

    extPortDecl = cxx_writer.writer_code.ClassDeclaration('TLMMemory', tlmPortElements, [memIfType, cxx_writer.writer_code.sc_moduleType], namespaces = [namespace])
    constructorBody = cxx_writer.writer_code.Code(constructorCode + 'end_module();')
    publicExtPortConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams + aliasParams, tlmPortInit + aliasInit)
    extPortDecl.addConstructor(publicExtPortConstr)

    return extPortDecl

def getGetIRQPorts(self, namespace):
    # Returns the classes implementing the interrupt ports; there can
    # be two different kind of ports: systemc based or TLM based
    TLMWidth = []
    SyscWidth = []
    for i in self.irqs:
        if i.operation:
            if i.tlm:
                if not i.portWidth in TLMWidth:
                    TLMWidth.append(i.portWidth)
            else:
                if not i.portWidth in SyscWidth:
                    SyscWidth.append(i.portWidth)


    # Lets now create the potyrt classes:
    classes = []
    for width in TLMWidth:
        # TLM ports: I declare a normal TLM slave
        tlmsocketType = cxx_writer.writer_code.TemplateType('tlm_utils::multi_passthrough_target_socket', ['IntrTLMPort_' + str(width), str(width), 'tlm::tlm_base_protocol_types', 1, 'sc_core::SC_ZERO_OR_MORE_BOUND'], 'tlm_utils/multi_passthrough_target_socket.h')
        payloadType = cxx_writer.writer_code.Type('tlm::tlm_generic_payload', 'tlm.h')
        tlmPortElements = []

        blockTransportCode = """unsigned char* ptr = trans.get_data_ptr();
            sc_dt::uint64 adr = trans.get_address();
            if(*ptr == 0){
                //Lower the interrupt
                this->irqSignal = -1;
            }
            else{
                //Raise the interrupt
                this->irqSignal = adr;
            }
            trans.set_response_status(tlm::TLM_OK_RESPONSE);
        """
        blockTransportBody = cxx_writer.writer_code.Code(blockTransportCode)
        tagParam = cxx_writer.writer_code.Parameter('tag', cxx_writer.writer_code.intType)
        payloadParam = cxx_writer.writer_code.Parameter('trans', payloadType.makeRef())
        delayParam = cxx_writer.writer_code.Parameter('delay', cxx_writer.writer_code.sc_timeType.makeRef())
        blockTransportDecl = cxx_writer.writer_code.Method('b_transport', blockTransportBody, cxx_writer.writer_code.voidType, 'pu', [tagParam, payloadParam, delayParam])
        tlmPortElements.append(blockTransportDecl)

        debugTransportBody = cxx_writer.writer_code.Code(blockTransportCode + 'return trans.get_data_length();')
        debugTransportDecl = cxx_writer.writer_code.Method('transport_dbg', debugTransportBody, cxx_writer.writer_code.uintType, 'pu', [tagParam, payloadParam])
        tlmPortElements.append(debugTransportDecl)

        nblockTransportCode = """THROW_EXCEPTION("Method not yet implemented");
        """
        nblockTransportBody = cxx_writer.writer_code.Code(nblockTransportCode)
        nblockTransportBody.addInclude('trap_utils.hpp')
        sync_enumType = cxx_writer.writer_code.Type('tlm::tlm_sync_enum', 'tlm.h')
        phaseParam = cxx_writer.writer_code.Parameter('phase', cxx_writer.writer_code.Type('tlm::tlm_phase').makeRef())
        nblockTransportDecl = cxx_writer.writer_code.Method('nb_transport_fw', nblockTransportBody, sync_enumType, 'pu', [tagParam, payloadParam, phaseParam, delayParam])
        tlmPortElements.append(nblockTransportDecl)

        socketAttr = cxx_writer.writer_code.Attribute('socket', tlmsocketType, 'pu')
        tlmPortElements.append(socketAttr)
        from isa import resolveBitType
        widthType = resolveBitType('BIT<' + str(width) + '>')
        irqSignalAttr = cxx_writer.writer_code.Attribute('irqSignal', widthType.makeRef(), 'pu')
        tlmPortElements.append(irqSignalAttr)
        constructorCode = ''
        tlmPortInit = []
        constructorParams = []
        constructorParams.append(cxx_writer.writer_code.Parameter('portName', cxx_writer.writer_code.sc_module_nameType))
        constructorParams.append(cxx_writer.writer_code.Parameter('irqSignal', widthType.makeRef()))
        tlmPortInit.append('sc_module(portName)')
        tlmPortInit.append('irqSignal(irqSignal)')
        tlmPortInit.append('socket(portName)')
        constructorCode += 'this->socket.register_b_transport(this, &IntrTLMPort_' + str(width) + '::b_transport);\n'
        constructorCode += 'this->socket.register_transport_dbg(this, &IntrTLMPort_' + str(width) + '::transport_dbg);\n'
        constructorCode += 'this->socket.register_nb_transport_fw(this, &IntrTLMPort_' + str(width) + '::nb_transport_fw);\n'
        irqPortDecl = cxx_writer.writer_code.ClassDeclaration('IntrTLMPort_' + str(width), tlmPortElements, [cxx_writer.writer_code.sc_moduleType], namespaces = [namespace])
        constructorBody = cxx_writer.writer_code.Code(constructorCode + 'end_module();')
        publicExtPortConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, tlmPortInit)
        irqPortDecl.addConstructor(publicExtPortConstr)
        classes.append(irqPortDecl)
    for width in SyscWidth:
        # SystemC ports: I simply have a method listening for a signal; note that in order to lower the interrupt,
        # the signal has to be equal to 0
        widthSignalType = cxx_writer.writer_code.TemplateType('sc_signal', [widthType], 'systemc.h')
        systemcPortElements = []
        sensitiveMethodCode = 'this->irqSignal = this->recvIntr.read();'
        sensitiveMethodBody = cxx_writer.writer_code.Code(sensitiveMethodCode)
        sensitiveMethodDecl = cxx_writer.writer_code.Method('irqRecvMethod', sensitiveMethodBody, cxx_writer.writer_code.voidType, 'pu')
        systemcPortElements.append(sensitiveMethodDecl)
        signalAttr = cxx_writer.writer_code.Attribute('recvIntr', widthSignalType, 'pu')
        systemcPortElements.append(signalAttr)
        irqSignalAttr = cxx_writer.writer_code.Attribute('irqSignal', widthType.makeRef(), 'pu')
        tlmPortElements.append(irqSignalAttr)
        constructorCode = ''
        tlmPortInit = []
        constructorParams = []
        constructorParams.append(cxx_writer.writer_code.Parameter('portName', cxx_writer.writer_code.sc_module_nameType))
        constructorParams.append(cxx_writer.writer_code.Parameter('irqSignal', widthType.makeRef()))
        tlmPortInit.append('sc_module(portName)')
        tlmPortInit.append('irqSignal(irqSignal)')
        constructorCode += 'SC_METHOD();\nsensitive << this->recvIntr;\n'
        irqPortDecl = cxx_writer.writer_code.ClassDeclaration('IntrSysCPort_' + str(width), systemcPortElements, [cxx_writer.writer_code.sc_moduleType], namespaces = [namespace])
        constructorBody = cxx_writer.writer_code.Code(constructorCode + 'end_module();')
        publicExtPortConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, tlmPortInit)
        irqPortDecl.addConstructor(publicExtPortConstr)
        classes.append(irqPortDecl)
    return classes

def getGetPINPorts(self, namespace):
    # Returns the code implementing pins for communication with external world.
    # there are both incoming and outgoing external ports. For the outgoing
    # I simply have to declare the port class (like memory ports), for the
    # incoming I also have to specify the operation which has to be performed
    # when the port is triggered (they are like interrupt ports)
    if len(self.pins) == 0:
        return None

    alreadyDecl = []
    inboundSysCPorts = []
    outboundSysCPorts = []
    inboundTLMPorts = []
    outboundTLMPorts = []
    for port in self.pins:
        if port.inbound:
            # I add all the inbound ports since there is an action specified for each
            # of them. In order to correctly execute the specified action the
            # port needs to have references to all the architectural elements
            if port.systemc:
                inboundSysCPorts.append(port)
            else:
                inboundTLMPorts.append(port)
        else:
            # I have to declare a new port only if there is not yet another
            # port with same width and it is systemc or tlm.
            if not (str(port.portWidth) + '_' + str(port.systemc)) in alreadyDecl:
                if port.systemc:
                    outboundSysCPorts.append(port)
                else:
                    outboundTLMPorts.append(port)
                alreadyDecl.append(str(port.portWidth) + '_' + str(self.systemc))

    pinClasses = []
    # Now I have to actually declare the ports; I declare only
    # blocking interfaces
    # outgoing
    for port in outboundTLMPorts:
        pinPortElements = []

        tlm_dmiType = cxx_writer.writer_code.Type('tlm::tlm_dmi', 'tlm.h')
        PinPortType = cxx_writer.writer_code.Type('PinTLM_out_' + str(port.portWidth))
        tlminitsocketType = cxx_writer.writer_code.TemplateType('tlm_utils::multi_passthrough_initiator_socket', [PinPortType, port.portWidth, 'tlm::tlm_base_protocol_types', 1, 'sc_core::SC_ZERO_OR_MORE_BOUND'], 'tlm_utils/multi_passthrough_initiator_socket.h')
        payloadType = cxx_writer.writer_code.Type('tlm::tlm_generic_payload', 'tlm.h')
        pinPortInit = []
        constructorParams = []

        sendPINBody = cxx_writer.writer_code.Code("""tlm::tlm_generic_payload trans;
        sc_time delay;
        trans.set_address(address);
        trans.set_write();
        trans.set_data_ptr((unsigned char*)&datum);
        trans.set_data_length(sizeof(datum));
        trans.set_byte_enable_ptr(0);
        trans.set_dmi_allowed(false);
        trans.set_response_status(tlm::TLM_INCOMPLETE_RESPONSE);
        this->initSocket->b_transport(trans, delay);

        if(trans.is_response_error()){
            std::string errorStr("Error from b_transport, response status = " + trans.get_response_string());
            SC_REPORT_ERROR("TLM-2", errorStr.c_str());
        }
        """)
        sendPINBody.addInclude('trap_utils.hpp')
        sendPINBody.addInclude('tlm.h')
        from isa import resolveBitType
        PINWidthType = resolveBitType('BIT<' + str(port.portWidth) + '>')
        addressParam = cxx_writer.writer_code.Parameter('address', PINWidthType.makeRef().makeConst())
        datumParam = cxx_writer.writer_code.Parameter('datum', PINWidthType)
        sendPINDecl = cxx_writer.writer_code.Method('send_pin_req', sendPINBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
        pinPortElements.append(sendPINDecl)

        constructorParams.append(cxx_writer.writer_code.Parameter('portName', cxx_writer.writer_code.sc_module_nameType))
        pinPortInit.append('sc_module(portName)')
        initSockAttr = cxx_writer.writer_code.Attribute('initSocket', tlminitsocketType, 'pu')
        pinPortInit.append('initSocket(sc_gen_unique_name(portName))')
        pinPortElements.append(initSockAttr)

        pinPortDecl = cxx_writer.writer_code.ClassDeclaration('PinTLM_out_' + str(port.portWidth), pinPortElements, [cxx_writer.writer_code.sc_moduleType], namespaces = [namespace])
        constructorBody = cxx_writer.writer_code.Code('end_module();')
        publicPINPortConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams, pinPortInit)
        pinPortDecl.addConstructor(publicPINPortConstr)
        pinClasses.append(pinPortDecl)

    for port in outboundSysCPorts:
        raise Exception('outbound SystemC ports not yet supported')

    # incoming
    for port in inboundTLMPorts:
        raise Exception('inbound TLM ports not yet supported')

    for port in inboundSysCPorts:
        raise Exception('inbound SystemC ports not yet supported')

    return pinClasses

def getIRQTests(self, trace, combinedTrace, namespace):
    # Returns the code implementing the tests for the interrupts
    from processor import extractRegInterval
    testFuns = []
    global testNames
    from procWriter import testNames

    from procWriter import resourceType

    archElemsDeclStr = ''
    destrDecls = ''
    for reg in self.regs:
        archElemsDeclStr += str(resourceType[reg.name]) + ' ' + reg.name + ';\n'
    for regB in self.regBanks:
        if (regB.constValue and len(regB.constValue) < regB.numRegs)  or (regB.delay and len(regB.delay) < regB.numRegs):
            archElemsDeclStr += str(resourceType[regB.name]) + ' ' + regB.name + '(' + str(regB.numRegs) + ');\n'
            for i in range(0, regB.numRegs):
                if regB.constValue.has_key(i) or regB.delay.has_key(i):
                    archElemsDeclStr += regB.name + '.setNewRegister(' + str(i) + ', new ' + str(resourceType[regB.name + '[' + str(i) + ']']) + '());\n'
                else:
                    archElemsDeclStr += regB.name + '.setNewRegister(' + str(i) + ', new ' + str(resourceType[regB.name + '_baseType']) + '());\n'
        else:
            archElemsDeclStr += str(resourceType[regB.name]) + ' ' + regB.name + ' = new ' + str(resourceType[regB.name].makeNormal()) + '[' + str(regB.numRegs) + '];\n'
            destrDecls += 'delete [] ' + regB.name + ';\n'
    for alias in self.aliasRegs:
        archElemsDeclStr += str(resourceType[alias.name]) + ' ' + alias.name + ';\n'
    for aliasB in self.aliasRegBanks:
        archElemsDeclStr += str(resourceType[aliasB.name].makePointer()) + ' ' + aliasB.name + ' = new ' + str(resourceType[aliasB.name]) + '[' + str(aliasB.numRegs) + '];\n'
        destrDecls += 'delete [] ' + aliasB.name + ';\n'
    memAliasInit = ''
    for alias in self.memAlias:
        memAliasInit += ', ' + alias.alias

    if (trace or (self.memory and self.memory[2])) and not self.systemc:
        archElemsDeclStr += 'unsigned int totalCycles;\n'
    if self.memory:
        memDebugInit = ''
        if self.memory[2]:
            memDebugInit += ', totalCycles'
        if self.memory[3]:
            memDebugInit += ', ' + self.memory[3]
        archElemsDeclStr += 'LocalMemory ' + self.memory[0] + '(' + str(self.memory[1]) + memDebugInit + memAliasInit + ');\n'
    # Note how I declare local memories even for TLM ports. I use 1MB as default dimension
    for tlmPorts in self.tlmPorts.keys():
        archElemsDeclStr += 'LocalMemory ' + tlmPorts + '(' + str(1024*1024) + memAliasInit + ');\n'
    # Now I declare the PIN stubs for the outgoing PIN ports
    # and alts themselves
    outPinPorts = []
    for pinPort in self.pins:
        if not pinPort.inbound:
            outPinPorts.append(pinPort.name)
            pinPortTypeName = 'Pin'
            if pinPort.systemc:
                pinPortTypeName += 'SysC_'
            else:
                pinPortTypeName += 'TLM_'
            if pinPort.inbound:
                pinPortTypeName += 'in_'
            else:
                pinPortTypeName += 'out_'
            pinPortTypeName += str(pinPort.portWidth)
            archElemsDeclStr += pinPortTypeName + ' ' + pinPort.name + '(sc_core::sc_gen_unique_name(\"' + pinPort.name + '_PIN\"));\n'
            archElemsDeclStr += 'PINTarget<' + str(pinPort.portWidth) + '> ' + pinPort.name + '_target(sc_core::sc_gen_unique_name(\"' + pinPort.name + '_target\"));\n'
            archElemsDeclStr += pinPort.name + '.initSocket.bind(' + pinPort.name + '_target.socket);\n'

    # Now we perform the alias initialization; note that they need to be initialized according to the initialization graph
    # (there might be dependences among the aliases)
    aliasInit = ''
    import networkx as NX
    from procWriter import aliasGraph
    orderedNodes = NX.topological_sort(aliasGraph)
    for alias in orderedNodes:
        if alias == 'stop':
            continue
        if isinstance(alias.initAlias, type('')):
            index = extractRegInterval(alias.initAlias)
            if index:
                curIndex = index[0]
                try:
                    for i in range(0, alias.numRegs):
                        aliasInit += alias.name + '[' + str(i) + '].updateAlias(' + alias.initAlias[:alias.initAlias.find('[')] + '[' + str(curIndex) + ']);\n'
                        curIndex += 1
                except AttributeError:
                    aliasInit += alias.name + '.updateAlias(' + alias.initAlias[:alias.initAlias.find('[')] + '[' + str(curIndex) + '], ' + str(alias.offset) + ');\n'
            else:
                aliasInit += alias.name + '.updateAlias(' + alias.initAlias + ', ' + str(alias.offset) + ');\n'
        else:
            curIndex = 0
            for curAlias in alias.initAlias:
                index = extractRegInterval(curAlias)
                if index:
                    for curRange in range(index[0], index[1] + 1):
                        aliasInit += alias.name + '[' + str(curIndex) + '].updateAlias(' + curAlias[:curAlias.find('[')] + '[' + str(curRange) + ']);\n'
                        curIndex += 1
                else:
                    aliasInit += alias.name + '[' + str(curIndex) + '].updateAlias(' + curAlias + ');\n'
                    curIndex += 1

    for irq in self.irqs:
        from isa import resolveBitType
        irqType = resolveBitType('BIT<' + str(irq.portWidth) + '>')
        archElemsDeclStr += '\n//Fake interrupt line\n' + str(irqType) + ' ' + irq.name + ';\n'
        testNum = 0
        for test in irq.tests:
            testName = 'irq_test_' + irq.name + '_' + str(testNum)
            code = archElemsDeclStr

            # Note that each test is composed of two parts: the first one
            # containing the status of the processor before the interrupt and
            # then the status of the processor after
            for resource, value in test[0].items():
                # I set the initial value of the global resources
                brackIndex = resource.find('[')
                memories = self.tlmPorts.keys()
                if self.memory:
                    memories.append(self.memory[0])
                if brackIndex > 0 and resource[:brackIndex] in memories:
                    try:
                        code += resource[:brackIndex] + '.write_word_dbg(' + hex(int(resource[brackIndex + 1:-1])) + ', ' + hex(value) + ');\n'
                    except ValueError:
                        code += resource[:brackIndex] + '.write_word_dbg(' + hex(int(resource[brackIndex + 1:-1], 16)) + ', ' + hex(value) + ');\n'
                elif resource == irq.name:
                    code += resource + ' = ' + hex(value) + ';\n'
                else:
                    code += resource + '.immediateWrite(' + hex(value) + ');\n'

            # Now I declare the actual interrupt code
            code += 'if('
            if(irq.condition):
                code += '('
            code += irq.name + ' != -1'
            if(irq.condition):
                code += ') && (' + irq.condition + ')'
            code += '){\n'
            # Now here we insert the actual interrupt behavior by simply creating and calling the
            # interrupt instruction
            from procWriter import baseInstrInitElement
            code += 'IRQ_' + irq.name + '_Instruction toTest(' + baseInstrInitElement + ', ' + irq.name + ');\n'
            code += """try{
                toTest.behavior();
            }
            catch(annull_exception &etc){
            }"""
            code += '\n}\n'

            # finally I check the correctness of the executed operation
            for resource, value in test[1].items():
                # I check the value of the listed resources to make sure that the
                # computation executed correctly
                code += 'BOOST_CHECK_EQUAL('
                brackIndex = resource.find('[')
                memories = self.tlmPorts.keys()
                if self.memory:
                    memories.append(self.memory[0])
                if brackIndex > 0 and resource[:brackIndex] in memories:
                    try:
                        code += resource[:brackIndex] + '.read_word_dbg(' + hex(int(resource[brackIndex + 1:-1])) + ')'
                    except ValueError:
                        code += resource[:brackIndex] + '.read_word_dbg(' + hex(int(resource[brackIndex + 1:-1], 16)) + ')'
                elif brackIndex > 0 and resource[:brackIndex] in outPinPorts:
                    try:
                        code += resource[:brackIndex] + '_target.readPIN(' + hex(int(resource[brackIndex + 1:-1])) + ')'
                    except ValueError:
                        code += resource[:brackIndex] + '_target.readPIN(' + hex(int(resource[brackIndex + 1:-1], 16)) + ')'
                else:
                    code += resource + '.readNewValue()'
                code += ', (' + str(self.bitSizes[1]) + ')' + hex(value) + ');\n\n'
            code += destrDecls
            curTest = cxx_writer.writer_code.Code(code)
            curTest.addInclude('instructions.hpp')
            wariningDisableCode = '#ifdef _WIN32\n#pragma warning( disable : 4101 )\n#endif\n'
            includeUnprotectedCode = '#define private public\n#define protected public\n#include \"registers.hpp\"\n#include \"memory.hpp\"\n#undef private\n#undef protected\n'
            curTest.addInclude(['boost/test/test_tools.hpp', 'customExceptions.hpp', wariningDisableCode, includeUnprotectedCode, 'alias.hpp'])
            curTestFunction = cxx_writer.writer_code.Function(testName, curTest, cxx_writer.writer_code.voidType)

            testFuns.append(curTestFunction)
            testNames.append(testName)
            testNum += 1

    return testFuns
