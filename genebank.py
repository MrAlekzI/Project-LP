'''
для работы необходим пакет biopython
при подключении по ID последовательности выдается объетк Bio.bio.seq из которго можно получить строку

примеры  ID :NM_018094, NM_001374734.1, NC_052532.1 (1 млн), CM021573.2 (170 млн - может долго грузить)
'''

from Bio import Entrez, SeqIO        

class DNALengthError(ValueError): #сделал ошибки чтобы при их возникновении веб быстрее их обрабатывал
    pass
class NonDNAError(TypeError):
    pass

class Nucleotide:
    def __init__(self,id_seq):
        self.id_seq = id_seq
        self.dna_description = id_parsing(self.id_seq) 
        self.length = int(self.dna_description[2])
        self.nuc_type = self.dna_description[4]
        if self.length <= 100000:
            self.sequence = genebank_querry(self.id_seq)
        else:
            raise DNALengthError (f'The lengh of the query:{id_seq} is longer than 100 kb!')

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

def id_parsing(id_seq:str) -> str:
    handle = Entrez.efetch(db="nucleotide", id=id_seq, rettype="gb", retmode="text") #хэндрел из другого типа описания, где содержится длин
    dna_description = handle.readline().split() #первая строка опсиания гена из базы данных Gene bank где через знаки табуляции тип гена, id, длина, тип полимера, топология, дата обновления
    return dna_description

def genebank_querry(id_seq:str) -> str:
    #gb_handle = id_parsing(id_seq) #парсим и cсоздаем первый хэндл с описанием гена
    #dna_obj = Nucleotide(id_seq, None)
    #if dna_obj.validation():
    handle = Entrez.efetch(db="nucleotide", id=id_seq, rettype="fasta", retmode='text') #создается хэндлей который уже содержит информацию о последвоательности и с нип проводятся дальнейшие манипуляции
    record = SeqIO.read(handle, 'fasta')
    return str(record.seq)
        
    

if __name__ == '__main__':
    id = input()
    dna_query = Nucleotide(id)
    print(dna_query.sequence)
    print(dna_query.type_check())