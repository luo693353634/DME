from features import *
from sklearn import svm
from sklearn.externals import joblib

def training(label,name):
    data=get_dict()
    feature=[]
    output=[]
    for article in data:
        content=data.get(article)
        if content[0]=='TRAIN':
            x=feature_vector(label,content[2].split())
            feature.append(x)
            if label in content[1].split():
                output.append(1)
            else:
                output.append(0)
    clf=svm.LinearSVC()
    print("training_start")
    clf.fit(feature,output)
    joblib.dump(clf,name)

def test_result(label,name):
    data=get_dict()
    feature=[]
    article_id=[]
    for article in data:
        content=data.get(article)
        if content[0]=='TEST':
            article_id.append(article)
            x=feature_vector(label,content[2].split())
            feature.append(x)
    clf=joblib.load(name)
    print('loading finished')
    result=clf.predict(feature)
    print("result getting")
    save_result(label,article_id,result)

def save_result(label,article_id,result):
    data=load_json('svm_model/result.json')
    data[label]=[]
    for i in range(len(article_id)):
        if result[i]==1:
            data[label].append(article_id[i])
    save_json('svm_model/result.json',data)

def save_true_result():
    data=get_dict()
    real_label={}
    id=get_label_id()
    for label in id:
        true=[]
        print(label)
        for article in data:
            content=data.get(article)
            if content[0]=="TEST" and label in content[1].split():
                true.append(article)
        print(true)
        real_label[label]=true
    print(real_label)
    save_json('svm_model/real_label.json',real_label)

def f1_score():
    true_value=load_json('svm_model/real_label.json')
    prediction=load_json('svm_model/result.json')
    for key in prediction:
        predict=len(prediction.get(key))
        true=len(true_value.get(key))
        right=0
        for value in true_value.get(key):
            if value in prediction.get(key):
                right+=1
        precision=right/predict
        recall=right/true
        F1=(2*precision*recall)/(precision+recall)
        print(round(F1,2))




if __name__=="__main__":
    # training('wheat','svm_model/wheat.m')
    # test_result('corn','svm_model/corn.m')
    f1_score()




