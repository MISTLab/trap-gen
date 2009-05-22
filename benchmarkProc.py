#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import csv, os, sys, numpy

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print ('Error, the command line for the benchmarking program is: processorExecurtable numRuns benchmark1,benchmark2 ...')
        sys.exit(0)

    maxSpeed = 0
    fastBench = ''
    runTime = []
    benchSpeed = {}
    for benchmark in sys.argv[3].split(','):
        if not os.path.exists(benchmark):
            raise Exception('Error, benchmark ' + benchmark + ' not existing')
        benchSpeed[benchmark] = []
        for i in range(0, int(sys.argv[2])):
            result = os.popen(sys.argv[1] + ' -a ' + benchmark).readlines()
            for res in result:
                if 'Execution Speed' in res:
                    speed = float(res.split()[2])
                    if speed > maxSpeed:
                        maxSpeed = speed
                        fastBench = benchmark
                    runTime.append(speed)
                    benchSpeed[benchmark].append(speed)
                    break

    # Lets now print the csv file with all the benchmarks
    fileHandle = open('TRAP_stats.csv', 'w')
    fileCsvWriter = csv.writer(fileHandle, delimiter = ';')
    for bench, speedRuns in benchSpeed.items():
        fileCsvWriter.writerow([bench] + [str(i) for i in speedRuns] + [str(numpy.average(speedRuns)), str(numpy.std(speedRuns))])
    fileHandle.close()

    # Finally I print some statistics
    print ('Average Execution Speed: ' + str(numpy.average(runTime)) + ' MIPS')
    print ('Standard Deviation: ' + str(numpy.std(runTime)) + ' MIPS')
    print ('Fastst benchmark: ' + fastBench + ' ( ' + str(maxSpeed) + ' MIPS )')
