# Remember to add the -DBIG_TARGET option to the CFLAGS in case we are compiling for a big endian system

TARGETS = deepCalls testAdd1 testChar1 testConv1 testConv2 testDiv1 testDiv2 testDiv3  testDiv4 testDiv5  testDouble  testDouble2 testDouble3  testLoadByte1 testLoadByte2 testLoadByte3 testLoadDouble testLoadHalf testLogic1 testLogic2 testLoop1 testLoop10 testLoop2 testLoop3 testLoop4 testLoop5 testLoop6 testLoop7 testLoop8 testLoop9 testMul1 testShift1 testShift2 testShift3 testStoreByte1 testStoreByte2 testStoreDouble testStoreHalf testStoreDouble2

all: $(addsuffix .O0, $(TARGETS)) $(addsuffix .O1, $(TARGETS)) $(addsuffix .O2, $(TARGETS)) $(addsuffix .O3, $(TARGETS))

$(addsuffix .O0, $(TARGETS)): $(addsuffix .c, $(basename $@))
ifneq ("$(CC_CROSS)", "")
	$(CC_CROSS) -o $@ -g3 -O0 $(CFLAGS) $(addsuffix .c, $(basename $@))
else
	echo "CC_CROSS environmental variable not set"
	exit 1
endif

$(addsuffix .O1, $(TARGETS)): $(addsuffix .c, $(basename $@))
ifneq ("$(CC_CROSS)", "")
	$(CC_CROSS) -o $@ -g3 -O1 $(CFLAGS) $(addsuffix .c, $(basename $@))
else
	echo "CC_CROSS environmental variable not set"
	exit 1
endif

$(addsuffix .O2, $(TARGETS)): $(addsuffix .c, $(basename, $@))
ifneq ("$(CC_CROSS)", "")
	$(CC_CROSS) -o $@ -g3 -O2 $(CFLAGS) $(addsuffix .c, $(basename $@))
else
	echo "CC_CROSS environmental variable not set"
	exit 1
endif

$(addsuffix .O3, $(TARGETS)): $(addsuffix .c, $(basename, $@))
ifneq ("$(CC_CROSS)", "")
	$(CC_CROSS) -o $@ -g3 -O3 $(CFLAGS) $(addsuffix .c, $(basename $@))
else
	echo "CC_CROSS environmental variable not set"
	exit 1
endif

clean:
	rm $(addsuffix .O0, $(TARGETS)) $(addsuffix .O1, $(TARGETS)) $(addsuffix .O2, $(TARGETS)) $(addsuffix .O3, $(TARGETS)) -rf
	rm $(addsuffix .O0.trace, $(TARGETS)) $(addsuffix .O1.trace, $(TARGETS)) $(addsuffix .O2.trace, $(TARGETS)) $(addsuffix .O3.trace, $(TARGETS)) -rf
	rm $(addsuffix .O0.dmp, $(TARGETS)) $(addsuffix .O1.dmp, $(TARGETS)) $(addsuffix .O2.dmp, $(TARGETS)) $(addsuffix .O3.dmp, $(TARGETS)) -rf
	rm *~ -rf

test: $(addsuffix .O0, $(TARGETS)) $(addsuffix .O1, $(TARGETS)) $(addsuffix .O2, $(TARGETS)) $(addsuffix .O3, $(TARGETS))
	python executeTests.py $(SIMULATOR) $(addsuffix .O0, $(TARGETS)) $(addsuffix .O1, $(TARGETS)) $(addsuffix .O2, $(TARGETS)) $(addsuffix .O3, $(TARGETS))
