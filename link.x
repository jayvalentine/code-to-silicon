OUTPUT_FORMAT(elf32-microblazeel)

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
  } > BRAM

  .data ALIGN(4) : {
    *(.data)
  } > BRAM
  
  .bss ALIGN(4) : {
    *(.bss)
  } > BRAM

  .crap ALIGN(4) : {
    *(.*)
  } > BRAM
}
