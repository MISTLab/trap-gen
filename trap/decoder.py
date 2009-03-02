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

try:
    import networkx as NX
except:
    import traceback
    traceback.print_exc()
    raise Exception('Error occurred during the import of module networkx, required for the creation of the decoder. Please correctly install the module, at least version 0.36 required')

def expandPatterns(curPattern, genericPattern, tablePattern):
    # taken in input the current pattern and the generic one,
    # it computes all the possible combinations of the pattern
    if len(curPattern) < len(genericPattern):
        if tablePattern[len(curPattern)] == 1:
            if genericPattern[len(curPattern)] == None:
                return expandPatterns(curPattern + [1], genericPattern, tablePattern) + expandPatterns(curPattern + [0], genericPattern, tablePattern)
            else:
                return expandPatterns(curPattern + [genericPattern[len(curPattern)]], genericPattern, tablePattern)
        else:
            return expandPatterns(curPattern + [None], genericPattern, tablePattern)
    else:
        return [curPattern]

def bitStringUnion(bitString, noCare = None):
    """Given a list of bitstring it computes
    their union using, as an answer, another bitstring
    expressed with three state logic"""
    maxLen = 0
    for curPattern in bitString:
        if len(curPattern) > maxLen:
            maxLen = len(curPattern)
    paddedbitString = []
    for curPattern in bitString:
        if len(curPattern) < maxLen:
            paddedbitString.append(list(curPattern) + [None for i in range(len(curPattern), maxLen)])
        else:
            paddedbitString.append(curPattern)
    validPattern = []
    for curPattern in paddedbitString:
        for i in range(0, len(curPattern)):
            if len(validPattern) > i:
                if validPattern[i] != curPattern[i]:
                    validPattern[i] = noCare
            else:
                validPattern.append(curPattern[i])
    return validPattern

def bitStringValid(bitStrings, noCare = None):
    """Given a list of bitstring it computes
    which bits are different from don't-care in
    every bitstring; I associate 1 to that bit"""
    validPattern = []
    for curPattern in bitStrings:
        for i in range(0, len(curPattern)):
            if len(validPattern) > i:
                if validPattern[i] is None or curPattern[i] is None:
                    validPattern[i] = noCare
            else:
                if curPattern[i] != None:
                    validPattern.append(1)
                else:
                    validPattern.append(noCare)
    return validPattern

def patternLen(pattern):
    """given a list of patterns (bit strings)
    it determines the maximum length"""
    maxLen = 0
    for i in pattern:
        if len(i) > maxLen:
            maxLen = len(i)
    return maxLen

class SplitFunction:
    """Represents the split function of a decoding node; it can either be
    a table split function or a pattern function"""
    def __init__(self, pattern = None, table = None):
        self.pattern = pattern
        self.table = table

    def toCode(self):
        mask = ''
        value = ''
        if self.pattern:
            for i in reversed(self.pattern):
                if i !=  None:
                    value += str(i)
                    mask += '1'
                else:
                    value += '0'
                    mask += '0'
            return (hex(int(mask, 2)), hex(int(value, 2)))
        if self.table:
            for i in reversed(self.table):
                mask += str(i)
            return hex(int(mask, 2))

    def __repr__(self):
        retVal = ''
        if self.pattern:
            for i in reversed(self.pattern):
                if i !=  None:
                    retVal += str(i)
                else:
                    retVal += '-'
            return retVal
        if self.table:
            for i in reversed(self.table):
                if i !=  0:
                    retVal += str(i)
                else:
                    retVal += '-'
            return retVal

    def __str__(self):
        return repr(self)

class DecodingNode:
    def __init__(self, patterns):
        self.patterns = patterns
        self.splitFunction = None
        self.instrId = None

    def __cmp__(self, other):
        # returns the outcome of the comparison between an
        # instance of the current object and of another one
        if list(self.patterns) == list(other.patterns) and self.splitFunction == other.splitFunction and self.instrId == other.instrId:
            return 0
        if len(self.patterns) < len(other.patterns):
            return -1
        return 1

    def __eq__(self, other):
        # returns the outcome of the comparison between an
        # instance of the current object and of another one
        if not isinstance(other, type(self)):
            return False
        return list(self.patterns) == list(other.patterns) and self.splitFunction == other.splitFunction and self.instrId == other.instrId

    def __ne__(self, other):
        # returns the outcome of the comparison between an
        # instance of the current object and of another one
        if not isinstance(other, type(self)):
            return True
        return not self == other

    def __hash__(self):
        # returns a hash of the object, necessary for the
        # utilization as a graph node
        return hash(str(self.patterns))

    def __repr__(self):
        retVal = ''
        if self.instrId != None:
            retVal += 'id=' + str(self.instrId) + ' ** '
        if self.splitFunction:
            retVal += str(self.splitFunction) + ' ** '
        # now I compute a summary of the patterns
        # associated with this node and then I
        # add it to the representation
        validPattern = bitStringUnion([i[0] for i in reversed(self.patterns)], 'x')
        for i in validPattern:
            if i !=  None:
                retVal += str(i)
            else:
                retVal += '-'
        return retVal + ''

    def __str__(self):
        # Returns a representation of the current node
        # in the dot language
        return repr(self)

