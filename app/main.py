import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

import streamlit as st
import tempfile
from app.controller import AppController
from core.key_manager import KeyManager

st.set_page_config(
    page_title="Hubrid Stego-Encryptor",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🛡️ Hubrid Stego-Encryptor")
st.markdown("""
**Professional Military-Grade File Hiding Tool.** Secured by **AES-256-GCM** & **RSA-4096** | Powered by **LSB Steganography**
""")
st.divider()

tab_hide, tab_extract, tab_keys = st.tabs([
    "🔒 Encrypt & Hide",
    "🔓 Extract & Decrypt",
    "🔑 Key Management"
])

###key Management

with tab_keys:
    st.header("🔑 Genrate RSA Key Pair")
    st.info("You need an RSA key Pair to use this tool. Generate one here if you don't have it.")

    if st.button("Generate 4096-bit RSA Keys"):
        with st.spinner("Generating Cryptographically secure keys... (This might take a few seconds)"):
            private_pem, public_pem = KeyManager.genrate_rsa_keypair()

            st.success("Key generated successfully! Downlaod and keep your Private key safe.")

            col1, col2 = st.columns(2)
            with col1:
                st.download_button("⬇️ Download Public Key", data=public_pem, file_name="public_key.pem", mime="text/plain")
            with col2:
                st.download_button("⬇️ Download Private Key", data=private_pem, file_name="private_key.pem", mime="text/plain")


##Encrypt and Hide
with tab_hide:
    st.header("🔒 Encrypt and Hide File")

    target_file = st.file_uploader("1. Upload Trget File (Any format)", type=None)
    carrier_image = st.file_uploader("2. Uplaod Carrier Image", type=['png', 'bmp'])
    public_key_file = st.file_uploader("3. Upload Public Key (.pem)", type=["pem"])
    password = st.text_input("4. Master Password (Used for AES generation )", type="password")

    if st.button("Encrypt & Hide 🚀", type="primary"):
        if target_file and carrier_image and public_key_file and password:
            with st.spinner("Encrypting and hiding data..."):
                try:
                    file_bytes = target_file.read()
                    file_name = target_file.name()
                    public_key_pem = public_key_file.read()

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_carrier:
                       temp_carrier.write(carrier_image.read())
                       carrier_path = temp_carrier.name

                    with tempfile.NamedTemporaryFile(delete="False", suffix=".png") as temp_output:
                        output_path = temp_output.name

                    AppController.process_encrypt_and_hide(
                        file_name, file_bytes, carrier_path, password, public_key_pem, output_path
                    )

                    with open(output_path, "rb") as out_file:
                        stego_bytes = out_file.read()

                    st.success("✅ File successfully encrypted and hidden inside the image!")
                    st.download_button(
                        "⬇️ Download Stego-Image",
                        data=stego_bytes,
                        file_name="secure_stego_image.png",
                        mime="image/png"
                    )

                    #clena the server from temp files
                    os.remove(carrier_path)
                    os.remove(output_path)

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

        else:
            st.warning("Please fill all fields and upload requireed files.")

with tab_extract:  
    st.header("🔓 Extract and Decrypt File")

    stego_image = st.file_uploader("1. Upload Stego_Image", type=['png'])
    private_key_file = st.file_uploader("2. Upload Private Key (.pem)", type=['pem'])

    st.info("Note: You do not need the Master Password here. Your private key decrepts the AES key automatic!")

    if st.button("Extract & Decrypt 🔓", type="primary"):
        if stego_image and private_key_file:
            with st.spinner("Extracting and decrypting data..."):
                try:
                    private_key_pem = private_key_file.read()

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_stego:
                        temp_stego.write(stego_image.read())
                        stego_path = temp_stego.name

                    orig_name, orig_bytes = AppController.process_extract_and_decrypt(stego_path, private_key_pem)

                    st.success(f"✅ Success! File '{orig_name}' extracted and decrypted.")
                    st.download_button(
                        f"⬇️Downlaod {orig_name}",
                        data=orig_bytes,
                        file_name=orig_name
                    )

                    os.remove(stego_path)

                except Exception as e:
                    st.error(f"❌ Decryption Faild: {str(e)}")

        else:
            st.warning("⚠️ Please upload image and your private key!")