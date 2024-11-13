import json
from google.protobuf import json_format
import spu.libspu.link as link
import spu.psi as psi
from algorithm.psi.spu_utils import create_link_by_port



def pir_clinet(client_config, link_desc,index):
    client_config = json_format.ParseDict(json.loads(client_config), psi.PirConfig())
    link_ctx = link.create_brpc(link_desc, index)
    psi.pir(client_config, link_ctx)

def make_query_csv(path = None):
    pir_client_input_content = '''id
                user808
                '''

    with open(path, 'w') as f:
        f.write(pir_client_input_content)
    f.close()


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

test_path = "./output/client/spu_test_pir_pir_client.csv"
id = 1710312463672
port_list= [57449,52610]

if __name__ == '__main__':
    make_query_csv(test_path)
    link_desc2 = create_link_by_port(id, port_list)
    pir_clinet(client_online_config, link_desc2, 1)
