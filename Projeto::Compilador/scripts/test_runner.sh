#!/bin/bash

TEST_DIR="../tests"
RES_DIR="${TEST_DIR}/res"
COMPILER="../src/translator.py"
LOG_FILE="test_results.log"

# Create results directory if it doesn't exist
mkdir -p "$RES_DIR"

# Clear log file
> "$LOG_FILE"

test_file() {
    local file=$1
    local filename=$(basename "$file")
    local output_file="${RES_DIR}/${filename%.txt}.ewvm"
    
    echo -e "\n=== Testing $filename ===" | tee -a "$LOG_FILE"
    
    python3 "$COMPILER" "$file" > "$output_file" 2>> "$LOG_FILE"
    if [ $? -ne 0 ]; then
        echo "❌ Error in compiling" | tee -a "$LOG_FILE"
        return 1
    fi
    
    echo "✅ Compiled successfully" | tee -a "$LOG_FILE"
    echo "EWVM output saved to $output_file" | tee -a "$LOG_FILE"
    
    return 0
}

echo "Running tests in $TEST_DIR..." | tee -a "$LOG_FILE"
echo "Output will be saved in $RES_DIR" | tee -a "$LOG_FILE"

passed=0
failed=0

for testfile in "$TEST_DIR"/test*.txt; do
    test_file "$testfile"
    if [ $? -eq 0 ]; then
        ((passed++))
    else
        ((failed++))
    fi
done

echo -e "\n=== Summary ===" | tee -a "$LOG_FILE"
echo "Passed Tests: $passed" | tee -a "$LOG_FILE"
echo "Failed Tests: $failed" | tee -a "$LOG_FILE"

exit $failed