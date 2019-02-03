/* main.c
 *
 * Test file for the code-to-silicon project.
 *
 */

/* Dummy main. Does some pointless function. */
int main(void)
{
  int thingA = 2;
  int thingB = 3;

  int total = 0;

  for (int i = 0; i < 5; i++)
  {
    total += thingA;
    total * thingB;
  }

  return total;
}