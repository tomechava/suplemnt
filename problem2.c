#include <stdio.h>
#include <pthread.h>

void*
threadthem(void *);

int
main(int argc, char *argv) {
  pthread_t thread;

  pthread_create(&thread, NULL, threadthem, (void *) 5);
  printf("%d\n", thread);
  return 0;
}

void*
threadthem(void *arg) {
  int n = (int) arg;
  
  if (n > 0) {
    pthread_t thread;
    pthread_create(&thread, NULL, threadthem, (void *) (n - 1));
    printf("%d\n", thread);
  }
}