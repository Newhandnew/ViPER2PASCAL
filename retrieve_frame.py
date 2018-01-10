import cv2
import os

def retrieve_image(video_name, input_dir='tests', frame_second=3, output_dir='output', image_sets='training'):
    """Gets the images every x frame from a video, save ImageSets file and output image names.

    Args:
      video_name: input video name
      frame_seconds: catch image every x seconds
      output_dir: output directory
      image_sets: name of image_sets file

    Returns:
      Image names as a array
    """
    videoPath = os.path.join(input_dir, video_name)
    vcap = cv2.VideoCapture(videoPath)
    if False == vcap.isOpened():
        print("video cannot open!\n")
        return -1
    videoFPS = vcap.get(cv2.CAP_PROP_FPS)
    framePerCatch = round(frame_second * videoFPS)

    outputImageDir = os.path.join(output_dir, "images")
    outputImageSetsDir = os.path.join(output_dir, "ImageSets")
    if not os.path.exists(outputImageDir):
        os.makedirs(outputImageDir)
    if not os.path.exists(outputImageSetsDir):
        os.makedirs(outputImageSetsDir)

    output = []

    while(True):
        ret, img = vcap.read()

        if False == ret:
            break

        frameNumber = round(vcap.get(cv2.CAP_PROP_POS_FRAMES))
        if(frameNumber % framePerCatch == 0):
            output_name = '{}_{:04}'.format(video_name, frameNumber)
            output_img = output_name + ".jpg"
            imgOutput = os.path.join(outputImageDir, output_img)
            cv2.imwrite(imgOutput, img)
            print('write image {}'.format(imgOutput))
            pathImageSets = os.path.join(outputImageSetsDir, image_sets + ".txt")
            # write imagesets file
            if not os.path.exists(pathImageSets):
                open(pathImageSets, 'a').close()
            if output_name in open(pathImageSets).read():
                print('{} already exist'.format(output_name))
            else:
                with open(pathImageSets, 'a') as f:
                    f.write(output_name + '\n')
            # output frame number and file name
            file = {}
            file['frame_number'] = frameNumber
            file['name'] = output_name
            file['size'] = img.shape
            output.append(file)

    return output


if __name__ == '__main__':
    video_name = 'actions1.mpg'
    output = retrieve_image(video_name=video_name)
    for file in output:
        print('frame number: {}, file: {}, size: {}'.format(file['frame_number'], file['name'], file['size']))
