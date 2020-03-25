import json

def read_file(name):
    f=open(name,'r',errors='ignore')
    lines=f.readlines()
    article=""
    for line in lines:
        article+=line.strip()
    return article

def transfer_dict(tokens):
    save={}
    for i in range(len(tokens)):
        save[str(i+1)]=tokens[i]
    return save

def save_json(name,tokens):
    dict=transfer_dict(tokens)
    file=open(name,'w+')
    json.dump(dict,file)

def load_json(name):
    file=open(name,'r+')
    return json.load(file)
