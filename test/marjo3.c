#include <cs50.h>
#include <stdio.h>

int main (void)
{

    int height = 5;


    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < height - i - 1; j++)
        {
            printf(".");
        }
        for(int k = 0; k < i + 1; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}