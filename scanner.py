import cv2 as cv

from model import PixelsClf

_clf = PixelsClf()

_MSK = (
    [255, 255, 255],
    [0, 255, 0],
    [255, 0, 0]
)


def downscale(source, max_width=800, max_height=550):
    img = source.copy()
    height, width, colors = img.shape

    assert colors == 3

    ratio = width / height

    if width > max_width:
        img = cv.resize(img, (max_width, int(max_width / ratio)))
        height, width, _ = img.shape

    if height > max_height:
        img = cv.resize(img, (int(max_height * ratio), max_height))

    return img


def get_rgb_pixels(source):
    img = cv.cvtColor(source, cv.COLOR_BGR2RGB)
    height, width, colors = source.shape
    assert colors == 3
    return img.reshape(width * height, 3)


def classify(filename):
    image = cv.imread(filename)
    image = downscale(image, max_width=200, max_height=135)

    h, w, _ = image.shape

    pixels = get_rgb_pixels(image)
    res = _clf.predict(pixels)

    return cv.cvtColor(image, cv.COLOR_RGB2BGR), res


def make_mask_image(image, classification_result):
    resulting_mask = image.copy()
    h, w, _ = image.shape

    for row in range(h):
        starting_pixel = row * w
        for x in range(w):
            resulting_mask[row][x] = _MSK[classification_result[starting_pixel + x]]

    resulting_mask = cv.cvtColor(resulting_mask, cv.COLOR_RGB2BGR)
    return resulting_mask

