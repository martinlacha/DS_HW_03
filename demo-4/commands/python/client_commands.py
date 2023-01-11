import os
import sys
import requests
from kazoo.client import KazooClient

# Zoo server IP address
zoo_server_ip = os.environ['ZOO_IP']
# Zookeeper client
zk = KazooClient(hosts=zoo_server_ip)
# Start Zookeeper client
zk.start()


# Print help for user
def help():
    print('User help:')
    print('Get: python3 client_commands.py <ip> get <key>')
    print('Put: python3 client_commands.py <ip> put <key> <value>')
    print('Delete: python3 client_commands.py <ip> delete <key>')
    print('Tree: python3 client_commands.py tree')

# Print entire tree of Distributed cache
def print_tree():
    paths = ['/']
    while len(paths) > 0:
        current_path = paths.pop()
        data, stats = zk.get(current_path)
        if stats.children_count > 0:
            child_list = zk.get_children(current_path)
            for child in child_list:
                if current_path == '/':
                    paths.append(f'/{child}')
                else:
                    paths.append(f'{current_path}/{child}')


if __name__ == '__main__':
    try:
        args = sys.argv
        argc = len(args)
        if argc < 2 or argc > 5:
            raise Exception(f'Invalid count of argument ({argc - 1}). Expected: 2,3 or 4')

        ip = args[1]
        operation = args[2]
        key = None
        if argc > 2:
            key = args[3]

        response = ''

        if operation == 'get':
            response = requests.get(f'http://{ip}:5000/api?key={key}')
        elif operation == 'put':
            value = args[4]
            response = requests.put(f'http://{ip}:5000/api?key={key}&value={value}')
        elif operation == 'delete':
            response = requests.delete(f'http://{ip}:5000/api?key={key}')
        elif operation == 'tree':
            print_tree()
            exit(code=0)
        else:
            raise Exception(f'Invalid operation ({operation}). Expected get, put, delete.')

        print(f'Code: {response.status_code}')
        print(f'Data: {response.text}')
    except Exception as ex:
        print(f'Error: {ex}')
        help()
    zk.stop()