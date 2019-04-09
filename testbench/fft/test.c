#define SAMPLES 6

// This is the only way I can think of to force the compiler
// not to combine test_failed and test_passed.
volatile int dummy;

extern short result[1 << SAMPLES];

void __attribute__((noinline)) test_failed(void) __attribute__((section(".break")));

void __attribute__((noinline)) test_passed(void) __attribute__((section(".break")));

void test(void)
{
  int failed = 0;

  for (int i = 0; i < (1 << SAMPLES); i++)
  {
    if (result[i] != 0) failed = 1;
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
