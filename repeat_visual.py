from tkinter import *
from tkinter import messagebox
import random
import string
import json


dna_symbol = "atgc" #перечень допустимых символов для ДНК
protein_symbol = "acdefghiklmnopqrstvuwy" #перечень допустимых символов для белка. 

#создание рандомной последовательности
def random_seq ():
	rand_seq = ""
	seq_template = ""
	size = random.randint(100,1000)
	if seq_var.get() == 0:
		seq_template = dna_symbol
	if seq_var.get() == 1:
		seq_template = protein_symbol
	rand_seq = rand_seq.join(random.choice (seq_template) for _ in range (size))
	return rand_seq


#форматирование полученой последовательности, чтобы унифицировать строку и удалить некоректные символы
def format_seq (seq):
	seq = seq.lower()
	seq_list = list (seq)
	counter = 0  #счетчик произведеных замен
	seq_format = []
	if seq_var.get() == 0:
		for sybmol in seq_list:
			if sybmol in list(dna_symbol):
				seq_format.append (sybmol)
			else:
				counter +=1
	if seq_var.get() == 1:
		for sybmol in seq_list:
			if sybmol in list(protein_symbol):
				seq_format.append (sybmol)
			else:
				counter +=1
				
	if counter >2: # 2 потому что знак переноса строки всегда учитывается - не знаю как с ним справиться
			messagebox.showwarning("Warning!", "{} unavailable symbols were deleted".format(counter) )
	if counter == 2:
			messagebox.showwarning ("Warning!", " One unavailable symbol was deleted")
	return "".join(seq_format)

#"дробление списка исходя из длины повтора 
def fold (seq, n_fold): #функция разбивает последовательность на несколько со сдвигом первого элемента а 1 вправо, при этом нформирующиеся последовательности содержат в n_fold раз меньше лементов
	seq_new = list (seq)
	seq_new.remove("\n")
	seq_temporary = [] 
	for j in range (0,n_fold):
		seq_temporary_2 = [] #список для конкретного сдвига последовательности
		for i in range (j, len(seq_new),n_fold):
			if i+j <= len(seq_new):	#при таком условии длина последних элементов может быть меньше длины остальных, что оприори делает их не идентичными при последующем поиске
				#сначала я хотел, чтобы таких неполных элеметов вообще не было в результирующем списке (это съэкономит ресуры), но так и не смог придумать условие  чтобы реальзовать 
				#такой алгоритм
				new_item=""
				new_item = new_item.join(seq_new [i:i+n_fold])
				seq_temporary_2.append(new_item)
		seq_temporary.append(seq_temporary_2)
	return seq_temporary # возвращает список, с элеметнами-списками новых последовательностей полученых фреймшифтом, 
#где элементы уже не один символ - а строка равная длине повтора

def dict_poly_repeat (letter, first_index, last_index, number_of_repeats, frameshift, n_fold):
        repeats = []
        for i in range (number_of_repeats):
                d = {"Type":None, "unit lengh":0,  "start index":0, "end index":0, "lengh total":0, "number of units in the tract":0, "frameshift": 0}
                d["Type"] = letter[i]
                d["unit lengh"] = n_fold
                start = (first_index[i]*n_fold)+frameshift	#пересчет индекса первого символа в этом тракте в первоначальной последовательности
                d["start index"] = start
                end = ((last_index[i]+1)*n_fold-1)+frameshift #пересчет индекса последнего символа в этом тракте в изначальной последовательности
                d["end index"] = end
                d["lengh total"] = (end - start)+1
                d["number of units in the tract"] = ((end - start)+1)//n_fold
                d["frameshift"] = frameshift
                repeats.append(d)  #список с последовательным описанием каждого повтора в пределах одной рамки             
        return repeats

def poly_repeat(folded_seq, n_fold): #находит тип тракта, начало и конец каждого тракта
	frameshift = -1
	repeat_list =[]
	for fr_list in folded_seq: 
		frameshift +=1
		letter = []
		first_index = []
		last_index = []
		number_of_repeats = 0
		if fr_list[0] == fr_list[1]:   #проверка начального элемента                             
				first_index.append(0)
		for i in range(1, len(fr_list)-1):                    
			if fr_list[i]== fr_list [i+1] and fr_list [i] != fr_list [i-1]:
				first_index.append(i)

			if fr_list [i] == fr_list [i-1] and fr_list [i]!=fr_list [i+1]:
				last_index.append(i)
				letter.append(fr_list [i])
				number_of_repeats+=1
	

		if fr_list [-1] == fr_list [-2]:          #проверка конечного элемента
			letter.append(fr_list [-1])
			last_index.append (len(fr_list)-1)
			number_of_repeats += 1
		a = [letter,first_index, last_index, number_of_repeats, frameshift, n_fold]
		dict_n = dict_poly_repeat (*a)
		repeat_list.extend(dict_n)
	return repeat_list #формируем список, где для каждого сдвига считывания есть список с найдеными повторяющимимся элементами

