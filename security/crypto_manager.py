import bcrypt
from core.logger import get_logger

# Initialize structured logging for security events
logger = get_logger("CryptoManager")

class CryptoManager:
    def __init__(self):
        logger.info("CryptoManager initialized with native bcrypt schema.")

    def hash_password(self, password: str) -> str:
        """
        Transforms a plain text password into a secure cryptographic hash.
        """
        # bcrypt requires bytes, so we encode the string
        pwd_bytes = password.encode('utf-8')
        
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
        
        logger.debug("Password hashed successfully.")
        
        # Return as a string to allow easy storage in PostgreSQL later
        return hashed_bytes.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifies if an incoming plain text password matches the stored cryptographic hash.
        """
        # Convert both the plain text and the stored hash back to bytes
        pwd_bytes = plain_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        
        # Check against the hash
        is_valid = bcrypt.checkpw(pwd_bytes, hash_bytes)
        
        if is_valid:
            logger.info("Password verification successful.")
        else:
            logger.warning("Password verification failed: Unauthorized access attempt.")
            
        return is_valid