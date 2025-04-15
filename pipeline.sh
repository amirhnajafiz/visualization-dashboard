#!/bin/bash

# This script executes a series of Python scripts in a specific order.
# The results of each script are used as input for the next script.
# The scripts are located in the "scripts/pipeline" directory.
# The output files are stored in the "tmp" directory.
# The script also creates a "datasets" directory if it does not exist.
# The results of the final scripts are stored in the "datasets" directory.

# set running command to python3 if exists, otherwise use python
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "[inf] using $PYTHON_CMD to run the scripts."

# global variables
OUTPUT_DIR="tmp"
DIRECTORY="scripts/pipeline"
DATA_DIR="assets/datasets"

# check if the output directory exists, if not create it
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir "$OUTPUT_DIR"
fi
if [ ! -d "$DATA_DIR" ]; then
    mkdir "$DATA_DIR"
fi

echo "[inf] output directories are created."

# execute the python scripts in the correct order
scripts=(
    "filter.py"
    "decouple.py"
    "normalization.py"
    "linguistics.py"
    "merge.py"
)

# loop through the scripts and execute them
for script in "${scripts[@]}"; do
    echo "[inf] executing $script ..."
    $PYTHON_CMD "$DIRECTORY/$script"
    if [ $? -ne 0 ]; then
        echo "[err] error executing $script. exiting."
        exit 1
    fi
done

# run the final scripts to create the final output
echo "[inf] executing final scripts ..."

$PYTHON_CMD "scripts/sampling.py"
if [ $? -ne 0 ]; then
    echo "[err] error executing sampling.py. exiting."
    exit 1
fi

$PYTHON_CMD "scripts/preload.py"
if [ $? -ne 0 ]; then
    echo "[err] error executing preload.py. exiting."
    exit 1
fi

echo "pipeline completed successfully."
echo "the output files are in the $OUTPUT_DIR directory."
