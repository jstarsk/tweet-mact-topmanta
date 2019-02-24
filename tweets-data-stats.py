import os
import numpy as np
import pandas as pd
import glob
from classifier import *

clf = SentimentClassifier()


def dir_os_db(wdir="db", os_system="WIN"):
    if os_system == "WIN":
        db_folder = "%s\\%s\\" % (os.getcwd(), wdir)
        db_csv = glob.glob("%s*.csv" % db_folder)
    elif os_system == "OSX":
        db_folder = "%s/%s/" % (os.getcwd(), wdir)
        db_csv = glob.glob("%s*.csv" % db_folder)
    else:
        db_folder = "%s/%s/" % (os.getcwd(), wdir)
        db_csv = glob.glob("%s*.csv" % db_folder)
    return db_csv


def sentiment_classifier_tweets():
    db_csv = dir_os_db(wdir="db", os_system='OSX')

    for db in db_csv:
        try:
            df = pd.read_csv(db)
            sentiment_classifier_score = []
            labels = []

            for index, row in df.iterrows():
                try:
                    score = 0.0
                    label = ""

                    if row['lang'] == "es":
                        score = round(clf.predict(row['text']), 3)
                        if score < 0.5:
                            label = 'NEG'
                        elif score > 0.5:
                            label = 'POS'
                        else:
                            label = 'NEU'
                    elif row['lang'] == "ca":
                        score = round(clf.predict(row['text']), 3)
                        if score < 0.5:
                            label = 'NEG'
                        elif score > 0.5:
                            label = 'POS'
                        else:
                            label = 'NEU'
                    elif row['lang'] == "en":
                        score = round(clf.predict(row['text']), 3)
                        if score < 0.5:
                            label = 'NEG'
                        elif score > 0.5:
                            label = 'POS'
                        else:
                            label = 'NEU'
                    else:
                        score = round(clf.predict(row['text']), 3)
                        if score < 0.5:
                            label = 'NEG'
                        elif score > 0.5:
                            label = 'POS'
                        else:
                            label = 'NEU'

                    sentiment_classifier_score.append(score)
                    labels.append(label)
                    print(row['text'] + ' ==> %.5f ==> %s' % (score, label))

                except Exception as e:
                    print(e)
                    pass

            series_sentiment_classifier_score = pd.Series(sentiment_classifier_score)
            series_label = pd.Series(labels)

            df['sentiment_classifier_score'] = series_sentiment_classifier_score.values
            df['label'] = series_label.values

            df.to_csv(db, index=False)

        except Exception as e:
            print(db)
            print(e)


if __name__ == "__main__":
    sentiment_classifier_tweets()
