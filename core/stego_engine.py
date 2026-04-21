import numpy as np
from PIL import Image

class StegoEngine:
    @staticmethod
    def hide_payload(image_path: str, payload: bytes, output_path: str):
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)

        payload_length = len(payload).to_bytes(4, byteorder='big')
        full_data = payload_length + payload

        data_array = np.frombuffer(full_data, dtype=np.uint8)
        high_nibbles = data_array >> 4
        low_nibbles = data_array & 0x0F

        nibbles = np.empty(len(data_array) * 2, dtype=np.uint8)
        nibbles[0::2] = high_nibbles
        nibbles[1::2] = low_nibbles

        flat_img = img_array.flatten()
        if len(nibbles) > len(flat_img):
            raise ValueError(f"حجم الملف كبير جداً! الصورة تتحمل {len(flat_img)//2} بايت، والملف حجمه {len(full_data)} بايت.")
        
        flat_img[:len(nibbles)] = (flat_img[:len(nibbles)] & 0xF0) | nibbles

        stego_img_array = flat_img.reshape(img_array.shape)
        stego_img = Image.fromarray(stego_img_array, 'RGB')
        stego_img.save(output_path, format='PNG')


    @staticmethod
    def extract_payload(image_path: str) -> bytes:
        ######
        img = Image.open(image_path).convert('RGB')
        flat_img = np.array(img).flatten()

        length_nibbles = flat_img[:8] & 0x0F

        length_bytes = (length_nibbles[0::2] << 4) | length_nibbles[1::2]
        payload_length = int.from_bytes(bytes(length_bytes), byteorder='big')
        
        total_nibbles = payload_length * 2

        payload_nibbles = flat_img[8 : 8 + total_nibbles] & 0x0F

        payload_bytes = (payload_nibbles[0::2] << 4) | payload_nibbles[1::2]

        return bytes(payload_bytes)