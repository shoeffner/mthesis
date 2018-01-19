# This is one of the hackiest files I ever wrote, please ignore it if you were
# looking for any kind of best practices.
# This file is filled with globals and I am a little bit ashamed of that fact.
# But it does what it should and that's enough - it will never be production
# code anyways.

import glob
import os

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as image
import scipy.misc as smisc


def get_csv_path(img_path):
    """Converts a /resized/*.jpeg to a /annotations/*.csv path."""
    return './annotations/' + img_path.split('/')[-1].split('.')[0] + '.csv'


def ensure_csv_files():
    """Creates non-existent annotations/*.csv files with the content:
    0, 0
    0, 0
    """
    global images
    for img in images:
        fp = get_csv_path(img)
        if not os.path.isfile(fp):
            with open(fp, 'w') as f:
                f.write('0, 0\n0, 0')


def reset_eyes():
    """Reads the eyes from the csv file and draws them."""
    global ax, current, eyes, images, left, markers
    with open(get_csv_path(images[current]), 'r') as f:
        lines = f.read().splitlines()
    if not lines:
        eyes = [(0, 0), (0, 0)]
    else:
        eyes = [tuple(int(x) for x in line.split(', ')) for line in lines]
    draw_eyes()
    left = True


def draw_eyes():
    """Draws the eyes as circles."""
    global ax, eyes, fig, markers
    for marker in markers:
        marker.remove()
    markers = [
        patches.Circle(eyes[0], radius=4, fc='none', ec='red'),
        patches.Circle(eyes[1], radius=4, fc='none', ec='red')
    ]
    for marker in markers:
        ax.add_artist(marker)
    fig.canvas.draw()


def save():
    """Saves the currently selected eyes."""
    global current, eyes, images
    with open(get_csv_path(images[current]), 'w') as f:
        eyes = sorted(eyes, key=lambda e: e[0])
        f.write('{0}, {1}\n{2}, {3}'.format(*eyes[0], *eyes[1]))
    next_image()


def swap_image():
    """Loads the next image."""
    global ax, axim, current, images
    reset_eyes()
    img = smisc.imread(images[current])
    if axim is None:
        axim = image.AxesImage(ax)
        ax.set_aspect('equal')
        ax.add_image(axim)
    axim.set_data(img)
    ax.set_title(f'Current: {images[current]}')
    ax.set_xlim([0, img.shape[1]])
    ax.set_ylim([img.shape[0], 0])


def next_image():
    """Increments current. Handles overflows. Swaps the image."""
    global current, images
    current = (current + 1) % len(images)
    swap_image()


def prev_image():
    """Increments current. Handles underflows. Swaps the image."""
    global current, images
    global current, images
    if current == 0:
        current = len(images) - 1
    else:
        current = current - 1
    swap_image()


def onkeypress(event):
    """Handles key presses."""
    actions = {
        'q': lambda: plt.close(),
        'escape': lambda: plt.close(),
        'right': next_image,
        'left': prev_image,
        ' ': save
    }
    actions.get(event.key, lambda: ...)()


def onclick(event):
    """Handles button clicks."""
    global eyes, left, markers
    if event.button == 1:
        if event.xdata is not None and event.ydata is not None:
            eyes[left] = (int(event.xdata), int(event.ydata))
            left = not left
    else:
        eyes = [(0, 0), (0, 0)]
    draw_eyes()


# Read image directory, create globals, pick first image
images = sorted(glob.glob('./resized/*.jpeg'))
current = -1
ensure_csv_files()
fig, ax = plt.subplots()
axim = None
eyes = list()
markers = list()
left = True
next_image()

evt_handlers = [
  fig.canvas.mpl_connect('button_press_event', onclick),
  fig.canvas.mpl_connect('key_press_event', onkeypress)
]

plt.show()

for eh in evt_handlers:
    fig.canvas.mpl_disconnect(eh)
