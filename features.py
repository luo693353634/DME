from tools import *
from preprocess import *


def get_features():
    word_dict = word_count()


def count_prob_categories():
    listcat = count_categories()
    prob_of_category = defaultdict(float)
    num_of_data = 0
    data = load_json('json_data/reut2.json')

    for key in data.keys():
        catagories = data.get(key)[1]
        if catagories:
            num_of_data += 1
    print(num_of_data)

    for i, item in enumerate(listcat):
        if i < 10:
            prob_of_category[item[0]] = item[1] / num_of_data

    save_json('json_data/catas_prob.json', prob_of_category)
    print(prob_of_category)


def count_prob_words():
    vocab = load_json('json_data/vocab.json')
    data = load_json('json_data/reut2.json')
    num_of_data = 0
    words_appearance_prob = defaultdict(float)
    words_appearance_count = defaultdict(int)

    for key in data.keys():
        catagories = data.get(key)[1]
        if catagories:
            num_of_data += 1
    print(num_of_data)

    for word in vocab.keys():
        for key in data.keys():
            catagories = data.get(key)[1]
            if catagories:
                if word in data.get(key)[2].split():
                    words_appearance_count[word] += 1
    for word in words_appearance_count.keys():
        words_appearance_prob[word] += words_appearance_count[word] / num_of_data

    save_json('json_data/words_prob.json', words_appearance_prob)


# def count_joint_prob():
#     vocab = load_json('json_data/vocab.json')
#     data = load_json('json_data/reut2.json')
#     num_of_data = 0
#     words_appearance_prob = defaultdict(float)
#     words_appearance_count = defaultdict(int)
#
#     for key in data.keys():
#         catagories = data.get(key)[1]
#         if catagories:
#             num_of_data += 1
#     print(num_of_data)
# 
#     for word in vocab.keys():
#         for key in data.keys():
#             catagories = data.get(key)[1]
#             if catagories:
#                 if word in data.get(key)[2].split():
#                     words_appearance_count[word] += 1
#     for word in words_appearance_count.keys():
#         words_appearance_prob[word] += words_appearance_count[word] / num_of_data
#
#     save_json('json_data/words_prob.json', words_appearance_prob)


if __name__ == "__main__":
    count_prob_categories()
    count_prob_words()
