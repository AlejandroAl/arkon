import requests
import json as js
from datetime import datetime
from dateutil import tz
import pprint
import copy
import pymongo



def normalize(s):
    ''' Convert string with stress values to strigt without them

    Parameters:
    s (str): String of characteres

    Returns:
    str: string without stress values

    '''
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


#This method is used by Airflow PythonOperator, it is the reason to doesnt return value
def getDataMetrobus():
    '''Get Data from Metrobus CDMX data and save in MongoDB

    Parameters:

    Returns:

    '''

    #Get Client to connect mongo
    myclient = pymongo.MongoClient("mongodb://mongo:27017/")

    #Create or get DataBase and collection from monboDB
    mydb = myclient["Metrobus"]
    mycol = mydb["Vehiculos"]

    # Get timezone Mexico city to save datatime UTC-5
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/Mexico_City')

    #Define request to get date from CDMX page
    resp = requests.get('https://datos.cdmx.gob.mx/api/records/1.0/search/?dataset=prueba_fetchdata_metrobus&rows=1000')

    #Get response result
    dictResponse = resp.json()

    #Get records from request and create copy, which it allows us dont modify the rest collection data
    records = copy.deepcopy(dictResponse["records"])

    #
    for value in records:
        datetime_object = datetime.strptime(value["record_timestamp"], '%Y-%m-%dT%H:%M:%S.%f+00:00')
        # Tell the datetime object that it's in UTC time zone since 
        # datetime objects are 'naive' by default
        utc = datetime_object.replace(tzinfo=from_zone)
        # Convert time zone
        central = datetime_object.astimezone(to_zone)
        #change datetime to central datetime
        value["record_timestamp"] = str(central)

    #Save data MongoDB
    x = mycol.insert_many(records)


#This method is used by Airflow PythonOperator, it is the reason to doesnt return value
def getDataTownHall():
    '''Get Data from "Alcaldias" CDMX data and save in MongoDB

    Parameters:

    Returns:

    '''

    #Get Client to connect mongo
    myclient = pymongo.MongoClient("mongodb://mongo:27017/")
    #Create or get DataBase and collection from monboDB
    mydb = myclient["Metrobus"]
    mycol = mydb["Alcaldias"]

    #Define request to get date from CDMX page
    resp = requests.get('https://datos.cdmx.gob.mx/api/records/1.0/search/?dataset=alcaldias&rows=100&facet=nomgeo&facet=cve_mun')

    #Get response result
    dictResponse = resp.json()
    #Get records from request and create copy, which it allows us dont modify the rest collection data
    records = copy.deepcopy(dictResponse["records"])

    newRecord = []

    #Create set specific set of data from records 
    for x,value in enumerate(records):
        newRecord.append({
            "cve_mun"               : value["fields"]["cve_mun"],
            "cvegeo"                : value["fields"]["cvegeo"],
            "cve_ent"               : value["fields"]["cve_ent"],
            "nomgeo"                : normalize(value["fields"]["nomgeo"]),
            "record_timestamp"      : value["record_timestamp"],
            "geo_shape_coordinates" : value["fields"]["geo_shape"]["coordinates"]
        })
    #Save data MongoDB
    x = mycol.insert_many(newRecord)