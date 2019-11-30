#! /usr/bin/python3
""" @title COUCOU PDFUSION"""
import os
import sys
from PyPDF2 import PdfFileMerger
import img2pdf
from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

imgExtensions = ['png', 'jpg', 'jpeg']

def merge(outfile, pdfsTab):
    ## Merge PDF files
    # outfile : output file path
    # pdfsTab : array of PDF filenames
    merger = PdfFileMerger()
    for pdf in pdfsTab:
        merger.append(open(pdf, 'rb'))
    if os.path.exists(outfile):
        os.remove(outfile)
    with open(outfile, 'wb') as fout:
        merger.write(fout)
    merger.close()

def imgToPdf(imagePath):
    ## Convert an image to pfd
    # imagePath : path of the image
    pdf_path = imagePath+".pdf"# storing pdf path
    image = Image.open(imagePath)# opening image
    pdf_bytes = img2pdf.convert(image.filename)# converting into chunks using img2pdf
    file = open(pdf_path, "wb")# opening or creating pdf file
    file.write(pdf_bytes)# writing pdf files with chunks
    image.close()# closing image file
    file.close()# closing pdf file
    return pdf_path

def getFilesFromFolder(folderPath):
    # Return array containing images and pdf paths contained
    # in given directorypdfs = []
    pdfs=[]
    for filename in os.listdir(folderPath):
        ext = filename.split('.')[-1].lower()
        if ext == 'pdf':
            pdfs.append(folderPath+filename)
        elif ext in imgExtensions:
            pdf = imgToPdf(folderPath+filename)
            pdfs.append(pdf)
    return pdfs



# Main Qt Window GUI
class MainQtWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 150, 500, 200)
        self.setWindowTitle('PDFusion')
        self.setWindowIcon(QIcon('logo.png'))

        mainLayout = QVBoxLayout()

        line = QHBoxLayout()
        label = QLabel('Dossier:')
        self.tf = QLineEdit()
        self.tf.setDisabled(True)
        bouton = QPushButton("Parcourir...")
        bouton.clicked.connect(self.getfile)
        line.addWidget(label)
        line.addWidget(self.tf)
        line.addWidget(bouton)
        mainLayout.addLayout(line)

        line = QHBoxLayout()
        bouton = QPushButton("Fusionner")
        bouton.clicked.connect(self.process)
        line.addWidget(bouton)
        mainLayout.addLayout(line)

        self.setLayout(mainLayout)
        self.show()

    def getfile(self):
        d = QFileDialog()
        d.setFileMode(QFileDialog.Directory)
        d.setOption(QFileDialog.ShowDirsOnly, False)
        #d.setOption(QFileDialog.DontUseNativeDialog, True)
        d.exec()
        self.tf.setText(d.selectedFiles()[0]+'/')

    def process(self):
        path = self.tf.text()
        files = getFilesFromFolder(path)
        merge(path, files)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        app = QApplication(sys.argv)
        ex = MainQtWindow()
        sys.exit(app.exec_())
    else:
        if '-h' in sys.argv:
            print('''Usage:
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
    ''')
            exit()
        verbose = False
        if '-v' in sys.argv:
            verbose = True
            sys.argv.remove('-v')
        if len(sys.argv) > 3:        
            print('Bad usage, use: pdfusion -h')
            exit()

        input_path = sys.argv[1]
        input_path += '/' if input_path[-1] != '/' else ''
        if verbose: print('Merging directory :', input_path)
        output_file = input_path+'result.pdf'
        if len(sys.argv) == 3:
            output_file = sys.argv[2]
        if verbose: print('Into :', output_file)
        
        files = getFilesFromFolder(input_path)
        merge(output_file, files)
        if verbose: print('Accomplished!')