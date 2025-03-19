#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void forkthem(int);

int
main(int argc, const char **argv) {
  forkthem(5);
  return 0;
}

void
forkthem(int n) {
  if (n > 0) {
    fork();
    printf("%d\n", getpid());
    forkthem(n-1);
  }
}