/****************************************************************************
 * mario.c
 *
 * CS50
 * Bob Borsboom
 *
 * This is the third CS50 program.
 * This program prints out a double half-pyramid of a specified height. Just like in the game mario.
 *
 * Demonstrates the use of:
 * - function printf;
 * - function if and else if;
 * - how to use a variable;
 * - do while loops;
 * - for loops.
 ***************************************************************************/
#include <stdio.h>
#include <cs50.h>

int main (void)
{
    int hoogte;


    do
    {
        // the line below asks the user for a integer between 0 and 24
        printf("give me a number between 0 and 24\n");
        hoogte = get_int();
    }
    // the line below ensures that the user types in a number between 0 and 24
    while (hoogte < 0 || hoogte > 23);

    // the for loops print the pyramid, it count the hashes and the spaces
    for (int i = 0 ; i < (hoogte) ; i++)
    {
        for (int s = 0 ; s < hoogte - 1 - i ; s++)
        {
            printf(" ");
        }
        for (int h = 0 ; h < ( i + 1) ; h++)
        {
            printf("#");
        }
        {
            printf("  ");
        }
        for (int h = 0 ; h < ( i + 1) ; h++)
        {
            printf("#");
        }
        {
            printf("\n");
        }
    }
}
