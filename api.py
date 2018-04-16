from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import os.path

dbfile = '/app/database.db'

if not os.path.isfile(dbfile):
    db_connect =  create_engine('sqlite:///' + dbfile)
    query = conn.execute("CREATE TABLE nodes(nodeid TEXT, latitude NUMERIC, longitude NUMERIC, status NUMERIC, dateadded DATE);")
    query = conn.execute("CREATE TABLE strikes(nodeid TEXT, date DATE, distance NUMERIC);")
    query = conn.execute("CREATE TABLE power(nodeid TEXT, date DATE, volts NUMERIC, amps NUMERIC, watts NUMERIC);")
    query = conn.execute("CREATE TABLE multisensor(nodeid TEXT, date DATE, humidity NUMERIC, pressure NUMERIC, temperature NUMERIC);")

db_connect = create_engine('sqlite:///' + dbfile)
app = Flask(__name__)
api = Api(app)

def dbcon():
    try:
        conn = db_connect.connect()
    except Exception as e:
        return {'error':'could not connect to database')

class Register(Resource):
    def get(self):
        conn = db_connect.connect():
        query = conn.execute("select MAX(nodeid) from nodes")
        query += 1
		return {'id':query}

class NodesList(Resource):
    def get(self):
        dbcon()
		try:
            query = conn.execute("select * from nodes")
            return {'nodes': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor.fetchall()]}
		except Exception as e:
            return {'error':'no nodes found'}

    def post(self):
        dbcon()
        #print(request.json)
        nodeid = request.json['nodeid']
        latitude = request.json['lattitude']
        longitude = request.json['longitude']
        status = request.json['status']
        dateadded = request.json['dateadded']
        try:
            query = conn.execute("insert into nodes values('{0}', '{1}', '{2}', '{3}', '{4}')".format(nodeid, latitude, longitude, status, dateadded))
            return {'status':'success'}
        except Exception as e:
            return {'error':e}

class Nodes(Resource):
    def get(self, nodeid):
        dbcon()
        try:
            query = conn.execute("select * from nodes where nodeid = '" + nodeid + "';")
            return {nodeid : [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor.fetchall()]}
        except Exception as e:
            return {'error':nodeid + ' not found'}

    def delete(self, nodeid):
        dbcon()
        try:
            query = conn.execute("delete from nodes where nodeid = '" + nodeid + "';")
            return {'status':'succcess'}
        except Exception as e:
            return {'error':nodeid + ' not found'}


class Strikes(Resource):
    def get(self, nodeid):
        dbcon()
        try:
            query = conn.execute("select * from strikes where nodeid = '" + nodeid + "';")
            return {'strikes': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor.fetchall()]}
        except Exception as e:
            return {'error':nodeid + ' not found'}


    def post(self, nodeid):
        dbcon()
        print(request.json)
        date = request.json['date']
        distance = request.json['distance']
        try:
            query = conn.execute("insert into strikes values('{0}', '{1}', '{2}')".format(nodeid, date, distance))
            return {'status':'success'}
        except Exception as e:
            return {'error':nodeid + ' not found'}


class Multidata(Resource):
    def get(self, nodeid):
        dbcon()
        try:
            query = conn.execute("select date, humidity, pressure, temperature from multisensor where nodeid = '" + nodeid + "';")
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return jsonify(result)
        except Exception as e:
            return {'error':nodeid + ' not found'}

    def post(self, nodeid):
        dbcon()
        print(request.json)
        date = request.json['date']
        humidity = request.json['humidity']
        pressure = request.json['pressure']
        temperature = request.json['temperature']
        try:
            query = conn.execute("insert into multisensor values('{0}', '{1}', '{2}', '{3}', '{4}')".format(nodeid, date, humidity, pressure, temperature))
            return {'status':'success'}
        except Exception as e:
            return {'error':nodeid + ' not found'}

class Power(Resource):
    def get(self, nodeid):
        dbcon()
        try:
            query = conn.execute("select * from power " + nodeid + ";")
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return jsonify(result)
        except Exception as e:
             return {'error':nodeid + ' not found'}

    def post(self, nodeid):
        dbcon()
        #print(request.json)
        date = request.json['date']
        volts = request.json['volts']
        amps = request.json['amps']
        watts = request.json['watts']
        try:
            query = conn.execute("insert into power values('{0}', '{1}', '{2}', '{3}', '{4}')".format(nodeid, date, volts, amps, watts))
            return {'status':'success'}
        except Exception as e:
            return {'error':nodeid + ' not found'}


api.add_resource(Register, '/register')
api.add_resource(NodesList, '/nodes')
api.add_resource(Nodes, '/nodes/<nodeid>')
api.add_resource(Strikes, '/nodes/<nodeid>/strikes')
api.add_resource(Multidata, '/nodes/<nodeid>/multidata')
api.add_resource(Power, '/nodes/<nodeid>/power')


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8081)
