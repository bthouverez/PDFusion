#! /bin/bash
echo 'Installing PDFusion'
cp mergePDF.py pdfusion
chmod +x pdfusion
mv pdfusion /usr/local/bin
echo "PDFusion installed"
echo "Use pdfusion -h"