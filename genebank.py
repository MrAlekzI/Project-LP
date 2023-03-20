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

class Nucleotide:
    def __init__(self, id_seq, length, nuc_type, sequence):
        self.id_seq = id_seq
        self.length = length
        self.nuc_type = nuc_type
        self.sequence = sequence

    def __repr__(self):
        return f'The query contains {self.nuc_type} with length {self.length}'
    
    def validation(self):
        if self.length <= 100000:
            return True
        
    def type_check(self):
        #чтобы сообщить что введена последовательноть РНК, это не критично но иногда следует знать это
        if self.nuc_type.find('RNA') != -1: #могут быть записаны RNA, mRNA, rRNA, tRNA поэтому ищем общее
            raise NonDNAError (f'AttentionThe query: {self.id_seq} contains RNA sequence')

Entrez.email = 'somemailsomemail@gmail.cpm' #необходим любой email чтобы больше запросов длеать

def id_parsing(id_seq:str) -> object:
    
    handle = Entrez.efetch(db="nucleotide", id=id_seq, rettype="gb", retmode="text") #хэндрел из другого типа описания, где содержится длин
    dna_decription = handle.readline().split() #первая строка опсиания гена из базы данных Gene bank где через знаки табуляции тип гена, id, длина, тип полимера, топология, дата обновления 
    length= int(dna_decription[2])
    nucleotide_type = dna_decription[4]
    nucl_query = Nucleotide(id_seq, length, nucleotide_type, None)
    return nucl_query

def genebank_querry(id_seq:str) -> str:
    dna_obj = id_parsing(id_seq) #gпарсим и создаем объект
    if dna_obj.validation():
        handle = Entrez.efetch(db="nucleotide", id=id_seq, rettype="fasta", retmode='text') #создается хэндлей и с нип проводятся дальнейшие манипуляции
        record = SeqIO.read(handle, 'fasta')
        sequence = str(record.seq)
        dna_obj.sequence = sequence #дописываем в объект атрибут
        return dna_obj 
    else:
        raise DNALengthError (f'The lengh of the query:{dna_obj.id_seqid_seq} is longer than 100 kb!')
    

if __name__ == '__main__':
    id = input()
    print(genebank_querry(id).sequence)
    print(genebank_querry(id).type_check())