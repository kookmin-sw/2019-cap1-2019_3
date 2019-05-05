import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


import nltk
import string

from nltk.tokenize import word_tokenize
# tknzr = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))


from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def cleanup_wordlist(words):


    # Remove punctuation
    translator = str.maketrans("", "", string.punctuation)
    words = [w.translate(translator) for w in words]


    # Make lower-case
    words = [w.lower() for w in words]

    # Remove english stop-words
    # words = [w for w in words if w not in stop_words]

    # Remove links
    def link(x):
        if ("http" in x) or ("www" in x):
            return "WEBSITE_TOKEN"
        else:
            return x
    words = [link(w) for w in words]

    # Remove numbers
    def number(x):
        if any(char.isdigit() for char in x) or ("½" in x):
            return "NUMBER_TOKEN"
        else:
            return x
    words = [number(w) for w in words]

    # Stemming / Lemmatizing
    # words = [stemmer.stem(w) for w in words]
    words = [lemmatizer.lemmatize(w) for w in words]

    # Remove empty elements, this is equivalent to
    # (item for item in iterable if item)
    words = list(filter(None, words))
    return words





def cleanup_string(initial_string):

    tokens = word_tokenize(initial_string)
    return cleanup_wordlist(tokens)


if (__name__ == "__main__"):
    final_data, final_labels, labels2names = load_csv2lists("final_dataset3.csv")
    for i in range(len(final_data)):
      final_data[i] = cleanup_string(final_data[i])
    for i in range(20):
      print(labels2names[final_labels[i]], final_data[i])

    pickle_object((final_data, final_labels, labels2names), "dataset_pickled.pkl")

    #test
    test = "Screw you @davidbrussee! I only have 3 weeks..."
    print(cleanup_wordlist(cleanup_string(test)))
