TARGETS = AES crc engine fir2 hanoi pocsag tolstoy bcnt des fft lms queens blit dhry fib gamma matrix mib_off_strsearch quicksort mib_auto_basicmath whets heapsort jpeg mdrAll v42 wavelt

all: $(addsuffix .O0, $(TARGETS)) $(addsuffix .O1, $(TARGETS)) $(addsuffix .O2, $(TARGETS)) $(addsuffix .O3, $(TARGETS))

$(addsuffix .O0, $(TARGETS)): $(addsuffix .c, $(basename $@))
ifneq ("$(CC_CROSS)", "")
	$(CC_CROSS) -o $@ -g3 -O0 $(CFLAGS) $(addsuffix .c, $(basename $@)) -lm
else
	echo "CC_CROSS environmental variable not set"
	exit 1
endif

$(addsuffix .O1, $(TARGETS)): $(addsuffix .c, $(basename $@))
ifneq ("$(CC_CROSS)", "")
	$(CC_CROSS) -o $@ -g3 -O1 $(CFLAGS) $(addsuffix .c, $(basename $@)) -lm
else
	echo "CC_CROSS environmental variable not set"
	exit 1
endif

$(addsuffix .O2, $(TARGETS)): $(addsuffix .c, $(basename $@))
ifneq ("$(CC_CROSS)", "")
	$(CC_CROSS) -o $@ -g3 -O2 $(CFLAGS) $(addsuffix .c, $(basename $@)) -lm
else
	echo "CC_CROSS environmental variable not set"
	exit 1
endif

$(addsuffix .O3, $(TARGETS)): $(addsuffix .c, $(basename $@))
ifneq ("$(CC_CROSS)", "")
	$(CC_CROSS) -o $@ -g3 -O3 $(CFLAGS) $(addsuffix .c, $(basename $@)) -lm
else
	echo "CC_CROSS environmental variable not set"
	exit 1
endif

run: $(addsuffix .O0, $(TARGETS)) $(addsuffix .O1, $(TARGETS)) $(addsuffix .O2, $(TARGETS)) $(addsuffix .O3, $(TARGETS))
	./benchmarkProc.py $(SIMULATOR) 1 $(addsuffix .O0, $(TARGETS)) $(addsuffix .O1, $(TARGETS)) $(addsuffix .O2, $(TARGETS)) $(addsuffix .O3, $(TARGETS))

clean:
	rm $(addsuffix .O0, $(TARGETS)) $(addsuffix .O1, $(TARGETS)) $(addsuffix .O2, $(TARGETS)) $(addsuffix .O3, $(TARGETS)) TRAP_stats.csv *~ -rf

