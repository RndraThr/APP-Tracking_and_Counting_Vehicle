import hashlib
import os

def hash_password(password: str, salt: bytes = None) -> tuple:
    """
    Menghasilkan hash password dengan SHA-512 dan salt.
    
    Args:
        password (str): Password yang akan di-hash.
        salt (bytes, optional): Salt acak. Jika None, akan dibuat salt baru.

    Returns:
        tuple: (salt dalam hex, hashed password dalam hex)
    """
    if salt is None:
        salt = os.urandom(16)

    hashed = hashlib.sha512(salt + password.encode()).hexdigest()
    return salt.hex(), hashed

def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    """
    Memverifikasi password dengan salt yang diberikan.
    
    Args:
        password (str): Password yang dimasukkan oleh pengguna.
        salt (str): Salt dalam format hex yang disimpan di database.
        stored_hash (str): Hash password yang tersimpan.

    Returns:
        bool: True jika password valid, False jika tidak.
    """
    salt_bytes = bytes.fromhex(salt)
    hashed = hashlib.sha512(salt_bytes + password.encode()).hexdigest()
    return hashed == stored_hash
