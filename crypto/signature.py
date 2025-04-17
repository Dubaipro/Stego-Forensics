from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def sign_message(private_key_path, message):
    try:
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(), password=None, backend=default_backend()
            )

        signature = private_key.sign(
            message.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return signature
    except Exception as e:
        print(f"Error in signing: {e}")
        return None

def verify_signature(public_key_path, message, signature):
    try:
        with open(public_key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(), backend=default_backend()
            )

        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Verification error: {e}")
        return False

if __name__ == "__main__":
    message = "Case ID:1234; Timestamp:2025-03-22; Chain:CustodyA->CustodyB;"
    print("Starting signature process...")

    signature = sign_message("../keys/private.pem", message)
    if signature:
        print("Generated Signature (hex):", signature.hex())
    else:
        print("Failed to generate signature.")
        exit(1)

    print("Starting verification process...")
    valid = verify_signature("../keys/public.pem", message, signature)

    if valid:
        print("Signature verification PASSED.")
    else:
        print("Signature verification FAILED.")
