import os
import urllib.parse
from typing import Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(password) -> str:
    """
    Hashes a plain text password using bcrypt.
    Args:
        password: The plain text password to hash
    Returns:
        The hashed password as a string
    """
    return pwd_context.hash(password)

def verify_password(plain, hashed) -> bool:
    """
    Verifies a plain text password against a hashed password.
    Args:
        plain: The plain text password to verify
        hashed: The hashed password to compare against
    Returns:
        True if the plain text password matches the hashed password, False otherwise
    """
    return pwd_context.verify(plain, hashed)

def validate_static_file_path(path: str, base_directory: str = "static") -> Optional[str]:
    """
    Validates and sanitizes a file path to prevent directory traversal attacks.
    
    Args:
        path: The requested file path
        base_directory: The base directory to serve files from
        
    Returns:
        Validated file path if safe and exists, None otherwise
    """
    if not path:
        return None
    
    try:
        # URL decode to catch encoded attacks (%2e%2e%2f -> ../)
        decoded_path = urllib.parse.unquote(path)
        
        # Check for various directory traversal patterns
        dangerous_patterns = ["..", "\\", "%2e", "%2f", "%5c", "~", "//"]
        if any(pattern in decoded_path.lower() for pattern in dangerous_patterns):
            return None
        
        # Normalize and validate path
        static_file_path = os.path.normpath(os.path.join(base_directory, decoded_path))
        resolved_path = os.path.abspath(static_file_path)
        base_dir = os.path.abspath(base_directory)
        
        # Ensure path is within base directory and file exists
        if (resolved_path.startswith(base_dir + os.sep) and 
            os.path.exists(static_file_path) and 
            os.path.isfile(static_file_path)):
            return static_file_path
            
    except (ValueError, OSError):
        pass
    
    return None

