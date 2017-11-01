#include <cs50.h>
#include <stdio.h>


int main (void)

{

    int height = 5;

    for(int i = 0; i < 5; i++)
    {
        for(int j = 0; j < i + 1; j++)
        {
            printf("#");
            printf(" ");
        }
        for(int k = 0; k < height - i - 1; k++)
        {
            printf(" ");
            printf(" ");
        }

    printf("\n");
    }
}