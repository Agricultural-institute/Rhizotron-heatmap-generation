#!/usr/bin/env bash

set -e
set -x

uv run ruff check src --fix
uv run ruff format src
