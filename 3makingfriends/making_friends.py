import sys

def kruskal(num_nodes, edges):
    # timsort is optimized in C so its quick 0(nlogn), however slowest step 
    edges.sort() 

    parent = list(range(num_nodes + 1))
    rank = [0] * (num_nodes + 1)

    def find(i):
        # path halving avoids recursion limits
        while parent[i] != i:
            parent[i] = parent[parent[i]] 
            i = parent[i]
        return i

    total_time = 0
    edges_used = 0
    
    for weight, source, target in edges:
        root_source = find(source)
        root_target = find(target)
        
        # inline union avoids function call overhead in hot loop
        if root_source != root_target:
            # union by rank keeps the tree shallow
            if rank[root_source] < rank[root_target]:
                parent[root_source] = root_target
            elif rank[root_source] > rank[root_target]:
                parent[root_target] = root_source
            else:
                parent[root_target] = root_source
                rank[root_source] += 1
                
            total_time += weight
            edges_used += 1
            
            # mst complete at num_nodes - 1 edges
            if edges_used == num_nodes - 1:
                break
                
    return total_time

def solve():
    def get_ints():
        for line in sys.stdin:
            for x in line.split():
                yield int(x)
                
    tokens = get_ints()
    
    try:
        num_nodes = next(tokens)
        num_edges = next(tokens)
    except StopIteration:
        return

    edges = []
    for _ in range(num_edges):
        source = next(tokens)
        target = next(tokens)
        weight = next(tokens)
        # pack weight first for optimization so we dont have to change the sort and automatically sort by weight. 
        edges.append((weight, source, target))
        
    result = kruskal(num_nodes, edges)
    print(result)

if __name__ == '__main__':
    solve()