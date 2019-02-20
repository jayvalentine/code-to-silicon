
#define SQUARE(x) ((x) * (x))

int sum_squares_8(const int* A)
{
  int sum = 0;

  sum += SQUARE(A[0]);
  sum += SQUARE(A[1]);
  sum += SQUARE(A[2]);
  sum += SQUARE(A[3]);
  sum += SQUARE(A[4]);
  sum += SQUARE(A[5]);
  sum += SQUARE(A[6]);
  sum += SQUARE(A[7]);

  return sum;
}

const int A[8] = {1, 2, 3, 4, 5, 6, 7, 8};

int main()
{
  volatile int sum = sum_squares_8(A);

  return 0;
}