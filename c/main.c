
#define APPROX_E_TO_X(x) ((x+1) + ((x*x)/2) + ((x*x*x)/6) + ((x*x*x*x)/24))

void matrix_e_to_x(int* M, int* R)
{
  int M_0 = M[0];
  int M_1 = M[1];

  R[0] = APPROX_E_TO_X(M_0);
  R[1] = APPROX_E_TO_X(M_1);
}

int main()
{
  int M[2] = {1, 2};
  int R[2];

  matrix_e_to_x(M, R);

  return 0;
}