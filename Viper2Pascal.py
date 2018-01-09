from lxml import etree
from pascal_voc_io import PascalVocWriter


def Viper_2_Pascal(viper_file, frame_num):
    """Get specific frame imformation of all objects from ViPER format to PASCAL VOC format

    Args:
        viper_file: ViPER file end with xgtf format, contain whole annotation of a video
        frame: specific frame information

    Returns:
        object array with element name and bbox [{name: , bbox: }]
    """
    namespace = {'viper': 'http://lamp.cfar.umd.edu/viper#',
                 'data': 'http://lamp.cfar.umd.edu/viperdata#'}
    root = etree.parse(viper_file).getroot()


    objectList = []
    for object in root.findall('.//viper:object', namespace):
        objectAttrib = {}
        objectName = change_to_regular_name(object.attrib.get('name'))
        for box in object.findall('./viper:attribute/data:bbox', namespace):
            frameSpan = box.attrib.get('framespan').split(':')
            if int(frameSpan[1]) >= frame_num and int(frameSpan[0]) <= frame_num:
                objectAttrib['name'] = objectName
                xmin = int(box.attrib.get('x'))
                ymin = int(box.attrib.get('y'))
                xmax = xmin + int(box.attrib.get('width'))
                ymax = ymin + int(box.attrib.get('height'))
                bbox = (xmin, ymin, xmax, ymax)
                objectAttrib['bbox'] = bbox
                objectList.append(objectAttrib)
                break
    print(objectList)
        # writer = PascalVocWriter('tests', 'test', (512, 512, 1), localImgPath='tests/test.bmp')
        # difficult = 1
        # writer.addBndBox(60, 40, 430, 504, 'person', difficult)
        # writer.addBndBox(113, 40, 450, 403, 'face', difficult)
        # writer.save('tests/test.xml')

def change_to_regular_name(name):
    outputName = name.lower()
    if outputName == 'vehicle':
        outputName = 'car'
    if outputName != 'person' and outputName != 'car':
        print('not a regular name: {}'.format(outputName))
    return outputName

if __name__ == "__main__":
    path = "tests/actions1.xgtf"
    Viper_2_Pascal(path, 272)