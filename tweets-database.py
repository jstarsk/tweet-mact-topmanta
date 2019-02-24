import os
import ast
import time
import datetime
from time import gmtime, strftime
import twitter
import csv
import pandas as pd


def fetched_tweets_by_hashtags(_search_string, _count, _loc, _loc_range):
    try:
        _gecode = "%f,%f,%dkm" % (_loc[0], _loc[1], _loc_range)
        tweets_fetched = api.GetSearch(_search_string, count=_count, geocode=_gecode)
        print("Great! We fetched " + str(len(tweets_fetched)) + " tweets with the term " + _search_string + "!!")
        print("---")

        _tweets_fetched = []

        for tweet in tweets_fetched:
            dict_tweet = {}

            # _SEARCH STRING
            try:
                dict_tweet["_search_string"] = _search_string
            except Exception as e:
                print("Sorry there was an error on the _search_string!")
                dict_tweet["_search_string"] = str(None)

            # _SEARCH LOC_LAT
            try:
                dict_tweet["_search_loc_lat"] = _loc[0]
            except Exception as e:
                print("Sorry there was an error on the _search_loc_lat!")
                dict_tweet["_search_loc_lat"] = str(None)

            # _SEARCH LOC_LON
            try:
                dict_tweet["_search_loc_lon"] = _loc[1]
            except Exception as e:
                print("Sorry there was an error on the _search_loc_lon!")
                dict_tweet["_search_loc_lon"] = str(None)

            # _SEARCH LOC_RANGE
            try:
                dict_tweet["_search_loc_range"] = _loc_range
            except Exception as e:
                print("Sorry there was an error on the _search_loc_range!")
                dict_tweet["_search_loc_range"] = str(None)

            # ID
            try:
                dict_tweet["id"] = tweet.id
            except Exception as e:
                print("Sorry there was an error on the tweet.id!")
                dict_tweet["id"] = str(None)

            # TEXT
            try:
                # Remove all newlines from inside a string
                _text = tweet.text.replace("\n", " - ")
                dict_tweet["text"] = _text
            except Exception as e:
                print("Sorry there was an error on the tweet.text!")
                dict_tweet["text"] = str(None)

            # USER ID
            try:
                dict_tweet["user_id"] = tweet.user.id
            except Exception as e:
                print("Sorry there was an error on the tweet.user_id!")
                dict_tweet["user_id"] = str(None)

            #  CREATE_AT
            try:
                dict_tweet["created_at"] = tweet.created_at
            except Exception as e:
                print("Sorry there was an error on the tweet.created_at!")
                dict_tweet["created_at"] = str(None)

            # LANGUAGE
            try:
                dict_tweet["lang"] = tweet.lang
            except Exception as e:
                print("Sorry there was an error on the tweet.lang!")
                dict_tweet["lang"] = str(None)

            # COORDINATES - TYPE
            try:
                dict_tweet["coordinates_type"] = tweet.coordinates["type"]
            except Exception as e:
                print("Sorry there was an error on the tweet.coordinates.type!")
                dict_tweet["coordinates_type"] = str(None)

            # COORDINATES - LAT
            try:
                dict_tweet["coordinates_lat"] = tweet.coordinates["coordinates"][1]
            except Exception as e:
                print("Sorry there was an error on the tweet.coordinates.coordinates[1]!")
                dict_tweet["coordinates_lat"] = str(None)

            # COORDINATES - LON
            try:
                dict_tweet["coordinates_lon"] = tweet.coordinates["coordinates"][0]
            except Exception as e:
                print("Sorry there was an error on the tweet.coordinates.coordinates[0]!")
                dict_tweet["coordinates_lon"] = str(None)

            # PLACE - ID
            try:
                dict_tweet["place_id"] = tweet.place["id"]
            except Exception as e:
                print("Sorry there was an error on the tweet.place.id!")
                dict_tweet["place_id"] = str(None)

            # PLACE - TYPE
            try:
                dict_tweet["place_type"] = tweet.place["place_type"]
            except Exception as e:
                print("Sorry there was an error on the tweet.place.place_type!")
                dict_tweet["place_type"] = str(None)

            # PLACE - NAME
            try:
                dict_tweet["place_name"] = tweet.place["place_name"]
            except Exception as e:
                print("Sorry there was an error on the tweet.place.place_name!")
                dict_tweet["place_name"] = str(None)

            # PLACE - COUNTRY_CODE
            try:
                dict_tweet["place_country_code"] = tweet.place["country_code"]
            except Exception as e:
                print("Sorry there was an error on the tweet.place.country_code!")
                dict_tweet["place_country_code"] = str(None)

            # RETWEET COUNT
            try:
                dict_tweet["retweet_count"] = tweet.retweet_count
            except Exception as e:
                print("Sorry there was an error on the tweet.retweet_count!")
                dict_tweet["retweet_count"] = str(None)

            # FAVORITE COUNT
            try:
                dict_tweet["favorite_count"] = tweet.favorite_count
            except Exception as e:
                print("Sorry there was an error on the tweet.favorite_count!")
                dict_tweet["favorite_count"] = str(None)

            dict_tweet["label"] = str(None)

            _tweets_fetched.append(dict_tweet)

        return _tweets_fetched
    except Exception as e:
        print("==========================================================================")
        print("Sorry there was an error! %s" % (ast.literal_eval(str(e))[0]["message"]))
        return [int(ast.literal_eval(str(e))[0]["code"])]


