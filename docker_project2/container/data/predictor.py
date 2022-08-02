import os
import pandas as pd
#import pickle as pkl
import flask

import io
import json
import os
import pickle
import signal
import sys
import traceback

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

prefix = "/data/container/data/"
model_path = os.path.join(prefix, "model1.pk")
vectorizer_path = os.path.join(prefix, "vectorizer1.pk")

class ScoringService(object):
    model = None  # Where we keep the model when it's loaded
    vectorizer = None

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model == None:
            with open(model_path, "rb") as inp:
                cls.model = pickle.load(inp)
        if cls.vectorizer == None:
            with open(vectorizer_path, "rb") as inp:
                cls.vectorizer = pickle.load(inp)
        return cls.model,cls.vectorizer

    @classmethod
    def predict(cls, input):
        """For the input, do the predictions and return them.
        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        clf,vectorizer = cls.get_model()
        return clf.predict(vectorizer.transform(input))

# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = ScoringService.get_model() is not None  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response="\n", status=status, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None

    # Convert from CSV to pandas
    print(flask.request.content_type)
    if flask.request.content_type == "text/csv":
        data = flask.request.data.decode("utf-8")
        s = io.StringIO(data)
        data = pd.read_csv(s, header=None)
    elif flask.request.content_type == "application/json":
        data = eval(flask.request.data)["data"]
        print(data)
    elif flask.request.content_type == "list":
        data = flask.request.data
    else:
        return flask.Response(
            response="This predictor only supports CSV data", status=415, mimetype="text/plain"
        )

    #print("Invoked with {} records".format(data.shape[0]))

    # Do the prediction
    predictions = ScoringService.predict(data)

    # Convert from numpy back to CSV
    out = io.StringIO()
    pd.DataFrame({"results": predictions}).to_csv(out, header=False, index=False)
    result = out.getvalue()

    return flask.Response(response=result, status=200, mimetype="text/csv")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8090)
