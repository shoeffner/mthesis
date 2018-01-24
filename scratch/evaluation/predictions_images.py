import scipy.misc as misc
import pandas as pd
import numpy as np


def map_and_clamp(value, rlim, limit):
    v = value / rlim * limit
    if v < 0:
        return 0
    if v > limit:
        return int(limit)
    return int(v)


def create_image(xs, ys, imsize=(24, 15), domain=(72, 45)):
    image = np.zeros((imsize[1], imsize[0], 3))
    for x, y in zip(xs, ys):
        x = map_and_clamp(x, domain[0], imsize[0] - 1)
        y = map_and_clamp(y, domain[1], imsize[1] - 1)
        image[y, x] += (1, 1, 1)

    image = np.log1p(np.log1p(image))
    return image


if __name__ == '__main__':
    pexels = pd.read_csv('pexels.csv')
    bioid = pd.read_csv('BioID.csv')

    gc_pexels_image = create_image(pexels['gazecapture_result_x'], pexels['gazecapture_result_y'])
    gc_bioid_image = create_image(bioid['gazecapture_result_x'], bioid['gazecapture_result_y'])
    # gaze_pexels_image = create_image(pexels['gazepoint_result_x'], pexels['gazepoint_result_y'])
    # gaze_bioid_image = create_image(bioid['gazepoint_result_x'], bioid['gazepoint_result_y'])

    misc.imsave('prediction_iTracker_BioID.png', misc.imresize(gc_bioid_image, 2000))
    misc.imsave('prediction_iTracker_Pexels.png', misc.imresize(gc_pexels_image, 2000))
    # misc.imsave('prediction_Gaze_Pexels.png', misc.imresize(gaze_pexels_image, 2000))
    # misc.imsave('prediction_Gaze_BioID.png', misc.imresize(gaze_bioid_image, 2000))
