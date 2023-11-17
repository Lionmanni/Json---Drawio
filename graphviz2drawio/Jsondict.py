import base64
import re
import json
from io import BytesIO
import xml.etree.ElementTree as ET
import os


def id_from_json_to_base64(json_file_path):
    if not os.path.exists(json_file_path):
        print(f"File does not exist: {json_file_path}")
        return
    entity_base64_list = []  # Dictionary to store entity ID and its corresponding base64 image

    # Open and load the JSON file
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    #print(data)
    # Convert image path to base64
    for entity, attributes in data.get("Entities", {}).items():
        if "image" in attributes:
            image_path = attributes["image"]
            #print(f"Found image for {entity}: {image_path}")
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                base64_data = base64.b64encode(image_data).decode("utf-8")
                entity_base64_list.append((entity, base64_data))
    #for pair in entity_base64_list:
        #print(f" The found pairs in your json file are: {pair}")
    return entity_base64_list


