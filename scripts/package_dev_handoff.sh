#!/bin/sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

OUTPUT="student_spot_dev_handoff.zip"
WORKDIR="$(mktemp -d)"
PACKAGE_DIR="$WORKDIR/student_spot_dev_handoff"

cleanup() {
  rm -rf "$WORKDIR"
}
trap cleanup EXIT

mkdir -p "$PACKAGE_DIR/docs" "$PACKAGE_DIR/app/static" "$PACKAGE_DIR/app/templates/main" "$PACKAGE_DIR/app/translations" "$PACKAGE_DIR/source_info"

cp README.md "$PACKAGE_DIR/"
cp baza_wiedzy.md "$PACKAGE_DIR/"
cp plan_pokazowy_student_spot.md "$PACKAGE_DIR/"
cp prezentacja_ustna_10_min.md "$PACKAGE_DIR/"
cp requirements.txt "$PACKAGE_DIR/"
cp .env.example "$PACKAGE_DIR/"

cp docs/PROJECT_REPORT.md "$PACKAGE_DIR/docs/"
cp docs/FROG_DEPLOYMENT.md "$PACKAGE_DIR/docs/"
cp docs/ODDANIE_PROJEKTU.md "$PACKAGE_DIR/docs/"

cp -R app/static/css "$PACKAGE_DIR/app/static/"
cp -R app/static/js "$PACKAGE_DIR/app/static/"
cp -R app/static/media/brand "$PACKAGE_DIR/app/static/media-brand"
cp -R app/static/media/visuals "$PACKAGE_DIR/app/static/media-visuals"
cp app/templates/base.html "$PACKAGE_DIR/app/templates/"
cp app/templates/main/info.html "$PACKAGE_DIR/app/templates/main/"
cp app/templates/main/demo.html "$PACKAGE_DIR/app/templates/main/"
cp app/translations/pl.py "$PACKAGE_DIR/app/translations/"
cp app/translations/en.py "$PACKAGE_DIR/app/translations/"

cp source_info/keyvisual_info.md "$PACKAGE_DIR/source_info/"
cp source_info/keyvisual_info_update.md "$PACKAGE_DIR/source_info/"
cp source_info/logo.png "$PACKAGE_DIR/source_info/"
cp source_info/background_new.png "$PACKAGE_DIR/source_info/"
cp source_info/pop_up_welcome.png "$PACKAGE_DIR/source_info/"
cp source_info/popup_en.png "$PACKAGE_DIR/source_info/"

rm -f "$OUTPUT"
(cd "$WORKDIR" && zip -r "$ROOT_DIR/$OUTPUT" student_spot_dev_handoff)

echo "Created $OUTPUT"
