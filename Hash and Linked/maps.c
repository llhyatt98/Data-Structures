/*

Project Description: 

Takes in a CSV file of various companies and maps each company into two different
maps; a Hash map and a map based on linked lists. I then conduct a performance study
which determines the amount of time it takes for the different data structure to 
store and fetch. 

 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

typedef struct
{
    char    *symbol;
    char    *name;
    float    lastSale;
    float    marketCap;
    int      IPOyear;
} Company;

//Prints elements of company
void PrintCompany(Company *c)
{
    printf("%s:\n", c->name);
    printf("\tSymbol: %s\n", c->symbol);
    /* .2f: only print two digits after the period. */
    printf("\tLast Sale: %.2f\n", c->lastSale);
    printf("\tMarket Capitalization: %.2f\n", c->marketCap);
    printf("\tYear of Initial Public Offering: %d\n", c->IPOyear);
}

void ReadFile(const char *filename, Company **companies_rv, int *numCompanies_rv)
{
    int  i, j;

    if (filename == NULL)
    {
        fprintf(stderr, "No filename specified!\n");
        exit(EXIT_FAILURE);
    }
    FILE *f_in = fopen(filename, "r");
    if (f_in == NULL)
    {
        fprintf(stderr, "Unable to open file \"%s\"\n", filename);
        exit(EXIT_FAILURE);
    }

    fseek(f_in, 0, SEEK_END);
    int numChars = ftell(f_in);
    // printf("The number of characters is %d\n", numChars);
    fseek(f_in, 0, SEEK_SET);

    char *file_contents = malloc(sizeof(char)*numChars);
    fread(file_contents, sizeof(char), numChars, f_in);
    fclose(f_in);
    /* Note: the memory for this array is used to populate
     * the fields of the companies.  If it is freed, then
     * the company structs all become invalid.  For the
     * context of this program, this array should not be 
     * freed. */

    // Find out how many lines there are
    int numLines = 0;
    for (i = 0 ; i < numChars ; i++)
        if (file_contents[i] == '\n')
            numLines++;
    // printf("Number of lines is %d\n", numLines);

    int      numCompanies = numLines-1; // first line is header info 
    Company *companies    = malloc(sizeof(Company)*numCompanies);

    /* strtok will parse the file_contents array.  
     * The first time we call it, it will replace every '"' with '\0'.
     * It will also return the first word before a 
     */
    int numColumns = 9;
    int numberOfQuotesPerColumn = 2;
    strtok(file_contents, "\"");
    for (i = 0 ; i < numberOfQuotesPerColumn*numColumns-1 ; i++)
         strtok(NULL, "\"");
    for (i = 0 ; i < numCompanies ; i++)
    {
         companies[i].symbol = strtok(NULL, "\"");
         strtok(NULL, "\"");
         companies[i].name = strtok(NULL, "\"");
         strtok(NULL, "\"");
         companies[i].lastSale = atof(strtok(NULL, "\""));
         strtok(NULL, "\"");
         companies[i].marketCap = atof(strtok(NULL, "\""));
         strtok(NULL, "\""); 

         /* Skip ADR TSO */
         strtok(NULL, "\"");
         strtok(NULL, "\"");

         companies[i].IPOyear = atoi(strtok(NULL, "\""));
         strtok(NULL, "\"");

         /* Skip Sector, Industry, Summary Quote */
         for (j = 0 ; j < 6 ; j++)
             strtok(NULL, "\"");

         //PrintCompany(companies+i);
    }

    /* Set parameters to have output values */
    *companies_rv    = companies;
    *numCompanies_rv = numCompanies;
}

/* ------------------------------------------------------------------------------- */
//Implementation of Map based on Hash Tables
//Original hash function
int hash(char *name, long array_size)
{
    int hashval = 0;
    char *p = name;
    while (*p != '\0')
    {
        hashval = 31*hashval + *p;
        p++;
    }

    return hashval%array_size;
}

