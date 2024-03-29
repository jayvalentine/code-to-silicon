OUTPUT_FORMAT(elf32-microblaze)

STACK_SIZE = 1024;

MEMORY
{
  BRAM (RWX) : ORIGIN = 0x00000000, LENGTH = 8K
}

SECTIONS
{
  . = 0x00000000;
  e = .;
  ENTRY(e)

  .entry ALIGN(4) : {
    *(.entry)
  } > BRAM

  .text ALIGN(4) : {
    *(.text.startup)
    *(.text)
    . += 32;
    *(.break)
  } > BRAM

  .data ALIGN(4) : {
    *(.data)
    *(.rodata)
  } > BRAM

  .bss ALIGN(4) : {
    *(.bss)
  } > BRAM

  .crap ALIGN(4) : {
    *(.*)
  } > BRAM

  .stack ALIGN(4) : {
    . += STACK_SIZE;
    STACK_START = .;
  } > BRAM

  . = 0x44A00000;
  HW_ACCEL_PORT = .;
}
