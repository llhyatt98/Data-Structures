/*
Project Description: 

This code implements a queue data structure to manage a file which contains
donors and recipients for transplants. When a hospital is open, and there is
a donor and recipient of the same sex available, then the two are matched. 

*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define QUEUE_SIZE 10

typedef struct
{
    int front;
    int back;
    char *strings[QUEUE_SIZE];
} Queue;

void InitializeQueue(Queue *q)
{
    q->front = 0;
    q->back = 0;
}

void Enqueue(Queue *q, char *new_val)
{
    int curr = ((q->back)%10); //If it is past index 9
    q->strings[curr] = new_val; 
    //Need to use strdup so that fget does not change new_val
    //q->back = curr;
    q->back = (q->back+1)%10;
}

char *Front(Queue *q)
{
    if(q->front == q->back)
    {
        return NULL;
    }
    else
    {
        return q->strings[q->front];
    }
}

char *Dequeue(Queue *q)
{
    if(q->front == q->back){
        return NULL;
    }

    char *val;
    val = q->strings[(q->front)];
    q->front = (q->front+1)%10;
    return val;
}

void PrintQueue(Queue *q)
{
    int i;
    printf("Printing queue %p\n", q);
    printf("\tThe index for the front of the queue is %d\n", q->front);
    printf("\tThe index for the back of the queue is %d\n", q->back);
    if (q->front == q->back)
    {
        printf("\tThe queue is empty.\n");
        return;
    }
    int back = q->back;
    if (q->back < q->front)
    {
        // wrapped around, so modify indexing 
        back += QUEUE_SIZE;
    }

    for (i = q->front ; i < back ; i++)
    {
        printf("\t\tEntry[%d] = \"%s\"\n", i%QUEUE_SIZE, q->strings[i%QUEUE_SIZE]);
    }
}

void PrettyPrintQueue(Queue *q, char *type)
{
    if (Front(q) == NULL)
    {
        printf("No unmatched entries for %s\n", type);
    }
    else
    {
        char *s;
        printf("Unmatched %s:\n", type);
        while ((s = Dequeue(q)))
        {
            printf("\t%s\n", s);
        }
    }
}

char *NewString(char *s)
{
    int len = strlen(s);
    char *rv = malloc(len);
    strcpy(rv, s);
    rv[len-1] = '\0'; /* take out newline */
    return rv;
}

int main(int argc, char *argv[])
{

//File pointers
FILE *input;

//Opening the file to read binary
input = fopen(argv[1], "rb");

//Creating array to copy
int size = 256;

//Hospitals
Queue hospitals;
InitializeQueue(&hospitals);
//Female donors 
Queue female_donors;
InitializeQueue(&female_donors);
//Male donors
Queue male_donors;
InitializeQueue(&male_donors);
//Male recipients
Queue male_recipients; 
InitializeQueue(&male_recipients);
//Female recipients
Queue female_recipients; 
InitializeQueue(&female_recipients);

char read[size];
//Logic for reading file
while(fgets(read, size, input) != NULL) {

    char *line = NewString(read);

    //Enqueueing
    if(line[0] == 'H')
        Enqueue(&hospitals, (line+2));
    if(line[0] == 'R')
    {
        if(line[2] == 'M')
        {
            Enqueue(&male_recipients, (line+4));
        }
        else if(line[2] == 'F')
        {
            Enqueue(&female_recipients, (line+4));
        }
    }
    if(line[0] == 'D')
    {
        if(line[2] == 'M')
        {
            Enqueue(&male_donors, (line+4));  
        }
        else if(line[2] == 'F')   
        {
            Enqueue(&female_donors, (line+4));
        }          
    }

    //Dequeueing
    if((Front(&female_recipients) != NULL) & (Front(&female_donors) != NULL) & (Front(&hospitals) != NULL))
    {
        char *recip = Dequeue(&female_recipients);
        char *donor = Dequeue(&female_donors);
        char *hosp = Dequeue(&hospitals);
        printf("MATCH: %s donates to %s at hospital %s\n", donor, recip, hosp);
    }

    if((Front(&male_recipients) != NULL) & (Front(&male_donors) != NULL) & (Front(&hospitals) != NULL))
    {
        char *recip = Dequeue(&male_recipients);
        char *donor = Dequeue(&male_donors);
        char *hosp = Dequeue(&hospitals);
        printf("MATCH: %s donates to %s at hospital %s\n", donor, recip, hosp);
    }
}

    PrettyPrintQueue(&female_donors, "female donors");
    PrettyPrintQueue(&female_recipients, "female recipients");
    PrettyPrintQueue(&male_donors, "male donors");
    PrettyPrintQueue(&male_recipients, "male recipients");
    PrettyPrintQueue(&hospitals, "hospitals");

fclose(input);

}
