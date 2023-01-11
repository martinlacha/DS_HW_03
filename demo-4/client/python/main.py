import os
from kazoo.client import KazooClient
from flask import Flask, jsonify, request
from cache_store import Cache_Store
from mylog import log
from node_binary_tree import Tree, Node
from flask_restx import Resource, Api
from zookeeper_node import register_new_node
import requests
import netifaces

app = Flask(__name__)
api = Api(app)

# Cache store object
cache = Cache_Store()
# Node IP address
node_ip = os.environ['NODE_IP']
# Root IP address
root_ip = os.environ['ROOT_IP']
# Zoo server IP address
zoo_server_ip = os.environ['ZOO_IP']
# Bool value if node is root
im_root = (node_ip == root_ip)
# IP address of parent node
parent_ip_address = None
# Instance of node object
root = None
# Instance of Tree
tree = None
# Zookeeper instance
zk = None

# Method to get parent ip address
@app.route('/parent', methods=['PUT'])
def get_parent_ip():
    log.info(f'Get request to find parent.')
    log.info(f'Request: {request.get_json}')
    if not im_root:
        log.error(f'Receive request for root.')
        return jsonify({'error' : "This node is not root."}), 400
    parameters = request.get_json()
    ip = parameters['node_ip_address']
    log.info(f'Get parent request for ip: {ip}')
    parent_node = tree.add_new_node(ip)
    if parent_node is not None:
        log.info(f'Returning parent IP: {parent_node._ip_address}')
        return jsonify({'parent_ip_address': parent_node._ip_address}), 200
    else:
        log.error('Can not found parent node!')
        exit(2)


#
@api.route('/api')
class ApiResource(Resource):
    # GET method
    @api.doc(
        params = {
            'key': 'Key identify record in cache.'
        },
        responses = {
            200: 'Value was found and return by key in cache.',
            201: 'Value not found in cache by key',
            400: 'Invalid parameters of request. Parameter key missing.',
        }
    )
    def get(self):
        key = request.args.get('key')
        if key is None:
            log.error(f'Invalid request for GET method. Reason: Invalid key')
            return 'Invalid parameters of request. Invalid key.', 400

        log.info(f'Receive GET method to find value for key: {key}')
        value = cache.get(key)

        if key is not None:
            return value, 200

        if im_root is True:
            log.info(f'Value was not found in cache')
            return 'Value not found in cache by key', 201
        else:
            # TODO zjistit zda to není v rodičovi
            pass


    # PUT method
    @api.doc(
        params = {
            'key': 'Find data in cache by this key.',
            'value': 'Value stored in cache under key.'
        },
        responses = {
            200: 'Value was insert in cache.',
            400: 'Invalid parameters of request. Parameter key missing.',
            401: 'Invalid parameters of request. Parameter value missing.'
        }
    )
    def put(self):
        key = request.args.get('key')
        value = request.args.get('value')
        
        # Check validity of key
        if key is None:
            log.error(f'Invalid parameters of request. Parameter key missing.')
            return 'Invalid parameters of request. Parameter key missing.', 400

        # Check validity of value
        elif value is None:
            log.error(f'Invalid parameters of request. Parameter value missing.')
            return 'Invalid parameters of request. Parameter value missing.', 401

        log.info(f'Receive PUT method to find value for key: {key}, value: {value}')
        cache.put(key, value)

        if im_root is True:
            return 'Value was insert in cache.', 200
        else:
            # TODO vypropagovat do rodiče
            pass


    # DELETE method
    @api.doc(
        params = {
            'key': 'Remove key-value record from cache.'
        },
        responses = {
            200: 'Value was delete by key in cache.',
            201: 'Value not found in cache by key',
            400: 'Invalid parameters of request. Parameter key missing.',
        }
    )
    def delete(self):
        key = request.args.get('key')

        # Check validity of key
        if key is None:
            log.error(f'Invalid parameters of request. Parameter key missing.')
            return 'Invalid parameters of request. Parameter key missing.', 400

        log.info(f'Receive DELETE method to find value for key: {key}')
        removed = cache.delete(key)

        # Check if value was removed from cache
        if removed is True:
            log.info(f'Value removed from local cache.')
            if im_root is True:                
                return 'Value was delete by key in cache.', 200
            else:
                # TODO vypropagovat do rodiče
                pass
        else:
            log.info(f'Value not found in cache for key: {key}')
            return 'Value not found in cache by key', 201

# Get parent by Call API of root node
def get_parent_ip_from_root():
    try:
        response = requests.put(f'http://{root_ip}:5000/parent', json={'node_ip_address' : node_ip})
        
        if response.status_code == 200:
            data = response.json()
            parent_ip = data['parent_ip_address']
            log.info(f'Found parent node with IP: {parent_ip}')
            return parent_ip
        else:
            log.error(f'Error: Parent node not found in tree structure for node with IP: {node_ip}')
    except Exception as e:
        log.error(f'Error: {e}')
    return None


# Get data from parent node
def get_parent_data():
    try:
        pass
    except Exception as e:
        log.error(f'Error while get data from cache.')
        log.error(f'Error: {e}')
    return None


# Put new key-value record into parent node
def put_parent_data():
    try:
        pass
    except Exception as e:
        log.error(f'Error while put data in cache.')
        log.error(f'Error: {e}')
    return None


# Delete value from parent node cache by key
def delete_parent_data():
    try:
        pass
    except Exception as e:
        log.error(f'Error while deleting data from cache.')
        log.error(f'Error: {e}')


# Main method
if __name__ == '__main__':
    zk = KazooClient(hosts=zoo_server_ip)
    zk.start()

    log.info(f'Starting node.')
    log.info(f'Parameters:')
    log.info(f'IP: {node_ip}')
    log.info(f'ROOT: {root_ip}')

    if im_root:
        log.info(f'Initialize root node on IP: {node_ip}')
        root = Node(root_ip, None)
        tree = Tree(root)
    else:
        parent_ip_address = get_parent_ip_from_root()
        log.info(f'Initialize regular node on IP: {node_ip}')
    log.info(f'Starting application on IP: {node_ip}')

    # Register new node to Zookeeper
    register_new_node(zk, node_ip, parent_ip_address, im_root)
    app.run(host=node_ip, debug=True)