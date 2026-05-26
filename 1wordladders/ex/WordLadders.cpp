#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <algorithm>

using namespace std;

// Helper function to check for directed edge
bool has_edge(const string &u, const string &v)
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
    // Check if v meets requirements
    for (int i = 0; i < 26; i++)
    {
        if (req[i] > avail[i])
            return false;
    }
    return true;
}

int main()
{
    // Fast I/O Optimization: Disconnects C++ streams from C streams for massive speed boosts
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    // Read N and Q, exit if end of file
    if (!(cin >> n >> q))
        return 0;

    vector<string> temp_words(n);
    for (int i = 0; i < n; i++)
    {
        cin >> temp_words[i];
    }

    // Sort and remove duplicates to create our unique vocabulary list
    sort(temp_words.begin(), temp_words.end());
    temp_words.erase(unique(temp_words.begin(), temp_words.end()), temp_words.end());

    int unique_n = temp_words.size();

    // Build the graph using an array of dynamically sized arrays (vectors)
    vector<vector<int>> graph(unique_n);
    for (int i = 0; i < unique_n; i++)
    {
        for (int j = 0; j < unique_n; j++)
        {
            if (i != j && has_edge(temp_words[i], temp_words[j]))
            {
                graph[i].push_back(j);
            }
        }
    }

    // Process Queries
    string start_word, end_word;
    for (int i = 0; i < q; i++)
    {
        cin >> start_word >> end_word;

        // Use binary search to find the integer index of the words instantly
        auto it_start = lower_bound(temp_words.begin(), temp_words.end(), start_word);
        auto it_end = lower_bound(temp_words.begin(), temp_words.end(), end_word);

        // Safety Net: Ensure the words were actually found in the dictionary
        if (it_start == temp_words.end() || *it_start != start_word ||
            it_end == temp_words.end() || *it_end != end_word)
        {
            cout << "Impossible\n";
            continue;
        }

        int start_idx = distance(temp_words.begin(), it_start);
        int end_idx = distance(temp_words.begin(), it_end);

        // Base Case
        if (start_idx == end_idx)
        {
            cout << "0\n";
            continue;
        }

        // Standard BFS Setup
        queue<int> qq;
        vector<int> dist(unique_n, -1); // -1 signifies unvisited

        qq.push(start_idx);
        dist[start_idx] = 0;
        bool found = false;

        while (!qq.empty())
        {
            int curr = qq.front();
            qq.pop();

            int current_dist = dist[curr];

            // Ranged-based for loop through neighbors
            for (int neighbor : graph[curr])
            {
                if (neighbor == end_idx)
                {
                    cout << current_dist + 1 << "\n";
                    found = true;
                    break;
                }

                if (dist[neighbor] == -1)
                {
                    dist[neighbor] = current_dist + 1;
                    qq.push(neighbor);
                }
            }
            if (found)
                break; // Break out of outer while loop
        }

        if (!found)
        {
            cout << "Impossible\n";
        }
    }

    return 0;
}