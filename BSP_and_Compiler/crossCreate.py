#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os, sys, shutil
import readline

class Completer:
    def __init__(self, namespace = None):
        """Create a new completer for the command line."""

        self.matches = []

    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        This is called successively with state == 0, 1, 2, ... until it
        returns None.  The completion should begin with 'text'.

        """
        if state == 0:
            import os
            import re
            text = os.path.expanduser(text)
            if not text.startswith(os.sep) and not text.startswith('.'):
                text = './' + text
            dirName = os.path.dirname(text)
            baseName = os.path.basename(text)
            if not os.path.exists(dirName):
                return None
            files = os.listdir(dirName)
            if not baseName == '':
                files = filter( lambda x: os.path.basename(x).startswith(baseName) , files )
            self.matches = []
            for i in files:
                curPath = os.path.join(dirName, i)
                if os.path.isdir(curPath):
                    self.matches.append(curPath + os.sep)
                else:
                    self.matches.append(curPath)
        try:
            return self.matches[state]
        except:
            return None

completer = Completer()
readline.set_completer(completer.complete)
readline.parse_and_bind("tab: complete")
readline.set_completer_delims('\t\n`!@#$%^&*)=+[{]}\\|;:,<>?')

binutils = (raw_input('Please specify the binutils archive: ')).replace('\n', '').strip()
while not os.path.exists(binutils):
    print 'path --> ' + binutils + ' <-- not existing, please specify an existing one'
    binutils = (raw_input('Please specify the binutils archive: ')).replace('\n', '').strip()

gcc = (raw_input('Please specify the gcc archive: ')).replace('\n', '').strip()
while not os.path.exists(gcc):
    print 'path --> ' + gcc + ' <-- not existing, please specify an existing one'
    gcc = (raw_input('Please specify the gcc archive: ')).replace('\n', '').strip()

newlib = (raw_input('Please specify the newlib archive: ')).replace('\n', '').strip()
while not os.path.exists(newlib):
    print 'path --> ' + newlib + ' <-- not existing, please specify an existing one'
    newlib = (raw_input('Please specify the newlib archive: ')).replace('\n', '').strip()

insight = (raw_input('Please specify the insight archive (ENTER for none): ')).replace('\n', '').strip()
gdb = (raw_input('Please specify the gdb archive (ENTER for none): ')).replace('\n', '').strip()

prefix = (raw_input('Please specify the toolchain installation folder (must be accessible by the user): ')).replace('\n', '').strip()
targetArch = (raw_input('Please specify the toolchain target architecture (e.g. arm-elf): ')).replace('\n', '')
addFlags = (raw_input('Specify additional compilation flags (ENTER for none): ')).replace('\n', '')
newlibPatch = (raw_input('Are you going to patch newlib?[N,y]: ')).replace('\n', '')
numProc = (raw_input('Specify the number of processes used during compilation[1]: ')).replace('\n', '')
try:
    int(numProc)
except:
    numProc = 1

binutilsName = ''
if binutils.find('.tar.bz2') == len(binutils) - 8:
    os.system('tar -xjkf ' + binutils + ' 2> /dev/null')
    binutilsName = os.path.basename(binutils)[:-8]
elif binutils.find('.tar.gz') == len(binutils) - 7:
    os.system('tar -xzkf ' + binutils + ' 2> /dev/null')
    binutilsName = os.path.basename(binutils)[:-7]
elif binutils.find('.tgz') == len(binutils) - 4:
    os.system('tar -xzkf ' + binutils + ' 2> /dev/null')
    binutilsName = os.path.basename(binutils)[:-4]
else:
    print binutils + ' is not a valid archive (use gzipped or bzipped tarred archives)'
    sys.exit()
if os.path.exists(os.path.basename(binutils) + '_build'):
    shutil.rmtree(os.path.basename(binutils) + '_build')
os.mkdir(os.path.basename(binutils) + '_build')

gccName = ''
if gcc.find('.tar.bz2') == len(gcc) - 8:
    os.system('tar -xjkf ' + gcc + ' 2> /dev/null')
    gccName = os.path.basename(gcc)[:-8]
elif gcc.find('.tar.gz') == len(gcc) - 7:
    os.system('tar -xzkf ' + gcc + ' 2> /dev/null')
    gccName = os.path.basename(gcc)[:-7]
elif gcc.find('.tgz') == len(gcc) - 4:
    os.system('tar -xzkf ' + gcc + ' 2> /dev/null')
    gccName = os.path.basename(gcc)[:-4]
else:
    print gcc + ' is not a valid archive (use gzipped or bzipped tarred archives)'
    sys.exit()
if os.path.exists(os.path.basename(gcc) + '_build'):
    shutil.rmtree(os.path.basename(gcc) + '_build')
os.mkdir(os.path.basename(gcc) + '_build')

newlibName = ''
if newlib.find('.tar.bz2') == len(newlib) - 8:
    os.system('tar -xjkf ' + newlib + ' 2> /dev/null')
    newlibName = os.path.basename(newlib)[:-8]
elif newlib.find('.tar.gz') == len(newlib) - 7:
    os.system('tar -xzkf ' + newlib + ' 2> /dev/null')
    newlibName = os.path.basename(newlib)[:-7]
elif newlib.find('.tgz') == len(newlib) - 4:
    os.system('tar -xzkf ' + newlib + ' 2> /dev/null')
    newlibName = os.path.basename(newlib)[:-4]
else:
    print newlib + ' is not a valid archive (use gzipped or bzipped tarred archives)'
    sys.exit()
if os.path.exists(os.path.basename(newlib) + '_build'):
    shutil.rmtree(os.path.basename(newlib) + '_build')
os.mkdir(os.path.basename(newlib) + '_build')

if os.path.exists(insight):
    insightName = ''
    if insight.find('.tar.bz2') == len(insight) - 8:
        os.system('tar -xjkf ' + insight + ' 2> /dev/null')
        insightName = os.path.basename(insight)[:-8]
    elif insight.find('.tar.gz') == len(insight) - 7:
        os.system('tar -xzkf ' + insight + ' 2> /dev/null')
        insightName = os.path.basename(insight)[:-7]
    elif insight.find('.tgz') == len(insight) - 4:
        os.system('tar -xzkf ' + insight + ' 2> /dev/null')
        insightName = os.path.basename(insight)[:-4]
    else:
        print insight + ' is not a valid archive (use gzipped or bzipped tarred archives)'
        sys.exit()
    if os.path.exists(os.path.basename(insight) + '_build'):
        shutil.rmtree(os.path.basename(insight) + '_build')
    os.mkdir(os.path.basename(insight) + '_build')
elif os.path.exists(gdb):
    gdbName = ''
    if gdb.find('.tar.bz2') == len(gdb) - 8:
        os.system('tar -xjkf ' + gdb + ' 2> /dev/null')
        gdbName = os.path.basename(gdb)[:-8]
    elif gdb.find('.tar.gz') == len(gdb) - 7:
        os.system('tar -xzkf ' + gdb + ' 2> /dev/null')
        gdbName = os.path.basename(gdb)[:-7]
    elif gdb.find('.tgz') == len(gdb) - 4:
        os.system('tar -xzkf ' + gdb + ' 2> /dev/null')
        gdbName = os.path.basename(gdb)[:-4]
    else:
        print gdb + ' is not a valid archive (use gzipped or bzipped tarred archives)'
        sys.exit()
    if os.path.exists(os.path.basename(gdb) + '_build'):
        shutil.rmtree(os.path.basename(gdb) + '_build')
    os.mkdir(os.path.basename(gdb) + '_build')

#Ok, lets finally procede with the actual compilation
print '\nCompiling binutils\n'
if os.system('cd ' + os.path.abspath(os.path.basename(binutils) + '_build') + ' && ' + os.path.abspath(binutilsName + '/configure') + ' --target=' + targetArch + ' --prefix=' + os.path.abspath(prefix) + ' --enable-multilib ' + addFlags + ' && make -j' + str(numProc) + ' && make install') != 0:
    sys.exit()
print '\nCompiling gcc step-1\n'
if os.system('export PATH=' + os.path.abspath(prefix + '/bin') + ':$PATH && cd ' + os.path.abspath(os.path.basename(gcc) + '_build') + ' && ' + os.path.abspath(gccName + '/configure') + ' --target=' + targetArch + ' --prefix=' + os.path.abspath(prefix) + ' --enable-multilib --with-newlib --with-tls --with-__thread --enable-languages=\'c,c++\' --with-headers=' + os.path.abspath(newlibName + '/newlib/libc/include') + ' --disable-__cxa_atexit --disable-__dso_handle ' + addFlags + ' && make all-gcc -j' + str(numProc) + ' && make install-gcc') != 0:
    sys.exit()
if newlibPatch.lower() == 'y':
    raw_input('Please perform all the necessary modifications to the newlib library in folder ' + os.path.abspath(os.path.basename(newlib) + '_build') + ' and press a key when ready to continue')
print '\nCompiling newlib\n'
if os.system('export PATH=' + os.path.abspath(prefix + '/bin') + ':$PATH && cd ' + os.path.abspath(os.path.basename(newlib) + '_build') + ' && ' + os.path.abspath(newlibName + '/configure') + ' --target=' + targetArch + ' --prefix=' + os.path.abspath(prefix) + ' --enable-multilib ' + addFlags + ' && make -j' + str(numProc) + ' && make install') != 0:
    sys.exit()
print '\nCompiling gcc step-2\n'
if os.system('export PATH=' + os.path.abspath(prefix + '/bin') + ':$PATH && cd ' + os.path.abspath(os.path.basename(gcc) + '_build') + ' && make -j' + str(numProc) + ' && make install') != 0:
    sys.exit()
#Now it is time to see if we need to cross-compiler GDB
print '\nCompiling debugger\n'
if os.path.exists(insight):
    if os.system('export PATH=' + os.path.abspath(prefix + '/bin') + ':$PATH && cd ' + os.path.abspath(os.path.basename(insight) + '_build') + ' && ' + os.path.abspath(insightName + '/configure') + ' --target=' + targetArch + ' --prefix=' + os.path.abspath(prefix) + ' --enable-multilib ' + addFlags + ' && make -j' + str(numProc) + ' && make install') != 0:
        sys.exit()
elif os.path.exists(gdb):
    if os.system('export PATH=' + os.path.abspath(prefix + '/bin') + ':$PATH && cd ' + os.path.abspath(os.path.basename(gdb) + '_build') + ' && ' + os.path.abspath(gdbName + '/configure') + ' --target=' + targetArch + ' --prefix=' + os.path.abspath(prefix) + ' --enable-multilib ' + addFlags + ' && make -j' + str(numProc) + ' && make install') != 0:
        sys.exit()
print '\n\n\nCross-Compiler correctly created in ' + os.path.abspath(prefix)
