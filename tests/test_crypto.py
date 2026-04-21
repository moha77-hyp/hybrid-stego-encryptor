import pytest
from core.key_manager import KeyManager
from core.crypto_engine import CryptoEngine

def tet_aes_key_derivation():
    ####
    password = "SuperSecretPassword123!"

    key1, salt1 = KeyManager.derive_aes_key(password)

    assert len(key1) == 32

def test_rsa_key_generation():
    private_pem, public_pem = KeyManager.generate_rsa_keypair()

    assert b"BEGIN PRIVATE KEY" in private_pem
    assert b"BEGIN PUBLIC KEY" in public_pem

def test_full_hybrid_encryption_cycle():

    password = "MySecurePassword"
    aes_key, _ = KeyManager.derive_aes_key(password)
    private_pem, public_pem = KeyManager.generate_rsa_keypair()
    original_data = b"This is top secret file data. Do not share"

    payload = CryptoEngine.hybrid_encrypt(original_data, aes_key, public_pem)

    assert original_data not in payload

    decrypted_data = CryptoEngine.hybrid_decrypt(payload, private_pem)

    assert decrypted_data == original_data

def test_tampered_payload_fails():
    aes_key, _ = KeyManager.derive_aes_key("pass")
    private_pem, public_pem = KeyManager.generate_rsa_keypair()

    payload = CryptoEngine.hybrid_encrypt(b"Data", aes_key, public_pem)

    tamperd_payload = bytearray(payload)
    tamperd_payload[-5] ^= 0xFF

    with pytest.raises(Exception):
        CryptoEngine.hybrid_decrypt(bytes(tamperd_payload), private_pem)