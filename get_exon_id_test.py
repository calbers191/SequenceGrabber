import requests

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

print(get_exon_id("ABL1", 2, None))

print(get_exon_id("ABL1", 2, "ENST00000393293"))
