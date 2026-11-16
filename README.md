# Traditional and Modern Encryption System

A Flask-based educational web application that demonstrates two traditional encryption techniques and modern cryptographic algorithms in one interface.

## Features

- **Atbash Cipher:** reverses letters across the alphabet.
- **Monoalphabetic Substitution Cipher:** maps each letter to a fixed substitute.
- **AES-256-GCM:** authenticated symmetric encryption.
- **RSA-OAEP (SHA-256):** asymmetric encryption for short messages.
- **Modern hybrid encryption:** AES-GCM encrypts the message while RSA-OAEP protects the AES key.
- **Traditional + modern integration:** Atbash or Substitution is applied first, then AES-GCM encrypts the result and RSA-OAEP protects the AES key.
- RSA key-pair generation in the browser interface.
- Encrypt and decrypt functions with a responsive web interface.

## Requirements

- Python 3.10 or newer
- pip
- Internet access only to install the required Python packages

## Installation

```bash
git clone https://github.com/Arsey12/traditional-modern-encryption-system.git
cd traditional-modern-encryption-system

python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## How to use

1. Select one of the five methods.
2. Enter a message.
3. For RSA or Hybrid, generate a key pair or paste a valid RSA public key.
4. Click **Encrypt message**.
5. Keep the ciphertext and any required key/nonce values.
6. Paste the ciphertext into the decryption area and provide the required key material.
7. Click **Decrypt message**.

## Method comparison

| Method | Type | Key approach | Intended lesson |
|---|---|---|---|
| Atbash | Traditional | No secret key | Alphabet reversal |
| Substitution | Traditional | Fixed mapping | Monoalphabetic substitution |
| AES-256-GCM | Modern | Shared secret key | Symmetric authenticated encryption |
| RSA-OAEP | Modern | Public/private key pair | Asymmetric encryption |
| Modern Hybrid | Combined modern | RSA protects AES key | Practical combination of symmetric and asymmetric cryptography |
| Traditional + Modern Integration | Integrated | Classical cipher, AES key, RSA key pair | Demonstrates a classical transformation inside a modern encryption workflow |

## Security notes

- Atbash and simple substitution are historical teaching examples, not secure encryption.
- AES-GCM keys and nonces are essential for decryption. Never reuse a nonce with the same AES-GCM key.
- RSA-OAEP is used with SHA-256 and a 2048-bit key. Direct RSA encryption has a strict message-size limit; use the Hybrid option for longer messages.
- This demo generates unencrypted private keys for learning. Do not use it to protect real confidential information.
- Do not publish private keys, AES keys, passwords, or real user data in GitHub.
- For production deployment, disable Flask debug mode, use HTTPS, add authentication/authorization if needed, protect keys with a secure key-management service, add rate limiting, and conduct a security review.

## Project structure

```text
traditional-modern-encryption-system/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
├── docs/
│   ├── project-report.md
│   ├── system-design.md
│   └── test-cases.md
├── tests/
│   └── test_ciphers.py
└── images/
    └── system-architecture.png
```

## Academic purpose

This project illustrates how classical letter-based techniques differ from modern cryptographic systems. It also demonstrates why modern applications commonly combine symmetric encryption for data with asymmetric cryptography for key exchange or key protection.

## Author
CYB301 GROUP3
