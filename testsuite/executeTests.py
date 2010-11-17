#!/usr/bin/env python
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
#   the Free Software Foundation; either version 3 of the License, or
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
#   (c) Luca Fossati, fossati@elet.polimi.it, fossati.l@gmail.com
#
####################################################################################

import os, sys

if __name__ == "__main__":
    # The first parameters to the script represents the name of the simulator, then we have the list of tests
    if not os.path.exists(sys.argv[1]):
        print 'Error, simulator executable file ' + sys.argv[1] + ' does not exists'
    failedBenchs = {}
    for test in sys.argv[2:]:
        shellCommandString = 'ulimit -t 120  && ' + sys.argv[1] + ' -a ' + test + ' 2>' + test + '.trace'
        try:
            import subprocess
            result = subprocess.Popen(shellCommandString, shell=True, stdout=PIPE, close_fds=True).stdout.readlines()
        except:
            result = os.popen(shellCommandString).readlines()
        foundExitLine = False
        for line in result:
            if line.startswith('Program exited with value'):
                foundExitLine = True
                retVal = int(line.split(' ')[-1])
                if retVal != 0:
                    failedBenchs[test] = retVal
                    if os.path.exists('memoryDump.dmp'):
                        os.rename('memoryDump.dmp', test + '.dmp')
                else:
                    os.remove(test + '.trace')
                break
        if not foundExitLine:
            failedBenchs[test] = 'Exit Line Not Found'
            if os.path.exists('memoryDump.dmp'):
                os.rename('memoryDump.dmp', test + '.dmp')
    print '\nFailed ' + str(len(failedBenchs)) + ' tests out of ' + str(len(sys.argv[2:]))
    sortedFailedBenchs = failedBenchs.keys()
    sortedFailedBenchs.sort()
    for test in sortedFailedBenchs:
        print 'Test ' + test + ' failed with return value ' + str(failedBenchs[test])
    print '\n'
