class ImPro:
    ASCII = [
        ' ', '.', '\'', '`', '\'', '-', '^', '"', '!',
        '>', ';', '=', '0', 'i', 'j', 'l', 't', 'c',
        'f', 'o', 'a', 'V', '5', 'e', 'b', 'D', 'p',
        'g', 'B', 'm', 'H', 'H', 'H', 'M', 'M', '@'
    ]

    def __init__(self, filename, scale):
        self.__image = self._read_image_from_binary(filename)
        self.__ascii_image = self._image_to_ascii(scale)

    #private: "_"
    def _read_image_from_binary(self, filename):
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

    def _get_pixel(self, height, width):
        idx = height * self.__image["width"] + width
        return self.__image["pixels"][idx]

    def _pixel_brightness(self, pixel):
        return (pixel["red"] + pixel["green"] + pixel["blue"]) / 3

    def _image_to_ascii(self, block_scale):
        lines = []
        block_width = self.__image["width"] // block_scale
        block_height = 2 * block_width
        for ih in range(self.__image["height"]//block_height):
            line = ""
            for iw in range(self.__image["width"]//block_width):
                brightness = 0
                for bh in range(block_height):
                    for bw in range(block_width):
                        pixel = self._get_pixel(ih*block_height+bh,
                                                iw*block_width+bw)
                        brightness += self._pixel_brightness(pixel)
                #scale brightness for ascii
                brightness *= 36 / 256 / (block_width * block_height)
                line += ImPro.ASCII[int(brightness)]
            lines.append(line)

        return lines

    #interface
    #public
    def show_ascii_image(self):
        print(*self.__ascii_image, sep="\n")

    def get_ascii_image(self):
        return self.__ascii_image

    def write_ascii_image(self, filename = "out.txt"):
        out_file = open(filename, "w")
        for line in self.__ascii_image:
            out_file.write(line + "\n")
        out_file.close()
