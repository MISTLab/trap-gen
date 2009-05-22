# Remember to add the -DBIG_TARGET option to the CFLAGS in case we are compiling for a big endian system

# SLOW: mib_auto_basicmath whets MSD heapsort mib_auto_basicmath2
# FAIL: SearchGame wavelt
TARGETS = AES crc engine fir2 hanoi jpeg pocsag tolstoy bcnt des fft g3fax lms queens v42 blit dhry fib gamma huff matrix mib_off_strsearch quicksort

all: $(TARGETS)

$(TARGETS): $(addsuffix .c, $@)
	$(CC) -o $@ $(CFLAGS) $(addsuffix .c, $@) -lm

run: $(TARGETS)
	./benchmarkProc.py $(SIMULATOR) 5 $(TARGETS)

clean:
	rm $(TARGETS) TRAP_stats.csv *~ -rf

