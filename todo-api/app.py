from flask import Flask, jsonify, request
from extensions import CORS
# from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
CORS.init_app(app)

# app.config["MONGO_URI"] = f'mongodb://admin:admin@' + os.environ['MONGO_HOST'] + ':27017/todo-db'

# mongo = PyMongo(app)

def getDB():
  client = MongoClient(
    host=os.environ['MONGO_HOST'],
    port=27017,
    username='admin',
    password='admin',
    authSource='admin'
  )
  db = client['todo-db']
  return db

@app.route('/', methods=["GET"])
def getTodos():
  try:
    collection = getDB().todo.find()
    response = []
    for c in collection:
      c['_id'] = str(c['_id'])
      response.append(c)
    return jsonify(response), 200
  except Exception as e:
    print(str(e))
    return jsonify({"message": "Error!"}), 500

@app.route('/add', methods=["POST"])
def addTodos():
  try:
    req = request.get_json()
    collection = getDB().todo.insert(req)
    return jsonify({"message": "To Do agregado correctamente!"})
  except Exception as e:
    print(str(e))
    return jsonify({"message": "Error!"})

@app.route('/delete/<id>', methods=["DELETE"])
def deleteTodos(id):
  try:
    collection = getDB().todo.delete_one({'_id': ObjectId(id)})
    return jsonify({"message": "To Do eliminado correctamente!"})
  except Exception as e:
    print(str(e))
    return jsonify({"message": "Error!"})

@app.route('/update/<id>', methods=["PUT"])
def updateTodos(id):
  try:
    req = request.get_json()
    collection = getDB().todo.find_one_and_update({'_id': ObjectId(id)}, {
      '$set': req
    })
    return jsonify({"message": "To Do actualizado correctamente!"})
  except Exception as e:
    print(str(e))
    return jsonify({"message": "Error!"})

if __name__ == '__main__':
    app.run()