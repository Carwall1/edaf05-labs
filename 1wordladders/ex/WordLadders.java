package ex;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.*;

public class WordLadders {

    // Helper function to check if a directed edge exists from u to v
    private static boolean hasEdge(String u, String v) {
        // Arrays to count the frequency of characters (a-z)
        int[] required = new int[26];
        int[] available = new int[26];

        // 1. Count the last 4 characters of the starting word (u)
        for (int i = 1; i < 5; i++) {
            required[u.charAt(i) - 'a']++;
        }

        // 2. Count all 5 characters of the destination word (v)
        for (int i = 0; i < 5; i++) {
            available[v.charAt(i) - 'a']++;
        }

        // 3. Check if we have enough of every required letter
        for (int i = 0; i < 26; i++) {
            if (required[i] > available[i]) {
                return false; // Missing an ingredient
            }
        }

        return true; // All required letters are present in sufficient quantities
    }

    // Helper function to build the adjacency list
    private static Map<String, List<String>> buildGraph(String[] words) {
        Map<String, List<String>> graph = new HashMap<>();

        // Initialize an empty list for each word
        for (String word : words) {
            graph.put(word, new ArrayList<>());
        }

        // Compare every word to build edges
        for (int i = 0; i < words.length; i++) {
            for (int j = 0; j < words.length; j++) {
                if (i != j && hasEdge(words[i], words[j])) {
                    graph.get(words[i]).add(words[j]);
                }
            }
        }

        return graph;
    }

    // The core BFS algorithm
    private static String bfs(Map<String, List<String>> graph, String start, String end) {
        if (start.equals(end)) {
            return "0";
        }

        // ArrayDeque gives us O(1) time complexity for queue operations
        Queue<String> queue = new ArrayDeque<>();

        // This map tracks visited nodes AND their distance from the start
        Map<String, Integer> distances = new HashMap<>();

        queue.add(start);
        distances.put(start, 0);

        while (!queue.isEmpty()) {
            String current = queue.poll();
            int currentDist = distances.get(current);

            for (String neighbor : graph.get(current)) {
                if (neighbor.equals(end)) {
                    return String.valueOf(currentDist + 1);
                }

                // If the neighbor is not in the distances map, it hasn't been visited
                if (!distances.containsKey(neighbor)) {
                    distances.put(neighbor, currentDist + 1);
                    queue.add(neighbor);
                }
            }
        }

        return "Impossible";
    }

    public static void main(String[] args) throws IOException {
        // Fast I/O setup required for competitive programming/algorithm labs
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        if (!st.hasMoreTokens())
            return;

        int N = Integer.parseInt(st.nextToken());
        int Q = Integer.parseInt(st.nextToken());

        String[] words = new String[N];
        for (int i = 0; i < N; i++) {
            st = new StringTokenizer(br.readLine());
            words[i] = st.nextToken();
        }

        // Build the graph once before processing queries
        Map<String, List<String>> graph = buildGraph(words);

        // Process each query
        for (int i = 0; i < Q; i++) {
            st = new StringTokenizer(br.readLine());
            String startWord = st.nextToken();
            String endWord = st.nextToken();

            String result = bfs(graph, startWord, endWord);
            System.out.println(result);
        }
    }
}