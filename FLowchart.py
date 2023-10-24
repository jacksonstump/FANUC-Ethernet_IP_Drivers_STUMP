import os
from graphviz import Digraph

# Set the path to the directory containing the 'dot' executable
graphviz_executable_dir = 'C:\\Users\\jacks\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\graphviz'

# Update the PATH environment variable to include the Graphviz directory
os.environ["PATH"] += os.pathsep + graphviz_executable_dir

# Create a Digraph object
dot = Digraph('Flowchart', format='png')

# Adjust DPI for image quality
dot.attr(dpi='300')

# Set the direction of the graph (left to right)
dot.attr(rankdir='LR')

# Node style
dot.node_attr.update(style='filled', color='lightyellow')

# Edge color
dot.edge_attr.update(color='blue')

# Load the DOT file and render it as an image
dot.render('FLowchart.dot', view=True, cleanup=True, format='png')
