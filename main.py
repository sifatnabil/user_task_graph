import json
from platform import node
import spacy
from pprint import pprint
from py2neo import Node, Graph, Relationship, NodeMatcher

from helper import *
from graph_functions import *
from pprint import pprint
from env import *

with open("data.json", "r") as f:
    data = json.load(f)

user_node, project_nodes, board_nodes, task_nodes, software_nodes, task_triples = create_task_triples(data)

print(user_node, project_nodes, board_nodes, task_nodes, software_nodes, sep="\n")

graph = Graph(neo4j_url, name=neo4j_username, password=neo4j_password)
nodes_matcher = NodeMatcher(graph)

add_nodes(graph, [user_node], labels={"user"}, keys=["id", "name", "email"])

add_nodes(graph, project_nodes, labels={"project"}, keys=["id", "name"])

add_nodes(graph, board_nodes, labels={"board"}, keys=["name"])

add_nodes(graph, task_nodes, labels={"task"}, keys=["id", "name", "time"])

add_nodes(graph, software_nodes, labels={"software"}, keys=["name"])

edge_tupl_ls = create_edges(task_triples)

print(edge_tupl_ls)

add_edges(graph, nodes_matcher, Node, Relationship, edge_tupl_ls)