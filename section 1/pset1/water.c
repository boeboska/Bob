/****************************************************************************
 * water.c
 *
 * CS50
 * Bob Borsboom
 *
 * This is the second CS50 program.
 * This program makes you aware of how much water you use during a shower.
 *
 * Demonstrates use of:
 * - function printf;
 * - function if and else if;
 * - how to use a variable.
 ***************************************************************************/

#include <stdio.h>
#include <cs50.h>

int main (void)

{
    // the line below asks the user for a intergeR > 0
    printf("how many minutes do you shower? \n");
    int i = get_int();
    if (i > 0)
    {
        // computes the minutes you shower times twelve, because 1 minute shower is twelve bottles of water
        printf("Wow! that means that you are using %i bottles of water!\n", i * 12);
    }
    // checks if the input from the user is smaller or equal to 0
    else if (i <= 0)
    {
        printf("typ in a number greater than 0\n");
    }
}