#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="plots"

counter=0
total=$(find "$ROOT_DIR" -type f -name "*.pdf" | wc -l)

find "$ROOT_DIR" -type f -name "*.pdf" | while read -r pdf; do
    ((counter += 1))
    echo "$counter/$total]"
    # echo "[$counter/$total] Converting: $pdf"

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