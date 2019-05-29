import xgboost as xgb
import numpy as np


class GBTrees(object):

    def __init__(self):
        self.initialize_default_parameters()
        self.model = None

    def initialize_default_parameters(self):


        # Set num rounds
        self.num_trees = 200

        # ------ Main parameters
        self.params = {}


        self.params["booster"] = "gbtree"

        # Set number of threads
        self.params["nthread"] = 10

        # set versobity
        self.params["silent"] = True
        # set number of classes
        self.params["num_class"] = 6

        # ------ Tree Boosting params

        self.params["eta"] = 0.3


        self.params["max_depth"] = 5

        # ------ Additional parameters

        self.params["objective"] = "multi:softmax"

    def train(self, X_train, Y_train, X_test=None, Y_test=None):

        # Wrap data into XBboost vars
        xg_train = xgb.DMatrix(X_train, label=Y_train)
        xg_test = xgb.DMatrix(X_test, label=Y_test)

        # Train
        watchlist = [(xg_train, "training_set"), (xg_test, "test_set")]
        self.model = xgb.train(self.params, xg_train, self.num_trees, watchlist)

    def predict(self, X_test):

        xg_test = xgb.DMatrix(X_test)
        return self.model.predict(xg_test)

    def get_accuracy(self, X_test, Y_test):

        pred = self.predict(X_test)
        error_rate = np.sum(pred != Y_test) / Y_test.shape[0]

        return error_rate

    def predict_from_sentence(self, document, text2features):

        bow_vector = text2features.raw_document2bow(document)
        return int(self.predict(bow_vector))
