from cryptography.hazmat.primitives.asymmetric import ec, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os, secrets

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def load_public_key(pem_bytes):
    """Loads and returns a PEM public key."""
    return serialization.load_pem_public_key(pem_bytes)

# ---------- Key Generation ----------

'''def generate_static_signing_keypair():
    """Generates ECDSA keypair (P-256) for signing."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key, pub_bytes'''


def generate_ephemeral_keypair():
    """Generates ECDSA keypair (P-256) for key exchange."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key, pub_bytes


'''def generate_identity_keypair():
    """Generates ECDSA keypair (P-256) for signing and key exchange."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key, pub_bytes'''

# ---------- Sign & Verify ----------

'''def sign_message(private_key, message_bytes):
    """Signs a message using ECDSA and SHA256."""
    signature = private_key.sign(
        message_bytes,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

def verify_signature(public_key, message_bytes, signature):
    """Verifies an ECDSA signature."""
    try:
        public_key.verify(
            signature,
            message_bytes,
            ec.ECDSA(hashes.SHA256())  # Correct ECDSA signature verification
        )
        return True
    except Exception as e:
        print(f"[!] Signature verification failed: {e}")
        return False'''

# ---------- Key Exchange (ECDH) ----------

def perform_key_exchange(my_private_key, peer_public_pem):
    """Derives shared session key using ECDH and HKDF."""
    peer_public_key = serialization.load_pem_public_key(peer_public_pem)
    shared_secret = my_private_key.exchange(ec.ECDH(), peer_public_key)

    # Use HKDF to derive a symmetric key from the shared secret
    session_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'p2p chat'
    ).derive(shared_secret)

    return session_key  # 32 bytes for AES-256-GCM

# ---------- Encryption / Decryption ----------

def rsa_encrypt(public_key, plaintext):
    return public_key.encrypt(
        plaintext,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

def generate_symmetric_key():
    return AESGCM.generate_key(bit_length=256)

def aesgcm_encrypt(key, plaintext):
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ct = aesgcm.encrypt(nonce, plaintext, associated_data=None)
    return nonce + ct

def aesgcm_decrypt(key, data):
    aesgcm = AESGCM(key)
    nonce = data[:12]
    ciphertext = data[12:]
    return aesgcm.decrypt(nonce, ciphertext, associated_data=None)


