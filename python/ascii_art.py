import image_processing as ip
from impro import ImPro

image = ip.read_image_from_binary("../test04.ppm")
lines = ip.image_to_ascii(image, block_scale=120)
#print(lines)
print(*lines, sep="\n")

impro_obj = ImPro("../test04.ppm", 240)
impro_obj.show_ascii_image()
impro_obj.write_ascii_image()
