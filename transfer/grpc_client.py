

from transfer.base_client import BaseClient
from utils.common_utils import loads_from_pickle,dumps_to_pickle,get_data_party_dir,write_bytes_to_file
from transfer.grpc_mode.grpc_fuc import send_message
from utils.record_instance import RecordInstace
import os



class GrpcClient(BaseClient):
    def __init__(self):
        super().__init__()
        self.client = "gprc"
        self.logger = None
        self.add_dict = {}

    def init_info(self, client_param:dict, run_identity:dict):
        super().init_info(clinet_param=client_param, run_indentity=run_identity)
        self._update_addr_dict()

    def _update_addr_dict(self):
        for party_id, ip_port in self.party_to_server.items():
            self.add_dict[party_id] = ip_port


    def remote(self,data, name:str, parties:list, suffix=tuple()):
        if not isinstance(suffix, tuple):
            suffix (suffix,)

        name = "_".join([name,*map(str,suffix)])
        print(f"start to remote data with name:{name} to parties:{parties}")
        for party_id in parties:
            if party_id not in self.add_dict:
                raise ValueError(f"party id ={party_id} does not exists")

            data = dumps_to_pickle(data)
            remote_dir = get_data_party_dir(self.task_id, self.local_party_id, party_id)
            os.makedirs(remote_dir,exist_ok=True)
            write_bytes_to_file(data, os.path.join(remote_dir,name+".pkl"))

            try:
                send_message(addr=self.add_dict[party_id],
                             bytes_data=data,
                             task_id=self.task_id,
                             src_party_id=self.local_party_id,
                             dst_party_id=party_id,
                             name=name)
            except Exception as e:
                raise e
        pass

    def get(self,name:str, parties:list,suffix=tuple()):
        if not isinstance(suffix, tuple):
            suffix(suffix, )

        data_list = []

        for party_id in parties:
            toname = "_".join([name,*map(str,suffix)])
            todata = loads_from_pickle(RecordInstace.check_in_and_get(self.task_id, party_id, self.local_party_id, toname))
            data_list.append(todata)
        return data_list