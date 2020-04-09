from preprocess import *
import math
import numpy as np
import matplotlib.pyplot as plt

def count_prob_categories(num_of_data):
    listcat = count_categories()
    prob_of_category = defaultdict(float)

    for i, item in enumerate(listcat):
        if i < 10:
            prob_of_category[item[0]] = item[1] / num_of_data

    save_json('json_data/catas_prob.json', prob_of_category)
    print(prob_of_category)


def count_prob_words(num_of_data):
    vocab = load_json('json_data/vocab.json')
    data = load_json('json_data/reut2.json')
    words_appearance_prob = defaultdict(float)
    words_appearance_count = defaultdict(int)

    for word in vocab.keys():
        for key in data.keys():
            catagories = data.get(key)[1]
            if catagories:
                if word in data.get(key)[2].split():
                    words_appearance_count[word] += 1
    for word in words_appearance_count.keys():
        words_appearance_prob[word] += words_appearance_count[word] / num_of_data

    save_json('json_data/words_prob.json', words_appearance_prob)


def count_joint_prob(num_of_data):
    vocab = load_json('json_data/vocab.json')
    data = load_json('json_data/reut2.json')
    catas = load_json('json_data/catas.json')
    joint_count_dict = defaultdict(lambda: defaultdict(int))
    joint_prob_dict = defaultdict(lambda: defaultdict(float))

    cat_list = []
    for i, c in enumerate(catas.keys()):
        if i < 10:
            cat_list.append(c)

    for cat in cat_list:
        for word in vocab.keys():
            for key in data.keys():
                if cat in data.get(key)[1].split():
                    if word in data.get(key)[2].split():
                        joint_count_dict[word][cat] += 1
    for word in joint_count_dict.keys():
        for cat in joint_count_dict[word].keys():
            joint_prob_dict[word][cat] = joint_count_dict[word][cat] / num_of_data

    save_json('json_data/joint_prob.json', joint_prob_dict)

def get_mi():
    vocab_prob = load_json('json_data/words_prob.json')
    data = load_json('json_data/reut2.json')
    catas_prob = load_json('json_data/catas_prob.json')
    joint_prob = load_json('json_data/joint_prob.json')
    label='earn'
    mi_dict={}
    for key in data:
        value=data.get(key)
        if label in value[1].split():
            for word in value[2].split():
                pmi = math.log2(joint_prob[word][label]/(catas_prob[label]*vocab_prob[word]))
                if pmi>0:
                    mi_dict[word]=joint_prob[word][label]*pmi
    save_json('json_data/mi_earn.json',mi_dict)

def feature_extract():
    files=glob.glob('json_data/mi_*.json')
    features={}
    for file in files:
        mi=load_json(file)
        name=str(file)
        label=re.findall(r'[_]\w+',name)[1]
        label=re.sub(r'[_]','',label)
        feature=[]
        for key in mi:
            feature.append(key)
        features[label]=feature[:256]
    save_json('json_data/features.json',features)

def feature_vector(label,text):
    features=load_json('json_data/features.json')
    feature=features[label]
    vector=[0]*len(feature)
    for i in range(len(feature)):
        if feature[i] in text:
            vector[i]=1
    return vector

if __name__ == "__main__":
    feature_extract()
    feature=load_json('json_data/features.json')
    for key in feature:
        print(len(feature.get(key)))
    # data=count_categories()
    # name=[]
    # freq=[]
    # for value in data:
    #     name.append(value[0])
    #     freq.append(value[1])
    # x=np.arange(1,11)
    # y=np.array(freq[:10])
    # print(y)
    # plt.xlabel('class_name')
    # plt.ylabel('frequency')
    # plt.bar(x,y,0.5,color='red',tick_label=name[:10])
    # plt.show()

    



