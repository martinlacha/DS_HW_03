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

# 
@app.route('/parent', methods=['PUT'])

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
            400: 'Invalid parameters of request',
            404: 'Value not found by key in cache.'
        }
    )
    def get(self):
        pass
    
    # PUT method
    @api.doc(
        params = {
            'key': 'Find data in cache by this key.',
            'value': 'Value stored in cache under key.'
        },
        responses = {
            200: 'Value was found by key in cache.',
            201: 'Value was updated.',
            400: 'Invalid parameters of request',
            404: 'Value not found by key in cache.'
        }
    )
    def put(self):
        pass

    # DELETE method
    @api.doc(
        params = {
            'key': 'Remove key-value record from cache.'
        },
        responses = {
            200: 'Value was found by key in cache.',
            400: 'Invalid parameters of request',
            404: 'Value not found by key in cache.'
        }
    )
    def delete(self):
        pass

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