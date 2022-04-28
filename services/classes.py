# classes.py: Endpoints for reading and writing Classes database
# 
# Authors: Ronin Sharma and Jude Javillo
# Version: 14 February 2022

from urllib import request
from flask import *
import services.databases as db
import services.users as users

classes = Blueprint('classes', __name__, url_prefix='/classes')

@classes.route('/all', methods=['GET'])
def getAll():
    result = db.getAll('Classes', 'Cornell_University')
    return {"result": result}


@classes.route('/some', methods=['GET'])
def getSome():
    result = db.getSome('Classes', 'Cornell_University', request.json)
    return {"result": result}


@classes.route('/', methods=['GET'])
def getOne(data = None):
    result = db.getCollection('Classes', 'Cornell_University').find_one(data if data else request.json)
    return {"result": result}


@classes.route('/', methods=['PATCH'])
def patch():
    success = db.patch('Classes', 'Cornell_University', request.args.get('id'), request.json)
    result = {"success": success}
    result["message"] = "Class successfully updated" if success else "Class unsuccessfully updated"
    return result


@classes.route('/', methods=['POST'])
def post():
    success = db.post('Classes', 'Cornell_University', request.json)
    result = {"success": success}
    result["message"] = "Class successfully added" if success else "Class unsuccessfully added"
    return result

@classes.route('/addUserToClass', methods=['POST'])
def addUserToClass(user = None, class_ = None):
    # request.json example: {'class_': class_, 'email': 'test123@gmail.com'}
    postRequest = request.json 
    user = users.getOneByEmail(postRequest['email'])['result'].to_bson()
    postRequest['user'] = user

    print('REQUEST')
    print(postRequest)

    success = db.post('Classes', 'Cornell_University', postRequest, False)
    id = success[1]
    result = {"success": success[0]}
    result["message"] = "User successfully added to class" if success else "User unsuccessfully added to class"
    return result

@classes.route('/', methods=['DELETE'])
def delete():
    success = db.delete('Classes', 'Cornell_University', request.json["_id"])
    result = {"success": success}
    result["message"] = "Class successfully removed" if success else "Class unsuccessfully removed"
    return result
