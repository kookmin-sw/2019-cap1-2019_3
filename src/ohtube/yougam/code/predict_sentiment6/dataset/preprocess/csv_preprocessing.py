import os
import csv
import pickle

currentPath = os.getcwd()

os.chdir('/content/gdrive/My Drive/sentiment/twitter-sentiment-analysis-master/dataset')



def preprocess_cvs(data):
    final_data = []
    final_labels = []

    original2labels = dict(sadness="sad",
                           boredom="sad",
                           anger="anger",
                           hate="anger",
                           surprise="surprise",
                           happiness="happy",
                           worry="fear",
                           neutral="neutral",
                           relief="happy",
                           love="happy",
                           fun="happy",
                           fear="fear",
                           enthusiasm="happy",
                           joy = "happy",
                           empty="empty")
    name2labels = dict(neutral=0,
                       happy=1,
                       sad=2,
                       surprise=3,
                       anger=4,
                       fear=5)
    labels2names = [item for item in name2labels]


    for datarow in data[1:]:
        name = original2labels[datarow[1]]
        if name == "empty":
            continue

        label = name2labels[name]
        final_labels.append(label)
        # text = tknzr.tokenize(datarow[3])
        text = datarow[2]
        final_data.append(text)

    # for i in range(20):
    #     print(labels2names[final_labels[i]], final_labels[i], final_data[i])
    return final_data, final_labels, labels2names






def load_cvs(filename):
    # filename = where_am_i() + "/text_emotion_full.csv"
    with open(filename, "r") as fp:
        data_iter = csv.reader(fp)
        data = [data_row for data_row in data_iter]

    return data


def load_csv2lists(filename):

    data = load_cvs(filename)
    final_data, final_labels, labels2names = preprocess_cvs(data)

    return final_data, final_labels, labels2names


def pickle_object(object, filename):
    with open(filename, "wb") as fp:
      pickle.dump(object, fp)



if (__name__ == "__main__"):
    final_data, final_labels, labels2names = load_csv2lists("final_dataset3.csv")
    pickle_object((final_data, final_labels, labels2names), "dataset_pickled.pkl")
