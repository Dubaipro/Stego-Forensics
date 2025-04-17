import cv2
from embedding.embed import embed_data
from embedding.extract import extract_data
from crypto.signature import sign_message, verify_signature

# Paths
original_image = "images/input_images/original.jpg"
embedded_image = "images/output_images/embedded.png"
private_key = "keys/private.pem"
public_key = "keys/public.pem"

# Metadata (your forensic data)
metadata = "Case ID:1234; Timestamp:2025-03-22; Chain:CustodyA->CustodyB;"

# STEP 1: Embed metadata into the image
print("[1] Embedding metadata...")
embed_data(original_image, embedded_image, metadata)
print("✅ Metadata embedded into image.\n")

# STEP 2: Extract metadata from image
print("[2] Extracting metadata...")
extracted_metadata = extract_data(embedded_image)
print(f"✅ Extracted metadata: {extracted_metadata}\n")

# STEP 3: Digitally sign extracted metadata
print("[3] Signing metadata...")
signature = sign_message(private_key, extracted_metadata)
print(f"✅ Signature (hex): {signature.hex()}\n")

# STEP 4: Verify the digital signature
print("[4] Verifying signature...")
is_valid = verify_signature(public_key, extracted_metadata, signature)

if is_valid:
    print("✅ Signature verification successful! The data is authentic and unmodified.")
else:
    print("❌ Signature verification FAILED! The data integrity is compromised.")
