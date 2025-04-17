import cv2

def message_to_binary(message):
    if isinstance(message, str):
        return ''.join([format(ord(char), "08b") for char in message])
    else:
        raise TypeError("Message must be a string")

def embed_data(image_path, output_path, secret_data):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found. Check the path carefully!")

    binary_data = message_to_binary(secret_data)
    binary_data += '1111111111111110'  # End-of-data delimiter

    data_index = 0
    data_len = len(binary_data)

    for row in image:
        for pixel in row:
            r, g, b = [format(color, "08b") for color in pixel]

            if data_index < data_len:
                pixel[0] = int(r[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[1] = int(g[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[2] = int(b[:-1] + binary_data[data_index], 2)
                data_index += 1

            if data_index >= data_len:
                break
        if data_index >= data_len:
            break

    cv2.imwrite(output_path, image)

if __name__ == "__main__":
    msg = """Case ID: 1234
Investigator: John Doe
Timestamp: 2025-04-07 22:00:00
Chain of Custody: Officer A → Officer B
Metadata: Image of the crime scene"""
    embed_data("input.jpg", "output.png", msg)
    print("✅ Embedding successful.")
