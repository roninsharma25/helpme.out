# queues.py: Endpoints for reading and writing Queues database
# 
# Authors: Ronin Sharma and Jude Javillo
# Version: 14 February 2022

from urllib import request
from flask import *
from services.caches import queueingCache
from services.databases import Queue, QueueEntry, User
import services.databases as db

queues = Blueprint('queues', __name__, url_prefix='/queues')

@queues.route('/all', methods=['GET'])
def getAll():
    result = db.getAll('Queues', 'CornellUniversity')
    return {"result": result}


@queues.route('/', methods=['GET'])
def getOne():
    result = db.getOne('Queues', 'CornellUniversity', request.args.get('id'))
    return {"result": result}


@queues.route('/', methods=['PATCH'])
def patch():
    success = db.patch('Queues', 'CornellUniversity', request.args.get('id'), request.json)
    result = {"success": success}
    result["message"] = "Query successfully updated" if success else "Query unsuccessfully updated"
    return result


@queues.route('/', methods=['POST'])
def post():
    success = db.post('Queues', 'CornellUniversity', request.json)
    result = {"success": success}
    result["message"] = "Query successfully added" if success else "Query unsuccessfully added"
    return result


@queues.route('/', methods=['DELETE'])
def delete():
    success = db.delete('Queues', 'CornellUniversity', request.json["_id"])
    result = {"success": success}
    result["message"] = "Query successfully removed" if success else "Query unsuccessfully removed"
    return result

######

"""
Posting Memcached:
-Get filtered questions from database
-Write new question from the cache to the database

-In class
	-Create question (add to cache)
	-Read question (read from cache)


Queuing Memcached:
-Create a new queue for the OH slot
-Get X most recent entries from the database
-User can delete an element from the memcached queue (leave the queue)
-Write statistics to the database
"""

@queues.route('/cacheTestGet', methods=['GET'])
@queueingCache.cached()
def testGet():
    return str(queueingCache.get('queue').id)

@queues.route('/cacheTestPost', methods=['GET', 'POST'])
@queueingCache.cached(timeout=1)
def testPost():
    input = request.args.get('test')
    return input

@queues.route('/createQueue', methods=['GET', 'POST'])
@queueingCache.cached()
def createQueue():
    id = request.args.get('id')
    queueingCache.set(f'queue-{id}', Queue(id))
    return 'done'

@queues.route('/addQueueEntry', methods=['GET', 'POST'])
@queueingCache.cached()
def addQueueEntry():
    id = request.args.get('id')
    queue = queueingCache.get(f'queue-{id}')
    
    x = QueueEntry() # update with actual info
    queue.addEntry(x)
    queueingCache.set(f'queue-{id}', queue)
    return "done"
    
@queues.route('/getAllQueueEntries', methods=['GET'])
@queueingCache.cached()
def getAllQueueEntries():
    id = request.args.get('id')
    queue = queueingCache.get(f'queue-{id}')
    
    entries = str(queue.getQueue())

    return entries
    
    
