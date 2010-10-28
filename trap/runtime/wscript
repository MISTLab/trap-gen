#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

def build(bld):
    bld.recurse('loader utils bfdFontend osEmulator debugger misc profiler')

    bld.objects(source='ToolsIf.cpp', 
        includes = '. utils',
        target = 'tools',
        install_path = None
    )

    bld.install_files('${PREFIX}/include', 'ABIIf.hpp trap.hpp ToolsIf.hpp instructionBase.hpp')
