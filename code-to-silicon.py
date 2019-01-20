import compile

compile.gcc_compile(["c/main.c"], "main.o")

compile.gcc_link(["main.o"], "main.elf")

compile.objdump("main.elf", ["-d"], "main.asm")