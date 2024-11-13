import json
import os
from tempfile import TemporaryDirectory
from google.protobuf import json_format
import spu.libspu.link as link
import spu.psi as psi
import multiprocess
from algorithm.psi.spu_utils import create_link_desc, wc_count, create_link_by_port




def make_oprf_key(key=None, save_path=None):
    ''' key should be a str thar like 0-f  hex type'''
    assert None != save_path, "save path should be valid or have a tmp dir"

    with open(os.path.join(save_path, "pir_server_secret_key.bin"), 'wb') as f:
        f.write(bytes.fromhex(key))
    f.close()



def pir_server(server_init_config, server_online_config,link_desc,index):

    init_config = json_format.json.loads(server_init_config)
    server_config = json_format.ParseDict(json.loads(server_online_config), psi.PirConfig())

    if not os.path.exists(init_config["pir_server_config"]["apsi_server_config"]["oprf_key_path"]):
        raise ValueError("oprf key is not exist")

    psi.pir(json_format.ParseDict(init_config, psi.PirConfig()))

    link_ctx = link.create_brpc(link_desc, index)

    psi.pir(server_config, link_ctx)







server_setup_config = f'''
    {{
        "mode": "MODE_SERVER_SETUP",
        "pir_protocol": "PIR_PROTOCOL_KEYWORD_PIR_APSI",
        "pir_server_config": {{
            "input_path": "./data/alice.csv",
            "setup_path": "./output/server/spu_test_pir_pir_server_setup",
            "key_columns": ["id"],
            "label_columns": ["x2"],
            "label_max_len": 288,
            "bucket_size": 1000000,
            "apsi_server_config": {{
                "oprf_key_path": "./output/server/pir_server_secret_key.bin",
                "num_per_query": 1,
                "compressed": false
            }}
        }}
    }}
'''

server_online_config = f'''
            {{
                "mode": "MODE_SERVER_ONLINE",
                "pir_protocol": "PIR_PROTOCOL_KEYWORD_PIR_APSI",
                "pir_server_config": {{
                    "setup_path": "./output/server/spu_test_pir_pir_server_setup"
                }}
            }}
'''


id = 1710312463672
port_list = [57449,52610]
key_value = "000102030405060708090a0b0c0d0e0ff0e0d0c0b0a090807060504030201000"

if __name__ == '__main__':
    make_oprf_key(key_value, './output/server')
    link_desc = create_link_by_port(id, port_list)
    pir_server(server_setup_config, server_online_config, link_desc, 0)
    pass
