// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 260000 + 2600 + 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int hashIx = hash(word);

    // convert to lowercase
    char lowerWord[LENGTH + 1];
    int ii;
    for (ii = 0; word[ii] != '\0'; ii++)
    {
        lowerWord[ii] = tolower(word[ii]);
    }
    lowerWord[ii] = '\0'; // terminate the string

    node *ptr = table[hashIx];
    while (ptr != NULL)
    {
        if (strcmp(ptr->word, lowerWord) == 0)
            return true;
        ptr = ptr->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int ix1 = toupper(word[0]) - 'A';
    int ix2 = 0;
    if (word[1] != '\0' && isalpha(word[1]))
        ix2 = toupper(word[1]) - 'A';

    int ix3 = 0;
    if (word[1] != '\0' && word[2] != '\0' && isalpha(word[2]))
        ix3 = toupper(word[2]) - 'A';

    return ix1 * 10000 + ix2 * 100 + ix3;

    // return toupper(word[0]) - 'A';  // original hash function
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *fp = fopen(dictionary, "r");
    if (fp == NULL)
    {
        printf("Error: could not open file %s", dictionary);
        return false;
    }

    node *prevNode = NULL;
    node *currNode = NULL;

    // Read line by line
    char buffer[LENGTH + 2]; // to accommodate newline at the end
    while (fgets(buffer, LENGTH + 2, fp))
    {
        if (strcmp(buffer, "at") == 0)
            printf("found1 [%s]\n", buffer);

        // Remove trailing newline
        buffer[strcspn(buffer, "\n")] = 0;

        currNode = (node *) malloc(sizeof(node));
        strcpy(currNode->word, buffer);
        currNode->next = NULL;

        if (strcmp(buffer, "at") == 0)
            printf("found [%s][%s]\n", buffer, currNode->word);

        int hashIndex = hash(buffer);
        if (table[hashIndex] == NULL)
            table[hashIndex] = currNode; // first node in the particular bucket
        else
        {
            node *tmp = table[hashIndex];
            // printf("step 1\n");
            while (tmp->next != NULL)
            {
                tmp = tmp->next;
            }
            tmp->next = currNode; // append currNode at the end
        }
    }

    // close the file
    fclose(fp);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    node *ptr = NULL;
    int count = 0;
    for (int ii = 0; ii < N; ii++)
    {
        ptr = table[ii];
        while (ptr != NULL)
        {
            count++;
            ptr = ptr->next;
        }
    }
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int ii = 0; ii < N; ii++)
    {
        node *ptr1 = table[ii];
        node *ptr2 = NULL;
        while (ptr1 != NULL)
        {
            ptr2 = ptr1;
            ptr1 = ptr1->next;
            free(ptr2);
        }
    }
    return true;
}
