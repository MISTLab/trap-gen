# Introduction #

TRAP (Transactional-level Retargetable Automatic Processor) is a framework for the generation of
processor simulators in C++ starting from high level descriptions. The processor description is given directly
in Python by calling the APIs of the TRAP library.
Once the description of the processor is complete, you can create the C++ code implementing the processor by
litterally executing the python module (among the ones describing your processor) containing the call to the _write_ API.

The rest of this document presents a short step-by-step How To on how to describe a processor using TRAP and
how to create the corresponding C++ code. For a more complete example look at the description of the ARM7TDMI
processor contained in folder `processor/ARM7TDMI` or at the description of the LEON3 processor in folder `processor/LEON3` (still work in
progress). In particular refer to the LEON3 for a more comprehensive overview on how to declare and describe
moderately complex pipelines.


# Details #

## Describing the Architecture ##
The architecture description consists of the indication of the _registers_, _ports_, _issue width_ of the real processor.
Not much information is needed in this section since we target the generation of **high level simulators** (more details
would be needed, for example, for the generation of RTL code).

The following code snippets are taken from file `processor/ARM7TDMI/ARMArch.py`:
```
import trap
```
Lets import the core trap modules; note that if they are not in the standard python search path we can specify
their path using the instruction `sys.path.append(_trap_path_)`.

We can then procede with the actual creation of the processor:
```
processor = trap.Processor('ARM7TDMI', version = '0.1', systemc = False, instructionCache = True, fastFetch = False)
processor.setLittleEndian()
processor.setWordsize(4, 8)
processor.setISA(ARMIsa.isa)
```
This means that the processor will be called _ARM7TDMI_ and that the current version is _0.1_. SystemC will not be used for
keeping time, so all will be executed in the same delta cycle; this option is valid only for functional descriptions and it cannot
be used if TLM ports are employed for communication with external IPs.
Note how SystemC will not be used for keeping time, but the structure of the architectural components will anyway be based on
this library. At processor construction we also indicate that the decoding instruction cache shall be used. Such a cache has nothing to do with
the cache of a real processor, it is simply a buffer holding already decoding instructions in order to avoid re-decoding them.
The use of the decoding cache consistently speeds up simulation. We also specify that the fastFetch option is not going to be used; with such
option we read from memory an instruction only the first time it is encountered: this speeds up simulation, but it has two drawbacks:
statistics regading access to memory are not correctly computed and self-modifying code cannot be simulated.
The other two instructions are self-explanatory: we are going to describe a _little endian_ system with _4_ bytes per word, _8_ bits per byte.
Finally the object hodling the _Instruction Set Architecture (ISA)_ Description is indicated.

Now we can start describing the architectural elements:
```
regBank = trap.RegisterBank('RB', 30, 32)
processor.addRegBank(regBank)
cpsrBitMask = {'N': (31, 31), 'Z': (30, 30), 'C': (29, 29), 'V': (28, 28), 'I': (7, 7), 'F': (6, 6), 'mode': (0, 3)}
cpsr = trap.Register('CPSR', 32, cpsrBitMask)
cpsr.setDefaultValue(0x000000D3)
processor.addRegister(cpsr)
```
Here we create a register bank (a group of registers) called _RB_ composed of _30_ registers each one _32_ bit wide.
Next a single register called _CPSR_ is created: it is _32_ bit wide. Note how a mask (_cpsrBitMask_) is defined: this mask easies
the access to the individual registers bits: from the ISA implementation code (see below) we can simply write `CPSR[key_mode]` to access
the first four bits of the regsiter (masks can be defined both for simple registers and register banks). We also set a default value,
which is the value that register CPSR have at processor reset; As shown
below it is possible to also specify special keywords as default values.
Other interesting register declarations, this time taken from the LEON3 processor are:
```
globalRegs = trap.RegisterBank('GLOBAL', 8, 32)
globalRegs.setConst(0, 0)
```
We declare a register bank of 8 registers, each one 32 bits wide and we specify that register 0 (the first argument) will
be constant to value 0 (the second argument): any write operation on this register will have no effect and any read
operation will always read 0. Method `setConst` also exists for simple registers.
```
yReg = trap.Register('Y', 32)
yReg.setDelay(3)
```
With this code we specify that in the functional model writes to this registers will be visible with a latency of 3 instructions:
this can be used to model the fact that, with long pipelines, writes to register happen at the end of
the pipeline while reads at the beginning. Method `setConst` also exists for register banks.

