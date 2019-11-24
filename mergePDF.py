import os
import sys
from PyPDF2 import PdfFileMerger
import img2pdf
from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

imgExtensions = ['png', 'jpg', 'jpeg']
# Merge PDF files
# pdfsTab : array of PDF filenames
def merge(path, pdfsTab):
    print(path)
    merger = PdfFileMerger()
    for pdf in pdfsTab:
        merger.append(open(pdf, 'rb'))
    with open(path+'result.pdf', 'wb') as fout:
        merger.write(fout)
    merger.close()

# Convert an image to pfd
# given image path
def imgToPdf(imagePath):
    pdf_path = imagePath+".pdf"# storing pdf path
    image = Image.open(imagePath)# opening image
    pdf_bytes = img2pdf.convert(image.filename)# converting into chunks using img2pdf
    file = open(pdf_path, "wb")# opening or creating pdf file
    file.write(pdf_bytes)# writing pdf files with chunks
    image.close()# closing image file
    file.close()# closing pdf file
    return pdf_path

def getFilesFromFolder(folderPath):
    pdfs = []
    for filename in os.listdir(folderPath):
        ext = filename.split('.')[-1].lower()
        if ext == 'pdf':
            pdfs.append(folderPath+filename)
        elif ext in imgExtensions:
            pdf = imgToPdf(folderPath+filename)
            pdfs.append(pdf)
    return pdfs



class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(1300, 300, 700, 500)
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
        bouton = QPushButton("Rechercher")
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
        print(files)
        merge(path, files)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
