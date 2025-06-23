#!/usr/bin/env bash

set -e
set -x

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install python libraries
uv venv
uv sync

# Install pre-commit
uv run pre-commit uninstall
uv run pre-commit install
