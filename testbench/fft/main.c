void application(void);
void test(void);

#define SAMPLES 8

extern short result[1 << SAMPLES];

unsigned int state = 777;

short rand(void)
{
  state = state * 1664525 + 1013904223;
  return (state >> 16);
}

int main()
{
  /* Set up sin wave samples. */
  for (int i = 0; i < (1<<SAMPLES); i++)
  {
      result[i] = rand();
  }

  application();

  // Make sure that the application and test are split up.
  // The linker might place the test_failed (or equally test_passed)
  // function right after application, and we don't want to get a
  // false positive when MicroBlaze fetches the first instruction while
  // in the process of returning.
  asm("nop");
  asm("nop");
  asm("nop");
  asm("nop");

  test();
}
