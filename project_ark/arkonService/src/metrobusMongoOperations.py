import pymongo


# Let get specific Metrobus unit data
def getSpecificData(data, th=True):
    '''

    :param data:dict
    :return:
        dict: {vehicle_id: "", vehicle_label:"" , townHall:"" }
    '''

    record = data["fields"]
    new_dict_record = {}
    new_dict_record["vehicle_id"] = record["vehicle_id"]
    new_dict_record["vehicle_label"] = record["vehicle_label"]
    if th:
        new_dict_record["townHall_position"] = data["townHall"]

    return new_dict_record


# Let get specific Metrobus unit data
def getListDetails(data):
    '''

    :param data:dict
    :return:
        dict: {vehicle_id: "", vehicle_label:"" , townHall:"" }
    '''

    record = data["fields"]
    new_dict_record = {}

    date_ = record["date_updated"]

    new_dict_record[date_] = {}
    new_dict_record[date_]["position_longitude"] = record["position_longitude"]
    new_dict_record[date_]["position_latitude"] = record["position_latitude"]
    new_dict_record[date_]["townHall_position"] = data["townHall"]

    return new_dict_record





def getAvailableUnits():
    ''' Get units availables

    :parameters

    :return:
        dict: Metrobus units without trip

    '''

    # Get Connection to mongoDB
    myclient = pymongo.MongoClient("mongodb://mongo:27017/")
    # Get or create data base and collection name
    mydb = myclient["Metrobus"]
    mycol_v = mydb["Vehiculos"]
    query_filter ={ "fields.trip_start_date" : None }
    #Get data from mongo
    data = list(mycol_v.find(query_filter))

    list_records = list(map(lambda x: getSpecificData(x), data))

    return list_records



def detailsByID(id):
    '''
    :param id:
    :return:
    '''

    # Get Connection to mongoDB
    myclient = pymongo.MongoClient("mongodb://mongo:27017/")
    # Get or create data base and collection name
    mydb = myclient["Metrobus"]
    mycol_v = mydb["Vehiculos"]
    query_filter = {"fields.vehicle_id": str(id)}
    # Get data from mongo
    data = list(mycol_v.find(query_filter))

    print(data)

    list_records = list(map(lambda x: getListDetails(x), data))

    return list_records



def getlistTownHall():
    '''
    :param id:
    :return:
    '''

    # Get Connection to mgetAvailableUnitsongoDB
    myclient = pymongo.MongoClient("mongodb://mongo:27017/")
    # Get or create data base and collection name
    mydb = myclient["Metrobus"]
    mycol_v = mydb["Vehiculos"]
    query_filter =  [
        {"$match": {
            "fields.trip_start_date":{"$ne":None}
            }
            },
        {
            "$group": {
                "_id": "$townHall",
                "count": { "$sum": 1 }
                }
            }
        ]

    print(query_filter)
    # Get data from mongo
    data = list(mycol_v.aggregate(query_filter))

    print(data)

    return data


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


def metrobusUnitsByTownHall(townHall):
    '''
    :param id:
    :return:
    '''

    # Get Connection to mgetAvailableUnitsongoDB
    myclient = pymongo.MongoClient("mongodb://mongo:27017/")
    # Get or create data base and collection name
    mydb = myclient["Metrobus"]
    mycol_v = mydb["Vehiculos"]
    query_filter ={"townHall": normalize(townHall)}

    print(query_filter)
    # Get data from mongo
    data = list(mycol_v.find(query_filter))

    list_records = list(map(lambda x: getSpecificData(x,False), data))

    return list_records