```
regs = trap.AliasRegBank('REGS', 16, 'RB[0-15]')
processor.addAliasRegBank(regs)
SP = trap.AliasRegister('SP', 'REGS[13]', offset = 0)
processor.addAliasReg(SP)
```
These lines create two aliases: one bank and one single. An alias is used (from the point of view of the processor instructions) exactly
like a normal register; the different is that, during execution, it can be remapped to point to different registers (or aliases: an alias
can also point to another alias). Aliases are useful for handling architectures which expose to the programmer only part of their registers.
Consider the ARM7 architecture: when in user mode the frame pointer _SP_ is mapped to register 13; after a switch to supervisor mode, it points
to register 15. Aliases can make this transparent to the instruction set implementation: the ISA keeps on accessing alias _SP_ which, depending
on the mode, points either to register 13 or 15.

Note how initially the 16 aliases _REGS_ point to registers _0-15_ while _SP_ to the alias _13_ in the alias bank _REGS_ (so if we change what
REGS points to, also _SP_ will point to the new target). For individual aliases we can also specify an offset: when accessing the value of the alias
we will see the value of the register it points to plus the offset.

```
PC = trap.AliasRegister('PC', 'REGS[15]')
PC.setDefaultValue(('ENTRY_POINT', 8))
processor.addAliasReg(PC)
```
As for registers, we can set default values also for aliases. In this case we use a special default value: it is the _entry point_ of the software
program which will be executed on the simulator; we also set the offset of 8 (this offset is considered just for functional description and it is
necessary in order to take into account the fact that in a functional description we do not have the pipeline). Other special values are `PROGRAM LIMIT`
(the highest address of the loaded executable code) and `PROGRAM_START` (the lowest address of the loaded executable code).

```
idMap = trap.MemoryAlias(0xFFFFFFF0, 'MP_ID')
processor.addMemAlias(idMap)
```
Here we have another type of alias: a memory alias. It maps processor registers to memory addresses: by accessing the address we actually access the register.

```
processor.setFetchRegister('PC', -4)
```
This instruction simply sets the register which holds the address of the next instruction: to fetch an instruction from memory the processor simply
reads a word from the address contained in this register. Again it is possible to specify an offset (as before only taken into account for functional
processors).

```
processor.setMemory('dataMem', 10*1024*1024)
```
We set an internal memory for the processor; to access this memory from the ISA implementation we have methods `read_word`, `read_half`, `read_byte`,
`write_word`, `write_half`, `write_byte`, `lock` and `unlock`. In addition to (instead of) the internal memory, we can declare TLM ports using the directive
`processor.addTLMPort('instrMem', fetch = True)`; `fetch` specifies that this is the TLM port from which instruction are fetched (useful for modeling Harvard
architectures, with separate instruction and data ports for communicating with memory). One and only one TLM port can be the fetch port.

```
irq = trap.Interrupt('IRQ', priority = 0)
processor.addIrq(irq)
processor.setIRQOperation(ARMIsa.IRQOperation)
```
Adding interrupt ports: a TLM port called _IRQ_ will be created; it has the lowest priority (higher numbers mean higher priorities), meaning that if
there are two ports and an interrupt is asserted on both of them, the interrupt coming from the port with higher priority will be serviced first. The
_IRQOperation_ is called before the fetch of a new instruction an it contains the code (manually written by the user) to check if an interrupt has occurred
and, in case, take the appropriate action. ~~CHECK: I do not like this solution too much, it requires to much knowledge from the user~~

In addition to declaring TLM interrupt ports, we can use the directive `addPin` to a SystemC ports as external processor pins;
~~TODO: we still have to decide how these pins are going to be used; declaring a pinOperation like done for the interrupts?~~

