# Disabled: v42

TARGETS = AES crc engine fir2 hanoi pocsag tolstoy bcnt des fft lms queens blit dhry fib gamma matrix mib_off_strsearch quicksort mib_auto_basicmath whets heapsort jpeg

all: $(TARGETS)

$(TARGETS): $(addsuffix .c, $(TARGETS))
	$(CC) -o $@ $(CFLAGS) $(addsuffix .c, $@) -lm

run: $(TARGETS)
	./benchmarkProc.py $(SIMULATOR) 5 $(TARGETS)

clean:
	rm $(TARGETS) TRAP_stats.csv *~ -rf

