import XML_update
import json_dot_XML
import Jsondict
import json


def main():
    json_file_path = "/home/andre/Downloads/JSON-XML/graphviz2drawio/datafiletest.json"

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    Connections = data['Connections']
    Entities = data['Entities']

    json_dot_XML.generate_dot(Connections, Entities)
    xml_content = json_dot_XML.main(json_file_path)

    entity_base64_list = Jsondict.id_from_json_to_base64(json_file_path)

    XML_update.update_xml(entity_base64_list, xml_content)


main()