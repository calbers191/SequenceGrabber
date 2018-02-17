import requests, sys, os, primer3
from splinter import Browser

#get -300/+300 bp on each side of variant based on its genomic coordinate position
def get_surrounding_sequence(chr, genomic_position, left_flanking=300, right_flanking=300):
    server = "https://rest.ensembl.org"
    ext = "/sequence/region/human/" + chr + ":" + str(int(genomic_position-left_flanking)) + ".." + str(int(genomic_position+right_flanking)) + "?coord_system_version=GRCh37"
    headers = {"Content-Type": "text/plain"}
    r = requests.get(server+ext, headers=headers)
    return r.text

#get exon id from gene name, exon number, and transcript id
def get_exon_id(gene, exon, transcript_id):
    server = "https://grch37.rest.ensembl.org"
    ext = "/lookup/symbol/human/" + gene + "?expand=1"
    headers = {"Content-Type": "application/json"}
    r = requests.get(server+ext, headers=headers)
    data = r.json()
    for item in data['Transcript']:
        if transcript_id is not None:
            if item['id'] == transcript_id:
                return item['Exon'][exon-1]['id']
        else:
            if item['is_canonical'] == 1:
                return item['Exon'][exon-1]['id']

#get sequence of feature by Ensembl ID
def get_sequence(sequence_id):
    server = "https://grch37.rest.ensembl.org"
    ext = "/sequence/id/" + sequence_id + "?"
    headers = {"Content-Type": "text/plain"}
    r = requests.get(server + ext, headers=headers)
    return r.text

def get_strand(gene):
    server = "https://grch37.rest.ensembl.org"
    ext = "/lookup/symbol/human/" + gene + "?expand=1"
    headers = {"Content-Type": "application/json"}
    r = requests.get(server + ext, headers=headers)
    data = r.json()
    return data['strand']

def reverse_complement(sequence):
    sequence = sequence[::-1]
    rev_seq = ""
    for base in sequence:
        base = base.lower()
        if base == "a":
            base = "T"
        elif base == "t":
            base = "A"
        elif base == "c":
            base = "G"
        elif base == "g":
            base = "C"
        rev_seq = rev_seq + base
    return rev_seq

def get_primers(sequence):
    primer3.setP3Globals(global_args={'PRIMER_PRODUCT_SIZE_RANGE': [301,450]})
    primer3out = primer3.bindings.designPrimers(seq_args={'SEQUENCE_TEMPLATE': sequence, 'SEQUENCE_TARGET': [151, 300]})
    return primer3out

class Primers(object):
    def __init__(self, sequence):
        self.sequence = sequence

        primer3.setP3Globals(global_args={'PRIMER_PRODUCT_SIZE_RANGE': [301, 450]})

        self.primer3out = primer3.bindings.designPrimers(seq_args={'SEQUENCE_TEMPLATE': self.sequence, 'SEQUENCE_TARGET': [151, 300]})

    def get_sequence(self, direction, primer_number):
        return self.primer3out['PRIMER_' + direction + '_' + str(primer_number) + '_SEQUENCE']

    def get_tm(self, direction, primer_number):
        return self.primer3out['PRIMER_' + direction + '_' + str(primer_number) + '_TM']

    def get_product_size(self, primer_number):
        return self.primer3out['PRIMER_PAIR_' + str(primer_number) + '_PRODUCT_SIZE']

    def get_gc_percent(self, direction, primer_number):
        return self.primer3out['PRIMER_' + direction + '_' + str(primer_number) + '_GC_PERCENT']

if __name__ == "__main__":

    sys.stderr = open('U:/primer_design/error.log', 'w')

    #parameters passed from VBA macro
    chr = sys.argv[1]
    genomic_position = int(sys.argv[2])
    gene = sys.argv[3]
    exon = int(sys.argv[4])
    transcript_id = sys.argv[5]
    copath_no = sys.argv[6]

    # chr = "10"
    # genomic_position = 63850973
    # gene = "ARID5B"
    # exon = 7
    # transcript_id = "ENST00000309334"
    # copath_no = "M17-test"

    #get exon id
    exon_id = get_exon_id(gene, exon, transcript_id)

    #make patient folder if it doesn't already exist
    if not os.path.exists(r"\\columbuschildrens.net\apps\ngs\samples\Exome Production Files\Sanger Confirmation\\" + copath_no):
        os.makedirs(r"\\columbuschildrens.net\apps\ngs\samples\Exome Production Files\Sanger Confirmation\\" + copath_no)

    #write exon sequence to txt file
    exon_txt = open(file=r"\\columbuschildrens.net\apps\ngs\samples\Exome Production Files\Sanger Confirmation\\" + copath_no + "\\" + gene + "_exon" + str(exon) + ".txt", mode="w")
    exon_txt.write(get_sequence(exon_id))
    exon_txt.close()

    #write genomic sequence to txt file
    genomic_txt = exon_txt = open(file=r"\\columbuschildrens.net\apps\ngs\samples\Exome Production Files\Sanger Confirmation\\" + copath_no + "\\" + gene + "_genomic.txt", mode="w")
    genomic_txt.write(get_sequence(transcript_id))
    genomic_txt.close()

    #write surrounding sequence to txt file
    surrounding_sequence = open(file=r"\\columbuschildrens.net\apps\ngs\samples\Exome Production Files\Sanger Confirmation\\" + copath_no + "\\" + gene + "_" + chr + "_" + str(genomic_position) + "_surrounding_seq.txt", mode="w")
    if get_strand(gene) == -1:
        surr_seq = reverse_complement(get_surrounding_sequence(chr, genomic_position))
    else:
        surr_seq = get_surrounding_sequence(chr, genomic_position)
    surrounding_sequence.write(surr_seq)
    surrounding_sequence.close()

    #write surrounding sequence to BED file
    surrounding_sequence_BED = open(file=r"\\columbuschildrens.net\apps\ngs\samples\Exome Production Files\Sanger Confirmation\\" + copath_no + "\\" + gene + "_" + chr + "_" + str(genomic_position) + "_surrounding_seq.bed", mode="w")
    surrounding_sequence_BED.write("chr" + chr + "\t" + str(genomic_position - 301) + "\t" + str(genomic_position + 300))
    surrounding_sequence_BED.close()

    #write sequences used to file
    sequence_ids_used = open(file=r"\\columbuschildrens.net\apps\ngs\samples\Exome Production Files\Sanger Confirmation\\" + copath_no + "\\" + "SEQUENCES_USED.txt", mode="a")
    sequence_ids_used.write(gene + "_genomic.txt: " + transcript_id + "\n\n" + gene + "_exon" + str(exon) + ".txt: " + exon_id + "\n\n" + gene + "_" + chr + "_" + str(genomic_position) + "_surrounding_seq.txt: Chr" + chr + ":" + str(genomic_position) + " -300/+300 bp on each side.\n\n")
    sequence_ids_used.close()

    #automatic primer design in primer3 using Splinter
    b = Browser('chrome')
    b.visit('http://bioinfo.ut.ee/primer3-0.4.0/')
    sequence_box = b.find_by_name('SEQUENCE')
    target_box = b.find_by_name('TARGET')
    pick_primers = b.find_by_name('Pick Primers')

    sequence = surr_seq
    parameters = '151, 300'

    sequence_box.fill(sequence)
    target_box.fill(parameters)
    pick_primers.click()