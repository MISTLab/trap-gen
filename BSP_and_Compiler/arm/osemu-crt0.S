#include "newlib.h"

/* ANSI concatenation macros.  */
#define CONCAT(a, b) CONCAT2(a, b)
#define CONCAT2(a, b) a ## b

#ifdef __USER_LABEL_PREFIX__
#define FUNCTION( name ) CONCAT (__USER_LABEL_PREFIX__, name)
#else
#error __USER_LABEL_PREFIX is not defined
#endif

#ifdef HAVE_INITFINI_ARRAY
#define _init   __libc_init_array
#define _fini   __libc_fini_array
#endif

/* .text is used instead of .section .text so it works with arm-aout too.  */
    .text
#if defined(__thumb2__)
    .syntax unified
    .thumb
.macro FUNC_START name
    .global \name
    .thumb_func
\name:
.endm
#else
    .code 32
.macro FUNC_START name
    .global \name
\name:
.endm
#endif
    .align  0

    FUNC_START  _mainCRTStartup
    FUNC_START  _start
    FUNC_START  start
#if defined(__ELF__) && !defined(__USING_SJLJ_EXCEPTIONS__)
    /* Annotation for EABI unwinding tables.  */
    .fnstart
#endif

/* In case we are using our hardware component to manage MP we do not want
software to set the stack pointers. Note that in case we are using the hardware
component, the stack has already been set, otherwise it is equal to 0 */
    cmp sp, #0
    bne .NOSPSET

    /*  Set up the stack pointer to a fixed value */
    /*  Changes by toralf:
        - Allow linker script to provide stack via __stack symbol - see
          defintion of .Lstack
        - Provide "hooks" that may be used by the application to add
          custom init code - see .Lhwinit and .Lswinit
        - Go through all execution modes and set up stack for each of them.
          Loosely based on init.s from ARM/Motorola example code.
              Note: Mode switch via CPSR is not allowed once in non-privileged
            mode, so we take care not to enter "User" to set up its sp,
            and also skip most operations if already in that mode. */

    ldr r3, .Lstack
    cmp r3, #0
    ldreq   r3, .LC0
    /* Note: This 'mov' is essential when starting in User, and ensures we
         always get *some* sp value for the initial mode, even if we
         have somehow missed it below (in which case it gets the same
         value as FIQ - not ideal, but better than nothing.) */
    mov sp, r3
    mrs r2, CPSR
    tst r2, #0x0F   /* Test mode bits - in User of all are 0 */
    beq .LC23       /* "eq" means r2 AND #0x0F is 0 */
    msr     CPSR_c, #0xD1   /* FIRQ mode, interrupts disabled */
    mov     sp, r3
    sub sl, sp, #0x1000 /* This mode also has its own sl (see below) */

    mov r3, sl
    msr     CPSR_c, #0xD7   /* Abort mode, interrupts disabled */
    mov sp, r3
    sub r3, r3, #0x1000

    msr     CPSR_c, #0xDB   /* Undefined mode, interrupts disabled */
    mov sp, r3
    sub r3, r3, #0x1000

    msr     CPSR_c, #0xD2   /* IRQ mode, interrupts disabled */
    mov sp, r3
    sub r3, r3, #0x2000

    msr     CPSR_c, #0xD3   /* Supervisory mode, interrupts disabled */
    mov sp, r3
    sub r3, r3, #0x8000 /* Min size 32k */
    bic r3, r3, #0x00FF /* Align with current 64k block */
    bic r3, r3, #0xFF00

    str r3, [r3, #-4]   /* Move value into user mode sp without */
    ldmdb   r3, {sp}^       /* changing modes, via '^' form of ldm */

    orr r2, r2, #0xC0   /* Back to original mode, presumably SVC, */
    msr CPSR_c, r2  /* with FIQ/IRQ disable bits forced to 1 */
.LC23:
    /* Setup a default stack-limit in-case the code has been
       compiled with "-mapcs-stack-check".  Hard-wiring this value
       is not ideal, since there is currently no support for
       checking that the heap and stack have not collided, or that
       this default 64k is enough for the program being executed.
       However, it ensures that this simple crt0 world will not
       immediately cause an overflow event:  */
    sub sl, r3, #64 << 10   /* Still assumes 256bytes below sl */

.NOSPSET:
    /* Zero the memory in the .bss section.  */
    mov     a2, #0          /* Second arg: fill value */
    mov fp, a2          /* Null frame pointer */
    mov r7, a2          /* Null frame pointer for Thumb */

    ldr a1, .LC1        /* First arg: start of memory block */
    ldr a3, .LC2
    sub a3, a3, a1      /* Third arg: length of block */

#if defined(__thumb__) && !defined(__thumb2__)
    /* Enter Thumb mode.... */
    add a4, pc, #1  /* Get the address of the Thumb block */
    bx  a4      /* Go there and start Thumb decoding  */

    .code 16
    .global __change_mode
    .thumb_func
__change_mode:
#endif

    bl  FUNCTION (memset)

/* Changes by toralf: Taken from libgloss/m68k/crt0.S
 * initialize target specific stuff. Only execute these
 * functions it they exist.
 */
    ldr r3, .Lhwinit
    cmp r3, #0
    beq .LC24
    mov lr, pc
    mov pc, r3
.LC24:
    ldr r3, .Lswinit
    cmp r3, #0
    beq .LC25
    mov lr, pc
    mov pc, r3
.LC25:
    mov r0, #0      /*  no arguments  */
    mov r1, #0      /*  no argv either */

#ifdef __USES_INITFINI__
    /* Some arm/elf targets use the .init and .fini sections
       to create constructors and destructors, and for these
       targets we need to call the _init function and arrange
       for _fini to be called at program exit.  */
    mov r4, r0
    mov r5, r1
    ldr r0, .Lfini
    bl  FUNCTION (atexit)
    bl  FUNCTION (_init)
    mov r0, r4
    mov r1, r5
#endif
    bl  FUNCTION (main)

    bl  FUNCTION (exit)     /* Should not return.  */

    /* For Thumb, constants must be after the code since only
       positive offsets are supported for PC relative addresses.  */

    .align 0
.LC0:

    /* Changes by toralf: Provide alternative "stack" variable whose value
       may be defined externally; .Lstack will be used instead of .LC0 if
       it points to a non-0 value. Also set up references to "hooks" that
           may be used by the application to provide additional init code. */

#ifdef __pe__
    .word   0x800000
#else
    .word   0x80000         /* Top of RAM on the PIE board.  */
#endif
.Lstack:
    .word   __stack
.Lhwinit:
    .word   FUNCTION (hardware_init_hook)
.Lswinit:
    .word   FUNCTION (software_init_hook)

    /* Set up defaults for the above variables in the form of weak symbols
       - so that application will link correctly, and get value 0 in
       runtime (meaning "ignore setting") for the variables, when the user
       does not provide the symbols. (The linker uses a weak symbol if,
       and only if, a normal version of the same symbol isn't provided
       e.g. by a linker script or another object file.) */

    .weak __stack
    .weak FUNCTION (hardware_init_hook)
    .weak FUNCTION (software_init_hook)

#if defined(__ELF__) && !defined(__USING_SJLJ_EXCEPTIONS__)
    /* Protect against unhandled exceptions.  */
    .cantunwind
    .fnend
#endif
.LC1:
    .word   __bss_start__
.LC2:
    .word   __bss_end__
#ifdef __USES_INITFINI__
.Lfini:
    .word   FUNCTION(_fini)
#endif

.global .__nop_busy_loop
.__nop_busy_loop:
    b .__nop_busy_loop

FUNC_START _osEmuError
    mov r0, #-1
    bl _exit

#ifdef __pe__
    .section .idata$3
    .long   0,0,0,0,0,0,0,0
#endif
