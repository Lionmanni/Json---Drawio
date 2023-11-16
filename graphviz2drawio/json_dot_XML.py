import os
import json
from graphviz2drawio import graphviz2drawio
import xml.dom.minidom


def generate_dot(Connections, Entities):
    groups = {}
    for node, attributes in Entities.items():
        for group in attributes["group"]:
            if group not in groups:
                groups[group] = []
            groups[group].append(node)

    dot_representation = "digraph G {\n"

    # Create subgraphs for each group
    for group, nodes in groups.items():
        dot_representation += f"    subgraph cluster_{group} {{\n"
        for node in nodes:
            attributes = Entities.get(node, {})
            image_attr = ""
            # If there's an image attribute, include it
            if "image" in attributes:
                image_path = attributes["image"].replace("\\", "\\\\")  # Escape the backslashes
                image_attr = f' [image="{image_path}"]'

            if len(attributes.get("group", [])) > 1:
                # Create ghost node for each group
                dot_representation += f"        {node}_{group}{image_attr} [label=\"\"];\n"
                dot_representation += f"        {node}_{group} -> {node} [style=invis];\n"
            else:
                dot_representation += f"        {node}{image_attr};\n"
        dot_representation += "    }\n"

    # Create connections
    for connection in Connections:
        source, _, target = connection.partition(" - ")
        dot_representation += f"    {source} -> {target};\n"

    dot_representation += "}"
    #print(dot_representation)
    return dot_representation

def format_xml(xml_string):
    dom = xml.dom.minidom.parseString(xml_string)
    pretty_xml = dom.toprettyxml()
    #Return pretty XML after removing any extra white spaces
    return '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])

def main(json_file_path):
        try:
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
            Connections = data['Connections']
            Entities = data['Entities']
            output = generate_dot(Connections, Entities)
            if output:
                module_name = os.path.splitext(os.path.basename(json_file_path))[0]
                dotfile_path = os.path.abspath(f"{module_name}.dot")
                with open(f"{module_name}.dot", 'w') as dot_file:
                    dot_file.write(output)

                # Generate PNG from DOT file
                os.system(f"dot -Tpng {module_name}.dot -o {module_name}.png")

                # Open PNG - this method varies based on the operating system
                if os.name == "posix":  # POSIX compliant (Unix, Linux, MacOS)
                    os.system(f"open {module_name}.png")
                elif os.name == "nt":  # Windows
                    os.system(f"start {module_name}.png")
        except (FileNotFoundError, KeyError):
            print("Error: The JSON file must exist and have 'Connections' and 'Entities' defined.")

        if dotfile_path:
            xml_data = graphviz2drawio.convert(dotfile_path)
            #print(dotfile_path)
            # print(xml_data)
            xml_content = format_xml(xml_data)
            #print(xml_data)
            with open(f"output_drawio_no_img.xml", "w") as drawio_xml_no_img_file:
                drawio_xml_no_img_file.write(xml_content)
        print(xml_content)

        return xml_content




















