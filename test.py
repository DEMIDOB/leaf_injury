import numpy as np
import cv2 as cv

from model import PixelsClf

test_image_path = "/Users/danademidov/Downloads/leaf.jpg"

MSK = (
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


if __name__ == '__main__':
    # clf = PixelsClf(model="model_0.92.dtclf")
    clf = PixelsClf()

    image = cv.imread(test_image_path)
    image = downscale(image, max_width=200, max_height=135)

    h, w, _ = image.shape

    cv.imwrite("test.jpg", image)

    pixels = get_rgb_pixels(image)
    res = clf.predict(pixels)

    resulting_mask = image.copy()

    for row in range(h):
        starting_pixel = row * w
        for x in range(w):
            resulting_mask[row][x] = MSK[res[starting_pixel + x]]

    resulting_mask = cv.cvtColor(resulting_mask, cv.COLOR_RGB2BGR)
    cv.imwrite("mask.jpg", resulting_mask)

    # for row in image:
    #     batch_size = 1000
    #     for step in range(w // batch_size + 1):
    #         pixels = row[step * batch_size:min(step * batch_size + batch_size, w)]
    #         res += list(clf.predict(pixels))

    print(len(res), w * h)
