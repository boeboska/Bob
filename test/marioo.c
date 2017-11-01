#include <cs50.h>
#include <stdio.h>

int main (void)

{

int height;
printf("number\n");
height = get_int();



for(int i = 0; i < height; i++)
{
    for(int k = 0; k < height - i - 1; k++)
    {
        printf(".");
    }
    for(int j = 0; j <= i; j++)
    {
        printf("#");
    }
    printf(".");
    for(int l = 0; l <= i; l++)
    {
        printf("#");
    }
    for(int m = 0; m < height - i - 1; m++)
    {
        printf(".");
    }
    printf("\n");

}


}