```
fetchStage = trap.PipeStage('fetch')
processor.addPipeStage(fetchStage)
decodeStage = trap.PipeStage('decode')
processor.addPipeStage(decodeStage)
regsStage = trap.PipeStage('regs')
regsStage.setHazard()
regsStage.setCheckUnknownInstr()
processor.addPipeStage(regsStage)
executeStage = trap.PipeStage('execute')
executeStage.setCheckTools()
processor.addPipeStage(executeStage)
memoryStage = trap.PipeStage('memory')
processor.addPipeStage(memoryStage)
exceptionStage = trap.PipeStage('exception')
processor.addPipeStage(exceptionStage)
wbStage = trap.PipeStage('wb')
wbStage.setWriteBack()
wbStage.setEndHazard()
processor.addPipeStage(wbStage)
```
Description of a seven stage pipeline. Some methods can be called to specify the behavior each pipeline stage:
  * `setWriteBack`: defaults to `False`, sets the stage as a write back stage, where intermediate results are committed into the registers. This means that following operation can read from the registers destination of the ISA operation in this stage.
  * `setCheckUnknownInstr`: defaults to `False`, instructs the stage to raise an exception in case an unknown instruction reaches this stage (i.e. in case in case an opcode not corresponding to  any declared instruction reaches this stage)
  * `setCheckTools`: defaults to `False`, instructs the simulator to call the processor tools (debuggeer, profiler, OS emulator, etc.) in this stage.
  * `setHazard`: defaults to `False`, specifies that instructions are checked for hazards when entering the stage; in case a hazard exists, the pipeline is stalled. (usually the decode stage is a _hazard_ stage). Usually this method is called for the stage were the register file is written.
  * `setEndHazard`: defaults to `False`, specifies that registers locked in the stage marked as `setHazard` because the current instruction was writing them, are unlock and, as such, if a following instruction tries to read/write them, no hazard is generated.

Finally it is possible to specify the order with which registers are written back to the main register file
after each clock cycle:
```
processor.setWBOrder('NPC', ('decode', 'execute', 'wb'))
processor.setWBOrder('PC', ('decode', 'fetch', 'execute', 'wb'))
```
The first line instructs the simulator to first check if NPC was modified in the _decode_ stage: in this case the value
of NPC after _decode_ is written back to the main register file; if there were no modifications, we check the
_execute_ stage and then the _wb_ stage. The remaining stages are checked in the order they were declared.
For the registers for which no `setWBOrder` method was called, we first check the stage marked with the _setWriteBack_
method and the the remaining stages in the order they were declared.

```
abi = trap.ABI('REGS[0]', 'REGS[0-3]', 'PC', 'LR', 'SP', 'FP')
abi.addVarRegsCorrespondence({'REGS[0-15]': (0, 15), 'CPSR': (25, 25)})
abi.setOffset('PC', -4)
abi.setOffset('REGS[15]', -4)
processor.setABI(abi)
```
These instructions declare the conventions for the ABI (_Application Binary Interface_) of the current processor. Such information is used
for the implementation of the GDB Stub (in order to be able to debug software running on the created simulator), the Operating System Emulation
(in order to be able to execute software without the need to also simulate a fully flagged OS) and the profiler. This data is also necessary in case
we want to retarget GCC backend for the architecture being described (this feature is not yet supported).

Instruction `ABI('REGS[0]', 'REGS[0-3]', 'PC', 'LR', 'SP', 'FP')` means that function return values are stored in `REGS[0]`, that registers `REGS[0-3]`
are used for parameter passing and that the program counter is contained in register `PC`. The following information are optional: `LR` is the register
representing the link register, `SP` the stack pointer and, finally, `FP` the frame pointer.

Directive `addVarRegsCorrespondence` is used to set the correspondence between the architectural elements and the register numbers as seen by GDB
for the architecture under description.

At the end, again just for the functional processor, we specify that registers `PC` and `REGS[15]` must be used with an offset of -8.

```
processor.write(folder = 'processor', models = ['funcLT'])
```
Finally we create the C++ files implementing our simulator; these files will be put in folder _processor_; we are just creating the functional
model using the loosley timed TLM interfaces (in case we specified to used SystemC in the processor description, otherwise time will not be
taken into account). The valid processor variants are _funcAT_ and _accAT_: functional model using Approximate Time TLM interfaces and
Cycle Accurate model using using Approximate Time TLM interfaces.
The write method has two other optional parameters:
  * `trace = True`: the processor model will be generated with tracing enabled; at each clock cycle the instruction being executed and the status of the processor after instruction execution will be printed.
  * `dumpDecoderName = FILENAME`: the tree representing the decoder will be printed to _FILENAME_ in the _.dot_ format.

## Describing the instruction coding ##
The instruction set encoding is described through a series of _machine codes_; they are described as they appear in the architecture reference
manual. Each instruction is then assigned a machine code; different instructions can have the same machine code, with the the instruction
identification bits set for the particular instruction.

This is an example of the machine code for the _data processing instruction_ with an immediate operand for the ARM7 processor:
```
dataProc_imm = trap.MachineCode([('cond', 4), ('id', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('rotate', 4), ('immediate', 8)])
dataProc_imm.setVarField('rn', ('REGS', 0), 'in')
dataProc_imm.setVarField('rd', ('REGS', 0), 'out')
dataProc_imm.setBitfield('id', [0, 0, 1])
```
The _machine code_ (called also instruction format) is composed of various fields: the first 4 bits represent the condition, which, if
verified enable instruction execution (remember that the ARM features a predicated instruction set). We then have the identifier of the
instruction (_id_) and so on...

