####################################################################################
#                    ___           ___           ___
#        ___        /  /\         /  /\         /  /\
#       /  /\      /  /::\       /  /::\       /  /::\
#      /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
#     /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
#    /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
#   /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
#   \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
#        \  \:\   \  \:\        \  \:\        \  \:\
#         \__\/    \  \:\        \  \:\        \  \:\
#                   \__\/         \__\/         \__\/
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
    raise Exception('Error occurred during the import of module networkx, required for the creation of the decoder. Please correctly install the module')

def bitStringUnion(bitString, noCare = None):
    """Given a list of bitstring it computes
    their union using, as an answer, another bitstring
    expressed with three state logic"""
    validPattern = []
    for curPattern in bitString:
        for i in range(0, len(curPattern)):
            if len(validPattern) > i:
                if validPattern[i] != curPattern[i]:
                    validPattern[i] = noCare
            else:
                validPattern.append(curPattern[i])
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

    def __repr__(self):
        if self.pattern:
            return str(self.pattern)
        if self.table:
            return str(self.table)

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
        if self.patterns == other.patterns and self.splitFunction == other.splitFunction and self.instrId == other.instrId:
            return 0
        if len(self.patterns) < len(other.patterns):
            return -1
        return 1

    def __eq__(self, other):
        # returns the outcome of the comparison between an
        # instance of the current object and of another one
        return self.patterns == other.patterns and self.splitFunction == other.splitFunction and self.instrId == other.instrId

    def __ne__(self, other):
        # returns the outcome of the comparison between an
        # instance of the current object and of another one
        return not self == other

    def __hash__(self):
        # returns a hash of the object, necessary for the
        # utilization as a graph node
        return hash(self.patterns)

    def __repr__(self):
        retVal = ''
        if self.instrId:
            retVal += str(self.instrId) + ' -- '
        if self.splitFunction:
            retVal += str(self.splitFunction) + ' -- '
        # now I compute a summary of the patterns
        # associated with this node and then I
        # add it to the representation
        validPattern = bitStringUnion(self.patterns, 'x')
        retVal += str(validPattern)

    def __str__(self):
        # Returns a representation of the current node
        # in the dot language
        repr(self)

