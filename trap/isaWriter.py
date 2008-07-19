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

# Contains, for each behavior, the type corresponding to the class which defines
# it. If a behavior is not here it means that it must be explicitly inlined
# in the instruction itself
behClass = {}

def getCppMethod(self):
    # Returns the code implementing a helper method
    return None

def getCppOperation(self):
    # Returns the code implementing a helper operation
    return None

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
    # we now have to check if there is a non-inline behavior common to all instructions:
    # in this case I declare it here in the base instruction class
    behNum = {}
    for instr in self.instructions.values():
        for behaviors in instr.postbehaviors.values() + instr.prebehaviors.values():
            for beh in behaviors:
                if behNum.has_key(beh.name):
                    behNum[beh.name][0] = behNum[beh.name][0] + 1
                else:
                    behNum[beh.name] = [1, beh]
    for behv, num in behNum.items():
        if num[0] == len(self.instructions):
            # This behavior is present in all the instructions: I declare it in
            # the base instruction class
            instructionElements.append(num[1].getCppOperation())
    # Ok, now I add the generic helper methods and operations
    for helpOp in self.helperOps + [self.beginOp, self.endOp]:
        if helpOp:
            instructionElements.append(helpOp.getCppOperation())
    for helpMeth in self.methods:
        if helpMeth:
            instructionElements.append(helpMeth.getCppMethod())
    # TODO: create references to the architectural elements contained in the processor
    instructionDecl = cxx_writer.writer_code.ClassDeclaration('Instruction', instructionElements)
    classes.append(instructionDecl)

    # we now have to check all the operation and the behaviors of the instructions and create
    # the classes for each shared non-inline behavior
    for instr in self.instructions.values():
        for behaviors in instr.postbehaviors.values() + instr.prebehaviors.values():
            for beh in behaviors:
                if not behClass.has_key(beh.name) and beh.inline:
                    behClass[beh.name] = beh.getCppOperation()

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
