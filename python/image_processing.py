ASCII = [
    ' ', '.', '\'', '`', '\'', '-', '^', '"', '!',
    '>', ';', '=', '0', 'i', 'j', 'l', 't', 'c',
    'f', 'o', 'a', 'V', '5', 'e', 'b', 'D', 'p',
    'g', 'B', 'm', 'H', 'H', 'H', 'M', 'M', '@'
]

def read_image_from_binary(filename):
    image = {}
    with open(filename, "rb") as in_file:
        p6 = in_file.readline().strip()
        width_height = in_file.readline().strip().split()
        depth = in_file.readline().strip()
        image["p6"] = p6
        image["width"] = int(width_height[0])
        image["height"] = int(width_height[1])
        image["depth"] = depth

        pixels = []
        while True:
            pixel = {}
            #red component
            byte = in_file.read(1)
            if byte == b"":
                break
            pixel["red"] = int.from_bytes(byte, "little")
            #green component
            byte = in_file.read(1)
            if byte == b"":
                break
            pixel["green"] = int.from_bytes(byte, "little")
            #blue component
            byte = in_file.read(1)
            if byte == b"":
                break
            pixel["blue"] = int.from_bytes(byte, "little")

            pixels.append(pixel)

    image["pixels"] = pixels
    return image

def get_pixel(image, height, width):
    idx = height * image["width"] + width
    return image["pixels"][idx]

def pixel_brightness(pixel):
    return (pixel["red"] + pixel["green"] + pixel["blue"]) / 3

def image_to_ascii(image, block_scale):
    lines = []
    block_width = image["width"] // block_scale
    block_height = 2 * block_width
    print(block_width, block_height)
    for ih in range(image["height"]//block_height):
        line = ""
        for iw in range(image["width"]//block_width):
            brightness = 0
            for bh in range(block_height):
                for bw in range(block_width):
                    pixel = get_pixel(image,
                                      ih*block_height+bh,
                                      iw*block_width+bw)
                    brightness += pixel_brightness(pixel)
            #scale brightness for ascii
            brightness *= 36 / 256 / (block_width * block_height)
            line += ASCII[int(brightness)]
        lines.append(line)

    return lines
