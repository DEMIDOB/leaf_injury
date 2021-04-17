import os
import sys
import time

import cv2 as cv
import processing_py

from gui import show_error
from scanner import classify, make_mask_image

clear_cmd = {
    "darwin": "clear",
    "win32": "cls"
}

opendir_cmd = {
    "darwin": "open",
    "win32": "explorer"
}

scan_area = 210 * 297  # mm2


def show_scan_info(filename, masked_filename, injured_area, percentage, w, h):
    app = processing_py.App(size_x=400, size_y=200)
    app.background(255)

    original = app.loadImage(filename)
    app.image(original, 0, 0, min(200, w), min(135, h))

    masked = app.loadImage(masked_filename)
    app.image(masked, 200, 0, min(200, w), min(135, h))

    app.fill(0)
    app.textAlign(processing_py.LEFT, processing_py.TOP)
    app.textSize(20)
    app.text(f"Injured: {round(percentage * 100, 2)} %", 10, 145)
    app.text(f"Area: {round(injured_area / 100, 2)} cm2", 10, 168)

    app.redraw()


def manage_file(filename):
    if filename == "archived":
        return

    extension = filename.split(".")[-1]
    if extension.lower() not in ("jpg", "png", "jpeg"):
        show_error(title="Несовместимый формат файла", message=f"{extension} — несовместимый формат файла."
                                                               f" Допустимые: jpg, jpeg, png")
    else:
        image, classification_result = classify(f"scans/{filename}")
        masked = make_mask_image(image, classification_result)
        cv.imwrite("current_mask.jpg", masked)

        h, w, _ = image.shape
        pixel_area = scan_area / (h * w)

        injured_pixels = 0
        healthy_pixels = 0

        for i in classification_result:
            if i == 1:
                healthy_pixels += 1
            elif i == 2:
                injured_pixels += 1

        injured_area = injured_pixels * pixel_area
        percentage = injured_pixels / (healthy_pixels + injured_pixels)

        print(f"Поражённая площадь: {round(injured_area / 100, 2)} см2")
        print(f"Поражено {round(percentage * 100, 2)} % листа")

        print()

        show_scan_info(filename=os.path.abspath(f"scans/{filename}"),
                       masked_filename=os.path.abspath("current_mask.jpg"),
                       injured_area=injured_area, percentage=percentage, w=w, h=h)

    new_path = f"scans\\archived\\{filename}"
    if os.path.exists(new_path):
        os.system(f"del /f {new_path}")

    os.rename(f"scans\\{filename}", new_path)


if __name__ == '__main__':
    args = sys.argv
    if "scan-area" in args:
        try:
            scan_area = int(args[args.index("scan-area") + 1])
        except Exception as exc:
            print(f"Could not use provided scan-area value due to:\n{exc}")

    platform = sys.platform.lower()

    if not os.path.exists("scans/"):
        os.system("mkdir scans")

    if platform == "win32":
        if not os.path.exists("scans\\archived\\"):
            os.system("mkdir scans\\archived")
    else:
        if not os.path.exists("scans/archived/"):
            os.system("mkdir scans/archived")

    os.system(clear_cmd[platform])
    os.system(f"{opendir_cmd[platform]} scans")

    print("Отсканированные изображения помещайте в открывшуюся папку, они автоматически будут обрабатываться и "
          "перемещаться в папку archived\n")

    while True:
        for file in os.listdir("scans/"):
            manage_file(file)

        time.sleep(1)
