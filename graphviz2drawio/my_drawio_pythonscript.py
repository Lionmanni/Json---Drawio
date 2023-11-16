from graphviz2drawio import graphviz2drawio

graph_to_convert = r'/home/andre/Downloads/Albis_JSON->DRAWIO/Albis_Vizual_Project/Python_scripts/DOT-py-testfile.dot'
xml = graphviz2drawio.convert(graph_to_convert)
print(xml)
