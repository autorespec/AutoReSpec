#!/bin/bash

set -e

OPENJML_VERSION="21-0.8"
TARGET_DIR="openjml"
MAJOR_DIR="major"
MAJOR_URL="https://mutation-testing.org/major-latest.zip"
MAJOR_ZIP="major-latest.zip"
VENV_DIR=".autorespec"
PYTHON_BIN="python3.12"

OS_TYPE=$(uname)
ARCH=$(uname -m)

if ! command -v $PYTHON_BIN &> /dev/null; then
    echo "$PYTHON_BIN not found."
    echo "Please install Python 3.12.8 from https://www.python.org/downloads/"
    exit 1
fi

if [[ "$OS_TYPE" == "Darwin" ]]; then
    ZIP_FILE="openjml-macos-13-${OPENJML_VERSION}.zip"
elif [[ "$OS_TYPE" == "Linux" ]]; then
    ZIP_FILE="openjml-linux-${OPENJML_VERSION}.zip"
else
    echo "Unsupported OS: $OS_TYPE"
    exit 1
fi

OPENJML_URL="https://github.com/OpenJML/OpenJML/releases/download/${OPENJML_VERSION}/${ZIP_FILE}"

if [[ -d "$TARGET_DIR" && -f "$TARGET_DIR/bin/openjml" ]]; then
    echo "OpenJML is already installed at '$TARGET_DIR'. Skipping download."
else
    echo "Downloading OpenJML for $OS_TYPE ($ARCH)..."
    curl -L -o "$ZIP_FILE" "$OPENJML_URL"
    echo "Extracting OpenJML to $TARGET_DIR..."
    mkdir -p "$TARGET_DIR"
    unzip -q "$ZIP_FILE" -d "$TARGET_DIR"
    rm "$ZIP_FILE"
fi

if [[ -d "$MAJOR_DIR" && -f "$MAJOR_DIR/bin/major" ]]; then
    echo "Major is already installed at '$MAJOR_DIR'. Skipping download."
else
    echo "Downloading Major..."
    curl -L -o "$MAJOR_ZIP" "$MAJOR_URL"
    echo "Extracting Major to $MAJOR_DIR..."
    unzip -q "$MAJOR_ZIP"
    rm "$MAJOR_ZIP"
fi

if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating Python virtual environment..."
    $PYTHON_BIN -m venv "$VENV_DIR"
fi

if [[ "$OS_TYPE" == "Darwin" || "$OS_TYPE" == "Linux" ]]; then
    source "$VENV_DIR/bin/activate"
else
    source "$VENV_DIR/Scripts/activate"
fi

echo "Installing Python dependencies..."
if [[ -f "requirements.txt" ]]; then
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "No requirements.txt found. Skipping package installation."
fi

echo "Setup complete."
echo "OpenJML path: $TARGET_DIR"
echo "Major path: $MAJOR_DIR"
echo "Virtual environment: $VENV_DIR"
