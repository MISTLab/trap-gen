#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

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


import unittest
from tests import testWriter
from tests import testClassDecls
from tests import testFileDumper
from tests import testSimpleDecls

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(testWriter.TestWriter)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testClassDecls.TestClassDecls))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testFileDumper.TestFileDumper))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testSimpleDecls.TestSimpleDecls))
    runner = unittest.TextTestRunner()
    runner.verbosity = 2
    runner.run(suite)
