#!/usr/bin/env python

import os

def build(bld):
    bld.add_subdirs('loader utils bfdFontend osEmulator debugger misc')

    obj = bld.new_task_gen('cxx', 'objects')
    obj.source="""
        ToolsIf.cpp
    """
    obj.includes = '. utils'
    obj.name = 'tools'
    obj.target = 'tools'
    obj.install_path = None

    bld.install_files('${PREFIX}/include', 'ABIIf.hpp trap.hpp ToolsIf.hpp')
