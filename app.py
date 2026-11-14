import base64
import os
from flask import Flask, render_template, request, jsonify
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SUBSTITUTION_KEY = "QWERTYUIOPASDFGHJKLZXCVBNM"

def b64e(data):
    return base64.b64encode(data).decode("ascii")

def b64d(data):
    return base64.b64decode(data, validate=True)

def atbash(text):
    result = []
    for ch in text:
        if ch.isupper() and ch in ALPHABET:
            result.append(ALPHABET[25 - ALPHABET.index(ch)])
        elif ch.islower() and ch.upper() in ALPHABET:
            result.append(ALPHABET[25 - ALPHABET.index(ch.upper())].lower())
        else:
            result.append(ch)
    return "".join(result)

def substitution(text, decrypt=False):
    source = SUBSTITUTION_KEY if decrypt else ALPHABET
    target = ALPHABET if decrypt else SUBSTITUTION_KEY
    table = {}
    for a, b in zip(source, target):
        table[a] = b
        table[a.lower()] = b.lower()
    return "".join(table.get(ch, ch) for ch in text)

def aes_encrypt(plaintext):
    key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext.encode("utf-8"), None)
    return {"ciphertext": b64e(ciphertext), "key": b64e(key), "nonce": b64e(nonce),
            "algorithm": "AES-256-GCM"}

def aes_decrypt(ciphertext, key, nonce):
    cipher_bytes = b64d(ciphertext)
    key_bytes = b64d(key)
    nonce_bytes = b64d(nonce)
    if len(key_bytes) != 32 or len(nonce_bytes) != 12:
        raise ValueError("AES-256 requires a 32-byte key and a 12-byte nonce.")
    return AESGCM(key_bytes).decrypt(nonce_bytes, cipher_bytes, None).decode("utf-8")

def generate_rsa_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode("ascii")
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("ascii")
    return public_pem, private_pem

def rsa_encrypt(plaintext, public_pem):
    public_key = load_pem_public_key(public_pem.encode("utf-8"))
    ciphertext = public_key.encrypt(
        plaintext.encode("utf-8"),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(), label=None)
    )
    return b64e(ciphertext)

def rsa_decrypt(ciphertext, private_pem):
    private_key = load_pem_private_key(private_pem.encode("utf-8"), password=None)
    plaintext = private_key.decrypt(
        b64d(ciphertext),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(), label=None)
    )
    return plaintext.decode("utf-8")

def hybrid_encrypt(plaintext, public_pem):
    # AES encrypts the message; RSA encrypts (wraps) the one-time AES key.
    aes = aes_encrypt(plaintext)
    wrapped_key = rsa_encrypt(base64.b64decode(aes["key"]), public_pem)
    return {"ciphertext": aes["ciphertext"], "nonce": aes["nonce"],
            "encrypted_key": wrapped_key, "algorithm": "Hybrid AES-256-GCM + RSA-OAEP"}


def hybrid_decrypt(ciphertext, nonce, encrypted_key, private_pem):
    private_key = load_pem_private_key(
        private_pem.encode("utf-8"),
        password=None
    )

    # Recover the original AES key as raw bytes
    key = private_key.decrypt(
        b64d(encrypted_key),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Decrypt the message using the recovered AES key
    plaintext = AESGCM(key).decrypt(
        b64d(nonce),
        b64d(ciphertext),
        None
    )

    return plaintext.decode("utf-8")




def integrated_encrypt(plaintext, traditional_method, public_pem):
    """Apply a classical cipher first, then AES-GCM, and protect its key with RSA-OAEP."""
    if traditional_method == "atbash":
        transformed = atbash(plaintext)
    elif traditional_method == "substitution":
        transformed = substitution(plaintext)
    else:
        raise ValueError("Choose Atbash or Substitution as the traditional layer.")

    aes_result = aes_encrypt(transformed)
    raw_aes_key = b64d(aes_result["key"])
    public_key = load_pem_public_key(public_pem.encode("utf-8"))
    wrapped_key = public_key.encrypt(
        raw_aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(), label=None)
    )
    return {
        "ciphertext": aes_result["ciphertext"],
        "nonce": aes_result["nonce"],
        "encrypted_key": b64e(wrapped_key),
        "traditional_method": traditional_method,
        "algorithm": "Integrated: Traditional cipher + AES-256-GCM + RSA-OAEP"
    }

