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

int isatty(int desc){
    _exit(-1);
    return 0;
}

void *sbrk(intptr_t increment){
    _exit(-1);
    return NULL;
}

ssize_t write(int fd, const void *buf, size_t count){
    _exit(-1);
    return -1;
}

int open(const char *pathname, int flags){
    _exit(-1);
    return -1;
}

int close(int fd){
    _exit(-1);
    return -1;
}

int fstat(int fd, struct stat *buf){
    _exit(-1);
    return -1;
}

int stat(const char *path, struct stat *buf){
    _exit(-1);
    return -1;
}

off_t lseek(int fd, off_t offset, int whence){
    _exit(-1);
    return -1;
}

ssize_t read(int fd, void *buf, size_t count){
    _exit(-1);
    return -1;
}

int creat(const char *pathname, mode_t mode){
    _exit(-1);
    return -1;
}

clock_t times(struct tms *buf){
    _exit(-1);
    return -1;
}

time_t time(time_t *t){
    _exit(-1);
    return -1;
}

long int random(void){
    _exit(-1);
    return 0L;
}

int kill(pid_t pid, int sig){
    _exit(-1);
    return -1;
}

pid_t getpid(void){
    _exit(-1);
    return -1;
}

int gettimeofday(struct timeval *tv, void *tz){
    _exit(-1);
    return -1;
}

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

int unlink(const char *pathname){
    _exit(-1);
    return -1;
}

void _exit(int exitVal){
    _exit(exitVal);
}
