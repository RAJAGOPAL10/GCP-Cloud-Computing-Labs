# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import lab6_pb2 as lab6__pb2


class addStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.add = channel.unary_unary(
                '/add/add',
                request_serializer=lab6__pb2.addMsg.SerializeToString,
                response_deserializer=lab6__pb2.addReply.FromString,
                )


class addServicer(object):
    """Missing associated documentation comment in .proto file."""

    def add(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_addServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'add': grpc.unary_unary_rpc_method_handler(
                    servicer.add,
                    request_deserializer=lab6__pb2.addMsg.FromString,
                    response_serializer=lab6__pb2.addReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'add', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class add(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def add(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/add/add',
            lab6__pb2.addMsg.SerializeToString,
            lab6__pb2.addReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class imageStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.imageRaw = channel.unary_unary(
                '/image/imageRaw',
                request_serializer=lab6__pb2.rawImageMsg.SerializeToString,
                response_deserializer=lab6__pb2.imageReply.FromString,
                )


class imageServicer(object):
    """Missing associated documentation comment in .proto file."""

    def imageRaw(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_imageServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'imageRaw': grpc.unary_unary_rpc_method_handler(
                    servicer.imageRaw,
                    request_deserializer=lab6__pb2.rawImageMsg.FromString,
                    response_serializer=lab6__pb2.imageReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'image', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class image(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def imageRaw(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/image/imageRaw',
            lab6__pb2.rawImageMsg.SerializeToString,
            lab6__pb2.imageReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class dotProductStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.dotProduct = channel.unary_unary(
                '/dotProduct/dotProduct',
                request_serializer=lab6__pb2.dotProductMsg.SerializeToString,
                response_deserializer=lab6__pb2.dotProductReply.FromString,
                )


class dotProductServicer(object):
    """Missing associated documentation comment in .proto file."""

    def dotProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_dotProductServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'dotProduct': grpc.unary_unary_rpc_method_handler(
                    servicer.dotProduct,
                    request_deserializer=lab6__pb2.dotProductMsg.FromString,
                    response_serializer=lab6__pb2.dotProductReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dotProduct', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class dotProduct(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def dotProduct(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dotProduct/dotProduct',
            lab6__pb2.dotProductMsg.SerializeToString,
            lab6__pb2.dotProductReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class jsonImageStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.imageJson = channel.unary_unary(
                '/jsonImage/imageJson',
                request_serializer=lab6__pb2.jsonImageMsg.SerializeToString,
                response_deserializer=lab6__pb2.imageReply.FromString,
                )


class jsonImageServicer(object):
    """Missing associated documentation comment in .proto file."""

    def imageJson(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_jsonImageServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'imageJson': grpc.unary_unary_rpc_method_handler(
                    servicer.imageJson,
                    request_deserializer=lab6__pb2.jsonImageMsg.FromString,
                    response_serializer=lab6__pb2.imageReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'jsonImage', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class jsonImage(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def imageJson(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jsonImage/imageJson',
            lab6__pb2.jsonImageMsg.SerializeToString,
            lab6__pb2.imageReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
