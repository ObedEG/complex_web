import uuid
from src.models.csc.nutanix_cigna.cigna_node import CignaNode
from src.common.database import Database
from src.models.csc.nutanix_cigna import constants as CignaConstants


class ClusterNutanix(object):

    def __init__(self, cluster_name, qty_nodes, hv_ip_start, hv_subnet, hv_gateway, cvm_ip_start, cvm_subnet,
                 cvm_gateway, storage_ip_start, storage_subnet, storage_gateway, imm_ip_start, imm_subnet, imm_gateway,
                 site_address, AOS_version, AHV_version, BestRecipe, nodes=None, start_date=None, finish_date=None,
                 _id=None):

        self.cluster_name = cluster_name
        self.qty_nodes = qty_nodes
        self.hv_ip_start = hv_ip_start
        self.hv_subnet = hv_subnet
        self.hv_gateway = hv_gateway
        self.cvm_ip_start = cvm_ip_start
        self.cvm_subnet = cvm_subnet
        self.cvm_gateway = cvm_gateway
        self.storage_ip_start = storage_ip_start
        self.storage_subnet = storage_subnet
        self.storage_gateway = storage_gateway
        self.imm_ip_start = imm_ip_start
        self.imm_subnet = imm_subnet
        self.imm_gateway = imm_gateway

        self.site_address = site_address
        self.AOS_version = AOS_version
        self.AHV_version = AHV_version
        self.BestRecipe = BestRecipe

        self.nodes = [] if nodes is None else nodes

        self.start_date = "" if start_date is None else start_date
        self.finish_date = "" if finish_date is None else finish_date

        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "_id": self._id,
            "cluster_name": self.cluster_name,
            "qty_nodes": self.qty_nodes,
            "hv_ip_start": self.hv_ip_start,
            "hv_subnet": self.hv_subnet,
            "hv_gateway": self.hv_gateway,
            "cvm_ip_start": self.cvm_ip_start,
            "cvm_subnet": self.cvm_subnet,
            "cvm_gateway": self.cvm_gateway,
            "storage_ip_start": self.storage_ip_start,
            "storage_subnet": self.storage_subnet,
            "storage_gateway": self.storage_gateway,
            "imm_ip_start": self.imm_ip_start,
            "imm_subnet": self.imm_subnet,
            "imm_gateway": self.imm_gateway,
            "site_address": self.site_address,
            "AOS_version": self.AOS_version,
            "AHV_version": self.AHV_version,
            "BestRecipe": self.BestRecipe,
            "start_date": self.start_date,
            "finish_date": self.finish_date
        }

    def create_cigna_cluster(self):

        hv_ip = self.get_segmented_ip(self.hv_ip_start)
        cvm_ip = self.get_segmented_ip(self.cvm_ip_start)
        storage_ip = self.get_segmented_ip(self.storage_ip_start)
        imm_ip = self.get_segmented_ip(self.imm_ip_start)

        for node in range(self.qty_nodes):
            node_hv_ip = hv_ip[0] + str(hv_ip[1])
            node_cvm_ip = cvm_ip[0] + str(cvm_ip[1])
            node_storage_ip = storage_ip[0] + str(storage_ip[1])
            node_imm_ip = imm_ip[0] + str(imm_ip[1])

            node = CignaNode(node_hv_ip, node_imm_ip, node_cvm_ip, node_storage_ip, cluster_id=self._id)
            node.save_to_db()
            self.nodes.append(node._id)

            hv_ip[1] += 1
            cvm_ip[1] += 1
            storage_ip[1] += 1
            imm_ip[1] += 1

    @staticmethod
    def get_segmented_ip(ip):
        """
        :param ip: IP  , e.g. ip = "10.5.5.10"
        :return: a touple ( first 3 elements of IP - string, last IP segment - int)
        """
        last_seg = int(ip.split('.')[-1])  # "10"
        ip_seg = '.'.join(ip.split('.')[0:3]) + '.'  # "10.5.5."
        return [ip_seg, last_seg]

    def save_to_db(self):
        Database.insert(CignaConstants.COLLECTIONS_CLUSTER, self.json())

    def update_to_mongo(self):
        Database.update(CignaConstants.COLLECTIONS_CLUSTER, {"_id": self._id}, self.json())

    @classmethod
    def get_cluster_by_id(cls, _id):
        return cls(**Database.find_one(CignaConstants.COLLECTIONS_CLUSTER, {"_id": _id}))
