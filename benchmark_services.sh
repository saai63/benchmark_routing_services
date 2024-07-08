#!/bin/bash

# Constants
VENV_NAME="benchmark_services"
VENV_PATH="$HOME/python_envs"
VENV="$VENV_PATH"/"$VENV_NAME"

prepare_python_env() {
    if [ ! -d "$VENV_PATH" ]; then
        echo "Creating folder $VENV_PATH"
        mkdir "$VENV_PATH"
    fi
    python3 -m venv "$VENV"
    source $VENV/bin/activate
    pip install -r requirements.txt
}

prepare_python_env
python benchmark_services.py
deactivate
