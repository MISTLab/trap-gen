#ifdef __ELF__
#define TYPE(x) .type x,function
#else
#define TYPE(x)
#endif

.section        ".exception_vectors", "ax"
.align 2
.global _exception_vectors
TYPE(_exception_vectors)

_exception_vectors:
    b _mainCRTStartup
    b _osEmuError      // vector for undefined instructions
    b _osEmuError      // vector for software interrupts
    b _osEmuError      // vector for prefectch abort
    b _osEmuError      // vector for data abort
    nop                // blank word
    b _osEmuError      // vector for IRQ (normal interrupts)
    b _osEmuError      // vector for FIQ (fast interrupts)
    nop                // lets leave a blank word before the start of the real code
    .end _exception_vectors
