#!/usr/bin/env python3
import grpc
import time
from concurrent import futures
import io
from PIL import Image
import base64

import lab6_pb2
import lab6_pb2_grpc

class addServicer(lab6_pb2_grpc.addServicer):
    def add(self, request, context):
        sumValue = request.a + request.b
        response = lab6_pb2.addReply(sum = sumValue)
        return response

class imageServicer(lab6_pb2_grpc.imageServicer):
    def imageRaw(self, request, context):
        ioBuffer = io.BytesIO(request.img)
        image = Image.open(ioBuffer)
        response = lab6_pb2.imageReply(width = image.size[0], height = image.size[1])      
        return response

class dotProductServicer(lab6_pb2_grpc.dotProductServicer):
    def dotProduct(self, request, context):
        sumValue = sum(x*y for x, y in zip(request.a, request.b))
        response = lab6_pb2.dotProductReply(dotproduct=sumValue)
        return response

class jsonImageServicer(lab6_pb2_grpc.jsonImageServicer):
    def imageJson(self, request, context):
        bytesData = base64.b64decode(request.img.encode('utf-8'))
        ioBuffer = io.BytesIO(bytesData)
        image = Image.open(ioBuffer)
        response = lab6_pb2.imageReply(width = image.size[0], height = image.size[1])      
        return response        

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
lab6_pb2_grpc.add_addServicer_to_server(addServicer(), server)
lab6_pb2_grpc.add_imageServicer_to_server(imageServicer(), server)
lab6_pb2_grpc.add_dotProductServicer_to_server(dotProductServicer(), server)
lab6_pb2_grpc.add_jsonImageServicer_to_server(jsonImageServicer(), server)

print("Starting server at 50051")
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()