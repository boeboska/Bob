#include <stdio.h>
#include <cs50.h>

int main (void)

{

int height;
printf("number: \n");
height = get_int();

for(int i = 0; i > height - 1; i++)
{
    for(int j = 0; j < i; j++)
    {
        printf(" ");
    }
    for(int x = 0; x < height - i -1; x++)
    {
        printf("#");
    }
    printf("\n");
}



}

