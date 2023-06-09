import base64
from IPython.display import Image, display
import matplotlib.pyplot as plt

def mm(graph,diagram_url):
  graphbytes = graph.encode("ascii")
  base64_bytes = base64.b64encode(graphbytes)
  base64_string = base64_bytes.decode("ascii")
  display(Image(url="https://mermaid.ink/img/" + base64_string))
  print('https://mermaid.ink/img/' + base64_string)


# mm("""
# graph LR;
#     A--> B & C & D;
#     B--> A & E;
#     C--> A & E;
#     D--> A & E;
#     E--> B & C & D;
# """)

mm("""
graph LR;
    Producer--> Cluster ;
    Cluster --> Consumer
""")
# TODO better way to get the diagram than print url in stdout