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

        gene1Label = QLabel("5' Fusion Partner:")
        self.gene1Line = QLineEdit()
        transcript1Label = QLabel("Transcript ID:")
        self.transcript1Line = QLineEdit()
        exon1Label = QLabel("Exon:")
        self.exon1Line = QLineEdit()
        gene2Label = QLabel("3' Fusion Partner:")
        self.gene2Line = QLineEdit()
        transcript2Label = QLabel("Transcript ID:")
        self.transcript2Line = QLineEdit()
        exon2Label = QLabel("Exon:")
        self.exon2Line = QLineEdit()
        self.submitButton = QPushButton("&Submit")

        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(gene1Label)
        buttonLayout1.addWidget(self.gene1Line)
        buttonLayout1.addWidget(transcript1Label)
        buttonLayout1.addWidget(self.transcript1Line)
        buttonLayout1.addWidget(exon1Label)
        buttonLayout1.addWidget(self.exon1Line)
        buttonLayout1.addWidget(gene2Label)
        buttonLayout1.addWidget(self.gene2Line)
        buttonLayout1.addWidget(transcript2Label)
        buttonLayout1.addWidget(self.transcript2Line)
        buttonLayout1.addWidget(exon2Label)
        buttonLayout1.addWidget(self.exon2Line)
        buttonLayout1.addWidget(self.submitButton)

        self.setLayout(buttonLayout1)
        self.setWindowTitle("Enter Fusion Partners")

        self.submitButton.clicked.connect(self.submitFusionPartners)

    def submitFusionPartners(self):
        gene1 = self.gene1Line.text()
        exon1 = self.exon1Line.text()
        gene2 = self.gene2Line.text()
        exon2 = self.exon2Line.text()

        if self.transcript1Line.text() == "":
            transcript1 = None
        else:
            transcript1 = self.transcript1Line.text()
        if self.transcript2Line.text() == "":
            transcript2 = None
        else:
            transcript2 = self.transcript2Line.text()

        exon1ID = get_exon_id(gene1, int(exon1), transcript1)
        exon2ID = get_exon_id(gene2, int(exon2), transcript2)

        exon1seq = get_sequence(exon1ID)
        exon2seq = get_sequence(exon2ID)

        # Set filepath for sequence files
        filepath = os.getcwd() + '\sequences\\'

        # If path doesn't exist yet, create directory
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        # Name file by chromosome and coordinate
        filename = gene1 + '_ex' + exon1 + '_' + gene2 + '_ex' + exon2 + '.txt'

        # Open and write to sequence file, close file
        sequenceFile = open(filepath + filename, 'w')
        sequenceFile.write(exon1seq + exon2seq)
        sequenceFile.close()

        # Success message box
        QMessageBox.information(self, "Success!", "Sequence written to " + filepath)

        # Clear all fields
        self.gene1Line.clear()
        self.transcript1Line.clear()
        self.exon1Line.clear()
        self.gene2Line.clear()
        self.transcript2Line.clear()
        self.exon2Line.clear()


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