from transfer.grpc_trans.proto import openrtb_pb2
from google.protobuf import json_format
import json

def pb_to_json(pbStringRequest):
    """将pbstring转化为jsonStringResponse返回"""
    jsonStringRequest=json_format.MessageToJson(pbStringRequest)
    return jsonStringRequest

def json_to_pb(jsonStringResponse):
    """将jsonStringResponse转化为pbString返回"""
    pbStringResponse = json_format.Parse(json.dumps(jsonStringResponse), openrtb_pb2.param())
    return pbStringResponse


if __name__ == '__main__':
    json_obj={'name':'fcao','value':'0.74','descibe':'202102241339'}
    request=json_to_pb(json_obj)
    print(request)
    print(type(request))
    json_result = pb_to_json(request)
    print(json_result)
    print(type(json_result))
