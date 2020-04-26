from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import pandas as pd
import pprint
import pymongo


def generateShapesByTownHall(df, nameColumnTown, nameColumnGeoShape):
    ''' Generate tuple list withe Name of Town hall and its polygon representation.
    
    Parameters:
        df (DataFrame): Town hall data, name and coordinates collection, which represent its area.
        nameColumnTown (str): Indicate the name column which represent town hall name
        nameColumnGeoShape (str): Indicate the name column which represent coordinates collection of Town hall.

    Returns:
        list: list of tuples (TownHall Name, polygon representation) 

    '''

    #Get list of coordinates collections
    shapesList = df[nameColumnGeoShape]

    #Get list TownHall names
    nameTownList = df[nameColumnTown].values
    listTuple = []

    #Convert coordinates collection to polygon shape and make tuple with the name of Townhall
    for x,y in enumerate(shapesList):
        listTuple.append((nameTownList[x],Polygon(y[0])))
    return listTuple

def getTownHall(lat,long,listTownHall):
    '''Return name of Town hall with a specific lat and long

    Paramters:
        lat: point latitude 
        long: point longitude
        listTownHall: List of tuple (Town hall name , polygon shape)

    Returns:
        str: Name of Town Hall 
    '''

    listTuple = listTownHall
    townHall = ""
    n = len(listTuple)-1
    for nom,polygon in listTuple:
        point = Point(long,lat)
        if polygon.contains(point):
            townHall = nom
    return townHall


#This method is used by Airflow python callable
def addTownHall():
    '''Add Town hall name in Metrobus Document saved in MongoDB

    Parameters:


    Returns:

    '''

    #Get Connection to mongoDB
    myclient = pymongo.MongoClient("mongodb://mongo:27017/")
    #Get or create data base and collection name
    mydb = myclient["Metrobus"]
    mycol_v = mydb["Vehiculos"]
    mycol_a = mydb["Alcaldias"]

    #Filter to get just the document without TownHall
    queryFilter = {"townHall":None}

    #Convert TownHall data to DataFrame 
    df = pd.DataFrame.from_dict(mycol_a.find())
    #Get listTuple of Name and polygin shape
    listTownHall = generateShapesByTownHall(df,"nomgeo","geo_shape_coordinates")
    #Get Metrbus data from MongoDB
    list_vi = list(mycol_v.find(queryFilter))

    #Update the record with TownHall data
    for dict_v in list_vi:
        lat = dict_v["fields"]["position_latitude"]
        lon = dict_v["fields"]["position_longitude"]
        dict_v["townHall"] = getTownHall(lat,lon,listTownHall)
        mycol_v.update({"_id":dict_v["_id"]},dict_v)