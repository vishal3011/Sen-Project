import sys
import random
import copy

#nltk imports

import nltk
from nltk.tokenize import *
from nltk.corpus import *
#from nltk.tag.stanford import *
from nltk.tag.stanford import StanfordPOSTagger

#pyqt5 imports

from PyQt5.QtWidgets import (QWidget, QPushButton, QTextEdit, QTextBrowser,
    QInputDialog, QApplication, QGridLayout, QLabel, QMessageBox)
from PyQt5.QtGui import (QPalette, QFont, QIntValidator)

#speech recognition imports

import speech_recognition as sr
import pyaudio

r = sr.Recognizer()


code_file = open('sag.c','a')

code_file.write("#include<stdio.h>\n\n")

code_file.write("main(){\n")

global lines

declarations=["declar","creat","tak","mak","consider","new"]
datatypes=["int","char","long","float","double"]
initialize=["giv","initializ","assign","store"]
scanner=["accept","input","scan","take from user","take from screen","intake","read"]
printer=["print", "output", "display"]
arithmetic = ["sum","add","difference","subtract","multiply","product","divide","mod","plus","minus","by","times"]
loop = ["loop", "iterat"]
conditional = ["if","else","otherwise","else if","while"]
var_names=[]

nam_val=[]
val_exists = []




# Main class for application widget display

class Example(QWidget):
    

    # Constructor

    def __init__(self):
        super().__init__()

        
        self.initUI()

    # PyQt application widget development
     
    def initUI(self):

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('C-erious')
        self.setFixedSize(720,600)
        self.setStyleSheet('background-color:'+'#005050'+';')
        
        global btn1, btn2, btn3, btn4, btngo,b1,b2,b3,b4,b5,b6,b7
        btn1 = QPushButton('LISTEN', self)
        btn1.move(10, 10)
        btn1.clicked.connect(lambda: self.create_listen_func())
        btn1.setStyleSheet('background-color:'+'#333333'+';')

          

        btngo = QPushButton('GO', self)
        btngo.move(190, 10)
        btngo.clicked.connect(lambda: self.go_func())
        btngo.setStyleSheet('background-color:'+'#333333'+';')

        btn2 = QPushButton('RESET', self)
        btn2.move(100, 10)
        btn2.setEnabled(False)
        btn2.clicked.connect(lambda: self.reset_func())
        btn2.setStyleSheet('background-color:'+'#333333'+';')

        global text1, text2, text3
        text1 = QTextEdit(self)
        text1.move(10, 60)
        text1.setFixedSize(340,80)
        text1.setStyleSheet('background-color:'+'#FFF'+';')

        btn3 = QPushButton('GET TUTORIAL', self)
        btn3.move(10, 160)
        btn3.clicked.connect(lambda: self.get_tutorial_func())
        btn3.setStyleSheet('background-color:'+'#333333'+';')
        #btn3.setEnabled(True)
       # btn3.setObjectName("get_tut")

    
        # b1 =  QPushButton('Declare', self)
        # b1.clicked.connect(lambda: self.get_declaration_func())


        # b2 = QPushButton('I/O',self)
        # b2.clicked.connect(lambda: self.get_inout_func())

        # b3 = QPushButton('For Loop', self)
        # b3.clicked.connect(lambda: self.get_for_loop_func())

        # b4 = QPushButton('While Loop', self)
        # b4.clicked.connect(lambda: self.get_while_loop_func())

        # b5 = QPushButton('Arrays', self)
        # b5.clicked.connect(lambda: self.get_arrays_func())

        # b6 = QPushButton('Pointers', self)
#        b6.clicked.connect(lambda: self.get_pointers_func())