After specifying the various fields which compose the instruction format, we have to associate these fields with their type:
```
dataProc_imm.setVarField('rn', ('REGS', 0), 'in')
```
it says that field _rn_ is the id of a register in the _REGS_ register bank and that, in particular, it refers to register REGS[+ 0](rn.md);
it also specifies that this is an input register, in the sense that it will be read, but not written,
by the instructions using this machine code.
Other valid values are `'out'` and `'inout'`, to specify respectively that the register is only written or both read and written
by the instructions using this machine code
```
dataProc_imm.setBitfield('id', [0, 0, 1])
```
it specifies that field _id_ is always assigned the bits 001

Note that all the fields called _zero_ are automatically assigned a sequence of 0s, while fields called _one_ are assigned a sequence of 1s.

## Describing the instruction behavior ##
This Section explains how we can combine all the details described so far in order to describe the
actual Instruction Set together with its behavior in each pipeline stage. As an example we will use the _AND_
instruction of the LEON3 processor:
```
opCodeReadRegs1 = cxx_writer.writer_code.Code("""
rs1_op = rs1;
""")
opCodeExecImm = cxx_writer.writer_code.Code("""
result = rs1_op & SignExtend(simm13, 13);
""")
opCodeWb = cxx_writer.writer_code.Code("""
rd = result;
""")
and_imm_Instr = trap.Instruction('AND_imm', True, frequency = 5)
and_imm_Instr.setMachineCode(dpi_format2, {'op3': [0, 0, 0, 0, 0, 1]}, ('and r', '%rs1', ' ', '%simm13', ' r', '%rd'))
and_imm_Instr.setCode(opCodeExecImm, 'execute')
and_imm_Instr.setCode(opCodeReadRegs1, 'regs')
and_imm_Instr.setCode(opCodeWb, 'wb')
and_imm_Instr.addBehavior(IncrementPC, 'fetch')
and_imm_Instr.addVariable(('result', 'BIT<32>'))
and_imm_Instr.addVariable(('rs1_op', 'BIT<32>'))
and_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[10]' : 0xffffffff, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8})
isa.addInstruction(and_imm_Instr)
```
First of all, in the `opCodeReadRegs1`, `opCodeExecImm`, and `opCodeWb` operations we define the C++ implementing the
behavior of the AND instruction respectively in the _regs_, _execute_, and _wb_ stages. In this code it is possible
to write normal C++ code, including declaration of new variables, etc. We have access to all the registers,
aliases, and memories previously declared in the architecture of the processor. Moreover we can access the different
bit of the instruction coding as specified in the instruction format (in this case `dpi_format2`). For example,
`dpi_format2` is defined as:
```
dpi_format2 = trap.MachineCode([('op', 2), ('rd', 5), ('op3', 6), ('rs1', 5), ('one', 1), ('simm13', 13)])
dpi_format2.setBitfield('op', [1, 0])
dpi_format2.setVarField('rd', ('REGS', 0), 'out')
dpi_format2.setVarField('rs1', ('REGS', 0), 'in')
```
In this case we can access `op`, `op3`, and `simm13` as integer variables; regarding the parts of the instruction
coding which reference archietctural elements (`rd` and `rs1`), two variables are created: `rd_bit` and `rs1_bit` which
contain the value of the `rd` and `rs1` fields, while variables `rd` and `rs1` are registers aliases directly pointing,
respectively, to `REGS[rd_bit + 0]` and `REGS[rs1_bit + 0]`. In addition we can access all the variables declared
using the `addVariable` directive; note how these variables retain their value throughout the pipeline stages of the
instruction being declared.

Concerning the `Instruction` constructor, the first parameter is the instruction name, the second specifies whether the
instruction can modify or not the program counter ~~TODO: this information is not used yet~~ and the `frequency`
parameters specify how often this instruction is found in normal programs; this information is used in the construction
of the decoder: the higher the `frequency` parameter, the faster will be the decoder in decoding this instruction.

The `setMachineCode` construct takes three parameters:
  1. the first one specifies what is the machine code of this instruction
  1. the second what are the bits, in the machine code, that uniquely identify this instruction
  1. the third one is used to build the disassembler: the different parts of the assembly code representing this instruction are the different elements of the list, elements staring with _%_ refer to the parts of the instruction encoding and are substituted with the value of the corresponding part in the actualy bistring.
