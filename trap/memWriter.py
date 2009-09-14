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

from procWriter import resourceType

def getCPPMemoryIf(self, model, namespace):
    # Creates the necessary structures for communicating with the memory; an
    # array in case of an internal memory, the TLM port for the use with TLM
    # etc.
    from isa import resolveBitType
    archDWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize*2) + '>')
    archWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize) + '>')
    archHWordType = resolveBitType('BIT<' + str(self.wordSize*self.byteSize/2) + '>')
    archByteType = resolveBitType('BIT<' + str(self.byteSize) + '>')
    # First of all I create the memory base class
    classes = []
    memoryIfElements = []
    emptyBody = cxx_writer.writer_code.Code('')
    addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
    readDecl = cxx_writer.writer_code.Method('read_dword', emptyBody, archDWordType, 'pu', [addressParam], pure = True, const = len(self.tlmPorts) == 0, noException = True)
    memoryIfElements.append(readDecl)
    readDecl = cxx_writer.writer_code.Method('read_word', emptyBody, archWordType, 'pu', [addressParam], pure = True, const = len(self.tlmPorts) == 0, noException = True)
    memoryIfElements.append(readDecl)
    readDecl = cxx_writer.writer_code.Method('read_half', emptyBody, archHWordType, 'pu', [addressParam], pure = True, const = len(self.tlmPorts) == 0, noException = True)
    memoryIfElements.append(readDecl)
    readDecl = cxx_writer.writer_code.Method('read_byte', emptyBody, archByteType, 'pu', [addressParam], pure = True, const = len(self.tlmPorts) == 0, noException = True)
    memoryIfElements.append(readDecl)
    readDeclDBGBody = cxx_writer.writer_code.Code('return this->read_dword(address);')
    readDecl = cxx_writer.writer_code.Method('read_dword_dbg', readDeclDBGBody, archDWordType, 'pu', [addressParam], virtual = True, const = len(self.tlmPorts) == 0)
    memoryIfElements.append(readDecl)
    readDeclDBGBody = cxx_writer.writer_code.Code('return this->read_word(address);')
    readDecl = cxx_writer.writer_code.Method('read_word_dbg', readDeclDBGBody, archWordType, 'pu', [addressParam], virtual = True, const = len(self.tlmPorts) == 0)
    memoryIfElements.append(readDecl)
    readDeclDBGBody = cxx_writer.writer_code.Code('return this->read_half(address);')
    readDecl = cxx_writer.writer_code.Method('read_half_dbg', readDeclDBGBody, archHWordType, 'pu', [addressParam], virtual = True, const = len(self.tlmPorts) == 0)
    memoryIfElements.append(readDecl)
    readDeclDBGBody = cxx_writer.writer_code.Code('return this->read_byte(address);')
    readDecl = cxx_writer.writer_code.Method('read_byte_dbg', readDeclDBGBody, archByteType, 'pu', [addressParam], virtual = True, const = len(self.tlmPorts) == 0)
    memoryIfElements.append(readDecl)

    datumParam = cxx_writer.writer_code.Parameter('datum', archDWordType)
    writeDecl = cxx_writer.writer_code.Method('write_dword', emptyBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], pure = True, noException = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archWordType)
    writeDecl = cxx_writer.writer_code.Method('write_word', emptyBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], pure = True, noException = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType)
    writeDecl = cxx_writer.writer_code.Method('write_half', emptyBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], pure = True, noException = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archByteType)
    writeDecl = cxx_writer.writer_code.Method('write_byte', emptyBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], pure = True, noException = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archDWordType)
    writeDeclDBGBody = cxx_writer.writer_code.Code('this->write_dword(address, datum);')
    writeDecl = cxx_writer.writer_code.Method('write_dword_dbg', writeDeclDBGBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], virtual = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archWordType)
    writeDeclDBGBody = cxx_writer.writer_code.Code('this->write_word(address, datum);')
    writeDecl = cxx_writer.writer_code.Method('write_word_dbg', writeDeclDBGBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], virtual = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType)
    writeDeclDBGBody = cxx_writer.writer_code.Code('this->write_half(address, datum);')
    writeDecl = cxx_writer.writer_code.Method('write_half_dbg', writeDeclDBGBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], virtual = True)
    memoryIfElements.append(writeDecl)
    datumParam = cxx_writer.writer_code.Parameter('datum', archByteType)
    writeDeclDBGBody = cxx_writer.writer_code.Code('this->write_byte(address, datum);')
    writeDecl = cxx_writer.writer_code.Method('write_byte_dbg', writeDeclDBGBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], virtual = True)
    memoryIfElements.append(writeDecl)

    for curType in [archWordType, archHWordType]:
        swapEndianessCode = str(archByteType) + """ helperByte = 0;
        for(int i = 0; i < sizeof(""" + str(curType) + """)/2; i++){
            helperByte = ((""" + str(archByteType) + """ *)&datum)[i];
            ((""" + str(archByteType) + """ *)&datum)[i] = ((""" + str(archByteType) + """ *)&datum)[sizeof(""" + str(curType) + """) -1 -i];
            ((""" + str(archByteType) + """ *)&datum)[sizeof(""" + str(curType) + """) -1 -i] = helperByte;
        }
        """
        swapEndianessBody = cxx_writer.writer_code.Code(swapEndianessCode)
        datumParam = cxx_writer.writer_code.Parameter('datum', curType.makeRef())
        swapEndianessDecl = cxx_writer.writer_code.Method('swapEndianess', swapEndianessBody, cxx_writer.writer_code.voidType, 'pu', [datumParam], inline = True, noException = True, const = True)
        memoryIfElements.append(swapEndianessDecl)

    lockDecl = cxx_writer.writer_code.Method('lock', emptyBody, cxx_writer.writer_code.voidType, 'pu', pure = True)
    memoryIfElements.append(lockDecl)
    unlockDecl = cxx_writer.writer_code.Method('unlock', emptyBody, cxx_writer.writer_code.voidType, 'pu', pure = True)
    memoryIfElements.append(unlockDecl)
    memoryIfDecl = cxx_writer.writer_code.ClassDeclaration('MemoryInterface', memoryIfElements, namespaces = [namespace])
    publicDestr = cxx_writer.writer_code.Destructor(emptyBody, 'pu', True)
    memoryIfDecl.addDestructor(publicDestr)
    classes.append(memoryIfDecl)

    # Now I check if it is the case of creating a local memory
    memoryElements = []
    readMemAliasCode = ''
    writeMemAliasCode = ''
    aliasAttrs = []
    aliasParams = []
    aliasInit = []
    MemoryToolsIfType = cxx_writer.writer_code.TemplateType('MemoryToolsIf', [str(archWordType)], 'ToolsIf.hpp')
    for alias in self.memAlias:
        aliasAttrs.append(cxx_writer.writer_code.Attribute(alias.alias, resourceType[alias.alias].makeRef(), 'pri'))
        aliasParams.append(cxx_writer.writer_code.Parameter(alias.alias, resourceType[alias.alias].makeRef()))
        aliasInit.append(alias.alias + '(' + alias.alias + ')')
        readMemAliasCode += 'if(address == ' + hex(long(alias.address)) + '){\nreturn this->' + alias.alias + ';\n}\n'
        writeMemAliasCode += 'if(address == ' + hex(long(alias.address)) + '){\n this->' + alias.alias + ' = datum;\nreturn;\n}\n'

    checkAddressCode = 'if(address >= this->size){\nTHROW_ERROR("Address " << std::hex << std::showbase << address << " out of memory");\n}\n'
    checkAddressCodeException = 'if(address >= this->size){\nTHROW_EXCEPTION("Address " << std::hex << std::showbase << address << " out of memory");\n}\n'

    if self.isBigEndian:
        swapEndianessCode = '#ifdef LITTLE_ENDIAN_BO\n'
    else:
        swapEndianessCode = '#ifdef BIG_ENDIAN_BO\n'
    swapEndianessCode += 'this->swapEndianess(datum);\n#endif\n'
    if self.isBigEndian:
        swapDEndianessCode = '#ifdef LITTLE_ENDIAN_BO\n'
    else:
        swapDEndianessCode = '#ifdef BIG_ENDIAN_BO\n'
    swapDEndianessCode += str(archWordType) + ' datum1 = (' + str(archWordType) + ')(datum);\nthis->swapEndianess(datum1);\n'
    swapDEndianessCode += str(archWordType) + ' datum2 = (' + str(archWordType) + ')(datum >> ' + str(self.wordSize*self.byteSize) + ');\nthis->swapEndianess(datum2);\n'
    swapDEndianessCode += 'datum = datum1 | (((' + str(archDWordType) + ')datum2) << ' + str(self.wordSize*self.byteSize) + ');\n#endif\n'

    memoryElements.append(cxx_writer.writer_code.Attribute('debugger', MemoryToolsIfType.makePointer(), 'pri'))
    setDebuggerBody = cxx_writer.writer_code.Code('this->debugger = debugger;')
    memoryElements.append(cxx_writer.writer_code.Method('setDebugger', setDebuggerBody, cxx_writer.writer_code.voidType, 'pu', [cxx_writer.writer_code.Parameter('debugger', MemoryToolsIfType.makePointer())]))
    checkWatchPointCode = """if(this->debugger != NULL){
        this->debugger->notifyAddress(address, sizeof(datum));
    }
    """

    if not self.memory or not self.memory[2]:
        emptyBody = cxx_writer.writer_code.Code('')
        addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + '\n' + str(archDWordType) + ' datum = *(' + str(archDWordType.makePointer()) + ')(this->memory + (unsigned long)address);\n' + swapDEndianessCode + '\nreturn datum;')
        readBody.addInclude('trap_utils.hpp')
        readDecl = cxx_writer.writer_code.Method('read_dword', readBody, archDWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, noException = True)
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + '\n' + str(archWordType) + ' datum = *(' + str(archWordType.makePointer()) + ')(this->memory + (unsigned long)address);\n' + swapEndianessCode + '\nreturn datum;')
        readBody.addInclude('trap_utils.hpp')
        readDecl = cxx_writer.writer_code.Method('read_word', readBody, archWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, inline = True, noException = True)
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + '\n' + str(archHWordType) + ' datum = *(' + str(archHWordType.makePointer()) + ')(this->memory + (unsigned long)address);\n' + swapEndianessCode + '\nreturn datum;')
        readDecl = cxx_writer.writer_code.Method('read_half', readBody, archHWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, noException = True)
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + 'return *(' + str(archByteType.makePointer()) + ')(this->memory + (unsigned long)address);')
        readDecl = cxx_writer.writer_code.Method('read_byte', readBody, archByteType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, noException = True)
        memoryElements.append(readDecl)

        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCodeException + '\n' + str(archDWordType) + ' datum = *(' + str(archDWordType.makePointer()) + ')(this->memory + (unsigned long)address);\n' + swapDEndianessCode + '\nreturn datum;')
        readBody.addInclude('trap_utils.hpp')
        readDecl = cxx_writer.writer_code.Method('read_dword_dbg', readBody, archDWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0)
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCodeException + '\n' + str(archWordType) + ' datum = *(' + str(archWordType.makePointer()) + ')(this->memory + (unsigned long)address);\n' + swapEndianessCode + '\nreturn datum;')
        readBody.addInclude('trap_utils.hpp')
        readDecl = cxx_writer.writer_code.Method('read_word_dbg', readBody, archWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, inline = True)
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCodeException + '\n' + str(archHWordType) + ' datum = *(' + str(archHWordType.makePointer()) + ')(this->memory + (unsigned long)address);\n' + swapEndianessCode + '\nreturn datum;')
        readDecl = cxx_writer.writer_code.Method('read_half_dbg', readBody, archHWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0)
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCodeException + 'return *(' + str(archByteType.makePointer()) + ')(this->memory + (unsigned long)address);')
        readDecl = cxx_writer.writer_code.Method('read_byte_dbg', readBody, archByteType, 'pu', [addressParam], const = len(self.tlmPorts) == 0)
        memoryElements.append(readDecl)

        addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + checkWatchPointCode + '\n' + swapDEndianessCode + '\n*(' + str(archDWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
        datumParam = cxx_writer.writer_code.Parameter('datum', archDWordType)
        writeDecl = cxx_writer.writer_code.Method('write_dword', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
        memoryElements.append(writeDecl)
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + checkWatchPointCode + '\n' + swapEndianessCode + '\n*(' + str(archWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
        datumParam = cxx_writer.writer_code.Parameter('datum', archWordType)
        writeDecl = cxx_writer.writer_code.Method('write_word', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], inline = True, noException = True)
        memoryElements.append(writeDecl)
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + checkWatchPointCode + '\n' + swapEndianessCode + '\n*(' + str(archHWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
        datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType)
        writeDecl = cxx_writer.writer_code.Method('write_half', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
        memoryElements.append(writeDecl)
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + checkWatchPointCode + '*(' + str(archByteType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
        datumParam = cxx_writer.writer_code.Parameter('datum', archByteType)
        writeDecl = cxx_writer.writer_code.Method('write_byte', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
        memoryElements.append(writeDecl)

        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCodeException + checkWatchPointCode + '\n' + swapDEndianessCode + '\n*(' + str(archDWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
        datumParam = cxx_writer.writer_code.Parameter('datum', archDWordType)
        writeDecl = cxx_writer.writer_code.Method('write_dword_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam])
        memoryElements.append(writeDecl)
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCodeException + checkWatchPointCode + '\n' + swapEndianessCode + '\n*(' + str(archWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
        datumParam = cxx_writer.writer_code.Parameter('datum', archWordType)
        writeDecl = cxx_writer.writer_code.Method('write_word_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], inline = True)
        memoryElements.append(writeDecl)
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCodeException + checkWatchPointCode + '\n' + swapEndianessCode + '\n*(' + str(archHWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
        datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType)
        writeDecl = cxx_writer.writer_code.Method('write_half_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam])
        memoryElements.append(writeDecl)
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCodeException + checkWatchPointCode + '*(' + str(archByteType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;')
        datumParam = cxx_writer.writer_code.Parameter('datum', archByteType)
        writeDecl = cxx_writer.writer_code.Method('write_byte_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam])
        memoryElements.append(writeDecl)

        lockDecl = cxx_writer.writer_code.Method('lock', emptyBody, cxx_writer.writer_code.voidType, 'pu')
        memoryElements.append(lockDecl)
        unlockDecl = cxx_writer.writer_code.Method('unlock', emptyBody, cxx_writer.writer_code.voidType, 'pu')
        memoryElements.append(unlockDecl)
        arrayAttribute = cxx_writer.writer_code.Attribute('memory', cxx_writer.writer_code.charPtrType, 'pri')
        memoryElements.append(arrayAttribute)
        sizeAttribute = cxx_writer.writer_code.Attribute('size', cxx_writer.writer_code.uintType, 'pri')
        memoryElements.append(sizeAttribute)
        memoryElements += aliasAttrs
        localMemDecl = cxx_writer.writer_code.ClassDeclaration('LocalMemory', memoryElements, [memoryIfDecl.getType()], namespaces = [namespace])
        constructorBody = cxx_writer.writer_code.Code('this->memory = new char[size];\nthis->debugger = NULL;')
        constructorParams = [cxx_writer.writer_code.Parameter('size', cxx_writer.writer_code.uintType)]
        publicMemConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams + aliasParams, ['size(size)'] + aliasInit)
        localMemDecl.addConstructor(publicMemConstr)
        destructorBody = cxx_writer.writer_code.Code('delete [] this->memory;')
        publicMemDestr = cxx_writer.writer_code.Destructor(destructorBody, 'pu', True)
        localMemDecl.addDestructor(publicMemDestr)
        classes.append(localMemDecl)
    else:
        emptyBody = cxx_writer.writer_code.Code('')
        addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + '\n' + str(archDWordType) + ' datum = *(' + str(archDWordType.makePointer()) + ')(this->memory + (unsigned long)address);\n' + swapDEndianessCode + '\nreturn datum;')
        readBody.addInclude('trap_utils.hpp')
        readDecl = cxx_writer.writer_code.Method('read_dword', readBody, archDWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, noException = True)
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + '\n' + str(archWordType) + ' datum = *(' + str(archWordType.makePointer()) + ')(this->memory + (unsigned long)address);\n' + swapEndianessCode + '\nreturn datum;')
        readBody.addInclude('trap_utils.hpp')
        readDecl = cxx_writer.writer_code.Method('read_word', readBody, archWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, inline = True, noException = True)
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + '\n' + str(archHWordType) + ' datum = *(' + str(archHWordType.makePointer()) + ')(this->memory + (unsigned long)address);\n' + swapEndianessCode + '\nreturn datum;')
        readDecl = cxx_writer.writer_code.Method('read_half', readBody, archHWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, noException = True)
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCode + 'return *(' + str(archByteType.makePointer()) + ')(this->memory + (unsigned long)address);')
        readDecl = cxx_writer.writer_code.Method('read_byte', readBody, archByteType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, noException = True)
        memoryElements.append(readDecl)

        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCodeException + '\n' + str(archDWordType) + ' datum = *(' + str(archDWordType.makePointer()) + ')(this->memory + (unsigned long)address);\n' + swapDEndianessCode + '\nreturn datum;')
        readBody.addInclude('trap_utils.hpp')
        readDecl = cxx_writer.writer_code.Method('read_dword_dbg', readBody, archDWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0)
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCodeException + '\n' + str(archWordType) + ' datum = *(' + str(archWordType.makePointer()) + ')(this->memory + (unsigned long)address);\n' + swapEndianessCode + '\nreturn datum;')
        readBody.addInclude('trap_utils.hpp')
        readDecl = cxx_writer.writer_code.Method('read_word_dbg', readBody, archWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0, inline = True)
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCodeException + '\n' + str(archHWordType) + ' datum = *(' + str(archHWordType.makePointer()) + ')(this->memory + (unsigned long)address);\n' + swapEndianessCode + '\nreturn datum;')
        readDecl = cxx_writer.writer_code.Method('read_half_dbg', readBody, archHWordType, 'pu', [addressParam], const = len(self.tlmPorts) == 0)
        memoryElements.append(readDecl)
        readBody = cxx_writer.writer_code.Code(readMemAliasCode + checkAddressCodeException + 'return *(' + str(archByteType.makePointer()) + ')(this->memory + (unsigned long)address);')
        readDecl = cxx_writer.writer_code.Method('read_byte_dbg', readBody, archByteType, 'pu', [addressParam], const = len(self.tlmPorts) == 0)
        memoryElements.append(readDecl)

        addressParam = cxx_writer.writer_code.Parameter('address', archWordType.makeRef().makeConst())
        dumpCode = 'MemAccessType dumpInfo;\n'
        if not self.systemc and not model.startswith('acc')  and not model.endswith('AT'):
            dumpCode += 'dumpInfo.simulationTime = curCycle;'
        else:
            dumpCode += 'dumpInfo.simulationTime = sc_time_stamp().to_double();'
        dumpCode += """
dumpInfo.programCounter = this->""" + self.memory[3] + """;
for(int i = 0; i < """ + str(self.wordSize*2) + """; i++){
    dumpInfo.address = address + i;
    dumpInfo.val = (char)((datum & (0xFF << i*8)) >> i*8);
    this->dumpFile.write((char *)&dumpInfo, sizeof(MemAccessType));
}
"""
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + checkWatchPointCode + '\n' + swapDEndianessCode + '\n*(' + str(archDWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;' + dumpCode)
        writeBody.addInclude('memAccessType.hpp')
        datumParam = cxx_writer.writer_code.Parameter('datum', archDWordType)
        writeDecl = cxx_writer.writer_code.Method('write_dword', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
        memoryElements.append(writeDecl)
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCodeException + checkWatchPointCode + '\n' + swapDEndianessCode + '\n*(' + str(archDWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;' + dumpCode)
        writeBody.addInclude('memAccessType.hpp')
        datumParam = cxx_writer.writer_code.Parameter('datum', archDWordType)
        writeDecl = cxx_writer.writer_code.Method('write_dword_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam])
        memoryElements.append(writeDecl)
        dumpCode = 'MemAccessType dumpInfo;\n'
        if not self.systemc and not model.startswith('acc') and not model.endswith('AT'):
            dumpCode += 'dumpInfo.simulationTime = curCycle;'
        else:
            dumpCode += 'dumpInfo.simulationTime = sc_time_stamp().to_double();'
        dumpCode += """
dumpInfo.programCounter = this->""" + self.memory[3] + """;
for(int i = 0; i < """ + str(self.wordSize) + """; i++){
    dumpInfo.address = address + i;
    dumpInfo.val = (char)((datum & (0xFF << i*8)) >> i*8);
    this->dumpFile.write((char *)&dumpInfo, sizeof(MemAccessType));
}
"""
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + checkWatchPointCode + '\n' + swapEndianessCode + '\n*(' + str(archWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;\n' + dumpCode)
        datumParam = cxx_writer.writer_code.Parameter('datum', archWordType)
        writeDecl = cxx_writer.writer_code.Method('write_word', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], inline = True, noException = True)
        memoryElements.append(writeDecl)
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCodeException + checkWatchPointCode + '\n' + swapEndianessCode + '\n*(' + str(archWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;\n' + dumpCode)
        datumParam = cxx_writer.writer_code.Parameter('datum', archWordType)
        writeDecl = cxx_writer.writer_code.Method('write_word_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], inline = True)
        memoryElements.append(writeDecl)
        dumpCode = 'MemAccessType dumpInfo;\n'
        if not self.systemc and not model.startswith('acc') and not model.endswith('AT'):
            dumpCode += 'dumpInfo.simulationTime = curCycle;'
        else:
            dumpCode += 'dumpInfo.simulationTime = sc_time_stamp().to_double();'
        dumpCode += """
dumpInfo.programCounter = this->""" + self.memory[3] + """;
for(int i = 0; i < """ + str(self.wordSize/2) + """; i++){
    dumpInfo.address = address + i;
    dumpInfo.val = (char)((datum & (0xFF << i*8)) >> i*8);
    this->dumpFile.write((char *)&dumpInfo, sizeof(MemAccessType));
}
"""
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + checkWatchPointCode + '\n' + swapEndianessCode + '\n*(' + str(archHWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;\n' + dumpCode)
        writeBody.addInclude('memAccessType.hpp')
        datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType)
        writeDecl = cxx_writer.writer_code.Method('write_half', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
        memoryElements.append(writeDecl)
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCodeException + checkWatchPointCode + '\n' + swapEndianessCode + '\n*(' + str(archHWordType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;\n' + dumpCode)
        writeBody.addInclude('memAccessType.hpp')
        datumParam = cxx_writer.writer_code.Parameter('datum', archHWordType)
        writeDecl = cxx_writer.writer_code.Method('write_half_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam])
        memoryElements.append(writeDecl)
        dumpCode = 'MemAccessType dumpInfo;\n'
        if not self.systemc and not model.startswith('acc') and not model.endswith('AT'):
            dumpCode += 'dumpInfo.simulationTime = curCycle;'
        else:
            dumpCode += 'dumpInfo.simulationTime = sc_time_stamp().to_double();'
        dumpCode += """
dumpInfo.programCounter = this->""" + self.memory[3] + """;
dumpInfo.address = address;
dumpInfo.val = (char)datum;
this->dumpFile.write((char *)&dumpInfo, sizeof(MemAccessType));
"""
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCode + checkWatchPointCode + '*(' + str(archByteType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;\n' + dumpCode)
        writeBody.addInclude('memAccessType.hpp')
        datumParam = cxx_writer.writer_code.Parameter('datum', archByteType)
        writeDecl = cxx_writer.writer_code.Method('write_byte', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam], noException = True)
        memoryElements.append(writeDecl)
        writeBody = cxx_writer.writer_code.Code(writeMemAliasCode + checkAddressCodeException + checkWatchPointCode + '*(' + str(archByteType.makePointer()) + ')(this->memory + (unsigned long)address) = datum;\n' + dumpCode)
        writeBody.addInclude('memAccessType.hpp')
        datumParam = cxx_writer.writer_code.Parameter('datum', archByteType)
        writeDecl = cxx_writer.writer_code.Method('write_byte_dbg', writeBody, cxx_writer.writer_code.voidType, 'pu', [addressParam, datumParam])
        memoryElements.append(writeDecl)

        lockDecl = cxx_writer.writer_code.Method('lock', emptyBody, cxx_writer.writer_code.voidType, 'pu')
        memoryElements.append(lockDecl)
        unlockDecl = cxx_writer.writer_code.Method('unlock', emptyBody, cxx_writer.writer_code.voidType, 'pu')
        memoryElements.append(unlockDecl)
        endOfSimBody = cxx_writer.writer_code.Code("""if(this->dumpFile){
           this->dumpFile.flush();
           this->dumpFile.close();
        }
        """)
        endOfSimDecl = cxx_writer.writer_code.Method('end_of_simulation', endOfSimBody, cxx_writer.writer_code.voidType, 'pu')
        memoryElements.append(endOfSimDecl)

        constructorParams = [cxx_writer.writer_code.Parameter('size', cxx_writer.writer_code.uintType)]
        constructorInit = ['size(size)']

        arrayAttribute = cxx_writer.writer_code.Attribute('memory', cxx_writer.writer_code.charPtrType, 'pri')
        memoryElements.append(arrayAttribute)

        if not self.systemc and not model.startswith('acc') and not model.endswith('AT'):
            cycleAttribute = cxx_writer.writer_code.Attribute('curCycle', cxx_writer.writer_code.uintType.makeRef(), 'pri')
            constructorParams.append(cxx_writer.writer_code.Parameter('curCycle', cxx_writer.writer_code.uintType.makeRef()))
            constructorInit.append('curCycle(curCycle)')
            memoryElements.append(cycleAttribute)

        sizeAttribute = cxx_writer.writer_code.Attribute('size', cxx_writer.writer_code.uintType, 'pri')
        memoryElements.append(sizeAttribute)
        dumpFileAttribute = cxx_writer.writer_code.Attribute('dumpFile', cxx_writer.writer_code.ofstreamType, 'pri')
        memoryElements.append(dumpFileAttribute)
        memoryElements += aliasAttrs
        memoryElements.append(cxx_writer.writer_code.Attribute(self.memory[3], resourceType[self.memory[3]].makeRef(), 'pri'))
        pcRegParam = [cxx_writer.writer_code.Parameter(self.memory[3], resourceType[self.memory[3]].makeRef())]
        pcRegInit = [self.memory[3] + '(' + self.memory[3] + ')']
        localMemDecl = cxx_writer.writer_code.ClassDeclaration('LocalMemory', memoryElements, [memoryIfDecl.getType()], namespaces = [namespace])
        constructorBody = cxx_writer.writer_code.Code("""this->memory = new char[size];
            this->debugger = NULL;
            this->dumpFile.open("memoryDump.dmp", ios::out | ios::binary | ios::ate);
            if(!this->dumpFile){
                THROW_EXCEPTION("Error in opening file memoryDump.dmp for writing");
            }
        """)
        publicMemConstr = cxx_writer.writer_code.Constructor(constructorBody, 'pu', constructorParams + aliasParams + pcRegParam, constructorInit + aliasInit + pcRegInit)
        localMemDecl.addConstructor(publicMemConstr)
        destructorBody = cxx_writer.writer_code.Code("""delete [] this->memory;
        if(this->dumpFile){
           this->dumpFile.flush();
           this->dumpFile.close();
        }
        """)
        publicMemDestr = cxx_writer.writer_code.Destructor(destructorBody, 'pu', True)
        localMemDecl.addDestructor(publicMemDestr)
        classes.append(localMemDecl)

    return classes
