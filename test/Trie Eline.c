/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>

#include "dictionary.h"

// declare functions for later use
node* insert(char* word, struct node* trie, int letter_number);
node* create_node();

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // determine length of input word
    int length = strlen(word);

    node* trie = trie_root;
    int number;

    // iterate over each letter in word
    for (int i = 0; i < length; i++)
    {
        // determine value of current letter
        number = tolower(word[i]) - 'a';

        // if the current char is a '\'', set number to 26
        if (number < 0)
        {
            number = APOSTROPHE;
        }

        if (trie->children[number] != NULL)
        {
            trie = trie->children[number];
        }
        else
        {
            return false;
        }
    }
    if (trie->is_word == true)
    {
        return true;
    }
    else
    {
        return false;
    }
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // create an array containing nodes for each letter of the alphabet
    trie_root = create_node();

    // open dictionary file
    FILE* dict = fopen(dictionary, "r");

    // make sure script stops if file is empty
    if (dict == NULL)
    {
        return false;
    }

    // inititalize variables
    int index = 0;
    char word[LENGTH + 1];
    word_count = 0;

    // spell-check each word in text
    for (int c = fgetc(dict); c != EOF; c = fgetc(dict))
    {
        // allow only alphabetical characters and apostrophes
        if (isalpha(c) || (c == '\'' && index > 0))
        {
            // append character to word
            word[index] = c;
            index++;

            // ignore alphabetical strings too long to be words
            if (index > LENGTH)
            {
                // consume remainder of alphabetical string
                while ((c = fgetc(dict)) != EOF && isalpha(c));

                // prepare for new word
                index = 0;
            }
        }

        // ignore words with numbers (like MS Word can)
        else if (isdigit(c))
        {
            // consume remainder of alphanumeric string
            while ((c = fgetc(dict)) != EOF && isalnum(c));

            // prepare for new word
            index = 0;
        }

        // we must have found a whole word
        else if (index > 0)
        {
            // terminate current word
            word[index] = '\0';

            // increase word count
            word_count++;

            // insert word in dictionary trie
            insert(word, trie_root, 0);

            // prepare for new word
            index = 0;
        }
    }

    // close dictionary when loaded into memory
    fclose(dict);
    return true;
}


/**
 * Returns number of words in dictionary if loaded else 0.
 */
unsigned int size(void)
{
    return word_count;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{

    if (unload_root(trie_root) == true)
    {
        return true;
    }
    else
    {
        return false;
    }
}

/**
 * Inserts new letters in the word tree if necessary.
 */
node* insert(char* word, node* trie, int letter_number)
{
    int length = strlen(word);
    int number = word[letter_number] - 97;

    // if the current char is a ', set number to the position of apostrophe
    if (number < 0)
    {
        number = 26;
    }

    if (trie->children[number] == NULL)
    {
        // set pointers
        trie->children[number] = create_node();
        //printf("nieuwe node gemaakt\n");
    }

    // when end of the word is reached, set boolean to true
    if (length == letter_number + 1)
    {
        // set is_word to true since this node represents the end of a word
        trie->children[number]->is_word = true;
        return 0;
    }

    // else, insert next letter in word
    else
    {
        insert(word, trie->children[number], letter_number + 1);
    }

    // return dictionary trie
    return trie;
}

/**
 * Allocates, creates and returns new node.
 */
node* create_node()
{
    // allocate memory for node
    node* new_node = malloc(sizeof(node));

    // check if malloc indeed give us memory
    if (new_node == NULL)
    {
        return NULL;
    }

    // iterate over pointers of this node
    for (int i = 0; i < POINTERS; i++)
    {
        // set all pointers (children) to NULL
        new_node->children[i] = NULL;
    }

    // set is_word to false
    new_node->is_word = false;

    // return new node
    return new_node;
}

/**
 * Unloads nodes from bottom to top from memory. Returns true if succesfull.
 */

bool unload_root(node* root)
{
    for (int i = 0; i < POINTERS; i++)
    {
        if (root->children[i] != NULL)
        {
            unload_root(root->children[i]);
        }
    }
    free(root);
    return true;
}