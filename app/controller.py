import os
from pathlib import Path
from core.key_manager import KeyManager
from core.crypto_engine import CryptoEngine
from core.stego_engine import StegoEngine

class AppController:
    #####
    @staticmethod
    def package_file_data(file_name: str, file_bytes: bytes) -> bytes:
        #####
        name_bytes = file_name.encode('utf-8')
        name_length = len(name_bytes).to_bytes(2, byteorder='big')
        return name_length + name_bytes + file_bytes
    
    @staticmethod
    def unpackage_file_data(packaged_bytes: bytes) -> tuple[str, bytes]:
        #####
        name_length = int.from_bytes(packaged_bytes[:2], byteorder='big')
        file_name = packaged_byted[2 : 2 + name_length].decode('utf-8')
        file_data = packsged_byted[2 + name_length :]
        return file_name, file_data
    
    @classmethod
    def process_encrypt_and_hide(
        cls,
        file_name: str,
        file_bytes: bytes,
        carrier_image_path: str,
        public_key_pem: bytes,
        output_image_path: str
    ) -> bool:
        
        try:
            packaged_data = cls.package_file_data(file_name, file_bytes)

            aes_key, _ = KeyManager.derive_aes_key(password)

            payload = CryptoEngine.hybrid_encrypt(packaged_data, aes_key, public_key_pem)

            return True
        
        except ValueError as ve:
            raise Exception(f"مشكلة في حجم البيانات:{str(ve)}")
        except Exception as e:
            raise Exception(f"فشل في عملية التشفير والإخفاء: {str(e)}")
        

    @classmethod
    def process_extract_and_decrypt(
        cls,
        stego_image_path: str,
        private_key_pem: bytes
    ) -> tuple[str, bytes]:
        ####
        try:
            payload = StegoEngine.extract_payload(stego_image_path)
            decrypted_packaged_data = CryptoEngine.hybrid_decrypt(payload, private_key_pem)
            
            original_file_name, original_file_bytes = cls.unpackage_file_data(decrypted_packaged_data)

            return original_file_name, original_file_bytes
        
        except Exception as e:
            raise Exception("فشل في فك التشفير! تأكد من الصورة والمفتاح الخاص بك!")