class decoderCreator:
    """Taking as input the different instructions with the associated
    bitstrings, this class contains all the necessary methods to create
    a decoder, so a function which takes an arbitraty bitstring in input and
    associates it with an instruction
    The decoder is created according to the algorithm described by Qin and Malik in
    Automated Synthesis of Efficient Binary Decodes for Retargetable Software Toolkits
    """

    def __init__(self, instructions, memPenaltyFactor = 0.5):
        # memPenaltyFactor represent how much the heuristic has to take
        # into account memory consumption: the lower the more memory is
        # consumed by the created decoder.
        self.instrId = {}
        self.instrPattern = []
        # Now, given the frequencies, I compute the probabilities
        # for each instruction
        self.minFreq = 0
        self.totalCount = 1
        if instructions:
            self.minFreq = instructions[0].frequency
            self.totalCount = 0
        for instr in instructions:
            self.totalCount += instr.frequency
            if instr.frequency < self.minFreq:
                self.minFreq = instr.frequency
        # for each instruction I get the ID and the machine
        # code
        for instr in instructions:
            self.instrId[instr.id] = (instr.bitstring, instr.frequency/self.totalCount)
            self.instrPattern.append(instr.bitstring)
        self.decodingTree = NX.DiGraph()
        self.computeIllegalBistreams()
        self.computeDecoder()

    def getCPPClass(self):
        # Creates the representation of the decoder as a C++ class
        pass

    # Here are some helper methods used in the creation of the decoder; they
    # are called by the constructor
    def computationalCost(self, subtree):
        # Computes the metric for estimating the computational cost of the decoding subtree.
        # In this version the height of the huffman tree is used as an
        # estimation of this cost
        pass

    def memoryCost(self, subtree):
        # Computes the memory cost of the given subtree; actually,
        # in case the split was a table, we need to add 2^m. Then
        # we also have to take the logarithm of everything
        partialCost = 1
        for node in NX.out_edges(subtree):
            partialCost += (len(node.patterns) - 1)
        return partialCost

    def computePatternCost(self, subtree, curMask, newBit, newBitVal):
        # Given the current leaf node, it computes the cost
        # that would derive from using the pattern given
        # by curMask + [newBit] for the split of the
        # current node.
        pass

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
        chosenBits = []
        chosenBitVals = []
        maxPatternLen = patternLen(subtree.patterns)
        bestBit = 0
        bestBitVal = 0
        bestLeaves = None
        while bestBit != None:
            bestBit = None
            for bit in range(0, maxPatternLen):
                if not bit in chosenBits:
                    curCost0, curLeaves0 = self.computePatternCost(subtree, chosenBits, bit, 0)
                    curCost1, curLeaves1 = self.computePatternCost(subtree, chosenBits, bit, 1)
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
            if i in chosenBits:
                matchPattern.append(chosenBitVals[i])
            else:
                matchPattern.append(None)
        return (SplitFunction(pattern = matchPattern), bestLeaves, bestCost)

    def findBestTable(self, subtree):
        # Given the subtree, it finds the best table for
        # the split of the top node of the subtree
        # It returns (bestTable, leavesTable, costTable), the best
        # table for the split, the splitted nodes and the cost of
        # the split
        # We evaluate all the 2-bit tables, then the 3-bit tables,
        # etc.
        maxPatternLen = patternLen(subtree.patterns)
        # I have to determine the best m-bits candidate,
        # where 2 < m < len(union)
        bestCost = None
        bestLeaves = None
        curTableLen = 2
        for startTable in range(0, maxPatternLen - curTableLen):
            curCost, curLeaves = self.computeTableCost(subtree, startTable, curTableLen)


    def computeIllegalBistreams(self):
        # From all the instructions it computes the illegal patterns as
        # the complement of the union of all the valid patterns; logic
        # minimization follows. In order to implement this I can simply
        # perform the union among the patters of the instructions (two
        # different bits yeld don't care) and the complement it
        validPattern = bitStringUnion(self.instrPattern)
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
                self.instrId[-1] = ([copy.deepcopy(pattern)], (self.minFreq/100)/self.totalCount)
            self.instrPattern.append(copy.deepcopy(pattern))

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
        rootNote = DecodingNode(self.instrPattern)
        self.decodingTree.add_node(rootNote)
        self.computeDecoderRec(rootNote)

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
            for instrId, instrVals in self.instrId:
                if instrVals[0] == instr:
                    if curClass == None:
                        curClass = instrId
                    elif curClass != instrId:
                        different = True
                    break
            if different:
                break
        if not different:
            # I simply have to tag this subtree with the instruction ids
            subtree.instrId = curClass
            return
        # If I'm here it means that I still have to split the node
        bestPattern, leavesPattern, costPattern = self.findBestPattern(subtree)
        bestTable, leavesTable, costTable = self.findBestTable(subtree)
        if costPattern > costTable:
            # It is better to split on the table
            subtree.splitFunction = bestTable
            if(len(leavesTable) > 1):
                for i in leavesTable:
                    self.decodingTree.add_node(i)
                    self.decodingTree.add_edge(subtree, i)
                    self.computeDecoder(i)
        else:
            # It is better to split on the pattern
            subtree.splitFunction = bestPattern
            if(len(leavesPattern) > 1):
                for i in leavesPattern:
                    self.decodingTree.add_node(i)
                    self.decodingTree.add_edge(subtree, i)
                    self.computeDecoder(i)

    def printDecoder(self, fileName):
        try:
            NX.write_dot(self.decodingTree, fileName)
        except:
            import traceback
            traceback.print_exc()
            print 'Error in printing the decoding tree on file ' + fileName
