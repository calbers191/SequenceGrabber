import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtGui
import os

from primer_design import get_surrounding_sequence, get_exon_id, get_sequence

class mainMenu(QWidget):
    def __init__(self, parent=None):
        super(mainMenu, self).__init__(parent)

        self.getSeqByCoordButton = QPushButton("Get Sequence by Genomic Coordinate")

        self.getFusionSequenceButton = QPushButton("Get Fusion Sequence")

        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(QLabel("What would you like to do?"), 1)
        buttonLayout1.addWidget(self.getSeqByCoordButton, 2)
        buttonLayout1.addWidget(self.getFusionSequenceButton, 3)

        self.getSeqByCoordButton.clicked.connect(self.getSeqByCoord)
        self.getFusionSequenceButton.clicked.connect(self.getFusionSequence)

        self.setLayout(buttonLayout1)
        self.setWindowTitle("Sequence Grabber")

    def getSeqByCoord(self):
        form = getSeqByCoordForm()
        form.exec()

    def getFusionSequence(self):
        form = getFusionSequenceForm()
        form.exec()

class getFusionSequenceForm(QDialog):
    def __init__(self, parent=None):
        super(getFusionSequenceForm, self).__init__(parent)

        p1Label = QLabel("5' Fusion Partner:")
        self.p1Line = QLineEdit()

        e1Label = QLabel("Exon:")
        self.e1Line = QLineEdit()

        p2Label = QLabel("3' Fusion Partner:")
        self.p2Line = QLineEdit()

        e2Label = QLabel("Exon:")
        self.e2Line = QLineEdit()

        self.submitButton = QPushButton("&Submit")

        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(p1Label)
        buttonLayout1.addWidget(self.p1Line)
        buttonLayout1.addWidget(e1Label)
        buttonLayout1.addWidget(self.e1Line)
        buttonLayout1.addWidget(p2Label)
        buttonLayout1.addWidget(self.p2Line)
        buttonLayout1.addWidget(e2Label)
        buttonLayout1.addWidget(self.e2Line)
        buttonLayout1.addWidget(self.submitButton)

        self.setLayout(buttonLayout1)
        self.setWindowTitle("Enter Fusion Partners")

        self.submitButton.clicked.connect(self.submitFusionPartners)

    def submitFusionPartners(self):
        pass

class getSeqByCoordForm(QDialog):
    def __init__(self, parent=None):
        super(getSeqByCoordForm, self).__init__(parent)

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

        self.setLayout(buttonLayout1)
        self.setWindowTitle("Enter Genomic Coordinate")

        self.submitButton.clicked.connect(self.submitCoordinate)

    def submitCoordinate(self):

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

    mainmenu = mainMenu()
    mainmenu.show()

    sys.exit(app.exec_())