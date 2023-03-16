'''
для работы необходим пакет biopython
при подключении по ID последовательности выдается объетк Bio.bio.seq из которго можно получить строку

примеры  ID :NM_018094, M_001374734.1, NC_052532.1 (1 млн), CM021573.2 (170 млн - может долго грузить)
'''

from Bio import Entrez, SeqIO

class DNALengthError(ValueError): #сделал ошибки чтобы при их возникновении веб быстрее их обрабатывал
    pass
class NonDNAError(TypeError):
    pass


Entrez.email = 'somemailsomemail@gmail.cpm' #необходим любой email чтобы больше запросов длеать

def validation(ID:str) -> dict:
    
    handle = Entrez.efetch(db="nucleotide", id=f'{ID}', rettype="gb", retmode="text") #хэндрел из другого типа описания, где содержится длин
    dna_decription = handle.readline().split()
    length= int(dna_decription[2])
    nucleotide_type = dna_decription[4]
    query = {'ID':ID, 'length':length, 'nucl_type':nucleotide_type}
    return query

def genebank_querry(ID:str) -> str:
    handle = Entrez.efetch(db="nucleotide", id=f"{ID}", rettype="fasta", retmode='text') #создается хэндлей и с нип проводятся дальнейшие манипуляции
    if validation(ID)['length'] <= 100000:
        record = SeqIO.read(handle, 'fasta')
        sequence = str(record.seq)
        return sequence
    else:
        raise DNALengthError (f'The lengh of the query:{ID} is longer than 100 kb!')
    
def isRNA(ID): #чтобы сообщить что введена последовательноть РНК, это не критично но иногда следует знать это
    if validation(ID)['nucl_type'].find('RNA') != -1: #могут быть записаны RNA, mRNA, rRNA, tRNA поэтому ищем общее
        raise NonDNAError (f'AttentionThe query: {ID} contains RNA sequence')

if __name__ == '__main__':
    ID = input()
    print(genebank_querry(ID))
    print(isRNA(ID))