//Second hash function (double hashing)
//Source for function: http://www.cs.yale.edu/homes/aspnes/pinewiki/C(2f)HashTables.html?highlight=%28CategoryAlgorithmNotes%29
#define BASE 256
int dhash(char *name, long array_size)
{
    long h;
    char *us;

    /* cast s to unsigned char * */
    /* this ensures that elements of s will be treated as having values >= 0 */
    us = (char *) name;
  
    h = 0;
    while(*us != '\0') 
    {
        h = (h * BASE + *us) % array_size;
        us++;
    }  

    return h;
}

typedef struct 
{
    int         numElements;
    char      **keys;
    Company    *companies;
} MapBasedOnHashTable;

void InitializeMapBasedOnHashTable(MapBasedOnHashTable *map, int numElements)
{
    map->numElements = numElements;
    map->keys = malloc(sizeof(char *)*numElements);
    map->companies = malloc(sizeof(Company)*numElements);
    for (int i = 0 ; i < numElements ; i++)
        map->keys[i] = NULL;
}

void StoreTo_MapBasedOnHashTable(MapBasedOnHashTable *map, Company *c)
{
    //First hash value
    int hashval = hash(c->symbol, map->numElements);
    //Second hash value
    int hashval2 = dhash(c->symbol, map->numElements);

    int idx = (hashval)%(map->numElements);

    if(idx < 0) idx += map->numElements;
    if(map->keys[idx] == NULL)
    {
        map->keys[idx]      = c->symbol;
        map->companies[idx] = *c;
        return;
    }
    else //If idx doesn't have a null, we go to another space
    {
        for (int i = 0 ; i < map->numElements ; i++)
        {
            int idx2 = (hashval2+i)%(map->numElements);   
            int new_idx = ((idx + i) * idx2)%(map->numElements);
            map->keys[new_idx]      = c->symbol;
            map->companies[new_idx] = *c;
            return;
        }
    }
}

Company *
FetchFrom_MapBasedOnHashTable(MapBasedOnHashTable *map, char *key)
{
    //First hash value
    int hashval = hash(key, map->numElements);
    //Second hash value
    int hashval2 = dhash(key, map->numElements);

    int idx = (hashval)%(map->numElements);

    if(idx < 0) idx += map->numElements;

    if(map->keys[idx] == NULL)
    {
        return NULL;
    }

    if(strcmp(map->keys[idx], key) == 0)
    {
        return &map->companies[idx];
    }
    
    for (int i = 0; i < map->numElements; i++)
    {
        int idx2 = (hashval2+i)%(map->numElements);   
        int new_idx = ((idx + i) * idx2)%(map->numElements);
        //If idx doesn't have a null, we go to another space
        if(map->keys[new_idx] == NULL)
        {
            return NULL;
        }
        if(strcmp(map->keys[new_idx], key) == 0)
        {
            return &map->companies[new_idx];
        }
    } 
    return NULL;  
}

void FetchAndPrint(MapBasedOnHashTable *mfht, char *key)
{
    Company *c = FetchFrom_MapBasedOnHashTable(mfht, key);
    if (c == NULL)
    {
        printf("Key %s has no corresponding company\n", key);
    }
    else
    {
        PrintCompany(c);
    }

}

/* ------------------------------------------------------------------------------- */
//Implementation of Map Based on Linked Lists

struct ll_node
{
    struct ll_node *next;
    char            *key;
    Company        *value;
};

struct ll_node *ll_insert(Company *v, struct ll_node *cur_head)
{
    struct ll_node *rv = malloc(sizeof(struct ll_node));
    rv->key = v->symbol;
    rv->value = v;
    rv->next = cur_head;
    return rv;
}

Company *ll_fetch(char *v, struct ll_node *cur_head) //Check this
{                            //v is what we want to fetch, cur_head is the front

    struct ll_node *curr = cur_head;
    //printf("%s\n", curr->value->symbol);
    while (curr != NULL)
    {
        if (strcmp(v, curr->key) == 0)
        {
            return curr->value;
        }
        curr = curr->next;
    }
    return NULL; /* nothing removed */
}

void ll_print(struct ll_node *head, char *key) //Need help on this 
{
    int counter = 0;
    Company *c = ll_fetch(key, head);
    //printf("%s\n", c->symbol);  
    if (c == NULL)
    {
        printf("Key %s has no corresponding company\n", key);
    }
    else
    {
        PrintCompany(c);
    }
}

