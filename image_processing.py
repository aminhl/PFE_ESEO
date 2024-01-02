import numpy as np
import os
OPENSLIDE_PATH = os.getcwd() + "\\openslide-win64-20221217\\bin"


def process_image(img_path, saving_path):

    if hasattr(os, 'add_dll_directory'):
        with os.add_dll_directory(OPENSLIDE_PATH):
            from openslide import OpenSlide
    else:
        from openslide import OpenSlide

    violet_threshold = 0.005
    black_threshold = 0.8
    white_threshold = 0.48

    img = OpenSlide(img_path)

    last_slash = img_path.rfind('/')
    point = img_path.rfind('_T')
    directory = img_path[last_slash + 1: point]

    dim = img.dimensions
    ratio = 2
    dim = (int(dim[0] / ratio), int(dim[1] / ratio))
    imageDL = img.get_thumbnail(dim)

    width, height = imageDL.size
    tileNumberHeight = 600
    tileNumberWidth = 600
    new_dir_path = saving_path + "/" + directory

    os.mkdir(new_dir_path)

    dir_ok = new_dir_path + "/Clean"
    dir_u = new_dir_path + "/Unusable"
    os.mkdir(dir_ok)
    os.mkdir(dir_u)

    for j in range(0, height, tileNumberHeight):
        top = j
        bottom = min(j + tileNumberHeight, height)

        for k in range(0, width, tileNumberWidth):
            left = k
            right = min(k + tileNumberWidth, width)
            box = (left, top, right, bottom)
            tile = imageDL.crop(box)
            largeur, hauteur = tile.size

            if largeur == 600 and hauteur == 600:
                pixel_data = np.array(tile)
                violet_mask = np.all(pixel_data >= [
                                     102, 0, 102], axis=-1) & np.all(pixel_data <= [255, 102, 255], axis=-1)
                num_violet_pixels = np.sum(violet_mask)
                total_pixels = pixel_data.shape[0] * pixel_data.shape[1]
                percent_violet_pixels = 100 * num_violet_pixels / total_pixels

                if percent_violet_pixels >= violet_threshold:
                    black_mask = pixel_data[:, :, 0] < 10
                    num_black_pixels = np.sum(black_mask)
                    percent_black_pixels = 100 * num_black_pixels / total_pixels
                    white_mask = pixel_data[:, :, 1] > 245
                    num_white_pixels = np.sum(white_mask)
                    percent_white_pixels = 100 * num_white_pixels / total_pixels

                    if percent_black_pixels <= black_threshold and percent_white_pixels <= white_threshold:
                        tile.save(f"{dir_ok}/{directory}{j}_{k}.png")
                    else:
                        tile.save(f"{dir_u}/{directory}{j}_{k}.png")
                else:
                    tile.save(f"{dir_u}/{directory}_{j}_{k}.png")

    print("fin de l'image " + directory)
