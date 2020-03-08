import xml.etree.ElementTree as ET
import nltk
from nltk.corpus import stopwords
import re
import glob

def read_file(name):
    f=open(name,'r',errors='ignore')
    lines=f.readlines()
    article=""
    for line in lines:
        article+=line.strip()
    return article

def preprocess(text):
    lower = text.lower()
    tokens=re.findall(r'\w+',lower)
    stop_words = stopwords.words('english')
    filtered_tokens = []
    for w in tokens:
        if w not in stop_words:
            filtered_tokens.append(w)
    s = nltk.stem.SnowballStemmer("english")
    normalisation_tokens = [s.stem(ws) for ws in filtered_tokens]
    return normalisation_tokens

def get_content(text):
    contents=re.findall(r'\<[B][O][D][Y]\>.*?\<\/[B][O][D][Y]\>',text)
    all_tokens=[]
    for content in contents:
        remove_content=re.sub(r'\<\/?[B][O][D][Y]\>','',content)
        tokens=preprocess(remove_content)
        all_tokens.append([' '.join(tokens)])
    return all_tokens

def get_topics(text):
    contents=re.findall(r'\<[T][O][P][I][C][S]\>.*?\<\/[T][O][P][I][C][S]\>',text)
    all_topics=[]
    for content in contents:
        remove_content=re.sub(r'\<\/?[T][O][P][I][C][S]\>','',content)
        remove_content=re.sub(r'\<\/?[D]\>','',remove_content)
        all_topics.append(remove_content)
    return all_topics


def read_document():
    files=glob.glob("reuters21578/reut2-000k.sgm")
    all_tokens=[]
    for file in files:
        whole_news=read_file(file)
        tokens_in_file=get_content(whole_news)
        topics_in_file=get_topics(whole_news)
        for i in range(len(topics_in_file)):
            tokens_in_file[i].insert(0,topics_in_file[i])
        all_tokens.extend(tokens_in_file)
        print(all_tokens)
    return all_tokens

if __name__=="__main__":
    read_document()

