import sys
import math

def get_min_dist(points):
    n = len(points)
    
    # overhead of splitting isn't worth it for tiny arrays
    if n <= 3:
        min_d = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                d = math.hypot(points[i][0] - points[j][0], points[i][1] - points[j][1])
                if d < min_d:
                    min_d = d
        return min_d

    mid = n // 2
    mid_x = points[mid][0]

    dl = get_min_dist(points[:mid])
    dr = get_min_dist(points[mid:])
    d = min(dl, dr)

    # zero distance means duplicate points
    if d == 0.0:
        return d

    # filter points near the boundary line and sort by y
    # timsort handles these nearly empty arrays efficiently
    strip = [p for p in points if abs(p[0] - mid_x) < d]
    strip.sort(key=lambda p: p[1])

    strip_len = len(strip)
    for i in range(strip_len):
        # pigeonhole principle guarantees we only need to check the next 7 points
        for j in range(i + 1, min(i + 8, strip_len)):
            # break early if y difference already exceeds our current best distance
            if strip[j][1] - strip[i][1] >= d:
                break
            
            dist = math.hypot(strip[i][0] - strip[j][0], strip[i][1] - strip[j][1])
            if dist < d:
                d = dist

    return d

def main():
    raw_input = sys.stdin.read().split()
    if not raw_input:
        return
        
    n = int(raw_input[0])
    points = []
    
    for i in range(n):
        idx = 1 + i * 2
        points.append((float(raw_input[idx]), float(raw_input[idx+1])))
        
    # sort by x once at the very beginning
    points.sort(key=lambda p: p[0])
    
    min_distance = get_min_dist(points)
    print(f"{min_distance:.6f}")

if __name__ == '__main__':
    main()