class HuffmanNode:
    def __init__(self, frequency, count = 1):
        self.frequency = frequency
        self.count = count
    def __repr__(self):
        return str(self.frequency) + ' -- ' + str(self.count)
    def __str__(self):
        return repr(self)

class decoderCreator:
    """Taking as input the different instructions with the associated
    bitstrings, this class contains all the necessary methods to create
    a decoder, so a function which takes an arbitraty bitstring in input and
    associates it with an instruction
    The decoder is created according to the algorithm described by Qin and Malik in
    Automated Synthesis of Efficient Binary Decodes for Retargetable Software Toolkits
    """

    def __init__(self, instructions, subInstructions, memPenaltyFactor = 2):
        # memPenaltyFactor represent how much the heuristic has to take
        # into account memory consumption: the lower the more memory is
        # consumed by the created decoder.
        self.memPenaltyFactor = memPenaltyFactor
        self.instrId = {}
        self.instrName = {}
        self.instrSub = {}
        self.instrPattern = []
        # Now, given the frequencies, I compute the probabilities
        # for each instruction
        self.minFreq = 0
        self.totalCount = 1
        if instructions:
            self.minFreq = instructions.values()[0].frequency
            self.totalCount = 0
        for instr in instructions.values():
            self.totalCount += instr.frequency
            if instr.frequency < self.minFreq:
                self.minFreq = instr.frequency
        # for each instruction I get the ID and the machine
        # code
        self.instrNum = len(instructions)
        # Note how the most significant bit of the bitstring is
        # the first one of instr.bitstring. So, in order to correctly
        # perform the computation I reverse the bistring and perform
        # the calculation. At the end, when it is time to print the
        # the decoder into C++ code, I reverse again the patterns so
        # that the decoder is correctly printed
        for name, instr in instructions.items():
            if not name in subInstructions.keys():
                revBitstring = list(instr.bitstring)
                revBitstring.reverse()
                self.instrName[instr.id] = name
                self.instrSub[instr.id] = instr.subInstructions
                self.instrId[instr.id] = (revBitstring, float(instr.frequency)/float(self.totalCount))
                self.instrPattern.append((revBitstring, float(instr.frequency)/float(self.totalCount)))
        if float(NX.__version__) < 0.99:
            self.decodingTree = NX.XDiGraph()
        else:
            self.decodingTree = NX.DiGraph()
        self.computeIllegalBistreams()
        self.computeDecoder()

    def getSubInstrCode(self, subInstructions):
        code = ''
        for instr in subInstructions:
            revBitstring = list(instr.bitstring)
            mask = ''
            value = ''
            for i in revBitstring:
                if i == None:
                    mask += '0'
                else:
                    mask += '1'
                if i == 1:
                    value += '1'
                else:
                    value += '0'
            code += 'if((instrCode & ' + hex(int(mask, 2)) + ') == ' + hex(int(value, 2)) + ' ){\n// Instruction ' + instr.name + '\nreturn ' + str(instr.id) + ';\n}\n'
        return code

    def createPatternDecoder(self, subtree):
        if subtree.instrId:
            if subtree.instrId != -1:
                return self.getSubInstrCode(self.instrSub[instrId]) + '// Instruction ' + self.instrName[subtree.instrId] + '\nreturn ' + str(subtree.instrId) + ';\n'
            else:
                return '// Non-valid pattern\nreturn ' + str(self.instrNum) + ';\n'
        if self.decodingTree.out_degree(subtree) != 2:
            raise Exception('subtree ' + str(subtree) + ' should have two out edges, while it has ' + str(self.decodingTree.out_degree(subtree)))
        if float(NX.__version__) < 0.99:
            outEdges = self.decodingTree.edges(subtree)
        else:
            outEdges = self.decodingTree.edges(subtree, data = True)
        (mask, value) = subtree.splitFunction.toCode()
        if outEdges[0][-1][-1] > outEdges[1][-1][-1]:
            nodeIf = outEdges[0][1]
            nodeElse = outEdges[1][1]
            if outEdges[0][-1][0] == 1:
                compareFun = '=='
            else:
                compareFun = '!='
        else:
            nodeIf = outEdges[1][1]
            nodeElse = outEdges[0][1]
            if outEdges[1][-1][0] == 1:
                compareFun = '=='
            else:
                compareFun = '!='
        code = 'if((instrCode & ' + mask + ') ' + compareFun + ' ' + value + '){\n'
        if nodeIf.instrId != None:
            if nodeIf.instrId != -1:
                #code += '\n' + str(nodeIf.patterns) + '\n'
                code += self.getSubInstrCode(self.instrSub[nodeIf.instrId]) + '// Instruction ' + self.instrName[nodeIf.instrId] + '\nreturn ' + str(nodeIf.instrId) + ';\n'
            else:
                code += '// Non-valid pattern\nreturn ' + str(self.instrNum) + ';\n'
        elif nodeIf.splitFunction.pattern:
            #code += '\n' + str(nodeIf.patterns) + '\n'
            code += self.createPatternDecoder(nodeIf)
        else:
            #code += '\n' + str(nodeIf.patterns) + '\n'
            code += self.createTableDecoder(nodeIf)
        code += '}\n'
        code += 'else{\n'
        if nodeElse.instrId != None:
            if nodeElse.instrId != -1:
                #code += '\n' + str(nodeElse.patterns) + '\n'
                code += self.getSubInstrCode(self.instrSub[nodeElse.instrId]) + '// Instruction ' + self.instrName[nodeElse.instrId] + '\nreturn ' + str(nodeElse.instrId) + ';\n'
            else:
                code += '// Non-valid pattern\nreturn ' + str(self.instrNum) + ';\n'
        elif nodeElse.splitFunction.pattern:
            #code += '\n' + str(nodeElse.patterns) + '\n'
            code += self.createPatternDecoder(nodeElse)
        else:
            #code += '\n' + str(nodeElse.patterns) + '\n'
            code += self.createTableDecoder(nodeElse)
        code += '}\n'
        return code

    def createTableDecoder(self, subtree):
        if subtree.instrId:
            if subtree.instrId != -1:
                return self.getSubInstrCode(self.instrSub[instrId]) + '// Instruction ' + self.instrName[subtree.instrId] + '\nreturn ' + str(subtree.instrId) + ';\n'
            else:
                return '// Non-valid pattern\nreturn ' + str(self.instrNum) + ';\n'
        if float(NX.__version__) < 0.99:
            outEdges = self.decodingTree.edges(subtree)
        else:
            outEdges = self.decodingTree.edges(subtree, data = True)
        mask = subtree.splitFunction.toCode()
        outEdges = sorted(outEdges, lambda x, y: cmp(y[-1][-1], x[-1][-1]))
        if '0' in  mask[2:]:
            code = 'switch(instrCode & ' + mask + '){\n'
        else:
            code = 'switch(instrCode){\n'
        for edge in outEdges:
            code += 'case ' + hex(edge[-1][0]) + ':{\n'
            if edge[1].instrId != None:
                if edge[1].instrId != -1:
                    #code += '\n' + str(edge[1].patterns) + '\n'
                    code += self.getSubInstrCode(self.instrSub[edge[1].instrId]) + '// Instruction ' + self.instrName[edge[1].instrId] + '\nreturn ' + str(edge[1].instrId) + ';\n'
                else:
                    code += '// Non-valid pattern\nreturn ' + str(self.instrNum) + ';\n'
            elif edge[1].splitFunction.pattern:
                #code += '\n' + str(edge[1].patterns) + '\n'
                code += self.createPatternDecoder(edge[1])
            else:
                #code += '\n' + str(edge[1].patterns) + '\n'
                code += self.createTableDecoder(edge[1])
            code += 'break;}\n'
        code += 'default:{\n// Non-valid pattern\nreturn ' + str(self.instrNum) + ';\n}\n'
        code += '}\n'
        return code

    def getCPPClass(self, fetchSizeType):
        # Creates the representation of the decoder as a C++ class
        import cxx_writer
        from isa import resolveBitType
        # OK: now I simply have to go over the decoding tree
        if self.rootNote.splitFunction.pattern:
            codeString = self.createPatternDecoder(self.rootNote)
        else:
            codeString = self.createTableDecoder(self.rootNote)
        code = cxx_writer.writer_code.Code(codeString)
        code.addInclude('utils.hpp')
        parameters = [cxx_writer.writer_code.Parameter('instrCode', fetchSizeType)]
        decodeMethod = cxx_writer.writer_code.Method('decode', code, cxx_writer.writer_code.intType, 'pu', parameters)
        decodeClass = cxx_writer.writer_code.ClassDeclaration('Decoder', [decodeMethod])
        return decodeClass

    def getCPPTests(self):
        # Creates the tests for the decoder; I normally create the
        # tests with boost_test_framework.
        # What I have to do is feeding all the instruction patterns
        # (including all the non valid ones) to the decoder and check
        # that they are correctly decoded. I choose random values
        # for the non-care bits
        import cxx_writer
        import random, math
        ranGen = random.SystemRandom()
        allTests = []
        testCount = 0
        for instrId, instruction in self.instrId.items():
            code = 'Decoder dec;\n'
            pattern = instruction[0]
            try:
                pattern[0][0]
                pattern = pattern[0]
            except:
                pass
            for i in range(0, len(pattern)):
                if pattern[i] == None:
                    if ranGen.random() > 0.5:
                        pattern[i] = '1'
                    else:
                        pattern[i] = '0'
                else:
                    pattern[i] = str(pattern[i])
            if instrId == -1:
                expectedId = self.instrNum
            else:
                # Now I have to check for the presence of a sub-instruction and, in case,
                # correct the target of the test
                expectedId = None
                for instr in self.instrSub[instrId]:
                    found = True
                    for i in range(0, len(pattern)):
                        if instr.bitstring[i] != None and pattern[i] != instr.bitstring[i]:
                            found = False
                    if found:
                        expectedId = instr.id
                        break
                if expectedId == None:
                    expectedId = instrId
            pattern.reverse()
            if instrId != -1:
                code += '// Checking Instruction ' + self.instrName[instrId] + '\n'
            else:
                code += '// Checking Invalid Instruction\n'
            code += 'BOOST_CHECK_EQUAL(dec.decode( ' + hex(int(''.join(pattern), 2)) + ' ), ' + str(expectedId) + ');\n'
            curTest = cxx_writer.writer_code.Code(code)
            curTest.addInclude(['boost/test/test_tools.hpp', 'decoder.hpp'])
            if instrId != -1:
                testName = self.instrName[instrId] + '_' + str(testCount) + '_decode'
            else:
                testName = 'Invalid_' + str(testCount) + '_decode'
            curTestFunction = cxx_writer.writer_code.Function(testName, curTest, cxx_writer.writer_code.voidType)
            from procWriter import testNames
            testNames.append(testName)
            allTests.append(curTestFunction)
            testCount += 1
        return allTests

    # Here are some helper methods used in the creation of the decoder; they
    # are called by the constructor
    def computationalCost(self, subtree):
        # Computes the metric for estimating the computational cost of the decoding subtree.
        # In this version the height of the huffman tree is used as an
        # estimation of this cost
        # First of all I have to create the huffman nodes and order them
        # in a list
        if not subtree.patterns:
            return 0
        huffmanList = []
        for i in subtree.patterns:
            huffmanList.append(HuffmanNode(i[1]))
        huffmanList = sorted(huffmanList, lambda x, y: cmp(x.frequency, y.frequency))
        while len(huffmanList) > 1:
            newElem = HuffmanNode(huffmanList[0].frequency + huffmanList[1].frequency, max(huffmanList[0].count, huffmanList[1].count) + 1)
            huffmanList = huffmanList[2:]
            huffmanList.append(newElem)
            huffmanList = sorted(huffmanList, lambda x, y: cmp(x.frequency, y.frequency))
        return huffmanList[0].count

    def computePatternCost(self, subtree, curMask, newBit, newBitVal):
        # Given the current leaf node, it computes the cost
        # that would derive from using the pattern given
        # by curMask + [newBit] for the split of the
        # current node.
        # it also phisically performs the split, returning
        # curCost, curLeaves, where the leaves are formed by
        # the subtrees and the respective splitting criteria (pattern
        # equal or not)
        if newBit in curMask[0]:
            raise Exception('Bit ' + newBit + ' is specified both by the current mask and as new bit')
        eqPattern = []
        neqPattern = []
        for pattern in subtree.patterns:
            added = False
            for i in range(0, len(curMask[0])):
                if (pattern[0][curMask[0][i]] != None) and (pattern[0][curMask[0][i]] != curMask[1][i]):
                    neqPattern.append(pattern)
                    added = True
                    break
            if not added:
                if (pattern[0][newBit] != None) and (pattern[0][newBit] != newBitVal):
                    neqPattern.append(pattern)
                else:
                    dontCare = False
                    for i in curMask[0]:
                        if pattern[0][i] is None:
                            dontCare = True
                            break
                    if dontCare or (pattern[0][newBit] is None):
                        neqPattern.append(pattern)
                        eqPattern.append(pattern)
                    else:
                        eqPattern.append(pattern)
        # Ok, I have created the two splitted nodes
        eqSubtree = DecodingNode(eqPattern)
        neqSubtree = DecodingNode(neqPattern)
        eqProb = 1.0
        neqProb = 1.0
        for i in eqPattern:
            eqProb += i[1]
        for i in neqPattern:
            neqProb += i[1]
        memoryCost = float(len(eqPattern) + len(neqPattern) - 1)/float(len(subtree.patterns) -1)
        import math
        cost = 1 + self.memPenaltyFactor*math.log(memoryCost, 2) + (eqProb/(neqProb + eqProb))*self.computationalCost(eqSubtree) + (neqProb/(neqProb + eqProb))*self.computationalCost(neqSubtree)
        if len(eqPattern) == 0 or len(neqPattern) == 0 or len(neqPattern) == len(subtree.patterns) or len(eqPattern) == len(subtree.patterns):
            return (None, None)
        return (cost, ((eqSubtree, (1, eqProb)), (neqSubtree, (0, neqProb))))

    def computeTableCost(self, subtree, startTable, curTableLen):
        # Given the current leaf node, it computes the cost
        # that would derive from using the current table function
        # for the split
        # it also phisically performs the split, returning
        # curCost, curLeaves where the lieaves are formed by the
        # subtrees and by the value of the table; I also associate
        # the sum of the frequencies in each leaf subtree
        import math
        maxPatternLen = patternLen([i[0] for i in subtree.patterns])
        tablePattern = []
        for i in range(0, maxPatternLen):
            if i >= startTable and i < startTable + curTableLen:
                tablePattern.append(1)
            else:
                tablePattern.append(0)
        leavesPatterns = {}
        for pattern in subtree.patterns:
            # now, in case some of the elements of the pattern, corresponding to the
            # the table elements are don't care, it means that I need to assign them to
            # the different table elements
            expandedPatterns = expandPatterns([], pattern[0], tablePattern)
            for curPattern in expandedPatterns:
                curTableVal = 0
                for i in range(0, len(tablePattern)):
                    if tablePattern[i] == 1:
                        curTableVal += int(curPattern[i]*math.pow(2, i))
                if leavesPatterns.has_key(curTableVal):
                    leavesPatterns[curTableVal].append(pattern)
                else:
                    leavesPatterns[curTableVal] = [pattern]
        for key, value in leavesPatterns.items():
            if len(value) == len(subtree.patterns):
                return (None, None)
        # Ok, I have created the splitted nodes
        cost = 0
        retTuple = []
        probs = {}
        probTotal = 1.0
        memoryCost = 1 + math.pow(2, curTableLen)
        for key, value in leavesPatterns.items():
            for i in value:
                if probs.has_key(key):
                    probs[key] += i[1]
                else:
                    probs[key] = i[1]
                probTotal += i[1]
            memoryCost += len(value) -1
        memoryCost = float(memoryCost + 1.0)/float(len(subtree.patterns) -1)
        import math
        for key, value in leavesPatterns.items():
            curNode = DecodingNode(value)
            cost += (probs[key]/probTotal)*self.computationalCost(curNode)
            retTuple.append((curNode, (key, probs[key])))
        cost += 1 + self.memPenaltyFactor*math.log(memoryCost, 2)
        return (cost, retTuple)

    def findBestPattern(self, subtree):
        # Given the subtree, it finds the best pattern for
        # the split of the top node of the subtree
        # It returns (bestPattern, leavesPattern, costPattern), the best
        # pattern for the split, the splitted nodes and the cost of
        # the split
        # First of all I have to compute the union of the pattern
        # then I take, one by one, the bits and build the pattern
        # with them: I have to evaluate candidate pattern one
        # by one
        bestCost = None
        tabuBits = []
        chosenBits = []
        chosenBitVals = []
        maxPatternLen = patternLen([i[0] for i in subtree.patterns])
        bestBit = 0
        bestBitVal = 0
        bestLeaves = None
        while bestBit != None:
            bestBit = None
            for bit in range(0, maxPatternLen):
                if not bit in chosenBits and not bit in tabuBits:
                    curCost0, curLeaves0 = self.computePatternCost(subtree, (chosenBits, chosenBitVals), bit, 0)
                    curCost1, curLeaves1 = self.computePatternCost(subtree, (chosenBits, chosenBitVals), bit, 1)
                    if not curLeaves0 or not curLeaves1:
                        if not chosenBits:
                            tabuBits.append(bit)
                        continue
                    if curCost0 > curCost1:
                        curCost = curCost1
                        curLeaves = curLeaves1
                        curBitVal = 1
                    else:
                        curCost = curCost0
                        curLeaves = curLeaves0
                        curBitVal = 0
                    if bestCost is None or bestCost > curCost:
                        bestBit = bit
                        bestBitVal = curBitVal
                        bestCost = curCost
                        bestLeaves = curLeaves
            if bestBit != None:
                chosenBits.append(bestBit)
                chosenBitVals.append(bestBitVal)
        # Now we return the tuple bestPattern, leavesPattern, costPattern
        # where bestPattern rappresents the best split function for this
        # subtree, leavesPattern the nodes directly descending from
        # the current subtre according to the split function and, finally,
        # costPattern is the cost of this split
        matchPattern = []
        for i in range(0, maxPatternLen):
            matchPattern.append(None)
        for i in range(0, len(chosenBits)):
            matchPattern[chosenBits[i]] = chosenBitVals[i]
        if bestCost == None:
            return(None, None, None)
        return (SplitFunction(pattern = matchPattern), bestLeaves, bestCost)

    def findBestTable(self, subtree):
        # Given the subtree, it finds the best table for
        # the split of the top node of the subtree
        # It returns (bestTable, leavesTable, costTable), the best
        # table for the split, the splitted nodes and the cost of
        # the split
        # We evaluate all the 2-bit tables, then the 3-bit tables,
        # etc.
        # I have to determine the best m-bits candidate,
        # where 2 < m < len(importantBits == 1)
        maxPatternLen = patternLen([i[0] for i in subtree.patterns])
        bestCost = None
        bestLeaves = None
        bestMask = ()
        curTableLen = 2
        improvement = True
        while curTableLen <= maxPatternLen and improvement:
            improvement = False
            for startTable in range(0, maxPatternLen - curTableLen + 1):
                curCost, curLeaves = self.computeTableCost(subtree, startTable, curTableLen)
                if not curCost:
                    continue
                if bestCost is None or curCost < bestCost:
                    bestMask = (startTable, curTableLen)
                    bestCost = curCost
                    bestLeaves = curLeaves
                    improvement = True
            curTableLen += 1
        if not bestMask:
            return (None, None, None)
        # Ok, found the best table for decoding
        tablePattern = []
        foundMask = False
        encounteredImportant = 0
        for i in range(0, maxPatternLen):
            if i >= bestMask[0] and i < bestMask[0] + bestMask[1]:
                tablePattern.append(1)
                foundMask = True
            else:
                tablePattern.append(0)
        if not foundMask:
            return (None, None, None)
        return (SplitFunction(table = tablePattern), bestLeaves, bestCost)

    def computeIllegalBistreams(self):
        # From all the instructions it computes the illegal patterns as
        # the complement of the union of all the valid patterns; logic
        # minimization follows. In order to implement this I can simply
        # perform the union among the patters of the instructions (two
        # different bits yeld don't care) and the complement it
        validPattern = bitStringUnion([i[0] for i in self.instrPattern])
        self.complementPattern(validPattern, 0)

    def complementPattern(self, pattern, bit):
        # Given a pattern it computes the negation starting from bit bit
        # this function is recursive. When each computed negated pattern is
        # added to self.instrId and self.instrPattern
        if bit == len(pattern):
            return
        import copy
        flipped = False
        for i in range(bit, len(pattern)):
            if flipped:
                pattern[i] = None
            elif pattern[i] == 1:
                self.complementPattern(copy.deepcopy(pattern), i + 1)
                pattern[i] = 0
                flipped = True
            elif pattern[i] == 0:
                self.complementPattern(copy.deepcopy(pattern), i + 1)
                pattern[i] = 1
                flipped = True
        if flipped and pattern:
            if self.instrId.has_key(-1):
                self.instrId[-1][0].append(copy.deepcopy(pattern))
            else:
                self.instrId[-1] = ([copy.deepcopy(pattern)], (float(self.minFreq)/float(100))/float(self.totalCount))
            self.instrPattern.append((copy.deepcopy(pattern), (float(self.minFreq)/float(100))/float(self.totalCount)))

    def computeDecoder(self):
        # Actually computes the decoder; the algorithm is:
        # -- Add fake instructions corresponding to the illegal bitstreams (done by computeIllegalBistreams)
        # -- Start with the decoding tree composed of all the instructions
        # -- For each leaf of the tree:
        # --     call findBestPattern (use memoryCost and huffmanHeight to compute the cost)
        # --     call findBestTable (use memoryCost and huffmanHeight to compute the cost)
        # --     pick up the best one (use memoryCost and huffmanHeight to compute the cost)
        # --     split the tree creating new leafs
        # --     iterate on the new leafs
        # --     go on until each leaf is composed of only one instruction
        # Note how the algorithm is implemented in a recursive way
        # Now I have to compute the starting node of the decoding tree;
        # it will contain all the instructions
        self.rootNote = DecodingNode(self.instrPattern)
        self.decodingTree.add_node(self.rootNote)
        self.computeDecoderRec(self.rootNote)

    def computeDecoderRec(self, subtree):
        # Given the subtree recursively computes the decodes for
        # the given subtree part
        # If there is only an instruction in the current subtree node
        # I simply tag the node to be a leaf and I associate to it the
        # id of the instruction. If more than one instruction is
        # present in the current subtree node, but all of them are tagged
        # with the same ID, then I tag the node as a leaf and I associate
        # to it the ID

        # First of all I check if the instructions in the current
        # node refer to more than one class
        curClass = None
        different = False
        for instr in subtree.patterns:
            for instrId, instrVals in self.instrId.items():
                if instrVals[0] == instr[0]:
                    if curClass == None:
                        curClass = instrId
                    elif curClass != instrId:
                        different = True
                    break
            if different:
                break
        if not different:
            # I simply have to tag this subtree with the instruction ids
            if curClass is None:
                subtree.instrId = -1
            else:
                subtree.instrId = curClass
            return
        # If I'm here it means that I still have to split the node
        bestPattern, leavesPattern, costPattern = self.findBestPattern(subtree)
        bestTable, leavesTable, costTable = self.findBestTable(subtree)
        if not bestTable and not bestPattern:
            curInstrNames = []
            for instr in subtree.patterns:
                for instrId, instrVals in self.instrId.items():
                    if instrVals[0] == instr[0]:
                        curInstrNames.append(self.instrName[instrId])
                        break
            raise Exception('Error, more than one instruction in the current decoder but no table or pattern decoder found --> ' + str(curInstrNames))
        if bestTable and not bestPattern:
            curInstrNames = []
            for instr in subtree.patterns:
                for instrId, instrVals in self.instrId.items():
                    if instrVals[0] == instr[0]:
                        curInstrNames.append(self.instrName[instrId])
                        break
            raise Exception('Error, more than one instruction in the current decoder but no pattern decoder found --> ' + str(curInstrNames))
        if bestTable and costPattern > costTable and len(leavesTable) > 1:
            # It is better to split on the table
            subtree.splitFunction = bestTable
            for i in leavesTable:
                self.decodingTree.add_node(i[0])
                self.decodingTree.add_edge(subtree, i[0], i[1])
                self.computeDecoderRec(i[0])
        else:
            # It is better to split on the pattern
            subtree.splitFunction = bestPattern
            if len(leavesPattern) > 1:
                for i in leavesPattern:
                    self.decodingTree.add_node(i[0])
                    self.decodingTree.add_edge(subtree, i[0], i[1])
                    self.computeDecoderRec(i[0])

    def printDecoder(self, fileName):
        try:
            NX.write_dot(self.decodingTree, fileName)
        except:
            import traceback
            traceback.print_exc()
            print ('Error in printing the decoding tree on file ' + fileName)
