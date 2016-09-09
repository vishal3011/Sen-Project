import nltk
from nltk.tokenize import *
from nltk.corpus import *

file = open('dummy.txt', 'r')
dummy= file.read()


lines = dummy.split('\n')


declarations=["declar","creat","tak","mak","consider","new",'New','Creat','Declar','Tak','Mak','Consider']
integers=["integer","int","integers"]
naming=["nam","call"]
initialize=["valu","giv","initializ","assign"]
var_names=[]

code_file = open('code.c','a')

def declare(di):
	for j in di["NN"]:
		#for jj in integers:
		if "int" in j:
			print("int")
			break

for a in lines:
	c = word_tokenize(a)
	b = nltk.pos_tag(c)
	

	dict = {"VB": [], "NN": [], "JJ": [], "DT": [], "CC": [], "PR": []}

	for (w,t) in b:
		if (t in dict):
			dict[t[:2]].append(w)

	print(dict)

	for i in dict["VB"]:
		for d in declarations:
			if d in i:
				print("yess!!!")
				declare(dict)

