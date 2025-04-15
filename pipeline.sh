#!/bin/bash


DIRECTORY="scripts/pipeline"

# execute the python scripts in the correct order
scripts=(
    "filter.py"
    "expansion.py"
    "normalization.py"
    "linguistics.py"
    "merge.py"
)

# loop through the scripts and execute them
for script in "${scripts[@]}"; do
    echo "executing $script..."
    python3 "$DIRECTORY/$script"
    if [ $? -ne 0 ]; then
        echo "error executing $script. exiting."
        exit 1
    fi
done

echo "Pipeline completed successfully."