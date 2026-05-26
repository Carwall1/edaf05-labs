import sys
from collections import deque

def make_graph(word_list):
    # Get rid of duplicates by converting to a set, then back to a list
    unique_words = list(set(word_list))
    
    graph = {}
    for w in unique_words:
        graph[w] = []
        
    # Save the letter counts in dictionaries so we don't recalculate them
    needed_letters = {}
    available_letters = {}
    
    for word in unique_words:
        # Count what we need from this word (the last 4 letters)
        req = {}
        for letter in word[-4:]:
            if letter in req:
                req[letter] += 1
            else:
                req[letter] = 1
        needed_letters[word] = req
        
        # Count all the letters this word can provide
        avail = {}
        for letter in word:
            if letter in avail:
                avail[letter] += 1
            else:
                avail[letter] = 1
        available_letters[word] = avail

    # Find which words connect to each other
    for word1 in unique_words:
        req = needed_letters[word1]
        
        for word2 in unique_words:
            # A word shouldn't connect to itself
            if word1 == word2:
                continue
                
            avail = available_letters[word2]
            
            # Check if word2 has enough letters to satisfy word1
            can_connect = True
            for letter in req:
                if letter not in avail or avail[letter] < req[letter]:
                    can_connect = False
                    break 
                    
            if can_connect:
                graph[word1].append(word2)
                
    return graph

def find_shortest_path(graph, start, end):
    # Check if words actually exist in our graph
    if start not in graph or end not in graph:
        return "Impossible"

    if start == end:
        return 0

    # Setup the queue for BFS
    queue = deque()
    queue.append((start, 0))
    
    # Keep track of visited words 
    visited_words = set()
    visited_words.add(start)

    while len(queue) > 0:
        current_word, steps = queue.popleft()

        # Check all the connected words
        for neighbor in graph[current_word]:
            if neighbor == end:
                return steps + 1
            
            if neighbor not in visited_words:
                visited_words.add(neighbor)
                queue.append((neighbor, steps + 1))

    return "Impossible"

def main():
    data = sys.stdin.read().split()
    
    # Check for empty input to avoid errors
    if len(data) == 0:
        return

    num_words = int(data[0])
    num_queries = int(data[1])

    my_words = data[2 : num_words + 2]
    
    # Build the dictionary of connections once
    word_graph = make_graph(my_words)

    # Figure out where the queries start in the data list
    query_start_index = num_words + 2

    # Process each query
    for i in range(num_queries):
        idx1 = query_start_index + (i * 2)
        idx2 = query_start_index + (i * 2) + 1
        
        start_word = data[idx1]
        end_word = data[idx2]
        
        ans = find_shortest_path(word_graph, start_word, end_word)
        print(ans)

if __name__ == "__main__":
    main()