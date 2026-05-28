import sys

GAP_PENALTY = -4

def parse_input(lines):
    symbols = lines[0].split()
    num_symbols = len(symbols)

    # Build a lookup table where scores[a][b] gives the match score
    scores = {}
    for i in range(num_symbols):
        scores[symbols[i]] = {}
        row_scores = list(map(int, lines[i + 1].split()))
        for j in range(num_symbols):
            scores[symbols[i]][symbols[j]] = row_scores[j]

    num_queries = int(lines[num_symbols + 1])
    
    # Extract each pair of sequences that need to be aligned
    queries = [lines[num_symbols + 2 + q].split() for q in range(num_queries)]
    
    return scores, queries

def compute_dp_table(seq1, seq2, scores):
    len1, len2 = len(seq1), len(seq2)

    # dp[i][j] stores the best alignment score
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    # Base cases: aligning characters against only gaps
    for i in range(1, len1 + 1):
        dp[i][0] = i * GAP_PENALTY
    for j in range(1, len2 + 1):
        dp[0][j] = j * GAP_PENALTY
        
    for i in range(1, len1 + 1):
        char1 = seq1[i - 1]
        curr_row = dp[i]
        prev_row = dp[i - 1]
        
        for j in range(1, len2 + 1):
            char2 = seq2[j - 1]
            
            # Option 1: align current characters together
            match_score = prev_row[j - 1] + scores[char1][char2]

            # Option 2: insert a gap into seq1
            gap_seq1 = curr_row[j - 1] + GAP_PENALTY

            # Option 3: insert a gap into seq2
            gap_seq2 = prev_row[j] + GAP_PENALTY
            
            # Pick the highest scoring transition
            best = match_score
            if gap_seq1 > best:
                best = gap_seq1
            if gap_seq2 > best:
                best = gap_seq2

            curr_row[j] = best
            
    return dp

def backtrack(dp, seq1, seq2, scores):
    aligned1, aligned2 = [], []
    i, j = len(seq1), len(seq2)
    
    # Reconstruct alignment by tracing backwards from bottom-right
    while i > 0 or j > 0:

        # Characters were aligned together
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + scores[seq1[i - 1]][seq2[j - 1]]:
            aligned1.append(seq1[i - 1])
            aligned2.append(seq2[j - 1])
            i -= 1
            j -= 1

        # Gap inserted into second sequence
        elif i > 0 and dp[i][j] == dp[i - 1][j] + GAP_PENALTY:
            aligned1.append(seq1[i - 1])
            aligned2.append('*')
            i -= 1

        # Gap inserted into first sequence
        else:
            aligned1.append('*')
            aligned2.append(seq2[j - 1])
            j -= 1
            
    # Alignment was built backwards, so reverse before returning
    return ''.join(reversed(aligned1)), ''.join(reversed(aligned2))

def solve():
    lines = sys.stdin.read().strip().split('\n')

    if not lines or not lines[0]:
        return

    scores, queries = parse_input(lines)

    # Solve each alignment query independently
    for seq1, seq2 in queries:
        dp = compute_dp_table(seq1, seq2, scores)
        res1, res2 = backtrack(dp, seq1, seq2, scores)
        print(f"{res1} {res2}")

if __name__ == '__main__':
    solve()