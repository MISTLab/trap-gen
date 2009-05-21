#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os, sys, numpy

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print ('Error, the command line for the benchmarking program is: processorExecurtable numRuns benchmark1,benchmark2 ...')
        sys.exit(0)

    maxSpeed = 0
    fastBench = ''
    runTime = []
    for benchmark in sys.argv[3].split(','):
        for i in range(0, int(sys.argv[2])):
            result = os.popen(sys.argv[1] + ' -a ' + benchmark).readlines()
            for res in result:
                if 'Execution Speed' in res:
                    speed = float(res.split()[2])
                    if speed > maxSpeed:
                        maxSpeed = speed
                        fastBench = benchmark
                    runTime.append(speed)
                    break
    print ('Average Execution Speed: ' + str(numpy.average(runTime)) + ' MIPS')
    print ('Standard Deviation: ' + str(numpy.std(runTime)) + ' MIPS')
    print ('Fastst benchmark: ' + fastBenchstr + '( ' + str(maxSpeed) + ' MIPS )')
