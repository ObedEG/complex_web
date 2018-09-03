import uuid
from src.common.database import Database
from src.models.csc.nutanix_cigna import constants as CignaConstants

class CignaNode(object):

    def __init__(self, hv_ip, imm_ip, cvm_ip, storage_ip, cluster_id, hv_name=None, imm_name=None, cvm_name=None,
                 serial_number=None, _id=None):
        self.hv_ip = hv_ip
        self.imm_ip = imm_ip
        self.cvm_ip = cvm_ip
        self.storage_ip = storage_ip
        self.cluster_id = cluster_id
        self.hv_name = "" if hv_name is None else hv_name
        self.imm_name = "" if imm_name is None else imm_name
        self.cvm_name = "" if cvm_name is None else cvm_name
        self.serial_number = "" if serial_number is None else serial_number
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "_id": self._id,
            "hv_ip": self.hv_ip,
            "hv_name": self.hv_name,
            "imm_ip": self.imm_ip,
            "imm_name": self.imm_name,
            "cvm_ip": self.cvm_ip,
            "storage_ip": self.storage_ip,
            "cluster_id": self.cluster_id,
            "cvm_name": self.cvm_name,
            "serial_number": self.serial_number
        }

    def save_to_db(self):
        Database.insert(CignaConstants.COLLECTIONS_NODES, self.json())

    def update_to_mongo(self):
        Database.update(CignaConstants.COLLECTIONS_NODES, {"_id": self._id}, self.json())

    @classmethod
    def get_node_by_id(cls, _id):
        return cls(**Database.find_one(CignaConstants.COLLECTIONS_NODES, {"_id": _id}))
