import sys
from collections import deque

def build_graph(words):
    # SAFETY NET 1: Remove duplicates from the vocabulary list
    unique_words = list(set(words))
    
    # Initialize the graph
    graph = {word: [] for word in unique_words}
    
    required_counts = {}
    available_counts = {}
    
    # Pre-compute letter frequencies for blazing speed
    for w in unique_words:
        req = {}
        for char in w[-4:]:
            req[char] = req.get(char, 0) + 1
        required_counts[w] = req
        
        avail = {}
        for char in w:
            avail[char] = avail.get(char, 0) + 1
        available_counts[w] = avail

    # Build edges using the pre-computed counts
    for u in unique_words:
        u_req = required_counts[u]
        
        for v in unique_words:
            if u == v:
                continue
            
            v_avail = available_counts[v]
            
            edge_valid = True
            for char, needed in u_req.items():
                if v_avail.get(char, 0) < needed:
                    edge_valid = False
                    break 
                    
            if edge_valid:
                graph[u].append(v)
                
    return graph

def bfs(graph, start_word, end_word):
    # SAFETY NET 2: If the query asks for a word not in our dictionary, it's impossible
    if start_word not in graph or end_word not in graph:
        return "Impossible"

    # Base case: distance to itself is 0
    if start_word == end_word:
        return 0

    queue = deque([(start_word, 0)])
    visited = set([start_word])

    while queue:
        current_word, dist = queue.popleft()

        for neighbor in graph[current_word]:
            if neighbor == end_word:
                return dist + 1
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return "Impossible"

def main():
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    N = int(input_data[0])
    Q = int(input_data[1])

    words = input_data[2:N+2]
    queries_data = input_data[N+2:]

    graph = build_graph(words)

    # SAFETY NET 3: Loop exactly Q times, ignoring any trailing garbage in the file
    for i in range(Q):
        start_word = queries_data[i * 2]
        end_word = queries_data[i * 2 + 1]
        
        result = bfs(graph, start_word, end_word)
        print(result)

if __name__ == "__main__":
    main()