/* ------------------------------------------------------------------------------- */

int main(int argc, char *argv[])
{
    Company *companies = NULL;
    int      numCompanies;
    ReadFile(argv[1], &companies, &numCompanies);

    struct timeval startTime; 
    struct timeval endTime;
    
    MapBasedOnHashTable mfht;
    // printf("num companies is %d\n", numCompanies);
    InitializeMapBasedOnHashTable(&mfht, numCompanies*2);

    //Timing storing
    gettimeofday(&startTime, 0);
    
    for (int i = 0 ; i < numCompanies ; i++)
    {
        StoreTo_MapBasedOnHashTable(&mfht, companies+i);
    }

    //Timing store
    gettimeofday(&endTime, 0);
    double hs_seconds = (double)(endTime.tv_sec - startTime.tv_sec) + 
                        (double)(endTime.tv_usec - startTime.tv_usec) / 1000000.;
    printf("Store for hash map executing, took %f\n", hs_seconds);



    //Timing fetching
    gettimeofday(&startTime, 0);

    FetchAndPrint(&mfht, "ZNWAA");
    FetchAndPrint(&mfht, "Z");
    FetchAndPrint(&mfht, "ZIOP");
    FetchAndPrint(&mfht, "ZIOQ");
    FetchAndPrint(&mfht, "YIOQ");
    FetchAndPrint(&mfht, "QIOQ");
    FetchAndPrint(&mfht, "WIOQ");
    FetchAndPrint(&mfht, "XIOQ");
    FetchAndPrint(&mfht, "TIOQ");
    FetchAndPrint(&mfht, "UIOQ");
    FetchAndPrint(&mfht, "VIOQ");

    gettimeofday(&endTime, 0);
    double hf_seconds = (double)(endTime.tv_sec - startTime.tv_sec) + 
                        (double)(endTime.tv_usec - startTime.tv_usec) / 1000000.;
    printf("Fetch for hash map executing, took %f\n", hf_seconds);




    struct ll_node *ll_head = NULL;
    //printf("num companies is %d\n", numCompanies);

    gettimeofday(&startTime, 0);

    for (int i = 0 ; i < numCompanies ; i++)
    {
        ll_head = ll_insert(companies+i,ll_head);
    }

    gettimeofday(&endTime, 0);
    double ls_seconds = (double)(endTime.tv_sec - startTime.tv_sec) + 
                        (double)(endTime.tv_usec - startTime.tv_usec) / 1000000.;
    printf("Store for hash map executing, took %f\n", ls_seconds);



    //Timing fetching
    gettimeofday(&startTime, 0);

    ll_print(ll_head, "ZNWAA");
    ll_print(ll_head, "Z");
    ll_print(ll_head, "ZIOP");
    ll_print(ll_head, "ZIOQ");
    ll_print(ll_head, "YIOQ");
    ll_print(ll_head, "QIOQ");
    ll_print(ll_head, "WIOQ");
    ll_print(ll_head, "XIOQ");
    ll_print(ll_head, "TIOQ");
    ll_print(ll_head, "UIOQ");
    ll_print(ll_head, "VIOQ");

    gettimeofday(&endTime, 0);
    double lf_seconds = (double)(endTime.tv_sec - startTime.tv_sec) + 
                        (double)(endTime.tv_usec - startTime.tv_usec) / 1000000.;
    printf("Fetch for linked lists executing, took %f\n", lf_seconds);

}

/* Performance Study:
 
    My choice of second hash function is incredibly similar to the first hash 
    except I am multiplying by a value called BASE. I defined this value as 256, 
    which is different than the original 36. Other than that, there are no 
    significant changes, and I have included the link to which I found the 
    dhash function. 

    My performance study has indicated that storing to my hash map takes longer than 
    my storing to the linked lists map. In terms of fetching, this is reversed, my 
    fetching from hash map takes less time than my fetching from linked lists. This
    certainly has something to do with the O(1) nature of fetching from a hash map,
    and the O(1) nature of insertion to a linked list. 

 */
