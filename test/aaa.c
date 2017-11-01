#include <stdio.h>
#include <cs50.h>
#include <string.h>


int main (void)
{

#define MAX_INT = 99;

    int guess;
    int answer = rand();

    do
    {
        printf("number between 0 - 99: ");
        guess = get_int();
    }while (guess == answer);

    printf("you guesset is!\n");
    printf("your guess was %d, and the answer is %d!", guess, answer);
}