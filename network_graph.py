from models.user import Users, User
import numpy as np
import networkx as nx
from plotly.tools import set_credentials_file
import plotly.plotly as py
from plotly.graph_objs import *
import os
import keys
import math

set_credentials_file(username='gabeleibo', api_key=os.environ["plotly_key"])

# Initialize the database
user_base = Users()
network = nx.Graph()

# Load in users
user_base.load_users('output/layer1.json')
init_user = user_base.get('/gabeleibo')

# Create nodes from hrefs (name uniquness)
user_network = init_user.get_friends()
full_network = user_network + [init_user.href]
network.add_nodes_from(full_network)


# Create edges (user 1 ->(follows) user 2)
for user in user_base.users:
    # Remove Celebrities
    if user.is_celebrity():
        try:
            network.remove_node(user.href)
        except:
            pass
        continue
    # Every follower on the network is a following on
    # the opposing node so only followers need to be added
    for follower in user.get_followers():
        if follower in full_network:
            network.add_edge(follower, user.href)
        else:
            continue


# Graph network
# Modified from https://plot.ly/python/network-graphs/

# Create coordinates for nodes
pos = nx.circular_layout(user_network)
pos['/gabeleibo'] = np.array([0,0])
for node in network.nodes:
    network.node[node]['pos'] = pos[node]

# Create Edge Lines
edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in network.edges():
    x0, y0 = network.node[edge[0]]['pos']
    x1, y1 = network.node[edge[1]]['pos']
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]

# Create Node points
node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=Marker(
        showscale=True,
        colorscale='Viridis',
        reversescale=True,
        color=[],
        size=[],
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

# figure details
for node in network.nodes():
    # Set position
    x, y = network.node[node]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)
    # Set color and size according to number of node connections
    connections = list(network.neighbors(node))
    node_trace['marker']['color'].append(len(connections))
    node_trace['marker']['size'].append(math.sqrt(len(connections))*10)
    # Add hover info for interactive graph
    user_name = user_base.get(node).user_name
    node_info = user_name + ' | # of connections: ' + str(len(connections))
    node_trace['text'].append(node_info)

# Create figure
fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
                title="SoundCloud 'Friend' Network Graph for 'gabeleibo'",
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

# Plot
py.iplot(fig, filename='networkx')
