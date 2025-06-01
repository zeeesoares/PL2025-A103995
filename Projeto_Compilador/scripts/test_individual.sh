#!/bin/bash

TEST_DIR="../tests"
COMPILER="../src/main.py"
RES_DIR="${TEST_DIR}/res"
LOG_FILE="test_results.log"

test_individual() {
    local test_num=$1
    local file="${TEST_DIR}/test${test_num}.txt"
    local output_file="${RES_DIR}/test${test_num}.astewvm"
    
    if [ ! -f "$file" ]; then
        echo "Error: Test file $file not found"
        return 1
    fi
    
    rm -f "$output_file"
    
    echo -e "\n=== Testing test$test_num ==="
    echo "Input file: $file"
    echo "Output file: $output_file"
    
    python3 "$COMPILER" "$file" > "$output_file"
    
    if [ ${PIPESTATUS[0]} -ne 0 ]; then
        echo "❌ Compilation failed"
        return 1
    fi
    
    echo "✅ Compiled successfully"
    echo "Verify with: cat $output_file"
    
    return 0
}

if [ $# -eq 0 ]; then
    echo "Usage: $0 <test_number>"
    echo "Example: $0 1  (will test ../tests/test1.txt)"
    exit 1
fi

test_individual "$1"