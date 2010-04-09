#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import csv, os, sys, numpy

if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise Exception('Error, the command line for the benchmarking program is: processorExecutable numRuns benchmark1 benchmark2 ...')

    maxSpeed = 0
    fastBench = ''
    runTime = []
    benchSpeed = {}
    for benchmark in sys.argv[3:]:
        if not os.path.exists(benchmark):
            raise Exception('Error, benchmark ' + benchmark + ' not existing')
        print ('Executing benchmark ' + benchmark)
        benchSpeed[benchmark] = []
        for i in range(0, int(sys.argv[2])):
            result = os.popen(sys.argv[1] + ' -a ' + benchmark).readlines()
            if not 'Program exited with value 0\n' in result:
                print('Benchmark ' + benchmark + ' failed since it has wrong exit value')
                break
            for res in result:
                if 'Execution Speed' in res:
                    speed = float(res.split()[2])
                    if speed > maxSpeed:
                        maxSpeed = speed
                        fastBench = benchmark
                    runTime.append(speed)
                    benchSpeed[benchmark].append(speed)
                    break

    for benchmark in sys.argv[3:]:
        if len(benchSpeed[benchmark]) < int(sys.argv[2]):
            print('Benchmark ' + benchmark + ' failed in at least one of its runs')
            benchSpeed.pop(benchmark, None)

    # Lets now print the csv file with all the benchmarks
    fileHandle = open('TRAP_stats.csv', 'w')
    fileCsvWriter = csv.writer(fileHandle, delimiter = ';')
    orderedBenchSpeed = sorted(benchSpeed.items(), lambda x, y: cmp(numpy.average(y[1]), numpy.average(x[1])))
    for bench, speedRuns in orderedBenchSpeed:
        fileCsvWriter.writerow([bench] + [str(i) for i in speedRuns] + [str(numpy.average(speedRuns)), str(numpy.std(speedRuns))])
    fileHandle.close()

    # Finally I print some statistics
    fileHandle = open('TRAP_summary.csv', 'w')
    fileCsvWriter = csv.writer(fileHandle, delimiter = ';')
    fileCsvWriter.writerow(['avg', str(numpy.average(runTime))])
    fileCsvWriter.writerow(['std', str(numpy.std(runTime))])
    fileHandle.close()

    print ('Executed ' + str(len(sys.argv[3:])) + ' benchmarks with ' + sys.argv[2] + ' runs per benchmark')
    print ('Average Execution Speed: ' + str(numpy.average(runTime)) + ' MIPS')
    print ('Standard Deviation: ' + str(numpy.std(runTime)) + ' MIPS')
    print ('Fastst benchmark: ' + fastBench + ' ( ' + str(maxSpeed) + ' MIPS )')
