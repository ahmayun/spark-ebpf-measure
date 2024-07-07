import networkx as nx
import matplotlib.pyplot as plt
import sys
import re
import matplotlib.patches as mpatches

NODE_SHAPE = None
NODE_TYPE = sys.argv[3] # should be either 'pid' or 'port'
SEED = 1
port_to_pid_map = {}
color_names = [
    "red", "green", "blue", "cyan", "magenta", "yellow", "black", "white",
    "grey", "orange", "brown", "pink", "lime", "purple", "navy", "gold",
    "salmon", "turquoise", "violet", "darkgreen", "tan", "skyblue", "olive",
    "maroon", "lavender", "lightgreen"]

PORT_LABELS = {
    '7077': 'Master:7077'
}

PID_LABELS = {
    '2590793': 'Master',
    '2590955': 'Worker1',
    '2591026': 'Worker2',
}


def create_index(val, exclusive_max):
    return int(val)%exclusive_max


def draw_directional_graph(file_content):
    # Create a new directed graph
    G = nx.DiGraph()

    # Split the file content into lines
    lines = file_content.split('\n')

    # Iterate over each line to extract the connection details
    for line in lines:
        if not line.startswith("{"):
            continue

        # Extract src_port, dst_port, pkt_count, and total_bytes
        parts = line.split(' ')
        dst_port = parts[1].split('->')[1][:-1]
        pid = parts[6][:-1]
        print(f"Extracted PID: {pid}")
        port_to_pid_map[dst_port] = pid

        # If we don't have a label for the pid, get it from port information
        if pid not in PID_LABELS:
            if dst_port in PORT_LABELS:
                PID_LABELS[pid] = PORT_LABELS[dst_port]
        # else:
        #     if dst_port in PORT_LABELS:
        #         PID_LABELS[pid] += f'||{PORT_LABELS[dst_port]}'

                # if 'RpcEndpoint' in PORT_LABELS[dst_port]:
                    # PID_LABELS[pid] = PORT_LABELS[dst_port]
                # if 'ShuffleService' in PORT_LABELS[dst_port]:
                    # PID_LABELS[pid] = PORT_LABELS[dst_port]
                    

        # print(src_port, dst_port, pkt_count, total_bytes)
    print(f'Port to PID: {port_to_pid_map}')

    for line in lines:
        if not line.startswith("{"):
            continue

        parts = line.split(' ')
        src_port = parts[1].split('->')[0]
        dst_port = parts[1].split('->')[1][:-1]
        pkt_count = int(parts[4][:-1])
        total_bytes = int(parts[5][:-1])

        src_pid = port_to_pid_map[src_port]
        dst_pid = port_to_pid_map[dst_port]

        if NODE_TYPE=='pid':
            src = src_pid
            dst = dst_pid
            LABELS = PID_LABELS
        elif NODE_TYPE=='port':
            src = src_port
            dst = dst_port
            LABELS = PORT_LABELS
        

        if not src in LABELS:
            LABELS[src] = f'unk:{src}'

        if not dst in LABELS:
            LABELS[dst] = f'unk:{dst}'
        # Add an edge to the graph from src_port to dst_port with pkt_count and total_bytes as attributes
        if G.has_edge(dst, src):
            # Add reverse edge with different attributes if it's a separate connection
            G[dst][src]['pkt_count'] += pkt_count
            G[dst][src]['total_bytes'] += total_bytes
        else:
            # Add an edge to the graph from src to dst with pkt_count and total_bytes as attributes
            G.add_edge(src, dst, pkt_count=pkt_count, total_bytes=total_bytes)
        # G.add_edge(src_port, dst_port, pkt_count=pkt_count, total_bytes=total_bytes)

    # Draw the graph
    # pos = nx.spring_layout(G, k=5)  # positions for all nodes
    pos = nx.spring_layout(G,seed=SEED, k=0.4)  # positions for all nodes

    color_arr = [color_names[create_index(n if NODE_TYPE=='pid' else port_to_pid_map[n], len(color_names))] for n in G]
    print(color_arr)
    color_tuples = set(list(zip([n if NODE_TYPE=='pid' else port_to_pid_map[n] for n in G], color_arr)))
    color_map = {name:color for name, color in color_tuples}
    print(color_map)
    # nodes
    nx.draw_networkx_nodes(G, pos, node_color=color_arr, node_size=700, node_shape=NODE_SHAPE)

    # edges
    nx.draw_networkx_edges(G, pos, width=2, arrowstyle='->', arrowsize=10)

    # labels
    # edge_labels = dict([((u, v,), f'({d["pkt_count"]}, {d["total_bytes"]})')
    #                     for u, v, d in G.edges(data=True)])
    edge_labels = {}
    for (u, v, data) in G.edges(data=True):
        label = f'({data["pkt_count"]}, {data["total_bytes"]})'
        edge_labels[(u, v)] = label

    print('LABELS', LABELS)
    legend_handles = []
    for (_pid, _color) in color_map.items():
        legend_handles.append(mpatches.Patch(color=_color, label=PID_LABELS[_pid]))

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    print(LABELS)
    nx.draw_networkx_labels(G, pos, labels=LABELS, font_size=10, font_family='sans-serif')

    plt.legend(handles=legend_handles)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def print_port_info(log_file):
    with open(log_file, 'r') as f:
        log_lines = f.read().split("\n")
    
    def add_to_port_dict(name, ports):
        for p in ports:
            if p not in PORT_LABELS:
                PORT_LABELS[p] = f'{p}:{name}'
            else:
                PORT_LABELS[p] += f'/{name}'

    def get_driver_port(lines):
        line = list(filter(lambda l: 'sparkDriver' in l, lines))[0]
        extracted_port = line[-6:-1]
        add_to_port_dict('Driver', [extracted_port])
        return extracted_port
    
    # def get_worker_ports(lines):
    #     filtered_lines = list(filter(lambda l: 'worker' in l, lines))
    #     matches = re.findall(r'\d+:(\d+)\)', "\n".join(filtered_lines))
    #     extracted_ports = [port for port in matches]
    #     add_to_port_dict('Worker', extracted_ports)
    #     return extracted_ports
    
    def get_executor_ports(lines):
        filtered_lines = list(filter(lambda l: 'Executor added' in l, lines))
        matches = re.findall(r'\d+:(\d+)\)', "\n".join(filtered_lines))
        extracted_ports = [port for port in matches]
        add_to_port_dict('Executor', extracted_ports)
        return extracted_ports
    
    def get_shuffleserver_ports(lines):
        filtered_lines = list(filter(lambda l: 'Shuffle server' in l, lines))
        extracted_ports = [l[-5:] for l in filtered_lines]
        add_to_port_dict('ShuffleService', extracted_ports)
        return extracted_ports
    
    def get_nettyrpc_ports(lines):
        filtered_lines = list(filter(lambda l: 'NettyRpcEndpointRef' in l and 'CoarseGrainedSchedulerBackend' in l, lines))
        matches = re.findall(r'\d+:(\d+)\)', "\n".join(filtered_lines))
        extracted_ports = [port for port in matches]
        add_to_port_dict('CGSB:RpcEndpointRef', extracted_ports)
        return extracted_ports

    driver_port = get_driver_port(log_lines) # filter for sparkDriver
    # worker_ports = get_worker_ports(log_lines) # filter for "worker"
    executor_ports = get_executor_ports(log_lines) # filter for "Executor added"
    shuffle_service_ports = get_shuffleserver_ports(log_lines) # filter for "Shuffle server"
    nettyrpc_ports = get_nettyrpc_ports(log_lines) # filter for "nettyrpcendpointref"
    print(f'Driver: {driver_port}')
    # print(f'Workers: {worker_ports}')
    print(f'Executors: {executor_ports}')
    print(f'Shuffle Service: {shuffle_service_ports}')
    print(f'CGSB: {nettyrpc_ports}')
    print(f'Port Labels: {PORT_LABELS}')



# Example usage (assuming your file's content is stored in `file_content` variable):
# draw_directional_graph(file_content)
BPF_MAP_FILE=sys.argv[1]
SPARK_LOG=sys.argv[2]
print_port_info(SPARK_LOG)

with open(BPF_MAP_FILE, 'r') as f:
    draw_directional_graph(f.read())