'''
def get_index(name):         #Create inverted_index
    titles = xml_read(name, "HEADLINE")
    len_titles = []          #Store the length of headline for each ID
    lines = xml_read(name, "TEXT")
    seq = []                 #Seq store the text after preprocessing
    for i in range(len(titles)):
        title = preprocess(titles[i])
        tokens = preprocess(lines[i])
        len_titles.append(str(len(title)))
        tokens = title + tokens     #Combine headline and text
        seq.append(tokens)
    id = xml_read(name, "DOCNO")   #Store article ID
    headline_value = []     #The link for headline
    for i in range(len(id)):
        headline_value.append([id[i], "1:" + len_titles[i]])
    whole_seq = []         #Store the whole word appear in corpus
    for i in range(len(seq)):
        for word in seq[i]:
            if word not in whole_seq:
                whole_seq.append(word)
    dict = {}    #This dictionary is to match article's id and its text
    for k in range(len(id)):
        dict[id[k]] = seq[k]
    index = {}  #This dictionary store inverted_index
    for word in whole_seq: #Words in this list are unique
        position = []   # store position and article ID, like [ID,position]
        for i in dict.keys(): #Find in one article
            link = []     #This list is to store position for a word in a document
            for j in range(len(dict[i])):
                if word == dict[i][j]: #Find the position j in article i
                    link.append(str(j + 1)) # j begins from 0
            if len(link) != 0:
                position.append([i, ",".join(link)]) # match position and article ID
        index[word] = position #Write into dictionary. e.g {word: ["1","2,3,4"]}
        print(position)
    index["headline"] = headline_value  #Write link for headline
    return index       #Output is a dict


def research(name, index,output):
    f = open(name, "r")
    lines = f.readlines()
    questions = []
    for question in lines:
        questions.append(question.strip())  #read questions and store into list
    for i in range(len(questions)):
        question = re.sub(r"^\w+\s","",questions[i]) #remove quetion id like "1 "
        if "#" in question:                            # "#" means proximity search
            pattern = re.compile(r"^#[0-9]+")
            proximity = re.findall(pattern, question)
            number = int(proximity[0][1:])            #get the distance limitation
            pattern = re.compile(r"\w+\,\s*\w+")      #match two words like "a,b" without other character
            word = re.findall(pattern, question)[0]
            word = re.split(r"\W+", word)             #split and get a list
            word1 = preprocess(word[0])[0]    #word1 and word2 are str not list
            word2 = preprocess(word[1])[0]
            result=get_proximity(word1,word2,index,number,True)
            print_boolean(i+1,result,output)
        else:
            if "\"" in question:            #word with " will use different method to handle
                number=1
                pattern = re.compile(r"\"\w+\s\w+\"")
                word = re.findall(pattern, question)
                if len(word)==1:       #only have one phrase, another one is word
                    word1=word[0].split() #find word "word1 word2" and get list [word1,word2]
                    word2 = re.sub(pattern, "", question).split()    #only keep another part,and get list[word3, word4,...]
                    word1_1=preprocess(word1[0])[0]
                    word1_2=preprocess(word1[1])[0]
                    list1=get_proximity(word1_1,word1_2,index,number,False) #return the result for "word1"
                    result=get_id(list1,word2,index)
                    print_boolean(i+1,result,output)
                else:           #both of two words are phrases
                    result=[]
                    word1=word[0].split()
                    word2=word[1].split()
                    word1_1,word1_2=preprocess(word1[0])[0],preprocess(word1[1])[0]
                    word2_1,word2_2=preprocess(word2[0])[0],preprocess(word2[1])[0]
                    list1=get_proximity(word1_1,word1_2,index,number,False)#return the result for "word1"
                    list2=get_proximity(word2_1,word2_2,index,number,False)#return the result for "word2"
                    word2 = re.sub(pattern, "", question).split()
                    if "AND" in word2:          #if the logic connection is "AND"
                        if "NOT" in word2:      #if "NOT" for phrase2
                            for a in list1:
                                if a not in list2:
                                    result.append(a)
                        else:
                            for a in list1:
                                if a in list2:
                                    result.append(a)
                    if "OR" in word2:           #if the logic connection is "OR"
                         for a in list1:
                            result.append(a)
                         for b in list2 :
                            if b not in result:
                                result.append(b)
                         result=map(int,result)  #change string to int for each element.
                         result=sorted(result)   #sorting
                         result=[str(i) for i in result] #make sure document_id is string.
                    print_boolean(i+1,result,output)
            else:
                word = re.findall("\w+", question) #separate the word
                word1 = word[0]
                word1 = preprocess(word1)[0]
                word2 = word[1:]
                list1=get_list(word1,index) # the result for word1
                result=get_id(list1,word2,index)
                print_boolean(i+1,result,output)

def get_list(word1,index):
    list=index[word1]
    list1=[]
    for i in range(len(list)):
        if list[i][0] not in list1:
            list1.append(list[i][0])
    return list1

def get_proximity(word1,word2,index,number,absolute_value):
    document=[]
    list1=index[word1]
    list2=index[word2]
    for a in list1:
        for b in list2:
            if a[0]==b[0]: #have same ID
                a_positions=re.findall(r"\w+",str(a[1]))    #The position for list1
                b_positions=re.findall(r"\w+",str(b[1]))    #The position for list2
                for a_position in a_positions:  #choose one position
                    for b_position in b_positions:  #choose one position
                        if absolute_value==True:
                            if abs(int(a_position)-int(b_position))<=number and a[0] not in document:
                                document.append(a[0])      #This is for proximity search
                        elif absolute_value==False:
                            if int(b_position)-int(a_position)==number and a[0] not in document:
                                document.append(a[0])       #This is for phrase and consider the order
    return document

def get_id(list1, word2, index):
    document=[]
    if "AND" in word2:          #if "AND" in word2
        word2.remove("AND")
        if "NOT" in word2:      #if "NOT" in word2
            word2.remove("NOT")
            word2 = preprocess(word2[0])[0]
            list2 = get_list(word2,index)
            for a in list1:
                if a not in list2:
                    document.append(a)
        else:
            word2 = preprocess(word2[0])[0]
            list2 = get_list(word2,index)
            for a in list1:
                if a in list2:
                    document.append(a)
    elif "OR" in word2:        #if "OR" in word2
        word2.remove("OR")
        word2 = preprocess(word2[0])[0]
        list2 = get_list(word2,index)
        for a in list1:
            document.append(a)
        for b in list2 :
            if b not in document:
                document.append(b)
        document=map(int,document)  #change string to int for each element.
        document=sorted(document)
        document=[str(i) for i in document] #make sure document_id is string.
    else:  #   In this situation, word2 is empty.
        document=list1
    return document


def tf_idf(name,index,result):
    f=open(name,"r")
    lines=f.readlines()
    queries=[]
    for line in lines:
        line=re.sub(r"^[0-9]+\s*","",line)
        line=preprocess(line)
        queries.append(line)
    weight={}
    number = len(xml_read("trec.5000.xml", "DOCNO"))
    for i in range(len(queries)):
        query=queries[i]
        for word in query:
            if word not in weight:
                position=index[word]
                df=len(position)
                id_score=[]
                for j in range(df):
                    id=position[j][0]
                    link=re.findall(r"\w+",position[j][1])
                    tf=len(link)
                    w=(1+math.log10(tf))*math.log10(number/df)
                    if w!=0:
                        id_score.append([id,w])
                weight[word]=id_score
        score={}
        for word in query:
            id_word_weight=weight[word]
            for j in range(len(id_word_weight)):
                if id_word_weight[j][0] not in score:
                    score[id_word_weight[j][0]]=id_word_weight[j][1]
                else:
                    score[id_word_weight[j][0]]+=id_word_weight[j][1]
        rank=sorted(score.items(),key=lambda item:item[1],reverse=True)[:1000]
        print(rank)
        print_ranked(i+1,rank,result)
'''
