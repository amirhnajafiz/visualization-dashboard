#!/bin/bash


OUTPUT_DIR="tmp"
DIRECTORY="scripts/pipeline"

# check if the output directory exists, if not create it
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir "$OUTPUT_DIR"
fi

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

echo "pipeline completed successfully."
echo "the output files are in the $OUTPUT_DIR directory."