#сортировка списка по начальному индексу повтора. 
def sorting (repeat_list, begin):
		min_index = begin
		current_min = repeat_list[begin]
		for i in range (begin, len(repeat_list)):
			if repeat_list[i]["start index"] < current_min["start index"]:
				min_index = i
				current_min = repeat_list[i]
		return min_index
def sorting_2 (repeat_list,i,j):
	t = repeat_list[i]
	repeat_list[i] = repeat_list [j]
	repeat_list[j] = t

def sorting_3 (repeat_list):
	for begin in range (len(repeat_list)): 
		i = sorting(repeat_list,begin)
		sorting_2(repeat_list, begin, i)
	return repeat_list
	

#Удаление "вложеных повторов"(что бы в abcabcabc не выводились bca и сab).
#как рекализовать это внутри других циклов я так и не придумал

def sec_rep_del (repeat_list):
	repeat_list.reverse()
	for i in range (len(repeat_list)-1):
		if (repeat_list[i]["start index"] - repeat_list[i+1]["start index"]) == 1:
			repeat_list[i] = 0
	repeat_list.reverse()
	repeat_list_short = list(filter(lambda x: x != 0, repeat_list))
	return repeat_list_short


def show_results():
	results = Tk()
	results.title ("Found repeats")
	results. minsize (600,500)

	text_results = Text (results, wrap = WORD)
	text_results.pack(expand = 1, fill = BOTH)
	text_results.insert(1.0,  rep_1)
	vscroll = Scrollbar (text_results, orient = "vert", command = text_results.yview)
	text_results ["yscrollcommand"] = vscroll.set
	vscroll.pack(side = RIGHT, fill = Y)

def show_types(): #выводит список типов повторов
	results = Tk()
	results.title ("Types of repeats")
	results. minsize (600,500)
	text_types = Text (results, wrap = WORD)
	text_types.pack(expand = 1, fill = BOTH)
	types_str = ""
	for i in range(len(type_list)):			#формируется строка с нумерацией и в столбик
		n = str(i+1)
		t = "{}. {} \n".format (n, type_list[i])
		types_str +=t
	text_types.insert(1.0, types_str)
	vscroll = Scrollbar (text_types, orient = "vert", command = text_types.yview)
	text_types ["yscrollcommand"] = vscroll.set
	vscroll.pack(side = RIGHT, fill = Y)

def show_in_querry (): #выводит исходную последовательность и выделяет повторы
	seq = text_querry.get(1.0,END)  #берем последовательность из окна ввода
	n = int(rep_entry.get())
	results_in_querry = Tk()
	results_in_querry.title ("Found repeats")
	results_in_querry. minsize (600,500)
	text_results_in_querry = Text (results_in_querry)
	text_results_in_querry.pack(expand = 1, fill = BOTH)
	text_results_in_querry.insert(1.0, seq )
	start = int (rep_1[n]["start index"])
	end = int(rep_1[n]["end index"])
	#text_results_in_querry.tag_add("repeat_track", 1.start, 1.end)  #здесь не хочет воспринимать индексы
	text_results_in_querry.tag_config("repeat_track", background = "yellow"  )
	vscroll = Scrollbar (text_results_in_querry, orient = "vert", command = text_results_in_querry.yview)
	text_results_in_querry ["yscrollcommand"] = vscroll.set
	vscroll.pack(side = RIGHT, fill = Y)

def rep_analysis (repeat_list): #находит типы повторов и записывает их в  список
	global type_list
	type_list = []
	for repeat in repeat_list:
		if repeat ["Type"] not in  type_list:
			type_list.append(repeat ["Type"])
	print (type_list) # список типов в командном окне
	return type_list

def click_1 ():
		text_querry.delete(1.0, END)
		text_querry.insert (1.0, random_seq ())
		
