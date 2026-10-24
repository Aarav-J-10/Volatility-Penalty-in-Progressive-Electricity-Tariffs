#!/bin/bash
# usage: build.sh name.md OUTSTEM
set -e
cd "$(dirname "$0")"
pandoc "$1" -o "$2.docx" --reference-doc=reference.docx --resource-path=.
soffice --headless --convert-to pdf "$2.docx" >/dev/null 2>&1
pdfinfo "$2.pdf" | grep Pages
