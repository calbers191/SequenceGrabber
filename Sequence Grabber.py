from PyQt5.QtWidgets import *
import xlsxwriter


from primer_design import *

class mainMenu(QWidget):
    def __init__(self, parent=None):
        super(mainMenu, self).__init__(parent)

        self.getSeqByCoordButton = QPushButton("Get Sequence by Genomic Coordinate")

        self.getFusionSequenceButton = QPushButton("Get Fusion Sequence")

        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(QLabel("What would you like to do?"), 1)
        buttonLayout1.addWidget(self.getSeqByCoordButton, 2)
        #buttonLayout1.addWidget(self.getFusionSequenceButton, 3)

        self.getSeqByCoordButton.clicked.connect(self.getSeqByCoord)
        self.getFusionSequenceButton.clicked.connect(self.getFusionSequence)

        self.setLayout(buttonLayout1)
        self.setWindowTitle("Sequence Grabber")

    def getSeqByCoord(self):
        form = getSeqByCoordForm()
        form.exec_()

    def getFusionSequence(self):
        form = getFusionSequenceForm()
        form.exec_()

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
            filename = chrom + '_' + coord + '_primer_report.xlsx'

            # Run Primer3 with surrounding sequence
            primers = Primers(sequence)

            # Open and format Excel workbook
            workbook = xlsxwriter.Workbook(filepath + filename)
            worksheet = workbook.add_worksheet('Primer Report')
            worksheet2 = workbook.add_worksheet('Query Sequence')
            bold = workbook.add_format({'bold': True})
            align_right = workbook.add_format()
            align_right.set_align('right')

            # Write primer report to Sheet 1
            j = 0
            for i in range(0, 5):
                worksheet.set_column(0, 0, 14)
                worksheet.set_column(1, 1, 30)
                worksheet.set_column(2, 2, 14)
                worksheet.set_column(3, 3, 30)
                worksheet.set_column(4, 4, 14)

                worksheet.write(i+j, 0, 'Left Primer ' + str(i+1), bold)
                worksheet.write(i+j, 1, primers.get_sequence('LEFT', i), align_right)
                worksheet.write(i+1+j, 0, 'Length', bold)
                worksheet.write(i+1+j, 1, len(primers.get_sequence('LEFT', i)))
                worksheet.write(i+2+j, 0, 'TM', bold)
                worksheet.write(i+2+j, 1, primers.get_tm('LEFT', i))
                worksheet.write(i+3+j, 0, 'GC percent', bold)
                worksheet.write(i+3+j, 1, primers.get_gc_percent('LEFT', i))

                worksheet.write(i+j, 2, 'Right Primer ' + str(i + 1), bold)
                worksheet.write(i+j, 3, primers.get_sequence('RIGHT', i), align_right)
                worksheet.write(i+1+j, 2, 'Length', bold)
                worksheet.write(i+1+j, 3, len(primers.get_sequence('RIGHT', i)))
                worksheet.write(i+2+j, 2, 'TM', bold)
                worksheet.write(i+2+j, 3, primers.get_tm('RIGHT', i))
                worksheet.write(i+3+j, 2, 'GC percent', bold)
                worksheet.write(i+3+j, 3, primers.get_gc_percent('RIGHT', i))

                worksheet.write(i+j, 4, 'Product Size', bold)
                worksheet.write(i+j, 5, primers.get_product_size(i))

                j += 4

            # Write query sequence to Sheet 2
            worksheet2.write(0, 0, sequence)

            # Success message box
            QMessageBox.information(self, "Success!",
                                    "Primer report written to " + filepath)

            # Clear all fields
            self.chromLine.clear()
            self.coordLine.clear()

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    mainmenu = mainMenu()
    mainmenu.show()

    sys.exit(app.exec_())