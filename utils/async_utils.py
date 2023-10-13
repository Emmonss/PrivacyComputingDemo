
import requests,json



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



