import os
import numpy as np
import pandas as pd
import glob
from geojson import Point, Feature, LineString, Polygon


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


def normalize(value, old_min, old_max, new_min, new_max):
    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    return (((value - old_min) * new_range) / old_range) + new_min


def classifier_search_tweets_loc():
    type_os = 'OSX'

    db_csv = dir_os_db(wdir="db_input", os_system=type_os)

    _search_tweets_loc = []

    for db in db_csv:
        try:
            df = pd.read_csv(db)

            list_counter_NEG = []
            list_counter_POS = []
            nor_list_counter_NEG = []
            nor_list_counter_POS = []

            for index, row in df.iterrows():
                try:
                    str_coordinates_lon = str.split(str(row['LONGITUD']), ".")
                    coordinates_lon = float("%s.%s" % (str_coordinates_lon[0], str_coordinates_lon[1][0:2]))
                    str_coordinates_lat = str.split(str(row['LATITUD']), ".")
                    coordinates_lat = float("%s.%s" % (str_coordinates_lat[0], str_coordinates_lat[1][0:2]))

                    _db_csv = dir_os_db(wdir="db", os_system=type_os)

                    _counter_NEG = 0
                    _counter_POS = 0

                    for _db in _db_csv:
                        try:
                            _df = pd.read_csv(_db)

                            for _index, _row in _df.iterrows():
                                try:
                                    _str_coordinates_lon = str.split(str(_row['_search_loc_lon']), ".")
                                    _coordinates_lon = float(
                                        "%s.%s" % (_str_coordinates_lon[0], _str_coordinates_lon[1][0:2]))
                                    _str_coordinates_lat = str.split(str(_row['_search_loc_lat']), ".")
                                    _coordinates_lat = float(
                                        "%s.%s" % (_str_coordinates_lat[0], _str_coordinates_lat[1][0:2]))

                                    if coordinates_lon == _coordinates_lon and \
                                            coordinates_lat == _coordinates_lat:

                                        if _row['label'] == "NEG":
                                            _counter_NEG += 1
                                        elif _row['label'] == "POS":
                                            _counter_POS += 1
                                except Exception as e:
                                    print(e, "-------")

                        except Exception as e:
                            print(e)

                    print("Counter | POS & NEG  ==> NEG: %d - POS: %d - Place: %s, " % (
                        _counter_NEG, _counter_POS, row['EQUIPAMENT']))
                    list_counter_NEG.append(_counter_NEG)
                    list_counter_POS.append(_counter_POS)

                except Exception as e:
                    print("%s: this search tweets has not localization" % e)

            series_counter_NEG = pd.Series(list_counter_NEG)
            series_counter_POS = pd.Series(list_counter_POS)

            df['counter_NEG'] = series_counter_NEG.values
            df['counter_POS'] = series_counter_POS.values
            df.to_csv(db, index=False)

            print("--------------------------------------------------------------------------")

            max_NEG = series_counter_NEG.max()
            max_POS = series_counter_POS.max()
            max_value = max_NEG + max_POS

            print(max_value)

            for index, row in df.iterrows():

                try:
                    nor_counter_NEG = int(normalize(int(row["counter_NEG"]), 0, max_value, 0, 100))
                    nor_counter_POS = int(normalize(int(row["counter_POS"]), 0, max_value, 0, 100))
                except Exception as e:
                    nor_counter_NEG = 0
                    nor_counter_POS = 0
                    print(e)

                if nor_counter_NEG == 0 and nor_counter_POS == 0:
                    nor_counter_POS = 0
                else:
                    nor_counter_POS = abs(100 - nor_counter_NEG)

                nor_list_counter_NEG.append(nor_counter_NEG)
                nor_list_counter_POS.append(nor_counter_POS)

                print("Normalization | POS & NEG ==> nor_NEG: %d - nor_POS: %d - Place: %s" %
                      (nor_counter_NEG, nor_counter_POS, row['EQUIPAMENT']))

            series_nor_counter_NEG = pd.Series(nor_list_counter_NEG)
            series_nor_counter_POS = pd.Series(nor_list_counter_POS)

            df['nor_counter_NEG'] = series_nor_counter_NEG.values
            df['nor_counter_POS'] = series_nor_counter_POS.values

            df.to_csv(db, index=False)


        except Exception as e:
            print(e)

    dir_os_db(wdir="db", os_system=type_os)

    _tweets_with_locations = []
    _tweets_without_locations = []


if __name__ == "__main__":
    classifier_search_tweets_loc()
