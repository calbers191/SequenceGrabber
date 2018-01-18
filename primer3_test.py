import primer3, primer_design

sequence = primer_design.get_surrounding_sequence('1', 123123)

def get_primers(sequence):
    primer3.setP3Globals(global_args={'PRIMER_PRODUCT_SIZE_RANGE': [301,450]})

    primer3out = primer3.bindings.designPrimers(seq_args={'SEQUENCE_TEMPLATE': sequence, 'SEQUENCE_TARGET': [151, 300]})

    primers = {}

    primers['left_primer_0'] = primer3out['PRIMER_LEFT_0_SEQUENCE']
    primers['left_primer_1'] = primer3out['PRIMER_LEFT_1_SEQUENCE']
    primers['left_primer_2'] = primer3out['PRIMER_LEFT_2_SEQUENCE']
    primers['left_primer_3'] = primer3out['PRIMER_LEFT_3_SEQUENCE']
    primers['left_primer_4'] = primer3out['PRIMER_LEFT_4_SEQUENCE']
    primers['right_primer_0'] = primer3out['PRIMER_RIGHT_0_SEQUENCE']
    primers['right_primer_1'] = primer3out['PRIMER_RIGHT_1_SEQUENCE']
    primers['right_primer_2'] = primer3out['PRIMER_RIGHT_2_SEQUENCE']
    primers['right_primer_3'] = primer3out['PRIMER_RIGHT_3_SEQUENCE']
    primers['right_primer_4'] = primer3out['PRIMER_RIGHT_4_SEQUENCE']
    primers['product_size_0'] = primer3out['PRIMER_PAIR_0_PRODUCT_SIZE']
    primers['product_size_1'] = primer3out['PRIMER_PAIR_1_PRODUCT_SIZE']
    primers['product_size_2'] = primer3out['PRIMER_PAIR_2_PRODUCT_SIZE']
    primers['product_size_3'] = primer3out['PRIMER_PAIR_3_PRODUCT_SIZE']
    primers['product_size_4'] = primer3out['PRIMER_PAIR_4_PRODUCT_SIZE']

    return primers

# print(left_primer_0, right_primer_0)
# print(left_primer_1, right_primer_1)
# print(left_primer_2, right_primer_2)
# print(left_primer_3, right_primer_3)
# print(left_primer_4, right_primer_4)
#
#
# for key, value in primers.items():
#     print(key, value)
#
