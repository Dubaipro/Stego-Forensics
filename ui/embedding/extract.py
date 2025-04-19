import cv2

def binary_to_message(binary_data):
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

def extract_data(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found. Check the path carefully!")

    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = [format(color, "08b") for color in pixel]
            binary_data += r[-1] + g[-1] + b[-1]

    delimiter = '1111111111111110'
    data = binary_data.split(delimiter)[0]

    return binary_to_message(data)

if __name__ == "__main__":
    extracted = extract_data("output.png")
    print("📤 Extracted Metadata:")
    print(extracted)
