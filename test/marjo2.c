#include <cs50.h>
#include <stdio.h>

int main (void)

{

    int height = 7;

    for(int i = 0; i < height; i++)
    {
        for(int k = 0; k < i; k++)
        {
            printf(".");
        }
        for(int j = 0; j < height - i; j++)
        {
            printf("#");
        }
        printf("\n");
    }

}
