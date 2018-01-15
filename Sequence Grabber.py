#!/usr/bin/env python

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtGui
import os

from primer_design import get_surrounding_sequence

class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        chromLabel = QLabel("Chromosome:")
        self.chromLine = QLineEdit()

        coordLabel = QLabel("Genomic coordinate:")
        self.coordLine = QLineEdit()

        self.submitButton = QPushButton("&Submit")

        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(chromLabel)
        buttonLayout1.addWidget(self.chromLine)
        buttonLayout1.addWidget(coordLabel)
        buttonLayout1.addWidget(self.coordLine)
        buttonLayout1.addWidget(self.submitButton)

        self.submitButton.clicked.connect(self.submitCoordinates)

        mainLayout = QGridLayout()
        mainLayout.addLayout(buttonLayout1, 0, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Sequence Grabber")

    def submitCoordinates(self):

        chrom = self.chromLine.text()
        coord = self.coordLine.text()

        # If either field is left blank, display error message
        if chrom == "" or coord == "":
            QMessageBox.information(self, "Error: Empty Field", "Please fill in all fields.")
        # Else get sequence
        else:
            # Get surrounding sequence +/- 300bp
            sequence = get_surrounding_sequence(chrom, int(coord))

            # Set filepath for sequence files
            filepath = os.getcwd() + '\sequences\\'

            # If path doesn't exist yet, create directory
            if not os.path.exists(filepath):
                os.makedirs(filepath)

            # Name file by chromosome and coordinate
            filename = chrom + '_' + coord + '.txt'

            # Open and write to sequence file, close file
            sequenceFile = open(filepath + filename, 'w')
            sequenceFile.write(sequence)
            sequenceFile.close()

            # Success message box
            QMessageBox.information(self, "Success!", "Sequence written to " + filepath)

            # Clear all fields
            self.chromLine.clear()
            self.coordLine.clear()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = Form()
    screen.show()

    sys.exit(app.exec_())