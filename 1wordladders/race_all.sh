#!/bin/bash

echo "========================================"
echo "🛠️  PRE-TEST SETUP: COMPILING LANGUAGES"
echo "========================================"

echo "Compiling C program (-O3 optimization)..."
gcc -O3 WordLadders.c -o WordLadders_c

echo "Compiling C++ program (-O3 optimization)..."
g++ -O3 WordLadders.cpp -o WordLadders_cpp

echo "Compiling Java program..."
javac WordLadders.java

echo "Compilation complete!"
echo ""

echo "========================================"
echo "🏎️  LANE 1: C++ TESTS"
echo "Command: ./WordLadders_cpp"
echo "========================================"
time ./check_solution.sh ./WordLadders_cpp
echo ""

echo "========================================"
echo "🏎️  LANE 2: C TESTS"
echo "Command: ./WordLadders_c"
echo "========================================"
time ./check_solution.sh ./WordLadders_c
echo ""

echo "========================================"
echo "🏎️  LANE 3: JAVA TESTS"
echo "Command: java WordLadders"
echo "========================================"
time ./check_solution.sh java WordLadders
echo ""

echo "========================================"
echo "🏎️  LANE 4: PYTHON TESTS"
echo "Command: python3 WordLadders.py"
echo "========================================"
time ./check_solution.sh python3 WordLadders.py
echo ""

echo "🏁 The Grand Prix is complete! Scroll up to compare the 'real' time totals for each language."