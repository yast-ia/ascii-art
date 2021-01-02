from ascii_art import AsciiImage

def convert_image(image, output, neighborhood=1, print_image=True):
    ascii_image = AsciiImage(filename=image, neighborhood=neighborhood)
    if print_image:
        print(ascii_image)
    ascii_image.save(output)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Convert image to ascii art.")

    ap.add_argument("-i", "--image", required=True, type=str, 
                    help="Input image.")
    ap.add_argument("-o", "--output", default="output.txt", type=str,
                    help="Output file. Use `.txt` to save it as text and `.jpg` to save it as an")
    ap.add_argument("-n", "--neighborhood", default=1, type=int,
                    help="Size of neighborhood of pixels to convert to ascii.")
    ap.add_argument("-p", action="store_true", dest="print_image")
    args = vars(ap.parse_args())

    convert_image(**args)