import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from core.logger import get_logger

# Initialize logger for RSA events
logger = get_logger("RSAManager")

class RSAManager:
    def __init__(self, private_key_path="private.pem", public_key_path="public.pem"):
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path

    def generate_key_pair(self):
        """
        Generates an RSA Public/Private key pair and saves them as PEM files.
        Skips generation if the keys already exist.
        """
        if os.path.exists(self.private_key_path) and os.path.exists(self.public_key_path):
            logger.info("RSA key pair already exists. Skipping generation.")
            return

        logger.info("Generating new RSA 2048-bit key pair...")
        
        # 1. Generate the Private Key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # 2. Extract the Public Key from the Private Key
        public_key = private_key.public_key()

        # 3. Serialize and save the Private Key (Keep this extremely safe)
        with open(self.private_key_path, "wb") as priv_file:
            priv_file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption() # Unencrypted for automated CI/CD pipelines
                )
            )

        # 4. Serialize and save the Public Key
        with open(self.public_key_path, "wb") as pub_file:
            pub_file.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )
        
        logger.info("RSA key pair generated and saved successfully (.pem).")