# Building and Installation Instruction #

TRAP uses waf (http://code.google.com/p/waf) as build system; from a user point of view it is similar to the usual autotools
based project: first there is a configuration step, then the compilation and, finally, the installation.

## Required Libraries and Tools ##

  * BFD: part of the binutils, it is used to read and parse the application software which is going to be executed on the processors. The development version of this package is needed
  * SystemC: downloadable from http://www.systemc.org, it is used to manage simulated time and the communication among the hardware modules
  * TLM 2.0: downloadable from http://www.systemc.org, it is used to manage connections among the hardware modules. This library is not necessary for the compilation of TRAP itself, but for the compilation of the generated processor models.
  * Boost: Boost libraries, downloadable from http://www.boost.org.
  * Python version 2.4 - 2.6
  * networkx: library used for the description of graphs in Python. This library can be dowloaded from http://networkx.lanl.gov/ and it is used during the generation of C++ code implementing the processor models.

### Configuration ###

In the base folder of TRAP run the _./waf configure_ command. Several configuration options are available:
  1. _--with-systemc=SYSC\_FOLDER_ specifies the location of the SystemC 2.2 library. It is compulsory to specify such option
  1. _--prefix=LIB\_DEST\_FOLDER_ specifies the destination folder for installation of the TRAP C++ runtime libraries. If this option is not specified _/usr/local_ is used as default
  1. _--py-install-dir=PYTHON\_DEST\_FOLDER_ specifies the destination folder for the installation of TRAP python files. If this option is not specified, _/usr/lib/pythonX.X/site-packages/_ is used as default
  1. _--with-bfd=BFD\_FOLDER_ specifies the location of the BFD library; if this option is not specified TRAP will look for libbfd in the standard library search path. Specifying this option is mandatory under Microsoft Windows.
  1. _--boost-includes=BOOSTINCLUDES_ specifies the location of the include files of the boost lbraries; it has to be specified in case the libraries are not installed in a standard path.
  1. _--boost-libs=BOOSTLIBS_ specifies the location of the library files of the boost lbraries; it has to be specified in case the libraries are not installed in a standard path.

To have the list of all the possible configuration options run _./waf --help_

### Compilation and Installation ###

Once the project is correctly configured execute the _./waf_ command to trigger the compilation. Once this is done, command _./waf install_
copies the python files and the generated runtime libraries in the chosend destination folders.

## Creation of the processor models ##

Once TRAP itself is correctly installed, simply execute the main python script of your processor model. For the ARM7TDMI processor go
into folder _processor/ARM7TDMI_ and run the command _python ARMArch.py_ . The C++ files implementing the different flavors of simulators
should be generated. Note that, in case the TRAP python files are installed in a custom folder, the main script ( _ARMArch.py_ in this case )
should be modified to specify this path.

### Configuration and Compilation ###

Once the processor implementation files are created, they need to be compiled; do do this the _waf_ build system is again used.

The configuration options which can be passed to the _./ waf configure_ command are:
  1. _--with-systemc=SYSC\_FOLDER_ specifies the location of the SystemC 2.2 library. It is compulsory to specify such option
  1. _--with-tlm=TLM\_FOLDER_ specifies the location of the TLM 2.0 library. It is compulsory to specify such option
  1. _--with-trap=TRAP\_FOLDER_ specifies the location of the TRAP runtime libraries and headers. It must be specified if TRAP was installed in a custom folder
  1. _--boost-includes=BOOSTINCLUDES_ specifies the location of the include files of the boost lbraries; it has to be specified in case the libraries are not installed in a standard path.
  1. _--boost-libs=BOOSTLIBS_ specifies the location of the library files of the boost lbraries; it has to be specified in case the libraries are not installed in a standard path.
  1. _--with-bfd=BFD\_FOLDER_ specifies the location of the BFD library; if this option is not specified TRAP will look for libbfd in the standard library search path. Specifying this option is mandatory under Microsoft Windows.
  1. _--static_ specifies that a fully static executable have to be built. Such executable can be redistributed standalone and it does not depend on any library.

After the configuration successfully ends, compilation can be started with the usual _./waf_ command; the executables files of the
processor simulator an of its testing scripts are contained inside the `_build_` folder.