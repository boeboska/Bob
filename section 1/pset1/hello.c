/****************************************************************************
 * hello.c
 *
 * CS50
 * Bob Borsboom
 *
 * This is the first CS50 program. Typ in your name and the program will greet you!
 *
 * Demonstrates use of printf.
 ***************************************************************************/

#include <stdio.h>
#include <cs50.h>

int main (void)
{
    printf("Name: ");
    // variable x is a string
    string x = get_string();
    // fill in your name and the program will say hallo, your name
    printf("Hello, %s!\n", x);
}