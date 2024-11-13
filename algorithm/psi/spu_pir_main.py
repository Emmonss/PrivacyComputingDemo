from spu_pir_server import *
from spu_pir_client import *


client_online_config = f'''
        {{
            "mode": "MODE_CLIENT",
            "pir_protocol": "PIR_PROTOCOL_KEYWORD_PIR_APSI",
            "pir_client_config": {{
                "input_path": "./output/client/spu_test_pir_pir_client.csv",
                "key_columns": ["id"],
                "output_path": "./output/client/spu_test_pir_pir_output.csv"
            }}
        }}
'''

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
port_list= [57449,52610]
key_value = "000102030405060708090a0b0c0d0e0ff0e0d0c0b0a090807060504030201000"

if __name__ == '__main__':
    link_desc = create_link_by_port(id, port_list)
    #key
    make_oprf_key(key_value, './output/server')

    #test data
    test_path = "./output/client/spu_test_pir_pir_client.csv"
    make_query_csv(test_path)


    jobs = [multiprocess.Process(target=pir_server, args=(server_setup_config, server_online_config, link_desc,0),),
            multiprocess.Process(target=pir_clinet, args=(client_online_config, link_desc, 1),)]

    for job in jobs:
        job.start()
    for job in jobs:
        job.join()

    # #server
    # pir_server(server_setup_config, server_online_config, link_desc, 0)
    #
    # #client
    # pir_clinet(client_online_config, link_desc, 1)



