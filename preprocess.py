import nltk
from nltk.corpus import stopwords
import re
import glob
from tools import *
from collections import defaultdict

def preprocess(text):
    lower = text.lower()
    tokens=re.findall(r'[a-z]+',lower)
    stop_words = stopwords.words('english')
    stop_words.append('reuter')
    stop_words.append('reuters')
    filtered_tokens = []
    for w in tokens:
        if w not in stop_words:
            filtered_tokens.append(w)
    s = nltk.stem.SnowballStemmer("english")
    normalisation_tokens = [s.stem(ws) for ws in filtered_tokens]
    return normalisation_tokens

def get_content(text):
    contents=re.findall(r'\<[T][E][X][T].*?\>.*?\<\/[T][E][X][T]\>',text)
    all_tokens=[]
    for content in contents:
        title=re.findall(r'\<[T][I][T][L][E]\>.*?\<\/[T][I][T][L][E]\>',content)
        body=re.findall(r'\<[B][O][D][Y]\>.*?\<\/[B][O][D][Y]\>',content)
        remove_title=''
        remove_body=''
        if title:
            remove_title=re.sub(r'\<\/?[T][I][T][L][E]','',title[0])
        if body:
            remove_body=re.sub(r'\<\/?[B][O][D][Y]\>','',body[0])
        remove_content=remove_title+' '+remove_body
        tokens=preprocess(remove_content)
        all_tokens.append([' '.join(tokens)])
    return all_tokens

def get_topics(text):
    contents=re.findall(r'\<[T][O][P][I][C][S]\>.*?\<\/[T][O][P][I][C][S]\>',text)
    all_topics=[]
    for content in contents:
        remove_content=re.sub(r'\<\/?[T][O][P][I][C][S]\>','',content)
        remove_content=re.sub(r'\<\/?[D]\>',' ',remove_content).lstrip().strip()
        all_topics.append(remove_content)
    return all_topics

def get_tag(text):
    tags=re.findall(r'[L][E][W][I][S][S][P][L][I][T]\=\".*?\"',text)
    all_tags=[]
    for tag in tags:
        remove_tag=re.findall(r'\".*?\"',tag)
        remove_tag=re.sub(r'\"',"",remove_tag[0])
        all_tags.append(remove_tag)
    return all_tags

def get_tokens():
    files=glob.glob("reuters21578/reut2-*.sgm")
    all_tokens=[]
    for file in files:
        print(file)
        whole_news=read_file(file)
        labels=get_tag(whole_news)
        tokens_in_file=get_content(whole_news)
        topics_in_file=get_topics(whole_news)
        print(len(labels),len(tokens_in_file),len(topics_in_file))
        for i in range(len(topics_in_file)):
            tokens_in_file[i].insert(0,topics_in_file[i])
            tokens_in_file[i].insert(0,labels[i])
        all_tokens.extend(tokens_in_file)
    dict=transfer_dict(all_tokens)
    save_json('json_data/reut2.json',dict)

def count_categories():
    data=get_dict()
    number_of_category=defaultdict(int)
    for key in data:
        catagories=data.get(key)[1]
        if catagories:
            catagories=catagories.split()
            for catagory in catagories:
                number_of_category[catagory]+=1
    list_catas=sorted(number_of_category.items(),key=lambda items:items[1],reverse=True)
    define={}
    i=0
    for name in list_catas:
        if i<11:
            i+=1
        define[name[0]]=str(i)
    save_json('json_data/catas.json',define)

def word_count():
    data=get_dict()
    number_word=defaultdict(int)
    length=0
    for key in data:
        content=data.get(key)[-1].split()
        length+=len(content)
        for word in content:
            number_word[word]+=1
    print("number of types: %d, number of tokens: %d." %(len(number_word),length))
    print(sorted(number_word.items(),key=lambda item:item[1],reverse=True))
    return number_word

if __name__=="__main__":
    # get_tokens()
    # count_categories()
    word_count()