It is also possible to give more complex directive to the disassembler:
```
('b', ('%cond', {int('1000', 2) : 'a',
int('0000', 2) : 'n', int('1001', 2) : 'ne', int('0001', 2) : 'e', int('1010', 2) : 'g', int('0010', 2) : 'le',
int('1011', 2) : 'ge', int('0011', 2) : 'l', int('1100', 2) : 'gu', int('0100', 2) : 'leu', int('1101', 2) : 'cc',
int('01010', 2) : 'cs', int('1110', 2) : 'pos', int('0110', 2) : 'neg', int('1111', 2) : 'vc', int('0111', 2) : 'vs',}),
('%a', {1: ',a'}), ' ', '%disp22'))
```
Here (taken from the specification of the _branch_ instruction of the LEON3 processor) we specify that
after the litteral `b` we have to write `a` if the `cond` field has the binary value `1000`, `n` if if has
value `0000`, etc.

Finally we describe the tests for testing the correctness of the instruction implementation; note that it is possible to
add an unlimited number of tests for each instruction (the more the better) and that the tests are automatically generated
only when creating a functional simulator without SystemC.
The code for a test is divided into three parts:
```
and_imm_Instr.addTest({'rd': 0, 'rs1': 10, 'simm13': 0xfff}, {'REGS[10]' : 0xffffffff, 'PC' : 0x0, 'NPC' : 0x4}, {'REGS[10]' : 0xffffffff, 'REGS[0]' : 0, 'PC' : 0x8, 'NPC' : 0x8})
```
The first one specifies the values of the machine code with which we want to exercise the instruction,
the second one the state of the processor before the execution of the instruction and the third one the desired
state of the processor after the execution of the instruction.

One final note: the `addBehavior` construct has three additional parameters:
  1. `pre = True` specifies whether the behavior has to be added before or after the instruction code for the specified pipeline stage
  1. `accurateModel = True` specifies that this behavior has to be added when a cycle accurate model is being created
  1. `functionalModel = True` specifies that this behavior has to be added when a functional model is being created

Behavior `IncrementPC` is declared as a helper method: since this method is used by many instructions,
its behavior is factored in a separate routine. Such routine could be decalred inside the ISA file or,
in order to keep things clearer, in a separate python file (in the LEON3 description it is declared
inside file _LEON3Mehotds.py_):
```
opCode = cxx_writer.writer_code.Code("""PC = NPC;
NPC += 4;
""")
IncrementPC = trap.HelperOperation('IncrementPC', opCode)
```

In addition to the _HelperOperation_ construct there are available for easing the description of the ISA behavior are
_HelperMethod_:
```
opCode = cxx_writer.writer_code.Code("""
if((bitSeq & (1 << (bitSeq_length - 1))) != 0)
    bitSeq |= (((unsigned int)0xFFFFFFFF) << bitSeq_length);
return bitSeq;
""")
SignExtend_method = trap.HelperMethod('SignExtend', opCode, 'execute')
SignExtend_method.setSignature(('BIT<32>'), [('bitSeq', 'BIT<32>'), cxx_writer.writer_code.Parameter('bitSeq_length', cxx_writer.writer_code.uintType)])
isa.addMethod(SignExtend_method)
```
This is a normal method and it can be freely called from the C++ code of the instruction as shown above.

Note that _HelperMethod_ and _HelperOperation_ can be declared with many parameters and in different ways;
refer to the _LEON3_ and _ARM7_ descriptions for more details on how to use these constructs.

## Creating the Instruction Set Simulator ##
Creating the instruction set simulator from the description is simple: define a file which directly or indirectly imports
all the other files composing the processor decsription and that ends with the call to the `write` method
of the _processor_ class. Then run this file in _Python_, i.e. `python myFile`. The C++ code implementing the processor
simulator will be written in folder _processor_.

For example, the main file for description of the _ARM7_ processor is _ARMArch.py_: at the beginning it includes
the file for description of the _ISA_ with the directive `import ARMIsa`; file _ARMIsa.py_ in turn includes
file _ARMCoding.py_ (where the instruction formats are decribed) and _ARMMethods.py_ containing helper
functions for easing the description of the behavior of the instruction set.
To generate the Instruction Set simulator we simply have to run command _python ARMArch.py_. Once
the processor simulator is generated, we can procede with its compilation following the instructions
contained in the _Setup_ page of this wiki.