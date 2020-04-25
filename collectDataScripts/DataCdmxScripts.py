import requests
import json as js
from datetime import datetime
from dateutil import tz
import pprint
import copy
import pymongo


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("Á", "A"),
        ("É", "E"),
        ("Í", "I"),
        ("Ó", "O"),
        ("Ú", "U"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def getDataMetrobus():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["Metrobus"]
    mycol = mydb["Vehiculos"]

    # METHOD 2: Auto-detect zones:
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/Mexico_City')

    resp = requests.get('https://datos.cdmx.gob.mx/api/records/1.0/search/?dataset=prueba_fetchdata_metrobus&rows=1000')
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))

    dictResponse = resp.json()
    # for todo_item in resp.json():
    #     # print('{} {}'.format(todo_item['id'], todo_item['summary']))
    #     print(todo_item)

    records = copy.deepcopy(dictResponse["records"])

    for value in records:
        datetime_object = datetime.strptime(value["record_timestamp"], '%Y-%m-%dT%H:%M:%S.%f+00:00')
        # Tell the datetime object that it's in UTC time zone since 
        # datetime objects are 'naive' by default
        utc = datetime_object.replace(tzinfo=from_zone)
        # Convert time zone
        central = datetime_object.astimezone(to_zone)
        value["record_timestamp"] = str(central)

    x = mycol.insert_many(records)

    #print list of the _id values of the inserted documents:

    return x.inserted_ids


def getDataTownHall():

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["Metrobus"]
    mycol = mydb["Alcaldias"]


    resp = requests.get('https://datos.cdmx.gob.mx/api/records/1.0/search/?dataset=alcaldias&rows=100&facet=nomgeo&facet=cve_mun')
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))

    dictResponse = resp.json()
    # for todo_item in resp.json():
    #     # print('{} {}'.format(todo_item['id'], todo_item['summary']))
    #     print(todo_item)

    records = copy.deepcopy(dictResponse["records"])

    newRecord = []

    for x,value in enumerate(records):
        newRecord.append({
            "cve_mun"               : value["fields"]["cve_mun"],
            "cvegeo"                : value["fields"]["cvegeo"],
            "cve_ent"               : value["fields"]["cve_ent"],
            "nomgeo"                : normalize(value["fields"]["nomgeo"]),
            "record_timestamp"      : value["record_timestamp"],
            "geo_shape_coordinates" : value["fields"]["geo_shape"]["coordinates"]
        })
    
    x = mycol.insert_many(newRecord)

    return newRecord

getDataTownHall()