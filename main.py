from security.crypto_manager import CryptoManager
from security.rsa_manager import RSAManager
from core.logger import get_logger
from core.config import settings

logger = get_logger("MainApp")

def run_security_test():
    logger.info("Starting production-grade security engine test...")
    
    # 1. Test Configuration Loader
    print(f"\n--- System Info ---")
    print(f"App Name: {settings.PROJECT_NAME}")
    print(f"Loaded Secret Key: {settings.SECRET_KEY}")
    print(f"-------------------\n")
    
    # 2. Test Cryptography (bcrypt)
    crypto = CryptoManager()
    test_password = "SuperSecretPassword123!"
    
    hashed_pwd = crypto.hash_password(test_password)
    print(f"Original: {test_password}")
    print(f"Hashed: {hashed_pwd}\n")
    
    print("--- Running Verification Checkpoints ---")
    crypto.verify_password("SuperSecretPassword123!", hashed_pwd)
    crypto.verify_password("WrongPassword!", hashed_pwd)
    
    # 3. Test RSA Generation
    print("\n--- Running RSA Key Generation ---")
    rsa_engine = RSAManager()
    rsa_engine.generate_key_pair()
    
    logger.info("Security engine test pipeline completed.")

if __name__ == "__main__":
    run_security_test()