/****************************************************************************
 * greedy.c
 *
 * CS50
 * Bob Borsboom
 *
 * This is the fourth CS50 program.
 * This program calculates the minimum number of coins required to give a user change.
 *
 * Demonstrates the use of:
 * - floats and integers.
 * - do while loops and while loops.
 ***************************************************************************/

#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main (void)
{
    int schuld = 0;
    int coins = 0;
    float geld;

    // this block blow ensures that the user types in a number greater than 0
    do
    {
        printf("how much dollar do I owe you?\n");
        geld = get_float();
        // the line below convert the dollars into cents
        schuld = round(geld * 100);
    }
    while (schuld < 0 );

    {
        // the loops below increase the 'coins' and it decreases the 'schuld' untill schuld = 0
        while ( schuld >= 25)
        {
            schuld = schuld - 25;
            coins++;
        }
        while ( schuld >= 10)
        {
            schuld = schuld - 10;
            coins++;
        }
        // if 'schuld' < 10 and if 'schuld' > 5 it counts how many times 5 fits in the remaining number
        while (schuld >= 5)
        {
            schuld = schuld - 5;
            coins++;
        }
        while (schuld >= 1)
        {
            schuld = schuld - 1;
            coins++;
        }
        // the line below print out the sum of the coins
        printf("%i\n", coins);
    }
}