# pip install pillow
from PIL import Image

def encode_image(image_path, data_to_hide):
    image = Image.open(image_path).convert("RGB")  # ensure RGB

    # Text -> UTF-8 bytes -> bits, then add 0x00 terminator
    binary_data = ''.join(format(b, '08b') for b in data_to_hide.encode('utf-8')) + '00000000'

    capacity = image.width * image.height * 3  # 3 bits/pixel (R,G,B)
    if len(binary_data) > capacity:
        raise Exception(f"Data too large: {len(binary_data)} bits > capacity {capacity} bits")

    data_index = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = image.getpixel((x, y))
            if data_index < len(binary_data):
                r = (r & ~1) | int(binary_data[data_index]); data_index += 1
            if data_index < len(binary_data):
                g = (g & ~1) | int(binary_data[data_index]); data_index += 1
            if data_index < len(binary_data):
                b = (b & ~1) | int(binary_data[data_index]); data_index += 1
            image.putpixel((x, y), (r, g, b))
            if data_index >= len(binary_data):
                break
        if data_index >= len(binary_data):
            break

    image.save("encoded_image.png")
    print("Data encoded successfully -> encoded_image.png")

def decode_image(encoded_image_path):
    encoded_image = Image.open(encoded_image_path).convert("RGB")
    bit_buffer = ""
    out = bytearray()

    for y in range(encoded_image.height):
        for x in range(encoded_image.width):
            r, g, b = encoded_image.getpixel((x, y))
            for comp in (r, g, b):
                bit_buffer += str(comp & 1)
                if len(bit_buffer) >= 8:
                    byte_bits = bit_buffer[:8]
                    bit_buffer = bit_buffer[8:]
                    if byte_bits == '00000000':  # terminator
                        return out.decode('utf-8', errors='replace')
                    out.append(int(byte_bits, 2))
    return out.decode('utf-8', errors='replace')

# Example
data_to_hide = "This is a hidden message!"
encode_image("original_image.png", data_to_hide)
decoded_data = decode_image("encoded_image.png")
print("Decoded data:", decoded_data)