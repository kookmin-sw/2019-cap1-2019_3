import numpy as np
from .cleanup_words import cleanup_wordlist


class Text2features(object):


    def __init__(self, training_data, occurance_treshold=10):
        self.initialize(training_data, occurance_treshold)

    def initialize(self, training_data, occurance_treshold=10):


        dictionary = dict()
        for document in training_data:
            words = set(document)
            for word in words:
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1

        # Remove words not occuring often
        mydicionary = dict()
        for (word, count) in dictionary.items():
            if count > occurance_treshold:
                mydicionary[word] = count

        # Calculate IDF for all words in a dict
        n_documents = len(training_data)
        for (word, count) in mydicionary.items():
            mydicionary[word] = np.log(1 + n_documents / count)

        mydicionary["UNKNOWN_TOKEN"] = 0
        self.idf_dictinary = mydicionary
        self.num2word = [w for w in mydicionary]
        self.word2num = dict([(index, key) for (key, index) in enumerate(mydicionary)])
        self.dictionary_size = len(mydicionary)

    def document2bow(self, document):

        bow = np.zeros((1, self.dictionary_size))
        if len(document) == 0:
            document = ["none"]
        inverse_Dlength = 1 / len(document)

        for word in document:
            try:
                bow[0, self.word2num[word]] += inverse_Dlength * self.idf_dictinary[word]
            except KeyError:
                # Not in dictionary
                pass

        return bow

    def raw_document2bow(self, document):
        return self.document2bow(cleanup_wordlist(document))



    def dataset2bow(self, data, labs):

        # Delete non-entries
        labels = []
        dataset = list()
        for index, sentence in enumerate(data):
            if len(sentence) > 1:
                dataset.append(sentence)
                labels.append(labs[index])

        dataset_size = len(dataset)
        final_dataset = np.zeros((dataset_size, self.dictionary_size))

        for index, document in enumerate(dataset):
            final_dataset[index, :] = self.document2bow(document)[0, :]

        return final_dataset, np.asarray(labels)
