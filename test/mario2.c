#include <stdio.h>
#include <cs50.h>

int main (void)

{

int height;
printf("number \n");
height = get_int();

for (int i = 0; i < height; i++)
{
    for(int j = 0; j < i; j++)
    {
        printf(".");
    }
    for(int k =0; k < height - i; k++)
    {
        printf("#");
    }



    printf("\n");
}



}
