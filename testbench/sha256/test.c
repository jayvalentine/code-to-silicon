#include <stdint.h>

#include "application_vars.h"

// This is the only way I can think of to force the compiler
// not to combine test_failed and test_passed.
volatile int dummy;

void test_failed(void) __attribute__((section(".break")));

void test_passed(void) __attribute__((section(".break")));

const uint8_t check[32] = {
  0x20, 0xC1, 0x89, 0x2D,
  0xF4, 0xE6, 0x65, 0x66,
  0x65, 0x58, 0x28, 0x93,
  0x67, 0xAE, 0x16, 0x82,
  0xD1, 0xF9, 0x3B, 0xC5,
  0xBE, 0x40, 0x49, 0x62,
  0x74, 0x92, 0xCD, 0xB5,
  0xA4, 0x26, 0x35, 0xE4
};

void test(void)
{
  for (int i = 0; i < 32; i++)
  {
    if (result[i] != check[i]) test_failed();
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
