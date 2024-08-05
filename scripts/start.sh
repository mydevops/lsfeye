#!/usr/bin/env bash

PDM_PYTHON_FILE=".pdm-python"

if [ -f "$PDM_PYTHON_FILE" ]; then
    PYTHON=$(<"$PDM_PYTHON_FILE")
    $PYTHON -m src
else
    echo "$PDM_PYTHON_FILE file does not exist."
fi