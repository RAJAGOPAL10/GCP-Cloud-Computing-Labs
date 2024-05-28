#!/usr/bin/env python3
from flask import Flask, request, Response
import jsonpickle, pickle
import platform
import io, os, sys
import redis
import hashlib, requests
import logging
from minio import Minio
import base64

# Initialize the Flask application
app = Flask(__name__)

redisHost = os.getenv("REDIS_HOST") or "localhost"
redisClient = redis.Redis(host=redisHost, decode_responses=True)

minioHost = os.getenv("MINIO_HOST") or "localhost:9000"
minioUser = os.getenv("MINIO_USER") or "rootuser"
minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"
minioClient = Minio(minioHost,
               access_key=minioUser,
               secret_key=minioPasswd)

def log(message):
    redisClient.lpush("logging", message)

def sendToWorker(hash):
    print("Sending",hash, "to queue")
    redisClient.lpush('queue',hash)


@app.route('/', methods=['GET'])
def hello():
    return '<h1> Music Separation Server</h1><p> Use a valid endpoint </p>'


@app.route('/apiv1/separate' , methods=['POST'])
def seprateMp3():
    mp3data = request.json['mp3']
    
    mp3data = mp3data.encode('utf-8')
    sha = hashlib.sha256()
    sha.update(mp3data)
    hash = sha.hexdigest()

    response = { 
        "hash" : hash
    }
    response_encoded = jsonpickle.encode(response)
    
    present = minioClient.bucket_exists("queue")
    if not present:
        minioClient.make_bucket("queue")
        print("Bucket 'queue' created")
    else:
        print("Bucket 'queue' already exists")
    sendToWorker(hash)

    mp3_as_a_stream = io.BytesIO(mp3data)
    minioClient.put_object("queue", hash, mp3_as_a_stream , length=len(mp3data))

    log("POST /apiv1/separate HTTP/1.1 200")
    return Response(response=response_encoded, status=200, mimetype="application/json")


@app.route('/apiv1/queue' , methods=['GET'])
def queueEntries():
    entries = redisClient.lrange( "queue", 0, -1 )
    response = { 
        "queue" : entries
    }
    response_pickled = jsonpickle.encode(response)
    log("POST /apiv1/queue HTTP/1.1 200")
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/apiv1/track/<string:hash>' , methods=['GET'])
def getTracks(hash: str):
    objects_to_download = minioClient.list_objects("output", prefix=hash, recursive=True)
    i = 0
    for item in objects_to_download:
        i += 1
        minioClient.fget_object("output",item.object_name,"../downloads/"+item.object_name)
    if i > 0:
        log('POST /apiv1/track/%s HTTP/1.1 200' % hash)
        return Response(response="Downloaded Successfully", status=200, mimetype="application/json")
    else:
       log('POST /apiv1/track/%s HTTP/1.1 404' % hash)
       return Response(response="Track not found", status=404, mimetype="application/json") 
    
@app.route('/apiv1/remove/<string:hash>' , methods=['DELETE'])
def removeTracks(hash: str):
    objects_to_delete = minioClient.list_objects("output", prefix=hash, recursive=True)
    i = 0
    for obj in objects_to_delete:
        i += 1
        minioClient.remove_object("output", obj.object_name)
    if i > 0:
        log('DELETE /apiv1/remove/%s HTTP/1.1 200' % hash)    
        return Response(response="Deleted Successfully", status=200, mimetype="application/json")
    else:
        log('DELETE /apiv1/remove/%s HTTP/1.1 404' % hash)
        return Response(response="Track not found", status=404, mimetype="application/json")     


# start flask app
app.run(host="0.0.0.0", port=5000)