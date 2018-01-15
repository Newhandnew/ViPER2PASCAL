import os
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
    return objectList


def change_to_regular_name(name):
    # vehicle -> car
    outputName = name.lower()
    if outputName == 'vehicle':
        outputName = 'car'
    if outputName != 'person' and outputName != 'car':
        print('not a regular name: {}'.format(outputName))
    return outputName

def write_pascal_file(input_folder, image_name, image_size, object_list, output_dir='output'):
    # write to Pascal format
    """input PASCAL format information and ViPer object list, then save PASCAL xml file

    Args:
        input_folder: input folder of image
        image_name: image name without file extension
        image_size: (height, width, depth)
        object_list: object list from ViPER format

    """
    outputAnnoDir = os.path.join(output_dir, "Annotations")
    if not os.path.exists(outputAnnoDir):
        os.makedirs(outputAnnoDir)
    writer = PascalVocWriter(input_folder, image_name + '.jpg', image_size)
    difficult = 0
    for object in object_list:
        writer.addBndBox(object['bbox'][0], object['bbox'][1], object['bbox'][2], object['bbox'][3], object['name'], difficult)
    outputPascalFile = os.path.join(outputAnnoDir, image_name + '.xml')
    writer.save(outputPascalFile)
    print("save PASCAL file {}".format(outputPascalFile))



if __name__ == "__main__":
    path = "tests/actions1.xgtf"
    objectList = Viper_2_Pascal(path, 272)
    for object in objectList:
        print('name: {}, bounding box: {}'.format(object['name'], object['bbox']) )
    inputFolder = "output/images"
    imageName = 'actions1.mpg_0072'
    image_size = (540, 960, 3)
    write_pascal_file(inputFolder, imageName, image_size, objectList)