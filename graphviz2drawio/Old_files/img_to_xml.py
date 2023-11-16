import base64
import re
from PIL import Image
import json
from io import BytesIO
import xml.etree.ElementTree as ET

dotfile_path = r"/home/andre/Downloads/JSON-XML/graphviz2drawio/datafile.json"

def id_from_json_to_base64(dotfile_path):
    entity_base64_dict = {}  # Dictionary to store entity ID and its corresponding base64 image

    # Open and load the JSON file
    with open(dotfile_path, 'r') as f:
        data = json.load(f)

    # Convert image path to base64
    for entity, attributes in data.get("Entities", {}).items():
        if "image" in attributes:
            image_path = attributes["image"]
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                base64_data = base64.b64encode(image_data).decode("utf-8")
                entity_base64_dict[entity] = base64_data

    return entity_base64_dict

entity_base64_images = id_from_json_to_base64(dotfile_path)
#print(entity_base64_images)




def update_xml_file_img(entity_base64_images, xml_file_path, width, height, base64_data):
    """
    Update an XML file by searching for each entity ID from the dictionary and adding a new XML element with the corresponding base64 image data.

    Parameters:
    - entity_base64_images: Dictionary with entity IDs as keys and their base64 images as values.
    - xml_file_path: Path to the XML file to be updated.
    """

    # Load XML
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Define a template for the new element
    new_element_template = '''
    <mxCell id="new_element_{entity}" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/jpeg,{base64_data};" vertex="1" parent="1">
        <mxGeometry x="10" y="30" width="{width}" height="{height}" as="geometry" />
    </mxCell>
    '''

    for entity, base64_data in entity_base64_images.items():
        #print(f"Processing entity: {entity}")
        for child in root.findall(".//mxCell"):
            if 'value' in child.attrib and entity in child.attrib['value']:
                geometry = child.find("mxGeometry")
                #print(geometry)
                if geometry is not None:
                    new_width = float(geometry.attrib['width']) / 2
                    new_height = float(geometry.attrib['height']) / 2
                    # Create new element from template
                    new_element_str = new_element_template.format(base64_data=base64_data, width=new_width, height=new_height)
                    #print(new_element_str)
                    new_element = ET.fromstring(new_element_str)
                    for i, existing_child in enumerate(list(root)):
                        if existing_child == child:
                            root.insert(i + 1, new_element)
                            print(f"Inserted new element for entity: {entity}")
                            break

                    break
    #print(new_element_template)
    # Save the updated XML
    tree.write(xml_file_path)


# Test
# entity_base64_images = {"B_14": "base64_string_here"}
# update_xml_file_img(entity_base64_images, "path_to_your_xml_file.xml")


if __name__ == "__main__":
    xml_file_path = r"/output_drawio_with_img.xml"

    # You can remove the loop below if you don't need to process images here.
    for entity, base64_data in entity_base64_images.items():
        # Convert the base64 data back to a byte stream to get image dimensions
        image_data = base64.b64decode(base64_data)
        image_stream = BytesIO(image_data)
        width, height = Image.open(image_stream).size
        # You might want to use width and height in the future.

    # Call the function to update XML.
    # With the current logic, it's enough to call it once, after processing all entities.
    update_xml_file_img(entity_base64_images, xml_file_path, width, height, base64_data)
