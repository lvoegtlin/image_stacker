import argparse
import os
import sys
from PIL import Image
import numpy as np
from tqdm import tqdm


def check_extension(filename, extension_list):
    return any(filename.endswith(extension) for extension in extension_list)


def get_file_list(dir, extension_list):
    list = []
    for root, _, fnames in sorted(os.walk(dir)):
        for fname in fnames:
            if check_extension(fname, extension_list):
                path = os.path.join(root, fname)
                list.append(path)
    list.sort()
    return list


def search_in_folder(folders, name):
    files = []
    for folder in folders:
        files.extend(get_file_list(folder, '.png'))

    return filter(lambda x: name in x, files)


def stack(images, output_path):
    images = list(images)
    output_file = os.path.join(output_path, os.path.splitext(os.path.basename(list(images)[0]))[0]) + '.png'

    for image in images:
        if not os.path.exists(image):
            print("path not found {}".format(image))
            sys.exit(1)

    images = [np.asarray(Image.open(img)) for img in images]

    # check if all have the same size
    init_shape = images[0].shape
    new_img = np.zeros(init_shape)
    for image in images:
        if image.shape != init_shape:
            print("not same shape")
            sys.exit(1)

    for image in images:
        new_img = np.maximum(new_img, image)

    new_img = Image.fromarray(new_img.astype('uint8'))
    new_img.save(output_file)


def main(image_folders, output_path, **kwargs):
    root_images = get_file_list(image_folders[0], '.png')

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for image in tqdm(root_images, ncols=150):
        name = os.path.splitext(os.path.basename(image))[0]
        images = search_in_folder(image_folders, name)
        stack(images, output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--image_folders', nargs='+', type=str,
                        required=True,
                        help='path to the folder, where the file are. the first folder is the root folder and in the'
                             ' other we are searching for similarly named files and then stack them')
    parser.add_argument('--output_path', type=str,
                        required=True,
                        help='path to the file')

    args = parser.parse_args()

    main(**args.__dict__)
