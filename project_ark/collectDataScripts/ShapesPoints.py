from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import pandas as pd
import pprint
import pymongo


def generateShapesByTownHall(df, nameColumnTown, nameColumnGeoShape):
    shapesList = df[nameColumnGeoShape]
    nameTownList = df[nameColumnTown].values
    listTuple = []
    for x,y in enumerate(shapesList):
        listTuple.append((nameTownList[x],Polygon(y[0])))
    return listTuple

def getListGeoShapes(array):
    keyList="coordinates"
    dictx = eval(array)
    return dictx[keyList][0]

def getTownHall(lat,long,listTownHall):
    listTuple = listTownHall
    townHall = ""
    n = len(listTuple)-1
    for nom,polygon in listTuple:
        point = Point(long,lat)
        if polygon.contains(point):
            townHall = nom
    return townHall

def addTownHall():
    myclient = pymongo.MongoClient("mongodb://mongo:27017/")
    mydb = myclient["Metrobus"]
    mycol_v = mydb["Vehiculos"]
    queryFilter = {"townHall":None}

    mydb = myclient["Metrobus"]
    mycol_a = mydb["Alcaldias"]
    df = pd.DataFrame.from_dict(mycol_a.find())
    listTownHall = generateShapesByTownHall(df,"nomgeo","geo_shape_coordinates")
    list_vi = list(mycol_v.find(queryFilter))

    for dict_v in list_vi:
        lat = dict_v["fields"]["position_latitude"]
        lon = dict_v["fields"]["position_longitude"]
        dict_v["townHall"] = getTownHall(lat,lon,listTownHall)
        pprint.pprint(mycol_v.update({"_id":dict_v["_id"]},dict_v))    