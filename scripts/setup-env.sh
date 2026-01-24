#!/bin/bash
# Copyright (c) 2025 TrailLensCo
# All rights reserved.
#
# This file is proprietary and confidential.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"

setup_venv() {
    echo "Setting up Python virtual environment..."

    if [ -d "${VENV_DIR}" ]; then
        echo "Virtual environment already exists at ${VENV_DIR}"
        read -p "Remove and recreate? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Removing existing virtual environment..."
            rm -rf "${VENV_DIR}"
        else
            echo "Keeping existing virtual environment"
            return 0
        fi
    fi

    echo "Creating virtual environment..."
    python3 -m venv "${VENV_DIR}"

    echo "Activating virtual environment..."
    # shellcheck disable=SC1091
    source "${VENV_DIR}/bin/activate"

    echo "Upgrading pip..."
    pip install --upgrade pip

    echo "Installing dependencies..."
    pip install -r "${SCRIPT_DIR}/requirements.txt"

    echo "Installing md2docx and md2pptx packages..."
    cd "${SCRIPT_DIR}/md2docx" && pip install -e .
    cd "${SCRIPT_DIR}/md2pptx" && pip install -e .

    echo ""
    echo "Setup complete!"
    echo ""
    echo "To activate the virtual environment, run:"
    echo "  source ${SCRIPT_DIR}/.venv/bin/activate"
}

main() {
    if [ "${1:-}" = "setup" ] || [ $# -eq 0 ]; then
        setup_venv
    else
        echo "Usage: $0 [setup]" >&2
        exit 1
    fi
}

main "$@"
