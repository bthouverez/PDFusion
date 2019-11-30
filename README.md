# PDFusion
GUI for merging PDF using PyPDF2 and PyQT

* PyPDF2 : merging PDF
* img2pdf : turning images into PDF
* PyQT : graphical

## Linux install

```bash
sudo sh install.sh
```
PDFusion will be installed under /usr/local/bin


## Usage
    pdfusion [OPTION] [INPUTDIR] [OUTPUTFILE]

    Without anything, pdfusion launches GUI

    OPTION
    -v show processing details
    -h show this help

    INPUTDIR 
    source directory, programm will merge pdf and images
    located in this directory

    OUTPUTFILE
    destination file, if not specified, result will be
    in INPUTDIR directory as result.pdf