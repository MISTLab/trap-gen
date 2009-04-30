#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os, sys

if __name__ == "__main__":
    # The first parameters to the script represents the name of the simulator, then we have the list of tests
    if not os.path.exists(sys.argv[1]):
        print 'Error, simulator executable file ' + sys.argv[1] + ' does not exists'
    failedBenchs = {}
    for test in sys.argv[2:]:
        #test = test + '.gdb'
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
    print '\nFailed ' + str(len(failedBenchs)) + ' tests'
    sortedFailedBenchs = failedBenchs.keys()
    sortedFailedBenchs.sort()
    for test in sortedFailedBenchs:
        print 'Test ' + test + ' failed with return value ' + str(failedBenchs[test])
    print '\n'
