    .section .entry,"ax",@progbits
    .align 2
start:
    addik r1, r0, STACK_START
    brlid r15, main
    nop
    nop
