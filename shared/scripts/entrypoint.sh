#!/usr/bin/env bash

# Initialize Conda in the shell
eval "$(conda shell.bash hook)"
conda activate server

# Execute the command passed to the container
exec "$@"
