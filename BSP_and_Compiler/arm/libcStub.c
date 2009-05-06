#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <sys/times.h>
#include <sys/time.h>
#include <time.h>

/************************************************************************
* This file contains placeholder routines in order to allow a correct
* linking of the binaries; note that these routines will actually never
* be called since their behavior will be emulated using hardware OS emulation
*************************************************************************/

int chmod(const char *path, mode_t mode){
    _exit(-1);
    return -1;
}

int chown(const char *path, uid_t owner, gid_t group){
    _exit(-1);
    return -1;
}

int usleep(useconds_t usec){
    _exit(-1);
    return -1;
}

int dup(int oldfd){
    _exit(-1);
    return -1;
}

int dup2(int oldfd, int newfd){
    _exit(-1);
    return -1;
}

long sysconf(int name){
    _exit(-1);
    return -1;
}
