# pip install cryptography
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa

def receiver():
    try:
        # Load the receiver's private key
        with open('receiver_private.pem', 'rb') as f:
            receiver_private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )
    except FileNotFoundError:
        print("Error: 'receiver_private.pem' file not found. Please generate the private key first.")
        return

    try:
        # Load the encrypted message
        with open('encrypted_message.bin', 'rb') as f:
            ciphertext = f.read()
    except FileNotFoundError:
        print("Error: 'encrypted_message.bin' file not found. Please make sure the sender has encrypted and saved the message.")
        return

    try:
        # Decrypt the message using RSA private key with OAEP padding
        plaintext = receiver_private_key.decrypt(
            ciphertext,
            OAEP(
                mgf=MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        print("\nDecrypted message:", plaintext.decode())
    except Exception as e:
        print("Decryption failed:", str(e))

if __name__ == "__main__":
    receiver()