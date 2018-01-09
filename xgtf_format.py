from lxml import etree

path = "tests/actions1.xgtf"

root = etree.parse(path).getroot()

print(root)

for child in root[1]:
    print('tag: {}, attrib: {}'.format(child.tag, child.attrib))

location = root[1][0][1][0][0].attrib
print('location: {}'.format(location))    # print {'framespan': '1:1', 'height': '64', 'width': '35', 'x': '445', 'y': '343'}
if(root[1][0][1].tag == "{http://lamp.cfar.umd.edu/viper#}object"):    #{http://lamp.cfar.umd.edu/viper#}object
    print("It's object")
objectNum = 0
for object in root.iter("{http://lamp.cfar.umd.edu/viper#}object"):
    objectNum += 1
    print('tag: {}, attrib: {}'.format(object.tag, object.attrib))
    for child in object:
        print(child.attrib.get('name'))
print('object number: {}'.format(objectNum))

namespace = {'viper': 'http://lamp.cfar.umd.edu/viper#',
      'data': 'http://lamp.cfar.umd.edu/viperdata#'}

for object in root.findall('.//viper:object', namespace):
    print('tag: {}, attrib: {}'.format(object.tag, object.attrib))
    for box in object.findall('./viper:attribute/data:bbox', namespace): #.findall('./attribute/data:bbox'):
        # print('tag: {}, attrib: {}'.format(box.tag, box.attrib))
        print('frame: {}'.format(box.attrib.get('framespan')))

