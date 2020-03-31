from tools import *
from preprocess import *


def get_features():
    word_dict = word_count()


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


if __name__ == "__main__":
    data = load_json('json_data/reut2.json')
    num_of_data = 0

    for key in data.keys():
        catagories = data.get(key)[1]
        if catagories:
            num_of_data += 1
    print(num_of_data)

    count_joint_prob(num_of_data)
    # count_prob_categories(num_of_data)
    # count_prob_words(num_of_data)
