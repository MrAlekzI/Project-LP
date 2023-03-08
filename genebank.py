'''
для работы необходим пакет biopython
при подключении по ID последовательности выдается объетк Bio.bio.seq из которго можно получить строку

примеры  ID :NM_018094, M_001374734.1, NC_052532.1 (1 млн), CM021573.2 (170 млн - может долго грузить)
'''

from Bio import Entrez, SeqIO

Entrez.email = 'somemailsomemail@gmail.cpm' #необходим любой email чтобы больше запросов длеать

def genebank_querry(ID:int) -> str:
    handle = Entrez.efetch(db="nucleotide", id=f"{ID}", rettype="fasta", retmode='text') #создается хэндлей и с нип проводятся дальнейшие манипуляции
    record = SeqIO.read(handle, 'fasta')
    sequence = str(record.seq)
    return sequence

if __name__ == '__main__':
    ID = input()
    print(genebank_querry(ID))