#        b7 = QPushButton('If/Else', self)
#        b7.clicked.connect(lambda: self.get_if_else_func())




        btn4 = QPushButton('HELP', self)
        btn4.move(100, 160)
        btn4.setStyleSheet('background-color:'+'#333333'+';')
        btn4.clicked.connect(lambda: self.get_help_func())


        text2 = QTextBrowser(self)
        text2.move(10,210)
        text2.setFixedSize(340,360)
        text2.setStyleSheet('background-color:'+'#FFF'+';')

        text3 = QTextEdit(self)
        text3.move(360, 10)
        text3.setFixedSize(340,560)
        text3.setStyleSheet('background-color:'+'#FFF'+';')
        

        self.move(200, 10)
        self.show()
        
        
    
    

    def create_listen_func(self):
        #btn2.setEnabled(True)
        #btn1.setEnabled(False)
        #text1.setText("")


        #listening
        
        with sr.Microphone(sample_rate = 16000) as source:
            audio = r.listen(source)	

        print("Listening")
 

        try:
            lines = r.recognize_google(audio)
            print("you said " + lines)
            text1.setText(lines)
        except LookupError:
            print("Couldn't understand audio")
            text1.setText("Couldn't understand audio")
            
        c = word_tokenize(lines.lower())
        st = StanfordPOSTagger('C:\stanford-postagger-2015-12-09\models\english-bidirectional-distsim.tagger')
        b = st.tag(c)

        
        #print(b)
        flag = 0
        loopflag = 0

            # decflag=0
            # iniflag=0
            # scanflag=0
            # pflag=0
            # aflag=0
            #print(b)

        dict = {"VB": [], "NN": [], "JJ": [], "DT": [], "CC": [], "PR": [], "CD": [], "IN": [], "RB": []}

        for (w,t) in b:
            if (t[:2] in dict):
                dict[t[:2]].append(w)

        print(dict)

        
        #checking if the statement is a declaration
        try:
            for i in dict["VB"]:
                for d in declarations:
                    if d in i:
                        dict["VB"].remove(i)
                        #decflag = 1
                        flag = 1
                        
                        self.declare(dict)
                        break
                    #if decflag == 1:
                if flag == 1:
                    break
            
            #checking if the statement is an initialization

            if(flag == 0):
            #if(decflag == 0):
                for i in dict["VB"]:
                    for ini in initialize:
                        if ini in i:
                            flag = 1
                            #print("hermoine")
                            #iniflag = 1                          
                            self.init(dict)
                            break
                    #if iniflag == 1:
                    if flag == 1:
                        break

            #Printing output to screen
            if(flag == 0):
            #if(decflag == 0 and iniflag == 0):
                for i in dict["NN"] or dict["VB"]:
                    for p in printer:
                        if p in i:
                            flag =1
                            #pflag = 1
                            self.prin(dict)
                            break
                    if flag == 1:
                        #if pflag == 1:
                        break

            #Scanning input from screen
            if(flag == 0):
            #if(decflag == 0 and iniflag == 0 and pflag == 0):
                for i in dict["VB"] or dict["NN"]:
                    for s in scanner:
                        if s in i:
                            #dict["VB"].remove(i)
                            flag = 1
                            #scanflag = 1
                            self.scan(dict)
                            break
                    #if scanflag == 1:
                    if flag == 1:
                        break
                    #if scanflag == 0:
                    if flag == 0:
                        if("take from user" in a or "take from screen" in a or "take in" in a):
                            self.scan(dict)
                            flag = 1
                            #scanflag = 1

            #Looping
            if(flag == 0):
                for i in loop:
                    if i in a:
                        flag = 1
                        self.loop(dict)
                        break



            #arithmetic operations
            #if(decflag==0 and iniflag==0 and pflag==0 and scanflag == 0):
            if(flag == 0):
                for i in dict["VB"] + dict["NN"] + dict["CC"]:
                    for art in arithmetic:
                        #print(a,i)
                        if art in i:
                            flag = 1
                            #aflag = 1
                            self.arithmo(dict)
                            break
                        if flag == 1:
                        #if aflag==1:
                            break

            if(flag == 0):

                for i in dict["IN"] + dict["JJ"] + dict["CC"] + dict["RB"]:
                    for art in conditional:
                        if art in i:
                            flag = 1
                            self.cond(dict)
                            break
                        if flag == 1:
                            break
        except Exception:
            print("exception")

        code_file.write("\n}")
        
        #temp_str = code_file.read()

        #text3.append(temp_str)
        #btn1.setEnabled(True)
        #btn2.setEnabled(False)
            

    def get_tutorial_func(self):
        #text2.setText("Sample Tutorial here.");

        #New dialog box added in get tutorial button
        #New buttons are added in dialog box
        #Every button is asssociated to read a file and show it on the tex2 box
        box2 = QMessageBox()
        box2.setWindowTitle("Tutorial")
        box2.setText("Please select any option!")

        b1 =  QPushButton('Declare', self)
        b1.clicked.connect(lambda: self.get_declaration_func())


        b2 = QPushButton('I/O',self)
        b2.clicked.connect(lambda: self.get_inout_func())

        b3 = QPushButton('For Loop', self)
        b3.clicked.connect(lambda: self.get_for_loop_func())

        b4 = QPushButton('While Loop', self)
        b4.clicked.connect(lambda: self.get_while_loop_func())

        b5 = QPushButton('Arrays', self)
        b5.clicked.connect(lambda: self.get_arrays_func())

        b6 = QPushButton('Pointers', self)
        b6.clicked.connect(lambda: self.get_pointers_func())

        b7 = QPushButton('If/Else', self)
        b7.clicked.connect(lambda: self.get_if_else_func())


        box2.addButton(b1, QMessageBox.AcceptRole)      
        box2.addButton(b2, QMessageBox.AcceptRole)
        box2.addButton(b3, QMessageBox.AcceptRole)
        box2.addButton(b4, QMessageBox.AcceptRole)
        box2.addButton(b5, QMessageBox.AcceptRole)
        box2.addButton(b6, QMessageBox.AcceptRole)
        box2.addButton(b7, QMessageBox.AcceptRole)
        box2.setStandardButtons(QMessageBox.Close)
        box2.exec_()

    def get_declaration_func(self):
        var_declare = open('declare.txt').read()
        #print (var_declare)
        text2.setText(var_declare)

    def get_inout_func(self):
        #inout_ = open('in_out.txt').read()
        text2.setText("""******************Printf() *******************

Printf is a predefined function in “stdio.h” header file, by using this function ,we can print the data or user defined message on console or moniter. It can take any number of arguments but first argument must be within the double quotes (“ ”) and every argument should be seperated with comma( , ).

Syntax:
        printf(“Format specifiers”,value1,value2....);
        
Format Specifier
Description
Supported Data Types
%d
Signed Integer
short
unsigned short
int
long
%c
Character
 char
unsigned char
%f
Floating point
float
%lf
Floating point
double
%s
String
char *


Examples:
        printf(“ user defined message ”);

l




********************Scanf()*******************

scanf() is a predefined function in “stdio.h” header file. It can be used to read the input value from the keyboard

Syntax
    scanf(“format specifiers”,&value1,&value2....);

Examples:
    int a;
    float b;
    scanf(“%d,%f”,&a,&b);

""")

    def get_for_loop_func(self):
        for_ = open('for_loop.txt').read()
        text2.setText(for_)

    def get_while_loop_func(self):
        while_ = open('while_loop.txt').read()
        text2.setText(while_)

    def get_arrays_func(self):
        array_ = open('array.txt').read()
        text2.setText(array_)

    def get_pointers_func(self):
        pointer_ = open('pointers.txt').read()
        text2.setText(pointer_)

    def get_if_else_func(self):
        if_ = open('ifelse.txt').read()
        text2.setText(if_)

    def get_help_func(self):
        box1 = QMessageBox()
        box1.setWindowTitle("HELP")
        #tut = open('tutorial.txt').read()
        box1.setText("Developed by Team 5 Software Engineering-IIITV")
        #text2.setText(tut)
        box1.setStandardButtons(QMessageBox.Ok)
        box1.exec_()
        
    #important methods for implementation

    def index_find(li,w):
        ind = 0
        for index in range(len(c)):
            if li[index] == w:
                ind = index
        return ind

    def go_func(self):
        global c
        c = word_tokenize(str(text1.toPlainText()).lower())
        st = StanfordPOSTagger('C:\stanford-postagger-2015-12-09\models\english-bidirectional-distsim.tagger')
        b = st.tag(c)

        
        #print(b)
        flag = 0
        loopflag = 0

            # decflag=0
            # iniflag=0
            # scanflag=0
            # pflag=0
            # aflag=0
            # print(b)

        dict = {"VB": [], "NN": [], "JJ": [], "DT": [], "CC": [], "PR": [], "CD": [], "IN": [], "RB": []}

        for (w,t) in b:
            if (t[:2] in dict):
                dict[t[:2]].append(w)

        print(dict)

        
        #checking if the statement is a declaration
        try:
            for i in dict["VB"]:
                for d in declarations:
                    if d in i:
                        dict["VB"].remove(i)
                        #decflag = 1
                        flag = 1
                        
                        self.declare(dict)
                        break
                    #if decflag == 1:
                if flag == 1:
                    break
            
            #checking if the statement is an initialization

            if(flag == 0):
            #if(decflag == 0):
                for i in dict["VB"]:
                    for ini in initialize:
                        if ini in i:
                            flag = 1
                            #print("hermoine")
                            #iniflag = 1                          
                            self.init(dict)
                            break
                    #if iniflag == 1:
                    if flag == 1:
                        break


            if(flag == 0):
