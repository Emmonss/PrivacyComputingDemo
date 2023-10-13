from time import sleep, time
from utils.constant_utils import DEFAULE_GET_OVERTIME,DEFAULT_GET_SLEEP_TIME
from utils.common_utils import get_data_party_dir,write_bytes_to_file
import shutil,os,io


class RecordInstace:
    def __init__(self):
        pass

    @staticmethod
    def check_in_and_get(task_id,src_party_id, dst_party_id, name):
        overtime = time() + DEFAULE_GET_OVERTIME
        pass


    @staticmethod
    def _local_check_part_data(task_id,src_party_id,dst_party_id,name):
        save_dir = get_data_party_dir(task_id,src_party_id,dst_party_id,name)
        if not os.path.exists(save_dir):
            return False

        part_data_list = os.listdir(save_dir)
        if not part_data_list:
            return False

        sample = part_data_list[0]
        _, total, _ = sample.split("_")

        if len(part_data_list) != int(total):
            return False

        for item in part_data_list:
            _, _, size = item.split("_")
            if os.path.getsize(os.path.join(save_dir,item))!= int(size):
                return False

        return True

    @staticmethod
    def _get_final_data(task_id,src_party_id,dst_party_id,name):
        save_dir = get_data_party_dir(task_id,src_party_id,dst_party_id,name)
        final_data = io.BytesIO()
        for item in sorted(os.listdir(save_dir), key=lambda x: int(x.split("_",maxsplit=1)[0])):
            with open(os.path.join(save_dir,item), "rb") as f:
                final_data.write(f.read())

        shutil.rmtree(save_dir, ignore_errors=True)
        os.makedirs(save_dir, exist_ok=True)
        write_bytes_to_file(final_data.getvalue(), os.path.join(save_dir,"final_data.pkl"))

        return final_data.getvalue()