# System Design

## Architecture

```mermaid
flowchart TD
    U[User] --> UI[Web interface: HTML, CSS and JavaScript]
    UI --> API[Flask application]
    API --> T[Traditional cipher module]
    API --> A[AES-256-GCM]
    API --> R[RSA-OAEP]
    A --> H[Hybrid encryption workflow]
    R --> H
    T --> OUT[Ciphertext / plaintext result]
    A --> OUT
    R --> OUT
    H --> OUT
    OUT --> UI
```

## Data flow

1. The user selects an encryption method.
2. The user enters plaintext and, when required, a public key.
3. JavaScript sends the request to the Flask backend.
4. The backend validates the request and performs the selected operation.
5. The backend returns the result as JSON.
6. The browser displays the ciphertext or decrypted plaintext.

## Integration logic

The application provides one interface and a common request/response structure for all algorithms. The selected algorithm determines which cryptographic operation is performed. The traditional methods operate on characters, AES-GCM operates on message bytes using a shared secret, and RSA-OAEP uses a public/private key pair. Hybrid encryption combines AES-GCM and RSA-OAEP by encrypting the message with AES and wrapping the AES key with RSA.


## Traditional and modern integration sequence

```mermaid
flowchart LR
    P[Original plaintext] --> C[Atbash or Substitution]
    C --> A[AES-256-GCM encryption]
    A --> K[RSA-OAEP encrypts AES key]
    A --> CT[Ciphertext + nonce]
    K --> EK[Encrypted AES key]
    CT --> R[Recipient]
    EK --> R
    R --> D[RSA private key recovers AES key]
    D --> G[AES-GCM decrypts ciphertext]
    G --> RC[Reverse selected classical cipher]
    RC --> O[Original plaintext]
```

The classical cipher must be reversed only after AES decryption. The order matters because decryption reverses the encryption sequence.