#if(decflag == 0 and iniflag == 0):
                for i in dict["NN"] or dict["VB"]:
                    for p in printer:
                        if p in i:
                            flag =1
                            #pflag = 1
                            self.prin(dict)
                            break
                    if flag == 1:
                    #if pflag == 1:
                        break


            #Scanning input from screen
            if(flag == 0):
            #if(decflag == 0 and iniflag == 0 and pflag == 0):
                for i in dict["VB"] or dict["NN"]:
                    for s in scanner:
                        if s in i:
                            #dict["VB"].remove(i)
                            flag = 1
                            #scanflag = 1
                            self.scan(dict)
                            break
                    #if scanflag == 1:
                    if flag == 1:
                        break
                    #if scanflag == 0:
                    if flag == 0:
                        if("take from user" in a or "take from screen" in a or "take in" in a):
                            self.scan(dict)
                            flag = 1
                            break
                            #scanflag = 1

            if(flag == 0):
            
                for i in dict["IN"] + dict["JJ"] + dict["CC"] + dict["RB"]:

                    for cond in conditional:
                        if cond in i:
                            flag = 1
                            
                            self.cond(dict)
                            break
                        if flag == 1:
                            break   
         






            #arithmetic operations
            #if(decflag==0 and iniflag==0 and pflag==0 and scanflag == 0):
            if(flag == 0):
            
                for i in dict["VB"] + dict["NN"] + dict["CC"]:
                    
                    for art in arithmetic:
                        #print("here     ")
                        #print(a,i)
                        if art in i:
                            flag = 1
                            #aflag = 1
                            t = self.arithmo(dict)
                            print(t)
                            break
                        if flag == 1:
                        #if aflag==1:
                            break
            #print(flag)
           
           


        except Exception:

            print("exception")

                    
    def quotes(self,w):
        return('\''+w+'\'')

    def addoperator(self,d):
        return d[0]+"+"+d[1]

    def suboperator(self,d):
        return d[0]+"-"+d[1]

    def muloperator(self,d):
        return d[0]+"*"+d[1]

    def divoperator(self,d):
        return d[0]+"/"+d[1]

    def modoperator(self,d):
        return d[0]+"%"+d[1]		

    def declare(self, di):
        dt = ''
        for j in di["NN"] or di["JJ"]:
            #comparing to find the datatype
            for d in datatypes:
                if d in j:
                    dt = d
                    if j in di["NN"]:
                        di["NN"].remove(j)
                    else:
                        di["JJ"].remove(j)
                    break
                if dt!='':
                    break
        if(dt == ''):
            dt = input("Please enter a valid datatype for the variable")

	#Variable or array?
        if 'variable' in di["NN"]:
            di["NN"].remove('variable')
        elif 'variable' in di["JJ"]:
            di["JJ"].remove('variable')
        #di["NN"].remove('array')

        

	#print(di)
	#Obtaining the names

        if len(di["NN"]) == 1:
            w = di["NN"][0]
            var_names.append(w)
            nam_val.append((w,dt))
            text3.append(dt+ " " + w+ ";\n")
            code_file.write(dt+ " " + w+ ";\n")
        else:
            w = input("Please give a name for the variable")
            var_names.append(w)
            nam_val.append((w,dt))
            print(dt+ " " + w+ ";")
            text3.append(dt+ " " + w+ ";")
            code_file.write(dt+ " " + w+ ";\n")



    def arith(self):
        if "add" in a or "sum" in a or "plus" in a:
            print(c[new_index]+ "="+ self.addoperator(new_var)+";")
            text3.append(c[new_index]+ "="+ self.addoperator(new_var)+";")
            code_file.write(c[new_index]+ "="+ self.addoperator(new_var)+";\n")
        elif "subtract" in a or "difference" in a or "minus" in a:
            print(c[new_index]+ "="+ self.suboperator(new_var)+";")
            text3.append(c[new_index]+ "="+ self.suboperator(new_var)+";")
            code_file.write(c[new_index]+ "="+ self.suboperator(new_var)+";\n")
        elif "multiply" in a or "product" in a or "times" in a:
            print(c[new_index]+ "="+ self.muloperator(new_var)+";")
            text3.append(c[new_index]+ "="+ self.muloperator(new_var)+";")
            code_file.write(c[new_index]+ "="+ self.muloperator(new_var)+";\n")
        elif "divide" in a or "by" in a or "quotient" in a :
            print(c[new_index]+ "="+ self.divoperator(new_var)+";")
            text3.append(c[new_index]+ "="+ self.divoperator(new_var)+";")
            code_file.write(c[new_index]+ "="+ self.divoperator(new_var)+";\n")
        elif "mod" in a or "modulus" in a or "remainder" in a:
            print(c[new_index]+ "="+ self.modoperator(new_var)+";")
            text3.append(c[new_index]+ "="+ self.modoperator(new_var)+";")
            code_file.write(c[new_index]+ "="+ self.modoperator(new_var)+";\n")

	


    def init(self, di):
        
        charflag = 0
        x= '1'
        y= '1'
        #print(c)
        for i in c:
            
            if (i,'char') in nam_val:
                
                if x=='1':
                    charflag = 1
                    x = i
                    #print(x)
                else:
                    y = i
                    break

            elif i in var_names:
                #text3.append(i)
                if x=='1':
                    x = i
                    
                else:
                    y=i
                    #text3.append(y)
                    break
           
        for index in range(len(c)):
            
            if c[index] == 'ascii':
                char_index = index+2

        #text3.append(x)
        #text3.append(y)
        #text3.append("enters here")
        #print(char_index)
        if charflag == 1:
            if 'ascii' in c:
                print(x + "=" +self.quotes((c[char_index]))+";" )
                text3.append(x + "=" + self.quotes((c[char_index]))+";\n")
                code_file.write(x + "=" + self.quotes((c[char_index]))+";\n" )

            else:
                if 'to' in c and di["VB"][0] == "assign":
                    print(y +" = " + x + ";")
                    text3.append(y +" = " + x + ";\n")
                    code_file.write(y +" = " + x + ";\n")
                else:
                    print(x +" = " + y + ";")
                    text3.append(x +" = " + y + ";\n")
                    code_file.write(x +" = " + y + ";\n")

        

        elif x == '1' and len(di["CD"]) == 0:
            print ("please first declare this variable")

        elif y == '1':
            #text3.append("enters here")
            print(x +" = " + di["CD"][0] + ";")
            text3.append(x +" = " + di["CD"][0] + ";\n")
            code_file.write(x +" = " + di["CD"][0] + ";\n")

        else:
            if 'to' in c and di["VB"][0] == "assign":
                print(y +" = " + x + ";")
                text3.append(y +" = " + x + ";\n")
                code_file.write(y +" = " + x + ";\n")
            else:
                print(x +" = " + y + ";")
                text3.append(x +" = " + y + ";\n")
                code_file.write(x +" = " + y + ";\n")
	


    def scan(self, di):
        for (w,t) in nam_val:
            if w in c:
                if t == "int":
                    print("scanf(\"%d\",&" + w + ");")
                    text3.append("scanf(\"%d\",&" + w + ");")
                    code_file.write("scanf(\"%d\",&" + w + ");\n")
                elif t == "float":
                    print("scanf(\"%f\",&" + w + ");")
                    text3.append("scanf(\"%f\",&" + w + ");")
                    code_file.write("scanf(\"%f\",&" + w + ");\n")
                elif t == "char":
                    print("scanf(\"%c\",&" + w + ");")
                    text3.append("scanf(\"%c\",&" + w + ");")
                    code_file.write("scanf(\"%c\",&" + w + ");\n")
                elif t == "long":
                    print("scanf(\"%ld\",&" + w + ");")
                    text3.append("scanf(\"%ld\",&" + w + ");")
                    code_file.write("scanf(\"%ld\",&" + w + ");\n")
                elif t == "double":
                    print("scanf(\"%lf\",&" + w + ");")
                    text3.append("scanf(\"%lf\",&" + w + ");")
                    code_file.write("scanf(\"%lf\",&" + w + ");\n")


    def prin(self, di):

        str="printf (\""
        #print(str)
        vars = []

        break_pts = []
        for i in range(len(c)):
            if (c[i] == "plain" and c[i+1] == "text") or (c[i] == "special" and c[i+1] == "character") or c[i] == "variable":
                break_pts.append(i)


        #print(break_pts)
        for i in range(len(break_pts)):
            #print(i)
            #print(c[break_pts[i]])
            if c[break_pts[i]] == "plain":
                p = break_pts[i]+2
                #print(c[p])
                if i < len(break_pts)-1:
                    #print(i)
                    #str = str + "\""
                    while p < break_pts[i+1]:
                        str = str + c[p] + " "
                        p = p+1
                        #str = str + "\""

                else:
                    #str = str + "\""
                    while p < len(c):
                        str = str + c[p] + " "
                        p = p+1
                        #str = str + "\""

            elif c[break_pts[i]] == "variable":

                v = c[break_pts[i]+1]

                for (w,t) in nam_val:
                    if v == w:
                        vars.append(v)
                        if t == "int":
                            str = str + "%d "
                        elif t == "float":
                            str = str + "%f "
                        elif t == "char":
                            str = str + "%c "
                        elif t == "long":
                            str = str + "%ld "
                        elif t == "double":
                            str = str + "%lf "

            else:
                p = break_pts[i] + 2
                if c[p] == "tab":
                    str = str + "\\t "
                elif c[p] == "space":
                    str = str + " "
                else:
                    str = str + "\\n"

        str = str + "\""

        for v in vars:
            str = str + "," + v

        str = str + ");"

        print(str)
        text3.append(str)
        code_file.write(str+"\n")

    def arithmo(self, di):
        new_var = []
        inflag = 0
        for index in range(len(c)):
            if c[index] == 'in':
                inflag = 1
                new_index = index+1
                break

        if inflag == 1:
            for i in c:
                if i in var_names:
                    new_var.append(i)

                new_var.remove(c[new_index])
                #print(new_var)
                print(a)
                if "add" in a or "sum" in a or "plus" in a:
                    print(c[new_index]+ "="+ addoperator(new_var)+";")
                    text3.append(c[new_index]+ "="+ addoperator(new_var)+";")
                    code_file.write(c[new_index]+ "="+ addoperator(new_var)+";\n")
                elif "subtract" in a or "difference" in a or "minus" in a:
                    print(c[new_index]+ "="+ suboperator(new_var)+";")
                    text3.append(c[new_index]+ "="+ suboperator(new_var)+";")
                    code_file.write(c[new_index]+ "="+ suboperator(new_var)+";\n")
                elif "multiply" in a or "product" in a or "times" in a:
                    print(c[new_index]+ "="+ muloperator(new_var)+";")
                    text3.append(c[new_index]+ "="+ muloperator(new_var)+";")
                    code_file.write(c[new_index]+ "="+ muloperator(new_var)+";\n")
                elif "divide" in a or "by" in a or "quotient" in a :
                    print(c[new_index]+ "="+ divoperator(new_var)+";")
                    text3.append(c[new_index]+ "="+ divoperator(new_var)+";")
                    code_file.write(c[new_index]+ "="+ divoperator(new_var)+";\n")
                elif "mod" in a or "modulus" in a or "remainder" in a:
                    print(c[new_index]+ "="+ modoperator(new_var)+";")
                    text3.append(c[new_index]+ "="+ modoperator(new_var)+";")
                    code_file.write(c[new_index]+ "="+ modoperator(new_var)+";\n")

        elif inflag == 0:
            #print("here")
            for index in range(len(c)):
                if c[index] == 'equals' or c[index] == 'equal' :
                    #print("her")
                    new_index = index-1

                new_var = var_names.copy()
                new_var.remove(c[new_index])

                #print(a)

                if "add" in a or "sum" in a or "plus" in a:
                    print(c[new_index]+ "="+ addoperator(new_var)+";")
                    text3.append(c[new_index]+ "="+ addoperator(new_var)+";")
                    code_file.write(c[new_index]+ "="+ addoperator(new_var)+";\n")
                elif "subtract" in a or "difference" in a or "minus" in a:
                    print(c[new_index]+ "="+ suboperator(new_var)+";")
                    text3.append(c[new_index]+ "="+ suboperator(new_var)+";")
                    code_file.write(c[new_index]+ "="+ suboperator(new_var)+";\n")
                elif "multiply" in a or "product" in a or "times" in a:
                    print(c[new_index]+ "="+ muloperator(new_var)+";")
                    text3.append(c[new_index]+ "="+ muloperator(new_var)+";")
                    code_file.write(c[new_index]+ "="+ muloperator(new_var)+";\n")
                elif "divide" in a or "by" in a or "quotient" in a :
                    print(c[new_index]+ "="+ divoperator(new_var)+";")
                    text3.append(c[new_index]+ "="+ divoperator(new_var)+";")
                    code_file.write(c[new_index]+ "="+ divoperator(new_var)+";\n")
                elif "mod" in a or "modulus" in a or "remainder" in a:
                    print(c[new_index]+ "="+ modoperator(new_var)+";")
                    text3.append(c[new_index]+ "="+ modoperator(new_var)+";")
                    code_file.write(c[new_index]+ "="+ modoperator(new_var)+";\n")

    def cond(self, di):
        ifcount = 0
        ifcount += 1
        print("condi")
        for index in range(len(c)):
            if c[index] == 'than':
                first_var = index-2
                if c[index+1] == 'variable':
                    second_var = index+2
                else:
                    second_var = index + 1
                break
            elif 'equal' in c[index]:
                first_var = index - 1
                if c[index+2] == 'variable':
                    second_var = index+3
                elif c[index+1] == 'variable':
                    second_var = index+2
                elif c[index+1] == 'to':
                    second_var = index+2
                else:
                    second_var = index+1

        #print(c)
        #print(a)
        if "greater" in c and "if" in c:
            print("if("+c[first_var] + " " + ">" + " " +c[second_var]+"){\n")
        elif "less" in c and "if" in c:
            print("if("+first_var + " " + "<" + " " +second_var+"){\n")
        elif ("else" in c or "otherwise" in c) :
            print("else{\n")
        elif ("else" in c or "otherwise" in c):
            print("else{\n")
        elif "greater than equal to" in a or "greater than or equal to" in a:
            print("hi")
        elif ("equals" in a or "equal" in a) and "if" in a:
            print("if("+c[first_var] + " " + "==" + " " +c[second_var]+"){\n")

        if "end" in c and ifcount!=0:
            print("}\n")
            ifcount -= 1
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


