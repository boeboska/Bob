#include <stdio.h>
#include <ctype.h>
#include <stdio.h>
#include <sys/resource.h>
#include <sys/time.h>


int main (void)

{


int *p;

int a = 8;

p = &a;



    printf("adress of a is %x\n", (unsigned int) &a);

    printf("adress of p is %x\n", (unsigned int) &p);

    printf(" value of p is %i\n", *p);

    printf(" value of a is %i\n", a);

}