def click_2 (): #очистка полей
		text_querry.delete(1.0, END)
		label_3.config(text = "Lengh: ")
		label_4.config(text = "Enter lengh of a pereat (max is ) :")
		label_5.config(text = "Overall repeats: ")
		label_6.config(text = "Repeats types: ")

def click_3 ():
		seq = text_querry.get(1.0,END)
		text_querry.delete(1.0, END)
		text_querry.insert(1.0, format_seq(seq))
		seq_len = len(format_seq(seq))
		label_3.config(text = "Lengh: "+str(seq_len))
		label_4.config(text = "Enter lengh of a pereat (max is {}) :".format(seq_len//2)) 
		



def click_4 ():
		global rep_1 #пытаюсь записать результат поиска как переменную чтобы дальнейшие для дальнейших действий не проводить поиск заново. Но не получается
		
		rep_1 = []
		seq = text_querry.get(1.0,END) 
		n = int(lengh_entry.get())
		if n > (len(seq)-1)//2:			#единица вычитается, т.к. я не могу избавиться от знака переноса строки
			messagebox.showwarning ("Warning", "The repeat is too long!")
		else:
			seq_fold = fold(seq, n)
			seq_fold_search = poly_repeat(seq_fold,n)
			seq_fold_sorting = sorting_3 (seq_fold_search)
			if var_seq_short.get() == 1:
				repeats_1 = sec_rep_del (seq_fold_sorting) #по умолчанию пусть выводит облегченую версию списка повторов
			else:
				repeats_1 = seq_fold_sorting

		#print (repeats_1) #вывод в командном окне
		rep_1 = repeats_1
		l = len(rep_1)
		types = rep_analysis(rep_1) #типы повторов
		l_types = len(types)

		label_5.config(text = "Overall repeats: {}".format(l))
		label_6.config(text = "Repeats types: {}".format (l_types))
		return repeats_1	


def save_repeats ():
	file = open ("repeats.json","w")
	json.dump(rep_1, file)
	file.close()

def click_5 ():
	show_results()

def click_6 ():
	rep_text.delete(1.0, END)
	n = int(rep_entry.get())
	t = rep_1[n-1]["Type"]
	rep_text.insert(1.0, t)
	index = type_list.index(t)+1  #ищет номер типа в списке типов
	start = rep_1[n-1]["start index"]+1 #+1 в последовательностях ДНК и белков счет с 1
	end = rep_1[n-1]["end index"]+1
	label_9.config(text = "Type: {}".format(index))
	label_10.config(text = "Position from {} to {}".format(start, end))

def click_7 ():
	rep_text_2.delete(1.0,END)
	n = int(type_entry_2.get())
	t = type_list[n-1]
	rep_text_2.insert(1.0, t)
	i = 0						#счетчик количества повторов данного типа
	for repeat in rep_1:
		if repeat["Type"] == t:
			i+=1
	label_13.config(text = "Quantity in the querry: {}".format(i))

def click_8 ():
	show_in_querry()

	


root = Tk()
root.title ("Searching of repeats")
root. geometry ("750x450")

querry_frame = LabelFrame(root,  text ="Querry", font = 14)
querry_frame.place ({"x":10, "y":10, "height":430, "width": 420 })

label_1 = Label(querry_frame)
label_1 ["text"] = "Choose type of sequence: "
label_1 .place ({"x":5, "y":0})

seq_var = BooleanVar ()
seq_var.set(0)
rbutton_DNA = Radiobutton(querry_frame,text = "DNA/RNA", variable = seq_var, value = 0) 
rbutton_protein = Radiobutton(querry_frame,text = "Protein", variable = seq_var, value = 1) 
rbutton_DNA.place({"x":150, "y":0})
rbutton_protein.place({"x":250, "y":0})

label_2 = Label (querry_frame)
label_2 ["text"] = "Enter sequence:"
label_2.place ({"x":5, "y":30})

button_random = Button(querry_frame)
button_random ["text"] = "Random generate"
button_random ["command"] = click_1
button_random.place({"x":300, "y":25})

text_querry = Text (querry_frame)
text_querry.place ({"x":5, "y":55, "height":240, "width": 390})

vscroll = Scrollbar (querry_frame, orient = "vert", command = text_querry.yview)
text_querry ["yscrollcommand"] = vscroll.set
vscroll.place({"x":395, "y":55, "height":240})



label_3 = Label(querry_frame)
label_3 ["text"] = "Lengh: "
label_3.place({"x":5, "y":320})

button_clear = Button(querry_frame)
button_clear ["text"] = "Clear"
button_clear ["command"] = click_2
button_clear.place({"x":350, "y":320, "width": 50})

button_format = Button (querry_frame)
button_format ["text"] = "Format"
button_format ["command"] = click_3
button_format.place ({"x":250, "y":320, "width": 50})



label_4 = Label (querry_frame)
label_4 ["text"] = "Enter lengh of a pereat (max is ) :"
label_4.place ({"x":5, "y":355})

lengh_entry = Entry (querry_frame)
lengh_entry.get()
lengh_entry.place({"x":230, "y":355, "width": 50, "height":20 })

var_seq_short = BooleanVar()
var_seq_short.set(1)
check_1 = Checkbutton (querry_frame, text = "Delete nested repeats?", variable = var_seq_short, onvalue = 1, offvalue = 0)
check_1.place ({"x": 5, "y":375})

button_search = Button (querry_frame)
button_search["text"] = "Search"
button_search ["command"] = click_4
button_search.place( {"x": 350, "y":375, "height":30, "width": 60})

result_frame = LabelFrame (root, text ="Results", font = 14)
result_frame.place({"x":440, "y":10, "height":430, "width": 300 })

label_5 = Label(result_frame)
label_5 ["text"] = "Overall repeats: "
label_5.place({"x":5, "y":0})

label_6 = Label(result_frame)
label_6 ["text"] = "Repeats types: "
label_6.place({"x":5, "y":20})

button_show = Button(result_frame)
button_show ["text"] = "Show results"
button_show ["command"] = click_5
button_show.place({"x":10, "y":40})


button_save = Button(result_frame)
button_save ["text"] = "Save as JSON"
button_save ["command"] = save_repeats
button_save.place({"x":100, "y":40})


button_show_types = Button(result_frame)
button_show_types ["text"] = "Show types"
button_show_types ["command"] = show_types
button_show_types.place({"x":200, "y":40})


frame_3 = LabelFrame(result_frame, text = "Searching by order")
frame_3.place({"x":5, "y":80, "height":150, "width": 285 })

label_7 = Label(frame_3)
label_7 ["text"] = "Enter a repeat number:"
label_7.place ({"x":5, "y":10})

rep_entry = Entry (frame_3)
rep_entry.get()
rep_entry.place({"x":140, "y":10, "width": 50, "height":20 })

button_highlight = Button(frame_3)
button_highlight ["text"] = "Show"
button_highlight ["command"] = click_6
button_highlight.place ({"x":200,"y":5})

label_8 = Label(frame_3)
label_8 ["text"] = "Sequence:"
label_8.place ({"x":5, "y":45})

rep_text = Text(frame_3)
rep_text.place({"x":70, "y":45, "width": 150, "height":20})

label_9 = Label(frame_3)
label_9 ["text"] = "Type: "
label_9.place ({"x":5, "y":70})

label_10 = Label(frame_3)
label_10 ["text"] = "Position from     to   "
label_10.place({"x":5, "y":95})

button_show_in_querry = Button (frame_3) #эта кнопка не работает
button_show_in_querry ["text"] = "Show in querry"
button_show_in_querry ["command"] = click_8 
button_show_in_querry.place ({"x": 180, "y":95})

frame_4 = LabelFrame(result_frame, text = "Searching by type")
frame_4.place({"x":5, "y":235, "height":160, "width": 285 })

label_11 = Label(frame_4)
label_11 ["text"] = "Enter a type number:"
label_11.place ({"x":5, "y":10})

type_entry_2 = Entry (frame_4)
type_entry_2.place({"x":140, "y":10, "width": 50, "height":20 })

button_highlight_2 = Button(frame_4)
button_highlight_2 ["text"] = "Show"
button_highlight_2 ["command"] = click_7
button_highlight_2.place ({"x":200,"y":5})

label_12 = Label(frame_4)
label_12 ["text"] = "Sequence:"
label_12 .place ({"x":5, "y":45})

rep_text_2 = Text(frame_4)
rep_text_2.place({"x":70, "y":45, "width": 150, "height":20})


label_13= Label(frame_4)
label_13 ["text"] = "Quantity in the querry: "
label_13.place ({"x":5, "y":70})
	


root.mainloop()