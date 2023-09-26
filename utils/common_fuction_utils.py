


import pickle,os,sys
from constant_utils import PICKLE_VERSION,ABS_PROJECT_PATH


def write_bytes_to_filw(data,filename):
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




def get_data_party_dir(task_id,src_party_id,dst_party_id,name):
    return os.path.join(ABS_PROJECT_PATH,"data","get",task_id,str(src_party_id),str(dst_party_id),name)

def remote_data_party_dir(task_id,src_party_id,dst_party_id,name):
    return os.path.join(ABS_PROJECT_PATH,"data","remote",task_id,str(src_party_id),str(dst_party_id),name)








