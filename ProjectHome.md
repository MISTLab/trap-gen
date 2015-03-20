# TRAP #
### TRansaction level Automatic Processor generator ###

**TRAP** (TRansaction level Automatic Processor generator) is a tool for the automatic generation of processor simulators starting from high level descriptions. This means that the developer only need to provide basic structural information (i.e. the number of registers, the endianess etc.) and the behavior of each instruction of the processor ISA; this data is then used for the generation of C++ code emulating the processor behavior. Such an approach consistently eases the developer's work (with respect to manual coding of the simulator) both because it requires only the specification of the necessary details and because it forces a separation of the processor behavior from its structure.
The tool is written in Python and it produces SystemC based simulators. With respect to standard ADL, having the input directly from Python eliminates the need for having an ad-hoc front-end thus consistently reducing the development effort.

The ARM7TDMI and the LEON3 processors are being developed using TRAP; their source code can be found in the _processor_ folder of TRAP itself.

## Features ##
  * **extensibility**, thanks to the use of Python for the high level description of the processor models
  * **interoperability** with the most recent standards in System Level Design (SystemC, TLM)
  * **speed** of the generated simulators, given by a careful exploitation of the features of the C++ language and of the features of the new TLM 2.0 library
  * **simplicity** of the processor description, requiring minimal effort from the architecture designer
  * ...

## Note ##
TRAP is still work in progress ...

## Links ##
Project page on ohloh: https://www.ohloh.net/p/trap-gen