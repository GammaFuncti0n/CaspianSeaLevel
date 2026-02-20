#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="plots"

find "$ROOT_DIR" -type f -name "*.pdf" | while read -r pdf; do
    echo "Converting: $pdf"

    tmp_pdf="${pdf%.pdf}_cmyk_tmp.pdf"

    gs \
      -dSAFER -dBATCH -dNOPAUSE \
      -sDEVICE=pdfwrite \
      -sProcessColorModel=DeviceCMYK \
      -sColorConversionStrategy=CMYK \
      -dOverrideICC \
      -sOutputFile="$tmp_pdf" \
      "$pdf"

    mv "$tmp_pdf" "$pdf"
done

echo "All PDFs converted to CMYK."