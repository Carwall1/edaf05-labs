import sys
from collections import deque

def solve():
    raw_input = sys.stdin.read().split()
    if not raw_input:
        return
        
    N = int(raw_input[0])
    M = int(raw_input[1])
    C = int(raw_input[2])
    P = int(raw_input[3])
    
    edges = []
    idx = 4

    # (source, destination, capacity)
    for _ in range(M):
        edges.append((int(raw_input[idx]), int(raw_input[idx+1]), int(raw_input[idx+2])))
        idx += 3
        
    # Order in which edges are removed from the network
    plan = [int(raw_input[idx+i]) for i in range(P)]
    
    def get_max_flow(remove_count):

        banned_edges = set(plan[:remove_count])

        # Residual graph
        cap = {i: {} for i in range(N)}
        
        for i, (u, v, c) in enumerate(edges):
            if i not in banned_edges:
                cap[u][v] = c
                cap[v][u] = c
                
        total_flow = 0
        
        # Edmonds-Karp algorithm. find augmenting paths using BFS
        while True:
            q = deque([(0, float('inf'))])
            parent = {0: -1}
            pushed = 0
            
            while q:
                curr, flow = q.popleft()
                
                # Reached sink node, so we found a valid augmenting path
                if curr == N - 1:
                    pushed = flow
                    break
                    
                for nxt, capacity in cap[curr].items():
                    if capacity > 0 and nxt not in parent:
                        parent[nxt] = curr

                        # Flow through path is limited by smallest edge capacity
                        q.append((nxt, min(flow, capacity)))
                        
            # No augmenting path left, max flow reached
            if not pushed:
                break
                
            total_flow += pushed
            
            # Update residual capacities along the chosen path
            curr = N - 1
            while curr != 0:
                prev = parent[curr]
                cap[prev][curr] -= pushed
                cap[curr][prev] += pushed
                curr = prev
                
        return total_flow

    low = 0
    high = P
    best_k = 0
    best_flow = 0
    
    # Binary search for the maximum number of removable edges
    while low <= high:
        mid = (low + high) // 2
        current_flow = get_max_flow(mid)
        
        # If required capacity still exists, try removing more edges
        if current_flow >= C:
            best_k = mid
            best_flow = current_flow
            low = mid + 1
        else:
            high = mid - 1
            
    print(f"{best_k} {best_flow}")

if __name__ == '__main__':
    solve()

    #./check_solution.sh pypy3 railway_planning.py