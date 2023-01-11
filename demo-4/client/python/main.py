import os
import requests
from kazoo.client import KazooClient
from flask import Flask, jsonify, request
from cache_store import Cache_Store
from mylog import log
from node_binary_tree import Tree, Node
from flask_restx import Resource, Api
from zookeeper_node import register_new_node

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

# Method to get parent ip address
@app.route('/parent', methods=['PUT'])
def get_parent_ip():
    if not im_root:
        log.error(f'Receive request for root.')
        return jsonify({'error' : "This node is not rootl."}), 401
    parameters = request.get_json()
    log.info(f'Get parent request for ip: {ip}')
    ip = parameters['node_ip_address']
    paren_node = tree.add_new_node(ip)
    if paren_node is not None:
        return jsonify({'parent_ip_address': parent_node._ip_address})
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
        
        if key is None:
            log.error(f'Invalid parameters of request. Parameter key missing.')
            return 'Invalid parameters of request. Parameter key missing.', 400
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

        if key is None:
            log.error(f'Invalid parameters of request. Parameter key missing.')
            return 'Invalid parameters of request. Parameter key missing.', 400

        log.info(f'Receive DELETE method to find value for key: {key}')
        removed = cache.delete(key)

        if removed is True:
            log.info(f'Value removed from local cache.')
            if im_root is True:
                # TODO vypropagovat do rodiče
                pass
                return 'Value was delete by key in cache.', 200
        else:
            log.info(f'Value not found in cache for key: {key}')
            return 'Value not found in cache by key', 201

        

# Main method
if __name__ == '__main__':
    '''
    if im_root:
        root = Node(root_ip, None)
        tree = Tree(root)
    else:
        pass
    '''
    app.run(host=str(node_ip), debug=True)