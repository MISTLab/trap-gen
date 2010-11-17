#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os

def build(bld):
    subfolders = 'utils osEmulator debugger misc profiler'
    if bld.env['LICENSE'] == 'gpl':
        subfolders += ' libbfd_objloader'
    else:
        subfolders += ' libelf_objloader'
    bld.recurse(subfolders)

    bld.objects(source='ToolsIf.cpp', 
        includes = '. utils',
        target = 'tools',
        install_path = None
    )

    bld.install_files(os.path.join(bld.env.PREFIX, 'include'), 'ABIIf.hpp trap.hpp ToolsIf.hpp instructionBase.hpp')
