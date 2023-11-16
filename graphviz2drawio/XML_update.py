import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring, ElementTree
from html import unescape
import re




def update_xml(entity_base64_list, xml_content):
    #Muss ersetzt werden durch eigentlichen Flowcode
    #Muss auch ersetzt werden durch eigentlichen FLowcode
    node_ids = []
    for node_id in entity_base64_list:
        node_ids.append(node_id[0])
    print(node_ids)
    #xml_file_path = r"/home/andre/Downloads/JSON-XML/graphviz2drawio/output_drawio_no_img.xml"
    tree = ET.ElementTree(ET.fromstring(xml_content))
    root = tree.find('root')

    geometries = {}

    for mxCell in root.findall('.//mxCell'):
        value = mxCell.get('value')
        if value:
            decoded_value = unescape(value)
            #print(decoded_value)
            match = re.search(r"'>([^&]+)</p>", decoded_value)
            #print(match)
            if match:
                key = match.group(1)
                #print("Matched Key:", key)
                if key in node_ids:
                    mxgeometry = mxCell.find('mxGeometry')
                    if mxgeometry is not None:
                        geometries[key] = {attr: mxgeometry.get(attr) for attr in ['x', 'y', 'width', 'height']}

    print(geometries)

    base64_dic = {}
    for key in geometries:

        new_width = float(geometries[key]['width']) / 2
        new_height = float(geometries[key]['height']) / 2
        new_x_position = float(geometries[key]['x']) + 20
        new_y_position = float(geometries[key]['y']) + 20

        for entity, base64_string in entity_base64_list:
            if entity == key:
                base64_dic[key] = base64_string

        base64_string = base64_dic.get(key, '')

        new_element_template = f'''
       <mxCell id="{key}_image" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/jpeg,{base64_string};" vertex="1" parent="1">
           <mxGeometry x="{new_x_position}" y="{new_y_position}" width="{new_width}" height="{new_height}" as="geometry" />
       </mxCell>
        '''
        #print(new_element_template)
        #parsing to an Element
        new_element = fromstring(new_element_template.strip())

        for elem in root.findall('.//mxCell'):
            if key in elem.get('value', ''):  # Check if the key is in the value attribute
                index = list(root).index(elem)
                root.insert(index + 1, new_element)
                break  # Stop the loop once the new element is inserted

        #Insert new Element into XML tree

        #inserted = insert_new_element(root, child_id_to_insert_after, new_element, key)

    #Write modified XML tree back to file
    tree.write("/home/andre/Downloads/JSON-XML/graphviz2drawio/output_drawio_with_img.xml", xml_declaration=True, encoding='utf-8')
