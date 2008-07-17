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

def getCPPInstr(self, model):
    # Returns the code implementing the current instruction: we have to provide the
    # implementation of all the abstract methods and call from the behavior method
    # all the different behaviors contained in the type hierarchy of this class
    # TODO:
    return None

def getCPPInstrTest(self, processor, model):
    # Returns the code testing the current instruction: note that a test
    # consists in setting the instruction variables, performing the instruction
    # behavior and then comparing the registers with what we expect.
    tests = []
    for test in self.tests:
        code = 'BOOST_AUTO_TEST_CASE( test_' + self.name + '_' + str(len(tests)) + ' ){\n'
        # TODO: first of all I create the instance of the instruction and of all the
        # processor elements
        for resource, value in test[0]:
            # I set the initial value of the local resources
            pass
        for resource, value in test[1]:
            # I set the initial value of the global resources
            pass
        # TODO: I perform the operation
        for resource, value in test[2]:
            # I check the value of the listed resources to make sure that the
            # computation executed correctly
            pass
        code += '}\n\n'
        curTest = cxx_writer.writer_code.Code(code, ['boost/test/auto_unit_test.hpp', 'boost/test/test_tools.hpp'])
        tests.append(curTest)
    return tests

def getCPPClasses(self, processor, modelType):
    # TODO: remember that we also need to print the INVALID
    # instruction (how do we deal with the cycle accurate? when do we
    # raise the error there?)
    # I go over each instruction and print the class representing it;
    # note how the instruction base class is part of the runtime
    from isa import resolveBitType
    archWordType = resolveBitType('BIT<' + str(processor.wordSize*processor.byteSize) + '>')
    classes = []
    # First of all I create the base instruction type: note that it contains references
    # to the architectural elements
    instructionType = cxx_writer.writer_code.Type('Instruction')
    instructionElements = []
    emptyBody = cxx_writer.writer_code.Code('')
    behaviorDecl = cxx_writer.writer_code.Method('behavior', emptyBody, cxx_writer.writer_code.uintType, 'pu', pure = True)
    instructionElements.append(behaviorDecl)
    replicateDecl = cxx_writer.writer_code.Method('replicate', emptyBody, instructionType.makePointer(), 'pu', pure = True)
    instructionElements.append(replicateDecl)
    setparamsParam = cxx_writer.writer_code.Parameter('bitString', archWordType.makeRef().makeConst())
    setparamsDecl = cxx_writer.writer_code.Method('setParams', emptyBody, cxx_writer.writer_code.voidType, 'pu', [setparamsParam], pure = True)
    instructionElements.append(setparamsDecl)
    # TODO: we have to check all the operation and the behaviors of the instructions and build
    # the instruction hierarchy in order to group them depending on which instructions use
    # them: the ones used by all in the base instruction, then if set A use another method, we
    # crea the superclass A, etc.
    # TODO: create references to the architectural elements contained in the processor
    instructionDecl = cxx_writer.writer_code.ClassDeclaration('Instruction', instructionElements)
    classes.append(instructionDecl)
    
    # Now I go over all the other instructions and I declare them
    for instr in self.instructions.values():
        classes.append(instr.getCPPClass(modelType))
    return classes

def getCPPTests(self, processor, modelType):
    # for each instruction I print the test: I do have to add some custom
    # code at the beginning in order to being able to access the private
    # part of the instructions
    tests = []
    includeCode = cxx_writer.writer_code.Code('#define private public\n#include \"instructions.hpp\"\n#undef private\n')
    tests.append(includeCode)
    for instr in self.instructions.values():
        tests.append(instr.getCPPTest(processor, modelType))
    return tests
