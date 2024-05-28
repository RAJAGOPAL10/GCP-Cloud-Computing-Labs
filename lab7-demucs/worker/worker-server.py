#!/usr/bin/env python3
import base64
import sys
import os
import redis
import subprocess
from minio import Minio
import time


redisHost = os.getenv("REDIS_HOST") or "localhost" #"10.102.191.87"
redisPort = os.getenv("REDIS_PORT") or 6379
minioHost = os.getenv("MINIO_HOST") or "localhost:9000"
minioUser = os.getenv("MINIO_USER") or "rootuser"
minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"
minioClient = Minio(minioHost,
               secure=False,
               access_key=minioUser,
               secret_key=minioPasswd)

redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
print("Created all the clients")
while True:
    print("Inside while loop")
    try:
        print("before the worker node")
        work = redisClient.blpop("queue", timeout=10)
        print("worker node has created")
        if work:
           hash = work[1].decode('utf-8')
           print(hash)
           response = minioClient.get_object("queue", hash)
           data = base64.b64decode(response.data)
           with open('input.mp3','wb') as f:
                f.write(data)
           cmd = 'python3 -m demucs.separate --out ./output input.mp3 --mp3'
           p = os.system(cmd)
           found = minioClient.bucket_exists("output")
           if not found:
               minioClient.make_bucket("output")
           files = os.listdir('./output/mdx_extra_q/input/') 
           number_files = len(files)
           while True:
               if len(os.listdir('./output/mdx_extra_q/input/')) == 4:
                  for f in files:
                     path = './output/mdx_extra_q/input/'+f 
                     minioClient.fput_object("output", hash+"/"+f, path)
                     os.remove(path)
                  break    
    except Exception as exp:
        print(f"Exception raised in log : {str(exp)}")