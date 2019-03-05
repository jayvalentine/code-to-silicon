#include "application_vars.h"

// This is the only way I can think of to force the compiler
// not to combine test_failed and test_passed.
volatile int dummy;

void test_failed(void) __attribute__((section(".break")));

void test_passed(void) __attribute__((section(".break")));

void test(void)
{
  int failed = 0;
  if (result != 204)
  {
    failed = 1;
  }

  if (failed)
  {
    // Avoid erroneous failure by ensuring that MicroBlaze won't accidentally prefetch
    // the test_failed address.
    asm("nop");
    asm("nop");
    asm("nop");
    asm("nop");
    test_failed();
  }
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
