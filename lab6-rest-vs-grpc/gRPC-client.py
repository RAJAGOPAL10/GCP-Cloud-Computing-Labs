#!/usr/bin/env python3
from __future__ import print_function
import requests
import time
import sys
import base64
import random
import grpc

import lab6_pb2
import lab6_pb2_grpc

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
    print(f"where <cmd> is one of add, rawImage, dotProduct or jsonImage")
    print(f"and <reps> is the integer number of repititions for measurement")

host = sys.argv[1]
cmd = sys.argv[2]
reps = int(sys.argv[3])

addr = f"{host}:50051"
print(f"Running {reps} reps against {addr}")

channel = grpc.insecure_channel(addr)

def doAdd(debug=False):
    stub = lab6_pb2_grpc.addStub(channel)
    numbers = lab6_pb2.addMsg(a=2,b=3)

    response = stub.add(numbers)
    if debug:
        print("Response is", response)

def doRawImage(debug=False):
    stub = lab6_pb2_grpc.imageStub(channel)

    image = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    data = lab6_pb2.rawImageMsg(img=image)

    response = stub.imageRaw(data)
    if debug:
        print("Response is", response)

def doDotProduct(debug=False):
    stub = lab6_pb2_grpc.dotProductStub(channel)

    length = 100
    a = [random.random() for _ in range(length)]
    b = [random.random() for _ in range(length)]
    data = lab6_pb2.dotProductMsg(a=a, b=b)

    response = stub.dotProduct(data)
    if debug:
        print("Response is", response)
    
def doJsonImage(debug=False):
    stub = lab6_pb2_grpc.jsonImageStub(channel)

    image = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    img_data = base64.b64encode(image).decode('utf-8')
    data = lab6_pb2.jsonImageMsg(img=img_data)

    response = stub.imageJson(data)
    if debug:
        print("Response is", response)

if cmd == 'add':
    start = time.perf_counter()
    for x in range(reps):
        doAdd()
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'rawImage':
    start = time.perf_counter()
    for x in range(reps):
        doRawImage()
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'jsonImage':
    start = time.perf_counter()
    for x in range(reps):
        doJsonImage()
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
elif cmd == 'dotProduct':
    start = time.perf_counter()
    for x in range(reps):
        doDotProduct()
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
else:
    print("Unknown option", cmd)