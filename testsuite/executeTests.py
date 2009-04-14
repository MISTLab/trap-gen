#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os, sys

if __name__ == "__main__":
    # The first parameters to the script represents the name of the simulator, then we have the list of tests
    if not os.path.exists(sys.argv[1]):
        print 'Error, simulator executable file ' + sys.argv[1] + ' does not exists'
    failedBenchs = {}
    for test in sys.argv[2:]:
        try:
            import subprocess
            result = subprocess.Popen(sys.argv[1] + ' -a ' + test + ' 2>' + test + '.trace', shell=True, stdout=PIPE, close_fds=True).stdout.readlines()
        except:
            result = os.popen(sys.argv[1] + ' -a ' + test + ' 2>' + test + '.trace').readlines()
        for line in result:
            if line.startswith('Program exited with value'):
                retVal = int(line.split(' ')[-1])
                if retVal != 0:
                    failedBenchs[test] = retVal
                else:
                    os.remove(test + '.trace')
                break
    print '\nFailed ' + str(len(failedBenchs)) + ' tests'
    for test, retVal in failedBenchs.items():
        print 'Test ' + test + ' failed with return value ' + str(retVal)
