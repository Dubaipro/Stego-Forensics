import cv2
import numpy as np

def embed_data(image_path, metadata, output_path):
    # Read image
    img = cv2.imread(image_path)
    # Convert metadata to binary
    metadata_bin = ''.join(format(ord(i), '08b') for i in metadata)
    # Embed data in LSB
    idx = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):  # RGB channels
                if idx < len(metadata_bin):
                    img[i][j][k] = (img[i][j][k] & 0xFE) | int(metadata_bin[idx])
                    idx += 1
    # Save image with embedded data
    cv2.imwrite(output_path, img)


def extract_data(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Invalid image file")

        binary_data = ""
        # Extract LSBs until end marker
        end_marker = "11111111"  # Indicates end of metadata
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                for k in range(3):
                    binary_data += str(img[i][j][k] & 1)
                    # Check for end marker every 8 bits
                    if len(binary_data) % 8 == 0:
                        last_byte = binary_data[-8:]
                        if last_byte == end_marker:
                            binary_data = binary_data[:-8]  # Remove end marker
                            raise StopIteration

        # Convert binary to string
        metadata = ""
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i + 8]
            metadata += chr(int(byte, 2))

        return metadata.split('||')  # Use double pipe as delimiter

    except StopIteration:
        return metadata.split('||')
    except Exception as e:
        print(f"Extraction error: {str(e)}")
        return []