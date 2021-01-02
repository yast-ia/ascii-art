import cv2
from pathlib import Path
import numpy as np


class AsciiImage:
    
    ASCII_CHARS = r"B8&WM#YXQO{}[]()I1i!pao;:,.    "
    N_CHARS = len(ASCII_CHARS)

    def __init__(self, filename=None, neighborhood=1, 
                 aspect_ratio=None, padding=True, mode="gray"):
        self.neighborhood = neighborhood
        self.aspect_ratio = aspect_ratio
        self.padding = padding
        self.mode = mode
        if filename is not None:
            self.load_image(filename=filename)
        self.convert()

    def load_image(self, filename=None, image_rgb=None):
        if image_rgb is not None:
            self.original_image = image_rgb
        elif Path(filename).exists():
            filename = Path(filename)
            self.original_image = cv2.imread(filename.as_posix())[::-1]
        else:
            raise ValueError(f"{filename} doesn't exists.")
        self.original_dim = self.original_image.shape
        if self.mode == "gray":
            self.src_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        else:
            #TODO: add knn color
            #self.src_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
            raise NotImplementedError()

        if self.neighborhood != 1:
            f_ = 1./self.neighborhood
            self.src_image = cv2.resize(self.src_image, None, fx=f_, fy=f_)

    def get_ascii(self, pixels_value):
        return AsciiImage.ASCII_CHARS[int(((AsciiImage.N_CHARS-1)*pixels_value)/256)]

    def convert(self):
        self.ascii = []
        rows, cols = self.src_image.shape
        for i in range(rows):
            self.ascii.append("")
            for j in range(cols):
                pixel = self.src_image[i,j]
                char = self.get_ascii(pixel)
                self.ascii[i] += char
        self.ascii = self.ascii[::-1]

    def save(self, output_path):
        output_filepath = Path(output_path)
        if output_filepath.suffix == ".txt":
            self.save_to_textfile(output_path)
        elif output_filepath.suffix in (".jpg", ".jpeg"):
            self.save_to_image(output_path)
        else:
            raise ValueError(f"Invalid extension: '{output_filepath.suffix}'")

    def save_to_textfile(self, output_path):
        with open(output_path, "w") as f:
            f.write(str(self) + "\n")

    def save_to_image(self, output_path):
        pass

    def __str__(self):
        return "\n".join(self.ascii)