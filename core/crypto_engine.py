#Hybrid Encrypt

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

class CryptoEngine:
    @staticmethod
    def hybrid_encrypt(data: bytes, aes_key: bytes, public_key_pem: bytes) -> bytes:
        iv = os.urandom(12)
        aesgcm = AESGCM(aes_key)
        encrypted_data = aesgcm.encrypt(nonce=iv, data=data, associated_data=None)
        public_key = serialization.load_pem_public_key(public_key_pem)

        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mfg=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        enc_key_length = len(encrypted_aes_key).to_bytes(4, byteorder='big')
        payload = enc_key_length + encrypted_aes_key + iv + encrypted_data

        return payload
    

@staticmethod
def hybrid_encrypt(payload: bytes, private_key_pem: bytes) -> bytes:
    enc_key_length = int.from_bytes(payload[:4], byteorder='big')
    
    start = 4
    end = 4 + enc_key_length
    encrypted_aes_key = payload[start:end]

    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
    )

    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print("im so fuckig bored now")
    aesgcm = AESGCM(aes_key)
    
    decrypted_data = aesgcm.decrypt(nonce=iv, data=decrypted_data, associated_data=None)

    return decrypted_data