import os
import argparse
from retrieve_frame import retrieve_image
from Viper2Pascal import Viper_2_Pascal
from Viper2Pascal import write_pascal_file



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process input filenames')
    parser.add_argument('-n', '--video_name', type=str, default='actions1.mpg',
                        help="only the name of input video")
    parser.add_argument('-d', '--input_dir', type=str, default='tests',
                        help="input directory of the video")
    parser.add_argument("-s", "--frame_second", type=int, default=3,
                        help="catch frame every x second interval")
    parser.add_argument("-l", "--anno_label", type=str, default='tests/actions1.xgtf',
                        help="label file of ViPER video")
    parser.add_argument("-o", "--output_dir", type=str, default='output',
                        help="output directory")
    args = parser.parse_args()

    files = retrieve_image(video_name=args.video_name,
                           input_dir=args.input_dir,
                           frame_second=args.frame_second,
                           output_dir=args.output_dir)

    for file in files:
        objectList = Viper_2_Pascal(args.anno_label, file['frame_number'])
        inputFolder = os.path.join(args.output_dir, 'images')
        write_pascal_file(inputFolder, file['name'], file['size'], objectList)