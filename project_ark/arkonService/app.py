from flask import Flask
from flask import request
import os
from src import metrobusMongoOperations as mb

app = Flask(__name__)
port = os.getenv("SERVICE_PORT")

@app.route('/getAvailableUnits', methods=["GET"])
def getAvailableUnits():
    listData = mb.getAvailableUnits()
    return {"AvailableUnitsList": listData}

@app.route('/metrobusDetailsById', methods=["GET"])
def detailsByID():
    id = request.args.get('ID')
    listData = mb.detailsByID(id)
    return {id: listData}


@app.route('/getlistTownHalls', methods=["GET"])
def getlistTownHall():
    listData = mb.getlistTownHall()
    return {"TownHallsList": listData}


@app.route('/metrobusUnitsByTownHall', methods=["POST"])
def metrobusUnitsByTownHall():
    id = request.get_json()
    listData = mb.metrobusUnitsByTownHall(id["TH"])
    return {id["TH"]: listData}



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
