#include <stdint.h>

#include "application_vars.h"

// This is the only way I can think of to force the compiler
// not to combine test_failed and test_passed.
volatile int dummy;

void __attribute__((noinline)) test_failed(void) __attribute__((section(".break")));

void __attribute__((noinline)) test_passed(void) __attribute__((section(".break")));

const uint8_t check[32] = {
  0x50, 0xcd, 0xfa, 0xe1, 0x75, 0x27, 0x62, 0xd1,
  0xc6, 0xe1, 0xaa, 0x44, 0xdd, 0x9e, 0x03, 0x22,
  0x76, 0x6c, 0xa0, 0x7e, 0x69, 0x76, 0x60, 0xb1,
  0x77, 0x8f, 0x5c, 0x33, 0x72, 0x85, 0x89, 0xc6
};

void test(void)
{
  int failed = 0;
  for (int i = 0; i < 32; i++)
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
