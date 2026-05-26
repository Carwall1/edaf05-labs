#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_WORDS 5000
#define WORD_LEN 5

// The Adjacency List representing our graph
int *graph[MAX_WORDS];
int degree[MAX_WORDS];

// Array to hold our unique vocabulary
char words[MAX_WORDS][WORD_LEN + 1];
int unique_n = 0;

// Helper function for qsort and bsearch to compare strings
int compare_strings(const void *a, const void *b)
{
    return strcmp((const char *)a, (const char *)b);
}

// Function to check if an edge exists from u to v
int has_edge(const char *u, const char *v)
{
    int req[26] = {0};
    int avail[26] = {0};

    // Count last 4 letters of u
    for (int i = 1; i < 5; i++)
    {
        req[u[i] - 'a']++;
    }

    // Count all 5 letters of v
    for (int i = 0; i < 5; i++)
    {
        avail[v[i] - 'a']++;
    }

    // Check if v has all required letters
    for (int i = 0; i < 26; i++)
    {
        if (req[i] > avail[i])
        {
            return 0; // False
        }
    }
    return 1; // True
}

// The Breadth-First Search Algorithm
void bfs(int start_idx, int end_idx)
{
    if (start_idx == end_idx)
    {
        printf("0\n");
        return;
    }

    // A simple array acts as our Queue
    int queue[MAX_WORDS];
    int head = 0, tail = 0;

    // Array to track visited status and distance simultaneously.
    // -1 means unvisited.
    int dist[MAX_WORDS];
    for (int i = 0; i < unique_n; i++)
        dist[i] = -1;

    // Start BFS
    queue[tail++] = start_idx;
    dist[start_idx] = 0;

    while (head < tail)
    {
        int curr = queue[head++];
        int curr_dist = dist[curr];

        // Check all neighbors
        for (int i = 0; i < degree[curr]; i++)
        {
            int neighbor = graph[curr][i];

            if (neighbor == end_idx)
            {
                printf("%d\n", curr_dist + 1);
                return;
            }

            if (dist[neighbor] == -1)
            {
                dist[neighbor] = curr_dist + 1;
                queue[tail++] = neighbor;
            }
        }
    }

    printf("Impossible\n");
}

int main()
{
    int n, q;

    // Read N and Q
    if (scanf("%d %d", &n, &q) != 2)
        return 0;

    // Read the vocabulary into a temporary array
    char temp_words[MAX_WORDS][WORD_LEN + 1];
    for (int i = 0; i < n; i++)
    {
        scanf("%s", temp_words[i]);
    }

    // Sort the temporary array alphabetically
    qsort(temp_words, n, sizeof(temp_words[0]), compare_strings);

    // Remove duplicates to build the unique vocabulary list
    for (int i = 0; i < n; i++)
    {
        if (i == 0 || strcmp(temp_words[i], temp_words[i - 1]) != 0)
        {
            strcpy(words[unique_n], temp_words[i]);
            unique_n++;
        }
    }

    // Build the graph using dynamic memory allocation for the edges
    for (int i = 0; i < unique_n; i++)
    {
        // Temporarily store edges in a large array
        int temp_edges[MAX_WORDS];
        int edge_count = 0;

        for (int j = 0; j < unique_n; j++)
        {
            if (i != j && has_edge(words[i], words[j]))
            {
                temp_edges[edge_count++] = j;
            }
        }

        // Allocate exactly the right amount of memory for this node's edges
        degree[i] = edge_count;
        graph[i] = (int *)malloc(edge_count * sizeof(int));
        for (int e = 0; e < edge_count; e++)
        {
            graph[i][e] = temp_edges[e];
        }
    }

    // Process Queries
    char start_word[WORD_LEN + 1];
    char end_word[WORD_LEN + 1];

    for (int i = 0; i < q; i++)
    {
        scanf("%s %s", start_word, end_word);

        // Find the integer index of the strings using Binary Search
        void *start_ptr = bsearch(start_word, words, unique_n, sizeof(words[0]), compare_strings);
        void *end_ptr = bsearch(end_word, words, unique_n, sizeof(words[0]), compare_strings);

        // Safety Net: If a queried word isn't in our dictionary, it's impossible
        if (start_ptr == NULL || end_ptr == NULL)
        {
            printf("Impossible\n");
        }
        else
        {
            // Calculate the array index from the returned pointer
            int start_idx = ((char *)start_ptr - (char *)words) / sizeof(words[0]);
            int end_idx = ((char *)end_ptr - (char *)words) / sizeof(words[0]);

            bfs(start_idx, end_idx);
        }
    }

    // Free allocated memory (good practice in C)
    for (int i = 0; i < unique_n; i++)
    {
        free(graph[i]);
    }

    return 0;
}