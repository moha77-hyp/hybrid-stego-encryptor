import streamlit as st
import tempfile
import os
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

            et.success("Key generated successfully! Downlaod and keep your Private key safe.")

            col1, col2 = st.columns(2)
            with col1:
                st.download_button("⬇️ Download Public Key", data=public_pem, file_name="public_key.pem", mime="text/plain")
            with col2:
                st.download_button("⬇️ Download Private Key", data=private_pem, file_name="private_key.pem", mime="text/plain")