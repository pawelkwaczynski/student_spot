#!/bin/sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

rm -f student_spot.zip

zip -r student_spot.zip . \
  -x ".git/*" \
  -x ".venv/*" \
  -x "__pycache__/*" \
  -x "*/__pycache__/*" \
  -x ".pytest_cache/*" \
  -x "*/.pytest_cache/*" \
  -x "*.pyc" \
  -x ".DS_Store" \
  -x "*/.DS_Store" \
  -x "instance/*" \
  -x "docs/*.local.md" \
  -x ".env" \
  -x ".env.local" \
  -x ".env.production" \
  -x ".env.development" \
  -x ".env.test" \
  -x "student_spot/*" \
  -x "student_spot_profesor/*" \
  -x "student_spot_dev_handoff/*" \
  -x "student_spot*.zip"

echo "Created student_spot.zip"
