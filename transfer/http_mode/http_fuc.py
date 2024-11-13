
import requests,json,ipaddress

from utils.common_utils import _check_protocol,check_port

from flask import jsonify


# def post_with_retry_sync(data:dict, url:str):
#     res = _safe_post_json(data,url)
#     if res and res.get("code",-1) ==

def _post_with_binary_data(data:bytes, args:dict, url:str):
    res = None
    headers = {"Content-Type": "application/octet-stream"}
    try:
        _res = requests.post(url = url, data = data,
                             params=args, headers = headers)
        res = _res.json()

    except Exception as e:
        print(e)

    return res

def _safe_post_json(data:dict, url:str):
    res = None
    headers = {"Content-Type": "application/octet-stream"}
    try:
        _res = requests.post(url = url, data = json.dumps(data),
                              headers = headers)
        res = _res.json()
    except Exception as e:
        print(e)

    return res

def get_json_result(code:int, message:str, data=None, status=None):
    if code is None:
        raise ValueError("code cannot be None")
    if message is None:
        raise ValueError("message canoot be None")

    response = {"code":code,"message":message}

    if data is not None:
        response['data'] = data
    if status is not None:
        response['status'] = status

    return jsonify(response)


def get_url(ip:str, port:str="", protocol:str="", path:str=""):
    if path!="":
        path = path if path.startswith("/") else "/"+path

    if ip.startswith("http"):
        return ip+path

    ipaddress.ip_address(ip)
    _check_protocol(protocol)
    check_port(port)
    return "{}://{}:{}".format(protocol,ip,port+path)




