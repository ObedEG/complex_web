from flask import Blueprint, request, redirect, session, url_for, render_template
from src.models.csc.nutanix_cigna.nutanix_cluster import ClusterNutanix
from src.models.csc.nutanix_cigna.nutanix_cluster import CignaNode
cigna_blueprint = Blueprint('cigna', __name__)


@cigna_blueprint.route('/create_cluster', methods=['POST', 'GET'])
def create_cluster():
    if request.method == 'POST':
        cluster_name = request.form['cluster_name']
        qty_nodes = request.form['qty_nodes']
        hv_ip_start = request.form['hv_ip_start']
        hv_subnet = request.form['hv_subnet']
        hv_gateway = request.form['hv_gateway']
        cvm_ip_start = request.form['cvm_ip_start']
        cvm_subnet = request.form['cvm_subnet']
        cvm_gateway = request.form['cvm_gateway']
        storage_ip_start = request.form['storage_ip_start']
        storage_subnet = request.form['storage_subnet']
        storage_gateway = request.form['storage_gateway']
        imm_ip_start = request.form['imm_ip_start']
        imm_subnet = request.form['imm_subnet']
        imm_gateway = request.form['imm_gateway']
        site_address = request.form['site_address']
        AOS_version = request.form['AOS_version']
        AHV_version = request.form['AHV_version']
        BestRecipe = request.form['BestRecipe']
        cluster = ClusterNutanix(cluster_name, qty_nodes, hv_ip_start, hv_subnet, hv_gateway, cvm_ip_start, cvm_subnet,
                                  cvm_gateway, storage_ip_start, storage_subnet, storage_gateway, imm_ip_start,
                                  imm_subnet, imm_gateway, site_address, AOS_version, AHV_version, BestRecipe)
        cluster.create_cigna_cluster()
        cluster.save_to_db()
        return redirect(url_for(".edit_nodes_info", _id=cluster._id))
    return render_template('csc/cigna/create_cigna_cluster.jinja2')


@cigna_blueprint.route('/edit_cluster/<string:_id>', methods=['POST', 'GET'])
def edit_nodes_info(_id):
    nodes = []
    cluster = ClusterNutanix.get_cluster_by_id(_id)
    for node_id in cluster.nodes:
        nodes.append(CignaNode.get_node_by_id(node_id))
    render_template('csc/cigna/edit_node_info.jinja2', nodes=nodes)
    return True