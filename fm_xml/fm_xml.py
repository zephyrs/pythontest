import argparse
import os
import sys

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from xml.dom import minidom

target_folder = ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create config.xml for all players' image"
    )

    parser.add_argument("-t", "--target", help="folder path to the images")
    args = parser.parse_args()

    if args.target:
        target_folder = args.target
        if not os.path.isdir(target_folder):
            print("Input target folder[%s] is not found" % target_folder)
            sys.exit(0)
    else:
        print("target not set")
        sys.exit(0)

    record = ET.Element("record")

    preload_attributes = {"id": "preload", "value": "false"}
    ET.SubElement(record, "boolean", attrib=preload_attributes)

    amap_attributes = {"id": "amap", "value": "false"}
    ET.SubElement(record, "boolean", attrib=amap_attributes)

    maps = ET.SubElement(record, "list", id="maps")

    for dirpath, dirnames, files in os.walk(target_folder):
        for f in files:
            fname, fext = os.path.splitext(f)
            if fext.lower() != ".png":
                continue

            from_value = fname
            to_value = "graphics/pictures/person/{0}/portrait".format(fname)
            record_attributes = {"from": from_value, "to": to_value}
            ET.SubElement(maps, "record", attrib=record_attributes)

    # tree = ET.ElementTree(record)
    # tree.write("config.xml", xml_declaration=True)
    xmlstr = minidom.parseString(ET.tostring(record)).toprettyxml(indent="\t")
    with open(os.path.join(target_folder, "config.xml"), "w") as f:
        f.write(xmlstr)

