


import pickle,os,sys
from utils.constant_utils import PICKLE_VERSION,ABS_PROJECT_PATH
from utils.constant_utils import HTTP_SUPPORT_PROTOCOLS
from typing import Union


def check_port(port: Union[int,str]):
    if isinstance(port,str) and not port.isdigit():
        raise ValueError(f"port:{port} is invalid")

    if not 0< int(port) <= 65535:
        raise ValueError(f"port:{port} is invalid")


def _check_protocol(protocol: str):
    if protocol not in HTTP_SUPPORT_PROTOCOLS:
        raise ValueError(f"{protocol} not supported")


def write_bytes_to_file(data,filename):
    with open(filename,"wb") as f:
        f.write(data)
    f.close()

def load_bytes_from_file(filename):
    with open(filename,"rb") as f:
        return f.read()


def dumps_to_pickle(data):
    return pickle.dumps(data,protocol=PICKLE_VERSION)

def loads_from_pickle(byte_data):
    return pickle.loads(byte_data)




def get_data_party_dir(task_id,src_party_id,dst_party_id):
    return os.path.join(ABS_PROJECT_PATH,"data",task_id,str(src_party_id),str(dst_party_id))

# def remote_data_party_dir(task_id,src_party_id,dst_party_id,name):
#     return os.path.join(ABS_PROJECT_PATH,"data","remote",task_id,str(src_party_id),str(dst_party_id))


if __name__ == '__main__':
    pass
    task_id = "test_01"
    src_party_id = "party_01"
    dst_party_id = "party_02"
    name = "test_fuck"
    dir = get_data_party_dir(task_id,src_party_id,dst_party_id)
    print(dir)









