from py2neo.bulk import merge_nodes 
from helper import get_card_members
from tqdm import tqdm

# * Add nodes to the graph
def add_nodes(graph, tup_ls, labels, keys):   
    merge_nodes(graph.auto(), tup_ls, ('Node', 'name'), labels=labels, keys=keys)
    print('Number of nodes in graph: ', graph.nodes.match('Node').count())
    
# * Create edges for graph
def create_edges(task_triples):
    
    edge_tupl = {}
    
    for triple in task_triples:
        relation = triple[1]
        if relation in edge_tupl:
            edge_tupl[relation].append(triple)
        else: 
            edge_tupl[relation] = [(triple[0], relation, triple[1])]

    return edge_tupl

# * Add edges between nodes
def add_edges(graph, nodes_matcher, Node, Relationship, edge_dc):
    for edge_labels, tup_ls in tqdm(edge_dc.items()):   # k=edge labels, v = list of tuples
        tx = graph.begin()
        
        for itr, el in enumerate(tup_ls):
            tx = graph.begin()
            source_node = nodes_matcher.match(name=el[0]).first()
            target_node = nodes_matcher.match(name=el[2]).first()
            if not source_node:
                source_node = Node('Node', name=el[0])
                print("Node not found, Source:", source_node )
                graph.create(source_node)
            if not target_node:
                try:
                    target_node = Node('Node', name=el[2], node_labels=el[4], url=el[5], word_vec=el[6])
                    print("Node not found, target:", source_node )
                    graph.create(target_node)
                except:
                    continue
            try:
                rel = Relationship(source_node, edge_labels, target_node)
            except:
                continue
            graph.create(rel)

        graph.commit(tx)