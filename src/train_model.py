import pickle
import sentiment_toolkit.model_gboost as st
import nltk
nltk.download('stopwords')


filename = "dataset/train_dataset_bow.pkl"
with open(filename, "rb") as fp:
    X_train, Y_train, labels2names, text2features = pickle.load(fp)

filename = "dataset/test_dataset_bow.pkl"
with open(filename, "rb") as fp:
    X_test, Y_test, labels2names, text2features = pickle.load(fp)


xbg_model = st.GBTrees()
xbg_model.train(X_train, Y_train, X_test, Y_test)

filename = "trained_model_gboost.pkl"
with open(filename, "wb") as fp:
    pickle.dump(xbg_model, fp)
