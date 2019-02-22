#define SQUARE(x) ((x) * (x))

int result;
const int A[8] = {1, 2, 3, 4, 5, 6, 7, 8};

int sum_squares_8(const int* arr)
{
  int sum = 0;

  sum += SQUARE(arr[0]);
  sum += SQUARE(arr[1]);
  sum += SQUARE(arr[2]);
  sum += SQUARE(arr[3]);
  sum += SQUARE(arr[4]);
  sum += SQUARE(arr[5]);
  sum += SQUARE(arr[6]);
  sum += SQUARE(arr[7]);

  return sum;
}

void application(void)
{
  result = sum_squares_8(&A[0]);
}
