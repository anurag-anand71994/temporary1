import pandas as pd
import pickle as pkl
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

prefix = "/data/container/data/"

def train():
    df_train = pd.read_csv(prefix + "SMS_train.csv" , encoding = "ISO-8859-1")
    df_test = pd.read_csv(prefix + "SMS_test.csv" , encoding = "ISO-8859-1")

    vectorizer = TfidfVectorizer()

    #create train vectors and labels
    xt = vectorizer.fit_transform(df_train['Message_body'])
    yt = df_train['Label']

    #create test vectors and labels
    xe = vectorizer.transform(df_test["Message_body"])
    ye = df_test['Label']

    #initialize and train model
    clf = LogisticRegression(random_state=0).fit(xt, yt)

    #outputs on test set
    op = clf.predict(xe)
    print(classification_report(ye, op))

    #save model and vectorizer
    with open(prefix + "vectorizer1.pk" , "wb") as pk :
        pkl.dump(vectorizer , pk)

    with open(prefix + "model1.pk" , "wb") as pk :
        pkl.dump(clf , pk)

if __name__=="__main__":
    train()