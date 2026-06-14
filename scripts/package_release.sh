#!/bin/sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

rm -f student_spot.zip

zip -r student_spot.zip . \
  -x ".venv/*" \
  -x "__pycache__/*" \
  -x "*/__pycache__/*" \
  -x ".pytest_cache/*" \
  -x "*/.pytest_cache/*" \
  -x "*.pyc" \
  -x ".DS_Store" \
  -x "*/.DS_Store" \
  -x "instance/*" \
  -x "student_spot.zip"

echo "Created student_spot.zip"
