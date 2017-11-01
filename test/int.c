#include <cs50.h>
#include <stdio.h>

int main (void)
{

    int height = 4;

    for (int i = 0; i < height; i ++)
    {
        for(int j = 0; j < i; j++)
        {
            printf(".");
        }
        for(int k = 0; k < height - i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}