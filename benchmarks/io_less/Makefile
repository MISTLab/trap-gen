TARGETS = AES bcnt blit crc des engine fib fir2 hanoi heapsort matrix pocsag queens quicksort

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

$(addsuffix .O2, $(TARGETS)): $(addsuffix .c, $(basename $@))
ifneq ("$(CC_CROSS)", "")
	$(CC_CROSS) -o $@ -g3 -O2 $(CFLAGS) $(addsuffix .c, $(basename $@))
else
	echo "CC_CROSS environmental variable not set"
	exit 1
endif

$(addsuffix .O3, $(TARGETS)): $(addsuffix .c, $(basename $@))
ifneq ("$(CC_CROSS)", "")
	$(CC_CROSS) -o $@ -g3 -O3 $(CFLAGS) $(addsuffix .c, $(basename $@))
else
	echo "CC_CROSS environmental variable not set"
	exit 1
endif

clean:
	rm $(addsuffix .O0, $(TARGETS)) $(addsuffix .O1, $(TARGETS)) $(addsuffix .O2, $(TARGETS)) $(addsuffix .O3, $(TARGETS)) TRAP_stats.csv *~ -rf

