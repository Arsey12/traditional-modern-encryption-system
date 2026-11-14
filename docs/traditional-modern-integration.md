# Integration of Traditional and Modern Encryption Methods

## Purpose

The central feature of this project is a workflow that combines a traditional cipher with modern cryptographic algorithms.

## Encryption sequence

1. The user enters plaintext.
2. The user selects Atbash or Substitution Cipher.
3. The selected traditional cipher transforms the message.
4. AES-256-GCM encrypts the transformed message with a newly generated secret key and nonce.
5. RSA-OAEP encrypts the AES key using the recipient's public key.
6. The application returns the AES ciphertext, nonce, and RSA-encrypted AES key.

## Decryption sequence

1. The recipient supplies the ciphertext, nonce, RSA-encrypted AES key, and private key.
2. RSA-OAEP uses the private key to recover the AES key.
3. AES-256-GCM authenticates and decrypts the ciphertext.
4. The recipient applies the reverse of the original traditional cipher.
5. The original plaintext is recovered.

## Important security explanation

This design integrates historical and modern techniques for demonstration. The security comes from correctly used AES-GCM and RSA-OAEP. Atbash and monoalphabetic substitution are weak historical ciphers and must not be represented as adding modern cryptographic strength.
