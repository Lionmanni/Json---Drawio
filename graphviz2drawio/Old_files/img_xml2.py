import base64
import re
from PIL import Image
import json
from io import BytesIO
import xml.etree.ElementTree as ET
import os



def insert_new_element(parent, child, new_element, entity):
    for index, elem in enumerate(parent):
        if elem == child:
            parent.insert(index + 1, new_element)
            print(f"Inserted new element for entity: {entity}")
            return True  # Successfully inserted
        if insert_new_element(elem, child, new_element, entity):
            return True
    return False





def update_xml_file_img(entity_base64_images, xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Define a template for the new element
    new_element_template = '''
    <mxCell id="new_element_{entity}" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/jpeg,{base64_data};" vertex="1" parent="1">
        <mxGeometry x="{x_position}" y="{y_position}" width="{width}" height="{height}" as="geometry" />
    </mxCell>
    '''

    for entity, base64_data in entity_base64_images.items():
        for child in root.findall(".//mxCell"):
            if 'value' in child.attrib and entity in child.attrib['value']:
                geometry = child.find("mxGeometry")
                if geometry is not None:
                    new_width = float(geometry.attrib['width']) / 2
                    new_height = float(geometry.attrib['height']) / 2
                    new_x_position = float(geometry.attrib['x']) + 20
                    new_y_position = float(geometry.attrib['y']) + 20
                    new_element_str = new_element_template.format(base64_data=base64_data, width=new_width, height=new_height, entity=entity, x_position=new_x_position, y_position=new_y_position)
                    new_element = ET.fromstring(new_element_str)
                    insert_new_element(root, child, new_element, entity)
                    break

    tree.write(xml_file_path)

#if __name__ == "__main__":


xml_file_path = r"/output_drawio_with_img.xml"
update_xml_file_img(entity_base64_images, xml_file_path)
"""