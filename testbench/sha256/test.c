#include <stdint.h>

#include "application_vars.h"

// This is the only way I can think of to force the compiler
// not to combine test_failed and test_passed.
volatile int dummy;

void __attribute__((noinline)) test_failed(void) __attribute__((section(".break")));

void __attribute__((noinline)) test_passed(void) __attribute__((section(".break")));

const uint8_t check[32] = {
  0x1E, 0xA0, 0xF3, 0x15,
  0xC6, 0x5A, 0x04, 0xB8,
  0x9D, 0xC7, 0x13, 0x3E,
  0x6B, 0xEF, 0x6F, 0xC7,
  0xD4, 0xD8, 0xCE, 0x4E,
  0x91, 0x36, 0xE0, 0x7D,
  0xAD, 0xC1, 0xD0, 0x65,
  0x83, 0xE6, 0x45, 0x8E
};

void test(void)
{
  int failed = 0;
  for (int i = 0; i < 3; i++)
  {
    if (check[i] != result[i]) failed = 1;
  }

  if (failed) test_failed();
  test_passed();
}

void test_failed(void)
{
  dummy = dummy * 2;
}

void test_passed(void)
{
  dummy = dummy + 3;
}
