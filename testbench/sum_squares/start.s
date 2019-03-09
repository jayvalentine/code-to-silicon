    .section .entry,"ax",@progbits
    .align 2
start:
    addik r1, r0, STACK_START
    addik r13, r0, HW_ACCEL_PORT
    brlid r15, main
    nop
    nop
