#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os

def build(bld):
    bld.recurse('loader utils bfdFontend osEmulator debugger misc profiler')

    bld.objects(source='ToolsIf.cpp', 
        includes = '. utils',
        target = 'tools',
        install_path = None
    )

    bld.install_files(os.path.join(bld.env.PREFIX, 'include'), 'ABIIf.hpp trap.hpp ToolsIf.hpp instructionBase.hpp')
