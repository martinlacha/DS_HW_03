from mylog import log
from kazoo.client import KazooClient
from time import sleep

# register new path to Zookeeper
def register_new_node(zk : KazooClient, new_node_ip, parent_node_ip, is_root):

    if is_root is True:
        log.info(f'Register root node into Zookeeper. Info: node: {new_node_ip}, parent: {parent_node_ip}, root: {is_root}')
        path = f'/{new_node_ip}'
        log.info(f'Path to check: {path}')
        if zk.exists(path):
            log.warn(f'Root path already exists.')
            return
        zk.create(path, makepath=True)
        return

    # Find path to parent
    parent_path = get_parent_path(zk, parent_node_ip)

    # Assert if parent path exists
    if parent_path is None:
        log.error(f'Parent path not exists for node {new_node_ip}')
        exit(404)
    
    new_node_path = f'{parent_path}/{new_node_ip}'
    
    # Check if path already exists
    if zk.exists(new_node_path):
        log.warn(f'Path for node with IP: {new_node_path} already exists')
        return
    
    # Create path for new node
    zk.create(new_node_path, makepath=True)


def get_parent_path(zk, parent_node_ip):
    log.info(f'Find parent node path in Zookeeper tree')
    
    # 3 attemps to find parent path
    # After failure attemp will sleep for one second
    for i in range(0, 3):
        parent_path = find_path_parent_node(zk, parent_node_ip)
        if parent_node_ip is not None:
            return parent_path
        sleep(1)
    return None


def find_path_parent_node(zk, parent_ip_address):
    paths = list()
    # Add root path to list
    paths.append('/')
    log.info(f'Try to find path for node {parent_ip_address}.')

    # Try to find parent path in tree structure
    while len(paths) > 0:
        log.info(f'List: {paths}')
        current_path = paths.pop()
        data, stats = zk.get(current_path)

        # Check number of children
        if stats.children_count > 0:
            children = zk.get_children(current_path)
            if current_path == '/':
                children.remove('zookeeper')
            log.info(f'Children: {children}')

            # Check if parent is in child nodes
            if parent_ip_address in children:
                parent_path = f'{current_path}/{parent_ip_address}'
                log.info(f'Found parent path: {parent_path}')
                return parent_path
            
            # Add new paths to check children nodes
            for ip in children:
                if current_path == '/':
                    paths.append(f'/{ip}')
                else:
                    paths.append(f'{current_path}/{ip}')
    log.warn(f'Path not found for parent node: {parent_ip_address}')
    return None