def integrated_decrypt(ciphertext, nonce, encrypted_key, private_pem, traditional_method):
    """Unwrap AES key with RSA, decrypt with AES-GCM, then reverse the classical cipher."""
    private_key = load_pem_private_key(private_pem.encode("utf-8"), password=None)
    raw_aes_key = private_key.decrypt(
        b64d(encrypted_key),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(), label=None)
    )
    transformed = AESGCM(raw_aes_key).decrypt(
        b64d(nonce), b64d(ciphertext), None
    ).decode("utf-8")

    if traditional_method == "atbash":
        return atbash(transformed)
    if traditional_method == "substitution":
        return substitution(transformed, decrypt=True)
    raise ValueError("Choose the same traditional method that was used during encryption.")

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/keys")
def keys():
    public_pem, private_pem = generate_rsa_pair()
    return jsonify(public_key=public_pem, private_key=private_pem)

@app.post("/api/encrypt")
def encrypt():
    data = request.get_json(force=True)
    method = data.get("method", "")
    text = data.get("text", "")
    try:
        if not text:
            raise ValueError("Enter a message first.")
        if method == "atbash":
            result = {"ciphertext": atbash(text), "algorithm": "Atbash Cipher"}
        elif method == "substitution":
            result = {"ciphertext": substitution(text), "algorithm": "Monoalphabetic Substitution Cipher",
                      "key_note": "This demonstration uses a fixed educational alphabet mapping."}
        elif method == "aes":
            result = aes_encrypt(text)
        elif method == "rsa":
            if not data.get("public_key"):
                raise ValueError("Paste an RSA public key or generate a key pair first.")
            result = {"ciphertext": rsa_encrypt(text, data["public_key"]), "algorithm": "RSA-OAEP (SHA-256)"}
        elif method == "hybrid":
            if not data.get("public_key"):
                raise ValueError("Paste an RSA public key or generate a key pair first.")
            result = hybrid_encrypt(text, data["public_key"])
        elif method == "integrated":
            if not data.get("public_key"):
                raise ValueError("Paste an RSA public key or generate a key pair first.")
            result = integrated_encrypt(text, data.get("traditional_method", ""), data["public_key"])
        else:
            raise ValueError("Choose a valid encryption method.")
        return jsonify(ok=True, result=result)
    except Exception as exc:
        return jsonify(ok=False, error=str(exc)), 400

@app.post("/api/decrypt")
def decrypt():
    data = request.get_json(force=True)
    method = data.get("method", "")
    try:
        if method == "atbash":
            plain = atbash(data.get("ciphertext", ""))
        elif method == "substitution":
            plain = substitution(data.get("ciphertext", ""), decrypt=True)
        elif method == "aes":
            plain = aes_decrypt(data["ciphertext"], data["key"], data["nonce"])
        elif method == "rsa":
            plain = rsa_decrypt(data["ciphertext"], data["private_key"])
        elif method == "hybrid":
            plain = hybrid_decrypt(data["ciphertext"], data["nonce"],
                                   data["encrypted_key"], data["private_key"])
        elif method == "integrated":
            plain = integrated_decrypt(data["ciphertext"], data["nonce"],
                                       data["encrypted_key"], data["private_key"],
                                       data.get("traditional_method", ""))
        else:
            raise ValueError("Choose a valid decryption method.")
        return jsonify(ok=True, plaintext=plain)
    except Exception as exc:
        return jsonify(ok=False, error=str(exc)), 400

@app.get("/health")
def health():
    return jsonify(status="ok", application="Traditional and Modern Encryption System")

if __name__ == "__main__":
    app.run(debug=True)
