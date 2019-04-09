import pickle
import nltk
# import os
# currentPath = os.getcwd()

#change path
# os.chdir('/content/gdrive/My Drive/sentiment/')
nltk.download('wordnet')
nltk.download('stopwords')
filename = "dataset/test_dataset_bow.pkl"
with open(filename, "rb") as fp:
  X_test, Y_test, labels2names, text2features = pickle.load(fp)


filename = "trained_model_gboost.pkl"
with open(filename, "rb") as fp:
    net = pickle.load(fp)

print(net)
print("Test error using softmax = {}".format(net.get_accuracy(X_test, Y_test)))
print(labels2names[net.predict_from_sentence("dude, that is my favorite sandwich place ever. ummm did you take PICTURES?".split(), text2features)])
