# Project Report: Traditional and Modern Encryption System

## 1. Introduction

Encryption is a process of transforming readable information (plaintext) into an unreadable form (ciphertext) so that only an authorised party with the appropriate key or method can recover the original information. Encryption is an important part of cybersecurity because it helps protect the confidentiality of information during storage and transmission.

This project demonstrates the integration of traditional and modern encryption techniques through a web-based application developed with Python and Flask.

## 2. Aim and Objectives

The aim is to develop an educational application that demonstrates traditional and modern encryption methods in one interface.

The objectives are to:
1. Explain and implement the Atbash cipher.
2. Explain and implement a monoalphabetic substitution cipher.
3. Implement AES-256-GCM symmetric encryption and decryption.
4. Implement RSA-OAEP asymmetric encryption and decryption.
5. Demonstrate hybrid encryption by combining AES and RSA.
6. Provide a simple interface for users to encrypt and decrypt messages.
7. Compare the strengths and limitations of the selected methods.

## 3. Traditional Encryption Methods

### Atbash Cipher

Atbash is a historical substitution cipher in which the alphabet is reversed. A is replaced by Z, B by Y, C by X, and so on. The process is reciprocal, meaning the same operation encrypts and decrypts a message.

### Monoalphabetic Substitution Cipher

A substitution cipher replaces each letter with another letter according to a fixed mapping. In this project, a fixed scrambled alphabet is used as the demonstration key. The reverse mapping is applied during decryption.

Traditional substitution ciphers are not suitable for modern confidentiality because patterns and letter frequencies can reveal the original message.

## 4. Modern Encryption Methods

### AES-256-GCM

Advanced Encryption Standard (AES) is a symmetric encryption algorithm. It uses the same secret key for encryption and decryption. This project uses a 256-bit key and Galois/Counter Mode (GCM), which provides confidentiality and authentication. A fresh random nonce is generated for each encryption operation.

### RSA-OAEP

RSA is an asymmetric cryptographic algorithm that uses a public key and a private key. The public key can be shared and is used to encrypt; the matching private key is kept secret and is used to decrypt. This project uses RSA with OAEP padding and SHA-256.

### Hybrid Encryption

Hybrid encryption combines the strengths of symmetric and asymmetric cryptography. AES-GCM encrypts the actual message because it is efficient for data. RSA-OAEP encrypts the randomly generated AES key. The recipient uses their RSA private key to recover the AES key and then decrypts the message.

## 5. Integration of Traditional and Modern Methods

The application includes a dedicated integration mode. The user chooses Atbash or the substitution cipher as the first layer. The output of that classical transformation is then encrypted using AES-256-GCM. The AES key is protected using RSA-OAEP and the recipient's RSA public key.

The decryption process reverses the sequence: the RSA private key recovers the AES key, AES-GCM decrypts the transformed message, and the selected classical cipher is reversed to recover the original plaintext.

This sequence demonstrates the integration of traditional and modern methods in one workflow. The traditional cipher is included for educational comparison; it does not provide meaningful additional security when used with modern encryption.

## 6. System Implementation

The backend is written in Python using Flask. The browser interface is built with HTML, CSS and JavaScript. The `cryptography` Python package provides the modern cryptographic primitives.

The application accepts a message and a selected method. It returns ciphertext and, where necessary, the information required for decryption. The application does not intentionally save messages or keys to a database.

## 7. Benefits

- Makes the differences between classical and modern encryption easier to understand.
- Places several algorithms in one interface.
- Demonstrates both symmetric and asymmetric encryption.
- Shows a practical reason for combining AES and RSA.
- Provides an expandable foundation for further cybersecurity learning.

## 8. Limitations

- The traditional ciphers are educational and insecure.
- The demonstration does not include user accounts or a persistent database.
- Private-key handling is simplified and is not appropriate for production.
- Direct RSA encryption can only handle short messages.
- The application has not been independently security-audited.

## 9. Conclusion

The project demonstrates the development of encryption from simple alphabet substitution to modern cryptographic algorithms. Atbash and substitution ciphers are useful for understanding the basic concept of encryption, while AES-GCM and RSA-OAEP provide stronger modern techniques. The hybrid option illustrates how symmetric and asymmetric cryptography can work together in a practical design.

## 10. Future Improvements

Possible improvements include secure user authentication, encrypted key storage, digital signatures, file encryption, audit logging, role-based access control, and deployment behind HTTPS after a proper security review.
