#!/bin/bash

for x in `ls | grep "\.gdb"`; do
	mv $x `basename $x .gdb`
done
