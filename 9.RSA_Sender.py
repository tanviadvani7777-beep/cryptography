# pip install cryptography
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

def sender():
    try:
        # Load receiver's public key
        with open('receiver_public.pem', 'rb') as f:
            receiver_public_key = serialization.load_pem_public_key(f.read())
    except FileNotFoundError:
        print("Error: 'receiver_public.pem' file not found. Run key generation first.")
        return

    # Take input message from user
    message = input("Enter the message to encrypt and send: ").encode()

    try:
        # Encrypt message using RSA public key and OAEP padding
        ciphertext = receiver_public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Save encrypted message to file
        with open('encrypted_message.bin', 'wb') as f:
            f.write(ciphertext)

        print("Message encrypted and saved as 'encrypted_message.bin'.")
    except Exception as e:
        print("Encryption failed:", str(e))

if __name__ == "__main__":
    sender()