from typing import Mapping, List


class BaseClient:
    def __init__(self):
        self.client = ""
        self.run_identity = None
        self.task_id = ""
        self.local_role = ""
        self.local_party_id = None
        self.local_executor_id = ""
        self.logger = None


        self.roles: Mapping[str,List[int]] = {}

        self.party_to_role:Mapping[int,str] = {}

        self.party_to_server:Mapping[int,str] = {}

    def init_info(self,clinet_param:dict, run_indentity: dict):
        self.run_identity = run_indentity

        self.task_id = run_indentity['task_id']
        self.local_party_id = run_indentity['local_party_id']
        self.local_role = run_indentity['local_role']
        self.local_executor_id = run_indentity['executor_id']

        self.roles = clinet_param['roles']
        self.party_to_server = clinet_param['party_to_server']
        self.party_to_role = clinet_param['party_to_role']

    def get_client_type(self):
        return self.client

    def remote(self,data, name:str, parties:list, suffix=tuple()):
        pass

    def get(self,name:str, parties:list,suffix=tuple()):
        pass