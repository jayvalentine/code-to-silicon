void application(void);
void test(void);

int main()
{
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
