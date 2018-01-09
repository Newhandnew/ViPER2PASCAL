from lxml import etree

path = "/home/new/Downloads/VOCdevkit/VOC2012/Annotations/2007_000663.xml"
f = open(path, 'r')
xml_str = f.read()
xml = etree.fromstring(xml_str)

def recursive_parse_xml_to_dict(xml):
  """Recursively parses XML contents to python dict.

  We assume that `object` tags are the only ones that can appear
  multiple times at the same level of a tree.

  Args:
    xml: xml tree obtained by parsing XML file contents using lxml.etree

  Returns:
    Python dictionary holding XML contents.
  """
  if not xml:
    return {xml.tag: xml.text}
  result = {}
  for child in xml:
    child_result = recursive_parse_xml_to_dict(child)
    result[child.tag] = child_result[child.tag]
    if child.tag != 'object':
      result[child.tag] = child_result[child.tag]
    else:
      if child.tag not in result:
        result[child.tag] = []
      result[child.tag].append(child_result[child.tag])
  return {xml.tag: result}
#{'annotation': {'folder': 'VOC2012', 'filename': '2007_000663.jpg', 'source': {'database': 'The VOC2007 Database', 'annotation': 'PASCAL VOC2007', 'image': 'flickr'}, 'size': {'width': '422', 'height': '500', 'depth': '3'}, 'segmented': '1', 'object': [{'name': 'bus', 'pose': 'Frontal', 'truncated': '0', 'difficult': '0', 'bndbox': {'xmin': '12', 'ymin': '2', 'xmax': '417', 'ymax': '467'}}, {'name': 'car', 'pose': 'Rear', 'truncated': '1', 'difficult': '0', 'bndbox': {'xmin': '7', 'ymin': '39', 'xmax': '63', 'ymax': '94'}}, {'name': 'car', 'pose': 'Unspecified', 'truncated': '1', 'difficult': '1', 'bndbox': {'xmin': '362', 'ymin': '24', 'xmax': '422', 'ymax': '53'}}, {'name': 'car', 'pose': 'Rear', 'truncated': '1', 'difficult': '0', 'bndbox': {'xmin': '376', 'ymin': '36', 'xmax': '422', 'ymax': '81'}}, {'name': 'car', 'pose': 'Unspecified', 'truncated': '1', 'difficult': '1', 'bndbox': {'xmin': '373', 'ymin': '68', 'xmax': '422', 'ymax': '108'}}, {'name': 'car', 'pose': 'Unspecified', 'truncated': '1', 'difficult': '1', 'bndbox': {'xmin': '376', 'ymin': '98', 'xmax': '422', 'ymax': '210'}}]}}
#{'annotation': {'folder': 'VOC2012', 'filename': '2007_000663.jpg', 'source': {'database': 'The VOC2007 Database', 'annotation': 'PASCAL VOC2007', 'image': 'flickr'}, 'size': {'width': '422', 'height': '500', 'depth': '3'}, 'segmented': '1', 'object': {'name': 'car', 'pose': 'Unspecified', 'truncated': '1', 'difficult': '1', 'bndbox': {'xmin': '376', 'ymin': '98', 'xmax': '422', 'ymax': '210'}}}}

if __name__ == "__main__":
    print(recursive_parse_xml_to_dict(xml))