import os
import pandas as pd
import glob
from geojson import Point, Feature, LineString, Polygon
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

# WINDOWS USERS
MAPBOX_ACCESS_KEY = 'pk.eyJ1Ijoic3RhcnNrIiwiYSI6ImNqcW1uYThkcjB5OXU0MnFuMmNsd2F6bm4ifQ.UVn8HyKNEtPabiMlYwJfPw'

# LINUX MAC USERS
# app.config.from_envvar('APP_CONFIG_FILE', silent=True)
# MAPBOX_ACCESS_KEY = app.config[MAPBOX_ACCESS_KEY]

map_center = [41.3851, 2.1734]
map_zoom = 11


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


def add_fetched_tweets_loc():
    db_csv = dir_os_db(wdir="db", os_system='WIN')

    _tweets_with_locations = []
    _tweets_without_locations = []

    for db in db_csv:
        try:
            df = pd.read_csv(db)

            for index, row in df.iterrows():
                try:
                    coordinates_lon = float(row['coordinates_lon'])
                    coordinates_lat = float(row['coordinates_lat'])
                    loc_range = 0.04
                    opacity = 0.03

                    point = Point((coordinates_lon, coordinates_lat))
                    properties_point = {
                        'title': row['place_name'],
                        'diameter': loc_range,
                        'opacity': opacity,
                        'sentiment_classifier_score': row['sentiment_classifier_score'],
                        'label': row['label'],
                        'created_at': row['created_at'],
                        'coordinates_type': row['coordinates_type'],
                        'place_name': row['place_name'],
                        'retweet_count': row['retweet_count'],
                        'favorite_count': row['favorite_count'],
                        '_search_string': row['_search_string'],
                    }

                    feature_point = Feature(geometry=point, properties=properties_point)

                    _tweets_with_locations.append(feature_point)

                except Exception as e:
                    coordinates_lon = float(row['_search_loc_lon'])
                    coordinates_lat = float(row['_search_loc_lat'])
                    loc_range = float(row['_search_loc_range'])
                    opacity = 1

                    point = Point((coordinates_lon, coordinates_lat))
                    properties_point = {
                        'title': row['place_name'],
                        'diameter': loc_range,
                        'opacity': opacity,
                        'sentiment_classifier_score': row['sentiment_classifier_score'],
                        'label': row['label'],
                        'created_at': row['created_at'],
                        'coordinates_type': row['coordinates_type'],
                        'place_name': row['place_name'],
                        'retweet_count': row['retweet_count'],
                        'favorite_count': row['favorite_count'],
                        '_search_string': row['_search_string'],
                    }

                    feature_point = Feature(geometry=point, properties=properties_point)

                    _tweets_without_locations.append(feature_point)
                    # print("%s: this tweets has not localization" % e)

        except Exception as e:
            print(e)

    return {"with_locations": _tweets_with_locations, "without_locations": _tweets_without_locations}


def add_search_tweets_loc():
    db_csv = dir_os_db(wdir="db_input", os_system='WIN')

    _search_tweets_loc = []

    for db in db_csv:
        try:
            df = pd.read_csv(db)

            for index, row in df.iterrows():
                try:
                    coordinates_lon = float(row['LONGITUD'])
                    coordinates_lat = float(row['LATITUD'])
                    counter_POS = int(row['counter_POS'])
                    counter_NEG = int(row['counter_NEG'])
                    nor_counter_NEG = float(row['nor_counter_NEG'])
                    nor_counter_POS = float(row['nor_counter_POS'])
                    loc_range = 0.04
                    opacity = 1
                    color = "#000000"

                    _place = row['EQUIPAMENT']
                    data2search = _place.split(" ")
                    if "FGC" not in data2search:

                        if counter_POS > counter_NEG:
                            color = '#FF0000'
                        elif counter_POS < counter_NEG:
                            color = '#00FF00'
                        else:
                            color = '#FFFF00'

                        point = Point((coordinates_lon, coordinates_lat))
                        properties_point = {
                            'title': _place,
                            'diameter': loc_range,
                            'opacity': opacity,
                            'counter_POS': counter_POS,
                            'counter_NEG': counter_NEG,
                            'nor_counter_NEG': nor_counter_NEG,
                            'nor_counter_POS': nor_counter_POS,
                            '_color': color
                        }

                        feature_point = Feature(geometry=point, properties=properties_point)

                        _search_tweets_loc.append(feature_point)

                except Exception as e:
                    print("%s: this search tweets has not localization" % e)

        except Exception as e:
            print(e)

    return {"with_locations": _search_tweets_loc}


@app.route('/twitter_map')
def mapbox_js():
    tweets_locations = add_fetched_tweets_loc()
    search_locations = add_search_tweets_loc()
    return render_template(
        'twitter_map.html',
        ACCESS_KEY=MAPBOX_ACCESS_KEY,
        center_lat=map_center[0],
        center_lon=map_center[1],
        map_zoom=map_zoom,
        _tweets_with_locations=tweets_locations["with_locations"],
        _tweets_without_locations=tweets_locations["without_locations"],
        _search_locations=search_locations['with_locations']
    )


if __name__ == "__main__":
    app.run()
