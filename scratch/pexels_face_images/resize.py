import glob
import scipy.misc

for file_name in glob.glob('./photos/*.jpeg'):
    image = scipy.misc.imread(file_name)
    h, w, c = image.shape
    image = scipy.misc.imresize(image, (int(640 / w * h), 640))
    scipy.misc.imsave('./resized/' + file_name.split('/')[-1], image)