def create_data_base(path_db, _tweets_data, search_topic):
    csv_file_fetched_tweets = "%s/fetched_tweets_by_%s.%s" % (path_db, search_topic, "csv")

    with open(csv_file_fetched_tweets, 'a') as csv_file:
        line_writer = csv.writer(csv_file, delimiter=',', quotechar="\"")
        for tweet in _tweets_data:
            try:
                line_writer.writerow(
                    [tweet["id"],
                     tweet["created_at"],
                     tweet["user_id"],
                     tweet["text"],
                     tweet["lang"],
                     tweet["coordinates_type"],
                     tweet["coordinates_lat"],
                     tweet["coordinates_lon"],
                     tweet["place_id"],
                     tweet["place_name"],
                     tweet["place_country_code"],
                     tweet["retweet_count"],
                     tweet["favorite_count"],
                     tweet["_search_string"],
                     tweet["_search_loc_lat"],
                     tweet["_search_loc_lon"],
                     tweet["_search_loc_range"],
                     tweet["label"],
                     ])
            except Exception as e:
                print(e)
    return _tweets_data


if __name__ == "__main__":

    api = twitter.Api(consumer_key='CaNf7S5GwXomvr9yJrAqSzLuw',
                      consumer_secret='GG7g28L4r77c5Efw77KbgUaKgiLK32GT4yTfefGcAtyeTBoS7V',
                      access_token_key='1057316422869757952-TvUn2pUMl4352lwxJPOJymNdIfkeN7',
                      access_token_secret='V0XB9cGTBCQwLUOSnNzIbWltpClTrvQ0uJBkohJnSPfY3')

    db_folder = "%s/db/" % (os.getcwd())

    trigger_times = [{"date": "2019-02-20",
                      "hour": "18:46"},
                     {"date": "2019-02-20",
                      "hour": "18:50"}
                     ]

    interest_point = pd.read_csv("%s/db_input/Transports.csv" % (os.getcwd()))

    search_topics = ["#TransportPublic", "#Catalonia", "#FreeToThom", "#NoSurrender", "#CataloniaRepublic",
                     "#Makeamove", "#WakeUpEurope", "bcitnews", "#freedomcatalonia", "#TMB_Barcelona",
                     "#metrobarcelona", "#ConstrumatBCN"]

    print("--------------------------------------------------------------------------")
    print("Twitter - DATABASE")
    print("--------------------------------------------------------------------------")
    is_stop = False
    counter = 0

    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    current_time = current_time.split(" ")

    if current_time == current_time:
        try:
            print("Algorithm is trigger at %s %s" % (current_time[0], current_time[1]))
            print("--------------------------------------------------------------------------")
            for index, row in interest_point.iterrows():
                # print(list(df_interest_point.columns.values))
                _coordinates = [row['LATITUD'], row['LONGITUD']]
                _place = row['EQUIPAMENT']
                data2search = _place.split(" ")
                if "FGC" not in data2search:
                    _search_radius = 1
                    print("Algorithm is searching at " + _place + " with a radius of search of " + str(
                        _search_radius) + " km")
                    for topic in search_topics:
                        tweets_data = fetched_tweets_by_hashtags(topic, 50, _coordinates, _search_radius)
                        if tweets_data != [88]:
                            create_data_base(db_folder, tweets_data, topic)
                        else:
                            print("Algorithm need to sleep for 15 min")
                            print("==========================================================================")
                            time.sleep(16 * 60)

        except Exception as e:
            print(e)
